from typing import Dict, List

def generate_summary(weather: Dict, exchange: Dict, stocks: List[Dict], news: List[Dict]) -> str:
    """Genera un resumen ejecutivo con los datos obtenidos."""
    try:
        # Información del clima
        weather_desc = weather.get('description', 'No disponible')
        temp = weather.get('temperature', 'N/A')
        
        # Información de cambio
        rate = exchange.get("rate")
        rate_str = f"{rate:.2f}" if rate else "no disponible"
        pair = exchange.get("pair", "USD/BRL")
        
        # Información de acciones
        successful_stocks = [s for s in stocks if s.get("success") and s.get("market_status") == "Abierto"]
        stock_info = "No hay datos disponibles"
        if successful_stocks:
            main_stock = successful_stocks[0]
            today_data = main_stock.get("today", {})
            if today_data:
                stock_info = f"{main_stock['symbol']} a ${today_data.get('close', 'N/A')}"
        
        # Información de noticias
        news_info = "sin noticias recientes"
        if news and "error" not in news[0]:
            news_info = news[0]['title'][:100] + "..." if len(news[0]['title']) > 100 else news[0]['title']

        summary = (
            f"🌤 **Clima**: {weather_desc} con temperatura de {temp}°C. "
            f"💱 **Tipo de cambio**: {pair} en {rate_str}. "
            f"📈 **Acción destacada**: {stock_info}. "
            f"📰 **Última noticia**: {news_info}."
        )
        
    except Exception as e:
        summary = f"⚠️ Error generando resumen: {str(e)}"
        
    return summary