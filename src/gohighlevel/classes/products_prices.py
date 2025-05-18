from typing import Optional, Dict, Any
import requests
from .auth.authdata import Auth


class ProductPrice:
    """
    ProductPrices class for managing product prices in GoHighLevel.
    """
    
    def __init__(self, auth_data: Optional[Auth] = None) -> None:
        """
        Initialize ProductPrices class.

        Args:
            auth_data (Optional[Auth]): Authentication data for API requests
        """
        self.auth_data = auth_data

    def create(self, product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Price for a Product.
        Documentation - https://highlevel.stoplight.io/docs/integrations/a47cd944aede9-create-price-for-a-product

        Args:
            product_id (str): ID of the product to create price for
            data (Dict[str, Any]): Price data to create

        Returns:
            Dict[str, Any]: API response containing created price data
        """
        headers = self.auth_data.headers if self.auth_data else None
        response = requests.post(f"{self.auth_data.baseurl}/products/{product_id}/prices", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def get(self, product_id: str, price_id: str) -> Dict[str, Any]:
        """
        Get Price by ID for a Product.
        Documentation - https://highlevel.stoplight.io/docs/integrations/f902955da364a-get-price-by-id-for-a-product

        Args:
            product_id (str): ID of the product
            price_id (str): ID of the price to retrieve

        Returns:
            Dict[str, Any]: API response containing price data
        """
        headers = self.auth_data.headers if self.auth_data else None
        response = requests.get(f"{self.auth_data.baseurl}/products/{product_id}/prices/{price_id}", headers=headers)
        response.raise_for_status()
        return response.json()

    def update(self, product_id: str, price_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update Price by ID for a Product.
        Documentation - https://highlevel.stoplight.io/docs/integrations/7ffcf47b1687a-update-price-by-id-for-a-product

        Args:
            product_id (str): ID of the product
            price_id (str): ID of the price to update
            data (Dict[str, Any]): Updated price data

        Returns:
            Dict[str, Any]: API response containing updated price data
        """
        headers = self.auth_data.headers if self.auth_data else None
        response = requests.patch(f"{self.auth_data.baseurl}/products/{product_id}/prices/{price_id}", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_all(self, product_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List Prices for a Product.
        Documentation - https://highlevel.stoplight.io/docs/integrations/4f8b3c58c2e81-list-prices-for-a-product

        Args:
            product_id (str): ID of the product to list prices for
            params (Optional[Dict[str, Any]]): Query parameters for filtering prices
                - page (int): Page number
                - limit (int): Number of items per page
                - sort (str): Sort field
                - order (str): Sort order
                - active (bool): Filter by active status

        Returns:
            Dict[str, Any]: API response containing list of prices
        """
        headers = self.auth_data.headers if self.auth_data else None
        query_params = {}

        if params:
            if 'page' in params:
                query_params['page'] = params['page']
            if 'limit' in params:
                query_params['limit'] = params['limit']
            if 'sort' in params:
                query_params['sort'] = params['sort']
            if 'order' in params:
                query_params['order'] = params['order']
            if 'active' in params:
                query_params['active'] = params['active']

        response = requests.get(f"{self.auth_data.baseurl}/products/{product_id}/prices", params=query_params, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete(self, product_id: str, price_id: str) -> Dict[str, Any]:
        """
        Delete Price by ID for a Product.
        Documentation - https://highlevel.stoplight.io/docs/integrations/6025f28b731c1-delete-price-by-id-for-a-product

        Args:
            product_id (str): ID of the product
            price_id (str): ID of the price to delete

        Returns:
            Dict[str, Any]: API response containing deleted price data
        """
        headers = self.auth_data.headers if self.auth_data else None
        response = requests.delete(f"{self.auth_data.baseurl}/products/{product_id}/prices/{price_id}", headers=headers)
        response.raise_for_status()
        return response.json() 