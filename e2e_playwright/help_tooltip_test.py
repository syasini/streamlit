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

from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction
from e2e_playwright.shared.app_utils import get_checkbox


def test_tooltip_does_not_overflow_on_the_left_side(
    app: Page, assert_snapshot: ImageCompareFunction
):
    sidebar_button = (
        app.get_by_test_id("stButton")
        .filter(has_text="Sidebar-button with help")
        .locator("button")
        .first
    )
    sidebar_button.hover()
    tooltip = app.get_by_test_id("stTooltipContent")
    expect(tooltip).to_be_visible()

    # make a screenshot of the entire app to capture potential overflow
    main_container = app.get_by_test_id("stMainBlockContainer")
    assert_snapshot(main_container, name="help_tooltip-no_left_side_overflow")


def test_tooltip_does_not_overflow_on_the_right_side(
    app: Page, assert_snapshot: ImageCompareFunction
):
    # Resize the viewport to make sure there is not a lot of space on the right side
    app.set_viewport_size({"width": 750, "height": 800})
    app.wait_for_function("() => window.innerWidth === 750")

    popover_button = (
        app.get_by_test_id("stPopover")
        .filter(has_text="Popover with toggle")
        .locator("button")
    )

    # Click the button to open it:
    popover_button.click()

    toggle = get_checkbox(app, "Right-toggle with help")
    expect(toggle).to_be_visible()
    toggle.get_by_test_id("stTooltipHoverTarget").hover()

    tooltip = app.get_by_test_id("stTooltipContent")
    expect(tooltip).to_be_visible()

    # make a screenshot of the entire app to capture potential overflow
    main_container = app.get_by_test_id("stMainBlockContainer")
    assert_snapshot(main_container, name="help_tooltip-no_right_side_overflow")
