"""Script de prueba para verificar que los agentes funcionan correctamente"""

import sys
from agents.orchestrator import AgentOrchestrator
from config.config import config

def test_simple_task():
    """Prueba: ejecutar una tarea simple"""
    print("\n" + "="*60)
    print("TEST 1: Tarea Simple con un Agente")
    print("="*60)
    
    orchestrator = AgentOrchestrator()
    
    try:
        result = orchestrator.execute_simple_task(
            agent_id="analyst",
            prompt="¿Cuáles son las 3 principales ventajas de usar IA en análisis de datos?"
        )
        
        print(f"\n✅ Estado: {result['status']}")
        print(f"📍 Agente: {result['agent_id']}")
        print(f"\n📝 Respuesta:\n{result.get('result', 'N/A')}\n")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_pipeline():
    """Prueba: ejecutar un pipeline"""
    print("\n" + "="*60)
    print("TEST 2: Pipeline (3 agentes secuencial)")
    print("="*60)
    
    orchestrator = AgentOrchestrator()
    
    try:
        result = orchestrator.execute_pipeline(
            agents_sequence=["analyst", "processor", "coordinator"],
            initial_prompt="Dame 3 ideas innovadoras para mejorar la educación online"
        )
        
        print(f"\n✅ Estado: {result['status']}")
        print(f"🔄 Agentes en pipeline: {' → '.join(result['agents'])}")
        
        for agent_id, agent_result in result['results'].items():
            print(f"\n📊 Resultado de {agent_id}:")
            print(f"   {agent_result['response'][:200]}...")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_parallel():
    """Prueba: ejecutar análisis en paralelo"""
    print("\n" + "="*60)
    print("TEST 3: Análisis Paralelo (3 agentes simultáneamente)")
    print("="*60)
    
    orchestrator = AgentOrchestrator()
    
    try:
        result = orchestrator.execute_parallel_analysis(
            prompt="¿Cuál es la importancia de los datos en la IA moderna?"
        )
        
        print(f"\n✅ Estado: {result['status']}")
        print(f"👥 Agentes participantes: {', '.join(result['agents'])}")
        
        for agent_id, agent_result in result['results'].items():
            print(f"\n💬 Perspectiva de {agent_id}:")
            print(f"   {agent_result['response'][:200]}...")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("\n" + "🤖 "*20)
    print("PRUEBAS DEL ORQUESTADOR DE AGENTES IA")
    print("🤖 "*20)
    
    # Validar configuración
    try:
        config.validate()
        print("\n✅ Configuración válida")
        print(f"   API Key: {'Configurada' if config.OPENAI_API_KEY else 'NO CONFIGURADA'}")
        print(f"   Modelo: {config.OPENAI_MODEL}")
        print(f"   Agentes: {', '.join(config.AGENTS.keys())}")
    except ValueError as e:
        print(f"\n❌ Error de configuración: {e}")
        sys.exit(1)
    
    # Ejecutar pruebas
    results = {
        "Simple": test_simple_task(),
        "Pipeline": test_pipeline(),
        "Paralelo": test_parallel()
    }
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    for test_name, passed in results.items():
        status = "✅ PASADA" if passed else "❌ FALLIDA"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for v in results.values() if v)
    print(f"\nTotal: {passed_count}/{len(results)} pruebas exitosas\n")
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
