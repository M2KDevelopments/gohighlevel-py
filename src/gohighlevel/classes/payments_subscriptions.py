"""Payment Subscriptions functionality for GoHighLevel API.

This module provides the PaymentSubscriptions class for managing payment subscriptions
in GoHighLevel, including retrieving and listing subscriptions.
"""

from typing import Dict, List, Optional
import requests

from .auth.authdata import Auth


class PaymentSubscriptions:
    """
    Endpoints For Payment Subscriptions
    https://highlevel.stoplight.io/docs/integrations/f5c8e2d1a4b92-list-subscriptions
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the PaymentSubscriptions class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get_all(self, contact_id: Optional[str] = None, status: Optional[str] = None,
                page: Optional[int] = None, limit: Optional[int] = None,
                sort: Optional[str] = None, order: Optional[str] = None) -> Dict[str, Any]:
        """List subscriptions.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/f5c8e2d1a4b92-list-subscriptions
        
        Args:
            contact_id (Optional[str]): Filter by contact ID
            status (Optional[str]): Filter by subscription status
            page (Optional[int]): Page number for pagination
            limit (Optional[int]): Number of items per page
            sort (Optional[str]): Field to sort by
            order (Optional[str]): Sort order ('asc' or 'desc')
            
        Returns:
            Dict[str, Any]: Dictionary containing subscriptions and pagination info
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        params = {}
        if contact_id:
            params['contactId'] = contact_id
        if status:
            params['status'] = status
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit
        if sort:
            params['sort'] = sort
        if order:
            params['order'] = order
            
        response = requests.get(
            f"{self.auth_data.baseurl}/payments/subscriptions",
            params=params,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 