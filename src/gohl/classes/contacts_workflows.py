"""Contacts Workflows functionality for GoHighLevel API.

This module provides the ContactsWorkflows class for managing workflow
associations with contacts in GoHighLevel.
"""

from typing import Dict, Optional
import requests

from .auth.authdata import Auth


class ContactsWorkflows:
    """
    Endpoints For Contacts Workflows
    https://highlevel.stoplight.io/docs/integrations/fe0f421553a9e-add-contact-to-workflow
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the ContactsWorkflows class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def add(self, contact_id: str, workflow_id: str, event_start_time: str) -> bool:
        """Add a contact to a workflow.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/fe0f421553a9e-add-contact-to-workflow
        
        Args:
            contact_id (str): The ID of the contact
            workflow_id (str): The ID of the workflow
            event_start_time (str): Start time for the workflow event (e.g., '2021-06-23T03:30:00+01:00')
            
        Returns:
            bool: True if successful
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/workflow/{workflow_id}",
            json={'eventStartTime': event_start_time},
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json().get('succeeded', True)

    def remove(self, contact_id: str, workflow_id: str) -> bool:
        """Remove a contact from a workflow.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/86cd9978f66ff-delete-contact-to-workflow
        
        Args:
            contact_id (str): The ID of the contact
            workflow_id (str): The ID of the workflow
            
        Returns:
            bool: True if successful
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/workflow/{workflow_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json().get('succeeded', True) 