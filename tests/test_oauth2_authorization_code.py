from responses import RequestsMock, urlencoded_params_matcher
import pytest
import requests

import requests_auth
from requests_auth.testing import BrowserMock, browser_mock, token_cache
from tests.auth_helper import get_header, get_request


def test_oauth2_authorization_code_flow_uses_provided_session(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    session = requests.Session()
    session.headers.update({"x-test": "Test value"})
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token", session=session
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={
            "access_token": "2YotnFZFEjr1zCsicMWpAA",
            "token_type": "example",
            "expires_in": 3600,
            "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
            "example_parameter": "example_value",
        },
    )
    assert (
        get_header(responses, auth).get("Authorization")
        == "Bearer 2YotnFZFEjr1zCsicMWpAA"
    )
    request = get_request(responses, "http://provide_access_token/")
    assert (
        request.body
        == "grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F&response_type=code&code=SplxlOBeZQQYbYS6WxSbIA"
    )
    assert request.headers["x-test"] == "Test value"
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_oauth2_authorization_code_flow_get_code_is_sent_in_authorization_header_by_default(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={
            "access_token": "2YotnFZFEjr1zCsicMWpAA",
            "token_type": "example",
            "expires_in": 3600,
            "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
            "example_parameter": "example_value",
        },
    )
    assert (
        get_header(responses, auth).get("Authorization")
        == "Bearer 2YotnFZFEjr1zCsicMWpAA"
    )
    assert (
        get_request(responses, "http://provide_access_token/").body
        == "grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F&response_type=code&code=SplxlOBeZQQYbYS6WxSbIA"
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_refresh_token(token_cache, responses: RequestsMock, browser_mock: BrowserMock):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={
            "access_token": "2YotnFZFEjr1zCsicMWpAA",
            "token_type": "example",
            "expires_in": "0",
            "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
            "example_parameter": "example_value",
        },
        match=[
            urlencoded_params_matcher({
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:5000/",
                "response_type": "code",
                "code": "SplxlOBeZQQYbYS6WxSbIA"
            })
        ]
    )
    assert (
            get_header(responses, auth).get("Authorization")
            == "Bearer 2YotnFZFEjr1zCsicMWpAA"
    )
    assert (
            get_request(responses, "http://provide_access_token/").body
            == "grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F&response_type=code&code=SplxlOBeZQQYbYS6WxSbIA"
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )
    # response for refresh token grant
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={
            "access_token": "rVR7Syg5bjZtZYjbZIW",
            "token_type": "example",
            "expires_in": 3600,
            "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
            "example_parameter": "example_value",
        },
        match=[
            urlencoded_params_matcher(
                {"grant_type": "refresh_token", "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA", "response_type": "code"})
        ]
    )

    response = requests.get("http://authorized_only", auth=auth)
    assert (
            response.request.headers.get("Authorization")
            == "Bearer rVR7Syg5bjZtZYjbZIW"
    )
    assert (
            get_request(responses, "http://provide_access_token/").body
            == "grant_type=refresh_token&response_type=code&refresh_token=tGzv3JOkF0XG5Qx2TlKWIA"
    )


