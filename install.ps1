# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is not installed. Please install Python and try again." -ForegroundColor Red
    exit 1
}

# Function to install Terraform using Chocolatey if not installed
function Install-Terraform {
    $terraform = Get-Command terraform -ErrorAction SilentlyContinue
    if (-not $terraform) {
        Write-Host "Terraform is not installed. Please install Terraform.  If chocolatey is installed run the following command in the terminal: 'choco install terraform -y' " -ForegroundColor Yellow
        exit 1
    }
}

# Define venv directory:
$venvDir = ".\venv"

# If venv does not exist create:
if (-not (Test-Path $venvDir)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv $venvDir
}

# Activate virtual environment:
$venvActivate = "$venvDir\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & $venvActivate
} else {
    Write-Host "Failed to activate virtual environment. Please check your Python installation." -ForegroundColor Red
}

# Install requirements if requirements.txt exists
$requirementsFile = ".\requirements.txt"
if (Test-Path $requirementsFile) {
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    python -m pip install -r $requirementsFile
    Write-Host "All dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "No requirements.txt file found. Skipping dependency installation." -ForegroundColor Red
}

# Add the az login command to authenticate to Azure
az login

# Define Terraform directory
$terraformDir = ".\terraform"

# Run Terraform deployment
if (Test-Path $terraformDir) {
    Write-Host "Navigating to Terraform directory..." -ForegroundColor Cyan
    Set-Location $terraformDir

    # Write-Host "Initializing Terraform..." -ForegroundColor Yellow
    # terraform init

    # Write-Host "Planning Terraform deployment..." -ForegroundColor Yellow
    # terraform plan

    # Write-Host "Applying Terraform deployment..." -ForegroundColor Yellow
    # terraform apply -auto-approve

    Write-Host "Terraform deployment completed!" -ForegroundColor Green
} else {
    Write-Host "Terraform directory not found. Please ensure './terraform' exists." -ForegroundColor Red
}

Write-Host "Navigating out of the 'terraform' directory..." -ForegroundColor Cyan
Set-Location ..

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