"""Payments functionality for GoHighLevel API.

This module provides the Payments class for managing payment operations
in GoHighLevel, including orders, transactions, subscriptions, and more.
"""

from typing import Optional

from .auth.authdata import Auth
from .payments_integrations import PaymentIntegrations
from .payments_orders import PaymentOrders
from .payments_orderfulfillments import PaymentOrderFulfillments
from .payments_transactions import PaymentTransactions
from .payments_subscriptions import PaymentSubscriptions
from .payments_coupons import PaymentCoupons
from .payments_customproviders import PaymentCustomProviders


class Payments:
    """
    Endpoints For Payments
    https://highlevel.stoplight.io/docs/integrations/YXBpOjI1MDQ4Mjg-payments
    """
    
    def __init__(self, auth_data: Optional[Auth] = None):
        """Initialize the Payments class.
        
        Args:
            auth_data (Optional[Auth]): Authentication data containing headers and base URL
        """
        self.auth_data = auth_data
        self.integrations = PaymentIntegrations(auth_data)
        self.orders = PaymentOrders(auth_data)
        self.fulfillments = PaymentOrderFulfillments(auth_data)
        self.transactions = PaymentTransactions(auth_data)
        self.subscriptions = PaymentSubscriptions(auth_data)
        self.coupons = PaymentCoupons(auth_data)
        self.custom_providers = PaymentCustomProviders(auth_data) 