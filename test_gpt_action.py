"""
Script para probar el endpoint /gpt/smart/request como lo haría ChatGPT
"""
import requests
import json

url = "https://agentes-ia-jamones.onrender.com/gpt/smart/request"

payload = {
    "request": "Necesito análisis completo para expandir a Portugal: viabilidad de mercado, requisitos legales, logística necesaria, estrategia de entrada y análisis fiscal",
    "context": {}
}

print("🔍 Probando endpoint como lo hace ChatGPT...")
print(f"📍 URL: {url}")
print(f"📦 Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
print("\n⏳ Enviando petición...\n")

try:
    response = requests.post(url, json=payload, timeout=120)
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"📄 Response:\n")
    
    if response.status_code == 200:
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Verificar que tenga los campos esperados
        print("\n🔎 Verificando estructura:")
        print(f"  - peticion_original: {'✅' if 'peticion_original' in result else '❌'}")
        print(f"  - tipo_trabajo: {'✅' if 'tipo_trabajo' in result else '❌'}")
        print(f"  - equipo_participante: {'✅' if 'equipo_participante' in result else '❌'}")
        print(f"  - conversaciones_entre_agentes: {'✅' if 'conversaciones_entre_agentes' in result else '❌'}")
        print(f"  - respuesta_final: {'✅' if 'respuesta_final' in result else '❌'}")
        
        if 'conversaciones_entre_agentes' in result:
            convos = result['conversaciones_entre_agentes']
            print(f"\n💬 Conversaciones detectadas: {len(convos)}")
            for i, convo in enumerate(convos[:3], 1):
                print(f"  {i}. {convo.get('from_agent', '?')} → {convo.get('to_agent', '?')}")
    else:
        print(f"❌ Error: {response.text}")
        
except requests.exceptions.Timeout:
    print("❌ TIMEOUT: El servidor tardó más de 120 segundos")
except requests.exceptions.ConnectionError:
    print("❌ CONNECTION ERROR: No se pudo conectar al servidor")
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {e}")
