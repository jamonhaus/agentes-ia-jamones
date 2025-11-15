"""
Test simple para VER la colaboración entre agentes en vivo
"""
from agents.orchestrator import AgentOrchestrator
import json

print("🚀 Iniciando test de colaboración entre agentes\n")
print("=" * 70)

orchestrator = AgentOrchestrator()

# Petición compleja que requiere múltiples agentes
peticion = """
Necesito análisis completo para expandir a Portugal:
- Viabilidad de mercado
- Requisitos legales
- Logística necesaria
- Estrategia de entrada
- Análisis fiscal
"""

print(f"\n📋 PETICIÓN:\n{peticion}\n")
print("=" * 70)
print("\n⏳ Procesando... (esto tardará 1-3 minutos)\n")

# Ejecutar coordinación automática CON colaboración
resultado = orchestrator.auto_coordinate(peticion, {})

print("\n" + "=" * 70)
print("✅ COORDINACIÓN COMPLETADA")
print("=" * 70)

# Mostrar equipo participante
if "agent_results" in resultado:
    print(f"\n👥 EQUIPO QUE TRABAJÓ ({len(resultado['agent_results'])} agentes):")
    for agent_id, result in resultado["agent_results"].items():
        print(f"   - {result.get('agent', agent_id)}: {result.get('tarea_asignada', 'N/A')[:60]}...")

# ESTO ES LO IMPORTANTE: Mostrar conversaciones entre agentes
print(f"\n💬 CONVERSACIONES ENTRE AGENTES:")
print("=" * 70)

conversaciones = resultado.get("agent_conversations", [])
if conversaciones:
    for i, conv in enumerate(conversaciones, 1):
        print(f"\n{i}. {conv.get('from_agent', '?')} consultó a {conv.get('to_agent', '?')}:")
        print(f"   Pregunta: \"{conv.get('message', '')[:100]}...\"")
        print(f"   Respuesta: \"{conv.get('response', '')[:150]}...\"")
else:
    print("   ⚠️  No hubo conversaciones entre agentes (puede que no hayan colaborado)")

# Mostrar respuesta final resumida
print(f"\n📊 RESPUESTA FINAL:")
print("=" * 70)
respuesta = resultado.get("final_response", "No disponible")
print(respuesta[:500] + "..." if len(respuesta) > 500 else respuesta)

print("\n" + "=" * 70)
print("🎉 TEST COMPLETADO")
print("=" * 70)

# Guardar resultado completo en archivo para revisión
with open("resultado_colaboracion.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("\n💾 Resultado completo guardado en: resultado_colaboracion.json")
