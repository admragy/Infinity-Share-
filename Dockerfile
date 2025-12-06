FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# إنشاء مجلد العمل
WORKDIR /app

# تثبيت المكتبات الأساسية
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المكتبات
COPY requirements.txt .

# تثبيت المكتبات Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# نسخ الملفات
COPY . .

# فتح المنفذ
EXPOSE 8000

# أمر التشغيل
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