def test_empty_token_is_invalid(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={
            "access_token": "",
            "token_type": "example",
            "expires_in": 3600,
            "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
            "example_parameter": "example_value",
        },
    )
    with pytest.raises(requests_auth.GrantNotProvided) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "access_token not provided within {'access_token': '', 'token_type': 'example', 'expires_in': 3600, 'refresh_token': 'tGzv3JOkF0XG5Qx2TlKWIA', 'example_parameter': 'example_value'}."
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_no_json(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST, "http://provide_access_token", body="failure", status=400
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert str(exception_info.value) == "failure"
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_invalid_request_error(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={"error": "invalid_request"},
        status=400,
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "invalid_request: The request is missing a required parameter, includes an "
        "unsupported parameter value (other than grant type), repeats a parameter, "
        "includes multiple credentials, utilizes more than one mechanism for "
        "authenticating the client, or is otherwise malformed."
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_invalid_request_error_and_error_description(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={"error": "invalid_request", "error_description": "desc of the error"},
        status=400,
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert str(exception_info.value) == "invalid_request: desc of the error"
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_invalid_request_error_and_error_description_and_uri(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={
            "error": "invalid_request",
            "error_description": "desc of the error",
            "error_uri": "http://test_url",
        },
        status=400,
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == f"invalid_request: desc of the error\nMore information can be found on http://test_url"
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_invalid_request_error_and_error_description_and_uri_and_other_fields(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={
            "error": "invalid_request",
            "error_description": "desc of the error",
            "error_uri": "http://test_url",
            "other": "other info",
        },
        status=400,
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "invalid_request: desc of the error\nMore information can be found on http://test_url\nAdditional information: {'other': 'other info'}"
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_without_error(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={"other": "other info"},
        status=400,
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert str(exception_info.value) == "{'other': 'other info'}"
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_invalid_client_error(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={"error": "invalid_client"},
        status=400,
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "invalid_client: Client authentication failed (e.g., unknown client, no "
        "client authentication included, or unsupported authentication method).  The "
        "authorization server MAY return an HTTP 401 (Unauthorized) status code to "
        "indicate which HTTP authentication schemes are supported.  If the client "
        'attempted to authenticate via the "Authorization" request header field, the '
        "authorization server MUST respond with an HTTP 401 (Unauthorized) status "
        'code and include the "WWW-Authenticate" response header field matching the '
        "authentication scheme used by the client."
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_invalid_grant_error(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={"error": "invalid_grant"},
        status=400,
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "invalid_grant: The provided authorization grant (e.g., authorization code, "
        "resource owner credentials) or refresh token is invalid, expired, revoked, "
        "does not match the redirection URI used in the authorization request, or was "
        "issued to another client."
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_unauthorized_client_error(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={"error": "unauthorized_client"},
        status=400,
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "unauthorized_client: The authenticated client is not authorized to use this "
        "authorization grant type."
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_unsupported_grant_type_error(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={"error": "unsupported_grant_type"},
        status=400,
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "unsupported_grant_type: The authorization grant type is not supported by the "
        "authorization server."
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_grant_request_invalid_scope_error(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={"error": "invalid_scope"},
        status=400,
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "invalid_scope: The requested scope is invalid, unknown, malformed, or "
        "exceeds the scope granted by the resource owner."
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_with_invalid_token_request_invalid_request_error(
    token_cache, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#error=invalid_request",
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "invalid_request: The request is missing a required parameter, includes an invalid parameter value, includes a parameter more than once, or is otherwise malformed."
    )
    tab.assert_failure(
        "Unable to properly perform authentication: invalid_request: The request is missing a required parameter, includes an invalid parameter value, includes a parameter more than once, or is otherwise malformed."
    )


def test_with_invalid_token_request_invalid_request_error_and_error_description(
    token_cache, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#error=invalid_request&error_description=desc",
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert str(exception_info.value) == "invalid_request: desc"
    tab.assert_failure(
        "Unable to properly perform authentication: invalid_request: desc"
    )


def test_with_invalid_token_request_invalid_request_error_and_error_description_and_uri(
    token_cache, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#error=invalid_request&error_description=desc&error_uri=http://test_url",
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "invalid_request: desc\nMore information can be found on http://test_url"
    )
    tab.assert_failure(
        "Unable to properly perform authentication: invalid_request: desc\nMore information can be found on http://test_url"
    )


def test_with_invalid_token_request_invalid_request_error_and_error_description_and_uri_and_other_fields(
    token_cache, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#error=invalid_request&error_description=desc&error_uri=http://test_url&other=test",
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "invalid_request: desc\nMore information can be found on http://test_url\nAdditional information: {'other': ['test']}"
    )
    tab.assert_failure(
        "Unable to properly perform authentication: invalid_request: desc\nMore information can be found on http://test_url\nAdditional information: {'other': ['test']}"
    )


def test_with_invalid_token_request_unauthorized_client_error(
    token_cache, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#error=unauthorized_client",
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "unauthorized_client: The client is not authorized to request an authorization code or an access token using this method."
    )
    tab.assert_failure(
        "Unable to properly perform authentication: unauthorized_client: The client is not authorized to request an authorization code or an access token using this method."
    )


def test_with_invalid_token_request_access_denied_error(
    token_cache, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#error=access_denied",
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "access_denied: The resource owner or authorization server denied the request."
    )
    tab.assert_failure(
        "Unable to properly perform authentication: access_denied: The resource owner or authorization server denied the request."
    )


def test_with_invalid_token_request_unsupported_response_type_error(
    token_cache, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#error=unsupported_response_type",
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "unsupported_response_type: The authorization server does not support obtaining an authorization code or an access token using this method."
    )
    tab.assert_failure(
        "Unable to properly perform authentication: unsupported_response_type: The authorization server does not support obtaining an authorization code or an access token using this method."
    )


def test_with_invalid_token_request_invalid_scope_error(
    token_cache, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#error=invalid_scope",
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "invalid_scope: The requested scope is invalid, unknown, or malformed."
    )
    tab.assert_failure(
        "Unable to properly perform authentication: invalid_scope: The requested scope is invalid, unknown, or malformed."
    )


def test_with_invalid_token_request_server_error_error(
    token_cache, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#error=server_error",
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "server_error: The authorization server encountered an unexpected condition that prevented it from fulfilling the request. (This error code is needed because a 500 Internal Server Error HTTP status code cannot be returned to the client via an HTTP redirect.)"
    )
    tab.assert_failure(
        "Unable to properly perform authentication: server_error: The authorization server encountered an unexpected condition that prevented it from fulfilling the request. (This error code is needed because a 500 Internal Server Error HTTP status code cannot be returned to the client via an HTTP redirect.)"
    )


def test_with_invalid_token_request_temporarily_unavailable_error(
    token_cache, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#error=temporarily_unavailable",
    )
    with pytest.raises(requests_auth.InvalidGrantRequest) as exception_info:
        requests.get("http://authorized_only", auth=auth)
    assert (
        str(exception_info.value)
        == "temporarily_unavailable: The authorization server is currently unable to handle the request due to a temporary overloading or maintenance of the server.  (This error code is needed because a 503 Service Unavailable HTTP status code cannot be returned to the client via an HTTP redirect.)"
    )
    tab.assert_failure(
        "Unable to properly perform authentication: temporarily_unavailable: The authorization server is currently unable to handle the request due to a temporary overloading or maintenance of the server.  (This error code is needed because a 503 Service Unavailable HTTP status code cannot be returned to the client via an HTTP redirect.)"
    )


def test_nonce_is_sent_if_provided_in_authorization_url(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code?nonce=123456", "http://provide_access_token"
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=code&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F&nonce=%5B%27123456%27%5D",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={
            "access_token": "2YotnFZFEjr1zCsicMWpAA",
            "token_type": "example",
            "expires_in": 3600,
            "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
            "example_parameter": "example_value",
        },
    )
    assert (
        get_header(responses, auth).get("Authorization")
        == "Bearer 2YotnFZFEjr1zCsicMWpAA"
    )
    assert (
        get_request(responses, "http://provide_access_token/").body
        == "grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F&response_type=code&code=SplxlOBeZQQYbYS6WxSbIA"
    )
    tab.assert_success(
        "You are now authenticated on 163f0455b3e9cad3ca04254e5a0169553100d3aa0756c7964d897da316a695ffed5b4f46ef305094fd0a88cfe4b55ff257652015e4aa8f87b97513dba440f8de. You may close this tab."
    )


def test_response_type_can_be_provided_in_url(
    token_cache, responses: RequestsMock, browser_mock: BrowserMock
):
    auth = requests_auth.OAuth2AuthorizationCode(
        "http://provide_code?response_type=my_code",
        "http://provide_access_token",
        response_type="not_used",
    )
    tab = browser_mock.add_response(
        opened_url="http://provide_code?response_type=my_code&state=49b67a19e70f692c3fc09dd124e5782b41a86f4f4931e1cc938ccbb466eecf1b730edb9eb01e42005de77ce3dd5a016418f8e780f30c4477d71102fe03e39e62&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F",
        reply_url="http://localhost:5000#code=SplxlOBeZQQYbYS6WxSbIA&state=49b67a19e70f692c3fc09dd124e5782b41a86f4f4931e1cc938ccbb466eecf1b730edb9eb01e42005de77ce3dd5a016418f8e780f30c4477d71102fe03e39e62",
    )
    responses.add(
        responses.POST,
        "http://provide_access_token",
        json={
            "access_token": "2YotnFZFEjr1zCsicMWpAA",
            "token_type": "example",
            "expires_in": 3600,
            "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
            "example_parameter": "example_value",
        },
    )
    assert (
        get_header(responses, auth).get("Authorization")
        == "Bearer 2YotnFZFEjr1zCsicMWpAA"
    )
    assert (
        get_request(responses, "http://provide_access_token/").body
        == "grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F&code=SplxlOBeZQQYbYS6WxSbIA"
    )
    tab.assert_success(
        "You are now authenticated on 49b67a19e70f692c3fc09dd124e5782b41a86f4f4931e1cc938ccbb466eecf1b730edb9eb01e42005de77ce3dd5a016418f8e780f30c4477d71102fe03e39e62. You may close this tab."
    )


def test_authorization_url_is_mandatory():
    with pytest.raises(Exception) as exception_info:
        requests_auth.OAuth2AuthorizationCode("", "http://test_url")
    assert str(exception_info.value) == "Authorization URL is mandatory."


def test_token_url_is_mandatory():
    with pytest.raises(Exception) as exception_info:
        requests_auth.OAuth2AuthorizationCode("http://test_url", "")
    assert str(exception_info.value) == "Token URL is mandatory."


def test_header_value_must_contains_token():
    with pytest.raises(Exception) as exception_info:
        requests_auth.OAuth2AuthorizationCode(
            "http://test_url", "http://test_url", header_value="Bearer token"
        )
    assert str(exception_info.value) == "header_value parameter must contains {token}."
