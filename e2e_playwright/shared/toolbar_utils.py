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

from typing import TYPE_CHECKING

from playwright.sync_api import Locator, expect

if TYPE_CHECKING:
    from e2e_playwright.conftest import ImageCompareFunction


def expand_element(element: Locator):
    # Hover over element to show the toolbar
    element.hover()

    # Check if the toolbar is visible
    element_toolbar = element.get_by_test_id("stElementToolbar")
    expect(element_toolbar).to_be_visible()
    expect(element_toolbar).to_have_css("opacity", "1")

    # Get the fullscreen button
    expand_button = element_toolbar.get_by_role("button", name="Fullscreen")
    expect(expand_button).to_be_visible()
    expand_button.click()

    # Make sure that the button shows the close fullscreen button
    expect(
        element_toolbar.get_by_role("button", name="Close fullscreen")
    ).to_be_visible()


def collapse_element(element: Locator):
    element_toolbar = element.get_by_test_id("stElementToolbar")
    expect(element_toolbar).to_be_visible()
    expect(element_toolbar).to_have_css("opacity", "1")

    close_button = element_toolbar.get_by_role("button", name="Close fullscreen")
    expect(close_button).to_be_visible()
    close_button.click()


def assert_fullscreen_toolbar_button_interactions(
    widget_element: Locator,
    assert_snapshot: ImageCompareFunction,
    filename_prefix: str = "",
    pixel_threshold: float = 0.05,
):
    """
    Shared test function to assert that clicking on fullscreen toolbar button
    expands the map into fullscreen.
    """

    fullscreen_wrapper = widget_element.page.locator(
        "[data-testid='stFullScreenFrame']", has=widget_element
    )

    expand_element(widget_element)
    assert_snapshot(
        fullscreen_wrapper,
        name=f"{filename_prefix}-fullscreen_expanded",
        pixel_threshold=pixel_threshold,
    )

    # Click again on fullscreen button to close fullscreen mode:
    collapse_element(widget_element)

    assert_snapshot(
        fullscreen_wrapper,
        name=f"{filename_prefix}-fullscreen_collapsed",
        pixel_threshold=pixel_threshold,
    )
