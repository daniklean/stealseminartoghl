from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class WebinarRegistrant:
    """Modelo para representar un registrante de webinar"""
    email: str
    first_name: str
    last_name: str
    phone: str
    webinar_id: str
    registration_date: datetime = field(default_factory=datetime.now)
    ip_address: Optional[str] = None
    custom_fields: Dict[str, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convierte el objeto a un diccionario"""
        return {
            "email": self.email,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "phone": self.phone,
            "webinarId": self.webinar_id,
            "registrationDate": self.registration_date.isoformat(),
            "ipAddress": self.ip_address,
            "customFields": self.custom_fields,
            "tags": self.tags
        }
    
    @classmethod
    def from_stealth_seminar_data(cls, data: Dict) -> 'WebinarRegistrant':
        """
        Crea una instancia desde los datos recibidos de Stealth Seminar
        
        Args:
            data (Dict): Datos recibidos del webhook de Stealth Seminar
            
        Returns:
            WebinarRegistrant: Nueva instancia con los datos procesados
        """
        return cls(
            email=data.get('email', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            phone=data.get('phone', ''),
            webinar_id=data.get('webinar_id', ''),
            ip_address=data.get('ip_address', None),
            registration_date=datetime.now(),
            tags=["webinar_registrant"],
            custom_fields={
                "webinar_name": data.get('webinar_name', ''),
                "source": "stealth_seminar",
            }
        )
