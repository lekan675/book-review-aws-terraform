variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr_block" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "project" {
  description = "The name of the project"
  type        = string
  default     = "book-review"
}

variable "web_subnet_1_cidr" {
  description = "The CIDR block for the first web subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "web_subnet_2_cidr" {
  description = "The CIDR block for the second web subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "app_subnet_1_cidr" {
  description = "The CIDR block for the first app subnet"
  type        = string
  default     = "10.0.3.0/24"
}

variable "app_subnet_2_cidr" {
  description = "The CIDR block for the second app subnet"
  type        = string
  default     = "10.0.4.0/24"
}

variable "db_subnet_1_cidr" {
  description = "The CIDR block for the first db subnet"
  type        = string
  default     = "10.0.5.0/24"
}

variable "db_subnet_2_cidr" {
  description = "The CIDR block for the second db subnet"
  type        = string
  default     = "10.0.6.0/24"
}

variable "keyname" {
  description = "Name of the SSH key pair to use for EC2 instances"
  type        = string
  default     = "book-review-key"
}

variable "web_instance_type" {
  description = "The instance type for web servers"
  type        = string
  default     = "t3.micro"
}

variable "app_instance_type" {
  description = "The instance type for app servers"
  type        = string
  default     = "t3.micro"
}

variable "allocated_storage" {
  description = "The allocated storage for the RDS database in gigabytes"
  type        = number
  default     = 20
}

variable "db_name" {
  description = "The name of the RDS database"
  type        = string
  default     = "bookreviewdb"
}

variable "engine" {
  description = "The database engine to use (e.g., mysql, postgres)"
  type        = string
  default     = "mysql"
}

variable "engine_version" {
  description = "The version of the database engine to use"
  type        = string
  default     = "8.0"
}

variable "instance_class" {
  description = "The instance class for the RDS database (e.g., db.t3.micro)"
  type        = string
  default     = "db.t3.micro"
}

variable "username" {
  description = "The master username for the RDS database"
  type        = string
  default     = "admin"
}

variable "password" {
  description = "The master password for the RDS database"
  type        = string
  sensitive   = true
}
