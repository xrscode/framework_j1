# Create ADF instance:
resource "azurerm_data_factory" "adf" {
  name                = "fj1-adf-dev-uks-${random_string.random_storage_account.result}"
  location           = azurerm_resource_group.framework_rg.location
  resource_group_name = azurerm_resource_group.framework_rg.name
   identity {
    type = "SystemAssigned"
  }

  
  github_configuration {
    account_name = var.git_user
    branch_name = "main"
    repository_name = "framework_j1"
    root_folder = "/"
    # Use github.com for open source repositories:
    git_url = "https://github.com"
  }
}