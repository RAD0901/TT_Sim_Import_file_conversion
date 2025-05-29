# TT Simulation Import and Conversion Tool

A Python application for importing and converting simulation data.

## Overview

This tool provides functionality to import simulation data from various sources, convert it to different formats, and export the converted data to specified locations.

## Installation

1. Ensure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with the following command:

```bash
python sim_import.py -i INPUT_PATH [-o OUTPUT_PATH] [-f FORMAT] [-v]
```

### Arguments

- `-i, --input`: Input file or directory path (required)
- `-o, --output`: Output directory path (optional)
- `-f, --format`: Output format (default: 'default')
- `-v, --verbose`: Enable verbose output (optional)

## Example

```bash
python sim_import.py -i ./data/simulation_results -o ./converted_data -f csv -v
```

## Project Structure

```
tt_sim_import/
├── sim_import.py    # Main script
├── requirements.txt # Project dependencies
└── README.md        # This file
```

## Extending the Tool

To implement specific simulation import/conversion functionality, edit the following functions in `sim_import.py`:

- `import_simulation_data()`: Add logic to import specific simulation data formats
- `convert_simulation_data()`: Add logic to convert between different formats
- `export_simulation_data()`: Add logic to export data in the desired format