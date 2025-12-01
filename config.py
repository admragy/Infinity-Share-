import os

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
