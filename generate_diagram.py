import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

fig, ax = plt.subplots(1, 1, figsize=(18, 22))
ax.set_xlim(0, 18)
ax.set_ylim(0, 22)
ax.axis('off')
fig.patch.set_facecolor('#F0F4F8')

# ── Colour palette ──────────────────────────────────────────────────────────
C = {
    'internet':    '#1A1A2E',
    'bg_public':   '#E8F4FD',
    'bg_private':  '#FFF3E0',
    'bg_db':       '#F3E5F5',
    'bg_vpc':      '#E3F2FD',
    'alb_pub':     '#1565C0',
    'alb_int':     '#6A1B9A',
    'ec2_web':     '#1B5E20',
    'ec2_app':     '#E65100',
    'rds':         '#880E4F',
    'sg':          '#B71C1C',
    'nat':         '#004D40',
    'igw':         '#01579B',
    'text_light':  '#FFFFFF',
    'text_dark':   '#1A1A2E',
    'arrow':       '#37474F',
    'border':      '#90A4AE',
}

def rect(ax, x, y, w, h, fc, ec='#90A4AE', lw=1.5, radius=0.3, alpha=1.0, zorder=2):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=f"round,pad=0,rounding_size={radius}",
                         facecolor=fc, edgecolor=ec, linewidth=lw,
                         alpha=alpha, zorder=zorder)
    ax.add_patch(box)
    return box

def label(ax, x, y, text, fs=9, color='#1A1A2E', bold=False, ha='center', va='center', zorder=5):
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va=va,
            fontweight=weight, zorder=zorder,
            fontfamily='DejaVu Sans')

def arrow(ax, x1, y1, x2, y2, color='#37474F', lw=2, style='->', zorder=4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=lw, connectionstyle='arc3,rad=0.0'),
                zorder=zorder)

def tag(ax, x, y, text, bg='#B71C1C', fg='white', fs=7, zorder=6):
    ax.text(x, y, text, fontsize=fs, color=fg, ha='center', va='center',
            fontweight='bold', zorder=zorder,
            bbox=dict(boxstyle='round,pad=0.25', facecolor=bg,
                      edgecolor='none', alpha=0.9))

# ═══════════════════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════════════════
rect(ax, 0.3, 20.8, 17.4, 0.9, fc='#1A1A2E', ec='none', radius=0.3, zorder=3)
label(ax, 9, 21.25, 'Book Review App — AWS Three-Tier Architecture', fs=14,
      color='white', bold=True)
label(ax, 9, 20.95, 'Region: us-east-1  |  VPC: 10.0.0.0/16  |  Terraform IaC',
      fs=8.5, color='#90CAF9')

# ═══════════════════════════════════════════════════════════════════════════
# INTERNET
# ═══════════════════════════════════════════════════════════════════════════
rect(ax, 5.5, 19.4, 7, 1.1, fc=C['internet'], ec='#37474F', radius=0.4, zorder=3)
label(ax, 9, 20.05, '🌐  INTERNET', fs=12, color='white', bold=True)
label(ax, 9, 19.65, '0.0.0.0/0', fs=8, color='#B0BEC5')

# ─── arrow: Internet → Public ALB ───
arrow(ax, 9, 19.4, 9, 18.45, color='#1565C0', lw=2.5)
tag(ax, 9.6, 18.95, 'HTTP :80')

# ═══════════════════════════════════════════════════════════════════════════
# VPC BOUNDARY
# ═══════════════════════════════════════════════════════════════════════════
rect(ax, 0.3, 1.0, 17.4, 18.1, fc='#E3F2FD', ec='#1565C0', lw=2,
     radius=0.5, alpha=0.35, zorder=1)
label(ax, 1.85, 18.7, 'AWS VPC  10.0.0.0/16', fs=9, color='#0D47A1',
      bold=True, ha='left')

# ── IGW badge ──
rect(ax, 14.5, 18.3, 2.8, 0.75, fc=C['igw'], ec='#01579B', radius=0.2, zorder=3)
label(ax, 15.9, 18.68, 'Internet Gateway', fs=8, color='white', bold=True)
label(ax, 15.9, 18.42, 'igw  ·  book-review-igw', fs=7, color='#B3E5FC')

# ═══════════════════════════════════════════════════════════════════════════
# PUBLIC ALB
# ═══════════════════════════════════════════════════════════════════════════
rect(ax, 3.2, 17.55, 11.6, 0.85, fc=C['alb_pub'], ec='#0D47A1', lw=2,
     radius=0.3, zorder=3)
label(ax, 9, 18.05, '⚖  PUBLIC APPLICATION LOAD BALANCER  —  public-alb', fs=10,
      color='white', bold=True)
