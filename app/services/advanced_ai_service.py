import os
import logging
from typing import List, Dict, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("AdvancedAIService")

class AdvancedAIService:
    def __init__(self):
        self.models = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "groq": os.getenv("GROQ_API_KEY"),
            "google": os.getenv("GOOGLE_API_KEY"),
            # "ollama": os.getenv("USE_OLLAMA") == "true"
        }
        self.default_model = "openai"
        self.openai_client = AsyncOpenAI(api_key=self.models.get("openai"))

    async def generate(self, prompt: str, system_prompt: str, temperature: float, max_tokens: int, model_name: str = None) -> str:
        """توليد رد ذكي باستخدام نموذج محدد أو الافتراضي"""
        model_to_use = model_name if model_name and model_name in self.models else self.default_model
        
        if model_to_use == "openai" and self.models.get("openai"):
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                response = await self.openai_client.chat.completions.create(
                    model=os.getenv("AI_MODEL", "gpt-4-turbo-preview"),
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"OpenAI Error: {e}")
                return f"❌ خطأ في OpenAI: {str(e)}"
        
        # هنا يمكن إضافة منطق Groq و Google Gemini و Ollama
        
        return f"🤖 AI في وضع Demo: استلمت طلب توليد لـ: {prompt[:30]}..."

    async def generate_bulk(self, prompts_list: List[str]) -> List[str]:
        """توليد رسائل متعددة"""
        results = []
        for prompt in prompts_list:
            results.append(await self.generate(prompt, "أنت خبير تسويق رقمي", 0.7, 500))
        return results

    async def test_models(self) -> Dict[str, str]:
        """اختبار حالة جميع النماذج"""
        status = {}
        for name, key in self.models.items():
            if key and not key.startswith("sk-proj-your"):
                status[name] = "Active"
            else:
                status[name] = "Inactive/Demo"
        return status

advanced_ai_service = AdvancedAIService()
