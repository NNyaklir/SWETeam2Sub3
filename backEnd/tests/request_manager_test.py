import pytest
from services.httpRequestManager.request_manager import RequestManager

# Constants
EXAMPLE_URL = "https://example.com"
EXAMPLE_DATA = {"key": "value"}
EXAMPLE_HEADERS = {"Content-Type": "application/json"}
EXAMPLE_PARAMETERS = {"page": 1, "limit": 20}
EXAMPLE_COOKIES = {"session_id": "abc123xyz"}
EXAMPLE_PROXIES = {"http": "http://proxy.example.com:8080"}

# ---- Fixtures ----
@pytest.fixture
def example_manager_minimal_attributes():
    return RequestManager(method="GET", url=EXAMPLE_URL)

@pytest.fixture
def example_manager_some_attributes():
    return RequestManager(
        method="POST",
        url=EXAMPLE_URL,
        data=EXAMPLE_DATA,
        headers=EXAMPLE_HEADERS
    )

@pytest.fixture
def example_manager_all_attributes():
    return RequestManager(
        method="PUT",
        url=EXAMPLE_URL,
        data=EXAMPLE_DATA,
        headers=EXAMPLE_HEADERS,
        parameters=EXAMPLE_PARAMETERS,
        cookies=EXAMPLE_COOKIES,
        proxies=EXAMPLE_PROXIES
    )

# ---- Tests ----
def test_minimal_initialization_with_required_attributes(
        example_manager_minimal_attributes):
    manager = example_manager_minimal_attributes

    assert manager.get_method() == "GET"
    assert manager.get_target_url() == EXAMPLE_URL
    assert manager.get_data() is None
    assert manager.get_headers() is None

def test_partial_initialization_with_some_optional_attributes(
        example_manager_some_attributes):
    manager = example_manager_some_attributes

    assert manager.get_method() == "POST"
    assert manager.get_data() == EXAMPLE_DATA
    assert manager.get_headers() == EXAMPLE_HEADERS
    assert manager.get_parameters() is None

def test_full_initialization_with_all_attributes(
        example_manager_all_attributes):
    manager = example_manager_all_attributes

    assert manager.get_method() == "PUT"
    assert manager.get_cookies() == EXAMPLE_COOKIES
    assert manager.get_proxies() == EXAMPLE_PROXIES

def test_empty_container_initialization():
    manager = RequestManager(
        method="GET",
        url=EXAMPLE_URL,
        headers={},
        parameters={}
    )
    assert manager.get_headers() == {}
    assert manager.get_parameters() == {}