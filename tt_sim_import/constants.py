#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Constants used throughout the application.
"""

# Modern color scheme with swapped background colors
COLORS = {
    "primary": "#3c556e",       # Medium blue-gray (from palette)
    "secondary": "#e9a061",     # Orange (from palette)
    "background": "#152643",    # Dark navy blue for outer window
    "text": "#101d37",          # Dark text for light background
    "accent": "#7fabc5",        # Light blue (from palette)
    "card_bg": "#F2F2F2",       # Light gray for inner panels
    "selected": "#97b9cb",      # Pale blue (from palette)
    "selected_logo_border": "#83E190", # Light green for selected logo border
    "vodacom_color": "#e40000", # Vodacom red
    "mtn_color": "#ffcb05",     # MTN yellow
    "vodacom_border": "#ff0000", # Red border for Vodacom
    "mtn_border": "#ffcc00",    # Yellow border for MTN
    "selected_border": "#e9a061", # Orange border for selected
    "vodacom_border_light": "#ffcccc", # Light red for semi-transparent effect
    "mtn_border_light": "#fff5cc"  # Light yellow for semi-transparent effect
}

# Column name mappings for flexibility - using lowercase for case-insensitive comparison
COLUMN_MAPPINGS = {
    "Cell Number": ["cell number", "cell no", "cellnumber", "cellno", "cell_number", "cell_no", "msisdn", "mobile no"],
    "Sim Number": ["sim number", "sim no", "simnumber", "simno", "sim_number", "sim_no", "iccid", "sim", "icc id", "sim id"]
}

# IP address column variations
VODACOM_IP_VARIANTS = ["ip address", "ip_address", "ipaddress", "ip"]
MTN_IP1_VARIANTS = ["ip address1", "ip_address1", "ipaddress1", "ip1", "cn", "cn-ip"]
MTN_IP2_VARIANTS = ["ip address2", "ip_address2", "ipaddress2", "ip2", "nl", "nl-ip"]