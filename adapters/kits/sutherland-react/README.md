# Sutherland React kit — read me first

This folder is everything the work machine needs to map Sutherland's React components onto Apollo's parts. It does not need the Apollo repo, a network, or anything installed beyond Python 3 (which VS Code's Python extension or any Mac or Windows box with Python already has). Carry it on a USB stick, zip it into an email, or drop it in OneDrive.

Where it starts: Apollo has no Sutherland mapping yet. No Sutherland component, prop or import name is known on the Apollo side; the kit is the list of Apollo parts for the Copilot agent to find in Sutherland. Four of those parts (cards, list items, status indicator, table) once had empty placeholder slots, added in June, that read "TODO — confirm in Sutherland repo" and name nothing. They are not a head start.

## What is in it

- `README.md` — this page.
- `FIRST-PROMPT.md` — the prompt to paste into Copilot chat. Nothing to edit.
- `BRIEF-FOR-COPILOT.md` — the full instructions the Copilot agent follows. You do not need to read it, but it is plain English if you want to.
- `manifest.json` — the file that gets filled. It has an empty row for every Apollo part in the list, with every Sutherland-side name set to `null`. Copilot fills the nulls.
- `parts.json` — the seventeen Apollo parts to map (the four that once had empty placeholder slots, then cohort one: button, tabs, table, date picker, metric, menus and select (both dropdown), accordion, slider, switch (selection controls), text input (input fields), dialog (modals), tooltip, pagination, notification). Pulled straight from the metas.
- `apollo-tokens.json` — the names of Apollo's semantic tokens, so Sutherland's tokens can be placed on them. Names only, no values.
- `schema.json` — the shape of the manifest. The checker reads it.
- `check_manifest.py` — the checker. One file, no installs.

## The six steps

1. Copy this whole folder to the work machine. Keep the files together; the checker looks for its neighbours.
2. In VS Code, open a workspace with two folders: this kit folder and Sutherland's repo (the one you run the Spider release from, the folder with its `package.json`). File menu, Add Folder to Workspace.
3. Open Copilot chat, switch it to Agent mode.
4. Open `FIRST-PROMPT.md`, copy everything between the two lines, paste it into Copilot chat, send.
5. Let it work. It reads Sutherland's component files, fills `manifest.json`, and runs the checker after each part. If it asks where Sutherland is, point it at the repo root. If it offers to write a script to do the mapping, tell it no, read the files and fill the JSON.
6. When it says the checker printed `PASS`, bring back two files: `manifest.json` and `FILL-NOTES.md`. Email, USB stick, OneDrive, whichever. Nothing else in the folder changes.

Back on this side, the file is filed as `adapters/sutherland-react.json` in the Apollo repo and the Apollo gate re-checks it. From there the side-by-side renders start, and each binding moves from unverified to rendered only when a render is on record, and to accepted only when you have looked at it and said so.

## If something goes wrong

- The checker says a file is missing: the folder was split up. Copy it again, whole.
- The checker says `FAIL` with a list: paste the list back into Copilot chat and say "fix these". Every line names where in the JSON the problem is.
- Copilot cannot find a Sutherland component for a part: that is a finding, not a failure. The brief tells it to leave the name `null`, say where it looked, and carry on. The gaps are what we want to know.
- You want to check the file yourself: open a terminal in the kit folder and run `python3 check_manifest.py manifest.json`.

## What this is for

Dave's ruling of 1 October 2026 (Apollo for other libraries, call 5): an adapter manifest per client library, Apollo governs, theirs renders, with a required list of what is not mapped. Sutherland is the first library. This kit is the "two computers" answer: the Apollo side wrote the questions, the work machine, which can see Sutherland, writes the answers, and one JSON file travels between them.
