# Check if Python is installed.  If it is not, exit.
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is not installed. Please install Python and try again." -ForegroundColor Red
    exit 1
}

# Check if terraform is installed.  If it is not, exit.
$terraform = Get-Command terraform -ErrorAction SilentlyContinue
if (-not $terraform) {
    Write-Host "Terraform is not installed. Please install Terraform.  If chocolatey is installed run the following command in the terminal: 'choco install terraform -y' " -ForegroundColor Yellow
    exit 1
}

# Get the list of installed ODBC drivers
$odbcDrivers = Get-OdbcDriver -Platform 64-bit | Select-Object -ExpandProperty Name

# Define the driver you're looking for
$driverName = "ODBC Driver 17 for SQL Server"

# Check if the driver is installed
if ($odbcDrivers -contains $driverName) {
    Write-Output "The ODBC driver '$driverName' is installed."
} else {
    Write-Output "The ODBC driver '$driverName' is NOT installed."
    Write-Output "Please install the driver: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16&redirectedfrom=MSDN"
    exit 1
}

$terraformTfvars = "./src/files/5_check_terraform_tfvars.py"
# Update git credentials:
if (Test-Path $terraformTfvars) {
    Write-Host "Running Python script: $terraformTfvars" -ForegroundColor Cyan
    python $terraformTfvars
    # Check if Python script failed
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python script failed! Stopping PowerShell execution." -ForegroundColor Red
        exit 1
    }
    Write-Host "Python script execution completed!" -ForegroundColor Green
} else {
    Write-Host "Python script not found at '$terraformTfvars'. Skipping execution." -ForegroundColor Red
    exit 1
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

# Set PYTHONPATH to the current directory
$env:PYTHONPATH = Get-Location

# Optionally, print it to verify it's set correctly
Write-Host "PYTHONPATH is set to: $env:PYTHONPATH"


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

# # Add the az login command to authenticate to Azure
# az login

# # Define Terraform directory
# $terraformDir = ".\terraform"

# # Run Terraform deployment
# if (Test-Path $terraformDir) {
#     Write-Host "Navigating to Terraform directory..." -ForegroundColor Cyan
#     Set-Location $terraformDir

#     Write-Host "Initializing Terraform..." -ForegroundColor Yellow
#     terraform init

#     Write-Host "Planning Terraform deployment..." -ForegroundColor Yellow
#     terraform plan

#     Write-Host "Applying Terraform deployment..." -ForegroundColor Yellow
#     terraform apply -auto-approve

#     Write-Host "Terraform deployment completed!" -ForegroundColor Green
# } else {
#     Write-Host "Terraform directory not found. Please ensure './terraform' exists." -ForegroundColor Red
# }

# Write-Host "Navigating out of the 'terraform' directory..." -ForegroundColor Cyan
# Set-Location ..

# # Setup the metadata database:
# $pythonScript = ".\src\files\1_setup_metadata_database.py"
# if (Test-Path $pythonScript) {
#     Write-Host "Running Python script: $pythonScript" -ForegroundColor Cyan
#     python $pythonScript
#     Write-Host "Python script execution completed!" -ForegroundColor Green
# } else {
#     Write-Host "Python script not found at '$pythonScript'. Skipping execution." -ForegroundColor Red
# }

# # Setup the totesys database:
# $pythonScript = ".\src\files\2_setup_totesys_database.py"
# if (Test-Path $pythonScript) {
#     Write-Host "Running Python script: $pythonScript" -ForegroundColor Cyan
#     python $pythonScript
#     Write-Host "Python script execution completed!" -ForegroundColor Green
# } else {
#     Write-Host "Python script not found at '$pythonScript'. Skipping execution." -ForegroundColor Red
# }