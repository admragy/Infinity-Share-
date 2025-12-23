import uvicorn
import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, select, func
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
import logging

# تهيئة logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Brilliox")

# تحميل الإعدادات البيئية
load_dotenv()

# =============================================================================
# DATABASE & AUTH SETUP
# =============================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./brilliox.db")
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
ALGORITHM = "HS256"
JWT_EXPIRATION_DAYS = int(os.getenv("JWT_EXPIRATION_DAYS", "7"))

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    status = Column(String, default="جديد")
    ai_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(request: Request) -> Optional[str]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

# =============================================================================
# FASTAPI APP
# =============================================================================
app = FastAPI(
    title="Brilliox Ultimate",
    version="5.0-Premium",
    description="AI-Powered CRM System"
)

app.mount("/static", StaticFiles(directory="ai.markitng-repo/static"), name="static")
templates = Jinja2Templates(directory="ai.markitng-repo/templates")

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting Brilliox Ultimate...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.username == "admin"))
        if not result.scalar():
            hashed_pw = pwd_context.hash("admin123")
            admin = User(username="admin", hashed_password=hashed_pw)
            db.add(admin)
            await db.commit()
            logger.info("✅ Admin created (admin/admin123)")
    
    logger.info("✅ System ready!")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar()
    
    if not user or not pwd_context.verify(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": {}, "error": "بيانات دخول خاطئة"}
        )
    
    token = create_access_token({"sub": user.username})
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=JWT_EXPIRATION_DAYS * 24 * 60 * 60
    )
    return response

@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("access_token")
    return response

@app.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not user:
        return RedirectResponse("/login")
    
    total_contacts = await db.scalar(select(func.count(Contact.id)))
    recent_contacts = await db.execute(
        select(Contact).order_by(Contact.created_at.desc()).limit(5)
    )
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "total_contacts": total_contacts or 0,
        "recent_contacts": recent_contacts.scalars().all()
    })

@app.post("/api/ask_brain")
async def ask_brain(
    prompt: str = Form(...),
    context: str = Form("general"),
    user: str = Depends(get_current_user)
):
    if not user:
        raise HTTPException(status_code=401)
    
    # يجب استيراد brain من app.brain
    from app.brain import brain
    answer = await brain.think(prompt, context)
    return JSONResponse({"answer": answer})

@app.post("/api/contacts/add")
async def add_contact(
    name: str = Form(...),
    phone: str = Form(None),
    email: str = Form(None),
    user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401)
    
    contact = Contact(name=name, phone=phone, email=email)
    db.add(contact)
    await db.commit()
    return JSONResponse({"success": True})

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
