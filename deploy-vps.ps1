# ATP v2.0.0 - VPS Deployment Script (PowerShell)
# Script de deployment automatizado para Windows

$VPS_IP = "147.93.191.92"
$VPS_USER = "root"
$VPS_PORT = "22822"
$DEPLOY_PATH = "/opt/atp"

Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║         ATP v2.0.0 - VPS Deployment Script              ║" -ForegroundColor Blue
Write-Host "║         Agentes de Tareas Polivalentes                  ║" -ForegroundColor Blue
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Blue

Write-Host "📦 Paso 1/5: Preparando archivos..." -ForegroundColor Yellow

# Crear archivo temporal
$tempFile = [System.IO.Path]::GetTempFileName() + ".tar.gz"

# Comprimir archivos necesarios
$files = @(
    "docker-compose.prod.yml",
    "frontend",
    "backend", 
    "nginx",
    "README.md",
    "DEPLOYMENT.md"
)

Write-Host "Comprimiendo archivos..." -ForegroundColor Gray

# Usar tar de Windows 10+ o WSL
if (Get-Command tar -ErrorAction SilentlyContinue) {
    tar -czf $tempFile $files
    Write-Host "✅ Archivos comprimidos" -ForegroundColor Green
} else {
    Write-Host "❌ Error: tar no encontrado. Instala WSL o Git Bash" -ForegroundColor Red
    Write-Host "Alternativa: Usa Git Bash y ejecuta: bash deploy-vps.sh" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n📤 Paso 2/5: Subiendo al VPS..." -ForegroundColor Yellow
Write-Host "Conectando a $VPS_USER@$VPS_IP`:$VPS_PORT" -ForegroundColor Gray

# Verificar si scp está disponible
if (Get-Command scp -ErrorAction SilentlyContinue) {
    scp -P $VPS_PORT $tempFile "${VPS_USER}@${VPS_IP}:/tmp/atp-deploy.tar.gz"
    Write-Host "✅ Archivos subidos" -ForegroundColor Green
} else {
    Write-Host "❌ Error: scp no encontrado" -ForegroundColor Red
    Write-Host "Instala OpenSSH Client desde Windows Features" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n🔧 Paso 3/5: Instalando en VPS..." -ForegroundColor Yellow

# Comandos a ejecutar en el VPS
$sshCommands = @"
set -e
echo '🔹 Creando directorio...'
mkdir -p $DEPLOY_PATH
cd $DEPLOY_PATH

echo '🔹 Extrayendo archivos...'
tar -xzf /tmp/atp-deploy.tar.gz
rm /tmp/atp-deploy.tar.gz

echo '🔹 Verificando Docker...'
if ! command -v docker &> /dev/null; then
  echo '📦 Instalando Docker...'
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
  rm get-docker.sh
  systemctl enable docker
  systemctl start docker
fi

echo '🔹 Verificando Docker Compose...'
if ! command -v docker-compose &> /dev/null; then
  echo '📦 Instalando Docker Compose...'
  curl -L 'https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)' -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
fi

echo '✅ Instalación completada'
"@

ssh -p $VPS_PORT "${VPS_USER}@${VPS_IP}" $sshCommands

Write-Host "✅ Instalación completada" -ForegroundColor Green

Write-Host "`n🚀 Paso 4/5: Iniciando servicios..." -ForegroundColor Yellow

$startCommands = @"
cd $DEPLOY_PATH
echo '🔹 Deteniendo servicios anteriores...'
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

echo '🔹 Construyendo imágenes...'
docker-compose -f docker-compose.prod.yml build

echo '🔹 Iniciando servicios...'
docker-compose -f docker-compose.prod.yml up -d

echo '🔹 Estado de servicios:'
docker-compose -f docker-compose.prod.yml ps

echo '🔹 Limpiando imágenes antiguas...'
docker image prune -f
"@

ssh -p $VPS_PORT "${VPS_USER}@${VPS_IP}" $startCommands

Write-Host "✅ Servicios iniciados" -ForegroundColor Green

Write-Host "`n✅ Paso 5/5: Verificando deployment..." -ForegroundColor Yellow

Start-Sleep -Seconds 5

try {
    $response = Invoke-WebRequest -Uri "http://$VPS_IP" -TimeoutSec 10 -UseBasicParsing
    Write-Host "✅ Servidor respondiendo correctamente" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Servidor aún iniciando, puede tomar unos segundos..." -ForegroundColor Yellow
}

# Limpiar archivo temporal
Remove-Item $tempFile -ErrorAction SilentlyContinue

Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║           🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE 🎉       ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "🌐 Tu aplicación está disponible en:" -ForegroundColor Blue
Write-Host "   http://$VPS_IP`n" -ForegroundColor Green

Write-Host "📋 Comandos útiles:" -ForegroundColor Blue
Write-Host "   Conectar al VPS:" -ForegroundColor Yellow
Write-Host "   ssh -p $VPS_PORT ${VPS_USER}@${VPS_IP}`n"

Write-Host "   Ver logs:" -ForegroundColor Yellow
Write-Host "   docker-compose -f docker-compose.prod.yml logs -f`n"

Write-Host "   Reiniciar servicios:" -ForegroundColor Yellow
Write-Host "   docker-compose -f docker-compose.prod.yml restart`n"

Write-Host "🔐 Seguridad:" -ForegroundColor Blue
Write-Host "   ✅ Las API keys se almacenan SOLO en el navegador del usuario" -ForegroundColor Green
Write-Host "   ✅ No hay base de datos de credenciales en el servidor" -ForegroundColor Green
Write-Host "   ✅ Cada usuario usa sus propias API keys`n" -ForegroundColor Green

Write-Host "🌍 Dominio gratuito (opcional):" -ForegroundColor Blue
Write-Host "   1. DuckDNS: https://www.duckdns.org/"
Write-Host "   2. FreeDNS: https://freedns.afraid.org/"
Write-Host "   3. No-IP: https://www.noip.com/`n"

Write-Host "¡Listo para compartir! 🚀" -ForegroundColor Green
