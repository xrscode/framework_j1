# Write to env file:
resource "local_file" "env_file" {
  filename = "../.env"
  content  = <<EOT
server_name="${azurerm_mssql_server.fj1sqlserver.name}.database.windows.net"

server_user = "${azurerm_mssql_server.fj1sqlserver.administrator_login}"

server_password = "${random_string.random_password.result}"

account_url = "https://${azurerm_storage_account.fj1_storage.name}.dfs.core.windows.net"

resource_group_name = "${azurerm_resource_group.framework_rg.name}"
databricks_workspace_url = "${azurerm_databricks_workspace.dbs_workspace.workspace_url}"
keyvault_name="${azurerm_key_vault.fj1kv.name}"
ip_address = "${data.http.my_ip.response_body}"
subscription_id = "${data.azurerm_client_config.current.subscription_id}"
totesysConnectionStringADO = "${azurerm_key_vault_secret.store_totesys_connection_string_ADO.value}"
dataLakeConnectionString = "${azurerm_key_vault_secret.storeSaSURL.value}"
databricksClusterID = "${databricks_cluster.low_cost_cluster.id}"
EOT
depends_on = [ azurerm_key_vault.fj1kv, azurerm_mssql_server.fj1sqlserver, 
azurerm_databricks_workspace.dbs_workspace, azurerm_resource_group.framework_rg,
databricks_cluster.low_cost_cluster ]
}