from .llm_base import LLMAgent
from typing import Dict, List
import json

class InvestmentAgent(LLMAgent):
    """Agente especializado en recomendaciones de inversión"""
    
    def analyze(self, data: Dict) -> Dict:
        """Implementación del método abstracto"""
        stocks_data = data.get('stocks_data', [])
        market_news = data.get('news', [])
        return self.analyze_investment(stocks_data, market_news)
    
    def analyze_investment(self, stocks_data: List[Dict], market_news: List[Dict]) -> Dict:
        """Analiza datos de acciones y noticias para generar recomendaciones"""
        
        # Preparar datos para el análisis
        stocks_summary = self._prepare_stocks_summary(stocks_data)
        news_summary = self._prepare_news_summary(market_news)
        
        prompt = f"""
        Eres un analista financiero experto. Analiza los siguientes datos de mercado y genera recomendaciones de inversión:

        DATOS DE ACCIONES:
        {stocks_summary}

        NOTICIAS RECIENTES:
        {news_summary}

        Por favor, genera un análisis que incluya:
        1. Recomendación general (COMPRAR/VENDER/MANTENER) para cada acción
        2. Justificación basada en datos técnicos y noticias
        3. Nivel de confianza (Alto/Medio/Bajo)
        4. Potencial de crecimiento a corto plazo
        5. Riesgos identificados

        Responde en formato JSON válido.
        """
        
        system_message = """Eres un analista financiero conservador y objetivo. 
        Basa tus recomendaciones únicamente en los datos proporcionados. 
        Sé cauteloso y destaca los riesgos."""
        
        # Usar múltiples LLMs para análisis diversificado
        openai_analysis = self.call_openai(prompt, system_message)
        deepseek_analysis = self.call_deepseek(prompt, system_message)
        
        return {
            "openai_analysis": self._parse_analysis(openai_analysis),
            "deepseek_analysis": self._parse_analysis(deepseek_analysis),
            "consensus": self._generate_consensus(openai_analysis, deepseek_analysis),
            "stocks_analyzed": len(stocks_data)
        }
    
    def _prepare_stocks_summary(self, stocks_data: List[Dict]) -> str:
        """Prepara resumen de datos de acciones"""
        summary = []
        for stock in stocks_data:
            if stock.get("success") and stock.get("market_status") == "Abierto":
                today = stock.get("today", {})
                summary.append(
                    f"- {stock['symbol']}: Apertura=${today.get('open', 'N/A')}, "
                    f"Cierre=${today.get('close', 'N/A')}, Volumen={today.get('volume', 'N/A')}"
                )
            else:
                summary.append(f"- {stock['symbol']}: Sin datos recientes")
        return "\n".join(summary)
    
    def _prepare_news_summary(self, news: List[Dict]) -> str:
        """Prepara resumen de noticias"""
        if not news or "error" in news[0]:
            return "No hay noticias recientes disponibles"
        
        summary = []
        for i, article in enumerate(news[:5], 1):
            summary.append(f"{i}. {article['title']} - {article['source']}")
        return "\n".join(summary)
    
    def _parse_analysis(self, analysis_text: str) -> Dict:
        """Parsea el análisis de texto a estructura de datos"""
        try:
            # Intentar extraer JSON si existe
            if "{" in analysis_text and "}" in analysis_text:
                start = analysis_text.find("{")
                end = analysis_text.rfind("}") + 1
                json_str = analysis_text[start:end]
                return json.loads(json_str)
            else:
                return {"raw_analysis": analysis_text}
        except json.JSONDecodeError:
            return {"raw_analysis": analysis_text}
    
    def _generate_consensus(self, analysis1: str, analysis2: str) -> Dict:
        """Genera consenso entre múltiples análisis"""
        prompt = f"""
        Tienes dos análisis de inversión del mismo conjunto de datos:
        
        ANÁLISIS 1:
        {analysis1}
        
        ANÁLISIS 2:
        {analysis2}
        
        Genera un consenso que combine ambos análisis, destacando:
        - Puntos de acuerdo
        - Puntos de desacuerdo
        - Recomendación final consensuada
        - Nivel de confianza combinado
        """
        
        consensus = self.call_mistral(prompt, "Eres un moderador de análisis financiero.")
        return self._parse_analysis(consensus)