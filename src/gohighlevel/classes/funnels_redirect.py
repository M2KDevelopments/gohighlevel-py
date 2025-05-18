"""Funnel Redirects functionality for GoHighLevel API.

This module provides the FunnelsRedirect class for managing funnel redirects
in GoHighLevel, including URL redirects and conditional routing.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class RedirectRule(TypedDict, total=False):
    """Type definition for redirect rule."""
    name: str
    description: str
    sourceUrl: str
    targetUrl: str
    type: str  # '301', '302'
    conditions: List[Dict]  # List of conditions for conditional redirects
    isActive: bool


class FunnelsRedirect:
    """Funnel Redirects management class for GoHighLevel API.

    This class provides methods for managing funnel redirects, including creating,
    updating, and retrieving redirect rules.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the FunnelsRedirect class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(
        self,
        funnel_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all redirect rules for a funnel.

        Args:
            funnel_id (str): The ID of the funnel
            limit (int, optional): Number of rules to return. Defaults to 50.
            skip (int, optional): Number of rules to skip. Defaults to 0.

        Returns:
            List[Dict]: List of redirect rules

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
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/redirects",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['redirects']

    def get(self, funnel_id: str, redirect_id: str) -> Dict:
        """Get a specific redirect rule.

        Args:
            funnel_id (str): The ID of the funnel
            redirect_id (str): The ID of the redirect rule to retrieve

        Returns:
            Dict: Redirect rule details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/redirects/{redirect_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['redirect']

    def add(self, funnel_id: str, rule: RedirectRule) -> Dict:
        """Create a new redirect rule.

        Args:
            funnel_id (str): The ID of the funnel
            rule (RedirectRule): Redirect rule data
                Example:
                {
                    "name": "Product Page Redirect",
                    "description": "Redirect old product URLs",
                    "sourceUrl": "/old-product",
                    "targetUrl": "/new-product",
                    "type": "301",
                    "conditions": [
                        {
                            "field": "country",
                            "operator": "equals",
                            "value": "US"
                        }
                    ],
                    "isActive": True
                }

        Returns:
            Dict: Created redirect rule details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/redirects",
            json=rule,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['redirect']

    def update(self, funnel_id: str, redirect_id: str, data: Dict) -> Dict:
        """Update a redirect rule.

        Args:
            funnel_id (str): The ID of the funnel
            redirect_id (str): The ID of the redirect rule to update
            data (Dict): Updated redirect rule data
                Example:
                {
                    "name": "Updated Rule Name",
                    "targetUrl": "/updated-target",
                    "isActive": False
                }

        Returns:
            Dict: Updated redirect rule details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/redirects/{redirect_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['redirect']

    def delete(self, funnel_id: str, redirect_id: str) -> Dict:
        """Delete a redirect rule.

        Args:
            funnel_id (str): The ID of the funnel
            redirect_id (str): The ID of the redirect rule to delete

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.delete(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/redirects/{redirect_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def test_rule(
        self,
        funnel_id: str,
        redirect_id: str,
        test_data: Dict
    ) -> Dict:
        """Test a redirect rule with sample data.

        Args:
            funnel_id (str): The ID of the funnel
            redirect_id (str): The ID of the redirect rule to test
            test_data (Dict): Test data to evaluate against conditions
                Example:
                {
                    "country": "US",
                    "device": "mobile",
                    "referrer": "google.com"
                }

        Returns:
            Dict: Test results including whether the rule would match

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.post(
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/redirects/{redirect_id}/test",
            json=test_data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['result']

    def get_analytics(
        self,
        funnel_id: str,
        redirect_id: str,
        start_date: str,
        end_date: str
    ) -> Dict:
        """Get analytics for a redirect rule.

        Args:
            funnel_id (str): The ID of the funnel
            redirect_id (str): The ID of the redirect rule
            start_date (str): Start date in ISO format (YYYY-MM-DD)
            end_date (str): End date in ISO format (YYYY-MM-DD)

        Returns:
            Dict: Redirect rule analytics data

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
            f"{self.auth_data['baseurl']}/funnels/{funnel_id}/redirects/{redirect_id}/analytics",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['analytics'] 