# Create databricks resource group:
resource "azurerm_databricks_workspace" "dbs_workspace" {
  name                        = "fj1-dbs-dev-uks"
  resource_group_name         = azurerm_resource_group.framework_rg.name
  location                    = azurerm_resource_group.framework_rg.location
  sku                         = "standard"
  
#   Ensure that SaS token has been stored first:
  depends_on = [ azurerm_key_vault_secret.storeSaS ]
}

# Create secret scope to allow access to keyvault:
resource "databricks_secret_scope" "sas_scope" {
  name = "sasscope"
  initial_manage_principal = "users"

  keyvault_metadata {
    resource_id = azurerm_key_vault.fj1kv.id
    dns_name    = azurerm_key_vault.fj1kv.vault_uri
  }
# Ensure that the keyvault has been setup first:
  depends_on = [ azurerm_key_vault.fj1kv ]
}

# Create a cluster:
resource "databricks_cluster" "low_cost_cluster" {
  cluster_name            = "fj1-db-cluster"
  spark_version           = "13.3.x-scala2.12"  # Latest LTS version, update if needed
  node_type_id            = "Standard_DS3_v2"   # Cheap VM type
  autotermination_minutes = 15                  # Auto-shutdown after 15 mins
  num_workers             = 0                   # Single-node mode (driver only)

  driver_node_type_id = "Standard_DS3_v2"  # Use the same cheap VM for the driver

  spark_conf = {
    "spark.databricks.cluster.profile" = "singleNode"  # Single-node mode for lowest cost
    "spark.master" = "local[*]"
  }

  custom_tags = {
    "Owner"   = "YourName"
    "Purpose" = "Cost-Optimized Databricks Cluster"
  }
}

# Create a PAT token
resource "databricks_token" "db_pat" {
  comment = "Terraform Provision"
  lifetime_seconds = 8640000
  depends_on = [ azurerm_data_factory.adf ]
}
