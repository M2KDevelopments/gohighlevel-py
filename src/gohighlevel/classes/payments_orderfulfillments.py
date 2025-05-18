"""Payment Order Fulfillments functionality for GoHighLevel API.

This module provides the PaymentOrderFulfillments class for managing order fulfillments
in GoHighLevel, including creating and listing fulfillments.
"""

from typing import Dict, List, Optional
import requests

from .auth.authdata import Auth


class PaymentOrderFulfillments:
    """
    Endpoints For Payment Order Fulfillments
    https://highlevel.stoplight.io/docs/integrations/670fe5beec7de-list-fulfillment
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the PaymentOrderFulfillments class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def create(self, order_id: str, data: Dict) -> Dict:
        """Create an order fulfillment.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/1e091099a92c6-create-order-fulfillment
        
        Args:
            order_id (str): The ID of the order to create fulfillment for
            data (Dict): The fulfillment data to create
            
        Returns:
            Dict: Created fulfillment details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/payments/orders/{order_id}/fulfillments",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def get_all(self, order_id: str, page: Optional[int] = None,
                limit: Optional[int] = None) -> Dict[str, Any]:
        """List fulfillments.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/670fe5beec7de-list-fulfillment
        
        Args:
            order_id (str): Filter by order ID
            page (Optional[int]): Page number for pagination
            limit (Optional[int]): Number of items per page
            
        Returns:
            Dict[str, Any]: Dictionary containing fulfillments and pagination info
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        params = {'orderId': order_id}
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit
            
        response = requests.get(
            f"{self.auth_data.baseurl}/payments/orders/fulfillments",
            params=params,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 