variable "web_sg_id" {
  description = "Security group ID for web servers"
  type        = string 
}
variable "app_sg_id" {
  description = "Security group ID for app servers"
  type        = string 
}

variable "web_subnet_1_id" {
  description = "Subnet ID for the first web subnet"
  type        = string 
  
}
variable "web_subnet_2_id" {
  description = "Subnet ID for the second web subnet"
  type        = string 
}
variable "app_subnet_1_id" {
  description = "Subnet ID for the first app subnet"
  type        = string 
}
variable "app_subnet_2_id" {
  description = "Subnet ID for the second app subnet"
  type        = string 
}
variable "keyname" {
  description = "Name of the SSH key pair to use for EC2 instances"
  type        = string
}
variable "web_instance_type" {
  description = "The instance type for web servers"
  type        = string
}
variable "app_instance_type" {
  description = "The instance type for app servers"
  type        = string
}
variable "project" {
  description = "The name of the project"
  type        = string
}