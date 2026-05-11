"""Unit tests for the gohl.classes.auth package.

Covers Auth (authdata.py), CallbackInfo (callback.py), and Credentials (credentials.py).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gohl.classes.auth.authdata import Auth  # noqa: E402
from gohl.classes.auth.callback import CallbackInfo  # noqa: E402
from gohl.classes.auth.credentials import Credentials  # noqa: E402


class AuthTests(unittest.TestCase):
    def test_stores_all_fields_verbatim(self):
        custom_headers = {"X-Custom": "value"}
        auth = Auth(
            access_token="tok",
            refresh_token="refresh",
            location_id="loc_1",
            company_id="co_1",
            expires_in=3600,
            user_type="Company",
            use_api_key=True,
            baseurl="https://example.com",
            scope="contacts.readonly",
            headers=custom_headers,
        )

        self.assertEqual(auth.access_token, "tok")
        self.assertEqual(auth.refresh_token, "refresh")
        self.assertEqual(auth.location_id, "loc_1")
        self.assertEqual(auth.company_id, "co_1")
        self.assertEqual(auth.expires_in, 3600)
        self.assertEqual(auth.user_type, "Company")
        self.assertTrue(auth.use_api_key)
        self.assertEqual(auth.baseurl, "https://example.com")
        self.assertEqual(auth.scope, "contacts.readonly")
        self.assertIs(auth.headers, custom_headers)

    def test_optional_fields_default_to_none(self):
        auth = Auth(access_token="tok")

        self.assertEqual(auth.access_token, "tok")
        self.assertIsNone(auth.refresh_token)
        self.assertIsNone(auth.location_id)
        self.assertIsNone(auth.company_id)
        self.assertIsNone(auth.expires_in)
        self.assertIsNone(auth.user_type)
        self.assertFalse(auth.use_api_key)
        self.assertIsNone(auth.baseurl)
        self.assertIsNone(auth.scope)

    def test_headers_default_uses_access_token_in_bearer(self):
        auth = Auth(access_token="my_token")

        self.assertEqual(
            auth.headers,
            {
                "Version": "2021-04-15",
                "Authorization": "Bearer my_token",
                "Accept": "application/json",
            },
        )

    def test_headers_none_falls_back_to_default(self):
        auth = Auth(access_token="tok", headers=None)

        self.assertEqual(auth.headers["Authorization"], "Bearer tok")
        self.assertEqual(auth.headers["Version"], "2021-04-15")
        self.assertEqual(auth.headers["Accept"], "application/json")

    def test_empty_dict_headers_falls_back_to_default(self):
        # `headers or {...}` treats {} as falsy and replaces it with the default.
        auth = Auth(access_token="tok", headers={})

        self.assertEqual(auth.headers["Authorization"], "Bearer tok")

    def test_custom_headers_override_default(self):
        auth = Auth(
            access_token="tok",
            headers={"Authorization": "Bearer override", "X-Extra": "y"},
        )

        self.assertEqual(auth.headers["Authorization"], "Bearer override")
        self.assertEqual(auth.headers["X-Extra"], "y")
        self.assertNotIn("Version", auth.headers)


class CallbackInfoTests(unittest.TestCase):
    def test_stores_code_and_refresh_token(self):
        info = CallbackInfo(code="abc123", refresh_token="r1")

        self.assertEqual(info.code, "abc123")
        self.assertEqual(info.refresh_token, "r1")

    def test_defaults_are_none(self):
        info = CallbackInfo()

        self.assertIsNone(info.code)
        self.assertIsNone(info.refresh_token)

    def test_get_code_returns_stored_value(self):
        self.assertEqual(CallbackInfo(code="abc").get_code(), "abc")
        self.assertIsNone(CallbackInfo().get_code())

    def test_get_refresh_token_returns_stored_value(self):
        self.assertEqual(CallbackInfo(refresh_token="r1").get_refresh_token(), "r1")
        self.assertIsNone(CallbackInfo().get_refresh_token())


class CredentialsTests(unittest.TestCase):
    def test_stores_all_fields_verbatim(self):
        scopes = ["contacts.readonly", "contacts.write"]
        creds = Credentials(
            client_id="cid",
            client_secret="secret",
            redirect_uri="https://app.example.com/callback",
            scopes=scopes,
            is_white_label=True,
            api_key="key",
            user_type="Company",
        )

        self.assertEqual(creds.client_id, "cid")
        self.assertEqual(creds.client_secret, "secret")
        self.assertEqual(creds.redirect_uri, "https://app.example.com/callback")
        self.assertIs(creds.scopes, scopes)
        self.assertTrue(creds.is_white_label)
        self.assertEqual(creds.api_key, "key")
        self.assertEqual(creds.user_type, "Company")

    def test_defaults_when_nothing_provided(self):
        creds = Credentials()

        self.assertIsNone(creds.client_id)
        self.assertIsNone(creds.client_secret)
        self.assertIsNone(creds.redirect_uri)
        self.assertEqual(creds.scopes, [])
        self.assertFalse(creds.is_white_label)
        self.assertIsNone(creds.api_key)
        self.assertEqual(creds.user_type, "Location")

    def test_scopes_none_becomes_empty_list(self):
        self.assertEqual(Credentials(scopes=None).scopes, [])

    def test_user_type_none_falls_back_to_location(self):
        # `user_type or "Location"` replaces None and any falsy value.
        self.assertEqual(Credentials(user_type=None).user_type, "Location")
        self.assertEqual(Credentials(user_type="").user_type, "Location")

    def test_api_key_only_construction(self):
        creds = Credentials(api_key="key")

        self.assertEqual(creds.api_key, "key")
        self.assertIsNone(creds.client_id)
        self.assertIsNone(creds.client_secret)


if __name__ == "__main__":
    unittest.main()
