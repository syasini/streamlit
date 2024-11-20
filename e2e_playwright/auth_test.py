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

import pytest
from playwright.sync_api import Page, expect

from e2e_playwright.conftest import wait_for_app_run
from e2e_playwright.shared.app_utils import get_button, get_markdown


@pytest.fixture(scope="module")
def app_port() -> int:
    """Fixture that returns an available port on localhost."""
    return 8501


def test_login_successful(app: Page, fake_oidc_server):
    """Test authentication flow with test provider."""
    button_element = get_button(app, "TEST LOGIN")
    button_element.click()
    app.wait_for_timeout(2_000)

    text = get_markdown(app, "authtest@example.com")
    expect(text).to_be_visible()
    wait_for_app_run(app)

    text = get_markdown(app, "John Doe")
    expect(text).to_be_visible()