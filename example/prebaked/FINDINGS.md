# Findings

Append-only. Written by Claude while building Discovery Log.

## 2026-11-11, Pain counts were inflated by repeated tags
**What happened:** The first version counted "pricing, Pricing, pricing" in one interview as three mentions, so one person could push a pain to the top.
**Cause:** Tags were counted as typed, with no cleanup.
**Rule from now on:** Clean tags when they are saved (trim, lowercase, remove repeats). Count a pain once per interview. A test covers it.

## 2026-11-11, Bad saved data crashed the page on load
**What happened:** A test that put broken text in browser storage made the app fail before showing anything.
**Cause:** The saved data was read without checking it.
**Rule from now on:** Anything read from storage is checked. If it is not a valid list, start empty. A test covers it.

## 2026-11-11, Notes with angle brackets broke the layout
**What happened:** A note containing "<b>" was shown as formatting instead of text.
**Cause:** User text was placed into the page without escaping.
**Rule from now on:** Every piece of user text is escaped before it is shown.
