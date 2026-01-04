@echo off
echo ========================================
echo    ATP - Agentes de Tareas Polivalentes
echo    Sistema de 30 Agentes de IA
echo ========================================
echo.

echo [1] Iniciando con Docker Compose...
docker-compose up -d backend frontend

echo.
echo [2] Esperando a que los servicios inicien...
timeout /t 10 /nobreak > nul

echo.
echo ========================================
echo    SISTEMA LISTO
echo ========================================
echo.
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo    Para detener: docker-compose down
echo ========================================

start http://localhost:3000
pause
