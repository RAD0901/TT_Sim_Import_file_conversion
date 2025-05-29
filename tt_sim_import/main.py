#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the SIM Management application.
This module imports and uses functionality from the other modules.
"""

import os
import sys
import traceback
import tkinter as tk
from tkinter import messagebox

# Add the parent directory to sys.path to ensure imports work in dev mode
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    # Try to import modules using relative imports (development mode)
    from tt_sim_import.gui import create_gui
except ImportError as e:
    try:
        # Try direct import (when running from this directory)
        from gui import create_gui
    except ImportError as e1:
        # If both imports fail
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        error_message = f"Failed to import GUI module.\n\nError details:\n{str(e1)}"
        messagebox.showerror("Import Error", error_message)
        print(f"Import Error: {error_message}")
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

def main():
    """Main function to start the application."""
    try:
        # Create the GUI and start the application
        root = create_gui()
        root.mainloop()
    except Exception as e:
        # Handle any unexpected errors
        if not isinstance(tk._default_root, tk.Tk):
            root = tk.Tk()
            root.withdraw()
        
        error_message = f"An error occurred while running the application:\n{str(e)}"
        messagebox.showerror("Application Error", error_message)
        print(f"Application Error: {error_message}")
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()
