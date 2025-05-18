from .auth.authdata import Auth
from typing import Optional, List, Dict, Any
import requests


class Blog:
    """
    Endpoints For Blogs
    https://highlevel.stoplight.io/docs/integrations/4c364bc1d8c73-blogs-api
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        self.auth_data = auth_data

    def get_all_categories(self, location_id: str, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get All Blog Categories. The "Get all categories" Api return the blog categories for a given location ID.
        Please use "blogs/category.readonly"
        Documentation - https://highlevel.stoplight.io/docs/integrations/8ebd3128ee462-get-all-categories
        
        Args:
            location_id: The location ID
            limit: Number of categories to show in the listing (default: 20)
            offset: Number of categories to skip in listing (default: 0)
            
        Returns:
            List of blog categories
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/blogs/categories?locationId={location_id}&limit={limit}&offset={offset}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['categories']

    def get_all_authors(self, location_id: str, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get All Blog Authors. The "Get all authors" Api return the blog authors for a given location ID.
        Please use "blogs/author.readonly"
        Documentation - https://highlevel.stoplight.io/docs/integrations/8ebd3128ee462-get-all-categories
        
        Args:
            location_id: The location ID
            limit: Number of authors to show in the listing (default: 20)
            offset: Number of authors to skip in listing (default: 0)
            
        Returns:
            List of blog authors
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.get(
            f"{self.auth_data.baseurl}/blogs/authors?locationId={location_id}&limit={limit}&offset={offset}",
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['authors']

    def add(self, blog: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Blog
        Documentation - https://highlevel.stoplight.io/docs/integrations/c24ff055e7cf8-create-blog-post
        
        Args:
            blog: Blog information to create
            
        Returns:
            Created blog information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.post(
            f"{self.auth_data.baseurl}/blogs",
            json=blog,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['data']

    def update(self, blog_id: str, blog: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update Blog. The "Update Blog Post" API allows you create blog post for any given blog site.
        Please use blogs/post-update.write
        Documentation - https://highlevel.stoplight.io/docs/integrations/9ac5fb40f9fb4-update-blog-post
        
        Args:
            blog_id: The blog ID to update
            blog: Updated blog information
            
        Returns:
            Updated blog information
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        response = requests.put(
            f"{self.auth_data.baseurl}/blogs/{blog_id}",
            json=blog,
            headers=self.auth_data.headers
        )
        response.raise_for_status()
        return response.json()['blog']

    def is_slug_url_exists(self, location_id: str, url_slug: str, post_id: str = "") -> bool:
        """
        Check url slug. The "Check url slug" API allows check the blog slug validation which is needed before publishing any blog post.
        Please use blogs/check-slug.readonly. you can find the POST ID from the post edit url.
        Documentation - https://highlevel.stoplight.io/docs/integrations/6f776fbd6dd1f-delete-blog
        
        Args:
            location_id: The location ID
            url_slug: The URL slug to check
            post_id: Optional post ID (default: "")
            
        Returns:
            True if the slug URL exists, False otherwise
        """
        if not self.auth_data:
            raise ValueError("Authentication data is required")
            
        url = f"{self.auth_data.baseurl}/blogs/posts/url-slug-exists?locationId={location_id}&urlSlug={url_slug}"
        if post_id:
            url += f"&postId={post_id}"
            
        response = requests.delete(url, headers=self.auth_data.headers)
        response.raise_for_status()
        return response.json()['exists'] 