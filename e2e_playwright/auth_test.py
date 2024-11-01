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

import os

import pytest
from playwright.sync_api import Page, expect

from e2e_playwright.shared.app_utils import get_button


@pytest.fixture(scope="module")
def app_port() -> int:
    return 8501


@pytest.mark.skip(
    reason="This test will work only in case if KAREN_PASSWORD env var is set."
)
def test_login_successful(app: Page):
    """Test authentication flow with Microsoft provider."""
    button_element = get_button(app, "LOGIN WITH MICROSOFT")
    button_element.click()
    app.wait_for_timeout(2_000)

    email_input = app.locator('input[type="email"]')
    email_input.fill("kajarenc2@gmail.com")
    app.wait_for_timeout(2_000)

    next_button = app.get_by_text("Next")
    next_button.click()
    app.wait_for_timeout(2_000)

    password_input = app.locator('input[type="password"]')
    password_input.fill(os.environ.get("KAREN_PASSWORD"))
    app.wait_for_timeout(2_000)

    sign_in_button = app.get_by_text("Sign In")
    sign_in_button.click()
    app.wait_for_timeout(2_000)

    if app.get_by_role("button", name="No"):
        no_button = app.get_by_role("button", name="No")
        no_button.click()
        app.wait_for_timeout(4_000)

    markdown_el = app.get_by_test_id("stMarkdown").filter(
        has_text="kajarenc2@gmail.com"
    )
    expect(markdown_el).to_be_attached()
