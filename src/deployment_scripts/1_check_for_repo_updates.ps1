# This file checks for updates to the main project at: 
# https://github.com/xrscode/framework_j
# It will pull the changes in and merge them into the current main branch. 
# It will then seek to push the updated main branch into your origin repo. 
# This is the repository in your github.

# 1. Check if 'upstream' remote exists:
$remotes = git remote
if (-not ($remotes -contains "upstream")) {
    Write-Host "Upstream remote not found.  Adding it now..."
    git remote add upstream https://github.com/xrscode/framework_j1
    Write-Host "Upstream set to: https://github.com/xrscode/framework_j1" -ForegroundColor Cyan
}

# 2. Pull latest changes:
Write-Host "Fetching latest changes from remote repository" -ForegroundColor Green
git fetch upstream

# 3. Checkout the main branch:
git checkout main

# 4. Merge changes from upstream/main
Write-Host "Merging upstream changes..." -ForegroundColor Green
git merge upstream/main
if ($LASTEXITCODE -eq 0) {
    Write-Host "Merge successful." -ForegroundColor Green

    # Try to push to origin/main
    Write-Host "Pushing updated main to origin..." -ForegroundColor Green
    git push origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Push to origin successful." -ForegroundColor Green
    } else {
        Write-Host "Unable to push main to origin. Please check your network connection or authentication." -ForegroundColor Red
    }

} else {
    Write-Host "Merge failed. Please resolve conflicts manually." -ForegroundColor Red
}

# 5. Remove upstream:
Write-Host "Cleaning up: Removing upstream remote..." -ForegroundColor Yellow
git remote remove upstream
Write-Host "Upstream remote removed." -ForegroundColor Cyan