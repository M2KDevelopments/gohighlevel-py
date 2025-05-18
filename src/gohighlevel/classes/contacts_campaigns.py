from typing import Optional
import requests

from .auth.authdata import Auth

class Campaign:
    """
    Endpoints For Contacts for Campaigns
    Documentation: https://highlevel.stoplight.io/docs/integrations/ecf9b5b45deaf-add-contact-to-campaign
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        self.auth_data = auth_data

    def add(self, contact_id: str, campaign_id: str) -> bool:
        """
        Add Contact to Campaign
        Documentation: https://highlevel.stoplight.io/docs/integrations/ecf9b5b45deaf-add-contact-to-campaign
        https://public-api.gohighlevel.com/#8a506dff-cea3-48bc-909f-4f85a0e8a7be
        
        Args:
            contact_id: The contact ID
            campaign_id: The campaign ID to add the contact to
            
        Returns:
            True if successful
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/campaigns/{campaign_id}",
            json={},
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json().get('succeeded', True)

    def remove(self, contact_id: str, campaign_id: str) -> bool:
        """
        Delete Contact from Campaign
        Documentation: https://highlevel.stoplight.io/docs/integrations/e88fc8bf2a781-remove-contact-from-campaign
        
        Args:
            contact_id: The contact ID
            campaign_id: The campaign ID to remove the contact from
            
        Returns:
            True if successful
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/campaigns/{campaign_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json().get('succeeded', True)

    def remove_all(self, contact_id: str, campaign_id: str) -> bool:
        """
        Delete Contact from all Campaign
        Documentation: https://highlevel.stoplight.io/docs/integrations/e9642e2d8bc8a-remove-contact-from-every-campaign
        
        Args:
            contact_id: The contact ID
            campaign_id: The campaign ID
            
        Returns:
            True if successful
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/campaigns/{campaign_id}/removeAll",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json().get('succeeded', True) 