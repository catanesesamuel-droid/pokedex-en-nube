variable "jwt_secret" {
  description = "Secreto para firmar JWT. Genera uno con: python -c \"import secrets; print(secrets.token_hex(32))\""
  type        = string
  sensitive   = true
}
