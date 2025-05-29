#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper module for handling resource paths in both development and PyInstaller frozen environments.
"""

import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # We are not running in a PyInstaller bundle
        base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    return os.path.join(base_path, relative_path)
