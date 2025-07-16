import os
import sys
from ftplib import FTP, error_perm

try:
    # Go up one level from the current script's directory (data_pipeline -> Energy_Manager)
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # This adds the data_pipeline directory to the python path so it can find sensor_report
    sys.path.insert(0, os.path.dirname(__file__))
    from sensor_report import SensorReport
except (ImportError, IndexError):
    print("FATAL ERROR: Could not find 'sensor_report.py'. Ensure it's in the same directory.")
    sys.exit(1)


# --- Configuration ---
HOST = "145.223.107.54"
USERNAME = "u209446640.csu"
PASSWORD = "Energy!2"

SANITIZED_DIR = os.path.join(PROJECT_ROOT, "output", "sanitized_reports")
UNPROCESSED_DIR = os.path.join(PROJECT_ROOT, "output", "unprocessed_reports")


def find_all_csv_files(ftp, path='/'):
    csv_file_paths = []
    try:
        items = ftp.nlst(path) if path else ftp.nlst()
    except error_perm:
        return []

    for item_name in items:
        base_name = os.path.basename(item_name)
        if base_name in ['.', '..', '.DS_Store']: continue
        item_path = f"{path.rstrip('/')}/{base_name}"
        try:
            ftp.cwd(item_path)
            ftp.cwd('..') 
            csv_file_paths.extend(find_all_csv_files(ftp, item_path))
        except error_perm:
            if item_path.lower().endswith('.csv'):
                print(f"  Found CSV: {item_path}")
                csv_file_paths.append(item_path)
        except Exception as e:
            print(f"Warning: Could not process item '{item_path}': {e}", file=sys.stderr)
    return csv_file_paths


def main():
    ftp = None
    # Create the output directories if they don't exist
    os.makedirs(SANITIZED_DIR, exist_ok=True)
    os.makedirs(UNPROCESSED_DIR, exist_ok=True)
    print(f"Sanitized output will be saved to: '{SANITIZED_DIR}'")
    print(f"Failed files will be saved to:    '{UNPROCESSED_DIR}'")

    try:
        print(f"\nConnecting to host: {HOST}...")
        ftp = FTP(HOST, timeout=30)
        ftp.login(USERNAME, PASSWORD)
        print("✓ Connection and login successful.")
        print("-" * 50)

        print("TASK 1: Searching for all CSV files on the server...")
        all_csv_files = find_all_csv_files(ftp)
        if not all_csv_files:
            print("No CSV files found on the server. Exiting.")
            return
        print(f"✓ Found {len(all_csv_files)} CSV files to process.")
        print("-" * 50)

        print("TASK 2: Downloading, transforming, and sanitizing files...")
        success_count = 0
        fail_count = 0
        for ftp_path in all_csv_files:
            unique_raw_filename = ftp_path.strip('/').replace('/', '-')
            raw_save_path = os.path.join(UNPROCESSED_DIR, unique_raw_filename)

            try:
                print(f"Processing '{ftp_path}'...")
                with open(raw_save_path, 'wb') as f:
                    ftp.retrbinary(f"RETR {ftp_path}", f.write)

                report = SensorReport(raw_save_path)
                sanitized_df = report.to_db_format()

                if sanitized_df.empty:
                    print(f"  -> SKIPPED: No data after processing. Raw file kept in '{UNPROCESSED_DIR}'.")
                    fail_count += 1
                    continue

                sanitized_filename = f"{os.path.splitext(unique_raw_filename)[0]}_sanitized.csv"
                sanitized_save_path = os.path.join(SANITIZED_DIR, sanitized_filename)
                sanitized_df.to_csv(sanitized_save_path, index=False)

                os.remove(raw_save_path)
                print(f"  -> ✓ Saved sanitized file to '{sanitized_save_path}'")
                success_count += 1

            except Exception as e:
                print(f"  -> ✗ FAILED to process '{ftp_path}'. Raw file saved as '{unique_raw_filename}'.")
                print(f"     Error: {e}", file=sys.stderr)
                fail_count += 1

        print("-" * 50)
        print("Processing complete.")
        print(f"  Successfully sanitized: {success_count} files")
        print(f"  Failed to process:      {fail_count} files (check '{UNPROCESSED_DIR}')")

    except error_perm as e:
        print(f"\nFTP ERROR: {e}", file=sys.stderr)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
    finally:
        if ftp:
            print("\nDisconnecting from the FTP server.")
            ftp.quit()


if __name__ == "__main__":
    main()