# Create a KeyVault with access policies:
resource "azurerm_key_vault" "fj1kv" {
  # Name random to ensure uniqueness:
  name                        = "fj1-kv-dev-uks-${random_string.random_storage_account.result}"
  location                    = azurerm_resource_group.framework_rg.location
  resource_group_name         = azurerm_resource_group.framework_rg.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"

  
  timeouts {
    create = "30m"
  }
  depends_on = [ data.azurerm_storage_account_sas.j1SaS ]

  # Enable RBAC:
  enable_rbac_authorization  = true
}


# RBAC:

# RBAC Databricks:
data "azuread_service_principal" "databricks" {
  display_name = "AzureDatabricks"
  depends_on = [ azurerm_databricks_workspace.dbs_workspace ]
}
resource "azurerm_role_assignment" "databricks_kv_admin" {
  scope                = azurerm_key_vault.fj1kv.id
  role_definition_name = "Key Vault Administrator"  # Grants full control
  principal_id         = data.azuread_service_principal.databricks.object_id
  depends_on = [ azurerm_key_vault.fj1kv, azurerm_databricks_workspace.dbs_workspace]
}

# RBAC ADF:
resource "azurerm_role_assignment" "adf_kv_admin" {
  scope                = azurerm_key_vault.fj1kv.id
  role_definition_name = "Key Vault Administrator"  # Grants full access to secrets, keys, and certificates
  principal_id         = azurerm_data_factory.adf.identity.0.principal_id
  depends_on = [ azurerm_key_vault.fj1kv, azurerm_data_factory.adf]
}

# RBAC User:
resource "azurerm_role_assignment" "user_kv_admin" {
  scope                = azurerm_key_vault.fj1kv.id
  role_definition_name = "Key Vault Administrator"  # Full access to secrets, keys, and certificates
  principal_id         = data.external.account_info.result.object_id
  depends_on = [ azurerm_key_vault.fj1kv]
}


# STORE:
# Store sql server password in keyvault
resource "azurerm_key_vault_secret" "store_sql_password" {
  name = "sqlPassword"
  value = azurerm_mssql_server.fj1sqlserver.administrator_login_password
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [ azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin ]
}

# Store sql user in keyvault
resource "azurerm_key_vault_secret" "store_sql_user" {
  name = "sqlUser"
  value = azurerm_mssql_server.fj1sqlserver.administrator_login
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [ azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin ]
}

# Store connection metadata string in keyvault:
resource "azurerm_key_vault_secret" "store_metadata_connection_string" {
  name = "metadataConnectionString"
  value = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:${azurerm_mssql_server.fj1sqlserver.name}.database.windows.net,1433;Database=${azurerm_mssql_database.fj1_database_metadata.name};Uid=${azurerm_mssql_server.fj1sqlserver.administrator_login};Pwd=${azurerm_mssql_server.fj1sqlserver.administrator_login_password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [ azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin ]
}

# Store connection totesys string in keyvault:
resource "azurerm_key_vault_secret" "store_totesys_connection_string" {
  name = "totesysConnectionString"
  value = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:${azurerm_mssql_server.fj1sqlserver.name}.database.windows.net,1433;Database=${azurerm_mssql_database.fj1_database_totesys.name};Uid=${azurerm_mssql_server.fj1sqlserver.administrator_login};Pwd=${azurerm_mssql_server.fj1sqlserver.administrator_login_password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [ azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin ]
}

# Store connection totesys string in keyvault in ADO format:
resource "azurerm_key_vault_secret" "store_totesys_connection_string_ADO" {
  name = "totesysConnectionStringADO"
  value = "Server=tcp:${azurerm_mssql_server.fj1sqlserver.name}.database.windows.net,1433;Database=${azurerm_mssql_database.fj1_database_totesys.name};User ID=${azurerm_mssql_server.fj1sqlserver.administrator_login};Password=${azurerm_mssql_server.fj1sqlserver.administrator_login_password};Encrypt=true;Connection Timeout=30;"
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [ azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin ]
}

# Store server name in keyvault:
resource "azurerm_key_vault_secret" "store_server_name" {
  name = "serverName"
  value = "${azurerm_mssql_server.fj1sqlserver.name}.database.windows.net"
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [ azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin ]
}

# Store metadata database name in keyvault:
resource "azurerm_key_vault_secret" "store_metadata_name" {
  name = "metadataDatabaseName"
  value = azurerm_mssql_database.fj1_database_metadata.name
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [azurerm_mssql_database.fj1_database_metadata, azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin]
}


# Store totesys database name in keyvault:
resource "azurerm_key_vault_secret" "store_totesys_name" {
  name = "totesysDatabaseName"
  value = azurerm_mssql_database.fj1_database_totesys.name
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [azurerm_mssql_database.fj1_database_totesys, azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin]
}

# Store SaS token in KeyVault
resource "azurerm_key_vault_secret" "storeSaS" {
  name         = "sastoken"
  value        = data.azurerm_storage_account_sas.j1SaS.sas
  key_vault_id = azurerm_key_vault.fj1kv.id
# Ensure keyvault created first:
  depends_on = [azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin]
}

locals {
  clean_sas_token = replace(data.azurerm_storage_account_sas.j1SaS.sas, "?", "")
  sas_url         = "https://${azurerm_storage_account.fj1_storage.name}.dfs.core.windows.net/?${local.clean_sas_token}"
}

resource "azurerm_key_vault_secret" "storeSaSURL" {
  name         = "sastokenURL"
  value        = local.sas_url
  key_vault_id = azurerm_key_vault.fj1kv.id

  depends_on = [
    azurerm_key_vault.fj1kv,
    azurerm_role_assignment.user_kv_admin
  ]
}

# Store storage account name in KeyVault:
resource "azurerm_key_vault_secret" "storeStorageName" {
  name         = "storageAccountName"
  value        = azurerm_storage_account.fj1_storage.name
  key_vault_id = azurerm_key_vault.fj1kv.id
# Ensure keyvault created first:
  depends_on = [azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin]
}

# Store container name in KeyVault:
resource "azurerm_key_vault_secret" "storeContainerName" {
  name         = "containerName"
  value        = azurerm_storage_container.fj1_container.name
  key_vault_id = azurerm_key_vault.fj1kv.id
# Ensure keyvault created first:
  depends_on = [azurerm_key_vault.fj1kv, azurerm_role_assignment.user_kv_admin]
}

# Store Databricks PAT in KeyVault
resource "azurerm_key_vault_secret" "storePAT" {
  name = "databricks-junior-token"
  value = databricks_token.db_pat.token_value
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [ databricks_token.db_pat, azurerm_role_assignment.databricks_kv_admin ]
}

# Store Databricks workspace url in KeyVault
resource "azurerm_key_vault_secret" "workspaceURL" {
  name = "databricks-workspace-url"
  value = azurerm_databricks_workspace.dbs_workspace.workspace_url
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [ databricks_token.db_pat, azurerm_role_assignment.databricks_kv_admin ]
}
