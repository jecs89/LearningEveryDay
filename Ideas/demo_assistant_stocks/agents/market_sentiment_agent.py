from .llm_base import LLMAgent
from typing import Dict, List
import json

class MarketSentimentAgent(LLMAgent):
    """Agente especializado en análisis de sentimiento del mercado"""
    
    def analyze(self, data: Dict) -> Dict:
        """Implementación del método abstracto"""
        news = data.get('news', [])
        stocks_data = data.get('stocks_data', [])
        return self.analyze_sentiment(news, stocks_data)
    
    def analyze_sentiment(self, news: List[Dict], stocks_data: List[Dict]) -> Dict:
        """Analiza el sentimiento general del mercado"""
        
        prompt = f"""
        Analiza el sentimiento del mercado basándote en estas noticias y datos:

        NOTICIAS RECIENTES (analiza sentimiento para cada una):
        {self._format_news_for_sentiment(news)}

        DATOS DE MERCADO ACTUAL:
        {self._format_market_data(stocks_data)}

        Proporciona un análisis de sentimiento que incluya:
        1. Sentimiento general (Alcista/Bajista/Neutral)
        2. Score de sentimiento (-10 a +10)
        3. Análisis por categorías: Tecnología, Mercado general, Economía
        4. Factores clave influyendo el sentimiento
        5. Recomendación basada en sentimiento

        Formato JSON.
        """
        
        system_message = """Eres un analista de sentimiento de mercados. 
        Evalúa objetivamente el tono y contenido de las noticias."""
        
        sentiment_analysis = self.call_deepseek(prompt, system_message)
        
        return {
            "sentiment_analysis": self._parse_sentiment(sentiment_analysis),
            "news_analyzed": len(news) if news and "error" not in news[0] else 0,
            "data_points": len([s for s in stocks_data if s.get("success")])
        }
    
    def _format_news_for_sentiment(self, news: List[Dict]) -> str:
        """Formatea noticias para análisis de sentimiento"""
        if not news or "error" in news[0]:
            return "No hay noticias para analizar"
        
        formatted = []
        for i, article in enumerate(news[:8], 1):  # Analizar hasta 8 noticias
            formatted.append(f"{i}. '{article['title']}' - {article['source']}")
        return "\n".join(formatted)
    
    def _format_market_data(self, stocks_data: List[Dict]) -> str:
        """Formatea datos de mercado para análisis"""
        market_summary = []
        successful_stocks = [s for s in stocks_data if s.get("success") and s.get("market_status") == "Abierto"]
        
        for stock in successful_stocks:
            today = stock.get("today", {})
            if today:
                change_pct = ((today.get('close', 0) - today.get('open', 0)) / today.get('open', 1)) * 100
                market_summary.append(
                    f"{stock['symbol']}: {change_pct:+.2f}%"
                )
        
        return f"Cambios diarios: {', '.join(market_summary)}" if market_summary else "Sin datos de mercado recientes"
    
    def _parse_sentiment(self, sentiment_text: str) -> Dict:
        """Parsea análisis de sentimiento"""
        try:
            if "{" in sentiment_text and "}" in sentiment_text:
                start = sentiment_text.find("{")
                end = sentiment_text.rfind("}") + 1
                json_str = sentiment_text[start:end]
                return json.loads(json_str)
            return {"raw_sentiment": sentiment_text}
        except json.JSONDecodeError:
            return {"raw_sentiment": sentiment_text}