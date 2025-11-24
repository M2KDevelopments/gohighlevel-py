"""Funnels functionality for GoHighLevel API.

This module provides the Funnels class for managing sales funnels
in GoHighLevel, including funnel pages, settings, and analytics.
"""

from typing import Dict, List, Optional, TypedDict
import requests

from .funnels_redirect import FunnelsRedirect


class FunnelSettings(TypedDict, total=False):
    """Type definition for funnel settings."""
    name: str
    description: str
    domain: str
    favicon: str
    headerScripts: List[str]
    footerScripts: List[str]
    isPublished: bool
    seoSettings: Dict[str, str]  # title, description, keywords


class FunnelPage(TypedDict, total=False):
    """Type definition for funnel page."""
    title: str
    slug: str
    content: str
    settings: Dict
    isPublished: bool
    seoSettings: Dict[str, str]
    customScripts: Dict[str, List[str]]  # header, footer scripts


class Funnels:
    """Funnels management class for GoHighLevel API.

    This class provides methods for managing sales funnels, including creating,
    updating, and retrieving funnels and their pages.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the Funnels class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data
        self.redirects = FunnelsRedirect(auth_data)

    def get_all(
        self,
        location_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all funnels for a location.

        Args:
            location_id (str): The ID of the location
            limit (int, optional): Number of funnels to return. Defaults to 50.
            skip (int, optional): Number of funnels to skip. Defaults to 0.

        Returns:
            List[Dict]: List of funnels

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
            f"{self.auth_data['baseurl']}/funnels",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['funnels']

    def get(self, funnel_id: str) -> Dict:
        """Get a specific funnel.

        Args:
            funnel_id (str): The ID of the funnel to retrieve

        Returns:
            Dict: Funnel details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['funnel']

    def add(
        self,
        location_id: str,
        settings: FunnelSettings,
        pages: Optional[List[FunnelPage]] = None
    ) -> Dict:
        """Create a new funnel.

        Args:
            location_id (str): The ID of the location
            settings (FunnelSettings): Funnel settings
                Example:
                {
                    "name": "Product Launch",
                    "description": "New product launch funnel",
                    "domain": "launch.example.com",
                    "isPublished": False,
                    "seoSettings": {
                        "title": "Product Launch",
                        "description": "Launch your product"
                    }
                }
            pages (Optional[List[FunnelPage]], optional): List of funnel pages.
                Defaults to None.

        Returns:
            Dict: Created funnel details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            'settings': settings
        }
        if pages:
            data['pages'] = pages

        response = requests.post(
            f"{self.auth_data['baseurl']}/funnels",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['funnel']

    def update(self, funnel_id: str, data: Dict) -> Dict:
        """Update a funnel.

        Args:
            funnel_id (str): The ID of the funnel to update
            data (Dict): Updated funnel data
                Example:
                {
                    "settings": {
                        "name": "Updated Funnel Name",
                        "isPublished": True
                    }
                }

        Returns:
            Dict: Updated funnel details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['funnel']

    def delete(self, funnel_id: str) -> Dict:
        """Delete a funnel.

        Args:
            funnel_id (str): The ID of the funnel to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_pages(self, funnel_id: str) -> List[Dict]:
        """Get all pages in a funnel.

        Args:
            funnel_id (str): The ID of the funnel

        Returns:
            List[Dict]: List of funnel pages

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/pages",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['pages']

    def add_page(self, funnel_id: str, page: FunnelPage) -> Dict:
        """Add a page to a funnel.

        Args:
            funnel_id (str): The ID of the funnel
            page (FunnelPage): Page data
                Example:
                {
                    "title": "Landing Page",
                    "slug": "landing",
                    "content": "<html>...</html>",
                    "isPublished": True,
                    "seoSettings": {
                        "title": "Landing Page",
                        "description": "Welcome to our product"
                    }
                }

        Returns:
            Dict: Created page details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/pages",
            json=page,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['page']

    def update_page(self, funnel_id: str, page_id: str, data: Dict) -> Dict:
        """Update a funnel page.

        Args:
            funnel_id (str): The ID of the funnel
            page_id (str): The ID of the page to update
            data (Dict): Updated page data
                Example:
                {
                    "title": "Updated Page Title",
                    "content": "<html>Updated content</html>",
                    "isPublished": True
                }

        Returns:
            Dict: Updated page details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/pages/{page_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['page']

    def delete_page(self, funnel_id: str, page_id: str) -> Dict:
        """Delete a funnel page.

        Args:
            funnel_id (str): The ID of the funnel
            page_id (str): The ID of the page to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/pages/{page_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_analytics(
        self,
        funnel_id: str,
        start_date: str,
        end_date: str
    ) -> Dict:
        """Get funnel analytics.

        Args:
            funnel_id (str): The ID of the funnel
            start_date (str): Start date in ISO format (YYYY-MM-DD)
            end_date (str): End date in ISO format (YYYY-MM-DD)

        Returns:
            Dict: Funnel analytics data

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {
            'startDate': start_date,
            'endDate': end_date
        }

        response = requests.get(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/analytics",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['analytics'] 