label(ax, 9, 17.73, 'Subnets: web_subnet_1 (10.0.1.0/24)  +  web_subnet_2 (10.0.2.0/24)   |   SG: pub_alb_sg  :80 → 0.0.0.0/0',
      fs=7.5, color='#BBDEFB')

# ─── arrow: Public ALB → Web Server ───
arrow(ax, 9, 17.55, 9, 16.55, color='#1B5E20', lw=2.5)
tag(ax, 9.6, 17.1, 'HTTP :80')

# ═══════════════════════════════════════════════════════════════════════════
# WEB TIER ZONE
# ═══════════════════════════════════════════════════════════════════════════
rect(ax, 0.6, 14.0, 16.8, 2.5, fc=C['bg_public'], ec='#1B5E20', lw=1.5,
     radius=0.4, zorder=2)
label(ax, 1.8, 16.2, 'WEB TIER  —  Public Subnets', fs=9, color='#1B5E20',
      bold=True, ha='left')
label(ax, 16.7, 16.2, 'web_subnet_1: 10.0.1.0/24  (AZ-a)', fs=7.5,
      color='#2E7D32', ha='right')

# NAT Gateway (inside web tier zone)
rect(ax, 0.85, 14.15, 2.8, 0.8, fc=C['nat'], ec='#004D40', radius=0.2, zorder=3)
label(ax, 2.25, 14.6, 'NAT Gateway', fs=8, color='white', bold=True)
label(ax, 2.25, 14.3, 'nat_gw  ·  Elastic IP', fs=7, color='#B2DFDB')

# Web Server box
rect(ax, 4.0, 14.15, 10.0, 1.95, fc='white', ec=C['ec2_web'], lw=2,
     radius=0.3, zorder=3)
# EC2 header bar
rect(ax, 4.0, 15.4, 10.0, 0.7, fc=C['ec2_web'], ec=C['ec2_web'],
     radius=0.3, zorder=4)
label(ax, 9, 15.75, '🖥  web_server  —  EC2 t3.micro  |  Ubuntu 24.04 LTS  |  Public IP: ✓',
      fs=9, color='white', bold=True)

# Web server internals
label(ax, 5.5, 15.15, 'Nginx :80', fs=8.5, color='#1B5E20', bold=True, ha='left')
label(ax, 5.5, 14.78, '├─  /api/*  →  proxy to Internal ALB :3001', fs=8,
      color='#2E7D32', ha='left')
label(ax, 5.5, 14.45, '└─  /*      →  localhost:3000  (Next.js)', fs=8,
      color='#2E7D32', ha='left')
label(ax, 12.5, 15.05, 'PM2', fs=7.5, color='white', bold=True, ha='center',
      va='center')
rect(ax, 11.8, 14.85, 1.4, 0.38, fc='#388E3C', ec='none', radius=0.15, zorder=5)
label(ax, 12.5, 14.85, 'Next.js :3000', fs=7.5, color='white', ha='center', va='center')
rect(ax, 11.8, 14.42, 1.4, 0.38, fc='#388E3C', ec='none', radius=0.15, zorder=5)
label(ax, 12.5, 14.42, 'frontend build', fs=7, color='white', ha='center', va='center')

# SG badge web
tag(ax, 4.5, 16.3, 'SG: web_sg', bg='#B71C1C')

# ─── arrow: web_server → Internal ALB ───
arrow(ax, 9, 14.15, 9, 13.2, color=C['alb_int'], lw=2.5)
tag(ax, 9.75, 13.7, 'HTTP :3001')

# ═══════════════════════════════════════════════════════════════════════════
# INTERNAL ALB
# ═══════════════════════════════════════════════════════════════════════════
rect(ax, 3.2, 12.4, 11.6, 0.75, fc=C['alb_int'], ec='#4A148C', lw=2,
     radius=0.3, zorder=3)
label(ax, 9, 12.82, '⚖  INTERNAL APPLICATION LOAD BALANCER  —  private-alb', fs=10,
      color='white', bold=True)
label(ax, 9, 12.55, 'Subnets: app_subnet_1 (10.0.3.0/24)  +  app_subnet_2 (10.0.4.0/24)   |   SG: internal_alb_sg  :3001 from web_sg',
      fs=7.5, color='#E1BEE7')

# ─── arrow: Internal ALB → App Server ───
arrow(ax, 9, 12.4, 9, 11.35, color=C['ec2_app'], lw=2.5)
tag(ax, 9.75, 11.9, 'HTTP :3001')

