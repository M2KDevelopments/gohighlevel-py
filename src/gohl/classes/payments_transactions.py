"""Payment Transactions functionality for GoHighLevel API.

This module provides the PaymentTransactions class for managing payment transactions
in GoHighLevel, including retrieving and listing transactions.
"""

from typing import Dict, List, Optional
import requests

from .auth.authdata import Auth


class PaymentTransactions:
    """
    Endpoints For Payment Transactions
    https://highlevel.stoplight.io/docs/integrations/b8c9d2f5e3a10-list-transactions
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the PaymentTransactions class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def get(self, transaction_id: str) -> Dict:
        """Get transaction by ID.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/a3b6a89c5d8f9-get-transaction-by-id
        
        Args:
            transaction_id (str): The ID of the transaction to retrieve
            
        Returns:
            Dict: Transaction details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/payments/transactions/{transaction_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def get_all(self, order_id: Optional[str] = None, page: Optional[int] = None,
                limit: Optional[int] = None, sort: Optional[str] = None,
                order: Optional[str] = None) -> Dict[str, Any]:
        """List transactions.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b8c9d2f5e3a10-list-transactions
        
        Args:
            order_id (Optional[str]): Filter by order ID
            page (Optional[int]): Page number for pagination
            limit (Optional[int]): Number of items per page
            sort (Optional[str]): Field to sort by
            order (Optional[str]): Sort order ('asc' or 'desc')
            
        Returns:
            Dict[str, Any]: Dictionary containing transactions and pagination info
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        params = {}
        if order_id:
            params['orderId'] = order_id
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit
        if sort:
            params['sort'] = sort
        if order:
            params['order'] = order
            
        response = requests.get(
            f"{self.auth_data.baseurl}/payments/transactions",
            params=params,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 