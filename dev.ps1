# Define venv directory:
$venvDir = ".\venv"

# Activate virtual environment:
$venvActivate = "$venvDir\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & $venvActivate
} else {
    Write-Host "Failed to activate virtual environment. Please check your Python installation." -ForegroundColor Red
}

# Set PYTHONPATH to the current directory
$env:PYTHONPATH = Get-Location

# Optionally, print it to verify it's set correctly
Write-Host "PYTHONPATH is set to: $env:PYTHONPATH"
