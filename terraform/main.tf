terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.8.0"
    }
  }
}

# Configure the Microsoft Azure Provider:
provider "azurerm" {
  features {
    key_vault {
        purge_soft_delete_on_destroy    = true
        recover_soft_deleted_key_vaults = true
        }
    }
}

# Retrieve information about the currently authenticated Azure client:
data "azurerm_client_config" "current" {}

output "tenant_id" {
  value = data.azurerm_client_config.current.tenant_id
}

output "object_id" {
  value = data.azurerm_client_config.current.object_id
}

# Create a resource group:
resource "azurerm_resource_group" "framework_rg" {
  name     = "framework-j1"
  location = "uksouth"
}

# Create Data Lake with Hierarchical Namespace:
resource "azurerm_storage_account" "fj1_storage" {
  name                     = "fj1adlsdevuks"
  resource_group_name      = azurerm_resource_group.framework_rg.name
  location                 = azurerm_resource_group.framework_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = "true"
}

# Create storage container for project:
resource "azurerm_storage_container" "fj1_container" {
  name                  = "vivaldi"
  storage_account_name    = azurerm_storage_account.fj1_storage.name
  container_access_type = "private"
}

# Create SaS token:
data "azurerm_storage_account_blob_container_sas" "j1SaS" {
  connection_string = azurerm_storage_account.fj1_storage.primary_connection_string
  container_name    = azurerm_storage_container.fj1_container.name
  https_only        = true


  start  = formatdate("YYYY-MM-DD", timestamp())
  expiry = "2050-01-01"

  permissions {
    read   = true
    add    = true
    create = true
    write  = true
    delete = true
    list   = true
  }

  cache_control       = "max-age=5"
  content_disposition = "inline"
  content_encoding    = "deflate"
  content_language    = "en-UK"
  content_type        = "application/json"
}


# Create a KeyVault with access policies:
resource "azurerm_key_vault" "fj1kv" {
  name                        = "fj1-kv-dev-uks"
  location                    = azurerm_resource_group.framework_rg.location
  resource_group_name         = azurerm_resource_group.framework_rg.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"

  # Create access policy to be able to store SaS token:
    access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    # MAKE DYNAMIC:
    object_id = "8801808f-99b4-415e-9635-9f06c85f4603"
    # MAKE DYNAMIC:
    secret_permissions = ["Backup", "Delete", "Get", "List", "Purge", "Recover", "Restore", "Set"]
}
  
  timeouts {
    create = "30m"
  }
  depends_on = [ data.azurerm_storage_account_blob_container_sas.j1SaS ]
}

# # Store SaS token in KeyVault
resource "azurerm_key_vault_secret" "storeSaS" {
  name         = "fj1-kv-adls"
  value        = data.azurerm_storage_account_blob_container_sas.j1SaS.sas
  key_vault_id = azurerm_key_vault.fj1kv.id
# Ensure keyvault created first:
  depends_on = [azurerm_key_vault.fj1kv]
}