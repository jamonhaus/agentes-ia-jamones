"""
Interfaz web simple con Gradio para interactuar con el orquestador
y VER la colaboración entre agentes
"""
import gradio as gr
from agents.orchestrator import AgentOrchestrator
import json

orchestrator = AgentOrchestrator()

def procesar_peticion(peticion):
    """Procesa la petición y muestra toda la colaboración"""
    
    # Ejecutar coordinación
    resultado = orchestrator.auto_coordinate(peticion, {})
    
    # Preparar respuesta formateada
    output = []
    
    # Título
    output.append("# 🎯 COORDINACIÓN COMPLETADA\n")
    
    # Equipo participante
    if "agent_results" in resultado:
        output.append(f"## 👥 EQUIPO ({len(resultado['agent_results'])} agentes)\n")
        for agent_id, result in resultado["agent_results"].items():
            output.append(f"- **{result.get('agent')}**: {result.get('tarea_asignada', 'N/A')[:80]}...\n")
        output.append("\n")
    
    # CONVERSACIONES ENTRE AGENTES (LO MÁS IMPORTANTE)
    conversaciones = resultado.get("agent_conversations", [])
    if conversaciones:
        output.append(f"## 💬 COLABORACIÓN ENTRE AGENTES ({len(conversaciones)} conversaciones)\n\n")
        for i, conv in enumerate(conversaciones, 1):
            output.append(f"### {i}. {conv.get('from_agent')} → {conv.get('to_agent')}\n")
            output.append(f"**Pregunta:** {conv.get('message', '')[:200]}...\n\n")
            output.append(f"**Respuesta:** {conv.get('response', '')[:300]}...\n\n")
            output.append("---\n\n")
    else:
        output.append("## ⚠️ No hubo conversaciones entre agentes\n\n")
    
    # Respuesta final
    output.append("## 📊 ANÁLISIS CONSOLIDADO\n\n")
    respuesta = resultado.get("final_response", "No disponible")
    output.append(respuesta[:1000] + "..." if len(respuesta) > 1000 else respuesta)
    
    return "".join(output)

# Crear interfaz
with gr.Blocks(title="Orquestador de Agentes IA - JamonHaus") as demo:
    gr.Markdown("""
    # 🚀 Orquestador de Agentes IA
    ## Sistema de Colaboración Inteligente
    
    Los agentes trabajan juntos y **se consultan entre sí** para darte la mejor respuesta.
    """)
    
    with gr.Row():
        with gr.Column():
            peticion = gr.Textbox(
                label="Tu Petición",
                placeholder="Ej: Necesito análisis para expandir a Portugal",
                lines=5
            )
            btn = gr.Button("🎯 Coordinar Equipo", variant="primary", size="lg")
        
        with gr.Column():
            resultado = gr.Markdown(label="Resultado")
    
    btn.click(procesar_peticion, inputs=[peticion], outputs=[resultado])
    
    gr.Examples(
        examples=[
            "Necesito análisis completo para expandir a Portugal",
            "Optimiza toda la operación de ventas online",
            "Plan de marketing para campaña de Navidad",
            "Análisis fiscal para expandir a Francia",
        ],
        inputs=[peticion]
    )

if __name__ == "__main__":
    print("🚀 Iniciando interfaz web del orquestador...")
    print("📍 Abre: http://localhost:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860)
