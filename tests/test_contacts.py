"""Unit tests for gohl.classes.contacts.Contacts."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gohl.classes.auth.authdata import Auth  # noqa: E402
from gohl.classes.contacts import Contacts  # noqa: E402
from gohl.classes.contacts_appointments import Appointment  # noqa: E402
from gohl.classes.contacts_campaigns import Campaign  # noqa: E402
from gohl.classes.contacts_notes import Note  # noqa: E402
from gohl.classes.contacts_tags import Tag  # noqa: E402
from gohl.classes.contacts_tasks import Task  # noqa: E402
from gohl.classes.contacts_workflows import ContactsWorkflows  # noqa: E402


def _api_key_auth():
    return Auth(
        access_token="api_key_value",
        use_api_key=True,
        baseurl="https://rest.gohighlevel.com/v1",
        location_id="loc_default",
    )


def _oauth_auth():
    return Auth(
        access_token="oauth_token",
        use_api_key=False,
        baseurl="https://services.leadconnectorhq.com",
        location_id="loc_default",
    )


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


class ContactsInitTests(unittest.TestCase):
    def test_stores_auth_data_and_sub_resources(self):
        auth = _oauth_auth()
        c = Contacts(auth)

        self.assertIs(c.auth_data, auth)
        self.assertIsInstance(c.appointments, Appointment)
        self.assertIsInstance(c.campaigns, Campaign)
        self.assertIsInstance(c.workflows, ContactsWorkflows)
        self.assertIsInstance(c.tasks, Task)
        self.assertIsInstance(c.notes, Note)
        self.assertIsInstance(c.tags, Tag)
        self.assertIs(c.appointments.auth_data, auth)
        self.assertIs(c.campaigns.auth_data, auth)
        self.assertIs(c.workflows.auth_data, auth)
        self.assertIs(c.tasks.auth_data, auth)
        self.assertIs(c.notes.auth_data, auth)
        self.assertIs(c.tags.auth_data, auth)

    def test_allows_none_auth_data(self):
        c = Contacts(None)
        self.assertIsNone(c.auth_data)
        self.assertIsInstance(c.appointments, Appointment)


class GetTests(unittest.TestCase):
    @patch("gohl.classes.contacts.requests.get")
    def test_builds_url_with_location_id_only(self, mock_get):
        auth = _oauth_auth()
        mock_get.return_value = _mock_response({"count": 0, "contacts": []})

        result = Contacts(auth).get("loc_1")

        mock_get.assert_called_once_with(
            f"{auth.baseurl}/contacts?locationId=loc_1",
            headers=auth.headers,
        )
        self.assertEqual(result, {"count": 0, "contacts": []})

    @patch("gohl.classes.contacts.requests.get")
    def test_builds_url_with_all_filters(self, mock_get):
        auth = _oauth_auth()
        mock_get.return_value = _mock_response(
            {"count": 1, "contacts": [{"id": "c1"}]}
        )

        Contacts(auth).get(
            "loc_1",
            filters={
                "query": "alice",
                "startAfter": "100",
                "startAfterId": "id_1",
                "limit": 25,
            },
        )

        mock_get.assert_called_once_with(
            f"{auth.baseurl}/contacts?locationId=loc_1&query=alice&startAfter=100&startAfterId=id_1&limit=25",
            headers=auth.headers,
        )

    @patch("gohl.classes.contacts.requests.get")
    def test_ignores_empty_or_missing_filter_values(self, mock_get):
        auth = _oauth_auth()
        mock_get.return_value = _mock_response({"count": 0, "contacts": []})

        Contacts(auth).get("loc_1", filters={"query": "", "limit": 0})

        mock_get.assert_called_once_with(
            f"{auth.baseurl}/contacts?locationId=loc_1",
            headers=auth.headers,
        )

    @patch("gohl.classes.contacts.requests.get")
    def test_propagates_http_error(self, mock_get):
        mock_get.return_value = _http_error_response(500)
        with self.assertRaises(requests.exceptions.HTTPError):
            Contacts(_oauth_auth()).get("loc_1")


class SearchTests(unittest.TestCase):
    def test_raises_when_auth_data_missing(self):
        with self.assertRaises(ValueError):
            Contacts(None).search(query="alice")

    @patch("gohl.classes.contacts.requests.get")
    def test_api_key_mode_uses_get_with_query_string(self, mock_get):
        auth = _api_key_auth()
        mock_get.return_value = _mock_response(
            {"meta": {"total": 2}, "contacts": [{"id": "c1"}, {"id": "c2"}]}
        )

        result = Contacts(auth).search(query="alice", order="asc", sort_by="date_updated", limit=10)

        mock_get.assert_called_once_with(
            f"{auth.baseurl}/contacts/?limit=10&query=alice&sortBy=date_updated&order=asc",
            headers=auth.headers,
        )
        self.assertEqual(result, {"total": 2, "contacts": [{"id": "c1"}, {"id": "c2"}]})

    @patch("gohl.classes.contacts.requests.post")
    def test_oauth_mode_uses_post_to_search_endpoint(self, mock_post):
        auth = _oauth_auth()
        mock_post.return_value = _mock_response(
            {"total": 1, "contacts": [{"id": "c1"}]}
        )

        result = Contacts(auth).search(query="alice")

        mock_post.assert_called_once_with(
            f"{auth.baseurl}/contacts/search/",
            json={},
            headers=auth.headers,
        )
        self.assertEqual(result, {"total": 1, "contacts": [{"id": "c1"}]})

    @patch("gohl.classes.contacts.requests.get")
    def test_propagates_http_error_in_api_key_mode(self, mock_get):
        mock_get.return_value = _http_error_response(401)
        with self.assertRaises(requests.exceptions.HTTPError):
            Contacts(_api_key_auth()).search(query="x")

    @patch("gohl.classes.contacts.requests.post")
    def test_propagates_http_error_in_oauth_mode(self, mock_post):
        mock_post.return_value = _http_error_response(500)
        with self.assertRaises(requests.exceptions.HTTPError):
            Contacts(_oauth_auth()).search(query="x")


class SearchWithFiltersTests(unittest.TestCase):
    def test_raises_when_auth_data_missing(self):
        with self.assertRaises(ValueError):
            Contacts(None).search_with_filters({"location_id": "loc_1"})

    @patch("gohl.classes.contacts.requests.post")
    def test_posts_query_payload_unchanged(self, mock_post):
        auth = _oauth_auth()
        mock_post.return_value = _mock_response(
            {"total": 1, "contacts": [{"id": "c1"}]}
        )
        query = {
            "location_id": "loc_1",
            "page_limit": 10,
            "filters": [{"field": "email", "operator": "contains", "value": "@example.com"}],
            "sort": [{"field": "dateAdded", "direction": "desc"}],
        }

        result = Contacts(auth).search_with_filters(query)

        mock_post.assert_called_once_with(
            f"{auth.baseurl}/contacts/search/",
            json=query,
            headers=auth.headers,
        )
        self.assertEqual(result, {"total": 1, "contacts": [{"id": "c1"}]})

    @patch("gohl.classes.contacts.requests.post")
    def test_propagates_http_error(self, mock_post):
        mock_post.return_value = _http_error_response(400)
        with self.assertRaises(requests.exceptions.HTTPError):
            Contacts(_oauth_auth()).search_with_filters({"location_id": "loc_1"})


class LookupTests(unittest.TestCase):
    def test_raises_when_auth_data_missing(self):
        with self.assertRaises(ValueError):
            Contacts(None).lookup(email="a@b.com")

    def test_raises_when_not_api_key_mode(self):
        with self.assertRaises(ValueError):
            Contacts(_oauth_auth()).lookup(email="a@b.com")

    @patch("gohl.classes.contacts.requests.get")
    def test_sends_email_and_phone_in_query_string(self, mock_get):
        auth = _api_key_auth()
        mock_get.return_value = _mock_response({"contacts": [{"id": "c1"}]})

        result = Contacts(auth).lookup(email="a@b.com", phone="555-1234")

        mock_get.assert_called_once_with(
            f"{auth.baseurl}/contacts/lookup?email=a@b.com&phone=555-1234",
            headers=auth.headers,
        )
        self.assertEqual(result, [{"id": "c1"}])

    @patch("gohl.classes.contacts.requests.get")
    def test_uses_empty_defaults(self, mock_get):
        auth = _api_key_auth()
        mock_get.return_value = _mock_response({"contacts": []})

        Contacts(auth).lookup()

        mock_get.assert_called_once_with(
            f"{auth.baseurl}/contacts/lookup?email=&phone=",
            headers=auth.headers,
        )

    @patch("gohl.classes.contacts.requests.get")
    def test_propagates_http_error(self, mock_get):
        mock_get.return_value = _http_error_response(404)
        with self.assertRaises(requests.exceptions.HTTPError):
            Contacts(_api_key_auth()).lookup(email="a@b.com")


class GetByBusinessIdTests(unittest.TestCase):
    def test_raises_when_auth_data_missing(self):
        with self.assertRaises(ValueError):
            Contacts(None).get_by_business_id("biz_1")

    @patch("gohl.classes.contacts.requests.get")
    def test_returns_total_count_and_contacts(self, mock_get):
        auth = _oauth_auth()
        mock_get.return_value = _mock_response(
            {"count": 2, "contacts": [{"id": "c1"}, {"id": "c2"}]}
        )

        result = Contacts(auth).get_by_business_id("biz_1")

        mock_get.assert_called_once_with(
            f"{auth.baseurl}/contacts/business/biz_1",
            headers=auth.headers,
        )
        self.assertEqual(
            result,
            {"total": 2, "count": 2, "contacts": [{"id": "c1"}, {"id": "c2"}]},
        )

    @patch("gohl.classes.contacts.requests.get")
    def test_propagates_http_error(self, mock_get):
        mock_get.return_value = _http_error_response(404)
        with self.assertRaises(requests.exceptions.HTTPError):
            Contacts(_oauth_auth()).get_by_business_id("biz_1")


class GetOneTests(unittest.TestCase):
    def test_raises_when_auth_data_missing(self):
        with self.assertRaises(ValueError):
            Contacts(None).get_one("c1")

    @patch("gohl.classes.contacts.requests.get")
    def test_returns_contact(self, mock_get):
        auth = _oauth_auth()
        mock_get.return_value = _mock_response({"contact": {"id": "c1"}})

        result = Contacts(auth).get_one("c1")

        mock_get.assert_called_once_with(
            f"{auth.baseurl}/contacts/c1",
            headers=auth.headers,
        )
        self.assertEqual(result, {"id": "c1"})

    @patch("gohl.classes.contacts.requests.get")
    def test_propagates_http_error(self, mock_get):
        mock_get.return_value = _http_error_response(404)
        with self.assertRaises(requests.exceptions.HTTPError):
            Contacts(_oauth_auth()).get_one("c1")


class CreateTests(unittest.TestCase):
    def test_raises_when_auth_data_missing(self):
        with self.assertRaises(ValueError):
            Contacts(None).create({"email": "a@b.com"})

    @patch("gohl.classes.contacts.requests.post")
    def test_api_key_mode_sends_contact_body_unchanged(self, mock_post):
        auth = _api_key_auth()
        contact = {"email": "a@b.com", "firstName": "Alice"}
        mock_post.return_value = _mock_response({"contact": {"id": "c1", **contact}})

        result = Contacts(auth).create(contact)

        mock_post.assert_called_once_with(
            f"{auth.baseurl}/contacts/",
            json=contact,
            headers=auth.headers,
        )
        self.assertEqual(result["id"], "c1")

    @patch("gohl.classes.contacts.requests.post")
    def test_oauth_mode_injects_location_id_from_auth(self, mock_post):
        auth = _oauth_auth()
        contact = {"email": "a@b.com"}
        mock_post.return_value = _mock_response({"contact": {"id": "c1"}})

        Contacts(auth).create(contact)

        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"], {"email": "a@b.com", "locationId": "loc_default"})

    @patch("gohl.classes.contacts.requests.post")
    def test_oauth_mode_prefers_explicit_location_id_argument(self, mock_post):
        auth = _oauth_auth()
        mock_post.return_value = _mock_response({"contact": {"id": "c1"}})

        Contacts(auth).create({"email": "a@b.com"}, location_id="loc_override")

        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["locationId"], "loc_override")

    @patch("gohl.classes.contacts.requests.post")
    def test_propagates_http_error(self, mock_post):
        mock_post.return_value = _http_error_response(400)
        with self.assertRaises(requests.exceptions.HTTPError):
            Contacts(_oauth_auth()).create({"email": "a@b.com"})


class UpdateTests(unittest.TestCase):
    def test_raises_when_auth_data_missing(self):
        with self.assertRaises(ValueError):
            Contacts(None).update("c1", {"firstName": "Alice"})

    @patch("gohl.classes.contacts.requests.put")
    def test_api_key_mode_sends_contact_body_unchanged(self, mock_put):
        auth = _api_key_auth()
        contact = {"firstName": "Alice"}
        mock_put.return_value = _mock_response({"contact": {"id": "c1", **contact}})

        result = Contacts(auth).update("c1", contact)

        mock_put.assert_called_once_with(
            f"{auth.baseurl}/contacts/c1",
            json=contact,
            headers=auth.headers,
        )
        self.assertEqual(result["id"], "c1")

    @patch("gohl.classes.contacts.requests.put")
    def test_oauth_mode_injects_location_id_from_auth(self, mock_put):
        auth = _oauth_auth()
        mock_put.return_value = _mock_response({"contact": {"id": "c1"}})

        Contacts(auth).update("c1", {"firstName": "Alice"})

        _, kwargs = mock_put.call_args
        self.assertEqual(
            kwargs["json"], {"firstName": "Alice", "locationId": "loc_default"}
        )

    @patch("gohl.classes.contacts.requests.put")
    def test_oauth_mode_prefers_explicit_location_id_argument(self, mock_put):
        auth = _oauth_auth()
        mock_put.return_value = _mock_response({"contact": {"id": "c1"}})

        Contacts(auth).update("c1", {"firstName": "Alice"}, location_id="loc_override")

        _, kwargs = mock_put.call_args
        self.assertEqual(kwargs["json"]["locationId"], "loc_override")

    @patch("gohl.classes.contacts.requests.put")
    def test_propagates_http_error(self, mock_put):
        mock_put.return_value = _http_error_response(400)
        with self.assertRaises(requests.exceptions.HTTPError):
            Contacts(_oauth_auth()).update("c1", {"firstName": "Alice"})


class RemoveTests(unittest.TestCase):
    def test_raises_when_auth_data_missing(self):
        with self.assertRaises(ValueError):
            Contacts(None).remove("c1")

    @patch("gohl.classes.contacts.requests.delete")
    def test_returns_succeeded_flag_when_present(self, mock_delete):
        auth = _oauth_auth()
        mock_delete.return_value = _mock_response({"succeeded": True})

        result = Contacts(auth).remove("c1")

        mock_delete.assert_called_once_with(
            f"{auth.baseurl}/contacts/c1",
            headers=auth.headers,
        )
        self.assertTrue(result)

    @patch("gohl.classes.contacts.requests.delete")
    def test_returns_false_when_succeeded_is_false(self, mock_delete):
        mock_delete.return_value = _mock_response({"succeeded": False})

        self.assertFalse(Contacts(_oauth_auth()).remove("c1"))

    @patch("gohl.classes.contacts.requests.delete")
    def test_defaults_to_true_when_succeeded_key_missing(self, mock_delete):
        mock_delete.return_value = _mock_response({})

        self.assertTrue(Contacts(_oauth_auth()).remove("c1"))

    @patch("gohl.classes.contacts.requests.delete")
    def test_propagates_http_error(self, mock_delete):
        mock_delete.return_value = _http_error_response(404)
        with self.assertRaises(requests.exceptions.HTTPError):
            Contacts(_oauth_auth()).remove("c1")


if __name__ == "__main__":
    unittest.main()
