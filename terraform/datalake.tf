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