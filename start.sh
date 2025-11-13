#!/bin/bash
# Script para iniciar el orquestador de agentes IA

echo "🤖 Iniciando Orquestador de Agentes IA..."
echo ""

# Verificar Python
if ! command -v python &> /dev/null; then
    echo "❌ Python no está instalado"
    exit 1
fi

# Instalar dependencias si es necesario
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv .venv
    source .venv/Scripts/activate
    pip install -r requirements.txt
else
    echo "✅ Entorno virtual existente"
fi

# Validar configuración
if [ ! -f ".env" ]; then
    echo "⚠️  No existe .env. Copia .env.example a .env"
    exit 1
fi

# Detectar modo
if [ "$1" == "test" ]; then
    echo "🧪 Ejecutando pruebas..."
    python test_agents.py
elif [ "$1" == "api" ]; then
    echo "🚀 Iniciando API..."
    python main.py
else
    echo "❓ Uso: ./start.sh [test|api]"
    echo ""
    echo "Ejemplos:"
    echo "  ./start.sh api    # Iniciar API FastAPI"
    echo "  ./start.sh test   # Ejecutar pruebas"
fi
