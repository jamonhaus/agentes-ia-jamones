from copy import deepcopy
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from config.config import config
from agents.orchestrator import AgentOrchestrator
from agents.gpt_actions import router as gpt_router
from shared.models import (
    AgentRequest, AgentResponse, PipelineRequest, 
    ParallelAnalysisRequest, WorkflowExecution
)
from datetime import datetime
import uvicorn

# Validar configuración
config.validate()

# Crear app FastAPI
app = FastAPI(
    title=config.__class__.__name__,
    description="Orquestador de agentes de IA con OpenAI",
    version="1.0.2"
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        description=app.description,
    )

    openapi_schema["servers"] = [{"url": config.PUBLIC_URL.rstrip("/") or "https://agentes-ia-jamones.onrender.com"}]

    # For GPT Actions compatibility, inline ALL request schemas (avoid $ref)
    gpt_endpoints_schemas = {
        "/gpt/task/execute": "TaskRequest",
        "/gpt/director/coordinate": "DirectorRequest",
        "/gpt/team/analyze": "TeamCoordinationRequest",
        "/gpt/workflow/execute": "WorkflowRequest"
    }
    
    # /gpt/smart/request usa Dict[str, Any] - ya está inline por defecto, no necesita procesamiento
    
    for endpoint_path, schema_name in gpt_endpoints_schemas.items():
        try:
            component = openapi_schema["components"]["schemas"][schema_name]
            inline_schema = {
                "type": "object",
                "required": component.get("required", []),
                "properties": deepcopy(component.get("properties", {})),
                "description": component.get("description", "")
            }
            request_body_path = openapi_schema["paths"][endpoint_path]["post"]["requestBody"]["content"]["application/json"]
            request_body_path["schema"] = inline_schema
        except KeyError:
            pass

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Inicializar orquestador
orchestrator = AgentOrchestrator()

# Registrar routers
app.include_router(gpt_router)

# ============= ENDPOINTS =============

@app.get("/", include_in_schema=False)
async def root():
    """Endpoint raíz - verificar que la API está funcionando"""
    return {
        "mensaje": "Orquestador de Agentes IA activo",
        "versión": "1.0.0",
        "agentes_disponibles": list(config.AGENTS.keys())
    }

@app.get("/agents", include_in_schema=False)
async def list_agents():
    """Listar todos los agentes disponibles"""
    agents = []
    for agent_id, agent_config in config.AGENTS.items():
        agents.append({
            "id": agent_id,
            "nombre": agent_config["name"],
            "descripción": agent_config["description"]
        })
    return {"agentes": agents}

@app.post("/execute/simple", include_in_schema=False)
async def execute_simple_task(request: AgentRequest):
    """
    Ejecutar una tarea simple con un agente específico
    
    Ejemplo:
    {
        "agent_id": "analyst",
        "prompt": "Analiza este conjunto de datos...",
        "context": {}
    }
    """
    try:
        execution = orchestrator.execute_simple_task(request.agent_id, request.prompt)
        
        if execution["status"] == "failed":
            raise HTTPException(status_code=500, detail=execution.get("error"))
        
        return {
            "agente": execution["agent_id"],
            "estado": execution["status"],
            "resultado": execution.get("result"),
            "timestamp": execution["timestamp"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute/pipeline", include_in_schema=False)
async def execute_pipeline(request: PipelineRequest):
    """
    Ejecutar un pipeline donde la salida de un agente es entrada del siguiente
    
    Ejemplo:
    {
        "agents_sequence": ["analyst", "processor", "coordinator"],
        "initial_prompt": "Analiza estos datos y crea un reporte..."
    }
    """
    try:
        execution = orchestrator.execute_pipeline(
            request.agents_sequence, 
            request.initial_prompt
        )
        
        if execution["status"] == "failed":
            raise HTTPException(status_code=500, detail=execution.get("error"))
        
        return {
            "estado": execution["status"],
            "agentes": execution["agents"],
            "resultados": execution["results"],
            "timestamp": execution["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute/parallel", include_in_schema=False)
async def execute_parallel_analysis(request: ParallelAnalysisRequest):
    """
    Ejecutar el mismo prompt en múltiples agentes en paralelo
    
    Ejemplo:
    {
        "prompt": "¿Cuál es tu análisis sobre esto?",
        "agents": ["analyst", "processor"]
    }
    """
    try:
        execution = orchestrator.execute_parallel_analysis(
            request.prompt,
            request.agents
        )
        
        if execution["status"] == "failed":
            raise HTTPException(status_code=500, detail=execution.get("error"))
        
        return {
            "estado": execution["status"],
            "agentes": execution["agents"],
            "resultados": execution["results"],
            "timestamp": execution["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", include_in_schema=False)
async def get_execution_history():
    """Obtener el historial de todas las ejecuciones"""
    return {
        "total": len(orchestrator.execution_history),
        "ejecuciones": orchestrator.execution_history
    }

@app.get("/health", include_in_schema=False)
async def health_check():
    """Verificar que la API está saludable"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ============= MAIN =============

if __name__ == "__main__":
    print(f"🚀 Iniciando Orquestador de Agentes IA")
    print(f"📍 Dirección: {config.API_HOST}:{config.API_PORT}")
    print(f"🤖 Agentes disponibles: {', '.join(config.AGENTS.keys())}")
    print(f"📚 Documentación: http://{config.API_HOST}:{config.API_PORT}/docs")
    
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        reload=False
    )
