import json
import time
from typing import Optional, List

from openai import OpenAI, APIError, APIConnectionError, APITimeoutError

from config.config import config

class AIAgentClient:
    """Cliente para comunicarse con agentes de OpenAI"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = config.OPENAI_MODEL
    
    def call_agent(self, agent_id: str, prompt: str, context: dict = None, *, max_retries: int = 3, timeout: float = 30.0) -> str:
        """
        Llama a un agente con un prompt específico
        
        Args:
            agent_id: ID del agente (analyst, processor, coordinator)
            prompt: Prompt a enviar al agente
            context: Contexto adicional para el agente
            
        Returns:
            Respuesta del agente como string
        """
        agent_config = config.get_agent(agent_id)
        
        # Preparar el sistema de instrucciones
        system_prompt = agent_config["instructions"]
        if context:
            system_prompt += f"\n\nContexto adicional: {json.dumps(context, ensure_ascii=False)}"
        
        # Llamar a OpenAI
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt < max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000,
                    timeout=timeout
                )
                return response.choices[0].message.content
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
