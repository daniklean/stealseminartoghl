import requests
from typing import Dict, Any, Tuple
from utils.logger import setup_logger
from models.webinar_registration import WebinarRegistrant
from config.settings import Config

logger = setup_logger("GHLService")

class GHLService:
    """Servicio para interactuar con Go High Level"""
    
    def __init__(self):
        """
        Inicializa el servicio de Go High Level
        
        Args:
            webhook_url (str, optional): URL del webhook de GHL.
            api_key (str, optional): API key para autenticación en GHL.
        """
        self.webhook_url = Config.GHL_WEBHOOK_URL
        self.api_key = Config.GHL_API_KEY
        self.whatsapp_number = Config.WHATSAPP_NUMBER
        self.template_name = Config.TEMPLATE_NAME
    
    def send_webinar_registration(self, registrant: WebinarRegistrant) -> Tuple[bool, Dict, int]:
        """
        Envía la información de registro de webinar a GHL
        
        Args:
            registrant (WebinarRegistrant): Datos del registrante
            
        Returns:
            Tuple[bool, Dict, int]: (éxito, respuesta, código de estado)
        """
        if not self.webhook_url or not self.api_key:
            logger.error("No se puede enviar a GHL: falta webhook_url o api_key")
            return False, {"error": "GHL configuration missing"}, 500
        payload = {
            "phone": registrant.phone,
            "email": registrant.email,
            "firstName": registrant.first_name,
            "lastName": registrant.last_name,
            "tags": registrant.tags,
            "template": {
                "name": self.template_name,
                "language": "es",
                "components": []
            },
            "custom_fields": registrant.custom_fields
        }
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Key": self.api_key
        }
        try:
            logger.info(f"Enviando a GHL: {payload}")
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=headers,
                timeout=40
            )
            response_data = response.json() if response.content else {}
            if response.ok:
                logger.info(f"Respuesta exitosa de GHL: {response_data}")
                return True, response_data, response.status_code
            else:
                logger.error(f"Error de GHL: {response.status_code} - {response.text}")
                return False, response_data, response.status_code
        except Exception as e:
            error_msg = f"Error en la solicitud a GHL: {str(e)}"
            logger.exception(error_msg)
            return False, {"error": error_msg}, 500
