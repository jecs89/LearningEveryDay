from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from agents.weather_agent import get_weather
from agents.exchange_agent import get_exchange_rate
from agents.news_agent import get_news
from agents.summarizer_agent import generate_summary
from agents.investment_agent import InvestmentAgent
from agents.sector_analysis_agent import SectorAnalysisAgent
from agents.market_sentiment_agent import MarketSentimentAgent
from agents.stocks_agent import StockDataAgent  # Nuevo agente

app = FastAPI(
    title="Sistema Multi-Agente Inteligente",
    description="API avanzada con agentes LLM para análisis financiero",
    version="2.1.0"  # Versión actualizada
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar agentes
investment_agent = InvestmentAgent()
sector_agent = SectorAnalysisAgent()
sentiment_agent = MarketSentimentAgent()
stock_agent = StockDataAgent()  # Nuevo agente de stocks

@app.get("/")
async def root():
    return {"message": "Sistema Multi-Agente Inteligente API v2.1"}

@app.get("/report/daily")
async def daily_report(city: str = "São Paulo"):
    """Endpoint original mejorado con nuevo agente de stocks"""
    try:
        logger.info(f"Obteniendo reporte diario para ciudad: {city}")
        weather = get_weather(city)
        exchange = get_exchange_rate()
        stocks = stock_agent.get_stock_data("NVDA,TSLA,INTC,ORCL,MSFT")  # Usar nuevo agente
        news = get_news()
        summary = generate_summary(weather, exchange, stocks, news)

        return {
            "success": True,
            "weather": weather,
            "exchange": exchange,
            "stocks": stocks,
            "news": news,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error en reporte diario: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/report/advanced")
async def advanced_report():
    """Nuevo endpoint con análisis de agentes LLM"""
    try:
        logger.info("Iniciando análisis avanzado con agentes LLM")
        
        # Obtener datos base con nuevo agente
        stocks = stock_agent.get_stock_data("NVDA,TSLA,INTC,ORCL,MSFT,AAPL,GOOGL")
        news = get_news(query="mercado tecnología finanzas", page_size=10)
        
        logger.info(f"Datos obtenidos: {len(stocks)} acciones, {len(news) if news else 0} noticias")
        
        # Preparar datos para los agentes
        analysis_data = {
            'stocks_data': stocks,
            'news': news
        }
        
        # Ejecutar análisis con múltiples agentes
        logger.info("Ejecutando agente de inversión...")
        investment_analysis = investment_agent.analyze(analysis_data)
        
        logger.info("Ejecutando agente sectorial...")
        sector_analysis = sector_agent.analyze(analysis_data)
        
        logger.info("Ejecutando agente de sentimiento...")
        sentiment_analysis = sentiment_agent.analyze(analysis_data)
        
        logger.info("Análisis completado exitosamente")
        
        return {
            "success": True,
            "basic_data": {
                "stocks_analyzed": len(stocks),
                "news_analyzed": len(news) if news and "error" not in news[0] else 0,
                "timestamp": datetime.now().isoformat()
            },
            "investment_recommendations": investment_analysis,
            "sector_analysis": sector_analysis,
            "market_sentiment": sentiment_analysis,
            "agent_metadata": {
                "investment_agent": "OpenAI GPT-4 + DeepSeek",
                "sector_agent": "OpenAI GPT-4", 
                "sentiment_agent": "DeepSeek",
                "stock_data_agent": "Alpha Vantage + Simulated Data"
            }
        }
    except Exception as e:
        logger.error(f"Error en análisis avanzado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in advanced analysis: {str(e)}")

@app.get("/stocks/{symbols}")
async def get_stocks_data(symbols: str):
    """Endpoint específico para datos de acciones"""
    try:
        stocks_data = stock_agent.get_stock_data(symbols)
        return {
            "success": True,
            "symbols": symbols,
            "data": stocks_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error obteniendo datos de acciones: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting stock data: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "version": "2.1.0", 
        "agents": "active",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    logger.info("Iniciando servidor API mejorado en puerto 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")