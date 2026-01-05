# 🚀 Instrucciones de Instalación en VPS

## 📋 Datos de tu VPS

- **IP**: 147.93.191.92
- **Puerto SSH**: 22822
- **Usuario**: root
- **OS**: Ubuntu 24.04
- **Dominio**: atp-app.duckdns.org

## 🔧 Paso 1: Configurar DuckDNS

1. Ve a https://www.duckdns.org/
2. Inicia sesión con tu cuenta
3. Verifica que el dominio `atp-app` esté configurado con la IP `147.93.191.92`
4. Copia tu token de DuckDNS (lo necesitarás después)

## 🖥️ Paso 2: Conectar al VPS

Abre tu terminal SSH favorita (PuTTY, MobaXterm, o terminal) y conecta:

```bash
ssh -p 22822 root@147.93.191.92
```

Contraseña: `Qa1Ws2Ed1`

## 📦 Paso 3: Ejecutar Instalación Automática

Una vez dentro del VPS, ejecuta estos comandos:

```bash
# Descargar script de instalación
curl -o install.sh https://raw.githubusercontent.com/LATINALU/ATP/main/INSTALL_VPS.sh

# Dar permisos de ejecución
chmod +x install.sh

# Ejecutar instalación
./install.sh
```

**El script hará automáticamente:**
- ✅ Actualizar el sistema
- ✅ Instalar Docker y Docker Compose
- ✅ Clonar el repositorio ATP
- ✅ Configurar variables de entorno
- ✅ Configurar firewall
- ✅ Construir e iniciar servicios

**Tiempo estimado: 5-10 minutos**

## 🔄 Paso 4: Configurar Auto-actualización de DuckDNS (Opcional)

Para mantener tu dominio actualizado automáticamente:

```bash
# Crear directorio
mkdir -p /opt/duckdns
cd /opt/duckdns

# Crear script (reemplaza TU-TOKEN con tu token de DuckDNS)
cat > duck.sh << 'EOF'
#!/bin/bash
echo url="https://www.duckdns.org/update?domains=atp-app&token=TU-TOKEN&ip=" | curl -k -o /opt/duckdns/duck.log -K -
EOF

# Dar permisos
chmod +x duck.sh

# Probar el script
./duck.sh
cat duck.log  # Debería decir "OK"

# Agregar a crontab para actualizar cada 5 minutos
crontab -e
# Agregar esta línea al final:
# */5 * * * * /opt/duckdns/duck.sh >/dev/null 2>&1
```

## ✅ Paso 5: Verificar Instalación

```bash
# Ver estado de servicios
cd /opt/atp
docker-compose -f docker-compose.prod.yml ps

# Deberías ver:
# atp-nginx      Up      0.0.0.0:80->80/tcp
# atp-frontend   Up      0.0.0.0:3000->3000/tcp
# atp-backend    Up      0.0.0.0:8000->8000/tcp

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
# Presiona Ctrl+C para salir
```

## 🌐 Paso 6: Probar Acceso

Abre tu navegador y visita:

- **Por IP**: http://147.93.191.92
- **Por dominio**: http://atp-app.duckdns.org

Deberías ver la interfaz de ATP v2.0.0

## 🔧 Comandos Útiles

### Ver logs en tiempo real
```bash
cd /opt/atp
docker-compose -f docker-compose.prod.yml logs -f
```

### Reiniciar servicios
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Detener servicios
```bash
docker-compose -f docker-compose.prod.yml down
```

### Iniciar servicios
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Ver uso de recursos
```bash
docker stats
```

### Actualizar aplicación
```bash
cd /opt/atp
git pull
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🛠️ Solución de Problemas

### Puerto 80 ocupado
```bash
# Ver qué está usando el puerto
lsof -i :80

# Si es Apache o Nginx preinstalado
systemctl stop apache2
systemctl disable apache2
# o
systemctl stop nginx
systemctl disable nginx

# Reiniciar servicios ATP
cd /opt/atp
docker-compose -f docker-compose.prod.yml restart
```

### Servicios no inician
```bash
# Ver logs detallados
docker-compose -f docker-compose.prod.yml logs

# Reconstruir desde cero
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

### Sin espacio en disco
```bash
# Ver espacio disponible
df -h

# Limpiar imágenes Docker antiguas
docker system prune -a

# Limpiar logs del sistema
journalctl --vacuum-time=3d
```

### Firewall bloqueando
```bash
# Ver reglas actuales
ufw status

# Permitir puertos necesarios
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3000/tcp
ufw allow 8000/tcp
```

## 🔐 Seguridad Adicional

### Cambiar contraseña de root
```bash
passwd
```

### Crear usuario no-root
```bash
adduser tuusuario
usermod -aG sudo tuusuario
usermod -aG docker tuusuario
```

### Instalar Fail2Ban
```bash
apt install fail2ban -y
systemctl enable fail2ban
systemctl start fail2ban
```

### Habilitar actualizaciones automáticas
```bash
apt install unattended-upgrades -y
dpkg-reconfigure --priority=low unattended-upgrades
```

## 📊 Monitoreo

### Ver uso de CPU y memoria
```bash
htop
# o
top
```

### Ver logs del sistema
```bash
journalctl -f
```

### Ver conexiones activas
```bash
netstat -tulpn
```

## 🎉 ¡Listo!

Tu aplicación ATP v2.0.0 está corriendo en:
- http://atp-app.duckdns.org
- http://147.93.191.92

Los usuarios pueden:
- ✅ Configurar sus propias API keys (se guardan en su navegador)
- ✅ Usar todos los 30 agentes
- ✅ Crear workflows visuales
- ✅ Cambiar temas e idioma
- ✅ Importar/exportar workflows

**Recuerda:** Las API keys de los usuarios se almacenan SOLO en sus navegadores, no en tu servidor.

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs: `docker-compose logs -f`
2. Verifica el estado: `docker-compose ps`
3. Reinicia servicios: `docker-compose restart`
4. Revisa el firewall: `ufw status`

---

**¡Disfruta compartiendo ATP con el mundo! 🚀**
