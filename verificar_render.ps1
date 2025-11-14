# Script para verificar que Render funciona correctamente

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 79 -ForegroundColor Cyan
Write-Host "VERIFICACIÓN DE RENDER" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan

Write-Host "`n1. Verificando que el servidor responde..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "https://agentes-ia-jamones.onrender.com/" -ErrorAction Stop
    Write-Host "   ✅ Servidor activo" -ForegroundColor Green
    Write-Host "   Versión: $($health.versión)" -ForegroundColor White
    Write-Host "   Agentes disponibles: $($health.agentes_disponibles.Count)" -ForegroundColor White
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n2. Verificando endpoint smart/request..." -ForegroundColor Yellow
try {
    $body = @{
        request = "Test rápido"
        context = @{}
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri "https://agentes-ia-jamones.onrender.com/gpt/smart/request" -Method Post -Body $body -ContentType "application/json" -ErrorAction Stop
    
    Write-Host "   ✅ Endpoint funciona correctamente" -ForegroundColor Green
    Write-Host "   Tipo de trabajo: $($response.tipo_trabajo)" -ForegroundColor White
    Write-Host "   Agentes participantes: $($response.equipo_participante.Count)" -ForegroundColor White
    Write-Host "   Modo: $($response.proceso.modo)" -ForegroundColor White
    
    Write-Host "`n" -NoNewline
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host "✅ ¡RENDER FUNCIONA PERFECTAMENTE!" -ForegroundColor Green
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host "`nYa puedes configurar tu GPT con:" -ForegroundColor White
    Write-Host "  URL: https://agentes-ia-jamones.onrender.com/openapi.json" -ForegroundColor Cyan
    
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`n⚠️  Posibles causas:" -ForegroundColor Yellow
    Write-Host "   - El deploy aún no terminó (espera 2-3 minutos más)" -ForegroundColor White
    Write-Host "   - La API Key no se guardó correctamente" -ForegroundColor White
    Write-Host "   - Render está procesando el cambio" -ForegroundColor White
    exit 1
}
