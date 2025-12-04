import requests
import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

def get_exchange_rate(base: str = "USD", target: str = "BRL") -> Dict:
    """Obtiene el tipo de cambio entre dos monedas."""
    api_key = os.getenv("EXCHANGE_RATE_API")
    url = f"https://open.er-api.com/v6/latest/{base}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("result") == "success":
            rate = data["rates"].get(target)
            return {
                "pair": f"{base}/{target}",
                "rate": rate,
                "success": True
            }
        else:
            return {
                "pair": f"{base}/{target}",
                "rate": None,
                "error": data.get("error", "Unknown error"),
                "success": False
            }
    except requests.exceptions.RequestException as e:
        return {
            "pair": f"{base}/{target}",
            "rate": None,
            "error": str(e),
            "success": False
        }