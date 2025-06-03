# This script checks for updates from an upstream repository and merges them into the local main branch only if changes exist.
# It auto-resolves known conflict files using the upstream version (theirs).

$ErrorActionPreference = 'Stop'

# Prompt the user
$updatePrompt = Read-Host "🔄 Check if upstream repo: https://github.com/xrscode/framework_j1 has updates? (y/n)"
if ($updatePrompt -notin @("y", "Y", "yes", "YES")) {
    Write-Host "❌ Skipping update process." -ForegroundColor Yellow
    exit 0
}

try {
    # 1. Ensure 'upstream' remote exists
    Write-Host "Checking if 'upstream' remote exists..." -ForegroundColor Yellow
    $remotes = git remote
    if (-not ($remotes -contains "upstream")) {
        Write-Host "Upstream remote not found. Adding it now..." -ForegroundColor Yellow
        git remote add upstream https://github.com/xrscode/framework_j1
        Write-Host "Upstream set to: https://github.com/xrscode/framework_j1" -ForegroundColor Cyan
    }

    # 2. Fetch latest changes from upstream
    Write-Host "Fetching latest changes from upstream..." -ForegroundColor Green
    git fetch upstream
    if ($LASTEXITCODE -ne 0) { throw "Failed to fetch from upstream." }

    # 3. Checkout main branch
    Write-Host "Switching to 'main' branch..." -ForegroundColor Green
    git checkout main
    if ($LASTEXITCODE -ne 0) { throw "Failed to checkout 'main' branch." }

    # 4. Check for local changes
    Write-Host "🔍 Checking for local changes..." -ForegroundColor Yellow
    $hasLocalChanges = git status --porcelain | Where-Object { $_ -match '^[ MADRCU]' }

    if ($hasLocalChanges) {
        Write-Host "📦 Local changes detected. Stashing them before merge..." -ForegroundColor Yellow
        git stash push -m "Auto-stash before upstream merge"
        if ($LASTEXITCODE -ne 0) { throw "❌ Failed to stash local changes." }
        $stashed = $true
    } else {
        $stashed = $false
    }

    # 5. Check if upstream/main has updates
    Write-Host "Checking for updates between 'main' and 'upstream/main'..." -ForegroundColor Green
    $mergeBase = git merge-base main upstream/main
    git diff --quiet $mergeBase upstream/main
    $hasChanges = $LASTEXITCODE -ne 0

    if (-not $hasChanges) {
        Write-Host "✅ No updates found. Your branch is up to date with upstream." -ForegroundColor Cyan
    } else {
        # 6. Merge changes
        Write-Host "Merging changes from upstream/main..." -ForegroundColor Green
        git merge upstream/main
        $mergeExitCode = $LASTEXITCODE

        if ($mergeExitCode -ne 0) {
            Write-Host "⚠️ Merge resulted in conflicts. Attempting to auto-resolve specific files using 'theirs'..." -ForegroundColor Yellow

            # List of known conflict-prone files
            $conflictFiles = @(
                "linkedService/Azure Key Vault.json",
                "linkedService/Framework Databricks.json",
                "linkedService/Metadata Database.json"
            )

            foreach ($file in $conflictFiles) {
                if (Test-Path $file) {
                    $content = Get-Content $file -Raw
                    if ($content -match '<<<<<<< HEAD') {
                        Write-Host "🔁 Conflict in $file. Using upstream version ('theirs')." -ForegroundColor Cyan
                        git checkout --theirs "$file"
                        git add "$file"
                    }
                }
            }

            git commit -m "Auto-resolved known conflicts using upstream version"
            if ($LASTEXITCODE -ne 0) { throw "❌ Could not complete merge after auto-resolving." }

            Write-Host "✅ Merge completed with automatic conflict resolution." -ForegroundColor Green
        } else {
            Write-Host "✅ Merge successful with no conflicts." -ForegroundColor Green
        }

        # 7. Restore stashed changes if any
        if ($stashed) {
            Write-Host "🔄 Restoring previously stashed changes..." -ForegroundColor Yellow
            git stash pop
            if ($LASTEXITCODE -ne 0) {
                Write-Host "⚠️ Conflicts occurred when applying stashed changes. Please resolve manually." -ForegroundColor Red
            } else {
                Write-Host "✅ Stashed changes successfully reapplied." -ForegroundColor Green
            }
        }

        # 8. Push to origin
        Write-Host "Pushing changes to origin/main..." -ForegroundColor Green
        git push origin main
        if ($LASTEXITCODE -ne 0) { throw "Failed to push to origin. Check authentication or network connection." }

        Write-Host "✅ Push to origin successful." -ForegroundColor Green
    }

    # 9. Remove upstream remote
    Write-Host "Cleaning up: Removing 'upstream' remote..." -ForegroundColor Yellow
    git remote remove upstream
    if ($LASTEXITCODE -ne 0) { throw "Failed to remove 'upstream' remote." }

    Write-Host "🧹 Upstream remote removed." -ForegroundColor Cyan
}
catch {
    Write-Host "`n❌ ERROR: $_" -ForegroundColor Red
    exit 1
}
