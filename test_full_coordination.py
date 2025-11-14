"""
Test completo de coordinación con colaboración entre agentes
"""
import sys
import json
import os
from agents.orchestrator import AgentOrchestrator

def test_full_coordination_with_collaboration():
    """
    Test del flujo completo:
    1. Andrés analiza y decide equipo
    2. Agentes colaboran entre sí según necesiten
    3. Andrés consolida resultado
    4. Respuesta muestra todas las conversaciones
    """
    print("=" * 80)
    print("TEST: COORDINACIÓN COMPLETA CON COLABORACIÓN")
    print("=" * 80)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY no configurada")
        return {"success": False, "error": "No API key"}
    
    orchestrator = AgentOrchestrator()
    
    # Petición compleja que debería requerir colaboración
    request = """
Necesito un plan completo para lanzar una nueva línea de jamones orgánicos 
en Barcelona y Madrid. El análisis debe incluir:
- Estudio de mercado y proyección de ventas
- Estrategia de marketing y branding
- Aspectos legales y fiscales
- Logística y distribución
- Plan de fidelización de clientes
"""
    
    print("\n📝 PETICIÓN COMPLETA:")
    print(request)
    print("\n" + "=" * 80)
    print("🎬 INICIANDO COORDINACIÓN AUTOMÁTICA...\n")
    
    try:
        result = orchestrator.auto_coordinate(request)
        
        print("\n" + "=" * 80)
        print("📋 RESULTADO DE LA COORDINACIÓN")
        print("=" * 80)
        
        # Mostrar plan del director
        if "director_plan" in result:
            plan = result["director_plan"]
            print(f"\n🎯 TIPO DE PETICIÓN: {plan.get('tipo_peticion')}")
            print(f"📊 ESTRATEGIA: {plan.get('estrategia')}")
            print(f"\n👥 EQUIPO ASIGNADO:")
            for ag in plan.get("agentes_requeridos", []):
                print(f"   - {ag['agent_id']}: {ag['tarea'][:60]}...")
        
        # Mostrar conversaciones entre agentes
        conversations = result.get("agent_conversations", [])
        print(f"\n💬 CONVERSACIONES ENTRE AGENTES: {len(conversations)}")
        print("=" * 80)
        
        if conversations:
            for i, conv in enumerate(conversations, 1):
                print(f"\n🗣️  Conversación #{i}")
                print(f"   {conv['from_agent']}")
                print(f"   ➜ consultó a: {conv['to_agent']}")
                print(f"   ❓ Pregunta: \"{conv['message'][:80]}...\"")
                print(f"   ✅ Respuesta: \"{conv['response'][:120]}...\"")
        else:
            print("\n⚠️  No se registraron conversaciones inter-agente")
            print("   Los agentes trabajaron de forma independiente")
        
        # Respuesta final
        print("\n" + "=" * 80)
        print("📄 RESPUESTA FINAL CONSOLIDADA")
        print("=" * 80)
        final = result.get("final_response", "")
        print(final[:500] + "..." if len(final) > 500 else final)
        
        print("\n" + "=" * 80)
        print("✅ TEST COMPLETADO")
        print("=" * 80)
        
        return {
            "success": True,
            "status": result.get("status"),
            "agents_count": len(result.get("agent_results", {})),
            "conversations_count": len(conversations),
            "execution_mode": result.get("execution_mode")
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    result = test_full_coordination_with_collaboration()
    print("\n" + "=" * 80)
    print("📊 RESUMEN:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 80)
