"""
Test REAL de colaboración múltiple entre agentes
"""
import os
import json
from agents.orchestrator import AgentOrchestrator

def test_real_collaboration():
    """
    Prueba REAL: Petición compleja que DEBE requerir colaboración
    """
    print("=" * 80)
    print("🔥 TEST REAL DE COLABORACIÓN MÚLTIPLE")
    print("=" * 80)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY no configurada")
        return
    
    orchestrator = AgentOrchestrator()
    
    # Petición compleja que DEBERÍA generar colaboración
    request = """
Quiero lanzar una campaña de Black Friday para jamones ibéricos premium en Madrid y Barcelona.
Necesito:
1. Análisis de inventario actual y stock necesario
2. Estrategia de marketing y contenido para redes sociales
3. Plan de logística y distribución express
4. Análisis de conversión y optimización del funnel
5. Estrategia de fidelización post-compra

Objetivo: 10,000 ventas en 72 horas
"""
    
    print("\n📝 PETICIÓN COMPLEJA:")
    print(request)
    print("\n" + "=" * 80)
    print("⏳ EJECUTANDO... (esto puede tardar 30-60 segundos)\n")
    
    try:
        result = orchestrator.auto_coordinate(request)
        
        # Mostrar plan del director
        print("=" * 80)
        print("🎯 PLAN DEL DIRECTOR (ANDRÉS)")
        print("=" * 80)
        if "director_plan" in result:
            plan = result["director_plan"]
            print(f"Tipo: {plan.get('tipo_peticion')}")
            print(f"Estrategia: {plan.get('estrategia')}")
            print(f"\n👥 Agentes asignados:")
            for ag in plan.get("agentes_requeridos", []):
                print(f"   ✓ {ag['agent_id']}: {ag['tarea'][:60]}...")
        
        # Mostrar conversaciones (LO IMPORTANTE)
        conversations = result.get("agent_conversations", [])
        print(f"\n{'=' * 80}")
        print(f"💬 CONVERSACIONES ENTRE AGENTES: {len(conversations)}")
        print("=" * 80)
        
        if conversations:
            for i, conv in enumerate(conversations, 1):
                print(f"\n🔸 Conversación #{i}")
                print(f"   De: {conv['from_agent']}")
                print(f"   A:  {conv['to_agent']}")
                print(f"   ❓ Pregunta:")
                print(f"      {conv['message'][:150]}...")
                print(f"   ✅ Respuesta ({len(conv['response'])} caracteres):")
                print(f"      {conv['response'][:150]}...")
        else:
            print("\n⚠️  NO SE REGISTRARON CONVERSACIONES")
            print("   Posibles razones:")
            print("   - Los agentes trabajaron independientemente")
            print("   - No consideraron necesario consultar a colegas")
            print("   - El contexto no requería colaboración explícita")
        
        # Resultados de cada agente
        print(f"\n{'=' * 80}")
        print("📊 RESULTADOS POR AGENTE")
        print("=" * 80)
        agent_results = result.get("agent_results", {})
        for agent_id, data in agent_results.items():
            print(f"\n{data['agent']}:")
            print(f"  Tarea: {data['tarea_asignada'][:80]}...")
            print(f"  Respuesta: {len(data['respuesta'])} caracteres")
        
        # Respuesta final
        print(f"\n{'=' * 80}")
        print("📄 RESPUESTA FINAL CONSOLIDADA")
        print("=" * 80)
        final = result.get("final_response", "")
        print(final[:800] if len(final) > 800 else final)
        
        print(f"\n{'=' * 80}")
        print("✅ TEST COMPLETADO")
        print("=" * 80)
        
        return {
            "success": True,
            "agents_used": len(agent_results),
            "conversations": len(conversations),
            "has_collaboration": len(conversations) > 0
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    result = test_real_collaboration()
    print(f"\n{'=' * 80}")
    print("📈 RESUMEN FINAL:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 80)
