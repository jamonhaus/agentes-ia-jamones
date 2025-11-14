"""
Script de prueba para la coordinación automática
Prueba local antes de verificar en Render
"""

import json
from agents.orchestrator import AgentOrchestrator

def test_auto_coordination():
    """Prueba la coordinación automática del Director"""
    
    orchestrator = AgentOrchestrator()
    
    # PRUEBA 1: Estudio de mercado
    print("=" * 80)
    print("PRUEBA 1: Estudio de mercado para Madrid")
    print("=" * 80)
    
    request = "Necesito un estudio de mercado completo para expandir JamonHaus a Madrid"
    context = {
        "presupuesto": "50,000 EUR",
        "deadline": "Q1 2024",
        "productos": ["jamón ibérico", "embutidos premium"]
    }
    
    result = orchestrator.auto_coordinate(request, context)
    
    print(f"\n✅ Status: {result['status']}")
    print(f"\n📋 Tipo de petición: {result.get('director_plan', {}).get('tipo_peticion')}")
    print(f"\n👥 Agentes participantes:")
    for agent_info in result.get('director_plan', {}).get('agentes_requeridos', []):
        print(f"   - {agent_info.get('agent_id')}: {agent_info.get('tarea')}")
    
    print(f"\n🔄 Modo de ejecución: {result.get('execution_mode')}")
    
    print(f"\n📊 RESPUESTA FINAL DEL DIRECTOR:")
    print("-" * 80)
    print(result.get('final_response'))
    print("-" * 80)
    
    # PRUEBA 2: Análisis de ventas
    print("\n\n" + "=" * 80)
    print("PRUEBA 2: Análisis de ventas del último trimestre")
    print("=" * 80)
    
    request2 = "Analiza las ventas del último trimestre y propón estrategias de mejora"
    
    result2 = orchestrator.auto_coordinate(request2)
    
    print(f"\n✅ Status: {result2['status']}")
    print(f"\n📋 Tipo de petición: {result2.get('director_plan', {}).get('tipo_peticion')}")
    print(f"\n👥 Agentes participantes:")
    for agent_info in result2.get('director_plan', {}).get('agentes_requeridos', []):
        print(f"   - {agent_info.get('agent_id')}: {agent_info.get('tarea')}")
    
    print(f"\n📊 RESPUESTA FINAL DEL DIRECTOR:")
    print("-" * 80)
    print(result2.get('final_response'))
    print("-" * 80)

if __name__ == "__main__":
    # Verificar que tenemos API key
    from config.config import config
    
    if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "sk-your-api-key-here":
        print("❌ ERROR: Necesitas configurar OPENAI_API_KEY en .env")
        print("No se pueden ejecutar las pruebas sin la API key de OpenAI")
    else:
        print("✅ OPENAI_API_KEY configurada")
        print("\nEjecutando pruebas de coordinación automática...\n")
        test_auto_coordination()
