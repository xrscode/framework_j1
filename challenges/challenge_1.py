from src.files.utility_functions import query_database

"""
This is the first challenge.  Contract generation. 
By running this script, the csv files for Adventure Works will be set to a 
'challenge' state - where students will have to work to complete the contracts.

This script will perform the following actions:

1. Reset the metadata database and remove Adventure Works source systems 
and entities. 

2.  Check that the AdventureWorks challenge 'csv' files exist. 

3.  If they do, delete data from them. 
"""

# First remove adventure works from metadata database if exists:
query = """
-- Create source system id variable first
DECLARE @ssid INT;

IF EXISTS (SELECT 1 FROM dbo.sourceSystem WHERE sourceSystemName = 'AdventureWorks')
BEGIN
    PRINT 'AdventureWorks exists.';

    -- Save source system id variable:
    SELECT @ssid = sourceSystemID
    FROM dbo.sourceSystem
    WHERE sourceSystemName = 'AdventureWorks';

    -- Print source system id:
    PRINT CONCAT('AdventureWorks sourceSystemID is: ', @ssid);

    -- Now delete from entity table
    DELETE FROM dbo.sourceEntity WHERE sourceSystemID = @ssid;
    DELETE FROM dbo.sourceSystem WHERE sourceSystemID = @ssid;
END
ELSE
BEGIN
    PRINT 'AdventureWorks not found.';
END 
"""

# Call query:
results = query_database('metadata', query)
print(results)