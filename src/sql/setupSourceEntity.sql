-- Purpose: Create the sourceEntity table.

-- Remove the existing table if it exists
DROP TABLE IF EXISTS sourceEntity;

-- Create the sourceEntity table
CREATE TABLE sourceEntity (
    entityID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-incrementing primary key
    entityName VARCHAR(255) NOT NULL UNIQUE, -- Unique entity name
    entityDescription VARCHAR(255), -- Description of the entity
    entitySourceQuery VARCHAR(255), -- Data to retrieve information from source
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP --Timestamp of when entity was created
);