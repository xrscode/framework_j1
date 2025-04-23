# First upload source system:
$pythonScript = ".\src\files\3_upload_source_system_contract.py"
if (Test-Path $pythonScript) {
    Write-Host "Uploading source system contract..." -ForegroundColor Cyan
    python $pythonScript
    Write-Host "Source system contract uploaded successfully" -ForegroundColor Green
} else {
    Write-Host "Python script not found at '$pythonScript'. Skipping execution." -ForegroundColor Red
}

# Next upload source entity contracts:
$pythonScript = ".\src\files\4_upload_source_entity_contract.py"
if (Test-Path $pythonScript) {
    Write-Host "Uploading source entity contracts..." -ForegroundColor Cyan
    python $pythonScript
    Write-Host "Source entity contracts uploaded successfully" -ForegroundColor Green
} else {
    Write-Host "Python script not found at '$pythonScript'. Skipping execution." -ForegroundColor Red
}