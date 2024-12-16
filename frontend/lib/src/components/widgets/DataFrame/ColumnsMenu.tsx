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

import React, { ReactElement } from "react"

import { useTheme } from "@emotion/react"
import { PLACEMENT, TRIGGER_TYPE, Popover as UIPopover } from "baseui/popover"
import { Visibility } from "@emotion-icons/material-outlined"
import {
  LABEL_PLACEMENT,
  STYLE_TYPE,
  Checkbox as UICheckbox,
} from "baseui/checkbox"
import { ToolbarAction } from "@streamlit/lib/src/components/shared/Toolbar"
import { hasLightBackgroundColor } from "@streamlit/lib/src/theme"

import { transparentize } from "color2k"
import { BaseColumn } from "./columns"

export interface ColumnsMenuProps {
  columns: BaseColumn[]
  hideColumn: (columnName: string) => void
  showColumn: (columnName: string) => void
}

const ColumnsMenu: React.FC<ColumnsMenuProps> = ({
  columns,
  hideColumn,
  showColumn,
}): ReactElement => {
  const [open, setOpen] = React.useState(false)
  const theme = useTheme()

  return (
    <div data-testid="stPopover" className="stPopover">
      <UIPopover
        triggerType={TRIGGER_TYPE.click}
        placement={PLACEMENT.bottomLeft}
        autoFocus={true}
        focusLock={true}
        content={() => (
          <div
            style={{
              paddingTop: theme.spacing.xs,
              paddingBottom: theme.spacing.xs,
            }}
          >
            {columns.map(column => (
              <UICheckbox
                checked={column.isHidden !== true}
                onChange={(e: React.ChangeEvent<HTMLInputElement>): void => {
                  if (e.target.checked) {
                    showColumn(column.name)
                  } else {
                    hideColumn(column.name)
                  }
                }}
                aria-label={column.title}
                checkmarkType={STYLE_TYPE.default}
                labelPlacement={LABEL_PLACEMENT.right}
                overrides={{
                  Root: {
                    style: ({
                      $isFocusVisible,
                    }: {
                      $isFocusVisible: boolean
                    }) => ({
                      marginBottom: theme.spacing.none,
                      marginTop: theme.spacing.none,
                      paddingLeft: theme.spacing.sm,
                      paddingRight: theme.spacing.sm,
                      paddingTop: theme.spacing.twoXS,
                      paddingBottom: theme.spacing.twoXS,
                      backgroundColor: $isFocusVisible
                        ? theme.colors.darkenedBgMix25
                        : "",
                      display: "flex",
                      alignItems: "start",
                    }),
                  },
                  Checkmark: {
                    style: ({
                      $isFocusVisible,
                      $checked,
                    }: {
                      $isFocusVisible: boolean
                      $checked: boolean
                    }) => {
                      const borderColor = $checked
                        ? theme.colors.primary
                        : theme.colors.fadedText40

                      return {
                        outline: 0,
                        width: theme.sizes.checkbox,
                        height: theme.sizes.checkbox,
                        marginTop: theme.spacing.twoXS,
                        marginLeft: 0,
                        marginBottom: 0,
                        boxShadow:
                          $isFocusVisible && $checked
                            ? `0 0 0 0.2rem ${transparentize(
                                theme.colors.primary,
                                0.5
                              )}`
                            : "",
                        // This is painfully verbose, but baseweb seems to internally
                        // use the long-hand version, which means we can't use the
                        // shorthand names here as if we do we'll end up with warn
                        // logs spamming us every time a checkbox is rendered.
                        borderLeftWidth: theme.sizes.borderWidth,
                        borderRightWidth: theme.sizes.borderWidth,
                        borderTopWidth: theme.sizes.borderWidth,
                        borderBottomWidth: theme.sizes.borderWidth,
                        borderLeftColor: borderColor,
                        borderRightColor: borderColor,
                        borderTopColor: borderColor,
                        borderBottomColor: borderColor,
                      }
                    },
                  },
                  Label: {
                    style: {
                      lineHeight: theme.lineHeights.small,
                      paddingLeft: theme.spacing.sm,
                      position: "relative",
                      color: theme.colors.bodyText,
                      fontSize: theme.fontSizes.sm,
                      fontWeight: theme.fontWeights.normal,
                    },
                  },
                }}
              >
                {column.title}
              </UICheckbox>
            ))}

            {/* <StyledMenuListItem>Foo</StyledMenuListItem> */}
          </div>
          // <List
          //   items={items}
          //   removable
          //   onChange={({ oldIndex, newIndex }) =>
          //     setItems(
          //       newIndex === -1
          //         ? arrayRemove(items, oldIndex)
          //         : arrayMove(items, oldIndex, newIndex)
          //     )
          //   }
          //   overrides={{
          //     DragHandle: {
          //       style: () => ({
          //         width: theme.iconSizes.sm,
          //       }),
          //     },
          //     Label: {
          //       style: () => ({
          //         fontSize: theme.fontSizes.sm,
          //       }),
          //     },
          //     Item: {
          //       style: () => ({
          //         paddingTop: 0,
          //         paddingBottom: 0,
          //         paddingLeft: 0,
          //         paddingRight: 0,
          //         borderTopColor: "transparent",
          //         borderBottomColor: "transparent",
          //         borderLeftColor: "transparent",
          //         borderRightColor: "transparent",
          //         ":hover": {
          //           borderTopColor: "transparent",
          //           borderBottomColor: "transparent",
          //           borderLeftColor: "transparent",
          //           borderRightColor: "transparent",
          //         },
          //       }),
          //     },
          //     CloseHandle: {
          //       style: () => ({
          //         width: theme.iconSizes.md,
          //       }),
          //     },
          //   }}
          // />
        )}
        isOpen={open}
        onClickOutside={() => setOpen(false)}
        // We need to handle the click here as well to allow closing the
        // popover when the user clicks next to the button in the available
        // width in the surrounding container.
        onClick={() => (open ? setOpen(false) : undefined)}
        onEsc={() => setOpen(false)}
        ignoreBoundary={false}
        overrides={{
          Body: {
            style: {
              // This is annoying, but a bunch of warnings get logged when the
              // shorthand version `borderRadius` is used here since the long
              // names are used by BaseWeb and mixing the two is apparently
              // bad :(
              borderTopLeftRadius: theme.radii.md,
              borderTopRightRadius: theme.radii.md,
              borderBottomLeftRadius: theme.radii.md,
              borderBottomRightRadius: theme.radii.md,

              paddingTop: "0 !important",
              paddingBottom: "0 !important",
              paddingLeft: "0 !important",
              paddingRight: "0 !important",

              backgroundColor: "transparent",
              border: `${theme.sizes.borderWidth} solid ${theme.colors.borderColor}`,
            },
          },
          Inner: {
            style: {
              backgroundColor: hasLightBackgroundColor(theme)
                ? theme.colors.bgColor
                : theme.colors.secondaryBg,
              color: theme.colors.bodyText,
              fontSize: theme.fontSizes.sm,
              fontWeight: theme.fontWeights.normal,
              minWidth: "7rem",
              maxWidth: "15rem",
              maxHeight: "15rem",
              overflow: "auto",
              // See the long comment about `borderRadius`. The same applies here
              // to `padding`.
              paddingTop: "0 !important",
              paddingBottom: "0 !important",
              paddingLeft: "0 !important",
              paddingRight: "0 !important",
            },
          },
        }}
      >
        {/* This needs to be wrapped into a div, otherwise
        the BaseWeb popover implementation will not work correctly. */}
        <div>
          <ToolbarAction
            label="Show/hide columns"
            icon={Visibility}
            onClick={() => {
              setOpen(true)
            }}
          />
        </div>
      </UIPopover>
    </div>
  )
}

export default ColumnsMenu
