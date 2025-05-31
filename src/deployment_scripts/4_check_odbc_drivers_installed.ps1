# Get the list of installed ODBC drivers
$odbcDrivers = Get-OdbcDriver -Platform 64-bit | Select-Object -ExpandProperty Name

# Define the driver you're looking for
$driverName = "ODBC Driver 18 for SQL Server"

# Check if the driver is installed
if ($odbcDrivers -contains $driverName) {
    Write-Host "The ODBC driver '$driverName' is installed." -ForegroundColor Yellow
} else {
    Write-Host "The 64-bit ODBC driver '$driverName' is NOT installed." -ForegroundColor Red
    Write-Host "Please install the driver: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16&redirectedfrom=MSDN" -ForegroundColor Red
    exit 1
}
