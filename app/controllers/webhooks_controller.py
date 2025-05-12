from flask import Blueprint, request, jsonify
from utils.logger import setup_logger
from models.webinar_registration import WebinarRegistrant
from services.stealth_seminar_service import StealthSeminarService
from services.ghl_service import GHLService
from typing import Dict, Any

webhook_bp = Blueprint('webhook', __name__, url_prefix='/api/webhooks')

logger = setup_logger("WebhookController")

stealth_service = StealthSeminarService()
ghl_service = GHLService()

@webhook_bp.route('/stealth-seminar', methods=['POST'])
def handle_stealth_seminar_webhook():
    """
    Manejador del webhook de Stealth Seminar
    
    Este endpoint recibe notificaciones de Stealth Seminar cuando
    un usuario se registra para un webinar.
    """
    try:
        if not request.is_json:
            logger.error("Solicitud no contiene datos JSON válidos")
            return jsonify({
                "status": "error",
                "message": "Se requieren datos JSON"
            }), 400
        
        data: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
        
        logger.info(f"Datos recibidos de Stealth Seminar: {data}")
        
        if not data:
            logger.error("Datos JSON están vacíos")
            return jsonify({
                "status": "error",
                "message": "No se recibieron datos"
            }), 400
        
        event_type_top = data.get('event', '').lower()
        event_type_nested = data.get('data', {}).get('event', '').lower()
        
        logger.debug(f"Evento nivel superior: {event_type_top}, Evento anidado: {event_type_nested}")
        
        if event_type_top == 'ping' or event_type_nested == 'ping':
            challenge = data.get('challenge')
            if challenge:
                return challenge
            else:
                return jsonify({
                    "status": "error",
                    "message": "No se encontró challenge en el ping"
                }), 400
        

        if (event_type_top in ['register', 'they register'] or 
            event_type_nested in ['register', 'they register']):
            
            registrant_data = data.get('data', {}) if 'data' in data else data
            
            phone = (registrant_data.get('phone', '') or 
                    registrant_data.get('sms_number', '') or 
                    registrant_data.get('phone_number', ''))
            
            if not phone:
                error_msg = f"Número de teléfono no encontrado en los datos: {registrant_data}"
                logger.error(error_msg)
                return jsonify({
                    "status": "error",
                    "message": error_msg,
                    "required_format": "10 dígitos (ej: 3528093144) o E.164 (ej: +13528093144)"
                }), 400

            try:
                registrant = WebinarRegistrant.from_stealth_seminar_data(registrant_data)
            except ValueError as ve:
                logger.error(f"Error al crear registrante: {ve}")
                return jsonify({
                    "status": "error",
                    "message": str(ve)
                }), 400
            
            success, response_data, status_code = ghl_service.send_webinar_registration(registrant)
            
            if success:
                logger.info(f"Registro procesado exitosamente para {registrant.email}")
                return jsonify({
                    "status": "success",
                    "message": "Registro procesado correctamente",
                    "ghl_response": response_data,
                    "contact": registrant.phone
                }), 200
            else:
                logger.error(f"Error al procesar registro: {response_data}")
                return jsonify({
                    "status": "error",
                    "message": "Error al enviar datos a GHL",
                    "error": response_data
                }), status_code
        else:
            logger.warning(f"Evento no manejado. Top: {event_type_top}, Nested: {event_type_nested}")
            return jsonify({
                "status": "warning",
                "message": f"Evento {event_type_top} ({event_type_nested}) no manejado"
            }), 200

    except Exception as e:
        logger.exception(f"Error en el webhook de Stealth Seminar: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Error interno del servidor",
            "error": str(e)
        }), 500

@webhook_bp.route('/test', methods=['GET'])
def test_webhook():
    """Endpoint de prueba para verificar que el servicio está funcionando"""
    return jsonify({
        "status": "success",
        "message": "Webhook service is running"
    }), 200

