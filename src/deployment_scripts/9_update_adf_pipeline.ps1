"
During deployment random names for resource group resource will be generated.
In order for the ADF pipeline to work without having to manually update
linked services.  The purpose of this script is to run 6_update_linked_serivce.
This script will make the modifications to the ADF pipeline and update the 
relevant information to the linked services. 

It will then try to push the changes onto the main branch so that when ADF
is opened and the main branch is selected from the GIT repo, the ETL pipeline
should work.
"

# Get current script directory (e.g., .\src\deployment_scripts)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go up two levels to root directory (deployment_scripts -> src -> root)
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
