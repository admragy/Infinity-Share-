import jwt
import datetime
import os
from typing import Dict, Optional
from config import config
from database import db

class AuthSystem:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET", "change-this-in-production")
        self.algorithm = "HS256"
    
    async def authenticate(self, username: str, password: str) -> Optional[Dict]:
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
    
    def create_token(self, user_id: str, role: str) -> str:
        payload = {
            "user_id": user_id,
            "role": role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def check_permission(self, user_role: str, required_permission: str) -> bool:
        role_permissions = config.ROLES.get(user_role, [])
        if "*" in role_permissions:
            return True
        return required_permission in role_permissions

auth = AuthSystem()
