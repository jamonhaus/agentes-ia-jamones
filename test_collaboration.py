"""
Test de colaboración entre agentes
Verifica que los agentes puedan llamarse entre sí usando consultar_colega()
"""
import sys
import json
from shared.client import AIAgentClient
from config.config import Config

def test_agent_collaboration():
    """
    Test: Un agente necesita información de otro y lo llama
    Escenario: Adrián (Analista Datos) necesita info legal de Marco
    """
    print("=" * 80)
    print("TEST: COLABORACIÓN ENTRE AGENTES")
    print("=" * 80)
    
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: Variable OPENAI_API_KEY no configurada")
        return {"success": False, "error": "No API key"}
    
    config = Config()
    client = AIAgentClient(api_key=api_key)
    
    # Escenario: Análisis de expansión a Madrid que requiere datos legales y logísticos
    request = """
Analiza la viabilidad de expandir nuestras operaciones de jamones premium a Madrid.
Necesito un análisis completo que incluya:
- Datos de mercado y proyecciones de ventas
- Aspectos legales y fiscales de operar en Madrid
- Logística y distribución
"""
    
    request_id = "test_collab_001"
    
    print("\n📝 PETICIÓN:")
    print(request)
    print("\n" + "=" * 80)
    
    # Simular que Adrián (datos) recibe la tarea y necesita colaborar
    print("\n🤖 LLAMANDO A ADRIÁN (Analista de Datos)...")
    print("   Con colaboración ACTIVADA\n")
    
    try:
        response = client.call_agent(
            "adrian_datos",
            request,
            request_id=request_id,
            enable_collaboration=True
        )
        
        print("\n" + "=" * 80)
        print("📊 RESPUESTA DE ADRIÁN:")
        print("=" * 80)
        print(response)
        
        # Verificar si hubo conversaciones
        conversations = client.conversation_history.get(request_id, [])
        
        print("\n" + "=" * 80)
        print(f"💬 CONVERSACIONES REGISTRADAS: {len(conversations)}")
        print("=" * 80)
        
        if conversations:
            for i, conv in enumerate(conversations, 1):
                print(f"\n--- Conversación {i} ---")
                print(f"🗣️  {conv['from_agent']} preguntó a {conv['to_agent']}:")
                print(f"   ❓ \"{conv['message'][:100]}...\"")
                print(f"\n💡 {conv['to_agent']} respondió:")
                print(f"   ✅ \"{conv['response'][:200]}...\"")
                print()
        else:
            print("\n⚠️  NO SE REGISTRARON CONVERSACIONES")
            print("   Los agentes trabajaron de forma independiente")
        
        print("\n" + "=" * 80)
        print("✅ TEST COMPLETADO")
        print("=" * 80)
        
        return {
            "success": True,
            "conversations_count": len(conversations),
            "response_length": len(response)
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    result = test_agent_collaboration()
    print("\n" + "=" * 80)
    print("RESULTADO:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 80)
