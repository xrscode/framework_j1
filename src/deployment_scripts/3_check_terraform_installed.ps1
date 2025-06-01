# Check if Terraform is installed by looking for the 'terraform' command
$terraform = Get-Command terraform -ErrorAction SilentlyContinue

# If Terraform is not found, display a message and exit the script
if (-not $terraform) {
    Write-Host "Terraform is not installed. Please install Terraform.  If chocolatey is installed run the following command in the terminal: 'choco install terraform -y' " -ForegroundColor Yellow
    exit 1
} else {
    # If Terraform is found, notify the user and continue
    Write-Host "Terraform is installed. Continuing with installation." -ForegroundColor Yellow
}

# First define root directory:
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Define the full path to the Python script responsible for checking terraform.tfvars,
# assuming $rootDir has been defined elsewhere to point to the project root directory
$terraformTfvars = Join-Path $rootDir "src\files\5_check_terraform_tfvars.py"

# Check if the Python script file exists at the specified location
if (Test-Path $terraformTfvars) {
    # Inform the user that the Python script is being executed
    Write-Host "Running Python script: $terraformTfvars" -ForegroundColor Cyan
    
    # Execute the Python script
    python $terraformTfvars
    
    # Check if the Python script exited with an error code (non-zero exit code)
    if ($LASTEXITCODE -ne 0) {
        # If there was an error, notify the user and stop PowerShell execution
        Write-Host "Python script failed! Stopping PowerShell execution." -ForegroundColor Red
        exit 1
    }
    
    # If the script ran successfully, notify the user
    Write-Host "Python script execution completed!" -ForegroundColor Green
} else {
    # If the Python script was not found, notify the user and exit the script
    Write-Host "Python script not found at '$terraformTfvars'. Skipping execution." -ForegroundColor Red
    exit 1
}
