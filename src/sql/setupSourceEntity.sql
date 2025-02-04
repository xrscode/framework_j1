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
    entityIngestionNotebook VARCHAR(255), --Details notebook used to ingest data
    entityTransformNotebook VARCHAR(255), --Details notebook used to transform data
    entityCurationNotebook VARCHAR(255), --Details notebook used to curate data
    entityColumns NVARCHAR(MAX), --Columns in the entity
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP --Timestamp of when entity was created
);