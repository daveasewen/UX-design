You are working in a project folder that is a design-system pack someone has just unzipped and opened (the folder you are in, Apollo-Spider-v1.0.15/). Treat it as a designer's fresh session in VS Code: you have only this folder. There is nobody to answer questions in this session.

Conditions for this session (they hold for the whole task):
- Read only inside this folder. Do not read anything outside it (no other directories on this machine). Inside it, do not read the SOURCE of any file whose name starts with an underscore and ends in .py (`_*.py`); you MAY RUN such a script when a skill tells you to run it. Do not read any folder named `notes/`, `reviews/`, `_DECISION-HISTORY/`, nor `_CHAIN.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md`, `knowledge/_rulings.json`, and do not run `_memento_search.py`.
- No eyes: do not render, screenshot, open a browser, run Playwright/Chromium/node-based page checks, or run any gate or validator during the build. Build, then stop where the skill says you are done.
- `briefs/` does not exist, so the grill fires. Nobody will answer it. ANSWERS: all six grill questions are skipped (a full skip is called at question 1): use each skill-declared default. The bento check ("dashboard bento — is that right?") is also skipped, which counts as a yes. Write each answer into the brief (skips marked *skipped/defaulted* with the default they cause), say any default out loud in your reply, and proceed without stopping.
- Follow the skill honestly, as a capable model would in VS Code: read files the way you naturally would, copy what the skill tells you to copy; do not game it in either direction.
- Write your outputs into `out/` in this folder: `out/dashboard.html` (per the skill's output rules), `out/brief.md` (the grill answers + your decisions), `out/GAPS.md` (the Gaps list the skill requires), and `out/READ-LOG.md` — every file you opened, how much of it you read (lines or bytes), and what you copied vs re-drew. If the dashboard needs sibling files (css, svg) to resolve, put them beside it in `out/` and say so.
- Note in READ-LOG.md which file the slash command below resolved to.

The designer's request, verbatim:

/generate-from-canon build me a financial dashboard for corporate international banking. Please make the all the interactive elements work such as filtering and navigation.
