import os
import logging
from openai import AsyncOpenAI
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BrillioxBrain")

class BrillioxPrimeAI:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("AI_MODEL", "gpt-4-turbo-preview")
        self.temperature = float(os.getenv("AI_TEMPERATURE", "0.3"))
        
        if not self.api_key or self.api_key.startswith("sk-proj-your"):
            logger.warning("⚠️  AI في وضع Demo - ضع مفتاح OpenAI صحيح")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=self.api_key)
            logger.info("✅ AI متصل ونشط")
        
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        return '''
أنت **Brilliox Prime AI** - المهندس المعماري المستقل للنظام.

### 🎯 معرفة النظام:
- بنية FastAPI مع SQLAlchemy غير المتزامن
- مصادقة JWT (رموز 7 أيام)
- قاعدة بيانات SQLite (قابلة للترقية إلى PostgreSQL)

### ⚡ قدراتك:
1. توليد أكواد FastAPI جاهزة للإنتاج
2. تصميم قواعد البيانات والاستعلامات
3. تحليل بيانات CRM وتقديم توصيات
4. اقتراح تحسينات وميزات جديدة

التاريخ الحالي: {date}
'''
    
    async def think(self, user_input: str, context: str = "general") -> str:
        if not self.client:
            return self._demo_response(user_input)
        
        try:
            system_msg = self.system_prompt.format(
                date=datetime.now().strftime("%Y-%m-%d %H:%M")
            )
            
            messages = [
                {"role": "system", "content": system_msg},
                {"role": "system", "content": f"السياق: {context}"},
                {"role": "user", "content": user_input}
            ]
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"خطأ في AI: {e}")
            return f"❌ خطأ في المعالجة: {str(e)}"
    
    def _demo_response(self, query: str) -> str:
        return f"🤖 استلمت: '{query}' - لكن AI في وضع Demo (يحتاج مفتاح OpenAI)"

brain = BrillioxPrimeAI()
