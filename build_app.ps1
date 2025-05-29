# Build script for SIM Management application
# PowerShell script to create the executable

Write-Host "================================================"
Write-Host "Building SIM Management Application Executable"
Write-Host "================================================"

# Check if PyInstaller is installed
try {
    $pyinstallerVersion = python -c "import PyInstaller; print(PyInstaller.__version__)" 2>$null
    if (-not $pyinstallerVersion) {
        Write-Host "PyInstaller not found. Installing..."
        pip install pyinstaller
    } else {
        Write-Host "Using PyInstaller version: $pyinstallerVersion"
    }
} catch {
    Write-Host "Installing PyInstaller..."
    pip install pyinstaller
}

# Create the application icon if it doesn't exist
$iconPath = ".\tt_sim_import\assets\app_icon.ico"
if (-not (Test-Path $iconPath)) {
    Write-Host "Creating application icon..."
    python create_ico.py
}

# Clean previous builds
Write-Host "Cleaning previous builds..."
if (Test-Path ".\build") { Remove-Item -Path ".\build" -Recurse -Force }
if (Test-Path ".\dist") { Remove-Item -Path ".\dist" -Recurse -Force }

# Build the executable using the spec file
Write-Host "Building executable..."
pyinstaller --clean --noconfirm sim_management.spec

# Check if build was successful
if (Test-Path ".\dist\SIM_Management.exe") {
    Write-Host "Build successful! Executable created at: .\dist\SIM_Management.exe"
    
    # Create a simple batch file to run the application
    $batchContent = @"
@echo off
echo Starting SIM Management Application...
start "" "SIM_Management.exe"
"@
    $batchContent | Out-File -FilePath ".\dist\Run_SIM_Management.bat" -Encoding ascii
    
    Write-Host "Created launcher batch file: .\dist\Run_SIM_Management.bat"
    Write-Host "`nDistribution ready in the 'dist' folder."
} else {
    Write-Host "Build failed. Executable not found." -ForegroundColor Red
}