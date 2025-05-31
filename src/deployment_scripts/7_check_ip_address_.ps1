# Get the current script directory (e.g., ...\src\scripts)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go up two levels to reach the root directory (from scripts -> src -> root)
$rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Define the full path to the Python script relative to root
$pythonScript = Join-Path $rootDir "src\files\check_db_connection.py"

# Check if the Python script exists
if (Test-Path $pythonScript) {
    Write-Host "Running Python script: $pythonScript. Checking connection..." -ForegroundColor Cyan
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
    exit 1
}
