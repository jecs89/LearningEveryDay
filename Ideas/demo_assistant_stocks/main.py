from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from agents.weather_agent import get_weather
from agents.exchange_agent import get_exchange_rate
from agents.stocks_agent import get_stock_data
from agents.news_agent import get_news
from agents.summarizer_agent import generate_summary

app = FastAPI(
    title="Reporte Diario Inteligente",
    description="API para dashboard de datos financieros, climáticos y noticias",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Reporte Diario Inteligente API"}

@app.get("/report/daily")
async def daily_report(city: str = "São Paulo"):
    try:
        weather = get_weather(city)
        exchange = get_exchange_rate()
        stocks = get_stock_data("NVDA,TSLA,INTC,ORCL,MSFT")
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
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)