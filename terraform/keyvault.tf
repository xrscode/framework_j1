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