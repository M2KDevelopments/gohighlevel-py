from typing import Optional, List, Dict, Any
import requests

from .auth.authdata import Auth

class Business:
    """
    Endpoints For Businesses
    https://highlevel.stoplight.io/docs/integrations/bb6b717cac89c-business-api
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        self.auth_data = auth_data

    def get_all(self, location_id: str) -> List[Dict[str, Any]]:
        """
        Get Business by location id
        Documentation - https://highlevel.stoplight.io/docs/integrations/a8db8afcbe0a3-get-businesses-by-location
        
        Args:
            location_id: The location ID to get businesses for
            
        Returns:
            List of businesses
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/businesses?locationId={location_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['businesses']

    def get(self, business_id: str) -> Dict[str, Any]:
        """
        Get Business
        Documentation - https://highlevel.stoplight.io/docs/integrations/c4d36fb259656-get-business
        
        Args:
            business_id: The business ID to retrieve
            
        Returns:
            Business information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/businesses/{business_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['business']

    def add(self, business: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Business
        Documentation - https://highlevel.stoplight.io/docs/integrations/7636876b20ac3-create-business
        
        Args:
            business: Business information to create
            
        Returns:
            Created business information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/businesses",
            json=business,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['business']

    def update(self, business_id: str, business: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update Business
        Documentation - https://highlevel.stoplight.io/docs/integrations/b95210ff2a8d7-update-business
        
        Args:
            business_id: The business ID to update
            business: Updated business information
            
        Returns:
            Updated business information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.put(
            f"{self.auth_data.baseurl}/businesses/{business_id}",
            json=business,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['business']

    def remove(self, business_id: str) -> bool:
        """
        Delete Business
        Documentation - https://highlevel.stoplight.io/docs/integrations/6f776fbd6dd1f-delete-business
        
        Args:
            business_id: The business ID to delete
            
        Returns:
            True if successful
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/businesses/{business_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json().get('succeeded', True) 