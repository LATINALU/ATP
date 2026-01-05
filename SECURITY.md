# 🔐 ATP v2.0.0 - Arquitectura de Seguridad

## 🎯 Principio Fundamental

**Las API keys NUNCA se almacenan en el servidor. Cada usuario configura y usa sus propias credenciales directamente desde su navegador.**

## 🏗️ Arquitectura Client-Side

### Cómo Funciona

```
┌─────────────────────────────────────────────────────────────┐
│                    NAVEGADOR DEL USUARIO                     │
│                                                              │
│  1. Usuario abre la aplicación                              │
│  2. Usuario configura sus API keys en ⚙️ Settings           │
│  3. Keys se guardan en localStorage del navegador           │
│  4. Peticiones a APIs se hacen DIRECTAMENTE desde navegador │
│                                                              │
│  ┌──────────────────────────────────────────────┐           │
│  │  localStorage (Solo en este navegador)       │           │
│  │  ┌────────────────────────────────────────┐  │           │
│  │  │ atp-api-providers: {                   │  │           │
│  │  │   "openai": {                          │  │           │
│  │  │     "apiKey": "sk-...",                │  │           │
│  │  │     "models": [...]                    │  │           │
│  │  │   },                                   │  │           │
│  │  │   "anthropic": { ... }                 │  │           │
│  │  │ }                                      │  │           │
│  │  └────────────────────────────────────────┘  │           │
│  └──────────────────────────────────────────────┘           │
│                                                              │
│  Peticiones API:                                            │
│  Browser → OpenAI/Anthropic/etc (DIRECTO)                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    (Solo interfaz HTML/CSS/JS)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      SERVIDOR VPS                            │
│                                                              │
│  ❌ NO almacena API keys                                     │
│  ❌ NO tiene base de datos de usuarios                       │
│  ❌ NO intercepta credenciales                               │
│  ✅ Solo sirve archivos estáticos (HTML/CSS/JS)             │
│  ✅ No procesa ni almacena información sensible             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🔒 Características de Seguridad

### 1. Almacenamiento Client-Side (localStorage)

**Ubicación:** `localStorage` del navegador del usuario

**Características:**
- ✅ Datos aislados por dominio
- ✅ Solo accesibles desde el navegador del usuario
- ✅ No se sincronizan con el servidor
- ✅ Persisten solo en ese dispositivo/navegador
- ✅ Usuario puede borrarlos en cualquier momento

**Código de implementación:**
```typescript
// frontend/src/components/ApiSettings.tsx

// Guardar API keys (SOLO en navegador)
const saveProviders = (newProviders: ApiProvider[]) => {
  setProviders(newProviders);
  if (saveToStorage) {
    localStorage.setItem("atp-api-providers", JSON.stringify(newProviders));
  }
  onProvidersChange(newProviders);
};

// Cargar API keys (SOLO desde navegador)
useEffect(() => {
  const saved = localStorage.getItem("atp-api-providers");
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      setProviders(parsed);
    } catch (e) {
      console.error("Error loading providers:", e);
    }
  }
}, []);
```

### 2. Sin Base de Datos de Usuarios

**El servidor NO tiene:**
- ❌ Base de datos SQL/NoSQL
- ❌ Sistema de autenticación
- ❌ Almacenamiento de credenciales
- ❌ Logs de API keys
- ❌ Sistema de usuarios/cuentas

**El servidor SOLO tiene:**
- ✅ Archivos estáticos (HTML, CSS, JS)
- ✅ Código de la aplicación frontend
- ✅ Lógica de interfaz de usuario

### 3. Peticiones API Directas

Las peticiones a APIs externas (OpenAI, Anthropic, etc.) se hacen **directamente desde el navegador del usuario**:

```typescript
// frontend/src/lib/workflowExecutor.ts

private async executeAgentNode(data: any, inputs: any[], nodeId: string): Promise<string> {
  // API key viene de localStorage del navegador
  const providerConfig = this.findConnectedProvider(nodeId);
  
  // Petición DIRECTA desde el navegador del usuario
  const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: finalMessage,
      agents: [agentName],
      provider: providerConfig?.provider || 'openai',
      model: providerConfig?.model || 'gpt-4',
      // API key del localStorage del usuario
      apiKey: providerConfig?.apiKey,
    }),
  });
}
```

### 4. Aislamiento por Usuario

**Cada usuario tiene:**
- ✅ Su propio localStorage en su navegador
- ✅ Sus propias API keys configuradas
- ✅ Sus propios workflows guardados
- ✅ Su propia configuración de temas/idioma

**Los usuarios NO pueden:**
- ❌ Ver las API keys de otros usuarios
- ❌ Acceder a los workflows de otros usuarios
- ❌ Compartir credenciales accidentalmente
- ❌ Afectar la configuración de otros usuarios

## 🛡️ Medidas de Seguridad Adicionales

### 1. Rate Limiting en Nginx

```nginx
# nginx/nginx.conf

