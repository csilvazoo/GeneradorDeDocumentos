# 🌐 Generador de Documentos Funcionales - Versión Web

Versión web del generador de documentos AFU2505, diseñada para ejecutarse en navegadores web dentro del entorno de intranet corporativa.

## 🚀 Características

- ✅ **Interfaz web moderna** - React con diseño responsive
- ✅ **Sin backend requerido** - Todo el procesamiento en el navegador
- ✅ **Conexión directa a intranet** - Acceso HTTP directo desde el navegador
- ✅ **Generación de documentos Word** - Usando librería docx.js
- ✅ **Logs en tiempo real** - Visualización del progreso del proceso
- ✅ **Deploy en Netlify** - Fácil distribución y actualizaciones

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Red Empresarial│    │   Intranet      │
│   Netlify       │───▶│   (Usuario)     │───▶│   reportes03    │
│   (React App)   │    │   navegador     │    │   (Servidor)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Requisitos

- **Navegador moderno** (Chrome, Firefox, Edge, Safari)
- **Acceso a red corporativa** donde está disponible `reportes03`
- **JavaScript habilitado**

## 🔧 Desarrollo Local

```bash
# Instalar dependencias
cd web/
npm install

# Ejecutar en desarrollo
npm start

# Construir para producción
npm run build
```

## 🚀 Deploy en Netlify

1. **Push a repositorio Git**
2. **Conectar con Netlify**
3. **Configurar build settings:**
   - Build command: `npm run build`
   - Publish directory: `build`
4. **Deploy automático** en cada push

## 🔄 Equivalencias con Versión Desktop

| Funcionalidad Desktop | Implementación Web |
|----------------------|-------------------|
| `logic.py` | `intranetApi.js` + `dataExtractor.js` |
| `selenium_helpers.py` | Fetch API nativo |
| `requerimientos.py` | `dataExtractor.js` |
| `docx_helpers.py` | `documentGenerator.js` (docx library) |
| GUI con tkinter | React components |
| Logs en terminal | Logs en interfaz web |

## 📁 Estructura del Proyecto

```
web/
├── public/
│   └── index.html          # HTML principal
├── src/
│   ├── components/
│   │   ├── DocumentGenerator.js  # Componente principal
│   │   └── DocumentGenerator.css
│   ├── services/
│   │   ├── intranetApi.js         # API calls a intranet
│   │   └── documentGenerator.js   # Generación Word
│   ├── utils/
│   │   └── dataExtractor.js       # Lógica de extracción
│   ├── App.js              # Componente raíz
│   ├── App.css
│   ├── index.js            # Entry point
│   └── index.css           # Estilos globales
├── package.json            # Dependencias
└── netlify.toml           # Configuración Netlify
```

## 🔧 Configuración CORS

Si encuentras problemas de CORS al acceder a la intranet, el administrador de sistemas puede configurar:

```apache
# En el servidor reportes03
Header set Access-Control-Allow-Origin "*"
Header set Access-Control-Allow-Methods "GET, POST, OPTIONS"
Header set Access-Control-Allow-Headers "Content-Type"
```

## 🐛 Troubleshooting

### Error: "No se puede conectar con la intranet"
- Verificar que estés en la red corporativa
- Verificar que `http://reportes03` sea accesible desde tu navegador
- Revisar configuración de proxy corporativo

### Error: "CORS blocked"
- Contactar al administrador de sistemas para configurar CORS
- Usar extensión de navegador para desarrollo local

### Error: "Failed to generate document"
- Verificar que los datos de intranet sean válidos
- Revisar logs del navegador (F12 → Console)

## 📊 Diferencias vs Versión Desktop

### ✅ Ventajas Web
- Acceso desde cualquier dispositivo en la red
- No requiere instalación local
- Actualizaciones automáticas
- Interfaz más moderna

### ⚠️ Limitaciones Web
- Requiere conexión a intranet
- Depende de CORS configuration
- Sin acceso directo al sistema de archivos

## 🔄 Migración de Desktop

Los usuarios pueden seguir usando la versión desktop mientras prueban la web. Ambas versiones:
- Generan documentos idénticos
- Usan la misma lógica de negocio
- Acceden a los mismos datos de intranet

## 📝 Roadmap

- [ ] Función "Actualizar documento existente"
- [ ] Caché local de datos frecuentes
- [ ] Modo offline limitado
- [ ] Estadísticas de uso
- [ ] Personalización de plantillas
