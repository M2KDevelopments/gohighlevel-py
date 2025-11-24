"""SaaS functionality for GoHighLevel API.

This module provides the SaaS class for managing SaaS-related features
in GoHighLevel, including subscriptions, billing, and user management.
"""

from typing import Dict, List, Optional, TypedDict
import requests


class Subscription(TypedDict, total=False):
    """Type definition for subscription."""
    planId: str
    customerId: str
    status: str
    startDate: str
    endDate: str
    billingCycle: str
    paymentMethod: Dict[str, str]
    features: List[str]


class SaaS:
    """SaaS management class for GoHighLevel API.

    This class provides methods for managing SaaS-related features,
    including subscriptions, billing, and user management.
    """

    def __init__(self, auth_data: Optional[Dict] = None) -> None:
        """Initialize the SaaS class.

        Args:
            auth_data (Optional[Dict]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all_subscriptions(
        self,
        location_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict]:
        """Get all subscriptions.

        Args:
            location_id (str): The ID of the location
            limit (int, optional): Number of subscriptions to return. Defaults to 50.
            skip (int, optional): Number of subscriptions to skip. Defaults to 0.

        Returns:
            List[Dict]: List of subscriptions

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
            f"{self.auth_data['baseurl']}/saas/subscriptions",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['subscriptions']

    def get_subscription(self, subscription_id: str) -> Dict:
        """Get a specific subscription.

        Args:
            subscription_id (str): The ID of the subscription to retrieve

        Returns:
            Dict: Subscription details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.get(
            f"{self.auth_data['baseurl']}/saas/subscriptions/{subscription_id}",
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['subscription']

    def create_subscription(
        self,
        location_id: str,
        subscription: Subscription
    ) -> Dict:
        """Create a new subscription.

        Args:
            location_id (str): The ID of the location
            subscription (Subscription): Subscription data
                Example:
                {
                    "planId": "plan123",
                    "customerId": "customer123",
                    "status": "active",
                    "startDate": "2024-01-01",
                    "billingCycle": "monthly",
                    "paymentMethod": {
                        "type": "card",
                        "last4": "4242"
                    },
                    "features": ["feature1", "feature2"]
                }

        Returns:
            Dict: Created subscription details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {
            'locationId': location_id,
            **subscription
        }

        response = requests.post(
            f"{self.auth_data['baseurl']}/saas/subscriptions",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['subscription']

    def update_subscription(self, subscription_id: str, data: Dict) -> Dict:
        """Update a subscription.

        Args:
            subscription_id (str): The ID of the subscription to update
            data (Dict): Updated subscription data
                Example:
                {
                    "status": "paused",
                    "endDate": "2024-12-31",
                    "features": ["feature1", "feature2", "feature3"]
                }

        Returns:
            Dict: Updated subscription details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        response = requests.put(
            f"{self.auth_data['baseurl']}/saas/subscriptions/{subscription_id}",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['subscription']

    def cancel_subscription(
        self,
        subscription_id: str,
        reason: Optional[str] = None
    ) -> Dict:
        """Cancel a subscription.

        Args:
            subscription_id (str): The ID of the subscription to cancel
            reason (Optional[str], optional): Reason for cancellation. Defaults to None.

        Returns:
            Dict: Response indicating success

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        data = {}
        if reason:
            data['reason'] = reason

        response = requests.post(
            f"{self.auth_data['baseurl']}/saas/subscriptions/{subscription_id}/cancel",
            json=data,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()

    def get_billing_history(
        self,
        subscription_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """Get billing history for a subscription.

        Args:
            subscription_id (str): The ID of the subscription
            start_date (Optional[str], optional): Start date in ISO format. Defaults to None.
            end_date (Optional[str], optional): End date in ISO format. Defaults to None.

        Returns:
            List[Dict]: List of billing transactions

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {}
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date

        response = requests.get(
            f"{self.auth_data['baseurl']}/saas/subscriptions/{subscription_id}/billing",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['transactions']

    def get_usage_metrics(
        self,
        subscription_id: str,
        metric: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """Get usage metrics for a subscription.

        Args:
            subscription_id (str): The ID of the subscription
            metric (str): The metric to retrieve (e.g., 'api_calls', 'storage')
            start_date (Optional[str], optional): Start date in ISO format. Defaults to None.
            end_date (Optional[str], optional): End date in ISO format. Defaults to None.

        Returns:
            Dict: Usage metrics data

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data or not self.auth_data.get('headers') or not self.auth_data.get('baseurl'):
            raise ValueError("Authentication data is required")

        params = {'metric': metric}
        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date

        response = requests.get(
            f"{self.auth_data['baseurl']}/saas/subscriptions/{subscription_id}/usage",
            params=params,
            headers=self.auth_data['headers']
        )
        response.raise_for_status()
        return response.json()['usage'] 