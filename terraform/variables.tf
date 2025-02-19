variable "git_user" {
    description = "The user for the github workspace."
    type = string
}

variable "git_pat" {
    description = "The pat token for the github workspace."
    type = string
}

variable "object_id" {
    description = "The object_id"
    type = string
}


variable "sql_user" {
    description = "The username for the SQL server"
    type = string
}

variable "sql_password" {
    description = "The password for the SQL server"
    type = string
}

variable "connection_string_metadata" {
    description = "Connection string for connecting to metadata database."
}