from agents.orchestrator import AgentOrchestrator

if __name__ == "__main__":
    orq = AgentOrchestrator()
    resultado = orq.auto_coordinate("Necesito un plan detallado para lanzar una nueva línea de jamón ecológico en Sevilla, incluyendo análisis de mercado, estrategia de marketing y logística.", context={})

    print("\n=== ORDEN Y DIÁLOGO DE LOS AGENTES ===\n")
    for paso, mensaje in enumerate(resultado.get("dialogo_agentes", []), 1):
        print(f"Paso {paso}: {mensaje}\n")

    print("\n=== RESPUESTA FINAL ===\n")
    print(resultado.get("final_response") or resultado.get("respuesta_final"))
