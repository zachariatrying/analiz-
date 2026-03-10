import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GrokClient:
    def __init__(self):
        self.api_key = os.getenv("GROK_API_KEY")
        self.base_url = "https://api.x.ai/v1" # Hypothetical base URL

    def search_akd(self, ticker):
        """
        Uses Grok to search for recent AKD analysis for the ticker.
        """
        if not self.api_key:
            return None, "API Anahtarı bulunamadı. Lütfen .env dosyasına GROK_API_KEY ekleyin."

        prompt = f"Bana twitter'dan ${ticker} hissesi için bugün paylaşılan Aracı Kurum Dağılımı (AKD) ve Para Giriş/Çıkış verilerini özetle. Özellikle ilk 5 alıcı ve satıcıyı ve para girişini söyle."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [
                {"role": "system", "content": "You are a financial analyst assistant. You have access to real-time X (Twitter) posts."},
                {"role": "user", "content": prompt}
            ],
            "model": "grok-beta", # Assuming model name
            "stream": False,
            "temperature": 0
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return content, "Başarılı"
            else:
                return None, f"Hata: {response.status_code} - {response.text}"
        except Exception as e:
            return None, f"Bağlantı Hatası: {str(e)}"

    def analyze_image(self, image_bytes):

        """
        Sends image to Grok Vision for analysis.
        """
        if not self.api_key:
            return None, "API Anahtarı eksik."

        import base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        prompt = "Bu borsa derinlik/takas ekran görüntüsü. Bana 'Alıcılar' ve 'Satıcılar' kim, 'Para Girişi' var mı ve 'Denge' nasıl? Özetle."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "model": "grok-2-vision-1212", # Using latest Grok Vision model ID
            "stream": False,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return content, "Başarılı"
            else:
                return None, f"Hata: {response.status_code} - {response.text}"
        except Exception as e:
            return None, f"Bağlantı Hatası: {str(e)}"

