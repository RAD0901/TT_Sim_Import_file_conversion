@echo off
echo Installing required packages for SIM Card Management Portal...
pip install -r tt_sim_import\requirements.txt
pip install pillow
echo All packages installed successfully!
echo.
echo Press any key to close...
pause > nul
