import os
import requests
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class LLMAgent(ABC):
    """Clase base para todos los agentes LLM"""
    
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
    
    @abstractmethod
    def analyze(self, data: Dict) -> Dict:
        pass
    
    def call_openai(self, prompt: str, system_message: str = None) -> str:
        """Llama a la API de OpenAI"""
        if not self.openai_key:
            return "Error: OpenAI API key no configurada"
            
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "gpt-4",
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error llamando a OpenAI: {str(e)}"
    
    def call_deepseek(self, prompt: str, system_message: str = None) -> str:
        """Llama a la API de DeepSeek"""
        if not self.deepseek_key:
            return "Error: DeepSeek API key no configurada"
            
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.deepseek_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error llamando a DeepSeek: {str(e)}"
    
    def call_mistral(self, prompt: str, system_message: str = None) -> str:
        """Llama a la API de Mistral"""
        if not self.mistral_key:
            return "Error: Mistral API key no configurada"
            
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.mistral_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "mistral-medium",
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error llamando a Mistral: {str(e)}"