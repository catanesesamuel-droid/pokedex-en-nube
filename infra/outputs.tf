output "function_app_url" {
  description = "URL base del backend (úsala en el frontend)"
  value       = "https://${azurerm_linux_function_app.main.default_hostname}/api"
}

#output "static_web_app_url" {
#  description = "URL del frontend"
#  value       = "https://${azurerm_static_web_app.main.default_host_name}"
#}

#output "static_web_app_api_key" {
#  description = "API Key para desplegar el frontend"
#  value       = azurerm_static_web_app.main.api_key
#  sensitive   = true
#}

output "frontend_url" {
  description = "URL del frontend (Static Website en Storage Account)"
  value       = "https://${azurerm_storage_account.main.primary_web_host}"
}

output "key_vault_name" {
  description = "Nombre del Key Vault"
  value       = azurerm_key_vault.main.name
}
