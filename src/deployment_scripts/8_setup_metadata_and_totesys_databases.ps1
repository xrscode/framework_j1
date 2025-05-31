# Get current script directory (e.g., ...\src\scripts)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go up two levels to root (from scripts -> src -> root)
$rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Setup the metadata database:
$metadataScript = Join-Path $rootDir "src\files\1_setup_metadata_database.py"
if (Test-Path $metadataScript) {
    Write-Host "Running Python script: $metadataScript. Creating metadata database..." -ForegroundColor Cyan
    python $metadataScript

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Metadata database setup completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Metadata database setup failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Python script not found at '$metadataScript'. Skipping execution." -ForegroundColor Red
    exit 1
}

# Setup the totesys database:
$totesysScript = Join-Path $rootDir "src\files\2_setup_totesys_database.py"
if (Test-Path $totesysScript) {
    Write-Host "Running Python script: $totesysScript. Populating TotesysDB database..." -ForegroundColor Cyan
    python $totesysScript

    if ($LASTEXITCODE -eq 0) {
        Write-Host "TotesysDB database setup completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "TotesysDB database setup failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Python script not found at '$totesysScript'. Skipping execution." -ForegroundColor Red
    exit 1
}
