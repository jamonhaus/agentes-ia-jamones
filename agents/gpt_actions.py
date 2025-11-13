"""
ROUTER PARA GPT ACTIONS
Este archivo contiene los endpoints que configurarás en los Actions de tus GPTs
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from agents.orchestrator import AgentOrchestrator
from config.config import config

router = APIRouter(prefix="/gpt", tags=["GPT Actions"])
orchestrator = AgentOrchestrator()

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


# ============= ENDPOINTS PARA ACTIONS =============

@router.post("/task/execute")
async def execute_agent_task(request: TaskRequest):
    """
    ENDPOINT PARA ACTIONS: Ejecutar tarea con agente específico
    
    Use this in your GPT Actions to delegate tasks to specialists
    
    Example from Andrés (Director):
    {
        "agent_id": "adrian_datos",
        "task": "Analiza las ventas del último mes por país",
        "context": {"period": "last_month"}
    }
    """
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
    """
    ENDPOINT PARA ACTIONS: Director (Andrés) coordina múltiples agentes
    
    Use this when you need complex coordination
    
    Example:
    {
        "request": "Necesito análisis de ventas Q4 y propuesta de estrategia",
        "required_agents": ["adrian_datos", "bruno_estrategia"],
        "context": {}
    }
    """
    try:
        # El Director (Andrés) recibe la petición
        director_prompt = f"""
        Como Andrés, Director de Ventas Online, has recibido esta solicitud: {request.request}
        
        Contexto: {request.context}
        
        Analiza qué especialistas necesitas consultar de esta lista:
        {', '.join([config.AGENTS[aid]['name'] for aid in request.required_agents or config.AGENTS.keys()])}
        
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
    """
    ENDPOINT PARA ACTIONS: Listar todos los agentes disponibles
    
    Use this in your GPT to understand who's available in the team
    """
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
    """
    ENDPOINT PARA ACTIONS: Análisis coordinado del equipo
    
    Multiple agents analyze the same problem from different angles
    
    Example:
    {
        "project": "Expansion Q1 2024",
        "objective": "Analizar viabilidad de expansión a nuevos mercados",
        "agents": ["adrian_datos", "leo_partners", "bruno_estrategia"],
        "context": {}
    }
    """
    try:
        results = orchestrator.execute_parallel_analysis(
            prompt=f"Proyecto: {request.project}\nObjetivo: {request.objective}\nContexto: {request.context}",
            agents=request.agents
        )
        
        if results["status"] == "failed":
            raise HTTPException(status_code=500, detail=results.get("error"))
        
        # Compilar análisis
        team_analysis = []
        for agent_id, agent_result in results["results"].items():
            agent_name = config.AGENTS[agent_id]["name"]
            team_analysis.append({
                "agent": agent_name,
                "role": config.AGENTS[agent_id].get("role"),
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
async def execute_workflow(request: Dict[str, Any]):
    """
    ENDPOINT PARA ACTIONS: Ejecutar workflow completo (pipeline)
    
    Agents work in sequence, each one using previous output
    
    Example:
    {
        "workflow_name": "Marketing Campaign Analysis",
        "steps": [
            {"agent": "adrian_datos", "task": "Analiza data histórica de campañas"},
            {"agent": "diego_automatizacion", "task": "Propón automatizaciones basadas en análisis"},
            {"agent": "andres_director", "task": "Revisa y da aprobación final"}
        ]
    }
    """
    try:
        workflow_name = request.get("workflow_name", "Unnamed Workflow")
        steps = request.get("steps", [])
        
        if not steps:
            raise HTTPException(status_code=400, detail="No workflow steps provided")
        
        # Extraer agentes en orden
        agent_sequence = [step["agent"] for step in steps]
        initial_prompt = steps[0].get("task", "")
        
        # Ejecutar pipeline
        execution = orchestrator.execute_pipeline(agent_sequence, initial_prompt)
        
        if execution["status"] == "failed":
            raise HTTPException(status_code=500, detail=execution.get("error"))
        
        return {
            "workflow": workflow_name,
            "agents_executed": agent_sequence,
            "results": execution["results"],
            "status": "workflow_completed",
            "timestamp": execution["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health/team")
async def team_health():
    """
    ENDPOINT PARA ACTIONS: Verificar salud del equipo
    
    Check that all agents are available
    """
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
