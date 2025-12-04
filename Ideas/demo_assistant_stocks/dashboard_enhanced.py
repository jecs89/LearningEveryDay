import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json

st.set_page_config(
    page_title="Sistema Multi-Agente Inteligente",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS mejorado
# st.markdown("""
# <style>
#     .agent-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white;
#         margin: 10px 0;
#     }
#     .recommendation-buy { border-left: 5px solid #28a745; background-color: #f8fff9; }
#     .recommendation-sell { border-left: 5px solid #dc3545; background-color: #fff8f8; }
#     .recommendation-hold { border-left: 5px solid #ffc107; background-color: #fffef0; }
#     .metric-positive { color: #28a745; font-weight: bold; }
#     .metric-negative { color: #dc3545; font-weight: bold; }
#     .metric-neutral { color: #6c757d; font-weight: bold; }
#     .main-header {
#         font-size: 2.5rem;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .metric-card {
#         background-color: #f0f2f6;
#         padding: 1rem;
#         border-radius: 10px;
#         border-left: 4px solid #1f77b4;
#     }
# </style>
# """, unsafe_allow_html=True)

def display_agent_analysis(analysis_data):
    """Muestra análisis de los agentes de forma organizada"""
    
    # Análisis de Inversión
    with st.expander("🤖 **Agente de Recomendaciones de Inversión**", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Análisis OpenAI")
            openai_analysis = analysis_data['investment_recommendations']['openai_analysis']
            if 'raw_analysis' in openai_analysis:
                st.write(openai_analysis['raw_analysis'])
            else:
                st.json(openai_analysis)
        
        with col2:
            st.subheader("🧠 Análisis DeepSeek") 
            deepseek_analysis = analysis_data['investment_recommendations']['deepseek_analysis']
            if 'raw_analysis' in deepseek_analysis:
                st.write(deepseek_analysis['raw_analysis'])
            else:
                st.json(deepseek_analysis)
        
        st.subheader("✅ Consenso Mistral")
        consensus = analysis_data['investment_recommendations']['consensus']
        if 'raw_analysis' in consensus:
            st.info(consensus['raw_analysis'])
        else:
            st.json(consensus)
    
    # Análisis Sectorial
    with st.expander("🎪 **Agente de Análisis Sectorial (Tecnología)**", expanded=True):
        sector_data = analysis_data['sector_analysis']
        st.metric("Acciones Analizadas", len(sector_data['stocks_analyzed']))
        st.metric("Noticias del Sector", sector_data['news_count'])
        
        if 'analysis' in sector_data['sector_analysis']:
            st.write(sector_data['sector_analysis']['analysis'])
        else:
            st.json(sector_data['sector_analysis'])
    
    # Sentimiento del Mercado
    with st.expander("📈 **Agente de Sentimiento del Mercado**", expanded=True):
        sentiment_data = analysis_data['market_sentiment']
        st.metric("Noticias Analizadas", sentiment_data['news_analyzed'])
        st.metric("Puntos de Datos", sentiment_data['data_points'])
        
        if 'raw_sentiment' in sentiment_data['sentiment_analysis']:
            st.write(sentiment_data['sentiment_analysis']['raw_sentiment'])
        else:
            st.json(sentiment_data['sentiment_analysis'])

def display_basic_dashboard(data):
    """Muestra el dashboard básico original"""
    # --- CLIMA Y CAMBIO ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌤 Clima")
        weather = data.get("weather", {})
        st.markdown(f"""
        <div class="metric-card">
            <p><strong>Descripción:</strong> {weather.get('description', 'Sin descripción')}</p>
            <p><strong>Temperatura:</strong> {weather.get('temperature', '?')}°C</p>
            <p><strong>Viento:</strong> {weather.get('windspeed', '?')} km/h</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💱 Tipo de Cambio")
        exchange = data.get("exchange", {})
        rate = exchange.get('rate')
        if rate:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{exchange.get('pair', 'USD/BRL')}</h3>
                <p style="font-size: 2rem; font-weight: bold; color: #1f77b4;">
                    {rate:.2f}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Tipo de cambio no disponible")

    # --- ACCIONES ---
    st.subheader("📈 Acciones - Últimos datos disponibles")

    stock_data = []
    for s in data.get("stocks", []):
        # Si hubo error al obtener los datos
        if "error" in s:
            stock_data.append({
                "Símbolo": s["symbol"],
                "Estado": "Error",
                "Mensaje": s["error"]
            })
            continue

        # Si el mercado está cerrado
        if s.get("market_status") == "Cerrado":
            stock_data.append({
                "Símbolo": s["symbol"],
                "Estado": "Mercado cerrado",
                "Última actualización": s.get("last_update", "-"),
                "Apertura (hoy)": None,
                "Cierre (hoy)": None,
                "Máx (hoy)": None,
                "Mín (hoy)": None,
                "Volumen (hoy)": None,
            })
            continue

        # Si hay datos del día actual
        today = s.get("today", {})
        stock_data.append({
            "Símbolo": s["symbol"],
            "Estado": s.get("market_status", "Abierto"),
            "Apertura (hoy)": today.get("open"),
            "Cierre (hoy)": today.get("close"),
            "Máx (hoy)": today.get("high"),
            "Mín (hoy)": today.get("low"),
            "Volumen (hoy)": today.get("volume"),
        })

    if stock_data:
        st.dataframe(pd.DataFrame(stock_data))
    else:
        st.warning("No hay datos de acciones disponibles")

    # --- NOTICIAS ---
    st.subheader("📰 Noticias")
    news = data.get("news", [])
    if not news:
        st.info("Sin noticias recientes.")
    else:
        for n in news:
            st.markdown(f"- [{n['title']}]({n['url']}) — *{n['source']}*")

def main():
    st.markdown('<h1 class="main-header">🤖 Sistema Multi-Agente Inteligente</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuración")
        analysis_type = st.radio(
            "Tipo de Análisis:",
            ["Básico", "Avanzado con Agentes LLM"]
        )
        
        city = st.selectbox(
            "Ciudad para el clima:",
            ["São Paulo", "Rio de Janeiro", "Lima", "Buenos Aires", "Madrid"],
            key="city_selector"
        )
        
        st.markdown("---")
        st.markdown("**Agentes Activados:**")
        st.markdown("- 🤖 Agente de Inversión")
        st.markdown("- 🎪 Agente Sectorial") 
        st.markdown("- 📈 Agente de Sentimiento")
        st.markdown("- 🌐 Múltiples LLMs")
        
        st.markdown(f"**Última actualización:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if st.button("🔄 Actualizar Datos"):
            st.rerun()

    # Contenido principal
    if analysis_type == "Avanzado con Agentes LLM":
        st.info("🚀 **Ejecutando análisis avanzado con múltiples agentes LLM...**")
        
        try:
            with st.spinner("🤖 Los agentes están analizando los datos (esto puede tomar 1-2 minutos)..."):
                response = requests.get("http://127.0.0.1:8000/report/advanced", timeout=120)
                
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    # Mostrar metadatos
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Acciones Analizadas", data['basic_data']['stocks_analyzed'])
                    with col2:
                        st.metric("Noticias Procesadas", data['basic_data']['news_analyzed'])
                    with col3:
                        st.metric("Agentes", "3 especializados")
                    
                    # Mostrar análisis de agentes
                    display_agent_analysis(data)
                else:
                    st.error("Error en el análisis avanzado")
                
            else:
                st.error(f"Error en la API: {response.status_code}")
                
        except requests.exceptions.Timeout:
            st.error("⏰ Timeout: Los agentes están tomando más tiempo del esperado.")
            st.info("💡 Esto puede ser normal en la primera ejecución o si las APIs de LLM están lentas.")
            
        except requests.exceptions.ConnectionError:
            st.error("🔌 Error de conexión: No se puede conectar con la API.")
            st.info("💡 **Asegúrate de que el servidor API esté ejecutándose:** `python api_server_enhanced.py`")
            
        except Exception as e:
            st.error(f"Error inesperado: {e}")
            st.info("💡 Verifica que las claves API estén configuradas en el archivo .env")
    
    else:
        # Modo básico
        st.info("📊 **Modo Básico: Datos en Tiempo Real**")
        
        try:
            with st.spinner("Cargando datos básicos..."):
                city = st.session_state.get("city_selector", "São Paulo")
                response = requests.get(f"http://127.0.0.1:8000/report/daily?city={city}", timeout=30)
                
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    display_basic_dashboard(data)
                else:
                    st.error("Error en los datos básicos")
            else:
                st.error(f"Error cargando datos: {response.status_code}")
            
        except requests.exceptions.ConnectionError:
            st.error("🔌 No se puede conectar con la API")
            st.info("""
            **Para solucionar esto:**
            1. Asegúrate de que el servidor API esté ejecutándose
            2. Ejecuta: `python api_server_enhanced.py`
            3. Verifica que el puerto 8000 esté disponible
            """)
            
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()