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
from typing import Final

import streamlit as st
from streamlit import config, runtime

if runtime.exists():
    # We are hacking here, but we are setting the secrets file to a different file to determine if it works
    TEST_ASSETS_DIR: Final[str] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_assets"
    )
    auth_secrets_file = os.path.join(TEST_ASSETS_DIR, "auth_secrets.toml")
    config.set_option("secrets.files", [auth_secrets_file])
    st.secrets._secrets = None


x = st.button("LOGIN WITH MICROSOFT")

if x:
    st.experimental_user.login("microsoft")


if st.experimental_user.is_logged_in():
    st.markdown(f"YOU ARE LOGGED IN: {st.experimental_user.email}")
    st.write(st.experimental_user)
