"""SubAccounts Custom Values functionality for GoHighLevel API.

This module provides the CustomValue class for managing custom values
in sub-accounts within GoHighLevel.
"""

from typing import Dict, List, Optional
import requests

from .auth.authdata import Auth


class CustomValue:
    """
    Endpoints For SubAccounts Custom Values
    https://highlevel.stoplight.io/docs/integrations/e283eac258a96-sub-account-formerly-location-api
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the CustomValue class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(self, location_id: str) -> List[Dict]:
        """Get all custom values for a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location
            
        Returns:
            List[Dict]: List of custom values
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/location/{location_id}/custom-values",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['values']

    def create(self, location_id: str, data: Dict) -> Dict:
        """Create a custom value for a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location
            data (Dict): The custom value data to create
            
        Returns:
            Dict: Created custom value details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/location/{location_id}/custom-values",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['value']

    def update(self, location_id: str, value_id: str, data: Dict) -> Dict:
        """Update a custom value in a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location
            value_id (str): The ID of the custom value to update
            data (Dict): The updated custom value data
            
        Returns:
            Dict: Updated custom value details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.put(
            f"{self.auth_data.baseurl}/location/{location_id}/custom-values/{value_id}",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['value']

    def delete(self, location_id: str, value_id: str) -> Dict:
        """Delete a custom value from a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location
            value_id (str): The ID of the custom value to delete
            
        Returns:
            Dict: Response indicating success
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/location/{location_id}/custom-values/{value_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 