#!/bin/bash

# ATP Deployment Script for VPS
# This script deploys the ATP system to a VPS with demo mode enabled

set -e

echo "🚀 ATP v2.0.0 - VPS Deployment Script"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# VPS Configuration
VPS_IP="147.93.191.92"
VPS_USER="root"
VPS_PORT="22822"
DEPLOY_PATH="/opt/atp"

echo -e "${YELLOW}📦 Step 1: Preparing files for deployment...${NC}"

# Create deployment package
tar -czf atp-deploy.tar.gz \
  docker-compose.prod.yml \
  frontend/ \
  backend/ \
  nginx/ \
  .env.example \
  README.md

echo -e "${GREEN}✅ Deployment package created${NC}"

echo -e "${YELLOW}📤 Step 2: Uploading to VPS...${NC}"

# Upload to VPS
scp -P $VPS_PORT atp-deploy.tar.gz $VPS_USER@$VPS_IP:/tmp/

echo -e "${GREEN}✅ Files uploaded${NC}"

echo -e "${YELLOW}🔧 Step 3: Installing on VPS...${NC}"

# Execute deployment on VPS
ssh -p $VPS_PORT $VPS_USER@$VPS_IP << 'ENDSSH'
set -e

echo "Creating deployment directory..."
mkdir -p /opt/atp
cd /opt/atp

echo "Extracting files..."
tar -xzf /tmp/atp-deploy.tar.gz -C /opt/atp
rm /tmp/atp-deploy.tar.gz

echo "Setting up environment..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "DEMO_MODE=true" >> .env
  echo "ALLOW_API_CONFIG=false" >> .env
fi

echo "Installing Docker and Docker Compose if needed..."
if ! command -v docker &> /dev/null; then
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
  rm get-docker.sh
fi

if ! command -v docker-compose &> /dev/null; then
  curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
fi

echo "Starting services..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

echo "Cleaning up old images..."
docker image prune -f

echo "✅ Deployment completed!"
echo "🌐 Access your application at: http://147.93.191.92"
echo "📊 Check status: docker-compose -f docker-compose.prod.yml ps"
echo "📝 View logs: docker-compose -f docker-compose.prod.yml logs -f"

ENDSSH

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo ""
echo "🌐 Your ATP system is now running at:"
echo "   http://147.93.191.92"
echo ""
echo "📋 Useful commands:"
echo "   ssh -p $VPS_PORT $VPS_USER@$VPS_IP"
echo "   cd /opt/atp"
echo "   docker-compose -f docker-compose.prod.yml ps"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🔄 To update:"
echo "   ./deploy.sh"

# Cleanup
rm atp-deploy.tar.gz

echo -e "${GREEN}🎉 Done!${NC}"
