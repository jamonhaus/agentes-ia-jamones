# 🎯 INSTRUCCIONES PARA CONFIGURAR TU GPT CON COLABORACIÓN REAL

## ⚠️ SISTEMA ASÍNCRONO - Los agentes se llaman entre sí

---

## 📋 1. ACTUALIZA EL SCHEMA DE ACTIONS

1. Abre tu GPT en ChatGPT
2. Ve a **Configure** → **Actions**  
3. **Borra** todo el schema anterior
4. Abre el archivo `GPT_ACTIONS_SCHEMA.json` de este proyecto
5. **Copia TODO** el contenido
6. **Pégalo** en el campo Schema
7. **Guarda**

---

## 📝 2. AÑADE ESTO AL FINAL DE LAS INSTRUCCIONES

```
---

COORDINACIÓN CON EQUIPO DE AGENTES:

Para peticiones complejas que requieran múltiples especialistas, usa el sistema de coordinación asíncrona:

PROCESO:
1. Llama a smartRequestAsync con la petición completa del usuario
2. Recibirás un job_id
3. Informa: "🔄 He activado el equipo completo. Los agentes están colaborando entre sí. Esto puede tardar 1-3 minutos..."
4. Consulta checkJobStatus cada 10-15 segundos con el job_id
5. Mientras status="processing", sigue consultando
6. Cuando status="completed", muestra EL RESULTADO COMPLETO

FORMATO DE RESPUESTA (MUY IMPORTANTE):

✅ Coordinación completada

👥 Equipo que participó:
[Lista cada agente con su rol]

💬 Colaboración entre agentes (CLAVE - MUESTRA ESTO):
[Para cada conversación en conversaciones_entre_agentes:]
- [from_agent] consultó a [to_agent]:
  Pregunta: "[message]"
  Respuesta: "[response]"

📊 Análisis consolidado:
[respuesta_final completa]

EJEMPLOS DE CUÁNDO USAR:
- "Analiza expansión a [país]" → Requiere: estrategia + legal + fiscal + logística
- "Plan de marketing completo" → Requiere: branding + canales + automatización + conversión
- "Optimiza toda la operación" → Requiere: datos + inventario + logística + ventas

IMPORTANTE:
- SIEMPRE muestra las conversaciones entre agentes
- El usuario QUIERE ver cómo colaboran
- No omitas las conversaciones aunque sean muchas
```

---

## 🧪 3. PRUEBA

Pregunta algo complejo:

```
Necesito análisis completo para expandir a Portugal:
- Viabilidad de mercado
- Requisitos legales  
- Logística necesaria
- Estrategia de entrada
- Análisis fiscal
```

---

## ✅ 4. QUÉ DEBERÍAS VER:

### Respuesta inicial (inmediata):
```
🔄 He activado el equipo completo. Los agentes están colaborando entre sí.

Andrés está coordinando a:
- Bruno (Estrategia)
- Valeria (Legal)
- Carlos (Logística)
- Marco (Fiscal)
- Leo (Alianzas)

Esto puede tardar 1-3 minutos porque se están consultando entre ellos...
```

### Después de 1-3 minutos:
```
✅ Coordinación completada

👥 Equipo que participó:
- Andrés - Director y coordinador
- Bruno - Análisis estratégico de mercado
- Valeria - Requisitos legales UE
- Carlos - Logística y distribución
- Marco - Análisis fiscal Portugal
- Leo - Identificación de partners

💬 Colaboración entre agentes:

1. Bruno consultó a Marco:
   Pregunta: "¿Cuáles son las tasas impositivas para exportación a Portugal?"
   Respuesta: "IVA 23% en Portugal continental, impuesto sobre sociedades 20% con surtasas..."

2. Valeria consultó a Carlos:
   Pregunta: "¿Qué certificaciones logísticas necesitamos para distribución en Portugal?"
   Respuesta: "Certificación sanitaria UE, control de cadena de frío, trazabilidad completa..."

3. Carlos consultó a Elena:
   Pregunta: "¿Qué productos tienen mejor rotación para priorizar en Portugal?"
   Respuesta: "Ibérico de bellota 50% y 100%, loncheados premium..."

📊 Análisis consolidado para expansión a Portugal:

[AQUÍ VA TODO EL ANÁLISIS FINAL COMPLETO]
```

---

## 🎯 ESTO ES LO QUE QUERÍAS:

- ✅ Ver cómo los agentes se llaman entre sí
- ✅ Ver qué preguntan
- ✅ Ver qué responden
- ✅ Ver cómo usan esa info
- ✅ Sin timeouts
- ✅ Colaboración REAL

---

## 🚀 PASOS FINALES:

1. ✅ Actualiza el schema en Actions
2. ✅ Añade las instrucciones al final
3. ✅ Guarda el GPT
4. ✅ Repite para TODOS tus 18 GPTs
5. ✅ Prueba con pregunta compleja
6. ✅ Verifica que veas las conversaciones entre agentes

---

## 💡 NOTA:

Render tardará ~2-3 minutos en re-deployar después del push que acabamos de hacer. Espera unos minutos antes de probar.

Puedes verificar que esté listo en: https://agentes-ia-jamones.onrender.com/docs
