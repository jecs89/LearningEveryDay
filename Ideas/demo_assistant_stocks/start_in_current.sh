#!/bin/bash

# Script para iniciar todo en la terminal actual (sin nuevas ventanas)

echo "🚀 Iniciando Sistema Multi-Agente en terminal actual"

# # Verificar directorio
# if [ ! -d "agents_demo" ]; then
#     echo "❌ Error: No se encuentra el directorio 'agents_demo'"
#     exit 1
# fi

# Verificar entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "🔧 Activando entorno virtual..."
    source bin/activate
fi

cd agents_demo

# Matar procesos anteriores
echo "🧹 Limpiando procesos anteriores..."
pkill -f "python.*api_server" 2>/dev/null
pkill -f "streamlit" 2>/dev/null
sleep 2

# Iniciar API Server en background
echo "🔧 Iniciando API Server en segundo plano..."
python api_server_enhanced.py &
API_PID=$!

# Esperar a que la API esté lista
echo "⏳ Esperando a que API Server esté listo..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        echo "✅ API Server listo (PID: $API_PID)"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Timeout esperando API Server"
        kill $API_PID 2>/dev/null
        exit 1
    fi
    sleep 1
done

# Iniciar Dashboard
echo "🎨 Iniciando Dashboard..."
echo "💡 El dashboard se abrirá en tu navegador automáticamente"
streamlit run dashboard_enhanced.py

# Cuando se cierre el dashboard, también cerrar la API
echo "🧹 Cerrando API Server..."
kill $API_PID 2>/dev/null