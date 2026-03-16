variable "project" {
  description = "The name of the project"
  type        = string  
}
variable "vpc_id" {
  description = "The ID of the VPC where the ALB will be deployed"
  type        = string
} 

variable "web_subnet_1_id" {
  description = "The ID of the first subnet for the web servers"
  type        = string
} 

variable "web_subnet_2_id" {
  description = "The ID of the second subnet for the web servers"
  type        = string
} 
variable "app_subnet_1_id" {
  description = "The ID of the first subnet for the app servers"
  type        = string
}
variable "app_subnet_2_id" {
  description = "The ID of the second subnet for the app servers"
  type        = string
}
variable "internal_alb_sg_id" {
  description = "The ID of the security group for the internal ALB" 
  type        = string
}
variable "pub_alb_sg_id" {
  description = "The ID of the security group for the public ALB"
  type        = string
}   

variable "web_server_instance_id" {
  description = "The ID of the web server instance"
  type        = string
}

variable "app_server_instance_id" {
  description = "The ID of the app server instance"
  type        = string
}


