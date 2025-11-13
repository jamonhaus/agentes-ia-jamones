@echo off
REM Script para iniciar el orquestador de agentes IA (Windows)

echo 🤖 Iniciando Orquestador de Agentes IA...
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    exit /b 1
)

REM Instalar dependencias si es necesario
if not exist ".venv" (
    echo 📦 Creando entorno virtual...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    echo ✅ Entorno virtual existente
    call .venv\Scripts\activate.bat
)

REM Validar configuración
if not exist ".env" (
    echo ⚠️  No existe .env
    exit /b 1
)

REM Detectar modo
if "%1"=="test" (
    echo 🧪 Ejecutando pruebas...
    python test_agents.py
) else if "%1"=="api" (
    echo 🚀 Iniciando API...
    python main.py
) else (
    echo ❓ Uso: start.bat [test^|api]
    echo.
    echo Ejemplos:
    echo   start.bat api    # Iniciar API FastAPI
    echo   start.bat test   # Ejecutar pruebas
)
