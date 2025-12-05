# 🤖 Sistema Multi-Agente Inteligente para Análisis Financiero

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Sistema multi-agente inteligente que integra múltiples fuentes de datos y modelos de lenguaje (LLMs) para proporcionar análisis financieros en tiempo real, recomendaciones de inversión y visualización interactiva de mercados.

## ✨ Características Principales

### 🤖 **Agentes Especializados**
- **Agente de Inversión**: Recomendaciones de compra/venta usando múltiples LLMs
- **Agente Sectorial**: Análisis específico por sectores (tecnología, energía, etc.)
- **Agente de Sentimiento**: Análisis de mercado basado en noticias y tendencias
- **Agente de Datos**: Integración con APIs financieras y meteorológicas

### 📊 **Dashboard Interactivo**
- Visualización en tiempo real de datos de mercado
- Métricas clave y KPIs financieros
- Análisis comparativo entre acciones
- Noticias relevantes del sector

### 🔗 **Integraciones Múltiples**
- **LLMs**: OpenAI, DeepSeek, Mistral
- **Datos Financieros**: Alpha Vantage
- **Noticias**: NewsAPI
- **Meteorología**: Open-Meteo
- **Tipo de Cambio**: Exchange Rate API

## 🏗️ Arquitectura del Sistema

```mermaid
graph TB
    A[Dashboard Streamlit] <--> B[API FastAPI]
    B <--> C[Agente de Inversión]
    B <--> D[Agente Sectorial]
    B <--> E[Agente de Sentimiento]
    C <--> F[LLMs: OpenAI/DeepSeek/Mistral]
    D <--> G[Datos de Mercado]
    E <--> H[Noticias y Redes]
```

## 🚀 Instalación y Uso

### 1. Crear un entorno virtual
Ejecuta en tu terminal:

python -m venv venv

### 2. Activar el entorno
En Linux / macOS:

source venv/bin/activate

### 3. Instalar dependencias

pip install -r requirements.txt

### 4. Crear archivo `.env` con tus claves:

```
#LLM APIs
OPENAI_API_KEY=sk-tu_clave_aquis
DEEPSEEK_API_KEY=tu_clave_aqui
MISTRAL_API_KEY=tu_clave_aqui
```

### 5. Dar permisos al script de inicio

chmod +x start_in_current.sh

### 6. Ejecutar la aplicación

source start_in_current.sh