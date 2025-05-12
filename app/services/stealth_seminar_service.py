import requests
import hashlib
import hmac
from typing import Dict, Any, Tuple, Optional
from utils.logger import setup_logger
from config.settings import Config

logger = setup_logger("StealthSeminarService")

class StealthSeminarService:
    """Servicio para interactuar con Stealth Seminar API"""

    def __init__(self, api_key: str = "", webhook_secret: str = ""):
        """
        Inicializa el servicio de Stealth Seminar

        Args:
            api_key (str, optional): API key para Stealth Seminar.
            webhook_secret (str, optional): Secreto para validar webhooks.
        """
        self.api_key = api_key or Config.STEALTH_SEMINAR_API_KEY
        self.webhook_secret = webhook_secret or Config.STEALTH_SEMINAR_WEBHOOK_SECRET
        self.base_url = "https://api.stealthseminar.com/v2"

    def verify_webhook_signature(self, signature: str, payload: bytes) -> bool:
        """
        Verifica la firma del webhook para asegurar que proviene de Stealth Seminar

        Args:
            signature (str): Firma proporcionada en el encabezado HTTP
            payload (bytes): Cuerpo de la solicitud en bytes

        Returns:
            bool: True si la firma es válida, False en caso contrario
        """
        if not self.webhook_secret or not signature:
            logger.warning("No se puede verificar la firma: falta webhook_secret o signature")
            return False

        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_signature, signature)

    def validate_webhook_data(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Valida que los datos del webhook contengan la información necesaria

        Args:
            data (Dict): Datos recibidos del webhook
 
        Returns:
            Tuple[bool, Optional[str]]: (éxito, mensaje de error)
        """
        # Verificar campos requeridos para registro de webinar
        required_fields = ['email', 'first_name', 'last_name']
        missing_fields = [field for field in required_fields if not data.get(field)]
 
        if missing_fields:
            error_msg = f"Faltan campos requeridos: {', '.join(missing_fields)}"
            logger.error(error_msg)
            return False, error_msg

        return True, None

    def register_for_webinar(self, registration_data: Dict[str, Any]) -> Tuple[bool, Dict, int]:
        """
        Registra a un usuario para un webinar en Stealth Seminar

        Args:
            registration_data (Dict): Datos de registro del usuario
        Returns:
            Tuple[bool, Dict, int]: (éxito, respuesta, código de estado)
        """
        if not self.api_key:
            logger.error("No se puede registrar: falta API key de Stealth Seminar")
            return False, {"error": "API key not configured"}, 500

        payload = {
            "api_key": self.api_key,
            "webinar_id": registration_data.get("webinar_id"),
            "email": registration_data.get("email"),
            "first_name": registration_data.get("first_name"),
            "last_name": registration_data.get("last_name"),
            "phone": registration_data.get("phone", ""),
        }
        try:
            logger.info(f"Enviando solicitud de registro a Stealth Seminar: {payload}")
            response = requests.post(
                f"{self.base_url}/webinars/register",
                json=payload,
                timeout=30
            )
            response_data = response.json() if response.content else {}
            if response.ok:
                logger.info(f"Registro exitoso en Stealth Seminar: {response_data}")
                return True, response_data, response.status_code
            else:
                logger.error(f"Error al registrar en Stealth Seminar: {response.status_code} - {response.text}")
                return False, response_data, response.status_code
        except Exception as e:
            error_msg = f"Error en la solicitud a Stealth Seminar: {str(e)}"
            logger.exception(error_msg)
            return False, {"error": error_msg}, 500
    def get_webinar_details(self, webinar_id: str) -> Tuple[bool, Dict, int]:
        """
        Obtiene los detalles de un webinar específico
        Args:
            webinar_id (str): ID del webinar
        Returns:
            Tuple[bool, Dict, int]: (éxito, respuesta, código de estado)
        """
        if not self.api_key:
            logger.error("No se puede obtener detalles: falta API key de Stealth Seminar")
            return False, {"error": "API key not configured"}, 500
        try:
            logger.info(f"Obteniendo detalles del webinar: {webinar_id}")
            response = requests.get(
                f"{self.base_url}/webinars/{webinar_id}",
                params={"api_key": self.api_key},
                timeout=30
            )
            response_data = response.json() if response.content else {}
            if response.ok:
                logger.info(f"Detalles obtenidos exitosamente: {response_data}")
                return True, response_data, response.status_code
            else:
                logger.error(f"Error al obtener detalles: {response.status_code} - {response.text}")
                return False, response_data, response.status_code
        except Exception as e:
            error_msg = f"Error en la solicitud a Stealth Seminar: {str(e)}"
            logger.exception(error_msg)
            return False, {"error": error_msg}, 500
