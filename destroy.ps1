# This file will delete the framework.
# Define Terraform directory
$terraformDir = ".\terraform"

# Run Terraform deployment
if (Test-Path $terraformDir) {
    Write-Host "Navigating to Terraform directory..." -ForegroundColor Cyan
    Set-Location $terraformDir

    Write-Host "Destroying Terraform deployment..." -ForegroundColor Yellow
    terraform destroy -auto-approve

    Write-Host "Framework destruction completed!" -ForegroundColor Green
} else {
    Write-Host "Terraform directory not found. Please ensure './terraform' exists." -ForegroundColor Red
}
