# 🚀 ATP v2.0.0 - Guía de Deployment en VPS

## 🔐 Arquitectura de Seguridad

### ✅ API Keys Client-Side (Ya implementado)
- **Las API keys se almacenan SOLO en el navegador del usuario** (localStorage)
- **NUNCA se envían al servidor**
- **Cada usuario usa sus propias credenciales**
- **No hay base de datos de usuarios ni credenciales en el servidor**

### 🛡️ Cómo Funciona
1. Usuario abre la aplicación en su navegador
2. Usuario configura sus API keys en ⚙️ Settings
3. Las keys se guardan en `localStorage` del navegador
4. Las peticiones a APIs externas se hacen **directamente desde el navegador del usuario**
5. El servidor VPS solo sirve la interfaz estática

## 📋 Requisitos del VPS

- **IP**: 147.93.191.92
- **Puerto SSH**: 22822
- **Sistema**: Ubuntu/Debian (recomendado)
- **RAM**: Mínimo 2GB
- **Disco**: Mínimo 10GB
- **Docker**: Se instalará automáticamente

## 🌐 Dominio Gratuito

### Opción 1: DuckDNS (Recomendado)
1. Ir a https://www.duckdns.org/
2. Iniciar sesión con GitHub/Google
3. Crear subdominio: `atp-demo.duckdns.org`
4. Configurar IP: `147.93.191.92`
5. Copiar el token

### Opción 2: FreeDNS
1. Ir a https://freedns.afraid.org/
2. Crear cuenta gratuita
3. Crear subdominio: `atp.mooo.com`
4. Apuntar a IP: `147.93.191.92`

### Opción 3: No-IP
1. Ir a https://www.noip.com/
2. Crear cuenta gratuita
3. Crear hostname: `atp-demo.ddns.net`
4. Configurar IP: `147.93.191.92`

## 🚀 Deployment Automático

### Paso 1: Preparar archivos localmente
```bash
cd C:\Users\TheosKek\Desktop\ATP
```

### Paso 2: Ejecutar script de deployment
```bash
# En Windows (Git Bash o WSL)
bash deploy-vps.sh

# O manualmente:
# 1. Comprimir archivos
tar -czf atp-deploy.tar.gz docker-compose.prod.yml frontend/ backend/ nginx/ README.md

# 2. Subir a VPS
scp -P 22822 atp-deploy.tar.gz root@147.93.191.92:/tmp/

# 3. Conectar al VPS
ssh -p 22822 root@147.93.191.92
```

### Paso 3: Instalar en VPS
```bash
# En el VPS
cd /opt
mkdir -p atp
cd atp

# Extraer archivos
tar -xzf /tmp/atp-deploy.tar.gz
rm /tmp/atp-deploy.tar.gz

# Instalar Docker (si no está instalado)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Iniciar servicios
docker-compose -f docker-compose.prod.yml up -d --build

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔧 Configuración Post-Deployment

### 1. Verificar servicios
```bash
docker-compose -f docker-compose.prod.yml ps
```

Deberías ver:
- `atp-nginx` (puerto 80)
- `atp-frontend` (puerto 3000)
- `atp-backend` (puerto 8000)

### 2. Configurar Firewall
```bash
# Permitir HTTP
ufw allow 80/tcp

# Permitir HTTPS (opcional)
ufw allow 443/tcp

# Habilitar firewall
ufw enable
```

### 3. Configurar dominio DuckDNS (opcional)
```bash
# Crear script de actualización
mkdir -p /opt/duckdns
cd /opt/duckdns

# Crear script
cat > duck.sh << 'EOF'
#!/bin/bash
echo url="https://www.duckdns.org/update?domains=TU-SUBDOMINIO&token=TU-TOKEN&ip=" | curl -k -o /opt/duckdns/duck.log -K -
EOF

chmod +x duck.sh

# Agregar a crontab (actualizar cada 5 minutos)
crontab -e
# Agregar: */5 * * * * /opt/duckdns/duck.sh >/dev/null 2>&1
```

## 🌐 Acceso a la Aplicación

### Con IP directa:
```
http://147.93.191.92
```

### Con dominio (después de configurar):
```
http://atp-demo.duckdns.org
http://atp.mooo.com
http://atp-demo.ddns.net
```

## 📊 Monitoreo

### Ver logs en tiempo real
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### Ver logs de un servicio específico
```bash
docker-compose -f docker-compose.prod.yml logs -f frontend
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Ver uso de recursos
```bash
docker stats
```

## 🔄 Actualización

### Método 1: Script automático
```bash
# Desde tu PC local
bash deploy-vps.sh
```

### Método 2: Manual
```bash
# En el VPS
cd /opt/atp

# Detener servicios
docker-compose -f docker-compose.prod.yml down

# Actualizar código (subir nuevos archivos)
# ... (usar scp como en deployment inicial)

# Reconstruir y reiniciar
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🛑 Detener Servicios
```bash
docker-compose -f docker-compose.prod.yml down
```

## 🗑️ Limpiar Sistema
```bash
# Eliminar contenedores e imágenes antiguas
docker system prune -a

# Eliminar volúmenes no usados
docker volume prune
```

## 🔒 Seguridad Adicional

### 1. Cambiar puerto SSH (recomendado)
```bash
nano /etc/ssh/sshd_config
# Cambiar: Port 22822 a otro puerto
systemctl restart sshd
```

### 2. Deshabilitar login root (después de crear usuario)
```bash
adduser tuusuario
usermod -aG sudo tuusuario
# Luego en sshd_config: PermitRootLogin no
```

### 3. Instalar Fail2Ban
```bash
apt update
apt install fail2ban -y
systemctl enable fail2ban
systemctl start fail2ban
```

## 📝 Notas Importantes

1. **Las API keys NUNCA se almacenan en el servidor**
2. **Cada usuario configura sus propias keys en su navegador**
3. **No hay base de datos de usuarios**
4. **El servidor solo sirve la interfaz web estática**
5. **Las peticiones a APIs se hacen desde el navegador del usuario**

## 🆘 Troubleshooting

### Puerto 80 ocupado
```bash
# Ver qué está usando el puerto
lsof -i :80
# Detener el servicio
systemctl stop apache2  # o nginx
```

### Docker no inicia
```bash
systemctl status docker
systemctl start docker
```

### Contenedores no arrancan
```bash
docker-compose -f docker-compose.prod.yml logs
```

### Sin espacio en disco
```bash
df -h
docker system prune -a
```

## 📞 Soporte

Para problemas o preguntas:
1. Revisar logs: `docker-compose logs -f`
2. Verificar estado: `docker-compose ps`
3. Reiniciar servicios: `docker-compose restart`

---

**🎉 ¡Tu aplicación ATP v2.0.0 está lista para compartir con el mundo!**

Los usuarios podrán:
- ✅ Acceder desde cualquier navegador
- ✅ Configurar sus propias API keys
- ✅ Usar todos los 30 agentes
- ✅ Crear workflows visuales
- ✅ Sin riesgo de compartir credenciales
