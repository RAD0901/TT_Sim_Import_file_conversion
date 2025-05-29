#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI functionality for the SIM Management application.
"""

import tkinter as tk
from tkinter import ttk
import ctypes
import sys
from constants import COLORS
from providers import select_provider, create_logo_canvas
from import_utils import import_sims
from export_utils import export_import_csv

def create_gui():
    """Function to create a modern GUI for SIM Management with improved resolution."""
    # Enable DPI awareness for Windows to support high-resolution displays
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Per-monitor DPI awareness
        except Exception:
            # Fallback to older method if shcore is not available
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

    # Initialize the application window
    root = tk.Tk()
    root.title("SIM Card Management Portal")
    # Increase initial height slightly more
    root.geometry("800x700") 
    root.configure(bg=COLORS["background"])  # Set root window to navy blue
    
    # Calculate scaling factor based on screen resolution
    scaling_factor = get_scaling_factor(root)
    
    # Apply a modern style to widgets
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure styles for various widgets with appropriate fonts
    style.configure('TFrame', background=COLORS["background"])
    style.configure('TLabel', background=COLORS["background"], foreground="white", 
                   font=('Segoe UI', 11))
    style.configure('TButton', background=COLORS["primary"], foreground="white", 
                   font=('Segoe UI', 11, 'bold'))
    style.configure('Secondary.TButton', background=COLORS["secondary"])
    
    # Create header frame
    header_frame = ttk.Frame(root, style='TFrame')
    header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
    
    # App title - white text on blue background
    title_label = tk.Label(header_frame, 
                          text="Techtool SIM Card Import file generator", 
                          font=('Segoe UI', 18, 'bold'),
                          bg=COLORS["background"],
                          fg="white")
    title_label.pack(side=tk.LEFT)
    
    # Main content frame with card-like appearance - now using light gray
    main_frame = tk.Frame(root, bg=COLORS["card_bg"], 
                         padx=30, 
                         pady=30, 
                         bd=1, relief=tk.RIDGE)
    # Allow main frame to expand vertically
    main_frame.pack(fill=tk.BOTH, expand=True, 
                   padx=20, 
                   pady=20)
    
    # Provider selection section - now with light gray background
    provider_section = tk.Frame(main_frame, bg=COLORS["card_bg"])
    # Add more bottom padding to this section
    provider_section.pack(fill=tk.X, pady=(10, 20))
    
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
    # Add more padding below the logos frame
    logos_frame.pack(pady=(10, 25))
    
    # Create container frames for logo + status label
    vodacom_container = tk.Frame(logos_frame, bg=COLORS["card_bg"])
    vodacom_container.pack(side=tk.LEFT, padx=20, anchor=tk.N)
    
    mtn_container = tk.Frame(logos_frame, bg=COLORS["card_bg"])
    mtn_container.pack(side=tk.LEFT, padx=20, anchor=tk.N)

    # Create frames for each logo with padding and border
    vodacom_frame = tk.Frame(vodacom_container, bd=2, relief=tk.FLAT, 
                            padx=10, 
                            pady=10, 
                            bg=COLORS["card_bg"])
    vodacom_frame.pack()
    
    mtn_frame = tk.Frame(mtn_container, bd=2, relief=tk.FLAT, 
                        padx=10, 
                        pady=10, 
                        bg=COLORS["card_bg"])
    mtn_frame.pack()
    
    # Create logos using canvas - standard size
    logo_size = 100
    vodacom_logo = create_logo_canvas(vodacom_frame, COLORS["vodacom_color"], "Vodacom", 
                                     width=logo_size, height=logo_size)
    vodacom_logo.pack()
    
    mtn_logo = create_logo_canvas(mtn_frame, COLORS["mtn_color"], "MTN", 
                                 width=logo_size, height=logo_size)
    mtn_logo.pack()

    # Create status labels below each logo container
    # Reserve height for ~3 lines of text and add bottom padding
    vodacom_status_label = tk.Label(vodacom_container, text="", 
                                   font=('Segoe UI', 8), 
                                   bg=COLORS["card_bg"], 
                                   fg=COLORS["text"], 
                                   wraplength=140, 
                                   justify=tk.CENTER,
                                   height=3) # Reserve height for 3 lines
    vodacom_status_label.pack(pady=(5, 3), fill=tk.X) # Add bottom padding

    mtn_status_label = tk.Label(mtn_container, text="", 
                                font=('Segoe UI', 8), 
                                bg=COLORS["card_bg"], 
                                fg=COLORS["text"], 
                                wraplength=140, 
                                justify=tk.CENTER,
                                height=3) # Reserve height for 3 lines
    mtn_status_label.pack(pady=(5, 3), fill=tk.X) # Add bottom padding
    
    # Bind click events for logo selection
    vodacom_logo.bind("<Button-1>", lambda e: select_provider("Vodacom", vodacom_frame, mtn_frame, selected_provider))
    vodacom_frame.bind("<Button-1>", lambda e: select_provider("Vodacom", vodacom_frame, mtn_frame, selected_provider))
    
    mtn_logo.bind("<Button-1>", lambda e: select_provider("MTN", vodacom_frame, mtn_frame, selected_provider))
    mtn_frame.bind("<Button-1>", lambda e: select_provider("MTN", vodacom_frame, mtn_frame, selected_provider))
    
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
                          text="Import SIM cards and then export data for Techtool", 
                          font=('Segoe UI', 10),
                          bg=COLORS["card_bg"],
                          fg=COLORS["text"])
    actions_desc.pack(anchor=tk.W, pady=(0, 15))
    
    # Button frame for better layout
    button_frame = tk.Frame(buttons_section, bg=COLORS["card_bg"])
    button_frame.pack(fill=tk.X)
    
    # Modern styled buttons with appropriate scaling
    button_font_size = 11
    button_padding_x = 20
    button_padding_y = 10
    
    import_icon = "📥 "  # Unicode icon
    import_sims_button = tk.Button(
        button_frame, 
        text=f"{import_icon}Import SIM Cards", 
        # Pass status labels to import_sims
        command=lambda: import_sims(selected_provider, vodacom_status_label, mtn_status_label),
        bg=COLORS["primary"],
        fg="white",
        font=('Segoe UI', button_font_size, 'bold'),
        padx=button_padding_x,
        pady=button_padding_y,
        bd=0,
        cursor="hand2",
        activebackground=COLORS["accent"],
        activeforeground="white"
    )
    import_sims_button.pack(side=tk.LEFT, padx=(0, 15))
    
    export_icon = "📤 "  # Unicode icon
    export_csv_button = tk.Button(
        button_frame, 
        text=f"{export_icon}Export to CSV", 
        command=export_import_csv,
        bg=COLORS["secondary"],
        fg="white",
        font=('Segoe UI', button_font_size, 'bold'),
        padx=button_padding_x,
        pady=button_padding_y,
        bd=0,
        cursor="hand2",
        activebackground="#f2b380",  # Lighter orange for hover
        activeforeground="white"
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
    
    return root
    
def get_scaling_factor(root):
    """Calculate a scaling factor based on screen resolution."""
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Base scaling on screen resolution
    if screen_width >= 3840:  # 4K
        return 1.5
    elif screen_width >= 2560:  # 1440p
        return 1.2
    elif screen_width >= 1920:  # 1080p
        return 1.0
    else:  # Lower resolutions
        return 0.9