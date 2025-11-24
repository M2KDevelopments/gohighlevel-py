"""Payment Coupons functionality for GoHighLevel API.

This module provides the PaymentCoupons class for managing payment coupons
in GoHighLevel, including creating, retrieving, listing, and deleting coupons.
"""

from typing import Dict, List, Optional, Union
import requests

from .auth.authdata import Auth


class PaymentCoupons:
    """
    Endpoints For Payment Coupons
    https://highlevel.stoplight.io/docs/integrations/d5e4f3c2b1a90-list-coupons
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the PaymentCoupons class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data

    def create(self, data: Dict) -> Dict:
        """Create a new coupon.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/c7d8e2f1b4a92-create-coupon
        
        Args:
            data (Dict): The coupon data to create
            
        Returns:
            Dict: Created coupon details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/payments/coupons",
            json=data,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def get(self, coupon_id: str) -> Dict:
        """Get coupon by ID.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/b9c8d2f5e3a10-get-coupon-by-id
        
        Args:
            coupon_id (str): The ID of the coupon to retrieve
            
        Returns:
            Dict: Coupon details
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/payments/coupons/{coupon_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def get_all(self, page: Optional[int] = None, limit: Optional[int] = None,
                sort: Optional[str] = None, order: Optional[str] = None,
                is_active: Optional[bool] = None) -> Dict[str, Any]:
        """List coupons.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/d5e4f3c2b1a90-list-coupons
        
        Args:
            page (Optional[int]): Page number for pagination
            limit (Optional[int]): Number of items per page
            sort (Optional[str]): Field to sort by
            order (Optional[str]): Sort order ('asc' or 'desc')
            is_active (Optional[bool]): Filter by active status
            
        Returns:
            Dict[str, Any]: Dictionary containing coupons and pagination info
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        params = {}
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit
        if sort:
            params['sort'] = sort
        if order:
            params['order'] = order
        if is_active is not None:
            params['isActive'] = str(is_active).lower()
            
        response = requests.get(
            f"{self.auth_data.baseurl}/payments/coupons",
            params=params,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()

    def delete(self, coupon_id: str) -> Dict:
        """Delete a coupon.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/f4e3d2c1b0a89-delete-coupon
        
        Args:
            coupon_id (str): The ID of the coupon to delete
            
        Returns:
            Dict: Response indicating success
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If authentication data is missing
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.delete(
            f"{self.auth_data.baseurl}/payments/coupons/{coupon_id}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json() 