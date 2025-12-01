from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import os
import time
from datetime import datetime
import json
import requests
import re
from supabase import create_client

# ==================== CONFIG ====================
class Config:
    APP_NAME = "Hunter Pro"
    VERSION = "4.0"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()
    
    SERPER_KEYS_STR = os.getenv("SERPER_KEYS", "").strip()
    SERPER_KEYS = [k.strip() for k in SERPER_KEYS_STR.split(",") if k.strip()]
    
    MAX_RESULTS = int(os.getenv("MAX_RESULTS", "50"))
    REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "2.0"))
    
    ROLES = {
        "owner": ["*"],
        "admin": ["view", "create", "edit", "delete", "export"],
        "manager": ["view", "create", "edit"],
        "agent": ["view", "create"],
        "viewer": ["view"]
    }
    
    @classmethod
    def validate(cls):
        errors = []
        warnings = []
        
        if not cls.SUPABASE_URL:
            errors.append("SUPABASE_URL مطلوب")
        elif not cls.SUPABASE_URL.startswith("https://"):
            warnings.append("SUPABASE_URL يجب أن يبدأ بـ https://")
        
        if not cls.SUPABASE_KEY:
            errors.append("SUPABASE_KEY مطلوب")
        
        if not cls.SERPER_KEYS:
            errors.append("SERPER_KEYS مطلوب (مفصولة بفاصلة)")
        elif len(cls.SERPER_KEYS) < 2:
            warnings.append("يفضل إضافة أكثر من مفتاح Serper")
        
        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}
    
    @classmethod
    def get_status(cls):
        validation = cls.validate()
        return {
            "app": cls.APP_NAME,
            "version": cls.VERSION,
            "database_configured": bool(cls.SUPABASE_URL and cls.SUPABASE_KEY),
            "search_configured": len(cls.SERPER_KEYS) > 0,
            "keys_count": len(cls.SERPER_KEYS),
            "valid": validation["valid"],
            "issues": validation["errors"] + validation["warnings"]
        }

config = Config()

# ==================== DATABASE ====================
class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.client = None
        self.connected = False
        
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            print("⚠️ إعدادات قاعدة البيانات غير مكتملة")
            return
        
        try:
            self.client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
            test = self.client.table("users").select("count", count="exact").limit(1).execute()
            self.connected = True
            print("✅ قاعدة البيانات متصلة بنجاح")
        except Exception as e:
            print(f"❌ فشل الاتصال بقاعدة البيانات: {e}")
            self.connected = False
    
    def test_connection(self):
        if not self.client:
            return False
        try:
            result = self.client.table("users").select("count", count="exact").limit(1).execute()
            return True
        except:
            return False
    
    def execute(self, table: str, operation: str, **kwargs):
        if not self.connected:
            raise ConnectionError("قاعدة البيانات غير متصلة")
        
        try:
            table_ref = self.client.table(table)
            
            if operation == "select":
                return table_ref.select(**kwargs).execute()
            elif operation == "insert":
                return table_ref.insert(kwargs.get("data")).execute()
            elif operation == "update":
                return table_ref.update(kwargs.get("data")).eq("id", kwargs.get("id")).execute()
            elif operation == "delete":
                return table_ref.delete().eq("id", kwargs.get("id")).execute()
            else:
                raise ValueError(f"عملية غير معروفة: {operation}")
                
        except Exception as e:
            print(f"❌ خطأ في قاعدة البيانات: {e}")
            raise

db = Database()

# ==================== MODELS ====================
class UserLogin:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class HuntRequest:
    def __init__(self, query: str, city: str, max_results: int = 20):
        self.query = query
        self.city = city
        self.max_results = max_results

class WhatsAppMessage:
    def __init__(self, phone: str, message: str):
        self.phone = phone
        self.message = message

# ==================== AUTH ====================
import jwt

