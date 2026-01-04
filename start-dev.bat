@echo off
echo ========================================
echo    ATP - Modo Desarrollo
echo ========================================
echo.

echo [1] Iniciando Backend...
start cmd /k "cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [2] Esperando backend...
timeout /t 5 /nobreak > nul

echo [3] Iniciando Frontend...
start cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ========================================
echo    DESARROLLO INICIADO
echo ========================================
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo ========================================
pause
