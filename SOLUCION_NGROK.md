# 🔧 SOLUCIÓN: Usar ngrok para exponer la API localmente

## El problema:
ChatGPT no puede acceder a `agentes-ia-jamones.onrender.com` (error "Unknown domain")

## La solución:
Ejecutar la API localmente y exponerla con ngrok

---

## PASOS:

### 1️⃣ Instala ngrok (si no lo tienes)
https://ngrok.com/download

### 2️⃣ Ejecuta la API localmente
```powershell
cd C:\PROYECTO1
python main.py
```

### 3️⃣ En otra terminal, ejecuta ngrok
```powershell
ngrok http 8000
```

### 4️⃣ Copia la URL que te da ngrok
Ejemplo: `https://abc123.ngrok.io`

### 5️⃣ Úsala en el schema de Actions
En lugar de:
```
https://agentes-ia-jamones.onrender.com
```

Usa:
```
https://abc123.ngrok.io
```

### 6️⃣ Guarda y prueba

---

## ⚠️ LIMITACIONES:
- ngrok free: la URL cambia cada vez que reinicias
- Solo funciona mientras tengas la terminal abierta

---

## 💡 MEJOR SOLUCIÓN PERMANENTE:

### Opción A: Dominio personalizado en Render
1. Compra un dominio (ej: `api-jamonhaus.com`)
2. Configúralo en Render
3. Usa ese dominio en Actions

### Opción B: Vercel/Railway (alternativas a Render)
A veces tienen mejor conectividad con ChatGPT

---

## 🎯 PARA AHORA (PRUEBA RÁPIDA):

1. Descarga ngrok: https://ngrok.com/download
2. Ejecuta localmente: `python main.py`
3. Ejecuta ngrok: `ngrok http 8000`
4. Copia la URL de ngrok al schema de Actions
5. ¡Prueba!
