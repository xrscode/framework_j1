# Setup the metadata database:
$pythonScript = ".\src\files\1_setup_metadata_database.py"
if (Test-Path $pythonScript) {
    Write-Host "Running Python script: $pythonScript" -ForegroundColor Cyan
    python $pythonScript
    Write-Host "Python script execution completed!" -ForegroundColor Green
} else {
    Write-Host "Python script not found at '$pythonScript'. Skipping execution." -ForegroundColor Red
}

# Setup the totesys database:
$pythonScript = ".\src\files\2_setup_totesys_database.py"
if (Test-Path $pythonScript) {
    Write-Host "Running Python script: $pythonScript" -ForegroundColor Cyan
    python $pythonScript
    Write-Host "Python script execution completed!" -ForegroundColor Green
} else {
    Write-Host "Python script not found at '$pythonScript'. Skipping execution." -ForegroundColor Red
}