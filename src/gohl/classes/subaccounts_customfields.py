"""SubAccounts Custom Fields functionality for GoHighLevel API.

This module provides the CustomField class for managing custom fields
in sub-accounts within GoHighLevel.
"""

from typing import Dict, List, Optional
import requests

from .auth.authdata import Auth


class CustomField:
    """
    Endpoints For SubAccounts Custom Fields
    https://highlevel.stoplight.io/docs/integrations/e283eac258a96-sub-account-formerly-location-api
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the CustomField class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(self, location_id: str) -> List[Dict]:
        """Get all custom fields for a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location
            
        Returns:
            List[Dict]: List of custom fields
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/location/{location_id}/custom-fields",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['fields']

    def create(self, location_id: str, data: Dict) -> Dict:
        """Create a custom field for a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location
            data (Dict): The custom field data to create
            
        Returns:
            Dict: Created custom field details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/location/{location_id}/custom-fields",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['field']

    def update(self, location_id: str, field_id: str, data: Dict) -> Dict:
        """Update a custom field in a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location
            field_id (str): The ID of the custom field to update
            data (Dict): The updated custom field data
            
        Returns:
            Dict: Updated custom field details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.put(
            f"{self.auth_data.baseurl}/location/{location_id}/custom-fields/{field_id}",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['field']

    def delete(self, location_id: str, field_id: str) -> Dict:
        """Delete a custom field from a sub-account.
        
        Args:
            location_id (str): The ID of the sub-account/location
            field_id (str): The ID of the custom field to delete
            
        Returns:
            Dict: Response indicating success
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/location/{location_id}/custom-fields/{field_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 