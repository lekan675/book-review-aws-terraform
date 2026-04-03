# Book Review App — Terraform IaC on AWS

A fully automated, three-tier cloud infrastructure for the **Book Review** web application, provisioned on AWS using Terraform. This project covers networking, compute, load balancing, database, and application bootstrap — everything needed to go from zero to a running app with a single `terraform apply`.

---

## Table of Contents

1. [What I Built](#what-i-built)
2. [Architecture](#architecture)
3. [Infrastructure Components](#infrastructure-components)
4. [Module Reference](#module-reference)
5. [Variable Reference](#variable-reference)
6. [User Data & App Bootstrap](#user-data--app-bootstrap)
7. [Traffic Flow](#traffic-flow)
8. [Getting Started](#getting-started)
9. [Outputs](#outputs)
10. [Security Considerations](#security-considerations)
11. [Common Operations](#common-operations)
12. [Troubleshooting](#troubleshooting)

---

## What I Built

This project automates the full AWS infrastructure for a three-tier web application:

### Problem Solved
Manually provisioning cloud infrastructure is slow, error-prone, and impossible to reproduce consistently. This IaC project solves that by codifying every resource — from VPC and subnets to load balancers and RDS — so the entire environment can be spun up or torn down repeatably.

### What Was Done

| Area | Work Done |
|------|-----------|
| **Project Structure** | Designed a modular Terraform layout with 5 independent modules |
| **Networking** | Created a custom VPC (`10.0.0.0/16`) with 6 subnets across 2 AZs — public (web), private (app), private (DB) |
| **Security** | Defined 5 security groups enforcing strict tier-to-tier traffic rules |
| **Compute** | Provisioned EC2 instances (Ubuntu 24.04 LTS, t3.micro) for web and app tiers |
| **Load Balancing** | Deployed a public-facing ALB (HTTP:80) and an internal ALB (HTTP:3001) |
| **Database** | Created an RDS MySQL 8.4 instance (db.t3.micro) in isolated private subnets |
| **SSH Key Management** | Automated RSA-4096 key generation, upload to AWS, and local `.pem` save |
| **App Bootstrap** | Wrote templated user data scripts that install Node.js, clone the app, configure env vars, and start processes via PM2 |
| **Nginx Reverse Proxy** | Configured Nginx on the web server to route `/api/*` to the internal ALB and `/*` to the Next.js frontend |
| **Dynamic Configuration** | Used `templatefile()` to inject ALB DNS names and DB credentials into user data at deploy time |

### Technology Stack

| Layer | Technology |
|-------|------------|
| IaC | Terraform >= 1.0, AWS Provider ~> 6.0 |
| Cloud | AWS (us-east-1) |
| OS | Ubuntu 24.04 LTS (Noble Numbat) |
| Web Server | Nginx |
| Frontend | Next.js (Node.js LTS) via PM2 |
| Backend API | Node.js (Express) on port 3001 via PM2 |
| Database | Amazon RDS MySQL 8.4 |
| Process Manager | PM2 |

---

## Architecture

```
                            ┌───────────────────────────────────────┐
                            │           INTERNET (0.0.0.0/0)        │
                            └──────────────────┬────────────────────┘
                                               │ HTTP :80
                                               ▼
                            ┌──────────────────────────────────────┐
                            │         PUBLIC ALB (public-alb)       │
                            │   web_subnet_1 (AZ-a) + web_subnet_2  │
                            │   SG: pub_alb_sg (0.0.0.0/0 → :80)  │
                            └──────────────────┬───────────────────┘
                                               │ HTTP :80
                  ╔════════════════════════════╧════════════════════════════╗
                  ║               WEB TIER — Public Subnets                 ║
                  ║                                                          ║
                  ║  ┌──────────────────────────────────────────────────┐   ║
                  ║  │  web_server  (EC2 t3.micro, Ubuntu 24.04)        │   ║
                  ║  │  Subnet: web_subnet_1  │  Public IP: yes         │   ║
                  ║  │  SG: web_sg                                       │   ║
                  ║  │                                                    │   ║
                  ║  │  Processes:                                        │   ║
                  ║  │   • Nginx :80  ──► /api/*  ──► internal ALB:3001 │   ║
                  ║  │                └─► /*      ──► localhost:3000     │   ║
                  ║  │   • Next.js frontend  (PM2, port 3000)            │   ║
                  ║  └──────────────────────────┬───────────────────────┘   ║
                  ╚═══════════════════════════════╪════════════════════════╝
                                                  │ HTTP :3001
                            ┌─────────────────────▼─────────────────────┐
                            │       INTERNAL ALB (private-alb)           │
                            │  app_subnet_1 (AZ-a) + app_subnet_2 (AZ-b) │
                            │  SG: internal_alb_sg (:3001 from web_sg)   │
                            └─────────────────────┬─────────────────────┘
                                                  │ HTTP :3001
                  ╔═══════════════════════════════╪════════════════════════╗
                  ║              APP TIER — Private Subnets                ║
                  ║                                                         ║
                  ║  ┌──────────────────────────────────────────────────┐  ║
                  ║  │  app_server  (EC2 t3.micro, Ubuntu 24.04)        │  ║
                  ║  │  Subnet: app_subnet_1  │  Public IP: no          │  ║
                  ║  │  SG: app_sg                                       │  ║
                  ║  │                                                    │  ║
                  ║  │  Processes:                                        │  ║
                  ║  │   • Node.js API  (PM2, port 3001)                 │  ║
                  ║  │   • Connects to RDS via env DB_HOST               │  ║
                  ║  └──────────────────────────┬───────────────────────┘  ║
                  ╚═══════════════════════════════╪═══════════════════════╝
                                                  │ MySQL :3306
                  ╔═══════════════════════════════╪════════════════════════╗
                  ║            DATABASE TIER — Private Subnets             ║
                  ║                                                         ║
                  ║  ┌──────────────────────────────────────────────────┐  ║
                  ║  │  RDS MySQL 8.4  (db.t3.micro)                    │  ║
                  ║  │  Subnets: db_subnet_1 (AZ-a), db_subnet_2 (AZ-b) │  ║
                  ║  │  SG: db_sg  (:3306 from app_sg only)             │  ║
                  ║  │  Database: bookreviewdb                           │  ║
                  ║  └──────────────────────────────────────────────────┘  ║
                  ╚══════════════════════════════════════════════════════╝

Outbound internet for private subnets: via NAT Gateway in web_subnet_1
```

![Architectural Diagram](assets/architetural-diagram.jpeg)

### Network Layout

| Subnet | CIDR | Type | Tier |
|--------|------|------|------|
| web_subnet_1 | 10.0.1.0/24 | Public | Web (AZ-a) |
| web_subnet_2 | 10.0.2.0/24 | Public | Web (AZ-b) |
| app_subnet_1 | 10.0.3.0/24 | Private | App (AZ-a) |
| app_subnet_2 | 10.0.4.0/24 | Private | App (AZ-b) |
| db_subnet_1  | 10.0.5.0/24 | Private | DB (AZ-a) |
| db_subnet_2  | 10.0.6.0/24 | Private | DB (AZ-b) |

---

## Infrastructure Components

### AWS Resources Provisioned (~40 total)

| Category | Resource | Count |
|----------|----------|-------|
| **Networking** | VPC | 1 |
| | Subnets (public + private) | 6 |
| | Internet Gateway | 1 |
| | NAT Gateway | 1 |
| | Elastic IP (NAT) | 1 |
| | Route Tables | 2 |
| | Route Table Associations | 6 |
| **Security** | Security Groups | 5 |
| **Compute** | EC2 Instances (t3.micro) | 2 |
| | SSH Key Pair | 1 |
| **Load Balancing** | Application Load Balancers | 2 |
| | Target Groups | 2 |
| | ALB Listeners | 2 |
| | Target Group Attachments | 2 |
| **Database** | RDS MySQL Instance (db.t3.micro) | 1 |
| | DB Subnet Group | 1 |

---

## Module Reference

### Project Structure

```
book-review-terraform-iac/
├── main.tf                          # Root orchestration, SSH key, module calls
├── variables.tf                     # Root variable definitions
├── outputs.tf                       # Root outputs
├── terraform.tfvars                 # Variable values (gitignored — contains secrets)
├── .gitignore
├── assets/
│   └── architetural-diagram.jpeg
├── scripts/
│   ├── frontend-userdata.sh.tpl     # Web server bootstrap template
│   └── backend-userdata.sh.tpl      # App server bootstrap template
└── modules/
    ├── networking/   (main.tf, variables.tf, outputs.tf)
    ├── security/     (main.tf, variables.tf, outputs.tf)
    ├── ec2/          (main.tf, variables.tf, outputs.tf)
    ├── alb/          (main.tf, variables.tf, outputs.tf)
    └── database/     (main.tf, variables.tf, outputs.tf)
```

---

### Module 1 — `networking`

**Purpose:** Foundation layer. Creates the VPC, all subnets, internet access, and NAT.

**Creates:**
- VPC with DNS hostnames enabled
- 2 public subnets (web tier) — `map_public_ip_on_launch = true`
- 2 private subnets (app tier)
- 2 private subnets (DB tier)
- Internet Gateway (IGW) → attached to VPC
- Elastic IP + NAT Gateway → placed in `web_subnet_1`
- Public route table: `0.0.0.0/0 → IGW` (associated to web subnets)
- Private route table: `0.0.0.0/0 → NAT GW` (associated to app + DB subnets)

**Key Design Decision:** Single NAT Gateway (cost-optimised). For production, deploy one NAT GW per AZ.

**Outputs:** `vpc_id`, `web_subnet_1/2_id`, `app_subnet_1/2_id`, `db_subnet_1/2_id`

---

### Module 2 — `security`

**Purpose:** Defines the firewall rules that enforce tier isolation.

| Security Group | Allows Inbound | From |
|----------------|---------------|------|
| `pub_alb_sg` | :80 | 0.0.0.0/0 |
| `web_sg` | :80, :22 | pub_alb_sg, 0.0.0.0/0 |
| `internal_alb_sg` | :3001 | web_sg |
| `app_sg` | :3001, :22 | internal_alb_sg, web_sg |
| `db_sg` | :3306 | app_sg |

All security groups allow all outbound traffic.

**Key Design Decision:** SSH on `web_sg` is open to `0.0.0.0/0` — restrict this to your IP range in production.

**Outputs:** `pub_alb_sg_id`, `web_sg_id`, `internal_alb_sg_id`, `app_sg_id`, `db_sg_id`

---

### Module 3 — `ec2`

**Purpose:** Provisions the compute instances for web and app tiers.

| Instance | Subnet | Public IP | SG | AMI |
|----------|--------|-----------|-----|-----|
| `web_server` | web_subnet_1 | Yes | web_sg | Ubuntu 24.04 LTS |
| `app_server` | app_subnet_1 | No | app_sg | Ubuntu 24.04 LTS |

**AMI Selection:** Uses a `data "aws_ami"` data source to always fetch the latest `ubuntu-noble-24.04-amd64` image from Canonical (owner `099720109477`), so the AMI ID stays current across regions.

**User Data:** Both instances receive a rendered `templatefile()` script injecting:
- `public_alb_dns` and `private_alb_dns` into the web server script
- `db_host`, `db_user`, `db_pass`, `db_name`, `public_alb_dns` into the app server script

**Outputs:** `web_server_pub_ip`, `app_server_prvt_ip`, `web_server_instance_id`, `app_server_instance_id`

---

### Module 4 — `alb`

**Purpose:** Creates two Application Load Balancers to handle north-south (public) and east-west (internal) traffic distribution.

| ALB | Scheme | Subnets | Listener | Target |
|-----|--------|---------|----------|--------|
| `public-alb` | internet-facing | web_subnet_1, web_subnet_2 | HTTP:80 | web_server:80 |
| `private-alb` | internal | app_subnet_1, app_subnet_2 | HTTP:3001 | app_server:3001 |

**Health Check Configuration (both target groups):**
```
Path:                /
Protocol:            HTTP
Matcher:             200
Interval:            30s
Timeout:             5s
Healthy threshold:   2
Unhealthy threshold: 2
```

**Outputs:** `public_alb_dns_name`, `private_alb_dns_name`

---

### Module 5 — `database`

**Purpose:** Managed RDS MySQL instance in isolated private subnets.

**RDS Configuration:**

| Setting | Value |
|---------|-------|
| Identifier | `book-review-db` |
| Engine | MySQL 8.4 |
| Instance Class | db.t3.micro |
| Storage | 20 GB |
| Port | 3306 |
| Subnet Group | db_subnet_1 + db_subnet_2 |
| Security Group | db_sg (port 3306 from app_sg only) |
| Skip Final Snapshot | true (dev setting) |
| Multi-AZ | false (dev setting) |

**Outputs:** `db_endpoint` (format: `hostname:3306`)

---

## Variable Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `aws_region` | `us-east-1` | AWS region to deploy into |
| `project` | `book-review` | Project name — used in all resource names/tags |
| `vpc_cidr_block` | `10.0.0.0/16` | VPC CIDR block |
| `web_subnet_1_cidr` | `10.0.1.0/24` | Public web subnet, AZ-a |
| `web_subnet_2_cidr` | `10.0.2.0/24` | Public web subnet, AZ-b |
| `app_subnet_1_cidr` | `10.0.3.0/24` | Private app subnet, AZ-a |
| `app_subnet_2_cidr` | `10.0.4.0/24` | Private app subnet, AZ-b |
| `db_subnet_1_cidr` | `10.0.5.0/24` | Private DB subnet, AZ-a |
| `db_subnet_2_cidr` | `10.0.6.0/24` | Private DB subnet, AZ-b |
| `keyname` | `book-review-key` | SSH key pair name |
| `web_instance_type` | `t3.micro` | Web server instance type |
| `app_instance_type` | `t3.micro` | App server instance type |
| `allocated_storage` | `20` | RDS storage in GB |
| `db_name` | `bookreviewdb` | Initial database name |
| `engine` | `mysql` | RDS engine |
| `engine_version` | `8.0` | MySQL version |
| `instance_class` | `db.t3.micro` | RDS instance class |
| `username` | `admin` | RDS master username |
| `password` | *(required)* | RDS master password — **never commit this** |

---

## User Data & App Bootstrap

Both EC2 instances use templated shell scripts (`scripts/*.sh.tpl`) rendered by Terraform at plan time. This injects live infrastructure values (ALB DNS names, DB credentials) directly into the startup scripts.

### Web Server (`frontend-userdata.sh.tpl`)

Executed once on first boot:

1. Install Node.js LTS, Nginx, Git
2. Clone app repo → `frontend/` directory
3. `npm install && npm run build` (Next.js production build)
4. Write `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://<public_alb_dns>
   ```
5. Start with PM2: `pm2 start npm --name frontend -- start` (port 3000)
6. Configure PM2 startup (survives reboots)
7. Write Nginx config at `/etc/nginx/sites-available/book-review`:
   ```nginx
   location /api/ {
       proxy_pass http://<private_alb_dns>:3001/api/;
   }
   location / {
       proxy_pass http://localhost:3000;
   }
   ```
8. Enable site, reload Nginx

### App Server (`backend-userdata.sh.tpl`)

Executed once on first boot:

1. Install Node.js LTS, MySQL client, Git
2. Clone app repo → `backend/` directory
3. `npm install`
4. Write `.env`:
   ```
   DB_HOST=<rds_hostname>
   DB_USER=admin
   DB_PASS=<password>
   DB_NAME=bookreviewdb
   DB_DIALECT=mysql
   PORT=3001
   JWT_SECRET=mysecret
   ALLOWED_ORIGINS=http://<public_alb_dns>
   ```
5. Start with PM2: `pm2 start src/server.js --name bk-backend` (port 3001)
6. Configure PM2 startup (survives reboots)

---

## Traffic Flow

```
User Browser
    │
    │  HTTP GET /
    ▼
Public ALB (public-alb:80)
    │
    ▼
web_server → Nginx (:80)
    ├── GET /api/*  ──────────────────────────────►  Internal ALB (private-alb:3001)
    │                                                        │
    │                                                        ▼
    │                                               app_server → Node.js (:3001)
    │                                                        │
    │                                                        ▼ MySQL :3306
    │                                               RDS MySQL (book-review-db)
    │
    └── GET /*  ──► localhost:3000 (Next.js)
                         │
                         ▼  (calls /api/* routes)
                    Public ALB (loops back)
```

**SSH Access:**
- To web_server: `ssh -i book-review-key.pem ubuntu@<web_server_pub_ip>`
- To app_server: SSH via web_server (jump host), using its private IP

---

## Getting Started

### Prerequisites

- Terraform >= 1.0 (`terraform --version`)
- AWS CLI v2 configured (`aws configure`)
- AWS credentials with sufficient IAM permissions (EC2, VPC, RDS, ELB, IAM)

### Deploy

```bash
# 1. Clone this repo
git clone <repo-url>
cd book-review-terraform-iac

# 2. Create terraform.tfvars (gitignored — do not commit)
cat > terraform.tfvars <<EOF
aws_region        = "us-east-1"
project           = "book-review"
vpc_cidr_block    = "10.0.0.0/16"
web_subnet_1_cidr = "10.0.1.0/24"
web_subnet_2_cidr = "10.0.2.0/24"
app_subnet_1_cidr = "10.0.3.0/24"
app_subnet_2_cidr = "10.0.4.0/24"
db_subnet_1_cidr  = "10.0.5.0/24"
db_subnet_2_cidr  = "10.0.6.0/24"
keyname           = "book-review-key"
web_instance_type = "t3.micro"
app_instance_type = "t3.micro"
allocated_storage = 20
db_name           = "bookreviewdb"
engine            = "mysql"
engine_version    = "8.4"
instance_class    = "db.t3.micro"
username          = "admin"
password          = "YourStrongPassword123!"   # Change this
EOF

# 3. Initialise providers
terraform init

# 4. Preview changes
terraform plan

# 5. Apply
terraform apply
# Review the plan, type 'yes' to confirm

# 6. Get outputs
terraform output
```

The SSH private key is automatically generated and saved as `book-review-key.pem` in the project directory.

### Destroy

```bash
terraform destroy
# Type 'yes' to confirm — this removes all AWS resources
```

---

## Outputs

After a successful `terraform apply`:

| Output | Description |
|--------|-------------|
| `webserver_pub_ip` | Public IP of the web server (for SSH and direct access) |
| `appserver_prvt_ip` | Private IP of the app server |
| `db_endpoint` | RDS endpoint (`hostname:3306`) |
| `public_alb_dns_name` | Public ALB DNS — the application's public URL |
| `private_alb_dns_name` | Internal ALB DNS — used by Nginx on the web server |

Access the application: `http://<public_alb_dns_name>`

---

## Security Considerations

### Current (Development) Posture

| Item | Status | Action for Production |
|------|--------|----------------------|
| SSH on web_sg | Open to `0.0.0.0/0` | Restrict to your IP / bastion host CIDR |
| DB accessible only from app_sg | Correct | No change needed |
| `terraform.tfvars` gitignored | Correct | Use AWS Secrets Manager for passwords |
| State file local | Local only | Move to S3 backend with DynamoDB locking |
| RDS Multi-AZ | Disabled | Enable for production |
| RDS `skip_final_snapshot` | `true` | Set `false` + configure retention in production |
| SSH key `.pem` local | Gitignored | Store in AWS Secrets Manager or SSM |

### Remote State Backend (Recommended for Production)

Add this to `main.tf` before running `terraform init`:

```hcl
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "book-review/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

---

## Common Operations

```bash
# List all managed resources
terraform state list

# Show details of a specific resource
terraform state show module.database.aws_db_instance.book_review_db

# Re-apply after changing tfvars (e.g., scaling instance type)
terraform plan
terraform apply

# Destroy only the database (careful — data loss)
terraform destroy -target=module.database.aws_db_instance.book_review_db

# SSH to web server
ssh -i book-review-key.pem ubuntu@$(terraform output -raw webserver_pub_ip)

# SSH to app server (via web server jump)
ssh -i book-review-key.pem -J ubuntu@$(terraform output -raw webserver_pub_ip) \
    ubuntu@$(terraform output -raw appserver_prvt_ip)
```

---

## Troubleshooting

**ALB health check failing (web tier)**
- Nginx must be running and proxying to Next.js on port 3000
- Check: `sudo systemctl status nginx` on web_server
- Check PM2: `sudo pm2 status`

**ALB health check failing (app tier)**
- Node.js backend must return HTTP 200 on `GET /`
- Check PM2 logs: `sudo pm2 logs bk-backend`
- Verify DB connection: `DB_HOST` in `.env` must resolve to the RDS hostname

**Cannot connect to RDS**
- Confirm app server's security group is `app_sg`
- Confirm RDS security group is `db_sg` with inbound `:3306` from `app_sg`
- Run from app_server: `mysql -h <db_host> -u admin -p bookreviewdb`

**User data script did not run**
- Check cloud-init log: `sudo cat /var/log/cloud-init-output.log`
- Scripts run only once on first boot

**`terraform apply` fails with "Invalid AMI ID"**
- The `aws_ami` data source fetches the latest Ubuntu AMI dynamically — ensure your AWS credentials have `ec2:DescribeImages` permission

**Insufficient IAM permissions**
- Minimum permissions needed: `AmazonEC2FullAccess`, `AmazonRDSFullAccess`, `ElasticLoadBalancingFullAccess`, `AmazonVPCFullAccess`

---

## Resources

- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Language Reference](https://developer.hashicorp.com/terraform/language)
- [AWS Three-Tier Architecture](https://docs.aws.amazon.com/whitepapers/latest/serverless-multi-tier-architectures-api-gateway-lambda/three-tier-architecture-overview.html)
