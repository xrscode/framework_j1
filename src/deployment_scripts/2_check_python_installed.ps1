# Check if Python is installed by looking for the 'python' command
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

# If 'python' is not found, try looking for 'python3' (common on some systems)
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
}

# If neither 'python' nor 'python3' commands are found, exit the script with a message
if (-not $pythonCmd) {
    Write-Host "Python is not installed. Please install Python and try again." -ForegroundColor Red
    exit 1
} else {
    # If Python is found, output its executable path
    Write-Host "Python is installed at: $($pythonCmd.Source)" -ForegroundColor Yellow
}

# Get the directory where the current script is located (e.g., '.\src\scripts')
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Move two directory levels up from the script directory:
# From 'scripts' to 'src' and then from 'src' to the root project directory
$rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Define the virtual environment directory path at the root of the project (e.g., '.\venv')
$venvDir = Join-Path $rootDir "venv"

# Display the path where the virtual environment will be created or already exists
Write-Host "Virtual environment directory: $venvDir"

# Check if the virtual environment directory does not exist
if (-not (Test-Path $venvDir)) {
    # If it doesn't exist, create the virtual environment using the located Python executable
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    & $pythonCmd.Source -m venv $venvDir
}

# Define the path to the activation script inside the virtual environment (Windows-specific path)
$venvActivate = Join-Path $venvDir "Scripts\Activate.ps1"

# Check if the activation script exists
if (Test-Path $venvActivate) {
    # If it exists, activate the virtual environment in the current PowerShell session
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & $venvActivate
} else {
    # If the activation script is not found, output an error message
    Write-Host "Failed to activate virtual environment. Check Python installation and permissions." -ForegroundColor Red
}
