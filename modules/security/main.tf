resource "aws_security_group" "pub_alb_sg" {

  name_prefix = "pub-alb-sg-"
  description = "Security group for public ALB in the book review app"
  vpc_id      = var.book_review_vpc_id


  tags = {
    Name = "${var.project}-pub-alb-sg"
  }
}

resource "aws_security_group_rule" "pub_alb_sg_inbound" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.pub_alb_sg.id
}
resource "aws_security_group_rule" "pub_alb_sg_egress_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.pub_alb_sg.id
}


resource "aws_security_group" "web_sg" {

  name_prefix = "web-sg-"
  description = "Security group for web servers in the book review app"
  vpc_id      = var.book_review_vpc_id


  tags = {
    Name = "${var.project}-web-sg"
  }
}

resource "aws_security_group_rule" "web_sg_inbound" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  source_security_group_id = aws_security_group.pub_alb_sg.id
  security_group_id        = aws_security_group.web_sg.id
}

resource "aws_security_group_rule" "web_sg_ssh_inbound" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id        = aws_security_group.web_sg.id
}

resource "aws_security_group_rule" "web_sg_egress_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.web_sg.id
}

resource "aws_security_group" "internal_alb_sg" {

  name_prefix = "internal-alb-sg"
  description = "Security group for internal ALB in the book review app"
  vpc_id      = var.book_review_vpc_id
  tags = {
    Name = "${var.project}-internal-alb-sg"
  }
}

resource "aws_security_group_rule" "internal_alb_sg_inbound" {
  type              = "ingress"
  from_port         = 3001
  to_port           = 3001
  protocol          = "tcp"
  source_security_group_id = aws_security_group.web_sg.id
  security_group_id        = aws_security_group.internal_alb_sg.id
}
resource "aws_security_group_rule" "internal_alb_sg_egress_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.internal_alb_sg.id
}

resource "aws_security_group" "app_sg" {

  name_prefix = "app-sg-"
  description = "Security group for app servers in the book review app"
  vpc_id      = var.book_review_vpc_id
  tags = {
    Name = "${var.project}-app-sg"
  }
}

resource "aws_security_group_rule" "app_sg_inbound" {
  type              = "ingress"
  from_port         = 3001
  to_port           = 3001
  protocol          = "tcp"
  source_security_group_id = aws_security_group.internal_alb_sg.id
  security_group_id        = aws_security_group.app_sg.id
}

resource "aws_security_group_rule" "app_sg_ssh_inbound" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  source_security_group_id = aws_security_group.web_sg.id
  security_group_id        = aws_security_group.app_sg.id
}

resource "aws_security_group_rule" "app_sg_egress_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.app_sg.id
}

resource "aws_security_group" "db_sg" {

  name_prefix = "db-sg-"
  description = "Security group for database servers in the book review app"
  vpc_id      = var.book_review_vpc_id
  tags = {
    Name = "${var.project}-db-sg"
  }
}

resource "aws_security_group_rule" "db_sg_inbound" {
  type              = "ingress"
  from_port         = 3306
  to_port           = 3306
  protocol          = "tcp"
  source_security_group_id = aws_security_group.app_sg.id
  security_group_id        = aws_security_group.db_sg.id
}
