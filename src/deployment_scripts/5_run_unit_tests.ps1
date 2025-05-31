# Get current script directory (e.g., ...\src\scripts)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go two levels up to root
$rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Define the test directory path relative to the root
$testDir = Join-Path $rootDir "src\tests"

Write-Host "Running tests in: $testDir" -ForegroundColor Cyan

# Run pytest on all tests in the test directory
pytest $testDir

# Check if pytest exited with an error
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Tests failed! Aborting Terraform deployment." -ForegroundColor Red
    exit 1
}

Write-Host "✅ All tests passed! Proceeding with Terraform deployment...✅" -ForegroundColor Green
