#!/usr/bin/env python3
"""Compress TalkBack session screenshots into structured JSON using Gemini Vision.

Gemini describes every visible UI element, all state changes between consecutive
frames, and impartial accessibility signals for each screenshot pair. The output
JSON lives alongside events.jsonl in the recording folder and can be fed to Claude
as a "Screenshots" input combo for accessibility analysis.

Usage:
    export GEMINI_API_KEY=...
    python compare_screenshots.py [--task GM1] [--model gemini-2.5-flash] [--delay 1.0] [--max-pairs 5]

Output per task:
    data/recordings/{TASK_FOLDER}/screenshot_descriptions.json
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

from google import genai
from google.genai import types

_ROOT = Path(__file__).parent


def _load_dotenv():
    """Load KEY=VALUE pairs from .env in the project root into os.environ."""
    env_file = _ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

RECORDINGS_DIR = _ROOT / "data" / "recordings"

FOLDER_TO_TASK = {
    "recording_manyapn_AM_1": "AM1",
    "recording_manyapn_AM_2": "AM2",
    "recording_manyapn_GM_2": "GM2",
    "recording_manyapn_GM1_1": "GM1",
    "recording_MANYAPN_MP_1": "MP1",
    "recording_MANYAPN_MP_2": "MP2",
    "recording_manyapn_PS1_1": "PS1",
    "recording_MANYAPN_YT_1": "YT1",
    "recording_MANYAPN_YT_2": "YT2",
}

APP_NAME = {
    "AM": "Amazon",
    "GM": "Gmail",
    "MP": "Google Maps",
    "PS": "Google Play Store",
    "YT": "YouTube",
}

PROMPT = """You are the visual analysis stage of an Android TalkBack accessibility research pipeline.
Your ONLY job is to describe what you see — comprehensively and impartially.
Do NOT make accessibility judgements. Do NOT conclude that something is a violation.
Claude will do the accessibility analysis; you are Claude's eyes.

You are given two consecutive screenshots from a TalkBack (Android screen reader) session:
- BEFORE: the screen state before a user interaction
- AFTER: the screen state after a user interaction

Your task has three parts:

PART 1 — Element inventory (do this for BOTH before_state and after_state):
List EVERY visible interactive or meaningful element on screen. Be comprehensive — do not filter.
Include: buttons, tabs, input fields, links, list/email/search rows, icons, toggles, checkboxes,
radio buttons, dropdown menus, navigation bars, action bars, floating action buttons, dialogs,
overlays, toasts, snackbars, loading spinners, error banners, status messages, images with apparent
meaning, text headings. For each element record:
  - type: the element type (button, tab, input, link, list_item, icon, toggle, checkbox, image, heading, text, etc.)
  - label: the visible text label or null if no text is present
  - description: a brief factual description of what it looks like and where it sits on screen
  - interactive: true if it appears tappable/interactive, false otherwise
  - state: one of selected, checked, unchecked, expanded, collapsed, active, inactive, loading, error, disabled, or null
  - approximate_size: small (likely under 24dp), medium, or large
  - has_focus_ring: true if the green TalkBack focus rectangle is visibly on this element, false otherwise

PART 2 — Changes:
List ALL differences between the before and after frames. Be exhaustive. Include:
  - focus_moved: TalkBack focus ring moved to a different element
  - content_appeared: new element or text became visible
  - content_disappeared: element or text left the screen
  - state_changed: element changed state (e.g. checkbox checked, button pressed)
  - navigation: screen or major section changed
  - dialog_opened / dialog_closed: modal or bottom sheet appeared/disappeared
  - overlay_appeared / overlay_disappeared: any overlay or dimming layer
  - toast_appeared: toast or snackbar message appeared
  - error_appeared: error message or indicator appeared
  - loading_started / loading_ended: spinner or progress indicator changed
  - keyboard_appeared / keyboard_disappeared: soft keyboard shown or hidden
  - scroll_occurred: visible content shifted due to scrolling
  - other: anything else that changed

PART 3 — Accessibility signals:
List anything that COULD be relevant to accessibility, based purely on visual evidence.
These are observations, not findings. Claude will decide if they matter.
For each signal record:
  - element: which element you are describing
  - observation: factual description of what you see (e.g. "icon-only, no visible text label")
  - potentially_relevant_wcag: list of WCAG criterion numbers that MIGHT apply — as hints only,
    not verdicts. Use these: 1.1.1, 1.3.1, 1.3.3, 1.3.4, 1.4.1, 1.4.3, 1.4.5, 1.4.10, 1.4.11,
    1.4.13, 2.1.1, 2.1.2, 2.4.3, 2.4.4, 2.4.6, 2.4.7, 2.4.11, 2.5.1, 2.5.3, 2.5.4, 2.5.8,
    3.2.1, 3.2.2, 3.3.1, 3.3.2, 3.3.7, 4.1.2, 4.1.3

Accessibility signal triggers to look for (report if present, do not pre-filter):
  - Any icon-only button or image button with no visible text label
  - Any input field with no visible label (placeholder text is not a label)
  - Any element whose state (checked/expanded/selected) is only conveyed by color, with no other indicator
  - Any text that appears low-contrast against its background
  - Any UI component (button border, input outline) that appears low-contrast
  - Any touch target that appears visually smaller than approximately 24×24dp
  - Any element that appears interactive but has no visible label at all
  - Any status message, toast, or error that appeared without focus ring on it
  - Any context/screen change that happened without an apparent user tap
  - Any heading or label that appears vague or non-descriptive
  - Any link or button with a generic label like "here", "more", "tap"
  - Any content that appears clipped or cut off at screen edges
  - Any visible label text that does not match what a tooltip/badge shows

