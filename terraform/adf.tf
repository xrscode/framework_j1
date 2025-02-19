# Create ADF instance:
resource "azurerm_data_factory" "adf" {
  name                = "fj1-adf-dev-uks"
  location           = azurerm_resource_group.framework_rg.location
  resource_group_name = azurerm_resource_group.framework_rg.name
   identity {
    type = "SystemAssigned"
  }
}
