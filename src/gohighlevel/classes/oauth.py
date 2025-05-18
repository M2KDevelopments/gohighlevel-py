"""OAuth functionality for GoHighLevel API.

This module provides the OAuth class for handling authentication and authorization
with the GoHighLevel API, including OAuth flow and scope management.
"""

from typing import Optional
import requests
from urllib.parse import urlencode

from .auth.authdata import Auth
from .auth.callback import CallbackInfo
from .auth.credentials import Credentials


class OAuth:
    """
    OAuth management class for GoHighLevel API.
    https://highlevel.stoplight.io/docs/integrations/a04191c0fabf9-authorization
    """
    
    def __init__(self, credentials: Optional[Credentials] = None):
        """Initialize the OAuth class.
        
        Args:
            credentials (Optional[Credentials]): Authentication credentials containing client ID, secret, etc.
        """
        self.credentials = credentials

    def get_oauth_url(self) -> str:
        """Get the OAuth URL for authorization.
        
        Documentation: https://highlevel.stoplight.io/docs/integrations/a04191c0fabf9-authorization
        You can set up an app in GoHighLevel Marketplace - https://marketplace.gohighlevel.com/
        
        Returns:
            str: The OAuth URL for authorization
            
        Raises:
            ValueError: If credentials are missing
        """
        if not self.credentials:
            raise ValueError("Credentials are required")
            
        client_id = self.credentials.client_id
        redirect_uri = self.credentials.redirect_uri or ""
        scope = " ".join(self.credentials.scopes or [])
        
        params = {
            'client_id': client_id,
            'response_type': 'code',
            'scope': scope,
            'redirect_uri': redirect_uri
        }
        
        domain = 'leadconnectorhq' if self.credentials.is_white_label else 'gohighlevel'
        return f'https://marketplace.{domain}.com/oauth/chooselocation?{urlencode(params)}'

    def get_callback_auth_tokens(self, info: CallbackInfo) -> Auth:
        """Get authentication tokens from callback information.
        
        Args:
            info (CallbackInfo): Callback information containing code or refresh token
            
        Returns:
            Auth: Authentication data including tokens and headers
            
        Raises:
            ValueError: If neither code nor refresh token is provided
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.credentials:
            raise ValueError("Credentials are required")
            
        if not info.code and not info.refresh_token:
            raise ValueError("Please provide either a code or refresh token")

        if info.code:
            data = {
                'grant_type': 'authorization_code',
                'client_id': self.credentials.client_id,
                'client_secret': self.credentials.client_secret,
                'code': info.code
            }
        else:
            data = {
                'grant_type': 'refresh_token',
                'client_id': self.credentials.client_id,
                'client_secret': self.credentials.client_secret,
                'refresh_token': info.refresh_token
            }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        try:
            response = requests.post('https://api.msgsndr.com/oauth/token', data=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            return Auth(
                access_token=result['access_token'],
                refresh_token=info.refresh_token or result.get('refresh_token'),
                expires_in=int(result['expires_in']),
                scope=result.get('scope'),
                location_id=result.get('locationId'),
                company_id=result.get('companyId'),
                user_type=result.get('userType'),
                headers={
                    'Version': '2021-04-15',
                    'Authorization': f'Bearer {result["access_token"]}',
                    'Accept': 'application/json'
                }
            )
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'json'):
                error_msg = e.response.json().get('message', str(e))
            else:
                error_msg = str(e)
            raise ValueError(f"OAuth token request failed: {error_msg}") from e

    def _add_scope(self, scope: str) -> 'OAuth':
        """Add a scope to the credentials.
        
        Args:
            scope (str): The scope to add
            
        Returns:
            OAuth: The OAuth instance for method chaining
        """
        if not self.credentials:
            self.credentials = Credentials()
        
        if not self.credentials.scopes:
            self.credentials.scopes = []
            
        if scope not in self.credentials.scopes:
            self.credentials.scopes.append(scope)
        
        return self

    def scope_all(self) -> None:
        """Add all available scopes to the credentials."""
        self.credentials.scopes = [
            'companies.readonly',
            'conversations.readonly',
            'links.write',
            'links.readonly',
            'calendars.write',
            'calendars.readonly',
            'calendars/events.readonly',
            'calendars/events.write',
            'calendars/groups.readonly',
            'calendars/groups.write',
            'calendars/resources.readonly',
            'calendars/resources.write',
            'locations.write',
            'locations/customFields.readonly',
            'locations/customValues.write',
            'locations/customFields.write',
            'locations/customValues.readonly',
            'locations/tags.write',
            'locations/tags.readonly',
            'locations.readonly',
            'opportunities.readonly',
            'opportunities.write',
            'businesses.readonly',
            'businesses.write',
            'contacts.readonly',
            'contacts.write',
            'locations/tasks.readonly',
            'locations/tasks.write'
        ]

    # Blogs
    def scope_blogs_post(self) -> 'OAuth': return self._add_scope("blogs/post.write")
    def scope_blogs_post_update(self) -> 'OAuth': return self._add_scope("blogs/post-update.write")
    def scope_blogs_check_slug(self) -> 'OAuth': return self._add_scope("blogs/check-slug.readonly")
    def scope_blogs_category(self) -> 'OAuth': return self._add_scope("blogs/category.readonly")
    def scope_blogs_author(self) -> 'OAuth': return self._add_scope("blogs/author.readonly")

    # Businesses
    def scope_businesses(self) -> 'OAuth': return self._add_scope("businesses.readonly")
    def scope_businesses_write(self) -> 'OAuth': return self._add_scope("businesses.write")

    # Companies
    def scope_companies(self) -> 'OAuth': return self._add_scope("companies.readonly")

    # Calendars
    def scope_calendars(self) -> 'OAuth': return self._add_scope("calendars.readonly")
    def scope_calendars_write(self) -> 'OAuth': return self._add_scope("calendars.write")
    def scope_calendars_events(self) -> 'OAuth': return self._add_scope("calendars/events.readonly")
    def scope_calendars_events_write(self) -> 'OAuth': return self._add_scope("calendars/events.write")
    def scope_calendars_groups(self) -> 'OAuth': return self._add_scope("calendars/groups.readonly")
    def scope_calendars_groups_write(self) -> 'OAuth': return self._add_scope("calendars/groups.write")
    def scope_calendars_resources(self) -> 'OAuth': return self._add_scope("calendars/resources.readonly")
    def scope_calendars_resources_write(self) -> 'OAuth': return self._add_scope("calendars/resources.write")

    # Contacts
    def scope_contacts(self) -> 'OAuth': return self._add_scope("contacts.readonly")
    def scope_contacts_write(self) -> 'OAuth': return self._add_scope("contacts.write")

    # Conversations
    def scope_conversations(self) -> 'OAuth': return self._add_scope("conversations.readonly")
    def scope_conversations_write(self) -> 'OAuth': return self._add_scope("conversations.write")
    def scope_conversations_messages(self) -> 'OAuth': return self._add_scope("conversations/message.readonly")
    def scope_conversations_messages_write(self) -> 'OAuth': return self._add_scope("conversations/message.write")
    def scope_conversations_reports(self) -> 'OAuth': return self._add_scope("conversations/reports.write")

    # Courses
    def scope_courses(self) -> 'OAuth': return self._add_scope("courses.readonly")
    def scope_courses_write(self) -> 'OAuth': return self._add_scope("courses.write")

    # Forms
    def scope_forms(self) -> 'OAuth': return self._add_scope("forms.readonly")
    def scope_forms_write(self) -> 'OAuth': return self._add_scope("forms.write")

    # Funnels
    def scope_funnels_redirect(self) -> 'OAuth': return self._add_scope("funnels/redirect.readonly")
    def scope_funnels_redirect_write(self) -> 'OAuth': return self._add_scope("funnels/redirect.write")
    def scope_funnels_page(self) -> 'OAuth': return self._add_scope("funnels/page.readonly")
    def scope_funnels_page_count(self) -> 'OAuth': return self._add_scope("funnels/pagecount.readonly")
    def scope_funnels_funnel(self) -> 'OAuth': return self._add_scope("funnels/funnel.readonly")

    # Locations
    def scope_locations(self) -> 'OAuth': return self._add_scope("locations.readonly")
    def scope_locations_write(self) -> 'OAuth': return self._add_scope("locations.write")
    def scope_locations_custom_values(self) -> 'OAuth': return self._add_scope("locations/customValues.readonly")
    def scope_locations_custom_values_write(self) -> 'OAuth': return self._add_scope("locations/customValues.write")
    def scope_locations_custom_fields(self) -> 'OAuth': return self._add_scope("locations/customFields.readonly")
    def scope_locations_custom_fields_write(self) -> 'OAuth': return self._add_scope("locations/customFields.write")
    def scope_locations_tasks(self) -> 'OAuth': return self._add_scope("locations/tasks.readonly")
    def scope_locations_tasks_write(self) -> 'OAuth': return self._add_scope("locations/tasks.write")
    def scope_locations_tags(self) -> 'OAuth': return self._add_scope("locations/tags.readonly")
    def scope_locations_tags_write(self) -> 'OAuth': return self._add_scope("locations/tags.write")
    def scope_locations_templates(self) -> 'OAuth': return self._add_scope("locations/templates.readonly")

    # LC-Email
    def scope_lc_email(self) -> 'OAuth': return self._add_scope("lc-email.readonly")

    # Media
    def scope_media(self) -> 'OAuth': return self._add_scope("medias.readonly")
    def scope_media_write(self) -> 'OAuth': return self._add_scope("medias.write")

    # Payments
    def scope_payments_orders(self) -> 'OAuth': return self._add_scope("payments/orders.readonly")
    def scope_payments_orders_write(self) -> 'OAuth': return self._add_scope("payments/orders.write")
    def scope_payments_integration(self) -> 'OAuth': return self._add_scope("payments/integration.readonly")
    def scope_payments_integration_write(self) -> 'OAuth': return self._add_scope("payments/integration.write")
    def scope_payments_transactions(self) -> 'OAuth': return self._add_scope("payments/transactions.readonly")
    def scope_payments_subscriptions(self) -> 'OAuth': return self._add_scope("payments/subscriptions.readonly")
    def scope_payments_custom_provider(self) -> 'OAuth': return self._add_scope("payments/custom-provider.readonly")
    def scope_payments_custom_provider_write(self) -> 'OAuth': return self._add_scope("payments/custom-provider.write")

    # Products
    def scope_products(self) -> 'OAuth': return self._add_scope("products.readonly")
    def scope_products_write(self) -> 'OAuth': return self._add_scope("products.write")
    def scope_products_prices(self) -> 'OAuth': return self._add_scope("products/prices.readonly")
    def scope_products_prices_write(self) -> 'OAuth': return self._add_scope("products/prices.write")
    def scope_products_collection(self) -> 'OAuth': return self._add_scope("products/collection.readonly")
    def scope_products_collection_write(self) -> 'OAuth': return self._add_scope("products/collection.write")

    # OAuth
    def scope_oauth(self) -> 'OAuth': return self._add_scope("oauth.readonly")
    def scope_oauth_write(self) -> 'OAuth': return self._add_scope("oauth.write")

    # Objects
    def scope_objects_schema(self) -> 'OAuth': return self._add_scope("objects/schema.readonly")
    def scope_objects_schema_write(self) -> 'OAuth': return self._add_scope("objects/schema.write")
    def scope_objects_record(self) -> 'OAuth': return self._add_scope("objects/record.readonly")
    def scope_objects_record_write(self) -> 'OAuth': return self._add_scope("objects/record.write")

    # Opportunities
    def scope_opportunities(self) -> 'OAuth': return self._add_scope("opportunities.readonly")
    def scope_opportunities_write(self) -> 'OAuth': return self._add_scope("opportunities.write")

    # SaaS
    def scope_saas_company(self) -> 'OAuth': return self._add_scope("saas/company.readonly")
    def scope_saas_company_write(self) -> 'OAuth': return self._add_scope("saas/company.write")
    def scope_saas_location(self) -> 'OAuth': return self._add_scope("saas/location.readonly")
    def scope_saas_location_write(self) -> 'OAuth': return self._add_scope("saas/location.write")

    # Snapshots
    def scope_snapshots(self) -> 'OAuth': return self._add_scope("snapshots.readonly")
    def scope_snapshots_write(self) -> 'OAuth': return self._add_scope("snapshots.write")

    # Store
    def scope_store_shipping(self) -> 'OAuth': return self._add_scope("store/shipping.readonly")
    def scope_store_shipping_write(self) -> 'OAuth': return self._add_scope("store/shipping.write")
    def scope_store_setting(self) -> 'OAuth': return self._add_scope("store/setting.readonly")
    def scope_store_setting_write(self) -> 'OAuth': return self._add_scope("store/setting.write")

    # Surveys
    def scope_surveys(self) -> 'OAuth': return self._add_scope("surveys.readonly")

    # Users
    def scope_users(self) -> 'OAuth': return self._add_scope("users.readonly")
    def scope_users_write(self) -> 'OAuth': return self._add_scope("users.write")

    # WordPress Site
    def scope_wordpress_site(self) -> 'OAuth': return self._add_scope("wordpress.site.readonly")

    # Workflows
    def scope_workflows(self) -> 'OAuth': return self._add_scope("workflows.readonly") 