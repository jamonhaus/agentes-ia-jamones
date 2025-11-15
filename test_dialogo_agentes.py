from agents.orchestrator import AgentOrchestrator

if __name__ == "__main__":
    orq = AgentOrchestrator()
    resultado = orq.auto_coordinate("Analiza el mercado de jamones en Madrid", context={})

    print("\n=== ORDEN Y DIÁLOGO DE LOS AGENTES ===\n")
    for paso, mensaje in enumerate(resultado.get("dialogo_agentes", []), 1):
        print(f"Paso {paso}: {mensaje}\n")

    print("\n=== RESPUESTA FINAL ===\n")
    print(resultado.get("final_response") or resultado.get("respuesta_final"))
