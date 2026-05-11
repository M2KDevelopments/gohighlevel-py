"""Unit tests for gohl.classes.conversations.Conversations."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gohl.classes.conversations import Conversations  # noqa: E402
from gohl.classes.conversations_email import ConversationsEmail  # noqa: E402
from gohl.classes.conversations_messages import ConversationsMessages  # noqa: E402
from gohl.classes.conversations_providers import ConversationsProviders  # noqa: E402


AUTH = {
    "baseurl": "https://services.leadconnectorhq.com",
    "headers": {
        "Authorization": "Bearer token",
        "Version": "2021-04-15",
    },
}


def _mock_response(json_body, status_code=200):
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status_code
    resp.json.return_value = json_body
    resp.raise_for_status = MagicMock()
    return resp


def _http_error_response(status_code=400):
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status_code
    resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
        f"{status_code} error"
    )
    return resp


class ConversationsInitTests(unittest.TestCase):
    def test_stores_auth_data_and_sub_resources(self):
        c = Conversations(AUTH)
        self.assertIs(c.auth_data, AUTH)
        self.assertIsInstance(c.email, ConversationsEmail)
        self.assertIsInstance(c.messages, ConversationsMessages)
        self.assertIsInstance(c.providers, ConversationsProviders)
        self.assertIs(c.email.auth_data, AUTH)
        self.assertIs(c.messages.auth_data, AUTH)
        self.assertIs(c.providers.auth_data, AUTH)

    def test_allows_none_auth_data(self):
        c = Conversations(None)
        self.assertIsNone(c.auth_data)
        self.assertIsInstance(c.email, ConversationsEmail)


class _AuthValidationMixin:
    """Reusable auth-validation checks. Subclasses set `call` to a no-arg lambda
    that invokes the method under test on a Conversations built from the given auth."""

    method_name = ""

    def _call(self, conv):  # pragma: no cover - overridden
        raise NotImplementedError

    def test_raises_when_auth_data_none(self):
        conv = Conversations(None)
        with self.assertRaises(ValueError):
            self._call(conv)

    def test_raises_when_headers_missing(self):
        conv = Conversations({"baseurl": AUTH["baseurl"]})
        with self.assertRaises(ValueError):
            self._call(conv)

    def test_raises_when_baseurl_missing(self):
        conv = Conversations({"headers": AUTH["headers"]})
        with self.assertRaises(ValueError):
            self._call(conv)


class GetAllTests(unittest.TestCase, _AuthValidationMixin):
    def _call(self, conv):
        return conv.get_all("loc_1")

    @patch("gohl.classes.conversations.requests.get")
    def test_sends_expected_request_and_returns_conversations(self, mock_get):
        mock_get.return_value = _mock_response(
            {"conversations": [{"id": "c1"}, {"id": "c2"}]}
        )
        conv = Conversations(AUTH)

        result = conv.get_all("loc_1", limit=10, skip=5)

        mock_get.assert_called_once_with(
            f"{AUTH['baseurl']}/conversations",
            params={"locationId": "loc_1", "limit": 10, "skip": 5},
            headers=AUTH["headers"],
        )
        self.assertEqual(result, [{"id": "c1"}, {"id": "c2"}])

    @patch("gohl.classes.conversations.requests.get")
    def test_uses_default_limit_and_skip(self, mock_get):
        mock_get.return_value = _mock_response({"conversations": []})
        Conversations(AUTH).get_all("loc_1")

        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs["params"], {"locationId": "loc_1", "limit": 50, "skip": 0})

    @patch("gohl.classes.conversations.requests.get")
    def test_propagates_http_error(self, mock_get):
        mock_get.return_value = _http_error_response(500)
        with self.assertRaises(requests.exceptions.HTTPError):
            Conversations(AUTH).get_all("loc_1")


class GetTests(unittest.TestCase, _AuthValidationMixin):
    def _call(self, conv):
        return conv.get("conv_1")

    @patch("gohl.classes.conversations.requests.get")
    def test_sends_expected_request_and_returns_conversation(self, mock_get):
        mock_get.return_value = _mock_response({"conversation": {"id": "conv_1"}})

        result = Conversations(AUTH).get("conv_1")

        mock_get.assert_called_once_with(
            f"{AUTH['baseurl']}/conversations/conv_1",
            headers=AUTH["headers"],
        )
        self.assertEqual(result, {"id": "conv_1"})

    @patch("gohl.classes.conversations.requests.get")
    def test_propagates_http_error(self, mock_get):
        mock_get.return_value = _http_error_response(404)
        with self.assertRaises(requests.exceptions.HTTPError):
            Conversations(AUTH).get("conv_1")


class CreateTests(unittest.TestCase, _AuthValidationMixin):
    def _call(self, conv):
        return conv.create("loc_1", "contact_1")

    @patch("gohl.classes.conversations.requests.post")
    def test_sends_expected_request_and_returns_conversation(self, mock_post):
        mock_post.return_value = _mock_response(
            {"conversation": {"id": "conv_new", "contactId": "contact_1"}}
        )

        result = Conversations(AUTH).create("loc_1", "contact_1")

        mock_post.assert_called_once_with(
            f"{AUTH['baseurl']}/conversations/",
            json={"locationId": "loc_1", "contactId": "contact_1"},
            headers=AUTH["headers"],
        )
        self.assertEqual(result, {"id": "conv_new", "contactId": "contact_1"})

    @patch("gohl.classes.conversations.requests.post")
    def test_propagates_http_error(self, mock_post):
        mock_post.return_value = _http_error_response(400)
        with self.assertRaises(requests.exceptions.HTTPError):
            Conversations(AUTH).create("loc_1", "contact_1")


class UpdateTests(unittest.TestCase, _AuthValidationMixin):
    def _call(self, conv):
        return conv.update("conv_1", {"starred": True})

    @patch("gohl.classes.conversations.requests.put")
    def test_sends_expected_request_and_returns_conversation(self, mock_put):
        payload = {"starred": True, "unreadCount": 0}
        mock_put.return_value = _mock_response({"conversation": {"id": "conv_1", **payload}})

        result = Conversations(AUTH).update("conv_1", payload)

        mock_put.assert_called_once_with(
            f"{AUTH['baseurl']}/conversations/conv_1",
            json=payload,
            headers=AUTH["headers"],
        )
        self.assertEqual(result["id"], "conv_1")
        self.assertTrue(result["starred"])

    @patch("gohl.classes.conversations.requests.put")
    def test_propagates_http_error(self, mock_put):
        mock_put.return_value = _http_error_response(400)
        with self.assertRaises(requests.exceptions.HTTPError):
            Conversations(AUTH).update("conv_1", {"starred": True})


class SearchTests(unittest.TestCase, _AuthValidationMixin):
    def _call(self, conv):
        return conv.search("loc_1", "hello")

    @patch("gohl.classes.conversations.requests.post")
    def test_sends_query_without_filters(self, mock_post):
        mock_post.return_value = _mock_response({"conversations": [{"id": "c1"}]})

        result = Conversations(AUTH).search("loc_1", "hello")

        mock_post.assert_called_once_with(
            f"{AUTH['baseurl']}/conversations/search",
            json={"locationId": "loc_1", "query": "hello"},
            headers=AUTH["headers"],
        )
        self.assertEqual(result, [{"id": "c1"}])

    @patch("gohl.classes.conversations.requests.post")
    def test_includes_filters_when_provided(self, mock_post):
        mock_post.return_value = _mock_response({"conversations": []})
        filters = {
            "status": "open",
            "dateRange": {"startDate": "2026-01-01", "endDate": "2026-05-01"},
        }

        Conversations(AUTH).search("loc_1", "hello", filters=filters)

        _, kwargs = mock_post.call_args
        self.assertEqual(
            kwargs["json"],
            {"locationId": "loc_1", "query": "hello", "filters": filters},
        )

    @patch("gohl.classes.conversations.requests.post")
    def test_propagates_http_error(self, mock_post):
        mock_post.return_value = _http_error_response(401)
        with self.assertRaises(requests.exceptions.HTTPError):
            Conversations(AUTH).search("loc_1", "hello")


if __name__ == "__main__":
    unittest.main()
