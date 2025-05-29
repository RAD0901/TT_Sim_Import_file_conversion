#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provider selection functionality for the SIM Management application.
"""

import tkinter as tk
import os
import time
from PIL import Image, ImageTk
from constants import COLORS
from resource_path import resource_path

# Store the PhotoImage objects as global variables to prevent garbage collection
logo_images = {}
logo_original_images = {}  # Store original size images
logo_enlarged_images = {}  # Store enlarged images for 3D effect

# Store canvas configurations for proper reset
canvas_original_configs = {}

def select_provider(provider_name, vodacom_frame, mtn_frame, selected_provider):
    """Function to handle provider selection and update UI accordingly.
    
    Args:
        provider_name (str): The name of the selected provider ('Vodacom' or 'MTN')
        vodacom_frame (tk.Frame): The frame containing the Vodacom logo
        mtn_frame (tk.Frame): The frame containing the MTN logo
        selected_provider (tk.StringVar): StringVar to store the selected provider
    """
    # Skip animation if provider is already selected
    if selected_provider.get() == provider_name:
        return
        
    # Get canvas elements
    vodacom_canvas = None
    mtn_canvas = None
    
    for child in vodacom_frame.winfo_children():
        if isinstance(child, tk.Canvas):
            vodacom_canvas = child
            
    for child in mtn_frame.winfo_children():
        if isinstance(child, tk.Canvas):
            mtn_canvas = child
    
    # Set the provider
    selected_provider.set(provider_name)
    
    # Update UI to show which provider is selected
    if provider_name == "Vodacom":
        # Change Vodacom border to orange (selected) and restore MTN to its default
        vodacom_frame.config(bg=COLORS["selected"], relief=tk.RAISED)
        mtn_frame.config(bg=COLORS["card_bg"], relief=tk.FLAT)
        
        # Update border colors and animation
        if vodacom_canvas:
            # Apply 3D effect to Vodacom (move forward)
            apply_3d_effect(vodacom_canvas, "Vodacom", True)
            
        if mtn_canvas:
            # Reset MTN to normal
            reset_to_normal(mtn_canvas, "MTN")
            
    else:  # MTN
        # Change MTN border to orange (selected) and restore Vodacom to its default
        vodacom_frame.config(bg=COLORS["card_bg"], relief=tk.FLAT)
        mtn_frame.config(bg=COLORS["selected"], relief=tk.RAISED)
        
        # Update border colors and animation
        if vodacom_canvas:
            # Reset Vodacom to normal
            reset_to_normal(vodacom_canvas, "Vodacom")
            
        if mtn_canvas:
            # Apply 3D effect to MTN (move forward)
            apply_3d_effect(mtn_canvas, "MTN", True)

def apply_3d_effect(canvas, provider_name, forward=True):
    """Apply 3D effect to the logo by making it larger and updating the border.
    
    Args:
        canvas (tk.Canvas): Canvas containing the logo
        provider_name (str): The name of the provider ('Vodacom' or 'MTN')
        forward (bool): Whether to apply forward effect or return to normal
    """
    # Update border with the new selected logo border color
    canvas.config(
        highlightthickness=4,
        highlightbackground=COLORS["selected_logo_border"],  # Using light green for selected logo
        highlightcolor=COLORS["selected_logo_border"]
    )
    
    # Clear all existing items on the canvas
    canvas.delete("all")
    
    # Get the enlarged image
    enlarged_img = logo_enlarged_images.get(provider_name)
    if not enlarged_img:
        print(f"WARNING: Enlarged image for {provider_name} not found")
        return
    
    # Get canvas dimensions
    width = canvas.winfo_width()  
    height = canvas.winfo_height()
    if width <= 1:  # Canvas not yet drawn
        width = int(canvas['width'])
        height = int(canvas['height'])
        
    # Draw the image centered
    canvas.create_image(width/2, height/2, image=enlarged_img, anchor=tk.CENTER, tags="logo")
    
    # Update the display
    canvas.update()

def reset_to_normal(canvas, provider_name):
    """Reset the logo to its normal state.
    
    Args:
        canvas (tk.Canvas): Canvas containing the logo
        provider_name (str): The name of the provider ('Vodacom' or 'MTN')
    """
    # Updated border colors for the new light background
    canvas.config(
        highlightthickness=3,
        highlightbackground=COLORS["accent"],
        highlightcolor=COLORS["accent"]
    )
    
    # Clear all existing items on the canvas
    canvas.delete("all")
    
    # Get the original image
    orig_img = logo_original_images.get(provider_name)
    if not orig_img:
        print(f"WARNING: Original image for {provider_name} not found")
        return
    
    # Get canvas dimensions
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width <= 1:  # Canvas not yet drawn
        width = int(canvas['width'])
        height = int(canvas['height'])
        
    # Draw the image centered
    canvas.create_image(width/2, height/2, image=orig_img, anchor=tk.CENTER, tags="logo")
    
    # Update the display
    canvas.update()

def create_logo_canvas(parent, color, provider_name, width=100, height=100):
    """Create a logo canvas that displays the provider's PNG logo.
    
    Args:
        parent (tk.Widget): Parent widget for the canvas
        color (str): HEX color code for the fallback logo
        provider_name (str): Name of the provider ('Vodacom' or 'MTN')
        width (int, optional): Canvas width. Defaults to 100.
        height (int, optional): Canvas height. Defaults to 100.
        
    Returns:
        tk.Canvas: The created logo canvas
    """
    print(f"Creating logo for provider: {provider_name}")
    
    # Set the border color for the light gray background
    border_color = COLORS["accent"]  # Light blue border
    
    # Create canvas with a colored border and WHITE background for logos
    canvas = tk.Canvas(parent, width=width, height=height, bg="white", 
                       highlightthickness=2, highlightbackground=border_color,
                       highlightcolor=border_color, cursor="hand2")
    
    # Store original canvas configuration
    canvas_original_configs[provider_name] = {
        "highlightthickness": 2,
        "highlightbackground": border_color,
        "highlightcolor": border_color
    }
      # Define the path to the logo image
    logo_filename = f"{provider_name.lower()}.png"
    
    # Use the resource_path helper to get the correct path whether we're running from source or as a frozen app
    logo_path = resource_path(os.path.join("tt_sim_import", "assets", logo_filename))
    
    print(f"Attempting to load logo from: {logo_path}")
    
    try:
        # Try to load the PNG logo
        if os.path.exists(logo_path):
            print(f"Found logo file for {provider_name}: {logo_path}")
            # Open the image using PIL
            pil_image = Image.open(logo_path)
            
            print(f"Loaded logo image for {provider_name}: {pil_image.size} {pil_image.mode}")
            
            # Resize the image to fit the canvas while maintaining aspect ratio
            # Reduce size slightly to account for border
            img_width, img_height = pil_image.size
            inner_width = width - 6  # Account for border thickness
            inner_height = height - 6
            ratio = min(inner_width/img_width, inner_height/img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            # Create normal size image - ensure each image has its own instance
            normal_pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            normal_tk_image = ImageTk.PhotoImage(normal_pil_image)
            
            # Create enlarged image (10% larger) for 3D effect - ensure each image has its own instance
            enlarged_width = int(new_width * 1.10)
            enlarged_height = int(new_height * 1.10)
            enlarged_pil_image = pil_image.resize((enlarged_width, enlarged_height), Image.Resampling.LANCZOS)
            enlarged_tk_image = ImageTk.PhotoImage(enlarged_pil_image)
            
            # Save references to prevent garbage collection - use separate variables for each provider
            logo_images[provider_name] = normal_tk_image
            logo_original_images[provider_name] = normal_tk_image
            logo_enlarged_images[provider_name] = enlarged_tk_image
            
            print(f"Created images for {provider_name}:")
            print(f"  - Normal: {id(normal_tk_image)} - {normal_tk_image.width()}x{normal_tk_image.height()}")
            print(f"  - Enlarged: {id(enlarged_tk_image)} - {enlarged_tk_image.width()}x{enlarged_tk_image.height()}")
            
            # Add the image to the canvas
            canvas.create_image(width/2, height/2, anchor=tk.CENTER, image=normal_tk_image, tags="logo")
            
            print(f"Successfully created logo on canvas for {provider_name}")
        else:
            print(f"ERROR: Logo file not found for {provider_name}: {logo_path}")
            # Fallback to the original circle with letter if image not found
            canvas.create_oval(10, 10, width-10, height-10, fill=color, outline="")
            canvas.create_text(width/2, height/2, text=provider_name[0], 
                               font=('Segoe UI', 36, 'bold'), fill="white", tags="logo")
    except Exception as e:
        print(f"ERROR loading logo for {provider_name}: {str(e)}")
        # Fallback to the original circle with letter if there's an error
        canvas.create_oval(10, 10, width-10, height-10, fill=color, outline="")
        canvas.create_text(width/2, height/2, text=provider_name[0], 
                           font=('Segoe UI', 36, 'bold'), fill="white", tags="logo")
    
    return canvas