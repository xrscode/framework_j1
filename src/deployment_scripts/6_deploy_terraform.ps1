# Get current script directory (e.g., ...\src\scripts)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go two levels up to root
$rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Define Terraform directory relative to root
$terraformDir = Join-Path $rootDir "terraform"

# Check if the Terraform directory exists
if (Test-Path $terraformDir) {
    Write-Host "Navigating to Terraform directory..." -ForegroundColor Cyan
    Set-Location $terraformDir

    # Check if Terraform has already been initialized
    $terraformStateDir = Join-Path $terraformDir ".terraform"
    if (Test-Path $terraformStateDir) {
        Write-Host "Terraform already initialized. Running 'terraform refresh'..." -ForegroundColor Yellow
        terraform refresh
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Terraform refresh failed!" -ForegroundColor Red
            Set-Location $rootDir
            exit 1
        }
        Write-Host "Terraform refresh complete." -ForegroundColor Green
    }
    else {
        # Run full deployment process since no prior init was detected
        Write-Host "Initializing Terraform..." -ForegroundColor Yellow
        terraform init
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Terraform initialization failed! Aborting deployment." -ForegroundColor Red
            Set-Location $rootDir
            exit 1
        }

        Write-Host "Planning Terraform deployment..." -ForegroundColor Yellow
        terraform plan
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Terraform plan failed! Aborting deployment." -ForegroundColor Red
            Set-Location $rootDir
            exit 1
        }

        Write-Host "Applying Terraform deployment..." -ForegroundColor Yellow
        terraform apply -auto-approve
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Terraform apply failed! Aborting deployment." -ForegroundColor Red
            Set-Location $rootDir
            exit 1
        }

        Write-Host "🚀 Deployment complete!" -ForegroundColor Green
    }

    # Return to root directory after deployment or refresh
    Write-Host "Navigating out of the 'terraform' directory..." -ForegroundColor Cyan
    Set-Location $rootDir
}
else {
    Write-Host "Terraform directory not found at '$terraformDir'. Please ensure the 'terraform' folder exists in the root." -ForegroundColor Red
    exit 1
}
