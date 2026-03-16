output "book_review_vpc_id" {
  value = aws_vpc.book-review-vpc.id
}

output "web_subnet_1_id" {
  value = aws_subnet.web_subnet_1.id
}

output "web_subnet_2_id" {
  value = aws_subnet.web_subnet_2.id
}
output "app_subnet_1_id" {
  value = aws_subnet.app_subnet_1.id 
}

output "app_subnet_2_id" {
  value = aws_subnet.app_subnet_2.id 
}
output "db_subnet_1_id" {
  value = aws_subnet.db_subnet_1.id 
}
output "db_subnet_2_id" {
  value = aws_subnet.db_subnet_2.id
}
output "vpc_id" {
  value = aws_vpc.book-review-vpc.id
}
