-- Purpose: Create the sourceSystem table.

-- Remove the existing table if it exists
DROP TABLE IF EXISTS sourceSystem;

-- Create the sourceSystem table
CREATE TABLE sourceSystem (
    sourceSystemID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-incrementing primary key
    sourceSystemName VARCHAR(255) NOT NULL UNIQUE, -- Unique source name
    sourceSystemDescription VARCHAR(255), -- Description of the source
    entityNames VARCHAR(255),
    keyVaultQuery VARCHAR(255), -- Keyvault secret Name
    notebooks VARCHAR(255)
);