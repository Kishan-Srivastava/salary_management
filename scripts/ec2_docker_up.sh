#!/usr/bin/env bash
# EC2-friendly start: builds with plain `docker build` (no compose buildx 0.17+).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Building API image..."
docker build -t salary-management-api:local -f Dockerfile .

echo "Building UI image..."
if ! docker build -t salary-management-ui:local -f Dockerfile.ui .; then
  echo "UI build failed. Fix Dockerfile.ui CMD (must be a single-line JSON array)." >&2
  exit 1
fi

export COMPOSE_BAKE=false
export SEED_DEMO_COUNT="${SEED_DEMO_COUNT:-500}"

PUBLIC_IP=$(curl -sf --max-time 2 http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || true)
if [ -n "${PUBLIC_IP}" ]; then
  export PUBLIC_API_URL="http://${PUBLIC_IP}:8001"
  echo "PUBLIC_API_URL=${PUBLIC_API_URL}"
fi

docker compose -f docker-compose.ec2.yml up -d

echo ""
echo "Dashboard: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo '<EC2-PUBLIC-IP>'):8501"
echo "Swagger:   http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo '<EC2-PUBLIC-IP>'):8001/docs"
docker compose ps
