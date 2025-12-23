import platform
import os
from typing import Dict, Any

class PlatformCompatibilityService:
    def get_system_info(self) -> Dict[str, Any]:
        """الحصول على معلومات النظام"""
        info = {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "os": "unknown",
                "device": "unknown"
            },
            "environment": {
                "python_version": platform.python_version(),
                "user": os.getenv("USER")
            }
        }

        if info["platform"]["system"] == "Windows":
            info["platform"]["os"] = "windows"
            info["platform"]["device"] = "desktop"
        elif info["platform"]["system"] == "Darwin":
            info["platform"]["os"] = "macos"
            info["platform"]["device"] = "desktop"
        elif info["platform"]["system"] == "Linux":
            info["platform"]["os"] = "linux"
            if "android" in info["platform"]["release"].lower():
                info["platform"]["device"] = "mobile"
            elif "raspberry" in info["platform"]["machine"].lower():
                info["platform"]["device"] = "raspberry_pi"
            else:
                info["platform"]["device"] = "server"
        
        return info

platform_service = PlatformCompatibilityService()
