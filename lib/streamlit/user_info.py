# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Iterator, Mapping, NoReturn, TypedDict, Union, cast

from streamlit import config, runtime
from streamlit.errors import StreamlitAPIException
from streamlit.proto.ForwardMsg_pb2 import ForwardMsg
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    get_script_run_ctx as _get_script_run_ctx,
)
from streamlit.runtime.secrets import secrets_singleton

if TYPE_CHECKING:
    from streamlit.runtime.scriptrunner_utils.script_run_context import UserInfo

    class ProviderTokenPayload(TypedDict):
        provider: str
        exp: int


def get_signing_secret() -> str:
    """Get the cookie signing secret from the configuration or secrets.toml."""
    signing_secret: str = config.get_option("server.cookieSecret")
    if secrets_singleton.load_if_toml_exists():
        auth_section = secrets_singleton.get("auth")
        if auth_section:
            signing_secret = auth_section.get("cookie_secret", signing_secret)
    return signing_secret


def encode_provider_token(provider: str) -> str:
    """Returns a signed JWT token with the provider and expiration time."""
    try:
        from authlib.jose import jwt  # type: ignore[import-untyped]
    except ImportError:
        raise StreamlitAPIException(
            "To use Auth you need to install the 'Authlib' package."
        ) from None

    header = {"alg": "HS256"}
    payload = {
        "provider": provider,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=2),
    }
    provider_token: bytes = jwt.encode(header, payload, get_signing_secret())
    # JWT token is a byte string, so we need to decode it to a URL compatible string
    return provider_token.decode("latin-1")


def decode_provider_token(provider_token: str) -> ProviderTokenPayload:
    """Decode the JWT token and validate the claims."""
    try:
        from authlib.jose import JoseError, JWTClaims, jwt
    except ImportError:
        raise StreamlitAPIException(
            "To use Auth you need to install the 'Authlib' package."
        ) from None

    claim_options = {"exp": {"essential": True}, "provider": {"essential": True}}
    try:
        payload: JWTClaims = jwt.decode(
            provider_token, get_signing_secret(), claims_options=claim_options
        )
        payload.validate()
    except JoseError as e:
        raise StreamlitAPIException(f"Error decoding provider token: {e}") from None

    return cast("ProviderTokenPayload", payload)


def validate_auth_credentials(provider: str) -> None:
    """Validate the general auth credentials and auth credentials for the given provider."""
    if not secrets_singleton.load_if_toml_exists():
        raise StreamlitAPIException(
            "To use Auth you need to configure auth credentials in secrets.toml."
        )

    auth_section = secrets_singleton.get("auth")
    if auth_section is None:
        raise StreamlitAPIException(
            "Auth credentials are missing. Please check your configuration."
        )
    if "redirect_uri" not in auth_section:
        raise StreamlitAPIException(
            "Auth credentials are missing 'redirect_uri'. Please check your configuration."
        )

    provider_section = auth_section.get(provider)
    if provider_section is None:
        raise StreamlitAPIException(
            f"Auth credentials are missing *'{provider}'*. Please check your configuration."
        )

    if not isinstance(provider_section, Mapping):
        raise StreamlitAPIException(
            f"Auth credentials for '{provider}' must be a toml section."
            f" Please check your configuration."
        )

    required_keys = ["client_id", "client_secret", "server_metadata_url"]
    missing_keys = [key for key in required_keys if key not in provider_section]
    if missing_keys:
        raise StreamlitAPIException(
            f"Auth credentials for '{provider}' are missing the following keys: "
            f"{missing_keys}. Please check your configuration."
        )


def generate_login_redirect_url(provider: str) -> str:
    """Generate the login redirect URL for the given provider."""
    provider_token = encode_provider_token(provider)
    return f"/auth/login?provider={provider_token}"


def _get_user_info() -> UserInfo:
    ctx = _get_script_run_ctx()
    if ctx is None:
        # TODO: Add appropriate warnings when ctx is missing
        return {}
    return ctx.user_info


class UserInfoProxy(Mapping[str, Union[str, None]]):
    """
    A read-only, dict-like object for accessing information about current user.

    ``st.experimental_user`` is dependant on the host platform running the
    Streamlit app. If the host platform has not configured the function, it
    will behave as it does in a locally running app.

    Properties can by accessed via key or attribute notation. For example,
    ``st.experimental_user["email"]`` or ``st.experimental_user.email``.

    Attributes
    ----------
    email : str
        If running locally, this property returns the string literal
        ``"test@example.com"``.

        If running on Streamlit Community Cloud, this
        property returns one of two values:

        * ``None`` if the user is not logged in or not a member of the app's\
        workspace. Such users appear under anonymous pseudonyms in the app's\
        analytics.
        * The user's email if the the user is logged in and a member of the\
        app's workspace. Such users are identified by their email in the app's\
        analytics.

    """

    def login(self, provider: str) -> None:
        """Initiate the login for the given provider."""
        context = _get_script_run_ctx()
        if context is not None:
            validate_auth_credentials(provider)
            fwd_msg = ForwardMsg()
            fwd_msg.auth_redirect.url = generate_login_redirect_url(provider)
            context.enqueue(fwd_msg)

    def logout(self) -> None:
        """Logout the current user."""
        context = _get_script_run_ctx()
        if context is not None:
            context.user_info.clear()
            session_id = context.session_id

            if runtime.exists():
                instance = runtime.get_instance()
                instance.clear_user_info_for_session(session_id)

            fwd_msg = ForwardMsg()
            fwd_msg.auth_redirect.url = "/auth/logout"
            context.enqueue(fwd_msg)

    def is_logged_in(self) -> bool:
        """Check if the user is logged in."""
        user_email = _get_user_info().get("email")
        return user_email is not None and user_email != "test@example.com"

    def __getitem__(self, key: str) -> str | None:
        return _get_user_info()[key]

    def __getattr__(self, key: str) -> str | None:
        try:
            return _get_user_info()[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name: str, value: str | None) -> NoReturn:
        raise StreamlitAPIException("st.experimental_user cannot be modified")

    def __setitem__(self, name: str, value: str | None) -> NoReturn:
        raise StreamlitAPIException("st.experimental_user cannot be modified")

    def __iter__(self) -> Iterator[str]:
        return iter(_get_user_info())

    def __len__(self) -> int:
        return len(_get_user_info())

    def to_dict(self) -> UserInfo:
        """
        Get user info as a dictionary.

        This method primarily exists for internal use and is not needed for
        most cases. ``st.experimental_user`` returns an object that inherits from
        ``dict`` by default.

        Returns
        -------
        Dict[str,str]
            A dictionary of the current user's information.
        """
        return _get_user_info()
