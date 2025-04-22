Write-Host "Logging in with following command:" -ForegroundColor Yellow
Write-Host "az login --tenant 6771b25a-f4d8-4f9f-9fcc-e7468a5cdc46" -ForegroundColor Cyan

# Add the az login command to authenticate to Azure, use Telefonica tenant_id:
az login --tenant 6771b25a-f4d8-4f9f-9fcc-e7468a5cdc46

# Check if the .env exists.  If it does, delete:
$envFile = ".\.env"  # Define the file name

Write-Host "Checking for .env..."
# Check if the .env file exists
if (Test-Path $envFile) {
    Write-Host ".env file found. Deleting..." -ForegroundColor Yellow
    Remove-Item $envFile -Force
    Write-Host ".env file deleted." -ForegroundColor Green
} else {
    Write-Host "No .env file found.  Deletion unnecessary." -ForegroundColor Green
}

# Define Terraform directory
$terraformDir = ".\terraform"

# Run Terraform deployment
if (Test-Path $terraformDir) {
    Write-Host "Navigating to Terraform directory..." -ForegroundColor Yellow
    Set-Location $terraformDir

    # Prompt user for confirmation
    $confirmation = Read-Host "Are you sure you want to destroy the Terraform deployment? (y/n)"3.
    
    if ($confirmation -eq "y") {
        Write-Host "Destroying Terraform deployment..." -ForegroundColor Yellow
        terraform destroy -auto-approve
        Write-Host "Framework destruction completed!" -ForegroundColor Green
    } else {
        Write-Host "Operation canceled. Terraform deployment remains intact." -ForegroundColor Cyan
        Set-Location "..\"
    }
} else {
    Write-Host "Terraform directory not found. Please ensure './terraform' exists." -ForegroundColor Red
}

Set-Location ..

Write-Host "Logging out with the following command:" -ForegroundColor Yellow
Write-Host "az logout" -ForegroundColor Cyan

# Logout
az logout