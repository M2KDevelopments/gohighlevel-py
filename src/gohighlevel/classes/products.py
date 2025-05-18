from typing import Optional, Dict, Any
import requests
from .auth.authdata import Auth
from .products_prices import ProductPrice

class Product:
    """
    Products class for managing products in GoHighLevel.
    """
    
    def __init__(self, auth_data: Optional[Auth] = None) -> None:
        """
        Initialize Products class.

        Args:
            auth_data (Optional[Auth]): Authentication data for API requests
        """
        self.auth_data = auth_data
        self.prices = ProductPrice(auth_data)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Product.
        Documentation - https://highlevel.stoplight.io/docs/integrations/9eda2dc176c9c-create-product

        Args:
            data (Dict[str, Any]): Product data to create

        Returns:
            Dict[str, Any]: API response containing created product data
        """
        headers = self.auth_data.headers if self.auth_data else None
        response = requests.post(f"{self.auth_data.baseurl}/products", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def get(self, product_id: str) -> Dict[str, Any]:
        """
        Get Product by ID.
        Documentation - https://highlevel.stoplight.io/docs/integrations/272e8f008adb0-get-product-by-id

        Args:
            product_id (str): ID of the product to retrieve

        Returns:
            Dict[str, Any]: API response containing product data
        """
        headers = self.auth_data.headers if self.auth_data else None
        response = requests.get(f"{self.auth_data.baseurl}/products/{product_id}", headers=headers)
        response.raise_for_status()
        return response.json()

    def update(self, product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update Product.
        Documentation - https://highlevel.stoplight.io/docs/integrations/469d7a90e0d15-update-product-by-id

        Args:
            product_id (str): ID of the product to update
            data (Dict[str, Any]): Updated product data

        Returns:
            Dict[str, Any]: API response containing updated product data
        """
        headers = self.auth_data.headers if self.auth_data else None
        response = requests.patch(f"{self.auth_data.baseurl}/products/{product_id}", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_all(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        List Products.
        Documentation - https://highlevel.stoplight.io/docs/integrations/7f6ce42d09400-list-products

        Args:
            params (Optional[Dict[str, Any]]): Query parameters for filtering products
                - page (int): Page number
                - limit (int): Number of items per page
                - sort (str): Sort field
                - order (str): Sort order
                - active (bool): Filter by active status

        Returns:
            Dict[str, Any]: API response containing list of products
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

        response = requests.get(f"{self.auth_data.baseurl}/products", params=query_params, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete(self, product_id: str) -> Dict[str, Any]:
        """
        Delete Product.
        Documentation - https://highlevel.stoplight.io/docs/integrations/285e8c049b2e1-delete-product-by-id

        Args:
            product_id (str): ID of the product to delete

        Returns:
            Dict[str, Any]: API response containing deleted product data
        """
        headers = self.auth_data.headers if self.auth_data else None
        response = requests.delete(f"{self.auth_data.baseurl}/products/{product_id}", headers=headers)
        response.raise_for_status()
        return response.json() 