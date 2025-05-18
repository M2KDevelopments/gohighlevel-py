"""Users functionality for GoHighLevel API.

This module provides the Users class for managing users
in GoHighLevel, including user management and permissions.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class UserProfile(TypedDict, total=False):
    """Type definition for user profile."""
    firstName: str
    lastName: str
    email: str
    phone: Optional[str]
    role: str  # 'admin', 'manager', 'user', etc.
    permissions: List[str]
    settings: Dict[str, any]  # user preferences
    status: str  # 'active', 'inactive', 'pending'


class Users:
    """Users management class for GoHighLevel API.

    This class provides methods for managing users, including
    creating, updating, and managing user permissions.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Users class.

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
        """Get all users.

        Args:
            location_id (str): The ID of the location
            limit (int, optional): Number of users to return. Defaults to 50.
            skip (int, optional): Number of users to skip. Defaults to 0.

        Returns:
            List[Dict]: List of users

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
            f"{self.auth_data['baseurl']}/users",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['users']

    def get(self, user_id: str) -> Dict:
        """Get a specific user.

        Args:
            user_id (str): The ID of the user to retrieve

        Returns:
            Dict: User details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/users/{user_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['user']

    def create(self, location_id: str, profile: UserProfile) -> Dict:
        """Create a new user.

        Args:
            location_id (str): The ID of the location
            profile (UserProfile): User profile data
                Example:
                {
                    "firstName": "John",
                    "lastName": "Doe",
                    "email": "john@example.com",
                    "phone": "+1234567890",
                    "role": "manager",
                    "permissions": ["read", "write", "manage_users"],
                    "settings": {
                        "timezone": "America/New_York",
                        "notifications": {
                            "email": True,
                            "sms": False
                        }
                    },
                    "status": "active"
                }

        Returns:
            Dict: Created user details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            **profile
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/users",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['user']

    def update(self, user_id: str, data: Dict) -> Dict:
        """Update a user.

        Args:
            user_id (str): The ID of the user to update
            data (Dict): Updated user data
                Example:
                {
                    "firstName": "John Updated",
                    "role": "admin",
                    "permissions": ["read", "write", "manage_users", "manage_billing"],
                    "status": "inactive"
                }

        Returns:
            Dict: Updated user details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/users/{user_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['user']

    def delete(self, user_id: str) -> Dict:
        """Delete a user.

        Args:
            user_id (str): The ID of the user to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/users/{user_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def update_permissions(
        self,
        user_id: str,
        permissions: List[str]
    ) -> Dict:
        """Update user permissions.

        Args:
            user_id (str): The ID of the user
            permissions (List[str]): List of permission codes
                Example: ["read", "write", "manage_users"]

        Returns:
            Dict: Updated user permissions

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {'permissions': permissions}

        response = requests.put(
            f"{self.auth_data['baseurl']}/users/{user_id}/permissions",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['permissions']

    def get_activity(
        self,
        user_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get user activity history.

        Args:
            user_id (str): The ID of the user
            start_date (Optional[str], optional): Start date in ISO format. Defaults to None.
            end_date (Optional[str], optional): End date in ISO format. Defaults to None.
            limit (int, optional): Number of activities to return. Defaults to 50.
            skip (int, optional): Number of activities to skip. Defaults to 0.

        Returns:
            List[Dict]: List of user activities

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
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date

        response = requests.get(
            f"{self.auth_data['baseurl']}/users/{user_id}/activity",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['activities']

    def reset_password(self, user_id: str) -> Dict:
        """Trigger password reset for a user.

        Args:
            user_id (str): The ID of the user

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/users/{user_id}/reset-password",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json() 