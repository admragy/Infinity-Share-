import json
import datetime
import os

LOG_FILE = "logs.json"

class Logger:
    @staticmethod
    def log(event: str, user_id: str, details: dict = None):
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "event": event,
            "user_id": user_id,
            "details": details or {}
        }
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        logs.append(entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs[-500:], f, ensure_ascii=False, indent=2)

logger = Logger()
