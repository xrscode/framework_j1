-- Purpose: Create the sourceSystem table.

-- Remove the existing table if it exists
DROP TABLE IF EXISTS sourceSystem;

-- Create the sourceSystem table
CREATE TABLE sourceSystem (
    sourceEntityID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-incrementing primary key
    sourceEntityName VARCHAR(255) NOT NULL UNIQUE, -- Unique entity name
    sourceEntityDescription VARCHAR(255), -- Description of the entity
    keyVaultQuery VARCHAR(255) -- Keyvault secret Name
);