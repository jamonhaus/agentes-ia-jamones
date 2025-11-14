# INSTRUCCIONES PARA GPT ORQUESTADOR (ENDPOINTS QUE FUNCIONAN)

## ENDPOINTS DISPONIBLES AHORA MISMO EN RENDER

```
✅ /gpt/task/execute       - Tarea simple con 1 agente
✅ /gpt/director/coordinate - Andrés analiza y decide equipo
✅ /gpt/team/analyze       - Varios agentes trabajan en paralelo
✅ /gpt/workflow/execute   - Pipeline secuencial
✅ /gpt/agents/list        - Lista de todos los agentes
✅ /gpt/health/team        - Estado del equipo

❌ /gpt/smart/request      - NO EXISTE (deployment fallido)
```

## SOLUCIÓN: USA `/gpt/director/coordinate` + `/gpt/team/analyze`

### PASO 1: Configura tu GPT

**Instructions:**
```
Eres Andrés, el Director General de JamonHaus. Coordinas un equipo de 14 agentes especializados.

PROCESO PARA CADA PETICIÓN:

1. ANALIZAR con director/coordinate:
   - Llamas a director/coordinate con la petición completa
   - Andrés decide qué agentes necesita y el plan

2. EJECUTAR con team/analyze:
   - Llamas a team/analyze con los agentes que Andrés decidió
   - Los agentes trabajan EN PARALELO automáticamente

3. PRESENTAR resultado:
   📊 EQUIPO PARTICIPANTE
   [Lista de agentes]
   
   🎯 RESULTADO CONSOLIDADO
   [Análisis integrado]

AGENTES DISPONIBLES:
- andres_director: Director y coordinación
- adrian_datos: Análisis de datos y mercado
- leo_partners: Alianzas estratégicas
- bruno_estrategia: Estrategia comercial
- francisco_success: Customer Success
- lucia_canales: Marketing multicanal
- diego_automatizacion: Automatización
- camila_branding: Branding y comunicación
- valeria_legal: Legal y compliance
- sofia_conversion: Optimización conversión
- elena_inventario: Gestión inventario
- carlos_logistica: Logística y distribución
- marco_fiscal: Optimización fiscal
- lalo_ventas: Ventas B2B/B2C

NUNCA inventes. SIEMPRE usa director/coordinate primero.
```

### PASO 2: Configura Actions

1. Ve a **Actions** → **Create new action**
2. Click **Import from URL**
3. URL: `https://agentes-ia-jamones.onrender.com/openapi.json`
4. Click **Import**
5. Verifica que aparezcan estos 6 endpoints
6. **Save**

## EJEMPLO DE USO REAL

**Usuario dice:**
```
"Necesito estudio de mercado para Portugal"
```

**GPT hace (automático):**

### Llamada 1: Análisis del Director
```json
POST /gpt/director/coordinate
{
  "request": "Necesito estudio de mercado completo para Portugal",
  "context": {}
}
```

**Respuesta:**
```json
{
  "director": "Andrés",
  "director_analysis": "Para este estudio necesito:
    - Adrián (adrian_datos): Analizar datos mercado portugués
    - Leo (leo_partners): Identificar partners potenciales
    - Bruno (bruno_estrategia): Plan estratégico de entrada
    - Valeria (valeria_legal): Compliance legal UE
    - Marco (marco_fiscal): Optimización fiscal Portugal",
  "status": "plan_created"
}
```

### Llamada 2: Ejecución Paralela del Equipo
```json
POST /gpt/team/analyze
{
  "project": "Expansión JamonHaus Portugal",
  "objective": "Estudio de mercado completo",
  "agents": ["adrian_datos", "leo_partners", "bruno_estrategia", "valeria_legal", "marco_fiscal"],
  "context": {}
}
```

**Respuesta:**
```json
{
  "project": "Expansión JamonHaus Portugal",
  "team_analyses": [
    {
      "agent": "Adrián",
      "role": "Analista de Datos",
      "analysis": "[Análisis mercado portugués...]"
    },
    {
      "agent": "Leo",
      "role": "Director Alianzas",
      "analysis": "[Partners potenciales...]"
    },
    {
      "agent": "Bruno",
      "role": "Estratega Comercial",
      "analysis": "[Plan estratégico...]"
    },
    {
      "agent": "Valeria",
      "role": "Directora Legal",
      "analysis": "[Compliance legal...]"
    },
    {
      "agent": "Marco",
      "role": "Director Fiscal",
      "analysis": "[Optimización fiscal...]"
    }
  ],
  "status": "analysis_completed"
}
```

### Llamada 3: GPT consolida y presenta

```
📊 EQUIPO PARTICIPANTE
- Andrés (Director) - Coordinación general
- Adrián (Datos) - Análisis mercado portugués
- Leo (Alianzas) - Partners potenciales  
- Bruno (Estrategia) - Plan de entrada
- Valeria (Legal) - Compliance UE
- Marco (Fiscal) - Optimización fiscal

🎯 RESULTADO CONSOLIDADO

[GPT integra los 5 análisis en un informe coherente]

MERCADO PORTUGUÉS
[Análisis de Adrián...]

PARTNERS ESTRATÉGICOS
[Análisis de Leo...]

PLAN DE ENTRADA
[Análisis de Bruno...]

MARCO LEGAL
[Análisis de Valeria...]

OPTIMIZACIÓN FISCAL
[Análisis de Marco...]
```

## PRUEBA AHORA

Copia las **Instructions** en tu GPT → Importa Actions → Prueba preguntando:

```
"Necesito analizar la viabilidad de abrir tienda en Barcelona"
```

El GPT automáticamente:
1. ✅ Llama a `director/coordinate` (Andrés decide equipo)
2. ✅ Llama a `team/analyze` (Equipo trabaja en paralelo)
3. ✅ Te muestra resultado consolidado

---

## NOTA TÉCNICA

El endpoint `/gpt/smart/request` que consolidaba esto en 1 sola llamada **EXISTE EN EL CÓDIGO** pero Render no lo deployó correctamente. 

Mientras se re-deploya, usa este método de 2 llamadas que **FUNCIONA PERFECTAMENTE** y hace exactamente lo mismo.
