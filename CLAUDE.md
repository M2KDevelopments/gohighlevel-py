# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`gohl` (PyPI package name; the repo is `gohighlevel-py`) is a Python client library wrapping the GoHighLevel REST API. There is no application — only the SDK that consumers import as `from gohl import GoHighLevel`. The package was renamed from `gohighlevel` to `gohl` (see commit `e38a0df`); any lingering references to the old name in code, docs, or imports should be treated as a bug.

There is no test suite, lint config, or formatter checked into the repo. The only CI workflow (`.github/workflows/workflow.yml`) builds with `python -m build` and publishes to PyPI on GitHub Release.

## Commands

```bash
# Install for local development (editable)
pip install -e .

# Build distribution artifacts (hatchling backend)
python -m build
```

Releases are cut by publishing a GitHub Release, which triggers PyPI trusted publishing. Bump `version` in `pyproject.toml` before tagging.

## Architecture

### Two authentication modes, two base URLs

`GoHighLevel` (`src/gohl/main.py`) is a facade that behaves differently depending on which credential type the caller provides:

- **API key mode** — `Credentials(api_key=...)`: the constructor immediately builds an `Auth` against `BASE_API_URL = https://rest.gohighlevel.com/v1` (the legacy v1 API) and initializes all endpoint classes.
- **OAuth mode** — `Credentials(client_id=..., client_secret=...)`: the constructor only wires up `self.oauth`. Endpoints are *not* available until the caller completes the OAuth dance and calls `ghl.set_auth(auth_data)`, which switches the base URL to `PROD = https://services.leadconnectorhq.com` (the v2 API) and then runs `_initialize_endpoints()`.
- **Test mode** — `ghl.set_test_mode(True)` repoints the base URL to the Stoplight mock (`https://stoplight.io/mocks/highlevel/integrations/39582850`) and re-initializes endpoints. Requires auth to already be set.

When adding or modifying an endpoint, remember that endpoint classes capture `self.auth_data` at construction time. `_initialize_endpoints()` is therefore called again after every auth-state change (set_auth, set_test_mode) — preserve this pattern rather than mutating endpoints in place.

### Endpoint class layout

`src/gohl/classes/` contains one module per top-level API resource (`contacts.py`, `calendars.py`, `conversations.py`, `opportunities.py`, `payments.py`, etc.) plus modules for nested sub-resources named `<parent>_<child>.py` (e.g. `contacts_tasks.py`, `calendars_events.py`, `conversations_messages.py`, `payments_orders.py`).

The parent class composes its sub-resources as instance attributes in `__init__`, e.g.:

```python
self.contacts = Contacts(auth_data)
# inside Contacts.__init__:
self.tasks = Task(auth_data)
self.notes = Note(auth_data)
self.appointments = Appointment(auth_data)
```

This produces the dotted access shown in the README (`ghl.contacts.tasks.add(...)`, `ghl.calendar.events.add_appointment(...)`, `ghl.conversations.email.send(...)`). When adding a new sub-resource, instantiate it in the parent's `__init__` and export the class from the parent module so the dotted path works.

`self.agency` is the one exception — it is a dict (`{'locations': ..., 'users': ...}`) rather than a class, so access is `ghl.agency['locations']`.

### HTTP layer

Endpoint methods call `requests` directly — there is no shared client/session, no retry layer, no central error handling. Each method reads headers from `self.auth_data.headers` and builds the URL from `self.auth_data.baseurl`. The `Authorization: Bearer <token>` and `Version: 2021-04-15` headers are set when `Auth` is constructed; if you need to change them globally, do it in `Auth.__init__` or in `GoHighLevel.set_auth`.

### OAuth

`OAuth.get_oauth_url()` builds the consent URL against either `marketplace.gohighlevel.com` or `marketplace.leadconnectorhq.com` depending on `Credentials.is_white_label`. Token exchange (`get_callback_auth_tokens`) POSTs to `https://api.msgsndr.com/oauth/token` and handles both `authorization_code` and `refresh_token` grants. The `OAuth` class also exposes ~80 `scope_*` helper methods plus `scope_all()` — when adding a new GHL scope, follow the existing `scope_<area>[_write]` naming convention.

## Conventions worth preserving

- Public methods are typed with `Optional`, `Dict[str, Any]`, and `TypedDict` shapes for complex filter inputs (see `ContactSearchFilter` in `contacts.py`). New endpoints should follow this same typing style.
- The README is the user-facing API contract. When endpoint signatures change, update the corresponding example in `README.md`.
- Each endpoint class carries a docstring linking to the relevant GHL Stoplight documentation page — keep this when adding new endpoints.
