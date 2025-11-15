from main import app
import json

schema = app.openapi()
paths = schema['paths']

print("\n🔍 VERIFICACIÓN DE DESCRIPCIONES:\n")
print("=" * 80)

for path, methods in paths.items():
    if path.startswith("/gpt/"):
        for method, details in methods.items():
            desc = details.get("description", "")
            length = len(desc)
            status = "✅" if length <= 300 else "❌ EXCEDE LÍMITE"
            print(f"\n{method.upper()} {path}")
            print(f"  Longitud: {length} chars {status}")
            if length > 300:
                print(f"  DESCRIPCIÓN: {desc[:100]}...")

print("\n" + "=" * 80)

print("\n=== SCHEMA /gpt/smart/request ===")
try:
    req_schema = schema['paths']['/gpt/smart/request']['post']['requestBody']['content']['application/json']['schema']
    print(json.dumps(req_schema, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error mostrando schema /gpt/smart/request: {e}")

print("\n=== SCHEMA /gpt/smart/request/sync ===")
try:
    req_schema_sync = schema['paths']['/gpt/smart/request/sync']['post']['requestBody']['content']['application/json']['schema']
    print(json.dumps(req_schema_sync, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error mostrando schema /gpt/smart/request/sync: {e}")
