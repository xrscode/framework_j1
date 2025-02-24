# Create ADF instance:
resource "azurerm_data_factory" "adf" {
  name                = "fj1-adf-dev-uks-${random_string.random_storage_account.result}"
  location           = azurerm_resource_group.framework_rg.location
  resource_group_name = azurerm_resource_group.framework_rg.name
   identity {
    type = "SystemAssigned"
  }
}
