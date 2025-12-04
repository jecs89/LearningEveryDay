import os
import requests
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

def get_news(query: str = "tecnología", language: str = "es", page_size: int = 5) -> List[Dict]:
    """Obtiene noticias recientes basadas en una consulta."""
    api_key = os.getenv("NEWS_API")
    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": language,
        "pageSize": page_size,
        "apiKey": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get("articles", [])
        return [
            {
                "title": article["title"],
                "source": article["source"]["name"],
                "url": article["url"],
                "publishedAt": article.get("publishedAt", "")
            }
            for article in articles
        ]
    except requests.exceptions.RequestException as e:
        return [{"error": f"Error fetching news: {str(e)}"}]