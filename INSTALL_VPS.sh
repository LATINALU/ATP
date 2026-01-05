#!/bin/bash

# ATP v2.0.0 - Manual VPS Installation Script
# Ejecuta este script DENTRO de tu VPS después de conectarte

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     ATP v2.0.0 - Instalación Manual en VPS              ║"
echo "║     Dominio: atp-app.duckdns.org                         ║"
echo "║     IP: 147.93.191.92                                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📦 Paso 1/8: Actualizando sistema...${NC}"
apt update
apt upgrade -y
echo -e "${GREEN}✅ Sistema actualizado${NC}\n"

echo -e "${BLUE}📦 Paso 2/8: Instalando dependencias básicas...${NC}"
apt install -y curl git wget nano ufw
echo -e "${GREEN}✅ Dependencias instaladas${NC}\n"

echo -e "${BLUE}🐳 Paso 3/8: Instalando Docker...${NC}"
if ! command -v docker &> /dev/null; then
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
  rm get-docker.sh
  systemctl enable docker
  systemctl start docker
  echo -e "${GREEN}✅ Docker instalado${NC}"
else
  echo -e "${GREEN}✅ Docker ya está instalado${NC}"
fi
echo ""

echo -e "${BLUE}🐳 Paso 4/8: Instalando Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
  curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
  echo -e "${GREEN}✅ Docker Compose instalado${NC}"
else
  echo -e "${GREEN}✅ Docker Compose ya está instalado${NC}"
fi
echo ""

echo -e "${BLUE}📁 Paso 5/8: Clonando repositorio...${NC}"
cd /opt
if [ -d "atp" ]; then
  echo -e "${YELLOW}⚠️  Directorio atp existe, actualizando...${NC}"
  cd atp
  git pull
else
  git clone https://github.com/LATINALU/ATP.git atp
  cd atp
fi
echo -e "${GREEN}✅ Repositorio clonado/actualizado${NC}\n"

echo -e "${BLUE}🔧 Paso 6/8: Configurando variables de entorno...${NC}"
cat > .env << 'EOF'
# ATP Production Environment
NODE_ENV=production
PYTHONUNBUFFERED=1

# API URL (usando dominio DuckDNS)
NEXT_PUBLIC_API_URL=http://atp-app.duckdns.org:8000

# No API keys needed - users configure their own in browser
EOF
echo -e "${GREEN}✅ Variables configuradas${NC}\n"

echo -e "${BLUE}🔥 Paso 7/8: Configurando firewall...${NC}"
ufw allow 22822/tcp  # SSH
ufw allow 80/tcp     # HTTP
ufw allow 443/tcp    # HTTPS
ufw allow 3000/tcp   # Frontend
ufw allow 8000/tcp   # Backend
ufw --force enable
echo -e "${GREEN}✅ Firewall configurado${NC}\n"

echo -e "${BLUE}🚀 Paso 8/8: Construyendo e iniciando servicios...${NC}"
echo "Esto puede tomar varios minutos..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "Esperando que los servicios inicien..."
sleep 15

echo ""
echo -e "${BLUE}📊 Estado de los servicios:${NC}"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo -e "${BLUE}🧹 Limpiando imágenes antiguas...${NC}"
docker image prune -f

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              🎉 INSTALACIÓN COMPLETADA 🎉                ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ ATP v2.0.0 está corriendo en tu VPS${NC}"
echo ""
echo -e "${BLUE}🌐 Acceso:${NC}"
echo "   • Por IP:      http://147.93.191.92"
echo "   • Por dominio: http://atp-app.duckdns.org"
echo ""
echo -e "${BLUE}📋 Comandos útiles:${NC}"
echo "   Ver logs:      docker-compose -f docker-compose.prod.yml logs -f"
echo "   Reiniciar:     docker-compose -f docker-compose.prod.yml restart"
echo "   Detener:       docker-compose -f docker-compose.prod.yml down"
echo "   Estado:        docker-compose -f docker-compose.prod.yml ps"
echo ""
echo -e "${BLUE}🔄 Para actualizar en el futuro:${NC}"
echo "   cd /opt/atp"
echo "   git pull"
echo "   docker-compose -f docker-compose.prod.yml up -d --build"
echo ""
echo -e "${GREEN}¡Listo para compartir! 🚀${NC}"
