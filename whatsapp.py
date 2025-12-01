import os
import requests
from typing import Dict
from config import config

class WhatsAppManager:
    def __init__(self):
        self.twilio_sid = os.getenv("TWILIO_SID")
        self.twilio_token = os.getenv("TWILIO_TOKEN")
        self.whatsapp_number = os.getenv("WHATSAPP_NUMBER")
        self.enabled = bool(self.twilio_sid and self.twilio_token and self.whatsapp_number)
    
    async def send_message(self, phone: str, message: str, user_id: str) -> Dict:
        if not self.enabled:
            return {"success": False, "error": "خدمة الواتساب غير مفعلة"}
        
        if not phone.startswith("+"):
            phone = f"+20{phone[1:]}" if phone.startswith("0") else f"+20{phone}"
        
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_sid}/Messages.json"
        
        data = {
            'From': f'whatsapp:{self.whatsapp_number}',
            'To': f'whatsapp:{phone}',
            'Body': message
        }
        
        try:
            response = requests.post(url, data=data, auth=(self.twilio_sid, self.twilio_token), timeout=30)
            
            if response.status_code == 201:
                return {
                    "success": True,
                    "message_id": response.json().get('sid'),
                    "status": "sent",
                    "to": phone
                }
            else:
                return {"success": False, "error": f"خطأ في الإرسال: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": f"فشل الإرسال: {str(e)}"}
    
    def get_templates(self) -> Dict:
        return {
            "welcome": "مرحباً {name} 👋\nشكراً لاهتمامك بـ {product}\nكيف يمكننا مساعدتك؟",
            "followup": "أهلاً {name} 🌟\nنأمل أن تكون الأمور على ما يرام\nهل تحتاج لمزيد من المعلومات؟",
            "offer": "عروض حصرية لك {name}! 🎁\nخصم {discount}% لمدة محدودة"
        }

whatsapp = WhatsAppManager()
