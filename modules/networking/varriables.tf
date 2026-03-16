variable "project" {
  description = "The name of the project"
  type        = string
}
variable "vpc_cidr_block" {
  description = "The CIDR block for the VPC"
  type        = string
  
}
variable "web_subnet_1_cidr" {
  description = "The CIDR block for the first web subnet"
  type        = string
}
variable "web_subnet_2_cidr" {
  description = "The CIDR block for the second web subnet"
  type        = string
}
variable "app_subnet_1_cidr" {
  description = "The CIDR block for the first app subnet"
  type        = string
}
variable "app_subnet_2_cidr" {
  description = "The CIDR block for the second app subnet"
  type        = string
}
variable "db_subnet_1_cidr" {
  description = "The CIDR block for the first db subnet"
  type        = string
}
variable "db_subnet_2_cidr" {
  description = "The CIDR block for the second db subnet"
  type        = string
}