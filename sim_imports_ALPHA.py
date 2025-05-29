import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from PIL import Image, ImageTk  # You'll need to pip install pillow
import os

# Initialize the global DataFrame and provider variable
global_df = pd.DataFrame()
selected_provider = None

# Modern color scheme
COLORS = {
    "primary": "#3498db",       # Blue
    "secondary": "#2ecc71",     # Green
    "background": "#f5f7fa",    # Light gray
    "text": "#2c3e50",          # Dark blue/gray
    "accent": "#e74c3c",        # Red for warnings/errors
    "card_bg": "#ffffff",       # White for cards
    "selected": "#e0f7fa",      # Light blue for selected state
    "vodacom_color": "#e40000", # Vodacom red
    "mtn_color": "#ffcb05"      # MTN yellow
}

def import_sims():
    """Function to import an Excel file and create a global DataFrame based on selected provider."""
    global global_df, selected_provider

    # Check if provider is selected
    if not selected_provider.get():
        messagebox.showerror("Error", "Please select a provider (Vodacom or MTN) first")
        return

    provider = selected_provider.get()

    # Open file dialog to select the Excel file
    file_path = filedialog.askopenfilename(
        title=f"Select {provider} Import Sim's File",
        filetypes=(("Excel Files", "*.xlsx;*.xls"), ("All Files", "*.*"))
    )

    if not file_path:
        return  # If no file selected, exit the function

    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)
        
        # Print column names to debug
        print("Available columns in the file:", df.columns.tolist())
        
        # Column name mappings for flexibility - using lowercase for case-insensitive comparison
        column_mappings = {
            "Cell Number": ["cell number", "cell no", "cellnumber", "cellno", "cell_number", "cell_no", "msisdn", "mobile no"],
            "Sim Number": ["sim number", "sim no", "simnumber", "simno", "sim_number", "sim_no", "iccid", "sim", "icc id", "sim id"]
        }
        
        # Create a lowercase version of column names for matching
        lowercase_columns = {col.lower().strip(): col for col in df.columns}
        
        print("Lowercase columns for matching:", lowercase_columns)
        
        # Find and rename columns based on variations
        renamed_columns = {}
        missing_cols = []
        
        for standard_name, variations in column_mappings.items():
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
                error_msg += f"- {col}: {', '.join([var.title() for var in column_mappings[col]])}\n"
            error_msg += "\nColumns found in file: " + ", ".join(df.columns.tolist())
            messagebox.showerror("Error", error_msg)
            return
            
        # Rename columns to standard names
        df = df.rename(columns=renamed_columns)

        # Provider-specific validation for IP addresses - using case-insensitive matching
        if provider == "Vodacom":
            # Vodacom always has 1 IP Address - check various naming patterns (case insensitive)
            ip_variants = ["ip address", "ip_address", "ipaddress", "ip"]
            ip_col_found = None
            
            for var in ip_variants:
                matching_cols = [col for col in lowercase_columns if var == col]
                if matching_cols:
                    ip_col_found = lowercase_columns[matching_cols[0]]
                    break
                    
            if not ip_col_found:
                messagebox.showerror("Error", 
                                    "Vodacom file must contain an IP Address column.\n\n"
                                    f"Columns found: {', '.join(df.columns.tolist())}")
                return
                
            # Standardize the IP column name
            df = df.rename(columns={ip_col_found: "IP Address"})
            ip_columns = ["IP Address"]
            
        else:  # MTN
            # MTN needs 2 IP addresses - check various naming patterns (case insensitive)
            ip1_variants = ["ip address1", "ip_address1", "ipaddress1", "ip1", "cn", "cn-ip"]
            ip2_variants = ["ip address2", "ip_address2", "ipaddress2", "ip2", "nl", "nl-ip"]
            
            ip1_col_found = None
            ip2_col_found = None
            
            # Print available columns for debug
            print("Looking for IP1 columns with variations:", ip1_variants)
            print("Looking for IP2 columns with variations:", ip2_variants)
            
            # More flexible matching for IP columns - check if any variant is contained in any column name
            for col_lower, col_original in lowercase_columns.items():
                # For primary IP
                for var in ip1_variants:
                    if var in col_lower or col_lower in var:
                        ip1_col_found = col_original
                        print(f"Found primary IP column: '{col_original}'")
                        break
                if ip1_col_found:
                    break  # Exit if found
            
            # Same for secondary IP
            for col_lower, col_original in lowercase_columns.items():
                # For secondary IP
                for var in ip2_variants:
                    if var in col_lower or col_lower in var:
                        ip2_col_found = col_original
                        print(f"Found secondary IP column: '{col_original}'")
                        break
                if ip2_col_found:
                    break  # Exit if found
            
            if not ip1_col_found or not ip2_col_found:
                messagebox.showerror("Error", "MTN file must contain both primary and secondary IP address columns.\n\n"
                                   "Acceptable column names for primary IP: IP Address1, IP1, CN, CN-IP\n"
                                   "Acceptable column names for secondary IP: IP Address2, IP2, NL, NL-IP\n\n"
                                   f"Columns found: {', '.join(df.columns.tolist())}")
                return
                
            # Standardize the IP column names
            df = df.rename(columns={ip1_col_found: "IP Address1", ip2_col_found: "IP Address2"})
            ip_columns = ["IP Address1", "IP Address2"]

        # Create the global DataFrame with the required columns including all available IP columns
        columns_to_keep = list(column_mappings.keys()) + ip_columns
        global_df = df[columns_to_keep]
        sim_count = len(global_df)
        messagebox.showinfo("Success", f"{provider} Sim's imported successfully!\n\n{sim_count} SIM cards imported with {len(ip_columns)} IP address columns.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Helper function to select provider and update UI
def select_provider(provider_name, vodacom_frame, mtn_frame):
    """Function to handle provider selection and update UI accordingly."""
    global selected_provider
    
    selected_provider.set(provider_name)
    
    # Update UI to show which provider is selected
    if provider_name == "Vodacom":
        vodacom_frame.config(bg=COLORS["selected"], relief=tk.RAISED)
        mtn_frame.config(bg=COLORS["card_bg"], relief=tk.FLAT)
    else:  # MTN
        vodacom_frame.config(bg=COLORS["card_bg"], relief=tk.FLAT)
        mtn_frame.config(bg=COLORS["selected"], relief=tk.RAISED)

# Create a custom logo canvas
def create_logo_canvas(parent, color, text, width=100, height=100):
    """Create a custom logo using a canvas with specified color and text."""
    canvas = tk.Canvas(parent, width=width, height=height, bg=COLORS["card_bg"], 
                      highlightthickness=0, cursor="hand2")
    canvas.create_oval(10, 10, width-10, height-10, fill=color, outline="")
    
    # Add the first letter of provider name in the center
    canvas.create_text(width/2, height/2, text=text[0], 
                      font=('Segoe UI', 36, 'bold'), fill="white")
    
    return canvas

def export_import_csv():
    """Function to create and export the export_sims DataFrame."""
    global global_df

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

def create_gui():
    """Function to create a modern GUI."""
    global selected_provider
    
    root = tk.Tk()
    root.title("SIM Management Portal")
    root.geometry("800x600")  # Increased window size
    root.configure(bg=COLORS["background"])
    
    # Apply a modern style to widgets
    style = ttk.Style()
    style.theme_use('clam')  # Use 'clam' theme as base
    
    # Configure styles for various widgets
    style.configure('TFrame', background=COLORS["background"])
    style.configure('TLabel', background=COLORS["background"], foreground=COLORS["text"], font=('Segoe UI', 11))
    style.configure('TButton', background=COLORS["primary"], foreground='white', font=('Segoe UI', 11, 'bold'))
    style.configure('Secondary.TButton', background=COLORS["secondary"])
    
    # Create header frame
    header_frame = ttk.Frame(root, style='TFrame')
    header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
    
    # App title
    title_label = tk.Label(header_frame, 
                          text="SIM Card Management Portal", 
                          font=('Segoe UI', 18, 'bold'),
                          bg=COLORS["background"],
                          fg=COLORS["primary"])
    title_label.pack(side=tk.LEFT)
    
    # Main content frame with card-like appearance
    main_frame = tk.Frame(root, bg=COLORS["card_bg"], padx=30, pady=30, bd=1, relief=tk.RIDGE)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Provider selection section
    provider_section = tk.Frame(main_frame, bg=COLORS["card_bg"])
    provider_section.pack(fill=tk.X, pady=10)
    
    provider_title = tk.Label(provider_section, 
                             text="Network Provider", 
                             font=('Segoe UI', 12, 'bold'),
                             bg=COLORS["card_bg"],
                             fg=COLORS["text"])
    provider_title.pack(anchor=tk.W)
    
    provider_desc = tk.Label(provider_section, 
                            text="Click on a provider logo to select", 
                            font=('Segoe UI', 10),
                            bg=COLORS["card_bg"],
                            fg=COLORS["text"])
    provider_desc.pack(anchor=tk.W, pady=(0, 10))
    
    # Provider selection with logos
    provider_frame = tk.Frame(provider_section, bg=COLORS["card_bg"])
    provider_frame.pack(fill=tk.X)
    
    # Create a StringVar for the selected provider
    selected_provider = tk.StringVar()
    
    # Create the logo frames with clickable behavior
    logos_frame = tk.Frame(provider_frame, bg=COLORS["card_bg"])
    logos_frame.pack(pady=10)
    
    # Create frames for each logo with padding and border
    vodacom_frame = tk.Frame(logos_frame, bd=2, relief=tk.FLAT, padx=10, pady=10, bg=COLORS["card_bg"])
    vodacom_frame.pack(side=tk.LEFT, padx=20)
    
    mtn_frame = tk.Frame(logos_frame, bd=2, relief=tk.FLAT, padx=10, pady=10, bg=COLORS["card_bg"])
    mtn_frame.pack(side=tk.LEFT, padx=20)
    
    # Create custom logos using canvas
    vodacom_logo = create_logo_canvas(vodacom_frame, COLORS["vodacom_color"], "Vodacom")
    vodacom_logo.pack()
    
    vodacom_text = tk.Label(vodacom_frame, text="Vodacom", font=('Segoe UI', 10, 'bold'), 
                           bg=COLORS["card_bg"], fg=COLORS["vodacom_color"])
    vodacom_text.pack(pady=(5, 0))
    
    mtn_logo = create_logo_canvas(mtn_frame, COLORS["mtn_color"], "MTN")
    mtn_logo.pack()
    
    mtn_text = tk.Label(mtn_frame, text="MTN", font=('Segoe UI', 10, 'bold'), 
                       bg=COLORS["card_bg"], fg=COLORS["mtn_color"])
    mtn_text.pack(pady=(5, 0))
    
    # Bind click events for logo selection
    vodacom_logo.bind("<Button-1>", lambda e: select_provider("Vodacom", vodacom_frame, mtn_frame))
    vodacom_text.bind("<Button-1>", lambda e: select_provider("Vodacom", vodacom_frame, mtn_frame))
    vodacom_frame.bind("<Button-1>", lambda e: select_provider("Vodacom", vodacom_frame, mtn_frame))
    
    mtn_logo.bind("<Button-1>", lambda e: select_provider("MTN", vodacom_frame, mtn_frame))
    mtn_text.bind("<Button-1>", lambda e: select_provider("MTN", vodacom_frame, mtn_frame))
    mtn_frame.bind("<Button-1>", lambda e: select_provider("MTN", vodacom_frame, mtn_frame))
    
    # Action buttons section
    buttons_section = tk.Frame(main_frame, bg=COLORS["card_bg"], pady=20)
    buttons_section.pack(fill=tk.X, pady=10)
    
    actions_title = tk.Label(buttons_section, 
                            text="Actions", 
                            font=('Segoe UI', 12, 'bold'),
                            bg=COLORS["card_bg"],
                            fg=COLORS["text"])
    actions_title.pack(anchor=tk.W)
    
    actions_desc = tk.Label(buttons_section, 
                          text="Import SIM cards or export data", 
                          font=('Segoe UI', 10),
                          bg=COLORS["card_bg"],
                          fg=COLORS["text"])
    actions_desc.pack(anchor=tk.W, pady=(0, 15))
    
    # Button frame for better layout
    button_frame = tk.Frame(buttons_section, bg=COLORS["card_bg"])
    button_frame.pack(fill=tk.X)
    
    # Modern styled buttons
    import_icon = "📥 "  # Unicode icon
    import_sims_button = tk.Button(
        button_frame, 
        text=f"{import_icon}Import SIM Cards", 
        command=import_sims,
        bg=COLORS["primary"],
        fg="white",
        font=('Segoe UI', 11),
        padx=15,
        pady=8,
        bd=0,
        cursor="hand2",
        activebackground="#2980b9"  # Darker blue for hover
    )
    import_sims_button.pack(side=tk.LEFT, padx=(0, 10))
    
    export_icon = "📤 "  # Unicode icon
    export_csv_button = tk.Button(
        button_frame, 
        text=f"{export_icon}Export to CSV", 
        command=export_import_csv,
        bg=COLORS["secondary"],
        fg="white",
        font=('Segoe UI', 11),
        padx=15,
        pady=8,
        bd=0,
        cursor="hand2",
        activebackground="#27ae60"  # Darker green for hover
    )
    export_csv_button.pack(side=tk.LEFT)
    
    # Status bar at the bottom
    status_bar = tk.Frame(root, bg=COLORS["primary"], height=30)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    status_text = tk.Label(
        status_bar, 
        text="Ready - Please select a provider and import SIMs", 
        bg=COLORS["primary"],
        fg="white",
        font=('Segoe UI', 9),
        padx=10
    )
    status_text.pack(side=tk.LEFT, pady=5)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()