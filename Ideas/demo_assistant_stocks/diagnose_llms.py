import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()

def diagnose_llms():
    """Diagnostica problemas con las APIs de LLM"""
    print("🔍 Diagnóstico de APIs LLM")
    print("=" * 50)
    
    # Verificar claves en .env
    openai_key = os.getenv("OPENAI_API_KEY")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    mistral_key = os.getenv("MISTRAL_API_KEY")
    
    print("📋 Claves API encontradas:")
    print(f"   OpenAI: {'✅' if openai_key else '❌'} {'(Configurada)' if openai_key else '(No configurada)'}")
    print(f"   DeepSeek: {'✅' if deepseek_key else '❌'} {'(Configurada)' if deepseek_key else '(No configurada)'}")
    print(f"   Mistral: {'✅' if mistral_key else '❌'} {'(Configurada)' if mistral_key else '(No configurada)'}")
    
    if not any([openai_key, deepseek_key, mistral_key]):
        print("\n❌ No hay claves API configuradas.")
        print("💡 Agrega al menos una clave API a tu archivo .env")
        return
    
    # Probar conectividad básica
    print("\n🌐 Probando conectividad...")
    
    test_endpoints = [
        ("OpenAI", "https://api.openai.com/v1/models", openai_key),
        ("DeepSeek", "https://api.deepseek.com/v1/models", deepseek_key),
        ("Mistral", "https://api.mistral.ai/v1/models", mistral_key),
    ]
    
    for name, url, key in test_endpoints:
        if not key:
            print(f"   {name}: ⚠️ Sin clave, omitiendo...")
            continue
            
        try:
            headers = {"Authorization": f"Bearer {key}"}
            start_time = time.time()
            response = requests.get(url, headers=headers, timeout=10)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                print(f"   {name}: ✅ Conectado ({elapsed:.1f}s)")
            elif response.status_code == 401:
                print(f"   {name}: ❌ Clave API inválida")
            elif response.status_code == 429:
                print(f"   {name}: ⚠️ Límite de tasa alcanzado")
            else:
                print(f"   {name}: ❌ Error {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   {name}: ⏰ Timeout (más de 10s)")
        except Exception as e:
            print(f"   {name}: ❌ Error: {e}")
    
    print("\n💡 Recomendaciones:")
    if not any([openai_key, deepseek_key, mistral_key]):
        print("   1. Configura al menos una clave API en .env")
    else:
        print("   1. Si hay timeouts, prueba aumentar el timeout en el código")
        print("   2. Verifica tu conexión a internet")
        print("   3. Para claves inválidas, genera nuevas claves en los portales respectivos")
    
    print("   4. El sistema funcionará con análisis básico si los LLMs fallan")

if __name__ == "__main__":
    diagnose_llms()