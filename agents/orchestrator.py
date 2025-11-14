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
    
    def execute_pipeline(self, agents_sequence: list, initial_prompt: str, step_tasks: list | None = None) -> dict:
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
            "results": {},
            "step_tasks": step_tasks or []
        }
        
        try:
            results = self.client.call_workflow(agents_sequence, initial_prompt, step_tasks)
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
                config.get_agent(agent_id)  # valida existencia o lanza ValueError
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
    
    def auto_coordinate(self, user_request: str, context: dict = None) -> dict:
        """
        COORDINACIÓN AUTOMÁTICA - El Director analiza y ejecuta
        
        1. Andrés (Director) analiza la petición
        2. Decide qué agentes necesita
        3. Reparte el trabajo entre ellos
        4. Ejecuta en paralelo o secuencia según corresponda
        5. Consolida resultados y entrega respuesta final
        
        Args:
            user_request: Petición del usuario
            context: Contexto adicional
            
        Returns:
            Dict con todo el proceso y resultado final
        """
        execution = {
            "timestamp": datetime.now().isoformat(),
            "type": "auto_coordination",
            "user_request": user_request,
            "context": context or {},
            "status": "running"
        }
        
        try:
            # PASO 1: Director analiza y planifica
            director_analysis_prompt = f"""
Eres Andrés, Director de Ventas Online. Has recibido esta petición del usuario:

"{user_request}"

Contexto adicional: {json.dumps(context or {}, ensure_ascii=False)}

EQUIPO DISPONIBLE:
- adrian_datos: Analista de datos y BI
- leo_partners: Alianzas y negocio internacional
- bruno_estrategia: Estrategia y marketing
- francisco_success: Customer success y fidelización
- lucia_canales: Atención multicanal
- diego_automatizacion: Automatización de marketing
- camila_branding: Branding y contenido
- valeria_legal: Legal y compliance
- sofia_conversion: Optimización de conversión
- elena_inventario: Gestión de inventario
- carlos_logistica: Logística y SCM
- marco_fiscal: Fiscal e internacional
- lalo_ventas: Ventas y sourcing

INSTRUCCIONES:
1. Analiza qué tipo de petición es (estudio de mercado, análisis de ventas, expansión, etc.)
2. Decide qué agentes necesitas (mínimo 2, máximo 5)
3. Define la tarea específica para cada agente
4. Responde SOLO en formato JSON así:

{{
  "tipo_peticion": "descripción breve",
  "agentes_requeridos": [
    {{"agent_id": "adrian_datos", "tarea": "descripción específica de qué debe hacer"}},
    {{"agent_id": "bruno_estrategia", "tarea": "descripción específica de qué debe hacer"}}
  ],
  "estrategia": "paralelo" o "secuencial"
}}
"""
            
            director_plan = self.client.call_agent("andres_director", director_analysis_prompt)
            execution["director_plan_raw"] = director_plan
            
            # Parsear el plan del director
            try:
                # Extraer JSON del texto (puede venir con markdown o explicaciones)
                plan_text = director_plan
                if "```json" in plan_text:
                    plan_text = plan_text.split("```json")[1].split("```")[0]
                elif "```" in plan_text:
                    plan_text = plan_text.split("```")[1].split("```")[0]
                
                plan = json.loads(plan_text.strip())
                execution["director_plan"] = plan
            except json.JSONDecodeError:
                # Si no puede parsear, usar análisis manual simple
                plan = {
                    "tipo_peticion": "análisis general",
                    "agentes_requeridos": [
                        {"agent_id": "adrian_datos", "tarea": user_request},
                        {"agent_id": "bruno_estrategia", "tarea": user_request}
                    ],
                    "estrategia": "paralelo"
                }
                execution["director_plan"] = plan
                execution["plan_parse_warning"] = "Usado plan por defecto"
            
            # PASO 2: Ejecutar según estrategia
            agent_results = {}
            
            if plan.get("estrategia") == "secuencial":
                # Ejecución secuencial (pipeline)
                agent_sequence = [ag["agent_id"] for ag in plan["agentes_requeridos"]]
                step_tasks = [ag["tarea"] for ag in plan["agentes_requeridos"]]
                
                pipeline_exec = self.execute_pipeline(
                    agent_sequence,
                    f"Petición original: {user_request}\n\nContexto: {json.dumps(context or {}, ensure_ascii=False)}",
                    step_tasks
                )
                agent_results = pipeline_exec.get("results", {})
                execution["execution_mode"] = "secuencial"
                
            else:
                # Ejecución en paralelo (por defecto)
                for agent_task in plan["agentes_requeridos"]:
                    agent_id = agent_task["agent_id"]
                    task = agent_task["tarea"]
                    
                    # Validar que el agente existe
                    config.get_agent(agent_id)
                    
                    # Ejecutar tarea
                    full_task = f"{task}\n\nContexto de petición original: {user_request}"
                    result = self.client.call_agent(agent_id, full_task)
                    
                    agent_results[agent_id] = {
                        "agent": config.get_agent(agent_id)["name"],
                        "tarea_asignada": task,
                        "respuesta": result
                    }
                
                execution["execution_mode"] = "paralelo"
            
            execution["agent_results"] = agent_results
            
            # PASO 3: Director consolida resultados
            consolidation_prompt = f"""
Eres Andrés, Director de Ventas Online. Has coordinado un equipo para atender esta petición:

PETICIÓN ORIGINAL: {user_request}

PLAN EJECUTADO:
{json.dumps(plan, ensure_ascii=False, indent=2)}

RESULTADOS DE LOS AGENTES:
{json.dumps(agent_results, ensure_ascii=False, indent=2)}

INSTRUCCIONES:
Analiza todos los aportes de tu equipo y elabora una RESPUESTA FINAL CONSOLIDADA que:
1. Integre los análisis de todos los especialistas
2. Sea coherente y organizada
3. Responda completamente a la petición original
4. Incluya recomendaciones concretas si aplica

Tu respuesta será lo que se entregue al usuario final.
"""
            
            final_response = self.client.call_agent("andres_director", consolidation_prompt)
            execution["final_response"] = final_response
            execution["status"] = "completed"
            
            # PASO 4: Preparar resumen ejecutivo
            execution["summary"] = {
                "peticion": user_request,
                "tipo": plan.get("tipo_peticion"),
                "agentes_participantes": [ag["agent_id"] for ag in plan["agentes_requeridos"]],
                "modo_ejecucion": execution["execution_mode"],
                "respuesta_final": final_response
            }
            
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
