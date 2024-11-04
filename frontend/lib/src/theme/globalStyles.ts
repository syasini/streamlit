/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { css, SerializedStyles } from "@emotion/react"
import { transparentize } from "color2k"

import { EmotionTheme } from "@streamlit/lib/src/theme"

export const globalStyles = (theme: EmotionTheme): SerializedStyles => css`
  // Override the base font-size value here.
  // This overrides the value set in reboot.scss.
  html {
    font-size: ${theme.fontSizes.mdPx}px;
  }

  // Set height to 100% for printing, otherwise the page on Safari might be blank
  @media print {
    html {
      height: 100%;
      // make background-colors appear by default (e.g. the sidebar background, widget background, multi-select element background, ...)
      print-color-adjust: exact;
      -webkit-print-color-adjust: exact;
    }
  }

  iframe {
    border: none;
    padding: 0;
    margin: 0;
  }

  // Embedded Overflow Management
  body.embedded {
    overflow: hidden;
  }

  body.embedded:hover {
    overflow: auto;
  }

  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

  // Body
  //
  // 1. Remove the margin in all browsers.
  // 2. As a best practice, apply a default background-color.
  // 3. Prevent adjustments of font size after orientation changes in iOS.
  // 4. Change the default tap highlight to be completely transparent in iOS.

  body {
    margin: 0; // 1
    font-family: ${theme.genericFonts.bodyFont};
    font-weight: ${theme.fontWeights.normal};
    line-height: ${theme.lineHeights.base};
    color: ${theme.colors.bodyText};
    background-color: ${theme.colors.bgColor}; // 2
    -webkit-text-size-adjust: 100%; // 3
    -webkit-tap-highlight-color: ${transparentize(theme.colors.black, 1)}; // 4
    -webkit-font-smoothing: auto;
  }

  // Future-proof rule: in browsers that support :focus-visible, suppress the focus outline
  // on elements that programmatically receive focus but wouldn't normally show a visible
  // focus outline. In general, this would mean that the outline is only applied if the
  // interaction that led to the element receiving programmatic focus was a keyboard interaction,
  // or the browser has somehow determined that the user is primarily a keyboard user and/or
  // wants focus outlines to always be presented.
  // See https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
  // and https://developer.paciellogroup.com/blog/2018/03/focus-visible-and-backwards-compatibility/

  [tabindex="-1"]:focus:not(:focus-visible) {
    outline: 0 !important;
  }

  h1 {
    font-family: ${theme.genericFonts.headingFont};
    font-weight: ${theme.fontWeights.extrabold};
    font-size: 2.75rem;
    // Use rem so we can remove it when first child, knowing that the
    // element-container above always adds 1rem.
    padding: 1.25rem 0 1rem 0;
    margin: 0;

    line-height: 1.2;
  }

  h2 {
    font-family: ${theme.genericFonts.headingFont};
    font-weight: ${theme.fontWeights.bold};
    font-size: 2.25rem;
    letter-spacing: -0.005em;

    // Use rem so we can remove it when first child, knowing that the
    // element-container above always adds 1rem.
    padding: 1rem 0 1rem 0;
    margin: 0;

    line-height: 1.2;
  }

  h3 {
    font-family: ${theme.genericFonts.headingFont};
    font-weight: ${theme.fontWeights.bold};
    font-size: 1.75rem;
    letter-spacing: -0.005em;

    // Use rem so we can remove it when first child, knowing that the
    // element-container above always adds 1rem.
    padding: 0.5rem 0 1rem 0;
    margin: 0;

    line-height: 1.2;
  }

  h4 {
    font-family: ${theme.genericFonts.headingFont};
    font-weight: ${theme.fontWeights.bold};
    font-size: 1.5rem;
    padding: 0.75rem 0 1rem 0;
    margin: 0;
    line-height: 1.2;
  }

  h5 {
    font-family: ${theme.genericFonts.headingFont};
    font-weight: ${theme.fontWeights.bold};
    font-size: 1.25rem;
    padding: 0 0 1rem 0;
    margin: 0;
    line-height: 1.2;
  }

  h6 {
    font-family: ${theme.genericFonts.headingFont};
    font-weight: ${theme.fontWeights.bold};
    font-size: 1rem;
    padding: 0 0 1rem 0;
    margin: 0;
    line-height: 1.2;
  }

  // Strong
  //
  // Add the correct font weight in Chrome, Edge, and Safari
  b,
  strong {
    font-weight: ${theme.fontWeights.bold};
  }

  // Override h1 font weight to default weight
  h1 b,
  h1 strong {
    font-weight: ${theme.fontWeights.extrabold};
  }

  // And undo these styles for placeholder links/named anchors (without href).
  // It would be more straightforward to just use a[href] in previous block, but that
  // causes specificity issues in many other styles that are too complex to fix.
  // See https://github.com/twbs/bootstrap/issues/19402

  a:not([href]):not([class]) {
    &,
    &:hover {
      color: inherit;
      text-decoration: none;
    }
  }

  // Set the cursor for non-<button> buttons
  //
  // Details at https://github.com/twbs/bootstrap/pull/30562
  [role="button"] {
    cursor: pointer;
  }

  // Set the cursor for all buttons buttons
  button {
    &:not(:disabled) {
      cursor: pointer;
    }
  }

  // 1. Prevent a WebKit bug where (2) destroys native audio and video
  //    controls in Android 4.
  // 2. Correct the inability to style clickable types in iOS and Safari.
  // 3. Opinionated: add "hand" cursor to non-disabled button elements.

  button,
  [type="button"], // 1
  [type="reset"],
  [type="submit"] {
    -webkit-appearance: button; // 2
  }

  // Remove inner border and padding from Firefox, but don't restore the outline like Normalize.

  ::-moz-focus-inner {
    padding: 0;
    border-style: none;
  }

  // Hidden attribute
  //
  // Always hide an element with the hidden HTML attribute.

  [hidden] {
    display: none !important;
  }

  // Make scrollbars awesome in Chrome

  ::-webkit-scrollbar {
    background: transparent;
    border-radius: 100px;
    height: 6px;
    width: 6px;
  }

  ::-webkit-scrollbar:active {
    background: ${theme.colors.fadedText10};
  }

  :hover::-webkit-scrollbar-thumb:vertical,
  :hover::-webkit-scrollbar-thumb:horizontal {
    background: ${theme.colors.fadedText40};
    border-radius: 100px;
  }
`
