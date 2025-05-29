#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the SIM Management application.
This module imports and uses functionality from the other modules.
"""

from gui import create_gui

if __name__ == "__main__":
    # Create the GUI and start the application
    root = create_gui()
    root.mainloop()