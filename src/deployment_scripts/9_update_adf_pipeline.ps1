# Get current script directory (e.g., ...\src\scripts)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go up two levels to root directory (scripts -> src -> root)
$rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Define the full path to the Python script relative to the root directory
$pythonScript = Join-Path $rootDir "src\files\6_update_linked_service.py"

Write-Host "Running Python script: $pythonScript." -ForegroundColor Cyan
python $pythonScript

# Check if the script executed successfully
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python script failed. Aborting Git operations." -ForegroundColor Red
    exit 1
}

# Define the specific JSON files in linkedService folder relative to root
$filesToCommit = @(
    Join-Path $rootDir "linkedService\Azure Key Vault.json"
    Join-Path $rootDir "linkedService\Framework Databricks.json"
    Join-Path $rootDir "linkedService\Metadata Database.json"
)

Write-Host "Staging specific Linked Service files for commit..." -ForegroundColor Cyan

# Add only the specified files to git staging area
git add $filesToCommit

# Check if there are any changes to commit
$gitStatus = git status --porcelain

if ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Write-Host "✅ No changes to commit. Working tree is clean." -ForegroundColor Yellow
    exit 0
}

# Commit the changes with a clear commit message
git commit -m 'Updated Linked Services'

# Push the committed changes to the main branch on origin
git push origin main

Write-Host "🚀 Changes pushed to GitHub successfully!" -ForegroundColor Green
