import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os

def visualize_csv(filepath):
    """
    Reads a sanitized CSV and plots the energy usage for each location.
    """
    try:
        df = pd.read_csv(filepath, parse_dates=['time_stamp'])
        
        required_columns = {'time_stamp', 'location', 'energy_usage', 'electric_or_gas'}
        if not required_columns.issubset(df.columns):
            print(f"Error: The selected file '{os.path.basename(filepath)}' is missing required columns.")
            print(f"Required: {required_columns}")
            return

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(15, 8))

        # Group by location and energy type to plot separate lines
        for (location, energy_type), group in df.groupby(['location', 'electric_or_gas']):
            ax.plot(group['time_stamp'], group['energy_usage'], marker='.', linestyle='-', label=f'{location} ({energy_type})')

        ax.set_title(f'Energy Usage Report: {os.path.basename(filepath)}', fontsize=16)
        ax.set_xlabel('Time Stamp', fontsize=12)
        ax.set_ylabel('Energy Usage', fontsize=12)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()

        fig.autofmt_xdate() # Improve formatting of x-axis date labels
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"An error occurred while trying to visualize the file: {e}")


def main():
    """
    Opens a file dialog to select a CSV and then visualizes it.
    """
    # Set up the root Tkinter window
    root = tk.Tk()
    root.withdraw() # Hide the main window, we only want the dialog

    # Open the file selection dialog
    filepath = filedialog.askopenfilename(
        title="Select a Sanitized CSV File",
        filetypes=(("CSV Files", "*.csv"), ("All files", "*.*")),
        initialdir=os.path.join(os.getcwd(), 'sanitized_reports') # Start in the sanitized reports folder
    )

    if filepath: # If the user selected a file
        visualize_csv(filepath)
    else:
        print("No file selected.")


if __name__ == "__main__":
    main()