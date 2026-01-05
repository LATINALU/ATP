#!/bin/bash

# ATP v2.0.0 - Automated VPS Deployment Script
# Este script automatiza el deployment completo en tu VPS

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuración VPS
VPS_IP="147.93.191.92"
VPS_USER="root"
VPS_PORT="22822"
DEPLOY_PATH="/opt/atp"

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         ATP v2.0.0 - VPS Deployment Script              ║"
echo "║         Agentes de Tareas Polivalentes                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}📦 Paso 1/5: Preparando archivos para deployment...${NC}"

# Crear directorio temporal
TEMP_DIR=$(mktemp -d)
echo "Directorio temporal: $TEMP_DIR"

# Copiar archivos necesarios
cp -r docker-compose.prod.yml "$TEMP_DIR/"
cp -r frontend "$TEMP_DIR/"
cp -r backend "$TEMP_DIR/"
cp -r nginx "$TEMP_DIR/"
cp README.md "$TEMP_DIR/"
cp DEPLOYMENT.md "$TEMP_DIR/"

# Crear archivo .env.example si no existe
if [ ! -f "$TEMP_DIR/.env.example" ]; then
  cat > "$TEMP_DIR/.env.example" << 'EOF'
# ATP Environment Variables
NODE_ENV=production
NEXT_PUBLIC_API_URL=http://localhost:8000

# No API keys needed - users configure their own in browser
# Las API keys se configuran en el navegador de cada usuario
EOF
fi

# Crear tarball
cd "$TEMP_DIR"
tar -czf atp-deploy.tar.gz *
mv atp-deploy.tar.gz /tmp/

echo -e "${GREEN}✅ Archivos preparados${NC}"

echo -e "${YELLOW}📤 Paso 2/5: Subiendo archivos al VPS...${NC}"
echo "Conectando a $VPS_USER@$VPS_IP:$VPS_PORT"

# Subir archivo al VPS
scp -P $VPS_PORT /tmp/atp-deploy.tar.gz $VPS_USER@$VPS_IP:/tmp/

echo -e "${GREEN}✅ Archivos subidos exitosamente${NC}"

echo -e "${YELLOW}🔧 Paso 3/5: Instalando en VPS...${NC}"

# Ejecutar comandos en el VPS
ssh -p $VPS_PORT $VPS_USER@$VPS_IP << 'ENDSSH'
set -e

echo "🔹 Creando directorio de deployment..."
mkdir -p /opt/atp
cd /opt/atp

echo "🔹 Extrayendo archivos..."
tar -xzf /tmp/atp-deploy.tar.gz
rm /tmp/atp-deploy.tar.gz

echo "🔹 Verificando Docker..."
if ! command -v docker &> /dev/null; then
  echo "📦 Instalando Docker..."
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
  rm get-docker.sh
  systemctl enable docker
  systemctl start docker
  echo "✅ Docker instalado"
else
  echo "✅ Docker ya está instalado"
fi

echo "🔹 Verificando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
  echo "📦 Instalando Docker Compose..."
  curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
  echo "✅ Docker Compose instalado"
else
  echo "✅ Docker Compose ya está instalado"
fi

echo "🔹 Configurando firewall..."
if command -v ufw &> /dev/null; then
  ufw allow 80/tcp
  ufw allow 443/tcp
  echo "✅ Firewall configurado"
fi

ENDSSH

echo -e "${GREEN}✅ Instalación completada${NC}"

echo -e "${YELLOW}🚀 Paso 4/5: Iniciando servicios...${NC}"

ssh -p $VPS_PORT $VPS_USER@$VPS_IP << 'ENDSSH'
cd /opt/atp

echo "🔹 Deteniendo servicios anteriores (si existen)..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

echo "🔹 Construyendo imágenes..."
docker-compose -f docker-compose.prod.yml build

echo "🔹 Iniciando servicios..."
docker-compose -f docker-compose.prod.yml up -d

echo "🔹 Esperando que los servicios inicien..."
sleep 10

echo "🔹 Estado de los servicios:"
docker-compose -f docker-compose.prod.yml ps

echo "🔹 Limpiando imágenes antiguas..."
docker image prune -f

ENDSSH

echo -e "${GREEN}✅ Servicios iniciados${NC}"

echo -e "${YELLOW}✅ Paso 5/5: Verificando deployment...${NC}"

# Verificar que el servicio responde
echo "Verificando conectividad..."
sleep 5

if curl -s -o /dev/null -w "%{http_code}" http://$VPS_IP | grep -q "200\|301\|302"; then
  echo -e "${GREEN}✅ Servidor respondiendo correctamente${NC}"
else
  echo -e "${YELLOW}⚠️  Servidor aún iniciando, puede tomar unos segundos...${NC}"
fi

# Limpiar archivos temporales
rm -rf "$TEMP_DIR"
rm /tmp/atp-deploy.tar.gz 2>/dev/null || true

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE 🎉       ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🌐 Tu aplicación está disponible en:${NC}"
echo -e "   ${GREEN}http://$VPS_IP${NC}"
echo ""
echo -e "${BLUE}📋 Comandos útiles:${NC}"
echo -e "   ${YELLOW}Conectar al VPS:${NC}"
echo "   ssh -p $VPS_PORT $VPS_USER@$VPS_IP"
echo ""
echo -e "   ${YELLOW}Ver logs:${NC}"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo -e "   ${YELLOW}Reiniciar servicios:${NC}"
echo "   docker-compose -f docker-compose.prod.yml restart"
echo ""
echo -e "   ${YELLOW}Ver estado:${NC}"
echo "   docker-compose -f docker-compose.prod.yml ps"
echo ""
echo -e "${BLUE}🔐 Seguridad:${NC}"
echo "   ✅ Las API keys se almacenan SOLO en el navegador del usuario"
echo "   ✅ No hay base de datos de credenciales en el servidor"
echo "   ✅ Cada usuario usa sus propias API keys"
echo ""
echo -e "${BLUE}🌍 Dominio gratuito (opcional):${NC}"
echo "   1. DuckDNS: https://www.duckdns.org/"
echo "   2. FreeDNS: https://freedns.afraid.org/"
echo "   3. No-IP: https://www.noip.com/"
echo ""
echo -e "${BLUE}📚 Documentación completa:${NC}"
echo "   Ver DEPLOYMENT.md para más detalles"
echo ""
echo -e "${GREEN}¡Listo para compartir! 🚀${NC}"
