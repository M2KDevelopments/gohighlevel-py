from typing import Optional, List, Dict, Any
import requests

from .auth.authdata import Auth

class CalendarAppointmentNote:
    """
    Endpoints For Calendars Appointments Notes
    https://highlevel.stoplight.io/docs/integrations/e04d0822bd613-get-notes
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        self.auth_data = auth_data

    def get_all(self, appointment_id: str, limit: int, offset: int) -> List[Dict[str, Any]]:
        """
        Get Appointment Notes
        Documentation - https://highlevel.stoplight.io/docs/integrations/e04d0822bd613-get-notes
        
        Args:
            appointment_id: The appointment ID to get notes for
            limit: Number of notes to return
            offset: Number of notes to skip
            
        Returns:
            List of appointment notes
        """
        if not limit or limit < 0:
            return []
        if not offset or offset < 0:
            return []
            
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/calendars/appointments/{appointment_id}/notes?limit={limit}&offset={offset}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['notes']

    def add(self, appointment_id: str, body: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create Appointment Note
        Documentation - https://highlevel.stoplight.io/docs/integrations/dcdda866d8b49-create-note
        
        Args:
            appointment_id: The appointment ID to add note to
            body: Note body (<= 5000 characters)
            user_id: Optional user ID
            
        Returns:
            Created note information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        data = {"body": body}
        if user_id:
            data["userId"] = user_id
            
        response = requests.post(
            f"{self.auth_data.baseurl}/appointments/{appointment_id}/notes",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['note']

    def update(self, appointment_id: str, note_id: str, body: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Update Appointment Note
        Documentation - https://highlevel.stoplight.io/docs/integrations/f27408b1ae367-update-note
        
        Args:
            appointment_id: The appointment ID
            note_id: The note ID to update
            body: Note body (<= 5000 characters)
            user_id: Optional user ID
            
        Returns:
            Updated note information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        data = {"body": body}
        if user_id:
            data["userId"] = user_id
            
        response = requests.put(
            f"{self.auth_data.baseurl}/appointments/{appointment_id}/notes/{note_id}",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['note']

    def remove(self, appointment_id: str, note_id: str) -> bool:
        """
        Delete Appointment Note
        Documentation - https://highlevel.stoplight.io/docs/integrations/fe10a2bff1674-delete-note
        
        Args:
            appointment_id: The appointment ID
            note_id: The note ID to delete
            
        Returns:
            True if successful
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/appointments/{appointment_id}/notes/{note_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json().get('succeeded', True) 