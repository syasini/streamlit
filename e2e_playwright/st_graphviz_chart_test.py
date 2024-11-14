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

from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction, wait_for_app_run
from e2e_playwright.shared.app_utils import check_top_level_class, select_radio_option
from e2e_playwright.shared.toolbar_utils import (
    assert_fullscreen_toolbar_button_interactions,
)


def get_first_graph_svg(app: Page):
    return app.get_by_test_id("stGraphVizChart").nth(0).locator("svg")


def test_initial_setup(app: Page):
    """Initial setup: ensure charts are loaded."""
    expect(
        app.get_by_test_id("stGraphVizChart").locator("svg > g > title")
    ).to_have_count(6)


def test_shows_left_and_right_graph(app: Page):
    """Test if it shows left and right graph."""

    expect(app.locator(".stGraphVizChart > svg > g > title").nth(3)).to_have_text(
        "Left"
    )
    expect(app.locator(".stGraphVizChart > svg > g > title").nth(4)).to_have_text(
        "Right"
    )


def test_first_graph_dimensions(app: Page):
    """Test the dimensions of the first graph."""

    first_graph_svg = get_first_graph_svg(app)
    expect(first_graph_svg).to_have_attribute("width", "79pt")
    expect(first_graph_svg).to_have_attribute("height", "116pt")


def test_clicking_on_fullscreen_toolbar_button(
    app: Page, assert_snapshot: ImageCompareFunction
):
    """Test that clicking on fullscreen toolbar button expands the
    graphviz chart into fullscreen."""

    df_element = app.get_by_test_id("stGraphVizChart").nth(0)
    expect(df_element).to_be_visible()

    assert_fullscreen_toolbar_button_interactions(
        df_element,
        assert_snapshot=assert_snapshot,
        filename_prefix="st_dataframe",
    )


def test_renders_with_specified_engines(
    app: Page, assert_snapshot: ImageCompareFunction
):
    """Test if it renders with specified engines."""

    engines = ["dot", "neato", "twopi", "circo", "fdp", "osage", "patchwork"]

    for engine in engines:
        select_radio_option(app, "Select engine", engine)
        wait_for_app_run(app)
        expect(app.get_by_test_id("stMarkdown").nth(0)).to_have_text(engine)

        assert_snapshot(
            app.get_by_test_id("stGraphVizChart").nth(2).locator("svg"),
            name=f"st_graphviz_chart_engine-{engine}",
        )


def test_dot_string(app: Page, assert_snapshot: ImageCompareFunction):
    """Test if it renders charts when input is a string (dot language)."""

    title = app.locator(".stGraphVizChart > svg > g > title").nth(5)
    expect(title).to_have_text("Dot")

    assert_snapshot(
        app.get_by_test_id("stGraphVizChart").nth(5).locator("svg"),
        name="st_graphviz-chart_dot_string",
    )


def test_check_top_level_class(app: Page):
    """Check that the top level class is correctly set."""
    check_top_level_class(app, "stGraphVizChart")
