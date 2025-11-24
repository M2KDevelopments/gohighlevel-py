from typing import Optional, List, Dict, Any
import requests

from .auth.authdata import Auth

class Appointment:
    """
    Endpoints For Appointments
    https://highlevel.stoplight.io/docs/integrations/6015cf49a7ae8-get-appointments-for-contact
    https://public-api.gohighlevel.com/#dbf523a3-c344-44cc-adf7-34b68c40dc81
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        self.auth_data = auth_data

    def get(self, contact_id: str) -> List[Dict[str, Any]]:
        """
        Get appointments for contact. For both GHL App and API
        Documentation - https://highlevel.stoplight.io/docs/integrations/6015cf49a7ae8-get-appointments-for-contact
        Documentation - https://public-api.gohighlevel.com/#af42b0d8-f002-4d09-a1a9-f860d653127f
        
        Args:
            contact_id: The contact ID to get appointments for
            
        Returns:
            List of appointments
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/appointments/",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['events'] 