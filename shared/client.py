import json
from openai import OpenAI
from config.config import config

class AIAgentClient:
    """Cliente para comunicarse con agentes de OpenAI"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = config.OPENAI_MODEL
    
    def call_agent(self, agent_id: str, prompt: str, context: dict = None) -> str:
        """
        Llama a un agente con un prompt específico
        
        Args:
            agent_id: ID del agente (analyst, processor, coordinator)
            prompt: Prompt a enviar al agente
            context: Contexto adicional para el agente
            
        Returns:
            Respuesta del agente como string
        """
        agent_config = config.AGENTS.get(agent_id)
        if not agent_config:
            raise ValueError(f"Agente {agent_id} no encontrado")
        
        # Preparar el sistema de instrucciones
        system_prompt = agent_config["instructions"]
        if context:
            system_prompt += f"\n\nContexto adicional: {json.dumps(context, ensure_ascii=False)}"
        
        # Llamar a OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def call_workflow(self, agents_sequence: list, initial_prompt: str) -> dict:
        """
        Ejecuta un workflow coordinado entre múltiples agentes
        
        Args:
            agents_sequence: Lista de IDs de agentes en orden
            initial_prompt: Prompt inicial
            
        Returns:
            Dict con resultados de cada agente
        """
        results = {}
        current_input = initial_prompt
        
        for agent_id in agents_sequence:
            response = self.call_agent(agent_id, current_input, context=results)
            results[agent_id] = {
                "agent": agent_id,
                "response": response,
                "order": len(results) + 1
            }
            # La salida de un agente es entrada del siguiente
            current_input = response
        
        return results
