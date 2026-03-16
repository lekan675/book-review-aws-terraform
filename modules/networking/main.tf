data "aws_availability_zones" "azs" {
  state = "available"
}

resource "aws_vpc" "book-review-vpc" {

  cidr_block           = var.vpc_cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.project}-vpc"
  }
}


resource "aws_subnet" "web_subnet_1" {

  vpc_id                  = aws_vpc.book-review-vpc.id
  cidr_block              = var.web_subnet_1_cidr
  availability_zone       = data.aws_availability_zones.azs.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name        = "${var.project}-web-subnet-1"
  }
}


resource "aws_subnet" "web_subnet_2" {

  vpc_id                  = aws_vpc.book-review-vpc.id
  cidr_block              = var.web_subnet_2_cidr
  availability_zone       = data.aws_availability_zones.azs.names[1]
  map_public_ip_on_launch = true

  tags = {
    Name        = "${var.project}-web-subnet-2"
  }
}

resource "aws_subnet" "app_subnet_1" {
  vpc_id            = aws_vpc.book-review-vpc.id
  availability_zone = data.aws_availability_zones.azs.names[0]
  cidr_block        = var.app_subnet_1_cidr 

  tags = {
    Name        = "${var.project}-app-subnet-1"
  }
}

resource "aws_subnet" "app_subnet_2" {
  vpc_id            = aws_vpc.book-review-vpc.id
  availability_zone = data.aws_availability_zones.azs.names[1]
  cidr_block        = var.app_subnet_2_cidr 

  tags = {
    Name        = "${var.project}-app-subnet-2"
  }
}


resource "aws_subnet" "db_subnet_1" {
  vpc_id            = aws_vpc.book-review-vpc.id
  availability_zone = data.aws_availability_zones.azs.names[0]
  cidr_block        = var.db_subnet_1_cidr 

  tags = {
    Name        = "${var.project}-db-subnet-1"
  }
}

resource "aws_subnet" "db_subnet_2" {
  vpc_id            = aws_vpc.book-review-vpc.id
  availability_zone = data.aws_availability_zones.azs.names[1]
  cidr_block        = var.db_subnet_2_cidr 

  tags = {
    Name        = "${var.project}-db-subnet-2"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.book-review-vpc.id

  tags = {
    Name = "${var.project}-igw"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.book-review-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public_rt_assoc_1" {
  subnet_id      = aws_subnet.web_subnet_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_rt_assoc_2" {
  subnet_id      = aws_subnet.web_subnet_2.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_eip" "nat_eip" {
  domain = "vpc"
  depends_on = [
    aws_internet_gateway.igw
  ]

  tags = {
    Name = "${var.project}-nat-eip"
  }
}

resource "aws_nat_gateway" "nat_gw" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.web_subnet_1.id

  tags = {
    Name = "${var.project}-nat-gw"
  }
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.book-review-vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gw.id
  }
}

resource "aws_route_table_association" "private_rt_assoc_1" {
  subnet_id      = aws_subnet.app_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}
resource "aws_route_table_association" "private_rt_assoc_2" {
  subnet_id      = aws_subnet.app_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}
resource "aws_route_table_association" "private_rt_assoc_3" {
  subnet_id      = aws_subnet.db_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}
resource "aws_route_table_association" "private_rt_assoc_4" {
  subnet_id      = aws_subnet.db_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}