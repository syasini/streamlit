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
import { Metric as MetricProto } from "@streamlit/lib/src/proto"
import { EmotionTheme } from "@streamlit/lib/src/theme"
import { labelVisibilityProtoValueToEnum } from "@streamlit/lib/src/util/utils"
import Icon from "@streamlit/lib/src/components/shared/Icon"
import { useTheme } from "@emotion/react"
import { ArrowDownward, ArrowUpward } from "@emotion-icons/material-outlined"
import { StyledWidgetLabelHelpInline } from "@streamlit/lib/src/components/widgets/BaseWidget"
import TooltipIcon from "@streamlit/lib/src/components/shared/TooltipIcon"
import { Placement } from "@streamlit/lib/src/components/shared/Tooltip"
import StreamlitMarkdown from "@streamlit/lib/src/components/shared/StreamlitMarkdown"
import {
  StyledTruncateText,
  StyledMetricLabelText,
  StyledMetricValueText,
  StyledMetricDeltaText,
} from "./styled-components"

export interface MetricProps {
  element: MetricProto
}

export default function Metric({ element }: MetricProps): ReactElement {
  const { colors, radii }: EmotionTheme = useTheme()
  const { MetricColor, MetricDirection } = MetricProto

  let direction: any = null
  let color = ""

  switch (element.color) {
    case MetricColor.RED:
      color = colors.red
      break
    case MetricColor.GREEN:
      color = colors.green
      break
    // this must be grey
    default:
      color = colors.fadedText60
      break
  }

  switch (element.direction) {
    case MetricDirection.DOWN:
      direction = ArrowDownward
      break
    case MetricDirection.UP:
      direction = ArrowUpward
      break
    // this must be none
    default:
      direction = null
      break
  }

  const arrowMargin = "0 threeXS 0 0"
  const deltaStyle = { color }

  const { body, label, delta, labelVisibility, help, border } = element
  const deltaExists = delta !== ""

  const style = {
    ...(border && {
      border: `1px solid ${colors.fadedText10}`,
      borderRadius: radii.lg,
      padding: "calc(1em - 1px)", // 1px to account for border
    }),
  }

  return (
    <div data-testid="stMetric" style={style}>
      <StyledMetricLabelText
        data-testid="stMetricLabel"
        visibility={labelVisibilityProtoValueToEnum(labelVisibility?.value)}
      >
        <StyledTruncateText>
          <StreamlitMarkdown source={label} allowHTML={false} isLabel />
        </StyledTruncateText>
        {help && (
          <StyledWidgetLabelHelpInline>
            <TooltipIcon content={help} placement={Placement.TOP_RIGHT} />
          </StyledWidgetLabelHelpInline>
        )}
      </StyledMetricLabelText>
      <StyledMetricValueText data-testid="stMetricValue">
        <StyledTruncateText> {body} </StyledTruncateText>
      </StyledMetricValueText>
      {deltaExists && (
        <StyledMetricDeltaText data-testid="stMetricDelta" style={deltaStyle}>
          <Icon
            testid={
              // if direction is null, icon will be null
              direction === ArrowUpward
                ? "stMetricDeltaIcon-Up"
                : "stMetricDeltaIcon-Down"
            }
            content={direction}
            size="lg"
            margin={arrowMargin}
          />
          <StyledTruncateText> {delta} </StyledTruncateText>
        </StyledMetricDeltaText>
      )}
    </div>
  )
}
