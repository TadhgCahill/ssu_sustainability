import pandas as pd
import re

class SensorReport:
    """
    A class to load sensor data from a CSV, perform initial cleaning, and transform
    it into a database-ready format. This version is more robust at finding the
    timestamp column.
    """
    def __init__(self, csv_path):
        df = pd.read_csv(csv_path, low_memory=False)
        
        # *** KEY FIX: Search for multiple possible timestamp column names ***
        timestamp_col_found = None
        possible_ts_names = ['Timestamp', 'timestamp', 'Date/Time', 'Time', 'Date Time']
        
        for name in possible_ts_names:
            if name in df.columns:
                timestamp_col_found = name
                break # Stop as soon as we find one

        if timestamp_col_found:
            # A valid timestamp column was found, so we process it.
            df[['timestamp', 'timezone']] = df[timestamp_col_found].astype(str).str.split(n=1, pat=' ', expand=True)
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce').dt.tz_localize(None)
            df.set_index('timestamp', inplace=True)
            df.drop(columns=[timestamp_col_found, 'timezone'], inplace=True, errors='ignore')

        self.units = {}
        for col in df.columns:
            series = df[col]
            if series.dtype == object:
                numeric = pd.to_numeric(series.str.extract(r'([-+]?[0-9]*\.?[0-9]+)')[0], errors='coerce')
                unit_match = series.str.extract(r'([A-Za-z]+)$')[0]
                unit = unit_match.dropna().iloc[0] if not unit_match.dropna().empty else None
                self.units[col] = unit
                df[col] = numeric
            else:
                lname = col.lower()
                if 'electric' in lname or 'kw' in lname:
                    self.units[col] = 'kWh'
                elif 'gas' in lname or 'btu' in lname:
                    self.units[col] = 'BTU'
                else:
                    self.units[col] = None
        self.df = df

    def to_db_format(self):
        if self.df.empty:
            return pd.DataFrame(columns=['time_stamp', 'location', 'energy_usage', 'electric_or_gas'])

        df_to_melt = self.df.reset_index()

        if 'timestamp' not in df_to_melt.columns:
            raise ValueError("File does not contain a recognizable timestamp column (e.g., 'Timestamp', 'date/time').")

        melted_df = df_to_melt.melt(
            id_vars=['timestamp'],
            var_name='location_raw',
            value_name='energy_usage'
        )

        melted_df.dropna(subset=['energy_usage'], inplace=True)
        if melted_df.empty:
             return pd.DataFrame(columns=['time_stamp', 'location', 'energy_usage', 'electric_or_gas'])

        def get_energy_type(col_name):
            unit = self.units.get(col_name)
            if unit:
                unit_lower = unit.lower()
                if unit_lower in ['kwh', 'kw']: return 'electric'
                if unit_lower in ['btu', 'therm']: return 'gas'
            col_name_lower = str(col_name).lower()
            if 'gas' in col_name_lower: return 'gas'
            if 'electric' in col_name_lower: return 'electric'
            return 'unknown'

        def clean_location_name(raw_name):
            keywords = ['Electric', 'Gas', 'BTU', 'kWh', 'kW']
            pattern = r'[\s_]*(' + '|'.join(keywords) + r')$'
            cleaned_name = re.sub(pattern, '', raw_name, flags=re.IGNORECASE)
            return cleaned_name.strip()

        melted_df['electric_or_gas'] = melted_df['location_raw'].apply(get_energy_type)
        melted_df['location'] = melted_df['location_raw'].apply(clean_location_name)
        melted_df.rename(columns={'timestamp': 'time_stamp'}, inplace=True)
        
        final_df = melted_df[['time_stamp', 'location', 'energy_usage', 'electric_or_gas']]

        return final_df.copy()

    def to_dataframe(self):
        return self.df.copy()