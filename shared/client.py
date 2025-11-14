import json
import time
from typing import Optional, List, Dict, Any

from openai import OpenAI, APIError, APIConnectionError, APITimeoutError

from config.config import config

class AIAgentClient:
    """Cliente para comunicarse con agentes de OpenAI con colaboración entre agentes"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = config.OPENAI_MODEL
        # Historial de conversaciones entre agentes para cada request
        self.conversation_history: Dict[str, List[Dict[str, Any]]] = {}
    
    def call_agent(
        self,
        agent_id: str,
        prompt: str,
        context: dict = None,
        *,
        max_retries: int = 3,
        timeout: float = 30.0,
        request_id: str = None,
        enable_collaboration: bool = False,
    ) -> str:
        """
        Llama a un agente con un prompt específico
        
        Args:
            agent_id: ID del agente (adrian_datos, bruno_estrategia, andres_director, etc.)
            prompt: Prompt a enviar al agente
            context: Contexto adicional para el agente
            request_id: ID de la petición para tracking de conversaciones
            enable_collaboration: Si True, el agente puede llamar a otros agentes
            
        Returns:
            Respuesta del agente como string
        """
        agent_config = config.get_agent(agent_id)
        
        # Preparar el sistema de instrucciones
        system_prompt = agent_config["instructions"]
        if context:
            system_prompt += f"\n\nContexto adicional: {json.dumps(context, ensure_ascii=False)}"
        
        # Si hay historial de conversaciones, añadirlo
        if request_id and request_id in self.conversation_history:
            history = self.conversation_history[request_id]
            if history:
                system_prompt += "\n\nCONVERSACIONES PREVIAS DEL EQUIPO:\n"
                for msg in history:
                    system_prompt += f"\n{msg['from_agent']} → {msg['to_agent']}: {msg['message']}\nRespuesta: {msg['response']}\n"
        
        # Preparar tools si la colaboración está habilitada
        tools = None
        if enable_collaboration:
            tools = [{
                "type": "function",
                "function": {
                    "name": "consultar_colega",
                    "description": "Consulta a otro agente del equipo cuando necesites su expertise. Úsalo cuando necesites información especializada que otro agente puede proporcionar mejor.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "agent_name": {
                                "type": "string",
                                "enum": ["adrian_datos", "leo_partners", "bruno_estrategia", "francisco_success", 
                                        "lucia_canales", "diego_automatizacion", "camila_branding", "valeria_legal",
                                        "sofia_conversion", "elena_inventario", "carlos_logistica", "marco_fiscal", "lalo_ventas"],
                                "description": "Nombre del agente a consultar"
                            },
                            "pregunta": {
                                "type": "string",
                                "description": "La pregunta específica para el colega"
                            }
                        },
                        "required": ["agent_name", "pregunta"]
                    }
                }
            }]
        
        # Llamar a OpenAI
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt < max_retries:
            try:
                client = self.client.with_options(timeout=timeout)
                
                call_params = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "timeout": timeout
                }
                
                if tools:
                    call_params["tools"] = tools
                    call_params["tool_choice"] = "auto"
                
                response = client.chat.completions.create(**call_params)
                message = response.choices[0].message
                
                # Si el agente quiere llamar a un colega
                if message.tool_calls and enable_collaboration:
                    for tool_call in message.tool_calls:
                        if tool_call.function.name == "consultar_colega":
                            args = json.loads(tool_call.function.arguments)
                            colleague_id = args["agent_name"]
                            question = args["pregunta"]
                            
                            # Registrar la consulta
                            if request_id:
                                if request_id not in self.conversation_history:
                                    self.conversation_history[request_id] = []
                            
                            # Llamar al colega (SIN colaboración recursiva para evitar loops)
                            colleague_response = self.call_agent(
                                colleague_id,
                                question,
                                context=context,
                                request_id=request_id,
                                enable_collaboration=False  # Evitar recursión infinita
                            )
                            
                            # Registrar la conversación
                            if request_id:
                                self.conversation_history[request_id].append({
                                    "from_agent": agent_config["name"],
                                    "to_agent": config.get_agent(colleague_id)["name"],
                                    "message": question,
                                    "response": colleague_response,
                                    "timestamp": time.time()
                                })
                            
                            # Continuar la conversación con la respuesta del colega
                            follow_up = client.chat.completions.create(
                                model=self.model,
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": prompt},
                                    message,
                                    {
                                        "role": "tool",
                                        "tool_call_id": tool_call.id,
                                        "content": colleague_response
                                    }
                                ],
                                temperature=0.7,
                                max_tokens=2000,
                                timeout=timeout
                            )
                            
                            return follow_up.choices[0].message.content
                
                return message.content
                
            except (APIError, APIConnectionError, APITimeoutError) as exc:
                last_error = exc
                attempt += 1
                if attempt >= max_retries:
                    raise
                sleep_time = min(2 ** attempt, 8)
                time.sleep(sleep_time)
            except Exception as exc:
                last_error = exc
                raise

        if last_error:
            raise last_error

    def call_workflow(self, agents_sequence: List[str], initial_prompt: str = "", step_tasks: Optional[List[str]] = None) -> dict:
        """
        Ejecuta un workflow coordinado entre múltiples agentes
        
        Args:
            agents_sequence: Lista de IDs de agentes en orden
            initial_prompt: Prompt inicial
            
        Returns:
            Dict con resultados de cada agente
        """
        results = {}
        previous_output = initial_prompt or ""
        if not isinstance(previous_output, str):
            previous_output = json.dumps(previous_output, ensure_ascii=False)

        for index, agent_id in enumerate(agents_sequence):
            step_task = None
            if step_tasks and index < len(step_tasks):
                step_task = step_tasks[index]

            prompt_parts = []
            if step_task:
                prompt_parts.append(step_task)

            if previous_output:
                context_block = previous_output if isinstance(previous_output, str) else json.dumps(previous_output, ensure_ascii=False)
                if step_task:
                    prompt_parts.append(f"Contexto previo:\n{context_block}")
                else:
                    prompt_parts.append(context_block)

            prompt = "\n\n".join(part for part in prompt_parts if part).strip()
            # fallback al flujo tradicional si no tenemos prompt explícito
            if not prompt:
                prompt = previous_output

            response = self.call_agent(agent_id, prompt, context=results)
            results[agent_id] = {
                "agent": agent_id,
                "response": response,
                "order": len(results) + 1,
                "prompt_sent": prompt,
                "task": step_task,
                "previous_output": previous_output
            }
            previous_output = response
        
        return results
