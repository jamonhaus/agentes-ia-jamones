"""
ROUTER PARA GPT ACTIONS
Este archivo contiene los endpoints que configurarás en los Actions de tus GPTs
"""
import json
import uuid
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from agents.orchestrator import AgentOrchestrator
from config.config import config

router = APIRouter(prefix="/gpt", tags=["GPT Actions"])
orchestrator = AgentOrchestrator()

# Almacenamiento en memoria de trabajos asíncronos
async_jobs: Dict[str, Dict[str, Any]] = {}

# ============= MODELOS =============

class TaskRequest(BaseModel):
    """Solicitud de tarea para un agente especializado"""
    agent_id: str
    task: str
    context: Optional[Dict[str, Any]] = None

class DirectorRequest(BaseModel):
    """Solicitud al Director (Andrés) para orquestar"""
    request: str
    required_agents: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None

class TeamCoordinationRequest(BaseModel):
    """Solicitud de coordinación entre múltiples agentes"""
    project: str
    objective: str
    agents: List[str]
    context: Optional[Dict[str, Any]] = None


class WorkflowStep(BaseModel):
    """Paso individual dentro de un workflow encadenado"""
    agent: str
    task: str


class WorkflowRequest(BaseModel):
    """Solicitud para ejecutar un workflow completo"""
    workflow_name: Optional[str] = "Unnamed Workflow"
    steps: List[WorkflowStep]
    context: Optional[Dict[str, Any]] = None




from pydantic import Field

class SmartRequest(BaseModel):
    """Solicitud para la coordinación automática completa"""
    request: str = Field(..., description="La petición del usuario que requiere coordinación de múltiples agentes especializados")
    context: dict = Field(default_factory=dict, description="Contexto adicional opcional para la petición")

    model_config = {
        "json_schema_extra": {
            "example": {
                "request": "Estudio mercado Madrid",
                "context": {}
            }
        }
    }


# ============= FUNCIONES AUXILIARES PARA JOBS ASÍNCRONOS =============

def process_coordination_job(job_id: str, user_request: str, context: Dict[str, Any]):
    """Procesar coordinación en background"""
    try:
        async_jobs[job_id]["status"] = "processing"
        async_jobs[job_id]["started_at"] = datetime.now().isoformat()
        
        # Ejecutar coordinación automática CON colaboración
        execution = orchestrator.auto_coordinate(user_request, context)
        
        if execution["status"] == "failed":
            async_jobs[job_id]["status"] = "failed"
            async_jobs[job_id]["error"] = execution.get("error")
        else:
            # Preparar respuesta estructurada
            response = {
                "peticion_original": user_request,
                "tipo_trabajo": execution.get("director_plan", {}).get("tipo_peticion", "análisis general"),
                "equipo_participante": [],
                "proceso": {
                    "modo": execution.get("execution_mode", "paralelo"),
                    "director": "Andrés coordinó el equipo"
                },
                "conversaciones_entre_agentes": execution.get("agent_conversations", []),
                "respuesta_final": execution.get("final_response"),
                "timestamp": execution["timestamp"]
            }
            
            # Agregar info de los agentes que participaron
            if "agent_results" in execution:
                for agent_id, result in execution["agent_results"].items():
                    response["equipo_participante"].append({
                        "agente": result.get("agent"),
                        "tarea": result.get("tarea_asignada")
                    })
            
            async_jobs[job_id]["status"] = "completed"
            async_jobs[job_id]["result"] = response
            
    except Exception as e:
        async_jobs[job_id]["status"] = "failed"
        async_jobs[job_id]["error"] = str(e)
    
    async_jobs[job_id]["completed_at"] = datetime.now().isoformat()


# ============= ENDPOINTS PARA ACTIONS =============

