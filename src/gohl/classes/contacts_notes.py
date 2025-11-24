from typing import Optional, Dict, Any, List
import requests

from .auth.authdata import Auth

class Note:
    """
    Endpoints For Contacts Notes
    https://highlevel.stoplight.io/docs/integrations/db572d519b209-get-all-notes
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        self.auth_data = auth_data

    def get_all(self, contact_id: str) -> List[Dict[str, Any]]:
        """
        Get all Notes
        Documentation - https://highlevel.stoplight.io/docs/integrations/73decb4b6d0c2-get-all-notes
        
        Args:
            contact_id: The contact ID to get notes for
            
        Returns:
            List of notes
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/notes",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['notes']

    def get(self, contact_id: str, note_id: str) -> Dict[str, Any]:
        """
        Get Note
        Documentation - https://highlevel.stoplight.io/docs/integrations/24cab1c2b3dfb-get-note
        
        Args:
            contact_id: The contact ID
            note_id: The note ID to retrieve
            
        Returns:
            Note information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/notes/{note_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['note']

    def add(self, contact_id: str, note: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Note
        Documentation - https://highlevel.stoplight.io/docs/integrations/5eab1684a9948-create-note
        
        Args:
            contact_id: The contact ID
            note: Note information to create
            
        Returns:
            Created note information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/notes",
            json=note,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['note']

    def update(self, contact_id: str, note_id: str, note: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update Note
        Documentation - https://highlevel.stoplight.io/docs/integrations/71814e115658f-update-note
        
        Args:
            contact_id: The contact ID
            note_id: The note ID to update
            note: Updated note information
            
        Returns:
            Updated note information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.put(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/notes/{note_id}",
            json=note,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['note']

    def remove(self, contact_id: str, note_id: str) -> bool:
        """
        Delete Note
        Documentation - https://highlevel.stoplight.io/docs/integrations/d7e867be69e9f-delete-note
        
        Args:
            contact_id: The contact ID
            note_id: The note ID to delete
            
        Returns:
            True if successful
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/contacts/{contact_id}/notes/{note_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json().get('succeeded', True) 