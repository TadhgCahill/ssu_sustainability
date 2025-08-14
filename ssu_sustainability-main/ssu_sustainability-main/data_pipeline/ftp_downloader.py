import os
import sys
from ftplib import FTP, error_perm

# --- Configuration ---
HOST = "145.223.107.54"
USERNAME = "u209446640.csu"
PASSWORD = "Energy!2"
OUTPUT_DIR = "server_raw"


def download_directory_recursively(ftp, ftp_path, local_path):
    """
    Recursively downloads files and creates directories from an FTP path
    to a local path, mirroring the server's structure.
    """
    try:
        os.makedirs(local_path, exist_ok=True)
        print(f"Ensured local directory: {local_path}")

        # Change to the FTP directory to list its contents
        ftp.cwd(ftp_path)
        items = ftp.nlst()
        
    except OSError as e:
        print(f"Error: Could not create local directory '{local_path}'. {e}", file=sys.stderr)
        return
    except error_perm as e:
        print(f"Error: Could not access FTP directory '{ftp_path}'. {e}", file=sys.stderr)
        return

    for item_name in items:
        # nlst() can return simple names, ignore '.' and '..'
        if item_name in ['.', '..']:
            continue

        local_item_path = os.path.join(local_path, item_name)
        
        try:
            # Check if the item is a directory by trying to change into it
            ftp.cwd(item_name)
            
            # If successful, it's a directory. Recurse into it.
            download_directory_recursively(ftp, ftp.pwd(), local_item_path)
            
            # Go back to the parent directory to continue the loop
            ftp.cwd('..')
            
        except error_perm:
            # If cwd fails, it's a file. Download it.
            print(f"  -> Downloading file: {ftp.pwd()}/{item_name}")
            try:
                with open(local_item_path, 'wb') as local_file:
                    ftp.retrbinary(f"RETR {item_name}", local_file.write)
            except Exception as e:
                print(f"  -> FAILED to download {item_name}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred with item '{item_name}': {e}", file=sys.stderr)


def main():
    """
    Main function to connect to the FTP server and start the full download.
    """
    ftp = None
    # Ensure the main output directory exists before we start
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"All server content will be downloaded to the '{OUTPUT_DIR}' directory.")
    
    try:
        print(f"\nConnecting to host: {HOST}...")
        ftp = FTP(HOST, timeout=30)
        ftp.login(USERNAME, PASSWORD)
        print("✓ Connection and login successful.")
        print("-" * 50)
        print("Starting full server download...")
        
        # Start the recursive download from the root directory ('/')
        download_directory_recursively(ftp, '/', OUTPUT_DIR)
        
        print("-" * 50)
        print("✓ Download process complete.")

    except error_perm as e:
        print(f"\nFTP ERROR: A permission error occurred. Check credentials or permissions.")
        print(f"   > {e}", file=sys.stderr)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
    finally:
        if ftp:
            print("\nDisconnecting from the FTP server.")
            ftp.quit()


if __name__ == "__main__":
    main()