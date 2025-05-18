from typing import Optional, Dict, Any
import requests

from .auth.authdata import Auth

class Email:
    def __init__(self, auth_data: Optional[Auth] = None):
        self.auth_data = auth_data

    def verify(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify Email
        Documentation - https://highlevel.stoplight.io/docs/integrations/47a095a7cf1af-email-verification
        
        Args:
            params: Dictionary containing email verification parameters
            
        Returns:
            Dictionary containing the email verification response
        """
        headers = self.auth_data.headers if self.auth_data else None
        response = requests.post(
            f"{self.auth_data.baseurl}/emails/verify" if self.auth_data else "",
            json=params,
            headers=headers
        )
        response.raise_for_status()
        return response.json() 