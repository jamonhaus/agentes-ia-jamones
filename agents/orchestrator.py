"""Orquestador de agentes - gestiona la comunicación entre agentes"""

from shared.client import AIAgentClient
from config.config import config
import json
from datetime import datetime

class AgentOrchestrator:
    """Coordina y gestiona la comunicación entre múltiples agentes de IA"""
    
    def __init__(self):
        self.client = AIAgentClient(config.OPENAI_API_KEY)
        self.execution_history = []
    
    def execute_simple_task(self, agent_id: str, prompt: str) -> dict:
        """
        Ejecuta una tarea simple con un agente único
        
        Args:
            agent_id: ID del agente a usar
            prompt: Descripción de la tarea
            
        Returns:
            Dict con el resultado de la ejecución
        """
        execution = {
            "timestamp": datetime.now().isoformat(),
            "type": "simple",
            "agent_id": agent_id,
            "prompt": prompt,
            "status": "running"
        }
        
        try:
            result = self.client.call_agent(agent_id, prompt)
            execution["status"] = "completed"
            execution["result"] = result
        except Exception as e:
            execution["status"] = "failed"
            execution["error"] = str(e)
        
        self.execution_history.append(execution)
        return execution
    
    def execute_pipeline(self, agents_sequence: list, initial_prompt: str) -> dict:
        """
        Ejecuta un pipeline donde la salida de un agente es entrada del siguiente
        
        Args:
            agents_sequence: Lista de IDs de agentes en orden
            initial_prompt: Prompt inicial para el primer agente
            
        Returns:
            Dict con todos los resultados del pipeline
        """
        execution = {
            "timestamp": datetime.now().isoformat(),
            "type": "pipeline",
            "agents": agents_sequence,
            "initial_prompt": initial_prompt,
            "status": "running",
            "results": {}
        }
        
        try:
            results = self.client.call_workflow(agents_sequence, initial_prompt)
            execution["results"] = results
            execution["status"] = "completed"
        except Exception as e:
            execution["status"] = "failed"
            execution["error"] = str(e)
        
        self.execution_history.append(execution)
        return execution
    
    def execute_parallel_analysis(self, prompt: str, agents: list = None) -> dict:
        """
        Ejecuta el mismo prompt en múltiples agentes en paralelo
        
        Args:
            prompt: Prompt a enviar a todos los agentes
            agents: Lista de IDs de agentes (si None, usa todos)
            
        Returns:
            Dict con resultados de cada agente
        """
        if agents is None:
            agents = list(config.AGENTS.keys())
        
        execution = {
            "timestamp": datetime.now().isoformat(),
            "type": "parallel",
            "agents": agents,
            "prompt": prompt,
            "status": "running",
            "results": {}
        }
        
        try:
            for agent_id in agents:
                result = self.client.call_agent(agent_id, prompt)
                execution["results"][agent_id] = {
                    "agent": agent_id,
                    "response": result
                }
            execution["status"] = "completed"
        except Exception as e:
            execution["status"] = "failed"
            execution["error"] = str(e)
        
        self.execution_history.append(execution)
        return execution
    
    def get_history(self) -> list:
        """Retorna el historial de ejecuciones"""
        return self.execution_history
    
    def save_history(self, filename: str = "execution_history.json"):
        """Guarda el historial en un archivo JSON"""
        with open(f"{config.LOG_DIR}/{filename}", "w", encoding="utf-8") as f:
            json.dump(self.execution_history, f, indent=2, ensure_ascii=False)
