"""Payment Orders functionality for GoHighLevel API.

This module provides the PaymentOrders class for managing payment orders
in GoHighLevel, including retrieving and listing orders.
"""

from typing import Dict, List, Optional
import requests

from .auth.authdata import Auth


class PaymentOrders:
    """
    Endpoints For Payment Orders
    https://highlevel.stoplight.io/docs/integrations/378562f514a17-list-orders
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the PaymentOrders class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get(self, order_id: str) -> Dict:
        """Get order by ID.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/bcdf47fc22520-get-order-by-id
        
        Args:
            order_id (str): The ID of the order to retrieve
            
        Returns:
            Dict: Order details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/payments/orders/{order_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def get_all(self, location_id: str, page: Optional[int] = None, 
                limit: Optional[int] = None, sort: Optional[str] = None,
                order: Optional[str] = None) -> Dict[str, Any]:
        """List orders.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/378562f514a17-list-orders
        
        Args:
            location_id (str): The ID of the location
            page (Optional[int]): Page number for pagination
            limit (Optional[int]): Number of items per page
            sort (Optional[str]): Field to sort by
            order (Optional[str]): Sort order ('asc' or 'desc')
            
        Returns:
            Dict[str, Any]: Dictionary containing orders and pagination info
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        params = {'locationId': location_id}
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit
        if sort:
            params['sort'] = sort
        if order:
            params['order'] = order
            
        response = requests.get(
            f"{self.auth_data.baseurl}/payments/orders",
            params=params,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 