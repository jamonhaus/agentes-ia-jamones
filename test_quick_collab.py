"""
Test rápido: Verificar que la colaboración funciona
"""
import os
from shared.client import AIAgentClient

api_key = os.getenv("OPENAI_API_KEY")
client = AIAgentClient(api_key)

request_id = "test_quick"

# Pregunta simple que debería hacer que Adrián llame a Bruno
prompt = "Analiza las ventas de Madrid y dame proyecciones estratégicas"

print("🤖 Llamando a Adrián con colaboración activada...")
response = client.call_agent(
    "adrian_datos",
    prompt,
    request_id=request_id,
    enable_collaboration=True
)

print("\n📊 RESPUESTA:")
print(response[:300] + "...\n")

conversations = client.conversation_history.get(request_id, [])
print(f"💬 CONVERSACIONES: {len(conversations)}")

for i, conv in enumerate(conversations, 1):
    print(f"\n{i}. {conv['from_agent']} ➜ {conv['to_agent']}")
    print(f"   Q: {conv['message'][:80]}")
    print(f"   A: {conv['response'][:80]}")
