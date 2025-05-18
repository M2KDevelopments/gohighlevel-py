"""Opportunity Notes functionality for GoHighLevel API.

This module provides the Notes class for managing opportunity notes
in GoHighLevel, including creation and tracking of notes.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class NoteData(TypedDict, total=False):
    """Type definition for note data."""
    content: str
    type: str  # 'text', 'call', 'email', etc.
    visibility: Optional[str]  # 'private', 'public'
    attachments: Optional[List[Dict[str, str]]]  # List of file attachments


class Notes:
    """Notes management class for GoHighLevel API.

    This class provides methods for managing opportunity notes,
    including creation and retrieval of notes.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Notes class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
        self,
        opportunity_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all notes for an opportunity.

        Args:
            opportunity_id (str): The ID of the opportunity
            limit (int, optional): Number of notes to return. Defaults to 50.
            skip (int, optional): Number of notes to skip. Defaults to 0.

        Returns:
            List[Dict]: List of notes

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'limit': limit,
            'skip': skip
        }

        response = requests.get(
            f"{self.auth_data['baseurl']}/opportunities/{opportunity_id}/notes",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['notes']

    def get(self, opportunity_id: str, note_id: str) -> Dict:
        """Get a specific note.

        Args:
            opportunity_id (str): The ID of the opportunity
            note_id (str): The ID of the note to retrieve

        Returns:
            Dict: Note details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/opportunities/{opportunity_id}/notes/{note_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['note']

    def create(self, opportunity_id: str, data: NoteData) -> Dict:
        """Create a new note.

        Args:
            opportunity_id (str): The ID of the opportunity
            data (NoteData): Note data
                Example:
                {
                    "content": "Called client to discuss proposal",
                    "type": "call",
                    "visibility": "public",
                    "attachments": [
                        {
                            "name": "proposal.pdf",
                            "url": "https://example.com/files/proposal.pdf"
                        }
                    ]
                }

        Returns:
            Dict: Created note details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/opportunities/{opportunity_id}/notes",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['note']

    def update(self, opportunity_id: str, note_id: str, data: Dict) -> Dict:
        """Update a note.

        Args:
            opportunity_id (str): The ID of the opportunity
            note_id (str): The ID of the note to update
            data (Dict): Updated note data
                Example:
                {
                    "content": "Updated note content",
                    "visibility": "private"
                }

        Returns:
            Dict: Updated note details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/opportunities/{opportunity_id}/notes/{note_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['note']

    def delete(self, opportunity_id: str, note_id: str) -> Dict:
        """Delete a note.

        Args:
            opportunity_id (str): The ID of the opportunity
            note_id (str): The ID of the note to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/opportunities/{opportunity_id}/notes/{note_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json() 