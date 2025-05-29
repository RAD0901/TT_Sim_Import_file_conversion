#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to convert PNG to ICO file for Windows application icon
"""

from PIL import Image
import os

def create_ico():
    # Source PNG file
    png_path = os.path.join('tt_sim_import', 'assets', 'New_Amecor_Logo.png')
    
    # Target ICO file
    ico_path = os.path.join('tt_sim_import', 'assets', 'app_icon.ico')
    
    # Load the image and convert to icon with multiple sizes
    img = Image.open(png_path)
    
    # Create different icon sizes
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
    img.save(ico_path, format='ICO', sizes=icon_sizes)
    
    print(f"Icon created successfully at {ico_path}")

if __name__ == "__main__":
    create_ico()
