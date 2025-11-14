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
