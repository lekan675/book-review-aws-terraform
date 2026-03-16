output "web_server_pub_ip" {
  value = aws_instance.web_server.public_ip 
}

output "app_server_prvt_ip" {
  value = aws_instance.app_server.private_ip
}

output "web_server_instance_id" {
  value = aws_instance.web_server.id
}

output "app_server_instance_id" {
  value = aws_instance.app_server.id
}
