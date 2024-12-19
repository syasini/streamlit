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

import random

import numpy as np
import pandas as pd

import streamlit as st
from shared.data_mocks import (
    INTERVAL_TYPES_DF,
)

np.random.seed(0)
random.seed(0)

st.set_page_config(layout="wide")

# st.subheader("Base types")
# st.dataframe(BASE_TYPES_DF, use_container_width=True, hide_index=True)

# st.subheader("Number types")
# st.dataframe(NUMBER_TYPES_DF, use_container_width=True, hide_index=True)

# st.subheader("Date, time and datetime types")
# st.dataframe(DATETIME_TYPES_DF, use_container_width=True, hide_index=True)

# st.subheader("List types")
# st.dataframe(LIST_TYPES_DF, use_container_width=True, hide_index=True)

st.subheader("Interval types")
st.dataframe(INTERVAL_TYPES_DF, use_container_width=True, hide_index=True)

df = pd.DataFrame(
    [["foo", 100], ["bar", 200]],
    index=pd.interval_range(
        start=pd.Timestamp("2017-01-01"), end=pd.Timestamp("2017-01-03")
    ),
    columns=pd.interval_range(
        start=pd.Timestamp("2017-01-01"), end=pd.Timestamp("2017-01-03")
    ),
)

st.dataframe(df, use_container_width=True)

# st.subheader("Special types")
# st.dataframe(SPECIAL_TYPES_DF, use_container_width=True, hide_index=True)

# st.subheader("Period types")
# st.dataframe(PERIOD_TYPES_DF, use_container_width=True, hide_index=True)

# st.subheader("Unsupported types (string fallback)")
# st.dataframe(UNSUPPORTED_TYPES_DF, use_container_width=True, hide_index=True)
