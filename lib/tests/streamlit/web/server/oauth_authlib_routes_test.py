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

from unittest.mock import MagicMock, patch

import tornado.httpserver
import tornado.testing
import tornado.web
import tornado.websocket

from streamlit.user_info import encode_provider_token
from streamlit.web.server.oauth_authlib_routes import AuthLoginHandler


class SecretMock(dict):
    def to_dict(self):
        return self


SECRETS_MOCK = SecretMock(
    {
        "redirect_uri": "http://localhost:8501/oauth2callback",
        "google": {
            "client_id": "CLIENT_ID",
            "client_secret": "CLIENT_SECRET",
            "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration",
        },
    }
)


class LoginHandlerTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application(
            [
                (
                    r"/auth/login",
                    AuthLoginHandler,
                )
            ]
        )

    @patch(
        "streamlit.web.server.oauth_authlib_routes.secrets_singleton",
        MagicMock(
            load_if_toml_exists=MagicMock(return_value=True),
            get=MagicMock(return_value=SECRETS_MOCK),
        ),
    )
    def test_login_handler_success(self):
        # TODO[kajarenc] Mock external network calls
        token = encode_provider_token("google")
        response = self.fetch(f"/auth/login?provider={token}", follow_redirects=False)
        assert response.code == 302
        assert response.headers["Location"].startswith(
            "https://accounts.google.com/o/oauth2/v2/auth"
        )
