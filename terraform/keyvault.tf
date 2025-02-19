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

  
  timeouts {
    create = "30m"
  }
  depends_on = [ data.azurerm_storage_account_sas.j1SaS ]
}


# Perform a service principal lookup:
data "azuread_service_principal" "databricks" {
  display_name = "AzureDatabricks"
  depends_on = [ azurerm_databricks_workspace.dbs_workspace ]
}

# ACCESS POLICIES:

# # Access policy to store SaS token:
resource "azurerm_key_vault_access_policy" "sas_token_policy" {
  key_vault_id = azurerm_key_vault.fj1kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = var.object_id  # Use dynamic object_id

  secret_permissions = ["Backup", "Delete", "Get", "List", "Purge", "Recover", "Restore", "Set"]
}

# Access Policy Databricks:
resource "azurerm_key_vault_access_policy" "db_access_policy" {
  key_vault_id = azurerm_key_vault.fj1kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azuread_service_principal.databricks.object_id
  secret_permissions = ["Get", "List", "Set", "Delete", "Recover", "Backup", "Restore"]
  depends_on = [ data.azuread_service_principal.databricks ]
}

# Access Policy ADF:
resource "azurerm_key_vault_access_policy" "adf_keyvault_policy" {
  key_vault_id = azurerm_key_vault.fj1kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_data_factory.adf.identity.0.principal_id

  secret_permissions = ["Get", "List"]
  depends_on = [ azurerm_data_factory.adf ]
}











# STORE:
# Store sql server password in keyvault
resource "azurerm_key_vault_secret" "store_sql_password" {
  name = "sqlPassword"
  value = azurerm_mssql_server.fj1sqlserver.administrator_login_password
  key_vault_id = azurerm_key_vault.fj1kv.id
}

# Store sql user in keyvault
resource "azurerm_key_vault_secret" "store_sql_user" {
  name = "sqlUser"
  value = azurerm_mssql_server.fj1sqlserver.administrator_login
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [azurerm_key_vault.fj1kv]
}

# Store connection metadata string in keyvault:
resource "azurerm_key_vault_secret" "store_metadata_connection_string" {
  name = "metadataConnectionString"
  value = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:${azurerm_mssql_server.fj1sqlserver.name}.database.windows.net,1433;Database=${azurerm_mssql_database.fj1_database_metadata.name};Uid=${azurerm_mssql_server.fj1sqlserver.administrator_login};Pwd=${azurerm_mssql_server.fj1sqlserver.administrator_login_password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [azurerm_key_vault.fj1kv]
}

# Store connection totesys string in keyvault:
resource "azurerm_key_vault_secret" "store_totesys_connection_string" {
  name = "totesysConnectionString"
  value = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:${azurerm_mssql_server.fj1sqlserver.name}.database.windows.net,1433;Database=${azurerm_mssql_database.fj1_database_totesys.name};Uid=${azurerm_mssql_server.fj1sqlserver.administrator_login};Pwd=${azurerm_mssql_server.fj1sqlserver.administrator_login_password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [azurerm_key_vault.fj1kv]
}

# Store server name in keyvault:
resource "azurerm_key_vault_secret" "store_server_name" {
  name = "serverName"
  value = "${azurerm_mssql_server.fj1sqlserver.name}.database.windows.net"
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [azurerm_key_vault.fj1kv]
}

# Store metadata database name in keyvault:
resource "azurerm_key_vault_secret" "store_metadata_name" {
  name = "metadataDatabaseName"
  value = azurerm_mssql_database.fj1_database_metadata.name
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [azurerm_mssql_database.fj1_database_metadata]
}


# Store totesys database name in keyvault:
resource "azurerm_key_vault_secret" "store_totesys_name" {
  name = "totesysDatabaseName"
  value = azurerm_mssql_database.fj1_database_totesys.name
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [azurerm_mssql_database.fj1_database_totesys]
}

# Store SaS token in KeyVault
resource "azurerm_key_vault_secret" "storeSaS" {
  name         = "fj1-kv-adls"
  value        = data.azurerm_storage_account_sas.j1SaS.sas
  key_vault_id = azurerm_key_vault.fj1kv.id
# Ensure keyvault created first:
  depends_on = [azurerm_key_vault.fj1kv]
}

# Store storage account name in KeyVault:
resource "azurerm_key_vault_secret" "storeStorageName" {
  name         = "storageAccountName"
  value        = azurerm_storage_account.fj1_storage.name
  key_vault_id = azurerm_key_vault.fj1kv.id
# Ensure keyvault created first:
  depends_on = [azurerm_key_vault.fj1kv]
}

# Store container name in KeyVault:
resource "azurerm_key_vault_secret" "storeContainerName" {
  name         = "containerName"
  value        = azurerm_storage_container.fj1_container.name
  key_vault_id = azurerm_key_vault.fj1kv.id
# Ensure keyvault created first:
  depends_on = [azurerm_key_vault.fj1kv]
}

# Store Databricks PAT in KeyVault
resource "azurerm_key_vault_secret" "storePAT" {
  name = "databricks-junior-token"
  value = databricks_token.db_pat.token_value
  key_vault_id = azurerm_key_vault.fj1kv.id
  depends_on = [ databricks_token.db_pat, azurerm_key_vault_access_policy.db_access_policy ]
}
