import os
from supabase import create_client, Client
from config import config

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.client: Client = None
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
