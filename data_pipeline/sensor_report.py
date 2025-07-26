# data_pipeline/sensor_report.py

import pandas as pd
import re

class SensorReport:
    """
    A class to load sensor data from a CSV, identify its format, perform cleaning,
    and transform it into a database-ready format.
    """
    def __init__(self, csv_path):
        """Loads the raw CSV into a pandas DataFrame."""
        # Use low_memory=False to prevent type inference issues with mixed data
        self.df = pd.read_csv(csv_path, low_memory=False)
        self.raw_df = self.df.copy() # Keep a copy of the original for inspection

    def _sanitize_energy_usage(self):
        """
        Processes standard interval meter reports.
        This format has a timestamp column and multiple location columns.
        """
        df = self.raw_df.copy()
        
        # 1. Find and format the timestamp column
        ts_col = df.columns[0]
        # Remove timezone info and convert to datetime objects
        df[ts_col] = df[ts_col].astype(str).str.split(n=1, pat=' ', expand=True)[0]
        df[ts_col] = pd.to_datetime(df[ts_col], errors='coerce')
        df.rename(columns={ts_col: 'time_stamp'}, inplace=True)
        
        # 2. Melt the DataFrame from wide to long format
        melted_df = df.melt(
            id_vars=['time_stamp'],
            var_name='location_raw',
            value_name='energy_usage_raw'
        )
        
        # 3. Clean up the melted data
        melted_df.dropna(subset=['energy_usage_raw'], inplace=True)
        if melted_df.empty:
            return pd.DataFrame() # Return empty if no data

        # 4. Extract numeric values and units
        # This regex handles numbers, including decimals, and the text that follows.
        extracted_data = melted_df['energy_usage_raw'].astype(str).str.extract(r'([-\d.]+)\s*([a-zA-Z]+)?')
        melted_df['energy_usage'] = pd.to_numeric(extracted_data[0], errors='coerce')
        melted_df['unit'] = extracted_data[1].str.lower()
        
        # 5. Unit conversion and type classification
        mbtu_to_kwh = 293.071
        btu_to_kwh = 0.000293071
        tonref_to_kwh = 3.51685
        
        def classify_and_convert(row):
            unit = row['unit']
            value = row['energy_usage']
            
            # GAS types (flag = 1)
            if unit in ['btu', 'mbtu', 'therm']:
                electric_or_gas = 1
                if unit == 'btu': value *= btu_to_kwh
                elif unit == 'mbtu': value *= mbtu_to_kwh
                return value, electric_or_gas
            
            # ELECTRIC types (flag = 0)
            elif unit in ['kwh', 'kw', 'tonref']:
                electric_or_gas = 0
                if unit == 'tonref': value *= tonref_to_kwh
                return value, electric_or_gas
            
            # If unit is missing, infer from column name
            else:
                if 'gas' in str(row['location_raw']).lower():
                    return value, 1 # Gas
                return value, 0 # Default to Electric

        melted_df[['energy_usage', 'electric_or_gas']] = melted_df.apply(
            classify_and_convert, axis=1, result_type='expand'
        )

        # 6. Clean location names
        melted_df['location'] = melted_df['location_raw'].str.split('/').str[0].str.strip()

        # 7. Finalize the DataFrame
        final_df = melted_df[['time_stamp', 'location', 'energy_usage', 'electric_or_gas']].copy()
        final_df.dropna(subset=['time_stamp', 'energy_usage'], inplace=True)
        
        return final_df

    def _sanitize_degree_days(self):
        """
        Processes heating/cooling degree day reports.
        This format has 'heating' and 'cooling' columns.
        """
        df = self.raw_df.copy()
        
        # 1. Find and format the timestamp column
        ts_col = df.columns[0]
        df[ts_col] = df[ts_col].astype(str).str.split(n=1, pat=' ', expand=True)[0]
        df[ts_col] = pd.to_datetime(df[ts_col], errors='coerce')
        df.rename(columns={ts_col: 'time_stamp'}, inplace=True)

        # 2. Identify heating and cooling columns
        heating_col = df.columns[1]
        cooling_col = df.columns[2]

        # 3. Extract just the numbers from the columns
        df['heating_usage'] = df[heating_col].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)
        df['cooling_usage'] = df[cooling_col].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)
        
        # 4. Finalize the DataFrame
        final_df = df[['time_stamp', 'heating_usage', 'cooling_usage']].copy()
        final_df.dropna(subset=['time_stamp'], inplace=True)

        return final_df

    def to_db_format(self):
        """
        Identifies the file type and calls the appropriate sanitization method.
        Returns a tuple of (DataFrame, target_table_name).
        """
        cols = {str(c).lower() for c in self.df.columns}

        # --- Logic to identify file type ---
        # NOTE: This uses column names from the *raw* file before any cleaning.
        if 'heating degree days' in cols and 'cooling degree days' in cols:
            # This is a degree day file
            print("  -> Identified as Degree Day Report. Sanitizing...")
            sanitized_df = self._sanitize_degree_days()
            return sanitized_df, 'temp_daily'
        
        elif len(cols) > 3: # Heuristic: energy usage files have many location columns
            # This is a standard energy usage file
            print("  -> Identified as Energy Usage Report. Sanitizing...")
            sanitized_df = self._sanitize_energy_usage()
            return sanitized_df, 'energy_usage'
            
        else:
            # Unrecognized format
            print(f"  -> WARNING: Unrecognized file format with columns: {list(self.df.columns)}. Skipping.")
            return pd.DataFrame(), None