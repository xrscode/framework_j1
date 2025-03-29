# Define Terraform directory
$terraformDir = ".\terraform"

# Run Terraform deployment
if (Test-Path $terraformDir) {
    Write-Host "Navigating to Terraform directory..." -ForegroundColor Cyan
    Set-Location $terraformDir

    # Prompt user for confirmation
    $confirmation = Read-Host "Are you sure you want to destroy the Terraform deployment? (y/n)"
    
    if ($confirmation -eq "y") {
        Write-Host "Destroying Terraform deployment..." -ForegroundColor Yellow
        terraform destroy -auto-approve
        Write-Host "Framework destruction completed!" -ForegroundColor Green
    } else {
        Write-Host "Operation canceled. Terraform deployment remains intact." -ForegroundColor Cyan
    }
} else {
    Write-Host "Terraform directory not found. Please ensure './terraform' exists." -ForegroundColor Red
}

