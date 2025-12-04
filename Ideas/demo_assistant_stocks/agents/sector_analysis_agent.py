from .llm_base import LLMAgent
from typing import Dict, List
import json

class SectorAnalysisAgent(LLMAgent):
    """Agente especializado en análisis sectorial"""
    
    def analyze(self, data: Dict) -> Dict:
        """Implementación del método abstracto - analiza sector tecnológico por defecto"""
        stocks_data = data.get('stocks_data', [])
        news = data.get('news', [])
        return self.analyze_technology_sector(stocks_data, news)
    
    def analyze_technology_sector(self, stocks_data: List[Dict], news: List[Dict]) -> Dict:
        """Analiza específicamente el sector tecnológico"""
        
        tech_stocks = [s for s in stocks_data if s['symbol'] in ['NVDA', 'MSFT', 'INTC', 'ORCL', 'AAPL', 'GOOGL']]
        tech_news = self._filter_tech_news(news)
        
        prompt = f"""
        Analiza el estado del sector tecnológico basándote en estos datos:

        ACCIONES TECNOLÓGICAS:
        {self._format_tech_stocks(tech_stocks)}

        NOTICIAS DEL SECTOR:
        {self._format_tech_news(tech_news)}

        Proporciona un análisis que incluya:
        1. Tendencia general del sector tecnológico
        2. Fortalezas y debilidades identificadas
        3. Impacto de noticias recientes
        4. Recomendación para inversión en el sector
        5. Empresas destacadas (positivas y negativas)

        Formato JSON estructurado.
        """
        
        system_message = "Eres un analista especializado en tecnología y mercados tech."
        
        analysis = self.call_openai(prompt, system_message)
        
        return {
            "sector_analysis": self._parse_analysis(analysis),
            "stocks_analyzed": [s['symbol'] for s in tech_stocks],
            "news_count": len(tech_news),
            "sector": "technology"
        }
    
    def _filter_tech_news(self, news: List[Dict]) -> List[Dict]:
        """Filtra noticias relacionadas con tecnología"""
        if not news or "error" in news[0]:
            return []
        
        tech_keywords = ['tech', 'tecnología', 'software', 'hardware', 'IA', 'AI', 
                        'NVIDIA', 'Microsoft', 'Intel', 'Oracle', 'chip', 'semiconductor',
                        'Apple', 'Google', 'Amazon', 'Meta', 'Tesla']
        
        tech_news = []
        for article in news:
            title = article.get('title', '').lower()
            if any(keyword.lower() in title for keyword in tech_keywords):
                tech_news.append(article)
        
        return tech_news[:3]  # Máximo 3 noticias
    
    def _format_tech_stocks(self, tech_stocks: List[Dict]) -> str:
        """Formatea datos de acciones tecnológicas"""
        formatted = []
        for stock in tech_stocks:
            if stock.get("success") and stock.get("market_status") == "Abierto":
                today = stock.get("today", {})
                change = ((today.get('close', 0) - today.get('open', 0)) / today.get('open', 1)) * 100
                formatted.append(
                    f"- {stock['symbol']}: ${today.get('close'):.2f} "
                    f"(Cambio: {change:+.2f}%) Vol: {today.get('volume'):,}"
                )
            else:
                formatted.append(f"- {stock['symbol']}: Datos no disponibles")
        return "\n".join(formatted)
    
    def _format_tech_news(self, tech_news: List[Dict]) -> str:
        """Formatea noticias del sector tecnológico"""
        if not tech_news:
            return "No hay noticias específicas de tecnología recientes"
        
        formatted = []
        for article in tech_news:
            formatted.append(f"• {article['title']} ({article['source']})")
        return "\n".join(formatted)
    
    def _parse_analysis(self, analysis_text: str) -> Dict:
        """Parsea análisis a estructura JSON"""
        try:
            if "{" in analysis_text and "}" in analysis_text:
                start = analysis_text.find("{")
                end = analysis_text.rfind("}") + 1
                json_str = analysis_text[start:end]
                return json.loads(json_str)
            return {"analysis": analysis_text}
        except json.JSONDecodeError:
            return {"analysis": analysis_text}