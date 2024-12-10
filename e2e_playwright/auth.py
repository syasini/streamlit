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

import streamlit as st

x = st.button("TEST LOGIN")

if x:
    st.experimental_user.login("testprovider")


if st.experimental_user.is_authenticated:
    st.markdown(f"YOU ARE LOGGED IN: {st.experimental_user.email}")
    st.markdown(st.experimental_user["name"])

if error := st.experimental_user.get("error"):
    st.markdown(f"ERROR: {error}")