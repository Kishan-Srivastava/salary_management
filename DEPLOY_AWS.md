# Deploy on AWS quickly (EC2 + Docker)

Fastest path for demos/interviews: **one EC2 instance** running your existing `docker-compose.yml`.

**Time:** ~20–30 minutes (first time)  
**Cost:** ~$15–30/month (t3.small) — stop the instance when not in use to save money.

---

## What you will get

| URL | Port | Service |
|-----|------|---------|
| `http://<EC2-PUBLIC-IP>:8501` | 8501 | Streamlit dashboard |
| `http://<EC2-PUBLIC-IP>:8001/docs` | 8001 | API Swagger |
| `http://<EC2-PUBLIC-IP>:8001/api/v1/health` | 8001 | API health |

---

## Step 1 — Launch EC2

1. AWS Console → **EC2** → **Launch instance**
2. Settings:
   - **Name:** `salary-management`
   - **AMI:** Amazon Linux 2023
   - **Instance type:** `t3.small` (or `t3.micro` for light demo)
   - **Key pair:** Create or select `.pem` (required for SSH)
   - **Security group:** Create new → allow:
     - **SSH (22)** — your IP only
     - **Custom TCP 8501** — `0.0.0.0/0` (Streamlit)
     - **Custom TCP 8001** — `0.0.0.0/0` (API / Swagger)
   - **Storage:** 20 GB gp3
3. **Launch** → wait until **Running** → copy **Public IPv4 address**

---

## Step 2 — SSH into the instance

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
```

---

## Step 3 — Install Docker

On the EC2 instance (Amazon Linux 2023):

```bash
sudo dnf update -y
sudo dnf install -y docker git
sudo systemctl enable --now docker
sudo usermod -aG docker ec2-user
```

Log out and back in so Docker group applies:

```bash
exit
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
```

Install Docker Compose plugin:

```bash
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
docker compose version
```

---

## Step 4 — Clone and run the app

```bash
git clone https://github.com/Kishan-Srivastava/salary_management.git
cd salary_management
git pull origin main   # must include DISPLAY_API_BASE + load_dotenv fix
```

If `git status` shows local edits, reset to GitHub before deploy:

```bash
git fetch origin
git reset --hard origin/main
```

Start (EC2 script — avoids `buildx 0.17` error):

```bash
chmod +x scripts/ec2_docker_up.sh
./scripts/ec2_docker_up.sh
```

Or manually:

```bash
docker build -t salary-management-api:local -f Dockerfile .
docker build -t salary-management-ui:local -f Dockerfile.ui .
docker compose -f docker-compose.ec2.yml up -d
docker compose -f docker-compose.ec2.yml ps
docker compose -f docker-compose.ec2.yml logs -f api   # Ctrl+C to exit
```

`docker-compose.ec2.yml` seeds **500** demo employees on first API start.

Wait until API healthcheck passes (~30s).

---

## Step 5 — Verify

From your laptop browser:

- Dashboard: `http://<EC2-PUBLIC-IP>:8501`
- Swagger: `http://<EC2-PUBLIC-IP>:8001/docs`
- Health: `http://<EC2-PUBLIC-IP>:8001/api/v1/health`

On the server:

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/api/v1/health
```

---

## Step 6 — Share with interviewer

Add to README or email:

```
Dashboard:  http://<EC2-PUBLIC-IP>:8501
API docs:   http://<EC2-PUBLIC-IP>:8001/docs
```

**Tip:** If you stop/start the instance, the **public IP may change** unless you attach an **Elastic IP** (free while instance is running).

---

## Elastic IP (stable URL)

1. EC2 → **Elastic IPs** → **Allocate**
2. **Associate** with your `salary-management` instance
3. Use that IP in README links instead of the changing public IP

---

## Troubleshooting: `streamlit_app.py: not found` during UI build

`.dockerignore` must **not** list `streamlit_app.py`, `ui/`, or `views/`. Older repo copies excluded them for API-only builds.

```bash
git pull
# or edit .dockerignore on EC2 and remove those lines
docker build -t salary-management-ui:local -f Dockerfile.ui .
```

---

## Troubleshooting: `compose build requires buildx 0.17.0 or later`

Amazon Linux often ships an older buildx plugin. **Do not use** `docker compose up --build` on EC2.

**Fix A (recommended):** use the EC2 script above (`scripts/ec2_docker_up.sh`).

**Fix B:** install buildx, then retry:

```bash
mkdir -p ~/.docker/cli-plugins
curl -SL https://github.com/docker/buildx/releases/download/v0.21.0/buildx-v0.21.0.linux-amd64 \
  -o ~/.docker/cli-plugins/docker-buildx
chmod +x ~/.docker/cli-plugins/docker-buildx
docker buildx version   # should be >= 0.17
docker compose up -d --build
```

On **ARM** (Graviton) instances, use `linux-arm64` instead of `linux-amd64`.

**Fix C:** disable compose bake (may work on some versions):

```bash
export COMPOSE_BAKE=false
docker compose up -d --build
```

---

## Useful commands

```bash
cd ~/salary_management
docker compose -f docker-compose.ec2.yml logs -f ui
docker compose -f docker-compose.ec2.yml restart
docker compose -f docker-compose.ec2.yml down
./scripts/ec2_docker_up.sh   # after git pull
```

Update app:

```bash
git pull
docker compose up -d --build
```

---

## Production notes (beyond quick demo)

| Topic | Quick demo (now) | Production |
|-------|------------------|------------|
| Database | SQLite on EC2 volume | Amazon RDS (PostgreSQL) |
| HTTPS | HTTP only | ALB + ACM certificate |
| Domain | IP:port | Route 53 + ALB |
| Secrets | `.env` on server | AWS Secrets Manager |
| Scale | Single EC2 | ECS Fargate or EKS |

---

## Faster AWS alternatives

| Service | Best for | Effort |
|---------|----------|--------|
| **EC2 + Docker** (this guide) | Interview demo, full control | Low |
| **AWS Lightsail** | Same as EC2 but simpler UI | Low |
| **App Runner** | Container per service, no SSH | Medium |
| **ECS Fargate** | Production containers | High |

For **Lightsail:** create instance → Docker setup → same `docker compose` steps as above.
