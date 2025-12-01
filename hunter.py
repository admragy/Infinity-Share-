import requests
import json
import time
import re
from typing import List, Dict, Optional
from datetime import datetime
from config import config
from database import db

class Hunter:
    def __init__(self):
        self.current_key_index = 0
        self.request_count = 0
        self.last_request = time.time()
    
    def get_next_key(self) -> Optional[str]:
        if not config.SERPER_KEYS:
            return None
        key = config.SERPER_KEYS[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(config.SERPER_KEYS)
        return key
    
    def safe_delay(self):
        elapsed = time.time() - self.last_request
        if elapsed < config.REQUEST_DELAY:
            time.sleep(config.REQUEST_DELAY - elapsed)
        self.last_request = time.time()
    
    def analyze_content(self, text: str) -> Dict:
        text_lower = text.lower()
        
        seller_words = ["للبيع", "for sale", "سمسار", "وسيط", "شركة", "مؤسسة"]
        seller_count = sum(1 for word in seller_words if word in text_lower)
        
        buyer_words = ["مطلوب", "محتاج", "عايز", "أبحث", "شراء", "buying", "wanted"]
        buyer_count = sum(1 for word in buyer_words if word in text_lower)
        
        phones = re.findall(r'(01[0125][0-9]{8})', text)
        
        score = buyer_count - seller_count
        quality = "good" if score > 0 else "bad" if score < 0 else "neutral"
        
        return {
            "seller_score": seller_count,
            "buyer_score": buyer_count,
            "total_score": score,
            "quality": quality,
            "phones": list(set(phones)),
            "has_phone": len(phones) > 0
        }
    
    async def search(self, query: str, city: str, user_id: str) -> Dict:
        if not config.SERPER_KEYS:
            return {"success": False, "error": "لا توجد مفاتيح بحث"}
        
        api_key = self.get_next_key()
        if not api_key:
            return {"success": False, "error": "مفتاح بحث غير صالح"}
        
        self.safe_delay()
        
        search_query = f'"{query}" "{city}"'
        payload = json.dumps({
            "q": search_query,
            "num": min(config.MAX_RESULTS, 50),
            "gl": "eg",
            "hl": "ar",
            "tbs": "qdr:w"
        })
        
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
        
        try:
            print(f"🔍 يبحث عن: {query} في {city}")
            response = requests.post("https://google.serper.dev/search", headers=headers, data=payload, timeout=30)
            
            if response.status_code == 429:
                return {"success": False, "error": "تم تجاوز الحد المسموح، حاول لاحقاً"}
            if response.status_code != 200:
                return {"success": False, "error": f"خطأ في API: {response.status_code}"}
            
            data = response.json()
            results = data.get("organic", [])
            found_leads = []
            
            for item in results:
                content = f"{item.get('title', '')} {item.get('snippet', '')}"
                analysis = self.analyze_content(content)
                
                if analysis["quality"] == "good" and analysis["has_phone"]:
                    for phone in analysis["phones"][:2]:
                        lead_data = {
                            "phone": phone,
                            "name": None,
                            "source": f"hunter:{query}",
                            "notes": f"المصدر: {item.get('link', '')}\n{content[:200]}...",
                            "created_by": user_id,
                            "created_at": datetime.now().isoformat()
                        }
                        
                        try:
                            db.execute(table="leads", operation="insert", data=lead_data)
                            found_leads.append(phone)
                        except:
                            continue
            
            return {
                "success": True,
                "query": query,
                "city": city,
                "total_results": len(results),
                "found_leads": len(found_leads),
                "leads": found_leads[:10]
            }
            
        except requests.exceptions.Timeout:
            return {"success": False, "error": "انتهت مهلة البحث"}
        except Exception as e:
            return {"success": False, "error": f"خطأ في البحث: {str(e)}"}

hunter = Hunter()
