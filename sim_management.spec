# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

# Add the data files, especially our assets
added_files = [
    ('tt_sim_import\\assets\\*.png', 'tt_sim_import\\assets'),
    ('tt_sim_import\\assets\\*.ico', 'tt_sim_import\\assets'),
    ('tt_sim_import\\*.py', 'tt_sim_import'),  # Include all Python modules
]

# Get the current directory
current_dir = os.path.abspath('.')
tt_sim_import_dir = os.path.join(current_dir, 'tt_sim_import')

a = Analysis(
    ['tt_sim_import/main.py'],  # Main script to execute
    pathex=[
        current_dir,
        tt_sim_import_dir,
        os.path.join(current_dir, 'tt_sim_import'),
        'c:\\Users\\ryadya\\Conda\\Scripts\\TT_Import_Sims\\TT_Sim_Import_Conversion',
    ],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk', 
        'tkinter.messagebox',
        'tkinter.filedialog',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'pandas',
        'numpy',
        'tt_sim_import',
        'tt_sim_import.gui',
        'tt_sim_import.constants',
        'tt_sim_import.providers',
        'tt_sim_import.import_utils',
        'tt_sim_import.export_utils',
        'tt_sim_import.resource_path',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SIM_Management',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for a windowed application (no console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='tt_sim_import/assets/app_icon.ico',  # Set the app icon
)
