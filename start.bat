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
