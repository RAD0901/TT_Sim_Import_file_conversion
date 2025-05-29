#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Import functionality for the SIM Management application.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from constants import COLUMN_MAPPINGS, VODACOM_IP_VARIANTS, MTN_IP1_VARIANTS, MTN_IP2_VARIANTS

# Define global_df as a module-level variable
global_df = pd.DataFrame()

def import_sims(selected_provider, vodacom_status_label, mtn_status_label):
    """Function to import an Excel file and update the status label.
    
    Args:
        selected_provider (tk.StringVar): StringVar containing the selected provider
        vodacom_status_label (tk.Label): Label to display Vodacom import status
        mtn_status_label (tk.Label): Label to display MTN import status
        
    Returns:
        pd.DataFrame: The imported data as a DataFrame, or empty DataFrame if import fails
    """
    global global_df

    # Clear previous status messages
    vodacom_status_label.config(text="", fg="green") # Reset color
    mtn_status_label.config(text="", fg="green") # Reset color

    # Check if provider is selected
    if not selected_provider.get():
        messagebox.showerror("Error", "Please select a provider (Vodacom or MTN) first")
        return pd.DataFrame()

    provider = selected_provider.get()
    # Determine the correct status label to update
    status_label = vodacom_status_label if provider == "Vodacom" else mtn_status_label

    # Open file dialog to select the Excel file
    file_path = filedialog.askopenfilename(
        title=f"Select {provider} Import Sim's File",
        filetypes=(("Excel Files", "*.xlsx;*.xls"), ("All Files", "*.*"))
    )

    if not file_path:
        status_label.config(text="Import cancelled.", fg="orange")
        return pd.DataFrame()  # If no file selected, return empty DataFrame

    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)
        
        # Print column names to debug
        print("Available columns in the file:", df.columns.tolist())
        
        # Create a lowercase version of column names for matching
        lowercase_columns = {col.lower().strip(): col for col in df.columns}
        
        print("Lowercase columns for matching:", lowercase_columns)
        
        # Find and rename columns based on variations
        renamed_columns = {}
        missing_cols = []
        
        for standard_name, variations in COLUMN_MAPPINGS.items():
            found = False
            for variation in variations:
                if variation in lowercase_columns:
                    # Map the actual column name (preserving case) to the standard name
                    renamed_columns[lowercase_columns[variation]] = standard_name
                    found = True
                    break
                    
            if not found:
                missing_cols.append(standard_name)
        
        # If any required column wasn't found, show detailed error
        if missing_cols:
            # Print more debug info
            print("Missing columns:", missing_cols)
            print("Lowercase columns in file:", lowercase_columns)
            
            error_msg = "File must contain columns: " + ", ".join(missing_cols) + "\n\n"
            error_msg += "Acceptable column name variations:\n"
            for col in missing_cols:
                error_msg += f"- {col}: {', '.join([var.title() for var in COLUMN_MAPPINGS[col]])}\n"
            error_msg += "\nColumns found in file: " + ", ".join(df.columns.tolist())
            messagebox.showerror("Error", error_msg) # Keep critical errors as popups
            status_label.config(text="Import failed: Missing columns.", fg="red")
            return pd.DataFrame()
            
        # Rename columns to standard names
        df = df.rename(columns=renamed_columns)

        # Provider-specific validation for IP addresses
        if provider == "Vodacom":
            # Vodacom always has 1 IP Address - check various naming patterns (case insensitive)
            ip_col_found = None
            
            for var in VODACOM_IP_VARIANTS:
                matching_cols = [col for col in lowercase_columns if var == col]
                if matching_cols:
                    ip_col_found = lowercase_columns[matching_cols[0]]
                    break
                    
            if not ip_col_found:
                error_msg = "Vodacom file must contain an IP Address column.\n\n"
                error_msg += f"Columns found: {', '.join(df.columns.tolist())}"
                messagebox.showerror("Error", error_msg) # Keep critical errors as popups
                status_label.config(text="Import failed: Missing IP column.", fg="red")
                return pd.DataFrame()
                
            # Standardize the IP column name
            df = df.rename(columns={ip_col_found: "IP Address"})
            ip_columns = ["IP Address"]
            
        else:  # MTN
            # MTN needs 2 IP addresses - check various naming patterns (case insensitive)
            ip1_col_found = None
            ip2_col_found = None
            
            # Print available columns for debug
            print("Looking for IP1 columns with variations:", MTN_IP1_VARIANTS)
            print("Looking for IP2 columns with variations:", MTN_IP2_VARIANTS)
            
            # More flexible matching for IP columns - check if any variant is contained in any column name
            for col_lower, col_original in lowercase_columns.items():
                # For primary IP
                for var in MTN_IP1_VARIANTS:
                    if var in col_lower or col_lower in var:
                        ip1_col_found = col_original
                        print(f"Found primary IP column: '{col_original}'")
                        break
                if ip1_col_found:
                    break  # Exit if found
            
            # Same for secondary IP
            for col_lower, col_original in lowercase_columns.items():
                # For secondary IP
                for var in MTN_IP2_VARIANTS:
                    if var in col_lower or col_lower in var:
                        ip2_col_found = col_original
                        print(f"Found secondary IP column: '{col_original}'")
                        break
                if ip2_col_found:
                    break  # Exit if found
            
            if not ip1_col_found or not ip2_col_found:
                error_msg = "MTN file must contain both primary and secondary IP address columns.\n\n"
                error_msg += "Acceptable column names for primary IP: IP Address1, IP1, CN, CN-IP\n"
                error_msg += "Acceptable column names for secondary IP: IP Address2, IP2, NL, NL-IP\n\n"
                error_msg += f"Columns found: {', '.join(df.columns.tolist())}"
                messagebox.showerror("Error", error_msg) # Keep critical errors as popups
                status_label.config(text="Import failed: Missing IP columns.", fg="red")
                return pd.DataFrame()
                
            # Standardize the IP column names
            df = df.rename(columns={ip1_col_found: "IP Address1", ip2_col_found: "IP Address2"})
            ip_columns = ["IP Address1", "IP Address2"]

        # Create the global DataFrame with the required columns including all available IP columns
        columns_to_keep = list(COLUMN_MAPPINGS.keys()) + ip_columns
        global_df = df[columns_to_keep]
        sim_count = len(global_df)
        
        # Update the status label instead of showing a messagebox
        success_message = f"{provider} Sim's imported successfully!\n{sim_count} SIMs ({len(ip_columns)} IP cols)."
        status_label.config(text=success_message, fg="green")
        
        # Clear the other provider's status label
        if provider == "Vodacom":
            mtn_status_label.config(text="")
        else:
            vodacom_status_label.config(text="")
            
        return global_df

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        messagebox.showerror("Error", error_message) # Keep unexpected errors as popups
        status_label.config(text="Import failed: Unexpected error.", fg="red")
        return pd.DataFrame()

def get_imported_data():
    """Function to get the currently imported data.
    
    Returns:
        pd.DataFrame: The current global DataFrame
    """
    global global_df
    return global_df