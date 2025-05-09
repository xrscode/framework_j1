terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.8.0"
    }
    databricks = {
      source = "databricks/databricks"
    }
    
  }
}

# Configure the Microsoft Azure Provider:
provider "azurerm" {
  features {
    key_vault {
        purge_soft_delete_on_destroy    = true
        recover_soft_deleted_key_vaults = false
        }
    resource_group {prevent_deletion_if_contains_resources = false}    
    }
    
}

provider "databricks" {
  host = azurerm_databricks_workspace.dbs_workspace.workspace_url
}

# Retrieve information about the currently authenticated Azure client:
data "azurerm_client_config" "current" {}

# Create a resource group:
resource "azurerm_resource_group" "framework_rg" {
  name     = "fj1-rg-uks-${random_string.random_storage_account.result}"
  location = "uksouth"
  # Possible locations:
  # uksouth
  # northeurope
}

# Work around to get object_id:
data external account_info {
  program  = ["az", "ad", "signed-in-user", "show", "--query", "{object_id:id}", "-o", "json"]
}

# Random String:
resource "random_string" "random_storage_account" {
  length = 7
  special = false
  lower = true
  upper = false
}

# Random Password:
# Random String:
resource "random_string" "random_password" {
  length = 16
  special = true
  lower = true
  upper = true
}