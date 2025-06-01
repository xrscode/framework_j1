try {
    # Run terraform version and capture all output
    $terraformOutput = terraform version 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Terraform version output:" -ForegroundColor Green
        Write-Host $terraformOutput

        # Check if output contains 'update' keyword (case-insensitive)
        if ($terraformOutput -match "(?i)update") {
            Write-Host ""
            Write-Host "⚠️ Terraform update detected!" -ForegroundColor Yellow
            Write-Host "ℹ️  Visit https://www.terraform.io/downloads.html to get the latest version." -ForegroundColor Yellow
            Write-Host "ℹ️  Or run: 'choco upgrade terraform' (in an elevated PowerShell window)." -ForegroundColor Yellow

            $userInput = Read-Host "❓ Do you want to continue with the current version? (y/n)"
            if ($userInput -notin @("y", "Y", "yes", "YES")) {
                Write-Host "🚫 Aborting script at user request due to outdated Terraform version." -ForegroundColor Red
                exit 2  # Exit with a custom code
            }

            Write-Host "✅ Continuing with current Terraform version..." -ForegroundColor Cyan
        }
        else {
            Write-Host "✅ Terraform is up to date." -ForegroundColor Green
        }

        exit 0
    }
    else {
        Write-Host "Terraform command found but failed to execute properly." -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "Terraform is not installed or not found in the system PATH." -ForegroundColor Red
    exit 1
}
