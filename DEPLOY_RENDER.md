# Render Deployment Guide

## Pasos para desplegar en Render.com

1. **Crea una cuenta en Render.com**
   - Ve a https://render.com
   - Regístrate con GitHub o email

2. **Sube tu código a GitHub**
   - Crea un repositorio en GitHub
   - Sube esta carpeta completa

3. **Crea un Web Service en Render**
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Configuración:
     - Name: `agentes-ia-orquestador`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Configura las variables de entorno**
   En la sección "Environment" añade tus valores reales:
   ```
   OPENAI_API_KEY=sk-xxxx-tu-clave-real
   OPENAI_MODEL=gpt-4
   API_HOST=0.0.0.0
   API_PORT=8000
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Espera 5-10 minutos
   - Obtendrás una URL tipo: `https://agentes-ia-orquestador.onrender.com`

6. **Usa la URL en tus GPTs**
   - Ve a cada GPT en ChatGPT Plus
   - Settings → Actions
   - Pega: `https://tu-url.onrender.com/openapi.json`

## Nota importante
El plan gratuito de Render duerme después de 15 minutos de inactividad. La primera petición puede tardar 30-60 segundos en despertar el servicio.