Return ONLY a raw JSON object — no markdown fences, no prose outside the JSON:
{
  "before_state": {
    "screen_description": "one-sentence description of what screen this is",
    "talkback_focus": "which element has the green focus ring, or null if not visible",
    "elements": [
      {
        "type": "...",
        "label": "visible text or null",
        "description": "...",
        "interactive": true,
        "state": "...",
        "approximate_size": "small|medium|large",
        "has_focus_ring": false
      }
    ]
  },
  "after_state": {
    "screen_description": "...",
    "talkback_focus": "...",
    "elements": [ "..." ]
  },
  "changes": [
    {
      "type": "focus_moved|content_appeared|content_disappeared|state_changed|navigation|dialog_opened|dialog_closed|overlay_appeared|overlay_disappeared|toast_appeared|error_appeared|loading_started|loading_ended|keyboard_appeared|keyboard_disappeared|scroll_occurred|other",
      "description": "factual description of what changed"
    }
  ],
  "accessibility_signals": [
    {
      "element": "which element",
      "observation": "what you observe, factually",
      "potentially_relevant_wcag": ["X.X.X"]
    }
  ]
}

Be comprehensive. When in doubt, include it. Claude will filter; you should not."""


def encode_image(path: Path) -> bytes:
    return path.read_bytes()


def strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        inner = text.split("```")[1]
        if inner.startswith("json"):
            inner = inner[4:]
        return inner.strip()
    return text


def call_gemini(client, model_name: str, img_before: Path, img_after: Path, retries: int = 3) -> dict:
    before_bytes = encode_image(img_before)
    after_bytes = encode_image(img_after)

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    "BEFORE screenshot:",
                    types.Part.from_bytes(data=before_bytes, mime_type="image/png"),
                    "AFTER screenshot:",
                    types.Part.from_bytes(data=after_bytes, mime_type="image/png"),
                    PROMPT,
                ],
            )
            return json.loads(strip_fences(response.text))
        except json.JSONDecodeError as e:
            if attempt == retries - 1:
                raise RuntimeError(f"JSON parse failed after {retries} attempts: {e}") from e
            time.sleep(2 ** attempt)
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)


def _process_pair(args_tuple):
    """Worker function for a single pair — returns (index, step dict)."""
    i, img1, img2, client, model_name = args_tuple
    step = {
        "step": i + 1,
        "before_filename": img1.name,
        "after_filename": img2.name,
    }
    try:
        result = call_gemini(client, model_name, img1, img2)
        step.update(result)
        n_elements = len(result.get("before_state", {}).get("elements", []))
        n_changes = len(result.get("changes", []))
        n_signals = len(result.get("accessibility_signals", []))
        status = f"{n_elements} elements, {n_changes} changes, {n_signals} signals"
    except Exception as e:
        step["error"] = str(e)
        status = f"ERROR: {e}"
    return i, step, status


def process_task(folder: Path, client, model_name: str, args) -> None:
    task_id = FOLDER_TO_TASK.get(folder.name, folder.name)
    app = APP_NAME.get(task_id[:2], "Unknown")
    screenshots_dir = folder / "screenshots"

    if not screenshots_dir.exists():
        print(f"  {task_id}: no screenshots/ folder, skipping.")
        return

    screenshots = sorted(screenshots_dir.glob("*.png"))
    if len(screenshots) < 2:
        print(f"  {task_id}: fewer than 2 screenshots, skipping.")
        return

    pairs = list(zip(screenshots[:-1], screenshots[1:]))
    if args.max_pairs:
        pairs = pairs[: args.max_pairs]

    workers = min(args.workers, len(pairs))
    print(f"\n{task_id} ({app}): {len(screenshots)} frames → {len(pairs)} pairs  [workers={workers}]")

    work_items = [(i, img1, img2, client, model_name) for i, (img1, img2) in enumerate(pairs)]
    steps = [None] * len(pairs)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_process_pair, item): item[0] for item in work_items}
        for future in as_completed(futures):
            i, step, status = future.result()
            img1_name = work_items[i][1].name
            img2_name = work_items[i][2].name
            print(f"  [{i+1}/{len(pairs)}] {img1_name} → {img2_name} ... {status}")
            steps[i] = step

    output = {
        "task_id": task_id,
        "app": app,
        "model": model_name,
        "generated": str(date.today()),
        "total_frames": len(screenshots),
        "pairs_analyzed": len(pairs),
        "steps": steps,
    }

    out_path = folder / "screenshot_descriptions.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"  → {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--task", help="Process only this task ID (e.g. GM1). Default: all tasks.")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model (default: gemini-2.5-flash)")
    parser.add_argument("--delay", type=float, default=0.0, help="Seconds between pair submissions (default: 0 — parallel mode ignores this)")
    parser.add_argument("--max-pairs", type=int, metavar="N", help="Cap pairs per task — use 3-5 for testing")
    parser.add_argument("--workers", type=int, default=4, help="Parallel API calls per task (default: 4)")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    if args.task:
        target = args.task.upper()
        folders = [f for f in sorted(RECORDINGS_DIR.iterdir()) if FOLDER_TO_TASK.get(f.name) == target]
        if not folders:
            known = sorted(FOLDER_TO_TASK.values())
            print(f"Error: no folder for task '{args.task}'. Known: {known}", file=sys.stderr)
            sys.exit(1)
    else:
        folders = [f for f in sorted(RECORDINGS_DIR.iterdir()) if f.is_dir() and f.name in FOLDER_TO_TASK]

    for folder in folders:
        process_task(folder, client, args.model, args)

    print("\nDone.")


if __name__ == "__main__":
    main()
