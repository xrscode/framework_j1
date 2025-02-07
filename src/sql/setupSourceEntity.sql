-- Purpose: Create the sourceEntity table.

-- Remove the existing table if it exists
DROP TABLE IF EXISTS sourceEntity;

-- Create the sourceEntity table
CREATE TABLE sourceEntity (
    entityID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-incrementing primary key
    sourceEntityID INT NOT NULL, -- Foreign Key to sourceSystem
    entityName VARCHAR(255) NOT NULL UNIQUE, -- Unique entity name
    entityDescription VARCHAR(255), -- Description of the entity
    entitySourceQuery VARCHAR(255), -- Data to retrieve information from source
    entityColumns NVARCHAR(MAX), --Columns in the entity
    curationStages NVARCHAR(255),
    bronzeLocation VARCHAR(255),
    silverLocation VARCHAR(255),
    goldLocation VARCHAR(255)
);