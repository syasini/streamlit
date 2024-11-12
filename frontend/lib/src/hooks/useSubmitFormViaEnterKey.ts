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

import { useCallback } from "react"

import { WidgetStateManager } from "@streamlit/lib/src/WidgetStateManager"

const isEnterKeyPressed = (
  event: Partial<React.KeyboardEvent<HTMLElement>> & {
    metaKey: boolean
    ctrlKey: boolean
    /** @deprecated */
    keyCode: number
    key: string
  }
): boolean => {
  const { keyCode, key } = event

  // Using keyCode as well due to some different behaviors on Windows
  // https://bugs.chromium.org/p/chromium/issues/detail?id=79407
  return (
    (key === "Enter" || keyCode === 13 || keyCode === 10) &&
    // Do not send the sentence being composed when Enter is typed into the IME.
    !(event.nativeEvent?.isComposing === true)
  )
}

/**
 * Will return a memoized function that will call commitWidgetValue and submit the form
 * if the Enter key (+ optionally the command key) is pressed.
 *
 * @param formId of the form to submit
 * @param commitWidgetValue callback to call
 * @param callCommitWidgetValue whether to call commitWidgetValue
 * @param widgetMgr used to handle form submission
 * @param fragmentId
 * @param requireCommandKey if true, the metaKey or ctrlKey must be pressed to trigger the callback
 * @returns memoized callback
 */
export default function useSubmitFormViaEnterKey(
  formId: string,
  commitWidgetValue: () => void,
  callCommitWidgetValue: boolean,
  widgetMgr: WidgetStateManager,
  fragmentId?: string,
  requireCommandKey = false
): (
  e: Partial<React.KeyboardEvent<HTMLElement>> & {
    metaKey: boolean
    ctrlKey: boolean
    keyCode: number
    key: string
  }
) => void {
  return useCallback(
    (
      e: Partial<React.KeyboardEvent<HTMLElement>> & {
        metaKey: boolean
        ctrlKey: boolean
        keyCode: number
        key: string
      }
    ): void => {
      const isCommandKeyPressed = requireCommandKey
        ? e.metaKey || e.ctrlKey
        : true
      console.log(
        "useSubmitFormViaEnterKey. isCommandKeyPressed",
        isCommandKeyPressed
      )
      if (!isEnterKeyPressed(e) || !isCommandKeyPressed) {
        return
      }

      e.preventDefault?.()
      if (callCommitWidgetValue) {
        commitWidgetValue()
      }

      if (widgetMgr.allowFormEnterToSubmit(formId)) {
        widgetMgr.submitForm(formId, fragmentId)
      }
    },
    [
      formId,
      fragmentId,
      callCommitWidgetValue,
      commitWidgetValue,
      widgetMgr,
      requireCommandKey,
    ]
  )
}
