# dashboard/data/csv_source.py

import pandas as pd
import os
import sys
from sqlalchemy import create_engine

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.sql_credentials import SQL_CREDENTIALS

# --- IMPORTANT!!! ---
# Set this to True to use the local test DB, False to use the live production DB.
USE_LOCAL_DB_FOR_DASHBOARD = False

print("=" * 50)
print("Dashboard Data Source Configuration")

if USE_LOCAL_DB_FOR_DASHBOARD:
    # --- Connect to local SQLite database ---
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'local_test_db.sqlite'))
    print(f"Mode: Local SQLite Database")
    print(f"Path: {db_path}")
    if not os.path.exists(db_path):
        print("\nFATAL ERROR: local_test_db.sqlite not found!")
        print("Please run 'database/load_data.py' first to create and populate it.")
        sys.exit(1)
    engine = create_engine(f'sqlite:///{db_path}')
else:
    # --- Connect to production MySQL database ---
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

# --- Load data from the selected database ---
try:
    print("Loading data from 'energy_usage' table...")
    df = pd.read_sql_table('energy_usage', engine)
    print(f"✓ Successfully loaded {len(df)} rows.")
except Exception as e:
    print(f"✗ Failed to load data from database: {e}")
    df = pd.DataFrame()

# --- Post-Processing ---
if not df.empty and 'electric_or_gas' in df.columns:
    # Convert electric_or_gas (which is 0 or 1) into a human-readable string
    df['unit'] = df['electric_or_gas'].apply(lambda x: 'Gas (kWh)' if x == 1 else 'Electric (kWh)')
elif not df.empty:
    print("Warning: 'electric_or_gas' column not found. The 'Unit' filter may not work.")