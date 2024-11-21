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

import time
from typing import Generator

import pytest
from playwright.sync_api import Page, expect

from e2e_playwright.conftest import AsyncSubprocess, wait_for_app_run
from e2e_playwright.shared.app_utils import get_button, get_markdown


@pytest.fixture(scope="module")
def fake_oidc_server() -> Generator[AsyncSubprocess, None, None]:
    """Fixture that starts and stops the Streamlit app server."""
    oidc_server_proc = AsyncSubprocess(
        ["python", "shared/oidc_mock_server.py"],
        cwd=".",
    )

    oidc_server_proc.start()
    time.sleep(1)
    yield oidc_server_proc
    oidc_server_stdout = oidc_server_proc.terminate()
    print(oidc_server_stdout, flush=True)


@pytest.fixture(scope="module")
@pytest.mark.early
def prepare_secrets_file(app_port: int) -> None:
    """Fixture that inject the correct port to auth_secrets.toml file redirect_uri."""
    # Read in the file
    with open("./test_assets/auth_secrets.toml") as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(
        "http://localhost:8501/oauth2callback",
        f"http://localhost:{app_port}/oauth2callback",
    )
    # Write the file out again
    with open("./test_assets/auth_secrets.toml", "w") as file:
        file.write(filedata)

    yield

    with open("./test_assets/auth_secrets.toml") as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace(
        f"http://localhost:{app_port}/oauth2callback",
        "http://localhost:8501/oauth2callback",
    )
    # Write the file out again
    with open("./test_assets/auth_secrets.toml", "w") as file:
        file.write(filedata)


def test_login_successful(app: Page, fake_oidc_server, prepare_secrets_file):
    """Test authentication flow with test provider."""
    button_element = get_button(app, "TEST LOGIN")
    button_element.click()
    app.wait_for_timeout(2_000)

    text = get_markdown(app, "authtest@example.com")
    expect(text).to_be_visible()
    wait_for_app_run(app)

    text = get_markdown(app, "John Doe")
    expect(text).to_be_visible()
