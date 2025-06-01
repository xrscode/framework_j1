# This script prompts the user to update the repository. Original repo:
# https://github.com/xrscode/framework_j
# It will pull the changes in and merge them into the current main branch.
# It will then push the updated main branch to your origin repository on GitHub.

# Enable script to stop on any error
$ErrorActionPreference = 'Stop'

# Ask the user if they want to check for updates
$updatePrompt = Read-Host "🔄 Do you want to check for and apply updates? (y/n)"
if ($updatePrompt -notin @("y", "Y", "yes", "YES")) {
    Write-Host "❌ Skipping update process." -ForegroundColor Yellow
    exit 0
}

try {
    # 1. Check if 'upstream' remote exists
    Write-Host "Checking if 'upstream' remote exists..." -ForegroundColor Yellow
    $remotes = git remote
    if (-not ($remotes -contains "upstream")) {
        Write-Host "Upstream remote not found. Adding it now..." -ForegroundColor Yellow
        git remote add upstream https://github.com/xrscode/framework_j1
        Write-Host "Upstream set to: https://github.com/xrscode/framework_j1" -ForegroundColor Cyan
    }

    # 2. Fetch the latest changes from upstream
    Write-Host "Fetching latest changes from upstream..." -ForegroundColor Green
    git fetch upstream
    if ($LASTEXITCODE -ne 0) { throw "Failed to fetch from upstream." }

    # 3. Checkout the local main branch
    Write-Host "Switching to 'main' branch..." -ForegroundColor Green
    git checkout main
    if ($LASTEXITCODE -ne 0) { throw "Failed to checkout 'main' branch." }

    # 4. Merge upstream/main into local main
    Write-Host "Merging changes from upstream/main..." -ForegroundColor Green
    git merge upstream/main
    if ($LASTEXITCODE -ne 0) { throw "Merge failed. Please resolve conflicts manually." }

    Write-Host "✅ Merge successful." -ForegroundColor Green

    # 5. Push the updated main to origin
    Write-Host "Pushing changes to origin/main..." -ForegroundColor Green
    git push origin main
    if ($LASTEXITCODE -ne 0) { throw "Failed to push to origin. Check authentication or network connection." }

    Write-Host "✅ Push to origin successful." -ForegroundColor Green

    # 6. Cleanup: remove upstream remote
    Write-Host "Cleaning up: Removing 'upstream' remote..." -ForegroundColor Yellow
    git remote remove upstream
    if ($LASTEXITCODE -ne 0) { throw "Failed to remove 'upstream' remote." }

    Write-Host "🧹 Upstream remote removed." -ForegroundColor Cyan
}
catch {
    Write-Host "`n❌ ERROR: $_" -ForegroundColor Red
    exit 1
}
