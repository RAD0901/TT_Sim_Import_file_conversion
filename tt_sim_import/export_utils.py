#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Export functionality for the SIM Management application.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from import_utils import get_imported_data

def export_import_csv():
    """Function to create and export the export_sims DataFrame.
    
    Exports the currently imported SIM data to a CSV file with proper formatting.
    """
    # Get the current data from import_utils
    global_df = get_imported_data()

    if global_df.empty:
        messagebox.showerror("Error", "No data available. Please import Sim's first.")
        return

    try:
        # Create the export_sims DataFrame
        export_sims = pd.DataFrame()
        export_sims["Count"] = range(1, len(global_df) + 1)
        
        # Dynamically check if cell numbers already have "27" prefix
        def add_prefix_if_needed(cell_num):
            cell_str = str(cell_num)
            if cell_str.startswith('27'):
                return cell_str
            else:
                return "27" + cell_str
        
        # Apply the function to add prefix only if needed
        export_sims["Cell Number"] = global_df["Cell Number"].apply(add_prefix_if_needed)
        export_sims["Sim Number"] = global_df["Sim Number"]
        
        # Handle IP address columns dynamically
        if "IP Address" in global_df.columns:
            export_sims["Ip Address1"] = global_df["IP Address"]
        
        if "IP Address1" in global_df.columns:
            export_sims["Ip Address1"] = global_df["IP Address1"]
            
        if "IP Address2" in global_df.columns:
            export_sims["Ip Address2"] = global_df["IP Address2"]

        # Open file dialog to select the save location
        file_path = filedialog.asksaveasfilename(
            title="Save Export CSV",
            defaultextension=".csv",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )

        if not file_path:
            return  # If no file selected, exit the function

        # Export the DataFrame to CSV
        sim_count = len(export_sims)
        export_sims.to_csv(file_path, index=False, encoding='utf-8')
        messagebox.showinfo("Success", f"File exported successfully!\n\n{sim_count} SIM cards exported to {file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")