# SIM Card Management Portal

A tool for importing and managing SIM card data and exporting it in formats compatible with Techtool.

## Development Setup

1. Clone the repository:
```powershell
git clone https://github.com/RAD0901/TT_Sim_Import_file_conversion.git
cd TT_Sim_Import_file_conversion
```

2. Install required packages:
```powershell
pip install -r tt_sim_import/requirements.txt
pip install pillow
```

3. Run the application in development mode:
```powershell
python -m tt_sim_import.main
```

## Building the Application

To build the standalone executable:

```powershell
# Run the build script
./BuildApp.bat
```

This will create a `SIM_Management.exe` in the `dist` folder.

## Distribution Guidelines

### Important: Do NOT commit build files to Git

The compiled application and build files are large and should NOT be committed to Git. They are automatically ignored via the `.gitignore` file.

### Options for Distributing the Application

#### Option 1: GitHub Releases (Recommended)

After building the application:

1. Go to your GitHub repository
2. Click on "Releases" on the right side
3. Click "Create a new release"
4. Tag the version (e.g., v1.0.0)
5. Upload the `SIM_Management.exe` from your `dist` folder
6. Publish the release

Users can then download the executable directly from the GitHub Releases page.

#### Option 2: File Sharing Services

Upload the executable to a file sharing service like:
- Google Drive
- Dropbox
- Microsoft OneDrive

Share the download link with your users.

#### Option 3: GitHub LFS (Large File Storage)

For advanced users who want to track large files in Git:

1. Install Git LFS from https://git-lfs.com
2. Set up Git LFS in your repository:
```powershell
git lfs install
git lfs track "dist/SIM_Management.exe"
git lfs track "*.pkg"
git add .gitattributes
git commit -m "Set up Git LFS"
```

Note: GitHub LFS has storage and bandwidth quotas to be aware of.

## Troubleshooting Git Issues

If you encounter errors related to large files:

1. Run the provided cleanup script:
```powershell
./clean_git_repo.ps1
```

2. Follow the instructions provided by the script to complete the process.

## Application Features

- Import SIM card data from various providers (Vodacom, MTN)
- Convert data to Techtool-compatible formats
- Export processed data to CSV
- Modern user interface with provider selection

## License

[Insert your license information here]
