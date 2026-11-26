# Click-through demo kit

A click-through is a recorded demo you can present like a live one. It is a series of real screenshots. On each screen a pulsing highlight shows where to click, and the speaker notes say what to tell the audience. Everything is in **one HTML file**, so it works offline, from a laptop, a shared drive or an email attachment.

This folder holds the **PHP2SHELL** demo for the IBM Concert webinar *Turn IT risk into action*. It also works as a kit for building your own click-through.

> **Just want to watch it?** Open [`click-through.html`](click-through.html) on GitHub, click **Download raw file** (the ⤓ icon), and open the downloaded file in your browser. Or use **Code → Download ZIP** and open `click-through.html` from the folder. GitHub does not run the page itself.

---

## 1. Watch or present the PHP2SHELL demo

Open **`click-through.html`** in Chrome, Edge or Safari. You need no server or internet connection.

| Key | What it does |
|---|---|
| **→** or click the highlight | Next step |
| **←** | Back |
| **N** | Speaker notes: what to say on this screen |
| **Home** | First screen |
| **?** | Help |
| **E** | Edit mode (for authors, see section 4) |

- The buttons at the top jump to a scene.
- Every screen has its own link, so `click-through.html#31` opens screen 31.
- **Keep the notes closed while you share your screen.** The audience would see them.

### What is in the demo

41 screens, about 14 minutes, recorded on 25 and 26 November 2026:

| Scene | Screens | The story |
|---|---|---|
| 1. Problem | 1–2 | PHP2SHELL (CVE-2026-109618) is critical, and the fix is PHP 8.3.36. |
| 2. Scan | 3–6 | Every push builds the image, scans it and sends the results to IBM Concert. |
| 3. Understand | 7–10 | Concert Protect: one CVE, two applications, blast radius, the fixed version. |
| 4. Prioritize | 11–12 | Same CVE, different risk: storefront 10, internal reports 4.7. |
| 5. Act | 13–22 | Ticket to the owner, then a Concert workflow opens a pull request with scan evidence. |
| 6. Proof | 23–27 | Merge, rebuild, redeploy, then Concert closes the finding and the ticket is closed. |
| 7. Secure Coder | 28–41 | Shift left: IBM Concert Secure Coder in IBM Bob fixes Log4Shell in a Java app, from the scan to the merged pull request and the rescan. |

The environment was TechZone, Concert 3.1.0, with the GitHub repos `storefront-php` and `ecommerce-app`. The screens are real, but some were lightly edited for clarity: an old commit message hidden, a toast or a floating button removed, an inaccurate table in a generated PR description hidden. No result was changed.

---

## 2. What is in this folder

| File | What it is |
|---|---|
| `click-through.html` | The finished demo. **This is the only file you need to share.** |
| `shots.json` | The script: one entry per screen. |
| `screens/` | The screenshots, one per entry in `shots.json`, named `<id>.png`. |
| `player.html` | The player template (layout, keys, highlight). |
| `build.py` | Combines `shots.json`, `screens/` and `player.html` into `click-through.html`. |
| `deck.json` | Settings: title and output file name. |
| `SHOT-LIST.md` | A list of the screens and what to click on each. |
| `marked/` | Copies of the screens with the highlight drawn on, used by the Word delivery guide. |
| `unused/` | Screens taken out of the demo. |

---

## 3. Change the PHP2SHELL demo

**Change what to say or click:** edit the `say` or `do` text in `shots.json`, then run:

```bash
python3 build.py
```

**Replace a screenshot:** save the new picture as `screens/<id>.png` with the same name, then run `python3 build.py`. If the layout changed, set the highlight again (section 4).

**Remove a screen:** delete its entry in `shots.json`. **Reorder:** move entries. The `scene` text sets the buttons at the top, and screens are shown in file order.

---

## 4. Build your own click-through

### Step 1: Start a new folder

Copy `player.html` and `build.py` into a new folder. Create a `screens/` folder there, and add a `deck.json`:

```json
{ "title": "My product: first demo", "out": "click-through.html" }
```

### Step 2: Write the script before you capture

Write the story first: what problem it solves, the 4–7 scenes, and the one thing each scene must land. Then list the screens in `shots.json`:

