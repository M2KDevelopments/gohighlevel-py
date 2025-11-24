"""Location functionality for GoHighLevel API.

This module provides the Location class for managing locations
in GoHighLevel, including details, settings, and branding.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class LocationSettings(TypedDict, total=False):
    """Type definition for location settings."""
    name: str
    address: str
    phone: str
    email: str
    timezone: str
    currency: str
    branding: Dict[str, str]  # logo, colors, etc.
    businessHours: Dict[str, List[Dict]]  # days and hours
    customDomain: str


class Location:
    """Location management class for GoHighLevel API.

    This class provides methods for managing locations, including creating,
    updating, and retrieving location details and settings.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Location class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(self, limit: int = 50, skip: int = 0) -> List[Dict]:
        """Get all locations.

        Args:
            limit (int, optional): Number of locations to return. Defaults to 50.
            skip (int, optional): Number of locations to skip. Defaults to 0.

        Returns:
            List[Dict]: List of locations

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
            f"{self.auth_data['baseurl']}/locations",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['locations']

    def get(self, location_id: str) -> Dict:
        """Get a specific location.

        Args:
            location_id (str): The ID of the location to retrieve

        Returns:
            Dict: Location details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/locations/{location_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['location']

    def add(self, settings: LocationSettings) -> Dict:
        """Create a new location.

        Args:
            settings (LocationSettings): Location settings
                Example:
                {
                    "name": "Downtown Office",
                    "address": "123 Main St",
                    "phone": "+1234567890",
                    "email": "office@example.com",
                    "timezone": "America/New_York",
                    "currency": "USD",
                    "branding": {
                        "logo": "https://example.com/logo.png",
                        "primaryColor": "#FF0000"
                    },
                    "businessHours": {
                        "monday": [
                            {"start": "09:00", "end": "17:00"}
                        ]
                    }
                }

        Returns:
            Dict: Created location details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/locations",
            json=settings,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['location']

    def update(self, location_id: str, data: Dict) -> Dict:
        """Update a location.

        Args:
            location_id (str): The ID of the location to update
            data (Dict): Updated location data
                Example:
                {
                    "name": "Updated Office Name",
                    "phone": "+1987654321",
                    "branding": {
                        "primaryColor": "#00FF00"
                    }
                }

        Returns:
            Dict: Updated location details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/locations/{location_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['location']

    def delete(self, location_id: str) -> Dict:
        """Delete a location.

        Args:
            location_id (str): The ID of the location to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/locations/{location_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_settings(self, location_id: str) -> Dict:
        """Get location settings.

        Args:
            location_id (str): The ID of the location

        Returns:
            Dict: Location settings

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/locations/{location_id}/settings",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['settings']

    def update_settings(self, location_id: str, settings: Dict) -> Dict:
        """Update location settings.

        Args:
            location_id (str): The ID of the location
            settings (Dict): Updated settings data
                Example:
                {
                    "businessHours": {
                        "monday": [
                            {"start": "08:00", "end": "18:00"}
                        ]
                    },
                    "timezone": "America/Los_Angeles"
                }

        Returns:
            Dict: Updated settings

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/locations/{location_id}/settings",
            json=settings,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['settings'] 