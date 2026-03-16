variable "db_subnet_1_id" { 
  description = "The ID of the first subnet for the RDS database"
  type        = string
  
}
variable "db_subnet_2_id" { 
  description = "The ID of the second subnet for the RDS database"
  type        = string
  
}


variable "project" {
  description = "The name of the project"
  type        = string
}

variable "allocated_storage" {
  description = "The allocated storage for the RDS database in gigabytes"
  type        = number
}
variable "db_name" {
  description = "The name of the RDS database"
  type        = string
}
variable "engine" {
  description = "The database engine to use (e.g., mysql, postgres)"
  type        = string
}
variable "engine_version" {
  description = "The version of the database engine to use"
  type        = string
}
variable "instance_class" {
  description = "The instance class for the RDS database (e.g., db.t3.micro)"
  type        = string
}
variable "username" {
  description = "The master username for the RDS database"
  type        = string
}
variable "password" {
  description = "The master password for the RDS database"
  type        = string
}
variable "db_sg_id" {
  description = "The ID of the security group for the RDS database"
  type        = string
}