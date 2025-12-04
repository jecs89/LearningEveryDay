import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv
import random

load_dotenv()

class StockDataAgent:
    """Agente mejorado para obtener datos de acciones con múltiples fuentes de respaldo"""
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API")
        self.yahoo_finance_url = "https://yahoo-finance127.p.rapidapi.com"
        self.fallback_enabled = True
    
    def get_stock_data(self, symbols: str = "NVDA,TSLA,INTC,ORCL,MSFT") -> List[Dict]:
        """Obtiene datos de acciones con múltiples fuentes de respaldo"""
        
        symbol_list = [s.strip().upper() for s in symbols.split(",")]
        result = []
        
        for symbol in symbol_list:
            stock_data = None
            
            # Intentar con Alpha Vantage primero
            if self.alpha_vantage_key:
                stock_data = self._get_alpha_vantage_data(symbol)
            
            # Si Alpha Vantage falla, intentar con datos simulados
            if not stock_data or not stock_data.get("success"):
                stock_data = self._get_simulated_data(symbol)
            
            result.append(stock_data)
        
        return result
    
    def _get_alpha_vantage_data(self, symbol: str) -> Dict:
        """Obtiene datos de Alpha Vantage"""
        base_url = "https://www.alphavantage.co/query"
        
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.alpha_vantage_key
        }

        try:
            response = requests.get(base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            # Verificar errores de la API
            if "Error Message" in data:
                return {
                    "symbol": symbol, 
                    "error": "Invalid API call or symbol",
                    "success": False
                }
                
            if "Note" in data:
                return {
                    "symbol": symbol,
                    "error": "API call limit reached",
                    "success": False
                }

            time_series = data.get("Time Series (Daily)", {})
            if not time_series:
                return {
                    "symbol": symbol, 
                    "error": "No data available",
                    "success": False
                }

            # Obtener fechas disponibles ordenadas
            dates = sorted(time_series.keys(), reverse=True)
            if not dates:
                return {
                    "symbol": symbol,
                    "error": "No dates available",
                    "success": False
                }
                
            latest_date = dates[0]
            latest_data = time_series[latest_date]

            # Verificar si los datos son del día actual
            latest_date_obj = datetime.strptime(latest_date, "%Y-%m-%d").date()
            today = datetime.utcnow().date()
            
            # Considerar que el mercado está cerrado si los datos no son del día actual
            market_closed = latest_date_obj < today

            stock_info = {
                "symbol": symbol,
                "last_update": latest_date,
                "market_status": "Cerrado" if market_closed else "Abierto",
                "success": True,
                "data_source": "Alpha Vantage"
            }

            if not market_closed:
                stock_info["today"] = {
                    "open": float(latest_data["1. open"]),
                    "high": float(latest_data["2. high"]),
                    "low": float(latest_data["3. low"]),
                    "close": float(latest_data["4. close"]),
                    "volume": int(latest_data["5. volume"])
                }

            # Agregar datos del día anterior para comparación
            if len(dates) > 1:
                previous_data = time_series[dates[1]]
                stock_info["yesterday"] = {
                    "open": float(previous_data["1. open"]),
                    "close": float(previous_data["4. close"])
                }

            return stock_info

        except Exception as e:
            return {
                "symbol": symbol, 
                "error": f"Alpha Vantage error: {str(e)}",
                "success": False
            }
    
    def _get_simulated_data(self, symbol: str) -> Dict:
        """Genera datos simulados realistas para demostración"""
        
        # Precios base realistas para cada símbolo
        base_prices = {
            "NVDA": 850.00,  # NVIDIA
            "TSLA": 180.00,  # Tesla
            "INTC": 35.00,   # Intel
            "ORCL": 120.00,  # Oracle
            "MSFT": 400.00,  # Microsoft
            "AAPL": 190.00,  # Apple
            "GOOGL": 160.00, # Google
        }
        
        base_price = base_prices.get(symbol, 100.00)
        
        # Variación diaria realista (±5%)
        daily_change = random.uniform(-0.05, 0.05)
        current_price = base_price * (1 + daily_change)
        
        # Generar datos del día
        open_price = current_price * random.uniform(0.99, 1.01)
        high_price = max(open_price, current_price) * random.uniform(1.00, 1.03)
        low_price = min(open_price, current_price) * random.uniform(0.97, 1.00)
        volume = random.randint(1000000, 50000000)
        
        # Determinar estado del mercado (simular horario de NY)
        now = datetime.utcnow()
        ny_time = now - timedelta(hours=5)  # UTC-5 para NY
        market_open = 9 <= ny_time.hour < 16  # 9 AM - 4 PM NY time
        
        return {
            "symbol": symbol,
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "market_status": "Abierto" if market_open else "Cerrado",
            "success": True,
            "data_source": "Simulated Data",
            "today": {
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "close": round(current_price, 2),
                "volume": volume
            },
            "yesterday": {
                "open": round(base_price * random.uniform(0.99, 1.01), 2),
                "close": round(base_price, 2)
            }
        }
    
    def get_stock_news(self, symbol: str) -> List[Dict]:
        """Obtiene noticias relacionadas con una acción específica"""
        # Esto podría integrarse con NewsAPI o otra fuente
        return []