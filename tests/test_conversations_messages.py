"""Unit tests for gohl.classes.conversations_messages.ConversationsMessages."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gohl.classes.conversations_messages import ConversationsMessages  # noqa: E402


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


class ConversationsMessagesInitTests(unittest.TestCase):
    def test_stores_auth_data(self):
        m = ConversationsMessages(AUTH)
        self.assertIs(m.auth_data, AUTH)

    def test_allows_none_auth_data(self):
        m = ConversationsMessages(None)
        self.assertIsNone(m.auth_data)

    def test_allows_omitted_auth_data(self):
        m = ConversationsMessages()
        self.assertIsNone(m.auth_data)


class _AuthValidationMixin:
    """Reusable auth-validation checks. Subclasses set `_call` to invoke the
    method under test on a ConversationsMessages built from the given auth."""

    def _call(self, messages):  # pragma: no cover - overridden
        raise NotImplementedError

    def test_raises_when_auth_data_none(self):
        with self.assertRaises(ValueError):
            self._call(ConversationsMessages(None))

    def test_raises_when_headers_missing(self):
        with self.assertRaises(ValueError):
            self._call(ConversationsMessages({"baseurl": AUTH["baseurl"]}))

    def test_raises_when_baseurl_missing(self):
        with self.assertRaises(ValueError):
            self._call(ConversationsMessages({"headers": AUTH["headers"]}))

    def test_raises_when_auth_data_empty(self):
        with self.assertRaises(ValueError):
            self._call(ConversationsMessages({}))


class GetAllTests(unittest.TestCase, _AuthValidationMixin):
    def _call(self, messages):
        return messages.get_all("conv_1")

    @patch("gohl.classes.conversations_messages.requests.get")
    def test_sends_expected_request_and_returns_messages(self, mock_get):
        mock_get.return_value = _mock_response(
            {"messages": [{"id": "m1"}, {"id": "m2"}]}
        )

        result = ConversationsMessages(AUTH).get_all("conv_1", limit=10, skip=5)

        mock_get.assert_called_once_with(
            f"{AUTH['baseurl']}/conversations/conv_1/messages",
            params={"limit": 10, "skip": 5},
            headers=AUTH["headers"],
        )
        self.assertEqual(result, [{"id": "m1"}, {"id": "m2"}])

    @patch("gohl.classes.conversations_messages.requests.get")
    def test_uses_default_limit_and_skip(self, mock_get):
        mock_get.return_value = _mock_response({"messages": []})

        ConversationsMessages(AUTH).get_all("conv_1")

        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs["params"], {"limit": 50, "skip": 0})

    @patch("gohl.classes.conversations_messages.requests.get")
    def test_returns_empty_list_when_no_messages(self, mock_get):
        mock_get.return_value = _mock_response({"messages": []})

        result = ConversationsMessages(AUTH).get_all("conv_1")

        self.assertEqual(result, [])

    @patch("gohl.classes.conversations_messages.requests.get")
    def test_raises_key_error_when_messages_key_missing(self, mock_get):
        mock_get.return_value = _mock_response({})

        with self.assertRaises(KeyError):
            ConversationsMessages(AUTH).get_all("conv_1")

    @patch("gohl.classes.conversations_messages.requests.get")
    def test_propagates_http_error(self, mock_get):
        mock_get.return_value = _http_error_response(500)

        with self.assertRaises(requests.exceptions.HTTPError):
            ConversationsMessages(AUTH).get_all("conv_1")

    @patch("gohl.classes.conversations_messages.requests.get")
    def test_propagates_http_error_404(self, mock_get):
        mock_get.return_value = _http_error_response(404)

        with self.assertRaises(requests.exceptions.HTTPError):
            ConversationsMessages(AUTH).get_all("missing_conv")


class AddTests(unittest.TestCase, _AuthValidationMixin):
    def _call(self, messages):
        return messages.add("conv_1", {"body": "hi", "type": "text"})

    @patch("gohl.classes.conversations_messages.requests.post")
    def test_sends_expected_request_and_returns_message(self, mock_post):
        message = {
            "body": "Hello! How can I help you today?",
            "type": "text",
            "attachments": [{"url": "https://example.com/file.pdf"}],
            "metadata": {"key": "value"},
        }
        mock_post.return_value = _mock_response(
            {"message": {"id": "m_new", **message}}
        )

        result = ConversationsMessages(AUTH).add("conv_1", message)

        mock_post.assert_called_once_with(
            f"{AUTH['baseurl']}/conversations/conv_1/messages",
            json=message,
            headers=AUTH["headers"],
        )
        self.assertEqual(result["id"], "m_new")
        self.assertEqual(result["body"], message["body"])

    @patch("gohl.classes.conversations_messages.requests.post")
    def test_forwards_message_payload_unchanged(self, mock_post):
        mock_post.return_value = _mock_response({"message": {"id": "m1"}})
        message = {"body": "minimal", "type": "text"}

        ConversationsMessages(AUTH).add("conv_1", message)

        _, kwargs = mock_post.call_args
        self.assertIs(kwargs["json"], message)

    @patch("gohl.classes.conversations_messages.requests.post")
    def test_raises_key_error_when_message_key_missing(self, mock_post):
        mock_post.return_value = _mock_response({})

        with self.assertRaises(KeyError):
            ConversationsMessages(AUTH).add("conv_1", {"body": "hi", "type": "text"})

    @patch("gohl.classes.conversations_messages.requests.post")
    def test_propagates_http_error(self, mock_post):
        mock_post.return_value = _http_error_response(400)

        with self.assertRaises(requests.exceptions.HTTPError):
            ConversationsMessages(AUTH).add("conv_1", {"body": "hi", "type": "text"})


class AddInboundTests(unittest.TestCase, _AuthValidationMixin):
    def _call(self, messages):
        return messages.add_inbound(
            {"type": "SMS", "conversationId": "conv_1", "message": "hi"}
        )

    @patch("gohl.classes.conversations_messages.requests.post")
    def test_sends_expected_request_and_returns_response(self, mock_post):
        message = {
            "type": "SMS",
            "conversationId": "conv_1",
            "conversationProviderId": "provider_1",
            "message": "Hello! How can I help you today?",
            "attachments": ["https://example.com/file.pdf"],
        }
        body = {
            "conversationId": "conv_1",
            "messageId": "m_new",
            "message": "Message added successfully",
        }
        mock_post.return_value = _mock_response(body)

        result = ConversationsMessages(AUTH).add_inbound(message)

        mock_post.assert_called_once_with(
            f"{AUTH['baseurl']}/conversations/messages/inbound",
            json=message,
            headers=AUTH["headers"],
        )
        self.assertEqual(result, body)

    @patch("gohl.classes.conversations_messages.requests.post")
    def test_targets_inbound_endpoint_not_nested_path(self, mock_post):
        mock_post.return_value = _mock_response({"messageId": "m1"})

        ConversationsMessages(AUTH).add_inbound({"type": "SMS", "contactId": "contact_1"})

        url, _ = mock_post.call_args
        self.assertEqual(
            url[0],
            f"{AUTH['baseurl']}/conversations/messages/inbound",
        )

    @patch("gohl.classes.conversations_messages.requests.post")
    def test_forwards_message_payload_unchanged(self, mock_post):
        mock_post.return_value = _mock_response({"messageId": "m1"})
        message = {"type": "SMS", "contactId": "contact_1"}

        ConversationsMessages(AUTH).add_inbound(message)

        _, kwargs = mock_post.call_args
        self.assertIs(kwargs["json"], message)

    @patch("gohl.classes.conversations_messages.requests.post")
    def test_returns_full_body_without_message_key(self, mock_post):
        body = {"conversationId": "conv_1", "messageId": "m1"}
        mock_post.return_value = _mock_response(body)

        result = ConversationsMessages(AUTH).add_inbound(
            {"type": "SMS", "conversationId": "conv_1"}
        )

        self.assertEqual(result, body)

    @patch("gohl.classes.conversations_messages.requests.post")
    def test_propagates_http_error(self, mock_post):
        mock_post.return_value = _http_error_response(400)

        with self.assertRaises(requests.exceptions.HTTPError):
            ConversationsMessages(AUTH).add_inbound(
                {"type": "SMS", "conversationId": "conv_1"}
            )


if __name__ == "__main__":
    unittest.main()
