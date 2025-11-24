"""Custom Menus functionality for GoHighLevel API.

This module provides the CustomMenus class for managing custom menus
in GoHighLevel, including menu items, structure, and permissions.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class MenuItem(TypedDict, total=False):
    """Type definition for menu item."""
    title: str
    url: str
    icon: str  # Font Awesome icon name
    order: int
    parentId: Optional[str]  # For nested menu items
    permissions: List[str]  # Role-based permissions
    isExternal: bool  # Whether the URL is external
    isVisible: bool


class MenuGroup(TypedDict, total=False):
    """Type definition for menu group."""
    name: str
    description: str
    items: List[MenuItem]
    permissions: List[str]
    isVisible: bool


class CustomMenus:
    """Custom Menus management class for GoHighLevel API.

    This class provides methods for managing custom menus, including creating,
    updating, and retrieving menu items and groups.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the CustomMenus class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
        self,
        location_id: str,
        include_items: bool = True,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all menu groups for a location.

        Args:
            location_id (str): The ID of the location
            include_items (bool, optional): Whether to include menu items. Defaults to True.
            limit (int, optional): Number of groups to return. Defaults to 50.
            skip (int, optional): Number of groups to skip. Defaults to 0.

        Returns:
            List[Dict]: List of menu groups

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'locationId': location_id,
            'includeItems': include_items,
            'limit': limit,
            'skip': skip
        }

        response = requests.get(
            f"{self.auth_data['baseurl']}/custom-menus",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['menuGroups']

    def get_group(self, group_id: str) -> Dict:
        """Get a specific menu group.

        Args:
            group_id (str): The ID of the menu group to retrieve

        Returns:
            Dict: Menu group details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/custom-menus/{group_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['menuGroup']

    def add_group(
        self,
        location_id: str,
        group: MenuGroup
    ) -> Dict:
        """Create a new menu group.

        Args:
            location_id (str): The ID of the location
            group (MenuGroup): Menu group data
                Example:
                {
                    "name": "Admin Tools",
                    "description": "Administrative tools and settings",
                    "items": [
                        {
                            "title": "User Management",
                            "url": "/admin/users",
                            "icon": "users",
                            "order": 1,
                            "permissions": ["admin"],
                            "isExternal": False,
                            "isVisible": True
                        }
                    ],
                    "permissions": ["admin"],
                    "isVisible": True
                }

        Returns:
            Dict: Created menu group details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            **group
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/custom-menus",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['menuGroup']

    def update_group(self, group_id: str, data: Dict) -> Dict:
        """Update a menu group.

        Args:
            group_id (str): The ID of the menu group to update
            data (Dict): Updated menu group data
                Example:
                {
                    "name": "Updated Group Name",
                    "description": "Updated description",
                    "isVisible": False
                }

        Returns:
            Dict: Updated menu group details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/custom-menus/{group_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['menuGroup']

    def delete_group(self, group_id: str) -> Dict:
        """Delete a menu group.

        Args:
            group_id (str): The ID of the menu group to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/custom-menus/{group_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def add_item(self, group_id: str, item: MenuItem) -> Dict:
        """Add a menu item to a group.

        Args:
            group_id (str): The ID of the menu group
            item (MenuItem): Menu item data
                Example:
                {
                    "title": "Reports",
                    "url": "/reports",
                    "icon": "chart-bar",
                    "order": 2,
                    "permissions": ["admin", "manager"],
                    "isExternal": False,
                    "isVisible": True
                }

        Returns:
            Dict: Created menu item details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/custom-menus/{group_id}/items",
            json=item,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['menuItem']

    def update_item(self, group_id: str, item_id: str, data: Dict) -> Dict:
        """Update a menu item.

        Args:
            group_id (str): The ID of the menu group
            item_id (str): The ID of the menu item to update
            data (Dict): Updated menu item data
                Example:
                {
                    "title": "Updated Item Title",
                    "order": 3,
                    "isVisible": False
                }

        Returns:
            Dict: Updated menu item details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/custom-menus/{group_id}/items/{item_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['menuItem']

    def delete_item(self, group_id: str, item_id: str) -> Dict:
        """Delete a menu item.

        Args:
            group_id (str): The ID of the menu group
            item_id (str): The ID of the menu item to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/custom-menus/{group_id}/items/{item_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def reorder_items(self, group_id: str, item_orders: List[Dict[str, int]]) -> List[Dict]:
        """Reorder menu items in a group.

        Args:
            group_id (str): The ID of the menu group
            item_orders (List[Dict[str, int]]): List of item IDs and their new orders
                Example:
                [
                    {"itemId": "item1", "order": 1},
                    {"itemId": "item2", "order": 2},
                    {"itemId": "item3", "order": 3}
                ]

        Returns:
            List[Dict]: Updated menu items with new order

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/custom-menus/{group_id}/items/reorder",
            json={'orders': item_orders},
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['menuItems'] 