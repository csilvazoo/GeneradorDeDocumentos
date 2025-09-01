# 🚀 Generador de Documentos Funcionales - Versión Web con Proxy

Esta solución combina una aplicación web React con un servidor proxy Python para acceder a la intranet corporativa sin problemas de CORS.

## 📋 Componentes

### 1. **Aplicación Web React** (`/web/`)
- Interfaz de usuario moderna
- Generación de documentos Word
- Logs en tiempo real

### 2. **Servidor Proxy Python** (`proxy_server.py`)
- Intermediario entre la app web y la intranet
- Manejo de CORS
- Logging detallado

## 🔧 Configuración e Instalación

### Paso 1: Instalar dependencias del proxy
```bash
pip install -r proxy_requirements.txt
```

### Paso 2: Instalar dependencias de la aplicación web
```bash
cd web
npm install
```

## 🚀 Uso

### 1. Iniciar el servidor proxy (Terminal 1)
```bash
python proxy_server.py
```
**Output esperado:**
```
🚀 Servidor Proxy iniciado en: http://localhost:5000
📋 Endpoints disponibles:
   • GET /health - Verificar estado del servidor
   • GET /api/funcionalidad/<numero> - Obtener datos de funcionalidad
   • GET /api/requerimiento/<numero> - Obtener datos de requerimiento
```

### 2. Iniciar la aplicación web (Terminal 2)
```bash
cd web
npm start
```
**Output esperado:**
```
Local:            http://localhost:3000
On Your Network:  http://192.168.x.x:3000
```

### 3. Usar la aplicación
1. Abrir http://localhost:3000 en tu navegador
2. Ingresar el número de funcionalidad (ej: 9107)
3. Hacer clic en "🚀 Generar Documento"
4. Observar los logs en tiempo real
5. El documento se descargará automáticamente

## 🔍 Troubleshooting

### Error: "No se puede conectar con el servidor proxy"
- ✅ Verificar que `proxy_server.py` esté ejecutándose
- ✅ Verificar que el puerto 5000 esté libre
- ✅ Comprobar que no haya firewall bloqueando

### Error: "No se puede conectar con la intranet"
- ✅ Verificar que estés en la red corporativa
- ✅ Verificar que `http://reportes03` sea accesible desde tu máquina
- ✅ Comprobar los logs del servidor proxy

### Verificar conectividad
```bash
# Probar el proxy
curl http://localhost:5000/health

# Probar acceso a funcionalidad
curl http://localhost:5000/api/funcionalidad/9107
```

## 📁 Estructura del Proyecto

```
/
├── proxy_server.py           # Servidor proxy Python
├── proxy_requirements.txt    # Dependencias del proxy
├── web/                      # Aplicación React
│   ├── package.json
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   └── DocumentGenerator.js
│   │   ├── services/
│   │   │   ├── intranetApi.js      # API que usa el proxy
│   │   │   └── documentGenerator.js
│   │   └── utils/
│   └── public/
├── app/                      # Código Python original
└── README.md                 # Este archivo
```

## 🌐 URLs Importantes

- **Aplicación Web**: http://localhost:3000
- **Servidor Proxy**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Funcionalidad**: http://localhost:5000/api/funcionalidad/{numero}
- **API Requerimiento**: http://localhost:5000/api/requerimiento/{numero}

## ⚡ Script de Inicio Rápido

Crear un archivo `start.bat` para Windows:

```batch
@echo off
echo 🚀 Iniciando Generador de Documentos Funcionales...
echo.
echo 📋 Iniciando servidor proxy...
start "Proxy Server" cmd /k "python proxy_server.py"
timeout /t 3 /nobreak > nul
echo.
echo 🌐 Iniciando aplicación web...
cd web
start "Web App" cmd /k "npm start"
echo.
echo ✅ Servicios iniciados!
echo 🔗 Aplicación web: http://localhost:3000
echo 🔗 Servidor proxy: http://localhost:5000
pause
```

## 🎯 Ventajas de esta solución

- ✅ **Sin problemas de CORS**: El proxy maneja las peticiones a la intranet
- ✅ **Interfaz moderna**: React con feedback visual en tiempo real  
- ✅ **Fácil debugging**: Logs detallados en ambos componentes
- ✅ **Escalable**: Fácil de extender con nuevas funcionalidades
- ✅ **Portable**: Funciona en cualquier máquina con Python y Node.js
