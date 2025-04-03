from typing import Optional, final, Dict, Any

@final
class RequestManager:
    """Manages and sends HTTP requests using the 'requests' library.

    This class provides a structured way to configure and manage HTTP requests,
    encapsulating all request components in a single object.

    Attributes:
        _method: HTTP method to use ('GET', 'POST', 'PUT')
        _target_url: The URL endpoint for the request 
                    (e.g., 'https://api.example.com/')
        _data: Optional request body data (e.g., {'name': 'John'})
        _headers: Optional HTTP headers 
                 (e.g., {'Content-Type': 'application/json'})
        _parameters: Optional query parameters 
                    (e.g., {'page': 1, 'limit': 20, 'sort': 'name'})
        _cookies: Optional cookies to send 
                 (e.g., {'session_id': 'abc123xyz'})
        _proxies: Optional proxy configuration 
                 (e.g., {'http': 'http://proxy.example.com:8080'})

    Note:
        All attributes have corresponding getter methods (e.g., 'get_method(),
        'get_url()'). These return the current value of the attribute and
        require no additional parameters.
    """

    def __init__(
        self,
        method: str,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        parameters: Optional[Dict[str, str | int | float | bool]] = None,
        cookies: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None
    ):
        self._method = method
        self._target_url = url
        self._data = data
        self._headers = headers
        self._parameters = parameters
        self._cookies = cookies
        self._proxies = proxies

    def get_method(self) -> str:
        return self._method

    def get_target_url(self) -> str:
        return self._target_url

    def get_data(self) -> Optional[Dict[str, Any]]:
        return self._data

    def get_headers(self) -> Optional[Dict[str, str]]:
        return self._headers

    def get_parameters(self) -> Optional[Dict[str, str | int | float | bool]]:
        return self._parameters

    def get_cookies(self) -> Optional[Dict[str, str]]:
        return self._cookies

    def get_proxies(self) -> Optional[Dict[str, str]]:
        return self._proxies
