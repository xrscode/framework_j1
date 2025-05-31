# Get current script directory (e.g., ...\src\scripts)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go up two levels to root directory (scripts -> src -> root)
$rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Define the full path to the Python script relative to the root directory
$pythonScript = Join-Path $rootDir "src\files\6_update_linked_service.py"

# Check if the Python script exists before running it
if (Test-Path $pythonScript) {
    Write-Host "Running Python script: $pythonScript." -ForegroundColor Cyan
    python $pythonScript

    # Check if Python script executed successfully
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python script execution completed!" -ForegroundColor Green
    } else {
        Write-Host "Python script execution failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Python script not found at '$pythonScript'. Skipping execution." -ForegroundColor Red
}

# Define the specific JSON files in linkedService folder relative to root
$filesToCommit = @(
    Join-Path $rootDir "linkedService\Azure Key Vault.json",
    Join-Path $rootDir "linkedService\Framework Databricks.json",
    Join-Path $rootDir "linkedService\Metadata Database.json"
)

Write-Host "Pushing specific changes to GitHub..." -ForegroundColor Cyan

# Add only the specified files to git staging area
git add $filesToCommit

# Commit the changes with a clear commit message
git commit -m 'Updated Linked Services'

# Push the committed changes to the main branch on origin
git push origin main