```json
[
  {
    "scene": "1. Problem",
    "id": "01-advisory",
    "capture": "The advisory page, with Critical and the fixed version visible",
    "do": "Point at Critical and 8.3.36.",
    "say": "This is PHP2SHELL, a critical remote code execution vulnerability in PHP.",
    "hotspot": [2.5, 36.22, 71.25, 21.11],
    "mark": "#d9480f"
  }
]
```

| Field | Meaning |
|---|---|
| `scene` | Scene name. Screens with the same scene are grouped under one button. Number it ("1. Problem") so the order is clear. |
| `id` | File name of the screenshot in `screens/` (without `.png`). Number it (`01-…`, `02-…`) so files sort in order. |
| `capture` | A note for the person taking the screenshot: what must be visible. |
| `do` | What the presenter clicks. Shown in the footer. |
| `say` | What the presenter says. Shown with **N**. Write it to be spoken, about 15–25 seconds per screen. |
| `hotspot` | `[left, top, width, height]` of the highlight, in **percent** of the screenshot. Use `null` for no highlight. |
| `mark` | Highlight colour. Use `#ffd60a` (yellow) on dark screens and `#d9480f` (orange) on light ones. |
| `steps` | Optional: several highlights on one screen, shown one after another. A list of hotspots, used instead of `hotspot`. |

You can build before you have any screenshots. Missing screens show as placeholders with their `capture` text, so you can rehearse the flow first.

### Step 3: Capture the screens

- **Use one size for every screen: 1600 × 900 (16:9).** The highlight is stored in percent, so the size must not change between captures.
- **Make it sharp.** Set the browser window to 1600 × 900 and take the screenshot on a Retina screen, or zoom the page to 125–150 % so the text is large enough to read when shared over Teams or Zoom.
- **Show one idea per screen.** Scroll so the thing you will click is in view and nothing important is cut off.
- **Clean up first:** close toasts and pop-ups, hide notifications, use a demo account, and blank or blur personal data, tokens and internal URLs you do not want to share.
- **Use real runs.** Record a real end-to-end run and capture each step as it happens. Do not mock results: the audience will ask questions.
- Save each picture as `screens/<id>.png`.

### Step 4: Set the highlights

1. Run `python3 build.py` and open `click-through.html`.
2. Go to the screen and press **E** (edit mode).
3. Drag a box over the area to click. The bar at the bottom shows `"hotspot": [l, t, w, h]` and copies it to the clipboard.
4. Paste it into that entry in `shots.json`. Press **E** again to leave edit mode.
5. Run `python3 build.py` again.

### Step 5: Rehearse and time it

- Read the `say` text aloud with a timer. 130–150 spoken words is about one minute, plus 3–5 seconds per click.
- Check that one scene leads into the next: the last line of a scene should set up the next one.
- Press **N** while you rehearse, and keep it closed when you present.

### Step 6: Share it

Share **only `click-through.html`**, for example on Box, a shared drive, Slack or by email. It is a single file of about 10–15 MB, and it opens in any browser with no installation. To point someone at one screen, add `#<number>` to the link.

---

## 5. Requirements

- **Python 3.8 or later.** Nothing else is required.
- To shrink screenshots, `build.py` uses **Pillow** (`pip install pillow`) if it is installed, macOS `sips` otherwise, and if neither is there it embeds the files as they are, which gives a larger HTML file.
- Options: `python3 build.py --title "My demo" --out my-demo.html --max-width 2000`.
- `--fragment` writes the page without `<!doctype>` and `<html>`, for hosts that wrap pages themselves, such as a claude.ai artifact.

---

## 6. Tips that saved time on PHP2SHELL

- **Run the story end to end once before you capture anything.** Problems show up in the flow, not on single screens.
- **Keep one story per scene.** We first had the Secure Coder part between the pull request and its merge, and the story broke. It now has a scene of its own at the end.
- **Compare like with like.** If you show "42 critical" before, show the same, unfiltered view after.
- **Reset the environment after recording** (revert the fix, close test tickets) so a live backup still works.
- **Check every screen at full size** for floating buttons ("Latest", "Scroll to bottom"), mouse cursors and toasts before you build.
