# Check if Python is installed by looking for the 'python' command
try {
    $pythonCmd = Get-Command python -ErrorAction Stop
} catch {
    try {
        $pythonCmd = Get-Command python3 -ErrorAction Stop
    } catch {
        Write-Host "❌ Python is not installed. Please install Python and try again." -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Python is installed at: $($pythonCmd.Source)" -ForegroundColor Yellow

# Get the directory where the current script is located (e.g., '.\src\deployment_scripts')
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Move two directory levels up from the script directory (to project root)
$rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Define the virtual environment directory path
$venvDir = Join-Path $rootDir "venv"
Write-Host "📁 Virtual environment directory: $venvDir"

# Create virtual environment if it doesn't exist
if (-not (Test-Path $venvDir)) {
    Write-Host "🛠️ Creating virtual environment..." -ForegroundColor Cyan
    try {
        & $pythonCmd.Source -m venv $venvDir
    } catch {
        Write-Host "❌ Failed to create virtual environment. Aborting." -ForegroundColor Red
        exit 1
    }
}

# Define path to activation script
$venvActivate = Join-Path $venvDir "Scripts\Activate.ps1"

# Activate the virtual environment
if (Test-Path $venvActivate) {
    Write-Host "⚙️ Activating virtual environment..." -ForegroundColor Green
    try {
        & $venvActivate
        exit 0
    } catch {
        Write-Host "❌ Failed to activate virtual environment. Aborting." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ Activation script not found at: $venvActivate" -ForegroundColor Red
    exit 1
}
