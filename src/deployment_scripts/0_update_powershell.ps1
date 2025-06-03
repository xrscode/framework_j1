# Define the minimum required version
$MinimumVersionString = "7.0.0.0"

# Safely create a Version object for the minimum version
try {
    $MinimumVersion = New-Object System.Version($MinimumVersionString)
} catch {
    Write-Error "Failed to parse the minimum version string. Script aborted."
    return
}

# Fallback if $PSVersionTable or PSVersion key is missing
if (-not ($PSVersionTable -and $PSVersionTable.ContainsKey("PSVersion"))) {
    Write-Warning "Unable to determine PowerShell version. You may be running an older version."
    Write-Host "It is recommended to update to PowerShell $MinimumVersionString or later." -ForegroundColor Yellow
    Write-Host "Download it here: https://aka.ms/powershell" -ForegroundColor Cyan
    return
}

# Try to parse the current version safely
try {
    $CurrentVersion = New-Object System.Version($PSVersionTable.PSVersion.ToString())
} catch {
    Write-Warning "Could not parse current PowerShell version. You may be running an unsupported version."
    Write-Host "It is recommended to update to PowerShell $MinimumVersionString or later." -ForegroundColor Yellow
    Write-Host "Download it here: https://aka.ms/powershell" -ForegroundColor Cyan
    return
}

Write-Host "Current PowerShell version: $CurrentVersion"

# Compare versions
if ($CurrentVersion.CompareTo($MinimumVersion) -lt 0) {
    Write-Warning "Your PowerShell version is outdated."
    Write-Host "It is recommended to update to version $MinimumVersionString or later." -ForegroundColor Yellow
    Write-Host "Download the latest version here: https://aka.ms/powershell" -ForegroundColor Cyan
} else {
    Write-Host "Your PowerShell version is up to date." -ForegroundColor Green
}