class AuthSystem:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET", "change-this-in-production")
        self.algorithm = "HS256"
    
    async def authenticate(self, username: str, password: str):
        try:
            result = db.execute(
                table="users",
                operation="select",
                data={"username": username, "password": password}
            )
            
            if result.data and len(result.data) > 0:
                user = result.data[0]
                if user.get("is_active", True):
                    token = self.create_token(user["id"], user["role"])
                    return {
                        "success": True,
                        "user": {
                            "id": user["id"],
                            "username": user["username"],
                            "role": user["role"],
                            "permissions": config.ROLES.get(user["role"], [])
                        },
                        "token": token
                    }
            
            return {"success": False, "error": "بيانات الدخول غير صحيحة"}
            
        except Exception as e:
            print(f"خطأ في المصادقة: {e}")
            return {"success": False, "error": "خطأ في الخادم"}
    
    def create_token(self, user_id: str, role: str):
        payload = {
            "user_id": user_id,
            "role": role,
            "exp": datetime.utcnow() + time.timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def check_permission(self, user_role: str, required_permission: str):
        role_permissions = config.ROLES.get(user_role, [])
        if "*" in role_permissions:
            return True
        return required_permission in role_permissions

auth = AuthSystem()

# ==================== HUNTER ====================
class Hunter:
    def __init__(self):
        self.current_key_index = 0
        self.request_count = 0
        self.last_request = time.time()
    
    def get_next_key(self):
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
    
    def analyze_content(self, text: str):
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
    
    async def search(self, query: str, city: str, user_id: str):
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

# ==================== WHATSAPP ====================
class WhatsAppManager:
    def __init__(self):
        self.twilio_sid = os.getenv("TWILIO_SID")
        self.twilio_token = os.getenv("TWILIO_TOKEN")
        self.whatsapp_number = os.getenv("WHATSAPP_NUMBER")
        self.enabled = bool(self.twilio_sid and self.twilio_token and self.whatsapp_number)
    
    async def send_message(self, phone: str, message: str, user_id: str):
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

whatsapp = WhatsAppManager()

# ==================== FASTAPI APP ====================
app = FastAPI(
    title=config.APP_NAME,
    version=config.VERSION,
    docs_url="/docs" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = auth.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="توكن غير صالح")
    return payload

# ==================== ROUTES ====================
@app.get("/")
async def root():
    status = config.get_status()
    return {
        "app": status["app"],
        "version": status["version"],
        "status": "يعمل" if status["valid"] else "بحاجة لإعدادات",
        "database": "متصلة" if status["database_configured"] else "غير متصلة",
        "search": "مفعل" if status["search_configured"] else "غير مفعل",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    db_status = db.test_connection() if hasattr(db, 'client') and db.client else False
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "search_keys": len(config.SERPER_KEYS),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/auth/login")
async def login(user_data: dict):
    username = user_data.get("username")
    password = user_data.get("password")
    
    if not username or not password:
        raise HTTPException(status_code=400, detail="اسم المستخدم وكلمة المرور مطلوبان")
    
    result = await auth.authenticate(username, password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["error"])
    return result

@app.post("/hunt")
async def start_hunt(hunt_data: dict, background_tasks: BackgroundTasks, user: dict = Depends(get_current_user)):
    if not auth.check_permission(user["role"], "create"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية للبحث")
    
    query = hunt_data.get("query")
    city = hunt_data.get("city")
    
    if not query or not city:
        raise HTTPException(status_code=400, detail="البحث والمدينة مطلوبان")
    
    background_tasks.add_task(hunter.search, query, city, user["user_id"])
    
    return {
        "success": True,
        "message": f"بدأ البحث عن {query} في {city}",
        "job_id": f"hunt_{int(time.time())}"
    }

@app.post("/whatsapp/send")
async def send_whatsapp(message_data: dict, user: dict = Depends(get_current_user)):
    if not auth.check_permission(user["role"], "create"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية للإرسال")
    
    phone = message_data.get("phone")
    message = message_data.get("message")
    
    if not phone or not message:
        raise HTTPException(status_code=400, detail="رقم الهاتف والرسالة مطلوبان")
    
    result = await whatsapp.send_message(phone, message, user["user_id"])
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/leads")
async def get_leads(user: dict = Depends(get_current_user)):
    try:
        result = db.execute(
            table="leads",
            operation="select",
            data={"created_by": user["user_id"]}
        )
        return {"success": True, "leads": result.data, "count": len(result.data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats(user: dict = Depends(get_current_user)):
    try:
        result = db.execute(
            table="leads",
            operation="select",
            data={"created_by": user["user_id"]}
        )
        
        leads = result.data
        total = len(leads)
        new = len([l for l in leads if l.get("status") == "new"])
        
        return {
            "success": True,
            "stats": {
                "total_leads": total,
                "new_leads": new,
                "converted": len([l for l in leads if l.get("status") == "converted"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== RENDER SPECIFIC ====================
# هذا الكود مهم للـ Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=config.DEBUG
    )
