"""Workflows functionality for GoHighLevel API.

This module provides the Workflows class for managing workflows
in GoHighLevel, including listing and managing workflows.
"""

from typing import Dict, List, Optional
import requests

from .auth.authdata import Auth


class Workflow:
    """
    Endpoints For Workflows
    https://highlevel.stoplight.io/docs/integrations/3c7cf6a44f362-workflows-api
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the Workflows class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(self, location_id: str) -> List[Dict]:
        """Get all workflows for a location.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/070d2f9be5549-get-workflow
        
        Args:
            location_id (str): The ID of the location to get workflows for
            
        Returns:
            List[Dict]: List of workflows
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/workflows",
            params={'locationId': location_id},
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['workflows'] 