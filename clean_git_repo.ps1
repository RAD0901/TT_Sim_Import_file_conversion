# Clean Git Repository
# This script helps remove the large files from Git history

Write-Host "========================================================"
Write-Host "Cleaning Git repository of large files" -ForegroundColor Green
Write-Host "========================================================"
Write-Host

# Remove the large files from git tracking (but keep them locally)
Write-Host "Step 1: Removing large files from git tracking..." -ForegroundColor Cyan
git rm --cached "dist/SIM_Management.exe" 
git rm --cached "build/sim_management/SIM_Management.pkg"
git rm -r --cached build/
git rm -r --cached dist/

Write-Host
Write-Host "Step 2: Adding .gitignore to prevent future issues..." -ForegroundColor Cyan
git add .gitignore

Write-Host
Write-Host "Step 3: Creating a commit with these changes..." -ForegroundColor Cyan
git commit -m "Remove large files from git tracking and update .gitignore"

Write-Host
Write-Host "========================================================"
Write-Host "INSTRUCTIONS TO COMPLETE THE PROCESS:" -ForegroundColor Yellow
Write-Host "========================================================"
Write-Host
Write-Host "You still need to force-push these changes to your GitHub repository:" -ForegroundColor Yellow
Write-Host "git push -f origin main" -ForegroundColor White
Write-Host
Write-Host "NOTE: This will overwrite your remote history. Make sure this is acceptable." -ForegroundColor Red
Write-Host "If you are working with others on this repo, they will need to do: git pull --rebase" -ForegroundColor Yellow
Write-Host
Write-Host "For future large file distribution, consider using GitHub Releases" -ForegroundColor Green
Write-Host "or GitHub LFS (Large File Storage)."
Write-Host "========================================================"
