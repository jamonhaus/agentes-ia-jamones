"""
Script de prueba para el sistema de coordinación automática
"""

import sys
import asyncio
from agents.orchestrator import AgentOrchestrator

async def test_auto_coordinate():
    """Prueba el método auto_coordinate directamente"""
    
    orchestrator = AgentOrchestrator()
    
    print("=" * 80)
    print("PRUEBA: COORDINACIÓN AUTOMÁTICA")
    print("=" * 80)
    print("\nPETICIÓN: Necesito un análisis de mercado para Barcelona\n")
    
    try:
        result = orchestrator.auto_coordinate(
            user_request="Necesito un análisis rápido de viabilidad de mercado para abrir tienda en Barcelona",
            context={}
        )
        
        print("\n📊 RESULTADO DE LA COORDINACIÓN\n")
        print(f"Estado: {result['status']}")
        print(f"Timestamp: {result['timestamp']}")
        
        if result['status'] == 'completed':
            print("\n🎯 PLAN DEL DIRECTOR:")
            director_plan = result.get('director_plan', {})
            print(f"  Tipo de petición: {director_plan.get('tipo_peticion')}")
            print(f"  Estrategia: {director_plan.get('estrategia')}")
            print(f"\n  Agentes seleccionados:")
            for agent in director_plan.get('agentes_necesarios', []):
                print(f"    - {agent['agente']}: {agent['tarea']}")
            
            print(f"\n  Modo de ejecución: {result.get('execution_mode')}")
            
            print("\n👥 RESULTADOS DE LOS AGENTES:")
            agent_results = result.get('agent_results', {})
            for agent_id, agent_data in agent_results.items():
                print(f"\n  🔹 {agent_data.get('agent')}:")
                print(f"     Tarea: {agent_data.get('tarea_asignada')}")
                response = agent_data.get('respuesta', '')
                # Mostrar solo primeros 200 caracteres
                print(f"     Respuesta: {response[:200]}...")
            
            print("\n🎯 RESPUESTA FINAL CONSOLIDADA:")
            final_response = result.get('final_response', '')
            print(f"\n{final_response[:500]}...\n")
            
            print("=" * 80)
            print("✅ PRUEBA EXITOSA - El sistema funciona correctamente")
            print("=" * 80)
            
        else:
            print(f"\n❌ ERROR: {result.get('error')}")
            
    except Exception as e:
        print(f"\n❌ EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_auto_coordinate())
