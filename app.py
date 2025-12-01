from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import os
import time
from datetime import datetime

from config import config
from database import db
from models import *
from auth import auth
from crm import crm
from hunter import hunter
from whatsapp import whatsapp

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

@app.get("/")
async def root():
    status = config.get_status()
    return {
        "app": status["app"],
        "version": status["version"],
        "status": "يعمل" if status["valid"] else "بحاجة لإعدادات",
        "database": "متصلة" if status["database_configured"] else "غير متصلة",
        "search": "مفعل" if status["search_configured"] else "غير مفعل"
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
async def login(user_data: UserLogin):
    result = await auth.authenticate(user_data.username, user_data.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["error"])
    return result

@app.post("/crm/leads")
async def create_lead(lead_data: LeadCreate, user: dict = Depends(get_current_user)):
    result = await crm.create_lead(lead_data, user["user_id"])
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/crm/leads")
async def get_user_leads(status: Optional[str] = None, user: dict = Depends(get_current_user)):
    filters = {}
    if status:
        filters["status"] = status
    leads = await crm.get_leads(user["user_id"], filters)
    return {"leads": leads, "count": len(leads)}

@app.get("/crm/dashboard")
async def get_dashboard(user: dict = Depends(get_current_user)):
    stats = await crm.get_dashboard_stats(user["user_id"])
    return stats

@app.post("/hunt")
async def start_hunt(hunt_data: HuntRequest, background_tasks: BackgroundTasks, user: dict = Depends(get_current_user)):
    if not auth.check_permission(user["role"], "create"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية للبحث")
    
    background_tasks.add_task(hunter.search, hunt_data.query, hunt_data.city, user["user_id"])
    
    return {
        "success": True,
        "message": f"بدأ البحث عن {hunt_data.query} في {hunt_data.city}",
        "job_id": f"hunt_{int(time.time())}"
    }

@app.post("/whatsapp/send")
async def send_whatsapp(message_data: WhatsAppMessage, user: dict = Depends(get_current_user)):
    if not auth.check_permission(user["role"], "create"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية للإرسال")
    
    result = await whatsapp.send_message(message_data.phone, message_data.message, user["user_id"])
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/admin/users")
async def get_all_users(user: dict = Depends(get_current_user)):
    if user["role"] not in ["owner", "admin"]:
        raise HTTPException(status_code=403, detail="صلاحية غير كافية")
    
    try:
        result = db.execute(table="users", operation="select")
        return {"users": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    status = config.validate()
    if not status["valid"]:
        print("⚠️ تحذيرات:")
        for error in status["errors"]:
            print(f"   ❌ {error}")
    
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=config.DEBUG)