# ═══════════════════════════════════════════════════════════════════════════
# APP TIER ZONE
# ═══════════════════════════════════════════════════════════════════════════
rect(ax, 0.6, 8.75, 16.8, 2.5, fc=C['bg_private'], ec=C['ec2_app'], lw=1.5,
     radius=0.4, zorder=2)
label(ax, 1.8, 10.95, 'APP TIER  —  Private Subnets', fs=9, color=C['ec2_app'],
      bold=True, ha='left')
label(ax, 16.7, 10.95, 'app_subnet_1: 10.0.3.0/24  (AZ-a)', fs=7.5,
      color='#BF360C', ha='right')

# App Server box
rect(ax, 4.0, 8.9, 10.0, 1.95, fc='white', ec=C['ec2_app'], lw=2,
     radius=0.3, zorder=3)
rect(ax, 4.0, 10.15, 10.0, 0.7, fc=C['ec2_app'], ec=C['ec2_app'],
     radius=0.3, zorder=4)
label(ax, 9, 10.5, '🖥  app_server  —  EC2 t3.micro  |  Ubuntu 24.04 LTS  |  Private IP only',
      fs=9, color='white', bold=True)

label(ax, 5.5, 9.9, 'Node.js API  :3001', fs=8.5, color=C['ec2_app'], bold=True, ha='left')
label(ax, 5.5, 9.52, '├─  Express REST API  (JWT auth)', fs=8, color='#BF360C', ha='left')
label(ax, 5.5, 9.15, '└─  Connects to RDS MySQL on :3306', fs=8, color='#BF360C', ha='left')
label(ax, 12.5, 9.8, 'PM2', fs=7.5, color='white', bold=True, ha='center', va='center')
rect(ax, 11.8, 9.6, 1.4, 0.38, fc='#F57C00', ec='none', radius=0.15, zorder=5)
label(ax, 12.5, 9.6, 'bk-backend', fs=7.5, color='white', ha='center', va='center')
rect(ax, 11.8, 9.17, 1.4, 0.38, fc='#F57C00', ec='none', radius=0.15, zorder=5)
label(ax, 12.5, 9.17, 'src/server.js', fs=7, color='white', ha='center', va='center')

tag(ax, 4.5, 11.1, 'SG: app_sg', bg='#B71C1C')

# ─── arrow: App Server → RDS ───
arrow(ax, 9, 8.9, 9, 7.85, color=C['rds'], lw=2.5)
tag(ax, 9.75, 8.42, 'MySQL :3306')

# ═══════════════════════════════════════════════════════════════════════════
# DATABASE TIER ZONE
# ═══════════════════════════════════════════════════════════════════════════
rect(ax, 0.6, 5.8, 16.8, 2.0, fc=C['bg_db'], ec=C['rds'], lw=1.5,
     radius=0.4, zorder=2)
label(ax, 1.8, 7.5, 'DATABASE TIER  —  Private Subnets', fs=9, color=C['rds'],
      bold=True, ha='left')
label(ax, 16.7, 7.5, 'db_subnet_1: 10.0.5.0/24  (AZ-a)  +  db_subnet_2: 10.0.6.0/24  (AZ-b)',
      fs=7.5, color='#6A1B4D', ha='right')

# RDS box
rect(ax, 4.0, 5.95, 10.0, 1.5, fc='white', ec=C['rds'], lw=2,
     radius=0.3, zorder=3)
rect(ax, 4.0, 6.95, 10.0, 0.5, fc=C['rds'], ec=C['rds'],
     radius=0.3, zorder=4)
label(ax, 9, 7.2, '🗄  Amazon RDS  —  MySQL 8.4  |  db.t3.micro  |  20 GB',
      fs=9.5, color='white', bold=True)

# RDS details in 3 columns
label(ax, 5.5, 6.7, 'Instance:', fs=8, color='#6A1B4D', bold=True, ha='left')
label(ax, 5.5, 6.4, 'book-review-db', fs=8, color=C['rds'], ha='left')
label(ax, 8.2, 6.7, 'Database:', fs=8, color='#6A1B4D', bold=True, ha='left')
label(ax, 8.2, 6.4, 'bookreviewdb', fs=8, color=C['rds'], ha='left')
label(ax, 11.0, 6.7, 'Port:', fs=8, color='#6A1B4D', bold=True, ha='left')
label(ax, 11.0, 6.4, '3306', fs=8, color=C['rds'], ha='left')
label(ax, 12.5, 6.7, 'SG:', fs=8, color='#6A1B4D', bold=True, ha='left')
label(ax, 12.5, 6.4, 'db_sg (:3306\nfrom app_sg only)', fs=7.5, color=C['rds'], ha='left')

tag(ax, 4.5, 7.65, 'SG: db_sg', bg='#B71C1C')

