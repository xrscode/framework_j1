# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is not installed. Please install Python and try again." -ForegroundColor Red
    exit 1
}

# Install VENV:
# Define the virtual environment directory:
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

# Install chocolatey:
function Install-Chocolatey {
    $choco = Get-Command choco -ErrorAction SilentlyContinue
    if (-not $choco) {
        Write-Host "Chocolatey is not installed. Installing now..." -ForegroundColor Yellow
        Set-ExecutionPolicy Bypass -Scope Process -Force
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        
        # Refresh the environment to recognize Chocolatey
        $env:Path += ";C:\ProgramData\chocolatey\bin"
    } else {
        Write-Host "Chocolatey is already installed." -ForegroundColor Green
    }
}

# Function to install Terraform using Chocolatey if not installed
function Install-Terraform {
    $terraform = Get-Command terraform -ErrorAction SilentlyContinue
    if (-not $terraform) {
        Write-Host "Terraform is not installed. Installing via Chocolatey..." -ForegroundColor Yellow
        choco install terraform -y
    } else {
        Write-Host "Terraform is already installed." -ForegroundColor Green
    }
}

# Add the az login command to authenticate to Azure
az login

# Call functions:
# Install Chocolatey
Install-Chocolatey

# Install Terraform
Install-Terraform

# Define Terraform directory
$terraformDir = ".\terraform"

# Run Terraform deployment
if (Test-Path $terraformDir) {
    Write-Host "Navigating to Terraform directory..." -ForegroundColor Cyan
    Set-Location $terraformDir

    Write-Host "Initializing Terraform..." -ForegroundColor Yellow
    terraform init

    Write-Host "Planning Terraform deployment..." -ForegroundColor Yellow
    terraform plan

    Write-Host "Applying Terraform deployment..." -ForegroundColor Yellow
    terraform apply -auto-approve

    Write-Host "Terraform deployment completed!" -ForegroundColor Green
} else {
    Write-Host "Terraform directory not found. Please ensure './terraform' exists." -ForegroundColor Red
}

Write-Host "Navigating out of the 'terraform' directory..." -ForegroundColor Cyan
Set-Location ..

# Prompt the user for the Key Vault name
$KeyVaultName = Read-Host "Please enter your Key Vault name"

# Define the .env file path (assuming it's in the root directory)
$envFilePath = ".\.env"

# Check if the .env file exists, create it if not
if (-not (Test-Path $envFilePath)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    New-Item -Path $envFilePath -ItemType File | Out-Null
}

# Read the current content of the .env file
$envContent = Get-Content $envFilePath -Raw

# Define the Key Vault entry
$envEntry = "k-v_name=$KeyVaultName"

# Check if a k-v_name entry already exists, update it, otherwise append
if ($envContent -match "k-v_name=") {
    # Replace existing line correctly
    $envContent = $envContent -replace "k-v_name=.*", $envEntry
} else {
    # Append new line (ensuring proper format)
    $envContent += "`n" + $envEntry
}

# Write the updated content back to the .env file
$envContent | Set-Content $envFilePath

Write-Host "Updated .env file with Key Vault name: $KeyVaultName" -ForegroundColor Green

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