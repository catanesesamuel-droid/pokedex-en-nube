terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.90"
    }
  }

  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstatepokedex1234"
    container_name       = "tfstate"
    key                  = "pokedex.terraform.tfstate"
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy    = true
      recover_soft_deleted_key_vaults = true
    }
  }
}

data "azurerm_client_config" "current" {}

# -------------------------------------------------------------
# Resource Group
# -------------------------------------------------------------

resource "azurerm_resource_group" "main" {
  name     = "rg-pokedex"
  location = "francecentral"
}

# -------------------------------------------------------------
# Cosmos DB — cuenta + base de datos + 4 contenedores
# -------------------------------------------------------------

resource "azurerm_cosmosdb_account" "main" {
  name                = "cosmos-pokedex"
  location            = "francecentral"
  resource_group_name = azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = "francecentral"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_sql_database" "main" {
  name                = "pokedex"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azurerm_cosmosdb_sql_container" "users" {
  name                = "users"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name
  partition_key_path  = "/id"
}

resource "azurerm_cosmosdb_sql_container" "favorites" {
  name                = "favorites"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name
  partition_key_path  = "/id"
}

resource "azurerm_cosmosdb_sql_container" "reports" {
  name                = "reports"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name
  partition_key_path  = "/id"
}

resource "azurerm_cosmosdb_sql_container" "team" {
  name                = "team"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name
  partition_key_path  = "/id"
}

# -------------------------------------------------------------
# Storage Account — requerido por Azure Functions
# -------------------------------------------------------------

resource "azurerm_storage_account" "main" {
  name                     = "stpokedex"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = "francecentral"
  account_tier             = "Standard"
  account_replication_type = "LRS"

  static_website {
    index_document     = "index.html"
    error_404_document = "error.html"
  }
}

# -------------------------------------------------------------
# Application Insights — monitoreo y logs
# -------------------------------------------------------------

resource "azurerm_log_analytics_workspace" "main" {
  name                = "law-pokedex"
  resource_group_name = azurerm_resource_group.main.name
  location            = "francecentral"
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_application_insights" "main" {
  name                = "appi-pokedex"
  resource_group_name = azurerm_resource_group.main.name
  location            = "francecentral"
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"
}

# -------------------------------------------------------------
# Key Vault — secretos seguros (COSMOS_KEY, JWT_SECRET)
# -------------------------------------------------------------

resource "azurerm_key_vault" "main" {
  name                       = "kv-pokedex2026"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = "francecentral"
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 7
  purge_protection_enabled   = false

  # Acceso para quien ejecuta Terraform (tú)
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = ["Get", "List", "Set", "Delete", "Purge", "Recover"]
  }
}

resource "azurerm_key_vault_secret" "cosmos_key" {
  name         = "cosmos-key"
  value        = azurerm_cosmosdb_account.main.primary_key
  key_vault_id = azurerm_key_vault.main.id
}

resource "azurerm_key_vault_secret" "jwt_secret" {
  name         = "jwt-secret"
  value        = var.jwt_secret
  key_vault_id = azurerm_key_vault.main.id
}

# -------------------------------------------------------------
# Azure Functions — Consumption Plan (Linux + Python 3.11)
# -------------------------------------------------------------

resource "azurerm_service_plan" "main" {
  name                = "asp-pokedex"
  resource_group_name = azurerm_resource_group.main.name
  location            = "francecentral"
  os_type             = "Linux"
  sku_name            = "Y1" # Consumption
}

resource "azurerm_linux_function_app" "main" {
  name                       = "func-pokedex"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = "francecentral"
  storage_account_name       = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key
  service_plan_id            = azurerm_service_plan.main.id

  # Identidad para leer secretos de Key Vault
  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      python_version = "3.11"
    }
    cors {
      allowed_origins     = ["*"]
      support_credentials = false
    }
  }

  app_settings = {
    # Runtime
    FUNCTIONS_WORKER_RUNTIME         = "python"
    FUNCTIONS_WORKER_RUNTIME_VERSION = "3.11"
    AzureWebJobsFeatureFlags         = "EnableWorkerIndexing"

    # Application Insights
    APPINSIGHTS_INSTRUMENTATIONKEY        = azurerm_application_insights.main.instrumentation_key
    APPLICATIONINSIGHTS_CONNECTION_STRING = azurerm_application_insights.main.connection_string

    # Cosmos DB — secretos desde Key Vault (no en texto plano)
    COSMOS_ENDPOINT = azurerm_cosmosdb_account.main.endpoint
    COSMOS_KEY      = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.cosmos_key.id})"
    COSMOS_DATABASE = azurerm_cosmosdb_sql_database.main.name

    # JWT — secreto desde Key Vault
    JWT_SECRET = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.jwt_secret.id})"
  }
}

# Dar acceso a Functions para leer secretos del Key Vault
resource "azurerm_key_vault_access_policy" "functions" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = azurerm_linux_function_app.main.identity[0].tenant_id
  object_id    = azurerm_linux_function_app.main.identity[0].principal_id

  secret_permissions = ["Get", "List"]
}

# -------------------------------------------------------------
# Static Web App — frontend
# NOTA: spaincentral no soporta Static Web Apps → westeurope
# -------------------------------------------------------------

#resource "azurerm_static_web_app" "main" {
#  name                = "swa-pokedex"
#  resource_group_name = azurerm_resource_group.main.name
#  location            = "westeurope" # ← corregido, spaincentral no está soportado
#  sku_tier            = "Free"
#  sku_size            = "Free"
#}
