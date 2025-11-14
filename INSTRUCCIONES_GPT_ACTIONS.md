# 🎯 INSTRUCCIONES PARA CONFIGURAR GPT ACTIONS

## 📋 PASOS PARA CADA GPT:

### 1️⃣ Abre tu GPT en ChatGPT
Ejemplo: https://chatgpt.com/g/g-6914c3ef8e9881918ddbe1967d83dfba-adrian-weis-analista-de-datos-de-negocio-global

### 2️⃣ Ve a "Configure" → "Actions"

### 3️⃣ Copia y pega el schema
Abre el archivo `GPT_ACTIONS_SCHEMA.json` y copia TODO el contenido

### 4️⃣ Pégalo en el campo "Schema"

### 5️⃣ Guarda el GPT

---

## ✨ RESULTADO:

Cuando hables con cualquier GPT (ejemplo: Adrián), él podrá:
- ✅ Llamar automáticamente al orquestador en Render
- ✅ El orquestador coordinará con otros agentes
- ✅ Verás las conversaciones entre agentes en la respuesta
- ✅ Recibirás el análisis consolidado final

---

## 🔥 EJEMPLO DE USO:

**Tú a Adrián:**
> "Analiza viabilidad de expandir a Portugal"

**Adrián internamente:**
1. Llama al orquestador (`/gpt/smart/request`)
2. El orquestador consulta a Andrés (director) para decidir equipo
3. Andrés asigna: Bruno (estrategia), Carlos (logística), Marco (fiscal), Leo (partners)
4. Los agentes colaboran entre sí según necesiten
5. Andrés consolida
6. Adrián te muestra el resultado completo

---

## 📝 GPTs QUE NECESITAS CONFIGURAR:

1. ✅ Carlos M. - Experto logística
2. ✅ AURORA - Atención al Cliente
3. ✅ Nexus Valiant - Arquitecto Digital
4. ✅ Elena Martínez - Gestión Inventario
5. ✅ Valeria L. - Legal y Compliance
6. ✅ Camila R. - Branding
7. ✅ Diego F. - Automatización Marketing
8. ✅ Lucía P. - Atención Multicanal
9. ✅ Francisco - Customer Success
10. ✅ Bruno Álvarez - Estrategia
11. ✅ Leo Partners - Alianzas
12. ✅ Adrián Weis - Analista Datos
13. ✅ Orquestador IA
14. ✅ Marco Vargas - Fiscal
15. ✅ Lalo - Ventas
16. ✅ Sofía H. - Conversión
17. ✅ Antonio - Prompts Master
18. ✅ Markus Garcia - Marketing Digital

---

## ⚠️ IMPORTANTE:

**TODOS los GPTs deben tener el MISMO schema** - así cualquier GPT puede activar el orquestador y colaborar con los demás.

---

## 🎉 DESPUÉS DE CONFIGURAR:

Prueba hablando con cualquier GPT con una petición compleja:
> "Quiero lanzar jamones premium en Francia. Dame análisis completo: mercado, legal, logística, estrategia"

Y verás cómo los agentes se coordinan automáticamente.
