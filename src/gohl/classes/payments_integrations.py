"""Payment Integrations functionality for GoHighLevel API.

This module provides the PaymentIntegrations class for managing payment integrations
in GoHighLevel, including retrieving available payment providers.
"""

from typing import Dict, List, Optional
import requests

from .auth.authdata import Auth


class PaymentIntegrations:
    """
    Endpoints For Payment Integrations
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the PaymentIntegrations class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_providers(self) -> List[Dict]:
        """Get available payment providers.
        
        Returns:
            List[Dict]: List of payment providers with their details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/payments/integrations/providers",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['providers'] 