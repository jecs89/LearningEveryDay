import requests
from typing import Dict, Optional

CITY_COORDINATES = {
    "São Paulo": (-23.55, -46.63),
    "Rio de Janeiro": (-22.91, -43.17),
    "Lima": (-12.04, -77.03),
    "Buenos Aires": (-34.60, -58.38),
    "Madrid": (40.42, -3.70)
}

def get_weather(city: str = "São Paulo") -> Dict:
    """Obtiene datos meteorológicos para una ciudad específica."""
    lat, lon = CITY_COORDINATES.get(city, (-23.55, -46.63))
    
    url = f"https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "current_weather" in data:
            current = data["current_weather"]
            return {
                "city": city,
                "temperature": current.get("temperature"),
                "windspeed": current.get("windspeed"),
                "winddirection": current.get("winddirection"),
                "description": f"Viento {current.get('windspeed')} km/h, dirección {current.get('winddirection')}°"
            }
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching weather data: {str(e)}"}
    
    return {"error": "Weather data not available"}