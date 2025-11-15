from agents.orchestrator import AgentOrchestrator

orq = AgentOrchestrator()
resultado = orq.auto_coordinate("Quiero un análisis de ventas del último trimestre para JamonHaus")
print(resultado)