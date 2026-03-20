# Book Review Terraform IaC

Terraform infrastructure for deploying a 3-tier Book Review application on AWS:
- Public web tier (EC2)
- Private app tier (EC2)
- Private database tier (RDS MySQL)
- Public + internal Application Load Balancers

## Architecture

![Architectural Diagram](assets/architetural-diagram.jpeg)

## Repository Structure

```text
.
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── deployment.md
├── scripts/
│   ├── frontend-userdata.sh.tpl
│   └── backend-userdata.sh.tpl
└── modules/
    ├── networking/
    ├── security/
    ├── ec2/
    ├── alb/
    └── database/
```

## What This Stack Provisions

### Networking (`modules/networking`)
- 1 VPC
- 2 public subnets (web tier)
- 2 private app subnets
- 2 private DB subnets
- Internet Gateway + NAT Gateway
- Public/private route tables and associations

### Security (`modules/security`)
- Public ALB SG (HTTP 80 from internet)
- Web SG (HTTP from public ALB, SSH open)
- Internal ALB SG (3001 from web tier)
- App SG (3001 from internal ALB, SSH from web tier)
- DB SG (3306 from app tier)

### Compute (`modules/ec2`)
- 1 public web EC2 instance
- 1 private app EC2 instance
- Ubuntu 24.04 AMI (latest Canonical image)
- User-data bootstrap for frontend and backend setup

### Load Balancing (`modules/alb`)
- Public ALB (port 80 -> web tier)
- Internal ALB (port 3001 -> app tier)
- Health checks:
  - Web target group: `/`
  - App target group: `/`

### Database (`modules/database`)
- RDS MySQL instance
- DB subnet group across private DB subnets
- DB name, username, and password supplied via Terraform variables

## Backend Runtime Configuration

The backend user-data template (`scripts/backend-userdata.sh.tpl`) now receives all DB connection fields from Terraform variables:
- `DB_HOST` from `module.database.db_endpoint`
- `DB_USER` from `var.username`
- `DB_PASS` from `var.password`
- `DB_NAME` from `var.db_name`

So database user/name are no longer hardcoded in the backend `.env` generation.

## Prerequisites

- Terraform CLI installed
- AWS CLI installed
- AWS credentials configured (`aws configure` or env vars)
- An existing EC2 key pair name in your target AWS region

## Required Variables (`terraform.tfvars`)

Example:

```hcl
aws_region     = "us-east-2"
project        = "book-review"
vpc_cidr_block = "10.0.0.0/16"

web_subnet_1_cidr = "10.0.1.0/24"
web_subnet_2_cidr = "10.0.2.0/24"
app_subnet_1_cidr = "10.0.10.0/24"
app_subnet_2_cidr = "10.0.11.0/24"
db_subnet_1_cidr  = "10.0.20.0/24"
db_subnet_2_cidr  = "10.0.21.0/24"

web_instance_type = "t3.micro"
app_instance_type = "t3.micro"

keyname = "infra"

allocated_storage = 20
db_name           = "book_review_db"
engine            = "mysql"
engine_version    = "8.4"
instance_class    = "db.t3.micro"
username          = "admin"
password          = "ChangeMe"
```

## Deploy

```bash
terraform init
terraform validate
terraform plan
terraform apply
```

## Useful Outputs

After apply:

```bash
terraform output
```

Available root outputs:
- `webserver_pub_ip`
- `appserver_prvt_ip`
- `db_endpoint`
- `public_alb_dns_name`
- `private_alb_dns_name`

## Destroy

```bash
terraform destroy
```

## Post-Infra App Deployment

For app-level deployment and operational checks, see:
- [deployment.md](deployment.md)

## Notes for Production Hardening

- Restrict SSH ingress (`0.0.0.0/0` is currently open for web SSH)
- Move DB credentials/JWT secret to AWS Secrets Manager or SSM Parameter Store
- Enable RDS final snapshots and stronger backup/retention policy
- Consider autoscaling groups instead of single EC2 instances per tier
