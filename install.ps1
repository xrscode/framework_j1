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

# Call functions:
# Install Chocolatey
Install-Chocolatey

# Install Terraform
Install-Terraform

# Define Terraform directory
$terraformDir = ".\terraform"

# Run Terraform deployment
if (Test-Path $terraformDir) {
    # Write-Host "Navigating to Terraform directory..." -ForegroundColor Cyan
    # Set-Location $terraformDir

    # Write-Host "Initializing Terraform..." -ForegroundColor Yellow
    # terraform init

    # Write-Host "Planning Terraform deployment..." -ForegroundColor Yellow
    # terraform plan

    # Write-Host "Applying Terraform deployment..." -ForegroundColor Yellow
    # terraform apply -auto-approve

    # Write-Host "Terraform deployment completed!" -ForegroundColor Green
} else {
    Write-Host "Terraform directory not found. Please ensure './terraform' exists." -ForegroundColor Red
}
