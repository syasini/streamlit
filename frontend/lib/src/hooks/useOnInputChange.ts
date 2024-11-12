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

import { Dispatch, SetStateAction, useCallback } from "react"

import { isInForm } from "@streamlit/lib/src/util/utils"
import { ValueWithSource } from "@streamlit/lib/src/hooks/useBasicWidgetState"

export default function useOnInputChange(
  formId: string,
  maxChars: number,
  setDirty: (dirty: boolean) => void,
  setUiValue: (value: string) => void,
  setValueWithSource: Dispatch<
    SetStateAction<ValueWithSource<string | null> | null>
  >
): (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void {
  return useCallback(
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>): void => {
      const { value: newValue } = e.target

      if (maxChars !== 0 && newValue.length > maxChars) {
        return
      }

      setDirty(true)
      setUiValue(newValue)

      // We immediately update its widgetValue on text changes in forms
      // see here for why: https://github.com/streamlit/streamlit/issues/7101
      // The widgetValue won't be passed to the Python script until the form
      // is submitted, so this won't cause the script to re-run.
      if (isInForm({ formId })) {
        // Make sure dirty is true so that enter to submit form text shows
        setValueWithSource({ value: newValue, fromUi: true })
      }
      // If the TextInput is *not* part of a form, we mark it dirty but don't
      // update its value in the WidgetMgr. This means that individual keypresses
      // won't trigger a script re-run.
    },
    [formId, maxChars, setDirty, setUiValue, setValueWithSource]
  )
}
