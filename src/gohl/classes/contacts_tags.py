from typing import Optional, List, Dict, Any
import requests

from .auth.authdata import Auth

class Tag:
    """
    Endpoints For Contacts Tags
    https://highlevel.stoplight.io/docs/integrations/c9bbad7cdacf5-add-tags
    https://public-api.gohighlevel.com/#dbb4ae8d-1fcc-45ce-a3f8-34fafe771e90
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        self.auth_data = auth_data

    def add(self, contact_id: str, tags: List[str]) -> List[str]:
        """
        Add tag to contact. For both GHL App and API
        Documentation - https://highlevel.stoplight.io/docs/integrations/6015cf49a7ae8-get-appointments-for-contact
        Documentation - https://public-api.gohighlevel.com/#2b4583f4-d525-43a3-89dc-0034e864df02
        
        Args:
            contact_id: The contact ID
            tags: List of tags to add
            
        Returns:
            List of tags
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/tags/",
            json={'tags': tags},
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['tags']

    def remove(self, contact_id: str, tags: List[str]) -> Dict[str, Any]:
        """
        Remove Tags from contact. For both GHL App and API
        Documentation - https://highlevel.stoplight.io/docs/integrations/e5d269b7415bf-remove-tags
        Documentation - https://public-api.gohighlevel.com/#14572da1-a341-42dc-a42c-ac0742d6178e
        
        Args:
            contact_id: The contact ID
            tags: List of tags to remove
            
        Returns:
            Response data
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/tags/",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 