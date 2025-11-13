# 🤖 Orquestador de Agentes IA con OpenAI

Sistema profesional para gestionar la comunicación entre múltiples agentes de IA usando ChatGPT Plus (OpenAI API).

## 📋 Características

✅ **3 modos de ejecución:**
- **Simple**: Ejecutar una tarea con un agente único
- **Pipeline**: Agentes en secuencia (salida de uno = entrada del siguiente)
- **Paralelo**: Mismo prompt en múltiples agentes simultáneamente

✅ **Arquitectura profesional:**
- Configuración centralizada
- Cliente reutilizable para OpenAI
- Modelos de datos con Pydantic
- API REST con FastAPI
- Historial de ejecuciones

✅ **3 agentes pre-configurados:**
- **Analyst**: Especializado en análisis de datos
- **Processor**: Especializado en procesamiento y transformación
- **Coordinator**: Orquesta tareas entre otros agentes

## 📁 Estructura del Proyecto

```
PROYECTO1/
├── main.py                 # API FastAPI principal
├── test_agents.py          # Script de pruebas
├── requirements.txt        # Dependencias Python
├── .env                    # Configuración (API keys)
│
├── config/
│   ├── __init__.py
│   └── config.py          # Configuración centralizada
│
├── agents/
│   ├── __init__.py
│   └── orchestrator.py    # Orquestador de agentes
│
├── shared/
│   ├── __init__.py
│   ├── client.py          # Cliente de OpenAI
│   └── models.py          # Modelos Pydantic
│
└── logs/                  # Historial de ejecuciones
```

## 🚀 Instalación y Configuración

### 1. Requisitos previos
- Python 3.8+
- Cuenta OpenAI con API key
- ChatGPT Plus (GPT-4)

### 2. Configurar variables de entorno

Edita el archivo `.env`:

```env
OPENAI_API_KEY=sk-tu-api-key-aqui
OPENAI_MODEL=gpt-4
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

O instala manualmente:
```bash
pip install fastapi uvicorn pydantic openai python-dotenv requests
```

## 💻 Uso

### Opción 1: Ejecutar la API FastAPI

```bash
python main.py
```

La API estará disponible en: `http://localhost:8000`

**Documentación interactiva**: `http://localhost:8000/docs`

### Opción 2: Ejecutar pruebas

```bash
python test_agents.py
```

Esto ejecutará 3 pruebas:
1. **Tarea simple** con el agente Analyst
2. **Pipeline** con 3 agentes en secuencia
3. **Análisis paralelo** con todos los agentes

## 📡 API Endpoints

### 1. Listar agentes disponibles
```bash
GET /agents
```

**Respuesta:**
```json
{
  "agentes": [
    {
      "id": "analyst",
      "nombre": "Analyst Agent",
      "descripción": "Especializado en análisis de datos"
    },
    ...
  ]
}
```

### 2. Ejecutar tarea simple
```bash
POST /execute/simple
```

**Body:**
```json
{
  "agent_id": "analyst",
  "prompt": "¿Cuáles son las 3 principales ventajas de usar IA?",
  "context": {}
}
```

**Respuesta:**
```json
{
  "agente": "analyst",
  "estado": "completed",
  "resultado": "Las principales ventajas son...",
  "timestamp": "2025-11-12T20:30:00.000000"
}
```

### 3. Ejecutar pipeline
```bash
POST /execute/pipeline
```

**Body:**
```json
{
  "agents_sequence": ["analyst", "processor", "coordinator"],
  "initial_prompt": "Dame 3 ideas para mejorar la educación online"
}
```

**Respuesta:**
```json
{
  "estado": "completed",
  "agentes": ["analyst", "processor", "coordinator"],
  "resultados": {
    "analyst": {
      "agent": "analyst",
      "response": "...",
      "order": 1
    },
    "processor": {
      "agent": "processor",
      "response": "...",
      "order": 2
    },
    "coordinator": {
      "agent": "coordinator",
      "response": "...",
      "order": 3
    }
  },
  "timestamp": "2025-11-12T20:30:00.000000"
}
```

### 4. Análisis paralelo
```bash
POST /execute/parallel
```

**Body:**
```json
{
  "prompt": "¿Cuál es la importancia de los datos en IA?",
  "agents": ["analyst", "processor"]
}
```

**Respuesta:**
```json
{
  "estado": "completed",
  "agentes": ["analyst", "processor"],
  "resultados": {
    "analyst": {
      "agent": "analyst",
      "response": "..."
    },
    "processor": {
      "agent": "processor",
      "response": "..."
    }
  },
  "timestamp": "2025-11-12T20:30:00.000000"
}
```

### 5. Obtener historial
```bash
GET /history
```

**Respuesta:**
```json
{
  "total": 5,
  "ejecuciones": [
    {
      "timestamp": "2025-11-12T20:30:00.000000",
      "type": "simple",
      "agent_id": "analyst",
      "status": "completed",
      "result": "..."
    },
    ...
  ]
}
```

### 6. Health check
```bash
GET /health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-12T20:30:00.000000"
}
```

## 🔧 Personalizar Agentes

Edita `config/config.py` para agregar o modificar agentes:

```python
AGENTS = {
    "mi_agente": {
        "name": "Mi Agente Custom",
        "description": "Descripción del agente",
        "instructions": "Instrucciones específicas para el agente"
    }
}
```

## 📝 Ejemplos de Uso con Python

### Ejemplo 1: Tarea Simple

```python
from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

result = orchestrator.execute_simple_task(
    agent_id="analyst",
    prompt="Analiza las tendencias del mercado tecnológico"
)

print(result["result"])
```

### Ejemplo 2: Pipeline

```python
result = orchestrator.execute_pipeline(
    agents_sequence=["analyst", "processor", "coordinator"],
    initial_prompt="Propón un plan de negocio para una startup de IA"
)

for agent_id, data in result["results"].items():
    print(f"\n{agent_id}: {data['response']}")
```

### Ejemplo 3: Análisis Paralelo

```python
result = orchestrator.execute_parallel_analysis(
    prompt="¿Cuáles son los riesgos de la IA?",
    agents=["analyst", "processor"]
)

for agent_id, data in result["results"].items():
    print(f"\n{agent_id}: {data['response']}")
```

## 🔐 Seguridad

⚠️ **Importante:**
- Nunca commits tu `.env` con la API key
- Usa variables de entorno en producción
- Implementa autenticación si expones la API públicamente

## 📊 Casos de Uso

- **Análisis de documentos**: Pipeline analyst → processor
- **Toma de decisiones**: Análisis paralelo para múltiples perspectivas
- **Automatización de tareas**: Coordinar múltiples agentes
- **Investigación**: Dividir tareas entre especialistas
- **Generación de reportes**: Pipeline para procesar información

## 🛠️ Troubleshooting

### Error: "OPENAI_API_KEY no configurada"
- Verifica que has creado el archivo `.env`
- Comprueba que contains una API key válida

### Error: "Agente no encontrado"
- Verifica que el ID del agente existe en `config/config.py`
- Disponibles: analyst, processor, coordinator

### Error de timeout
- Aumenta el timeout en `config/config.py`
- Verifica tu conexión a Internet

## 📚 Documentación OpenAI

- [OpenAI API Docs](https://platform.openai.com/docs)
- [ChatGPT API](https://platform.openai.com/docs/guides/gpt)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

## 📄 Licencia

Este proyecto es de código abierto.

---

**¡Lista para usar! 🚀**

Para iniciar: `python main.py`
