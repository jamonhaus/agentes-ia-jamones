"""Modelos de datos para la comunicación entre componentes"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AgentRequest(BaseModel):
    """Solicitud a un agente"""
    agent_id: str
    prompt: str
    context: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    """Respuesta de un agente"""
    agent_id: str
    response: str
    timestamp: str
    status: str

class PipelineRequest(BaseModel):
    """Solicitud para ejecutar un pipeline de agentes"""
    agents_sequence: List[str]
    initial_prompt: str

class PipelineResponse(BaseModel):
    """Respuesta de un pipeline"""
    timestamp: str
    agents: List[str]
    results: Dict[str, Any]
    status: str

class ParallelAnalysisRequest(BaseModel):
    """Solicitud para análisis en paralelo"""
    prompt: str
    agents: Optional[List[str]] = None

class WorkflowExecution(BaseModel):
    """Ejecución de un workflow"""
    workflow_id: Optional[str] = None
    workflow_type: str  # "simple", "pipeline", "parallel"
    status: str
    timestamp: str
    results: Dict[str, Any]