# Limitar peticiones por IP
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=general_limit:10m rate=30r/s;

location /api/ {
  limit_req zone=api_limit burst=10 nodelay;
  # ...
}
```

### 2. Headers de Seguridad

```nginx
# Protección contra clickjacking
add_header X-Frame-Options "SAMEORIGIN" always;

# Prevenir MIME type sniffing
add_header X-Content-Type-Options "nosniff" always;

# Protección XSS
add_header X-XSS-Protection "1; mode=block" always;

# Política de referrer
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

### 3. HTTPS (Opcional pero Recomendado)

Para habilitar HTTPS con Let's Encrypt:

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx

# Obtener certificado (requiere dominio)
certbot --nginx -d tu-dominio.com

# Renovación automática
certbot renew --dry-run
```

### 4. Firewall UFW

```bash
# Permitir solo puertos necesarios
ufw allow 22822/tcp  # SSH
ufw allow 80/tcp     # HTTP
ufw allow 443/tcp    # HTTPS
ufw enable
```

## 🔍 Verificación de Seguridad

### Comprobar que NO hay API keys en el servidor

```bash
# Conectar al VPS
ssh -p 22822 root@147.93.191.92

# Buscar API keys (no debería encontrar nada)
cd /opt/atp
grep -r "sk-" . 2>/dev/null
grep -r "apiKey" backend/ 2>/dev/null

# Verificar que no hay base de datos
ls -la | grep -E "\.db|\.sqlite|mysql|postgres"
```

### Comprobar localStorage en el navegador

1. Abrir DevTools (F12)
2. Ir a Application → Local Storage
3. Buscar `atp-api-providers`
4. Verificar que las keys están ahí

### Comprobar peticiones de red

1. Abrir DevTools (F12) → Network
2. Ejecutar un workflow
3. Verificar que las peticiones van directamente a:
   - `api.openai.com`
   - `api.anthropic.com`
   - etc.

## 📊 Comparación con Otros Sistemas

| Característica | ATP v2.0.0 | Sistemas Tradicionales |
|----------------|------------|------------------------|
| **Almacenamiento de API keys** | ❌ No (client-side) | ✅ Sí (servidor) |
| **Base de datos de usuarios** | ❌ No | ✅ Sí |
| **Sistema de autenticación** | ❌ No necesario | ✅ Sí (login/password) |
| **Riesgo de filtración** | 🟢 Muy bajo | 🔴 Alto |
| **Privacidad del usuario** | 🟢 Máxima | 🟡 Limitada |
| **Mantenimiento** | 🟢 Mínimo | 🔴 Alto |
| **Costos de servidor** | 🟢 Muy bajo | 🔴 Alto |

## ⚠️ Consideraciones Importantes

### Ventajas

1. **Privacidad Total**: Las API keys nunca salen del navegador del usuario
2. **Sin Riesgo de Filtración**: No hay base de datos que hackear
3. **Costo Cero**: No necesitas pagar por almacenamiento o bases de datos
4. **Escalabilidad**: Cada usuario usa sus propios recursos
5. **Simplicidad**: No necesitas gestionar usuarios ni autenticación

### Limitaciones

1. **Datos por Dispositivo**: Si el usuario cambia de navegador/dispositivo, debe reconfigurar
2. **Sin Sincronización**: Los workflows no se sincronizan entre dispositivos
3. **Borrado de Datos**: Si el usuario borra localStorage, pierde su configuración

### Soluciones a las Limitaciones

**Para compartir configuración entre dispositivos:**
- Usar la función Import/Export de workflows
- Exportar configuración como JSON
- Importar en otro dispositivo

**Para backup:**
```javascript
// Exportar configuración
const config = localStorage.getItem('atp-api-providers');
const blob = new Blob([config], { type: 'application/json' });
// Descargar archivo
```

## 🎓 Educación del Usuario

### Mensaje en la Interfaz

Agregar un banner informativo en la configuración de APIs:

```typescript
<div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 mb-4">
  <div className="flex items-start gap-3">
    <Shield className="h-5 w-5 text-blue-500 mt-0.5" />
    <div>
      <h4 className="font-semibold text-sm mb-1">🔐 Tus datos están seguros</h4>
      <p className="text-xs text-muted-foreground">
        Tus API keys se almacenan SOLO en tu navegador (localStorage). 
        Nunca se envían al servidor ni se comparten con otros usuarios.
        Solo tú tienes acceso a tus credenciales.
      </p>
    </div>
  </div>
</div>
```

## 📝 Resumen

✅ **Las API keys se almacenan en localStorage del navegador del usuario**
✅ **El servidor NO almacena, procesa ni ve las API keys**
✅ **Cada usuario usa sus propias credenciales de forma aislada**
✅ **No hay riesgo de filtración de credenciales desde el servidor**
✅ **Arquitectura simple, segura y escalable**

---

**Esta arquitectura garantiza que tu VPS no tiene ninguna responsabilidad sobre las credenciales de los usuarios, eliminando riesgos legales y de seguridad.**
