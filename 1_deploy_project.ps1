# 1. Check for updates on upstream repository.
# & "$PSScriptRoot\src\deployment_scripts\1_check_for_repo_updates.ps1"

# 2. Check Python is installed.
& "$PSScriptRoot\src\deployment_scripts\2_check_python_installed.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python not installed.  Aborting deployment..." -ForegroundColor Red
    exit 1
}

# 3. Set the Pythonpath to the current directory.
# Set PYTHONPATH to the current directory
$env:PYTHONPATH = Get-Location
# # Optionally, print it to verify it's set correctly
Write-Host "PYTHONPATH is set to: $env:PYTHONPATH"


# 4. Install requirements:
$requirementsFile = ".\requirements.txt"
if (Test-Path $requirementsFile) {
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to upgrade pip. Exiting." -ForegroundColor Red
        exit 1
    }

    python -m pip install -r $requirementsFile
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Dependency installation failed. Exiting." -ForegroundColor Red
        exit 1
    }
    Write-Host "All dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "No requirements.txt file found. Skipping dependency installation." -ForegroundColor Red
}

# 5. Check Terraform is installed & env exists:
& "$PSScriptRoot\src\deployment_scripts\3_check_terraform_installed.ps1"

# 6. Check ODBC drivers:
& "$PSScriptRoot\src\deployment_scripts\4_check_odbc_drivers_installed.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ODBC not installed.  Aborting deployment..." -ForegroundColor Red
    exit 1
}

# 7. Run Unit tests:
& "$PSScriptRoot\src\deployment_scripts\5_run_unit_tests.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Unit tests failed.  Aborting deployment..." -ForegroundColor Red
    exit 1
}

# 8. Login to Azure using Data & Ai tenant:
Write-Host "Logging into Azure..." -ForegroundColor Cyan
az login --tenant 6771b25a-f4d8-4f9f-9fcc-e7468a5cdc46

if ($LASTEXITCODE -ne 0) {
    Write-Host "Azure login failed. Aborting deployment..." -ForegroundColor Red
    exit 1
}

# 9. Run Terraform deployment:
& "$PSScriptRoot\src\deployment_scripts\6_deploy_terraform.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Terraform deployment script failed. Aborting overall deployment." -ForegroundColor Red
    exit 1
}

# 10. Check ip address is valid:
& "$PSScriptRoot\src\deployment_scripts\7_check_ip_address.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Azure does not allow current ip address access... Aborting..." -ForegroundColor Red
    exit 1
}

# 11. Set up the metadata and totesys database:
& "$PSScriptRoot\src\deployment_scripts\8_setup_metadata_and_totesys_databases.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Unable to setup metadata/totesys database." -ForegroundColor Red
    exit 1
}

# 12. Update the ADF pipeline so linked services work:
& "$PSScriptRoot\src\deployment_scripts\9_update_adf_pipeline.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Unable to setup metadata/totesys database." -ForegroundColor Red
    exit 1
}



Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║       🎉  Junior Framework Deployment Complete! 🎉      ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║        ✅ All steps finished successfully! ✅           ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║        🔐 Check your .env file for user credentials. 🔐 ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║        🚀 Ready to process your data pipelines!  🚀     ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

