# data_pipeline/automated_watcher.py

import os
import sys
import time
from datetime import datetime
from ftplib import FTP, error_perm
import pandas as pd
from sqlalchemy import create_engine

# --- Add project root to path for imports ---
try:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, PROJECT_ROOT)
    from data_pipeline.sensor_report import SensorReport
except ImportError:
    print("FATAL ERROR: Could not import SensorReport. Ensure this script is in 'data_pipeline/'")
    sys.exit(1)


# --- Configuration ---
FTP_HOST = "145.223.107.54"
FTP_USERNAME = "u209446640.csu"
FTP_PASSWORD = "Energy!2"
CHECK_INTERVAL_SECONDS = 86400

# Path Configuration
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
PULSE_LOG_FILE = os.path.join(LOGS_DIR, "pulse.txt")
PROCESSED_FILES_LOG = os.path.join(LOGS_DIR, "processed_files.log")
DB_FILE = os.path.join(PROJECT_ROOT, "database", "local_test_db.sqlite")
TEMP_RAW_DIR = os.path.join(PROJECT_ROOT, "output", "unprocessed_reports")
MAX_LOG_LINES = 10000


def log_activity(message: str):
    """Logs a message to the pulse.txt file with a timestamp, handling log rotation."""
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n"
    
    lines = []
    if os.path.exists(PULSE_LOG_FILE):
        # Read with UTF-8 to be safe
        with open(PULSE_LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    
    lines.append(log_entry)
    
    if len(lines) > MAX_LOG_LINES:
        lines = lines[-MAX_LOG_LINES:]
        
    # *** KEY FIX: Write with explicit UTF-8 encoding ***
    with open(PULSE_LOG_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    # Print the clean message to the console
    print(log_entry.strip())


def get_processed_files() -> set:
    """Reads the list of already processed files from its log."""
    os.makedirs(LOGS_DIR, exist_ok=True)
    if not os.path.exists(PROCESSED_FILES_LOG):
        return set()
    with open(PROCESSED_FILES_LOG, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)


def mark_file_as_processed(filename: str):
    """Adds a filename to the log of processed files."""
    with open(PROCESSED_FILES_LOG, 'a', encoding='utf-8') as f:
        f.write(f"{filename}\n")


def find_all_csv_on_ftp(ftp) -> list:
    """Recursively finds all .csv files on the FTP server."""
    all_files = []
    def recursive_scan(path):
        try:
            items = ftp.nlst(path)
            for item in items:
                if os.path.basename(item) in ['.', '..']:
                    continue
                try:
                    ftp.cwd(item)
                    recursive_scan(item)
                    ftp.cwd('..')
                except error_perm:
                    if item.lower().endswith('.csv'):
                        all_files.append(item)
        except error_perm as e:
            log_activity(f"FTP Warning: Could not access path '{path}'. Error: {e}")
        except Exception as e:
            log_activity(f"FTP Error: An unexpected error occurred during scan at '{path}': {e}")
            
    recursive_scan('/')
    return all_files


def process_new_file(ftp, ftp_path, db_engine):
    """Downloads, sanitizes, and loads a single new file into the database."""
    log_activity(f"Processing new file: {ftp_path}")
    
    unique_filename = ftp_path.strip('/').replace('/', '-')
    raw_save_path = os.path.join(TEMP_RAW_DIR, unique_filename)
    
    try:
        with open(raw_save_path, 'wb') as f:
            ftp.retrbinary(f"RETR {ftp_path}", f.write)
        log_activity(f"  -> Downloaded to '{os.path.basename(raw_save_path)}'")
        
        report = SensorReport(raw_save_path)
        sanitized_df = report.to_db_format()
        if sanitized_df.empty:
            raise ValueError("Sanitization resulted in an empty DataFrame.")
        log_activity(f"  -> Sanitized {len(sanitized_df)} rows of data.")
        
        with db_engine.connect() as connection:
            sanitized_df.to_sql('energy_usage', connection, if_exists='append', index=False)
        log_activity(f"  -> Loaded data into local SQLite database.")
        
        mark_file_as_processed(ftp_path)
        # Using a more robust logging format
        log_activity(f"[OK] Successfully processed and loaded '{ftp_path}'.")
        
    except Exception as e:
        # Using a more robust logging format
        log_activity(f"[FAIL] FAILED to process '{ftp_path}'. Error: {e}")
    finally:
        if os.path.exists(raw_save_path):
            os.remove(raw_save_path)


def main():
    """Main loop to continuously check for and process new files."""
    log_activity("--- Automated Watcher Started ---")
    
    os.makedirs(TEMP_RAW_DIR, exist_ok=True)
    db_engine = create_engine(f'sqlite:///{DB_FILE}')

    while True:
        try:
            log_activity("Starting new check cycle.")
            
            processed_files = get_processed_files()
            
            ftp = FTP(FTP_HOST, timeout=30)
            ftp.login(FTP_USERNAME, FTP_PASSWORD)
            remote_files = find_all_csv_on_ftp(ftp)
            ftp.quit() # Disconnect as soon as we have the list
            
            new_files = [f for f in remote_files if f not in processed_files]
            
            if not new_files:
                log_activity("No new files found.")
            else:
                log_activity(f"Found {len(new_files)} new files to process.")
                # Re-establish connection for downloading
                ftp = FTP(FTP_HOST, timeout=30)
                ftp.login(FTP_USERNAME, FTP_PASSWORD)
                for ftp_path in new_files:
                    process_new_file(ftp, ftp_path, db_engine)
                ftp.quit()
            
        except Exception as e:
            log_activity(f"[CRITICAL] CRITICAL ERROR in main loop: {e}")
            
        log_activity(f"Check cycle complete. Waiting for {CHECK_INTERVAL_SECONDS} seconds...")
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()