@router.post("/smart/request")
async def smart_request(request: SmartRequest, background_tasks: BackgroundTasks):
    """
    ENDPOINT PRINCIPAL: Coordinación automática completa (ASÍNCRONO)
    
    Inicia la coordinación en background y devuelve un job_id para consultar estado.
    """
    try:
        user_request = request.request
        if not user_request:
            raise HTTPException(
                status_code=400,
                detail="Falta el parámetro 'request' con la petición del usuario"
            )
        
        context = request.context or {}
        
        # Crear job asíncrono
        job_id = str(uuid.uuid4())
        async_jobs[job_id] = {
            "status": "queued",
            "request": user_request,
            "context": context,
            "created_at": datetime.now().isoformat()
        }
        
        # Iniciar procesamiento en background
        background_tasks.add_task(process_coordination_job, job_id, user_request, context)
        
        return {
            "job_id": job_id,
            "status": "queued",
            "message": "Coordinación iniciada. Los agentes están trabajando juntos. Consulta el estado en /gpt/smart/status/{job_id}",
            "estimated_time": "60-180 segundos"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/smart/request/sync")
async def smart_request_sync(request: SmartRequest):
    """
    Consultar el estado de un trabajo de coordinación
    """
    try:
        user_request = request.request
        if not user_request:
            raise HTTPException(
                status_code=400,
                detail="Falta el parámetro 'request' con la petición del usuario"
            )
        context = request.context or {}
        # Ejecutar coordinación automática
        execution = orchestrator.auto_coordinate(user_request, context)
        if execution["status"] == "failed":
            raise HTTPException(status_code=500, detail=execution.get("error"))
        # Preparar respuesta estructurada
        response = {
            "peticion_original": user_request,
            "tipo_trabajo": execution.get("director_plan", {}).get("tipo_peticion", "análisis general"),
            "equipo_participante": [],
            "proceso": {
                "modo": execution.get("execution_mode", "paralelo"),
                "director": "Andrés coordinó el equipo"
            },
            "conversaciones_entre_agentes": execution.get("agent_conversations", []),
            "respuesta_final": execution.get("final_response"),
            "timestamp": execution["timestamp"]
        }
        # Agregar info de los agentes que participaron
        if "agent_results" in execution:
            for agent_id, result in execution["agent_results"].items():
                response["equipo_participante"].append({
                    "agente": result.get("agent"),
                    "tarea": result.get("tarea_asignada")
                })
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/task/execute")
async def execute_agent_task(request: TaskRequest):
    """ACTION: Ejecutar tarea con agente. Ej: {"agent_id": "adrian_datos", "task": "Analiza ventas Q4", "context": {}}"""
    try:
        agent_config = config.get_agent(request.agent_id)
        execution = orchestrator.execute_simple_task(request.agent_id, request.task)
        
        if execution["status"] == "failed":
            raise HTTPException(status_code=500, detail=execution.get("error"))
        
        return {
            "agent": agent_config.get("name"),
            "task_received": request.task,
            "status": "completed",
            "response": execution.get("result"),
            "timestamp": execution["timestamp"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/director/coordinate")
async def director_coordinate(request: DirectorRequest):
    """ACTION: Director coordina agentes. Ej: {"request": "Analizar ventas Q4", "required_agents": ["adrian_datos"], "context": {}}"""
    try:
        # El Director (Andrés) recibe la petición
        # Validar agentes solicitados (o usar todos si no se especifican)
        try:
            target_agents = request.required_agents or list(config.AGENTS.keys())
            validated_agents = [config.get_agent(aid)["name"] for aid in target_agents]
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        director_prompt = f"""
        Como Andrés, Director de Ventas Online, has recibido esta solicitud: {request.request}
        
        Contexto: {request.context}
        
        Analiza qué especialistas necesitas consultar de esta lista:
        {', '.join(validated_agents)}
        
        Propón un plan de acción: qué pregunta hacer a cada especialista, en qué orden y cómo integrar sus respuestas.
        """
        
        director_analysis = orchestrator.execute_simple_task(
            "andres_director",
            director_prompt
        )
        
        return {
            "director": "Andrés",
            "request": request.request,
            "director_analysis": director_analysis.get("result"),
            "status": "plan_created",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/list")
async def list_all_agents():
    """ACTION: Lista todos los agentes del equipo con sus roles y descripciones"""
    agents_list = []
    for agent_id, agent_config in config.AGENTS.items():
        agents_list.append({
            "id": agent_id,
            "name": agent_config.get("name"),
            "role": agent_config.get("role"),
            "description": agent_config.get("description")
        })
    
    return {
        "total_agents": len(agents_list),
        "team": agents_list
    }


@router.post("/team/analyze")
async def team_analyze(request: TeamCoordinationRequest):
    """ACTION: Coordinación de equipo. Varios agentes aportan análisis sobre un mismo proyecto. Ejemplo: {"project": "Expansion Q1", "objective": "Validar mercados", "agents": ["adrian_datos", "bruno_estrategia"]}"""
    try:
        try:
            for agent_id in request.agents:
                config.get_agent(agent_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        results = orchestrator.execute_parallel_analysis(
            prompt=f"Proyecto: {request.project}\nObjetivo: {request.objective}\nContexto: {request.context}",
            agents=request.agents
        )
        
        if results["status"] == "failed":
            raise HTTPException(status_code=500, detail=results.get("error"))
        
        # Compilar análisis
        team_analysis = []
        for agent_id, agent_result in results["results"].items():
            agent_config = config.get_agent(agent_id)
            team_analysis.append({
                "agent": agent_config["name"],
                "role": agent_config.get("role"),
                "analysis": agent_result.get("response")
            })
        
        return {
            "project": request.project,
            "objective": request.objective,
            "team_analyses": team_analysis,
            "status": "analysis_completed",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflow/execute")
async def execute_workflow(request: WorkflowRequest):
    """ACTION: Pipeline secuencial. Ej: {"workflow_name": "Análisis", "steps": [{"agent": "adrian_datos", "task": "Analizar"}]}"""
    try:
        if not request.steps:
            raise HTTPException(status_code=400, detail="No workflow steps provided")
        
        # Extraer agentes en orden y tareas por paso
        try:
            agent_sequence = [step.agent for step in request.steps]
            for agent_id in agent_sequence:
                config.get_agent(agent_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        step_tasks = [step.task for step in request.steps]

        initial_context_parts = []
        if request.workflow_name:
            initial_context_parts.append(f"Workflow: {request.workflow_name}")
        if request.context:
            initial_context_parts.append(
                f"Contexto inicial: {json.dumps(request.context, ensure_ascii=False)}"
            )

        initial_prompt = "\n\n".join(initial_context_parts).strip()
        
        # Ejecutar pipeline
        execution = orchestrator.execute_pipeline(agent_sequence, initial_prompt, step_tasks)
        
        if execution["status"] == "failed":
            raise HTTPException(status_code=500, detail=execution.get("error"))
        
        return {
            "workflow": request.workflow_name or "Unnamed Workflow",
            "agents_executed": agent_sequence,
            "steps_requested": [step.model_dump() for step in request.steps],
            "initial_context": initial_prompt,
            "results": execution["results"],
            "status": "workflow_completed",
            "timestamp": execution["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health/team")
async def team_health():
    """ACTION: Verifica que todos los agentes estén disponibles"""
    team_status = {
        "total_agents": len(config.AGENTS),
        "agents": {}
    }
    
    for agent_id, agent_config in config.AGENTS.items():
        team_status["agents"][agent_id] = {
            "name": agent_config["name"],
            "role": agent_config.get("role"),
            "status": "available"
        }
    
    return {
        **team_status,
        "api_status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
