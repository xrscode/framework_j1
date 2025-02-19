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
data "azurerm_storage_account_sas" "j1SaS" {
  connection_string = azurerm_storage_account.fj1_storage.primary_connection_string
  https_only        = true
  start             = formatdate("YYYY-MM-DD", timestamp())
  expiry            = formatdate("YYYY-MM-DD", timeadd(timestamp(), "35040h"))  # 4 years
  signed_version = "2022-11-02"

  services {
    blob  = true
    queue = true
    table = true
    file  = true
  }   # Allow Blob storage
  resource_types {
    service   = true
    container = true
    object    = true
  }  # Allow access to Service, Container, Object

  permissions {
    read   = true
    add    = true
    create = true
    write  = true
    delete = true
    list   = true
    update = true  # Added
    process = true # Added
    filter = true
    tag = true
  }
}