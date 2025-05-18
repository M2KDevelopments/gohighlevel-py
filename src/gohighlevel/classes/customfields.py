"""Custom Fields functionality for GoHighLevel API.

This module provides the CustomFields class for managing custom fields
in GoHighLevel.
"""

from typing import Dict, List, Optional, TypedDict, Union
import requests


class CustomFieldType(TypedDict, total=False):
    """Type definition for custom field type."""
    type: str  # 'text', 'number', 'date', 'select', 'multiselect', etc.
    options: List[str]  # For select and multiselect types
    defaultValue: Union[str, int, float, List[str], None]


class CustomFieldData(TypedDict, total=False):
    """Type definition for custom field data."""
    name: str
    type: CustomFieldType
    description: str
    isRequired: bool
    isPrivate: bool
    displayOrder: int


class CustomFields:
    """Custom Fields management class for GoHighLevel API.

    This class provides methods for managing custom fields, including creating,
    updating, and retrieving custom fields for various entities.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the CustomFields class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
        self,
        location_id: str,
        entity_type: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all custom fields for an entity type.

        Args:
            location_id (str): The ID of the location
            entity_type (str): Type of entity ('contact', 'opportunity', etc.)
            limit (int, optional): Number of fields to return. Defaults to 50.
            skip (int, optional): Number of fields to skip. Defaults to 0.

        Returns:
            List[Dict]: List of custom fields

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'locationId': location_id,
            'entityType': entity_type,
            'limit': limit,
            'skip': skip
        }

        response = requests.get(
            f"{self.auth_data['baseurl']}/custom-fields",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['customFields']

    def get(self, field_id: str) -> Dict:
        """Get a specific custom field.

        Args:
            field_id (str): The ID of the custom field to retrieve

        Returns:
            Dict: Custom field details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/custom-fields/{field_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['customField']

    def add(
        self,
        location_id: str,
        entity_type: str,
        field: CustomFieldData
    ) -> Dict:
        """Create a new custom field.

        Args:
            location_id (str): The ID of the location
            entity_type (str): Type of entity ('contact', 'opportunity', etc.)
            field (CustomFieldData): Custom field data
                Example:
                {
                    "name": "Preferred Contact Time",
                    "type": {
                        "type": "select",
                        "options": ["Morning", "Afternoon", "Evening"],
                        "defaultValue": "Morning"
                    },
                    "description": "Best time to contact",
                    "isRequired": False,
                    "isPrivate": False,
                    "displayOrder": 1
                }

        Returns:
            Dict: Created custom field details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            'entityType': entity_type,
            **field
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/custom-fields",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['customField']

    def update(self, field_id: str, data: Dict) -> Dict:
        """Update a custom field.

        Args:
            field_id (str): The ID of the custom field to update
            data (Dict): Updated custom field data
                Example:
                {
                    "name": "Updated Field Name",
                    "description": "Updated description",
                    "isRequired": True
                }

        Returns:
            Dict: Updated custom field details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/custom-fields/{field_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['customField']

    def delete(self, field_id: str) -> Dict:
        """Delete a custom field.

        Args:
            field_id (str): The ID of the custom field to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/custom-fields/{field_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_values(
        self,
        entity_id: str,
        entity_type: str
    ) -> Dict[str, Union[str, int, float, List[str], None]]:
        """Get custom field values for an entity.

        Args:
            entity_id (str): The ID of the entity
            entity_type (str): Type of entity ('contact', 'opportunity', etc.)

        Returns:
            Dict[str, Union[str, int, float, List[str], None]]: Custom field values

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'entityId': entity_id,
            'entityType': entity_type
        }

        response = requests.get(
            f"{self.auth_data['baseurl']}/custom-fields/values",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['values']

    def update_values(
        self,
        entity_id: str,
        entity_type: str,
        values: Dict[str, Union[str, int, float, List[str], None]]
    ) -> Dict:
        """Update custom field values for an entity.

        Args:
            entity_id (str): The ID of the entity
            entity_type (str): Type of entity ('contact', 'opportunity', etc.)
            values (Dict[str, Union[str, int, float, List[str], None]]): Custom field values
                Example:
                {
                    "field_id_1": "value1",
                    "field_id_2": ["option1", "option2"],
                    "field_id_3": 42
                }

        Returns:
            Dict: Updated custom field values

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'entityId': entity_id,
            'entityType': entity_type,
            'values': values
        }

        response = requests.put(
            f"{self.auth_data['baseurl']}/custom-fields/values",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['values'] 