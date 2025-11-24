"""Payment Custom Providers functionality for GoHighLevel API.

This module provides the PaymentCustomProviders class for managing custom payment providers
in GoHighLevel.
"""

from typing import Dict, List, Optional
import requests

from .auth.authdata import Auth


class PaymentCustomProviders:
    """
    Endpoints For Payment Custom Providers
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the PaymentCustomProviders class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(self, location_id: str) -> List[Dict]:
        """Get all custom payment providers for a location.
        
        Args:
            location_id (str): The ID of the location
            
        Returns:
            List[Dict]: List of custom payment providers
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/payments/custom-providers",
            params={'locationId': location_id},
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['providers'] 