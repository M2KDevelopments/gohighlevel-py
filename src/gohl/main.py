"""GoHighLevel API Python client.

This module provides the main GoHighLevel class for interacting with the GoHighLevel API,
including authentication, OAuth flow, and access to all API endpoints.
"""

from .classes.auth.authdata import Auth
from .classes.auth.credentials import Credentials
from .classes.blogs import Blog
from .classes.business import Business
from .classes.calendars import Calendar
from .classes.campaigns import CampaignAPI
from .classes.company import CompanyAPI
from .classes.contacts import Contacts
from .classes.workflows import Workflow
from .classes.conversations import Conversations
from .classes.courses import Course
from .classes.customfields import CustomFields
from .classes.custommenus import CustomMenus
from .classes.email import Email
from .classes.forms import Form
from .classes.location import Location
from .classes.medialibrary import MediaLibrary
from .classes.oauth import OAuth
from .classes.opportunities import Opportunities
from .classes.products import Product
from .classes.saas import SaaS
from .classes.snapshots import Snapshots
from .classes.subaccounts import SubAccounts
from .classes.surveys import Surveys
from .classes.triggerlinks import TriggerLinks
from .classes.users import Users


BASE_API_URL = 'https://rest.gohighlevel.com/v1'
PROD = "https://services.leadconnectorhq.com"
MOCK = "https://stoplight.io/mocks/highlevel/integrations/39582850"


class GoHighLevel:
    """Main class for interacting with the GoHighLevel API."""

    def __init__(self, credentials: Credentials):
        """Initialize the GoHighLevel client.
        
        Args:
            credentials (Credentials): Authentication credentials
        """
        self.credentials = credentials
        self.oauth = OAuth(credentials)
        
        # Initialize API endpoints if using API key
        if credentials.api_key:
            self.auth_data = Auth(
                access_token=credentials.api_key,
                refresh_token=credentials.api_key,
                use_api_key=True,
                baseurl=BASE_API_URL,
                headers={
                    'Version': '2021-04-15',
                    'Authorization': f'Bearer {credentials.api_key}',
                    'Accept': 'application/json'
                }
            )
            self._initialize_endpoints()

    def set_auth(self, auth_data: Auth) -> None:
        """Set the authorization data for the GoHighLevel account.
        
        This should be called after getting auth data from OAuth.get_callback_auth_tokens()
        
        Args:
            auth_data (Auth): Authentication data containing tokens and headers
        """
        self.auth_data = auth_data
        self.auth_data.baseurl = PROD
        self.auth_data.headers = {
            'Version': auth_data.headers.get('Version', '2021-04-15'),
            'Authorization': auth_data.headers.get('Authorization') or f'Bearer {auth_data.access_token}',
            'Accept': auth_data.headers.get('Accept', 'application/json')
        }
        self._initialize_endpoints()

    def set_test_mode(self, test: bool = False) -> None:
        """Set whether to use test mode (mock API) or production.
        
        Args:
            test (bool): Whether to use test mode
        """
        if not hasattr(self, 'auth_data'):
            raise ValueError("Authentication data must be set before changing test mode")
            
        self.auth_data.baseurl = MOCK if test else PROD
        self._initialize_endpoints()

    def _initialize_endpoints(self) -> None:
        """Initialize all API endpoint classes with current auth data."""
        self.calendar = Calendar(self.auth_data)
        self.contacts = Contacts(self.auth_data)
        self.conversations = Conversations(self.auth_data)
        self.medialibrary = MediaLibrary(self.auth_data)
        self.campaigns = CampaignAPI(self.auth_data)
        self.company = CompanyAPI(self.auth_data)
        self.links = TriggerLinks(self.auth_data)
        self.courses = Course(self.auth_data)
        self.businesses = Business(self.auth_data)
        self.workflows = Workflow(self.auth_data)
        self.surveys = Surveys(self.auth_data)
        self.blogs = Blog(self.auth_data)
        self.forms = Form(self.auth_data)
        self.subaccounts = SubAccounts(self.auth_data)
        self.agency = {
            'locations': Location(self.auth_data),
            'users': Users(self.auth_data)
        }
        self.custom_fields = CustomFields(self.auth_data)
        self.custom_menus = CustomMenus(self.auth_data)
        self.opportunities = Opportunities(self.auth_data)
        self.products = Product(self.auth_data)
        self.saas = SaaS(self.auth_data)
        self.snapshots = Snapshots(self.auth_data)
        self.email = Email(self.auth_data) 