# ═══════════════════════════════════════════════════════════════════════════
# LEGEND
# ═══════════════════════════════════════════════════════════════════════════
rect(ax, 0.5, 1.1, 17.0, 4.5, fc='white', ec='#90A4AE', lw=1, radius=0.3, zorder=2)
label(ax, 1.0, 5.3, 'LEGEND & KEY FACTS', fs=9, color='#37474F', bold=True, ha='left')

# Legend items — row 1
items_r1 = [
    (C['alb_pub'], 'Public ALB  (internet-facing)'),
    (C['alb_int'], 'Internal ALB  (east-west)'),
    (C['ec2_web'], 'EC2  Web Server  (public IP)'),
    (C['ec2_app'], 'EC2  App Server  (private IP)'),
    (C['rds'],     'Amazon RDS MySQL'),
]
for i, (clr, txt) in enumerate(items_r1):
    x = 0.9 + i * 3.4
    rect(ax, x, 4.8, 0.4, 0.3, fc=clr, ec='none', radius=0.08, zorder=4)
    label(ax, x + 0.55, 4.95, txt, fs=7.5, color='#37474F', ha='left')

# Legend items — row 2
items_r2 = [
    (C['nat'], 'NAT Gateway  (outbound for private subnets)'),
    (C['igw'], 'Internet Gateway  (public internet access)'),
    ('#B71C1C', 'Security Group  (firewall rules per tier)'),
]
for i, (clr, txt) in enumerate(items_r2):
    x = 0.9 + i * 5.5
    rect(ax, x, 4.3, 0.4, 0.3, fc=clr, ec='none', radius=0.08, zorder=4)
    label(ax, x + 0.55, 4.45, txt, fs=7.5, color='#37474F', ha='left')

# Key facts
facts = [
    ('Terraform Providers:', 'AWS ~> 6.0  |  TLS ~> 4.0  |  Local ~> 2.0'),
    ('SSH Key:',             'Auto-generated RSA-4096  →  book-review-key.pem  (saved locally)'),
    ('AMI:',                 'Ubuntu 24.04 LTS Noble  (latest, dynamic lookup via aws_ami data source)'),
    ('Process Manager:',     'PM2  —  frontend (Next.js :3000) + backend (Node.js :3001)'),
    ('Total AWS Resources:', '~40  (VPC, 6 subnets, IGW, NAT, 2 ALBs, 2 EC2, 5 SGs, RDS, Route Tables…)'),
    ('State:',               'Local terraform.tfstate  |  Recommend: S3 backend + DynamoDB lock for production'),
]
for i, (k, v) in enumerate(facts):
    y = 3.85 - i * 0.45
    label(ax, 1.0, y, k, fs=7.5, color='#1A1A2E', bold=True, ha='left')
    label(ax, 4.2, y, v, fs=7.5, color='#37474F', ha='left')

# ─── Availability Zones callout ───
rect(ax, 15.0, 1.2, 2.6, 4.2, fc='#E8EAF6', ec='#3F51B5', lw=1.2,
     radius=0.25, zorder=3)
label(ax, 16.3, 5.1, 'Multi-AZ', fs=8, color='#283593', bold=True)
label(ax, 16.3, 4.78, 'Coverage', fs=8, color='#283593', bold=True)
rows = [
    ('AZ-a', 'us-east-1a'),
    ('',     'web_subnet_1'),
    ('',     'app_subnet_1'),
    ('',     'db_subnet_1'),
    ('AZ-b', 'us-east-1b'),
    ('',     'web_subnet_2'),
    ('',     'app_subnet_2'),
    ('',     'db_subnet_2'),
]
for i, (a, b) in enumerate(rows):
    y = 4.45 - i * 0.38
    if a:
        label(ax, 15.2, y, a, fs=7, color='#283593', bold=True, ha='left')
    label(ax, 15.8, y, b, fs=7, color='#37474F', ha='left')

# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════
rect(ax, 0.3, 0.1, 17.4, 0.75, fc='#37474F', ec='none', radius=0.2, zorder=3)
label(ax, 9, 0.5, 'book-review-terraform-iac  |  AWS us-east-1  |  VPC 10.0.0.0/16  |  Generated by Terraform IaC  |  github: pravinmishraaws/book-review-app',
      fs=7.5, color='#B0BEC5')

plt.tight_layout(pad=0)
out = r'c:\Users\admin\project\book-review-terraform-iac\assets\architectural-diagram.jpg'
fig.savefig(out, dpi=150, format='jpeg', bbox_inches='tight',
            facecolor=fig.get_facecolor(), quality=95)
print(f"Saved: {out}")
