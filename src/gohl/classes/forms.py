"""Forms functionality for GoHighLevel API.

This module provides the Forms class for managing forms and form submissions
in GoHighLevel.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class FormField(TypedDict, total=False):
    """Type definition for form field."""
    name: str
    label: str
    type: str  # 'text', 'email', 'phone', 'select', etc.
    required: bool
    options: List[str]  # For select fields
    defaultValue: str
    placeholder: str
    order: int


class FormSettings(TypedDict, total=False):
    """Type definition for form settings."""
    title: str
    description: str
    submitButtonText: str
    successMessage: str
    redirectUrl: str
    notifyEmails: List[str]
    style: Dict


class Form:
    """Forms management class for GoHighLevel API.

    This class provides methods for managing forms, including creating,
    updating, and retrieving forms and their submissions.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Forms class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
        self,
        location_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all forms for a location.

        Args:
            location_id (str): The ID of the location
            limit (int, optional): Number of forms to return. Defaults to 50.
            skip (int, optional): Number of forms to skip. Defaults to 0.

        Returns:
            List[Dict]: List of forms

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'locationId': location_id,
            'limit': limit,
            'skip': skip
        }

        response = requests.get(
            f"{self.auth_data['baseurl']}/forms",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['forms']

    def get(self, form_id: str) -> Dict:
        """Get a specific form.

        Args:
            form_id (str): The ID of the form to retrieve

        Returns:
            Dict: Form details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/forms/{form_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['form']

    def add(
        self,
        location_id: str,
        fields: List[FormField],
        settings: FormSettings
    ) -> Dict:
        """Create a new form.

        Args:
            location_id (str): The ID of the location
            fields (List[FormField]): List of form fields
                Example:
                [
                    {
                        "name": "email",
                        "label": "Email Address",
                        "type": "email",
                        "required": True,
                        "placeholder": "Enter your email"
                    }
                ]
            settings (FormSettings): Form settings
                Example:
                {
                    "title": "Contact Us",
                    "description": "Get in touch with our team",
                    "submitButtonText": "Send Message",
                    "successMessage": "Thank you for contacting us!",
                    "notifyEmails": ["support@example.com"]
                }

        Returns:
            Dict: Created form details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            'fields': fields,
            'settings': settings
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/forms",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['form']

    def update(self, form_id: str, data: Dict) -> Dict:
        """Update a form.

        Args:
            form_id (str): The ID of the form to update
            data (Dict): Updated form data
                Example:
                {
                    "fields": [...],
                    "settings": {
                        "title": "Updated Form Title",
                        "description": "Updated description"
                    }
                }

        Returns:
            Dict: Updated form details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/forms/{form_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['form']

    def delete(self, form_id: str) -> Dict:
        """Delete a form.

        Args:
            form_id (str): The ID of the form to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/forms/{form_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_submissions(
        self,
        form_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get form submissions.

        Args:
            form_id (str): The ID of the form
            limit (int, optional): Number of submissions to return. Defaults to 50.
            skip (int, optional): Number of submissions to skip. Defaults to 0.

        Returns:
            List[Dict]: List of form submissions

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
            f"{self.auth_data['baseurl']}/forms/{form_id}/submissions",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['submissions']

    def get_submission(self, form_id: str, submission_id: str) -> Dict:
        """Get a specific form submission.

        Args:
            form_id (str): The ID of the form
            submission_id (str): The ID of the submission

        Returns:
            Dict: Submission details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/forms/{form_id}/submissions/{submission_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['submission'] 