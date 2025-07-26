# dashboard/data/csv_source.py

import pandas as pd
import os
import sys
from sqlalchemy import create_engine
from .sql_credentials import SQL_CREDENTIALS

# --- IMPORTANT!!! ---
# Set this to True to use the local test DB, False to use the live production DB.
USE_LOCAL_DB_FOR_DASHBOARD = True

print("=" * 50)
print("Dashboard Data Source Configuration")

engine = None
df_energy = pd.DataFrame()
df_temp = pd.DataFrame()

if USE_LOCAL_DB_FOR_DASHBOARD:
    project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    db_path = os.path.join(project_root_dir, 'database', 'local_test_db.sqlite')
    print(f"Mode: Local SQLite Database")
    print(f"Path: {db_path}")
    if not os.path.exists(db_path):
        print("\nWARNING: local_test_db.sqlite not found! The dashboard will start with empty data.")
    else:
        engine = create_engine(f'sqlite:///{db_path}')
else:
    print("Mode: Production MySQL Database")
    try:
        conn_str = (
            f"mysql+pymysql://{SQL_CREDENTIALS['user']}:{SQL_CREDENTIALS['password']}"
            f"@{SQL_CREDENTIALS['host']}:{SQL_CREDENTIALS['port']}/{SQL_CREDENTIALS['database']}"
        )
        engine = create_engine(conn_str)
    except Exception as e:
        print(f"FATAL ERROR: Could not create MySQL engine: {e}")
        sys.exit(1)

print("=" * 50)

# --- Load data from both tables ---
if engine:
    try:
        print("Loading data from 'energy_usage' table...")
        df_energy = pd.read_sql_table('energy_usage', engine)
        print(f"✓ Successfully loaded {len(df_energy)} rows from 'energy_usage'.")
    except Exception as e:
        print(f"✗ Failed to load data from 'energy_usage' table: {e}")

    try:
        print("Loading data from 'temp_daily' table...")
        df_temp = pd.read_sql_table('temp_daily', engine)
        print(f"✓ Successfully loaded {len(df_temp)} rows from 'temp_daily'.")
    except Exception as e:
        print(f"✗ Failed to load data from 'temp_daily' table: {e}")


# --- UNIFY DATA SOURCES INTO A SINGLE DATAFRAME ---
all_dfs = []

# Process energy data
if not df_energy.empty:
    df_energy['unit'] = df_energy['electric_or_gas'].apply(lambda x: 'Gas (kWh)' if x == 1 else 'Electric (kWh)')
    all_dfs.append(df_energy[['time_stamp', 'location', 'energy_usage', 'unit']])

# Process and reshape temperature data
if not df_temp.empty:
    # Melt the dataframe to turn 'heating_usage' and 'cooling_usage' columns into rows
    df_temp_melted = df_temp.melt(
        id_vars=['time_stamp'],
        value_vars=['heating_usage', 'cooling_usage'],
        var_name='unit',
        value_name='energy_usage'
    )
    # Assign a generic location since this is campus-wide data
    df_temp_melted['location'] = 'Campus Wide'
    all_dfs.append(df_temp_melted)

# Combine into the final dataframe 'df'
if all_dfs:
    df = pd.concat(all_dfs, ignore_index=True)
    print(f"✓ Combined data sources into a single DataFrame with {len(df)} total rows.")
else:
    df = pd.DataFrame()

# --- Final Post-Processing on the unified DataFrame ---
if not df.empty:
    df['time_stamp'] = pd.to_datetime(df['time_stamp'])
    df['date_only'] = df['time_stamp'].dt.date