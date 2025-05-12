import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración global de la aplicación"""

    FLASK_PORT = int(os.getenv("FLASK_PORT", 5001))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    GHL_WEBHOOK_URL = os.getenv(
        "GHL_WEBHOOK_URL", 
        "https://services.leadconnectorhq.com/hooks/TBRqtQPrHGgg9lCBNCxM/webhook-trigger/e1f13c38-edb1-49d1-9136-77edd699ff96"
    )
    GHL_API_KEY = os.getenv("GHL_API_KEY")

    WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+13528093144")
    TEMPLATE_NAME = os.getenv("TEMPLATE_NAME", "upsell_m2_mes_mujer_2025")

    STEALTH_SEMINAR_API_KEY = os.getenv("STEALTH_SEMINAR_API_KEY")
    STEALTH_SEMINAR_WEBHOOK_SECRET = os.getenv("STEALTH_SEMINAR_WEBHOOK_SECRET")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
