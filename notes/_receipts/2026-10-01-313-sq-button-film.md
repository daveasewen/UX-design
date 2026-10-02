# #313 side-quest receipt — film B, "It started with a button"

provenance: 313-sq · 2026-10-01 18:2x BST · Opus 5.5 side-quest WORKER seat (cloud, linked to Dave's computer)
status: in progress — script v1 put to Dave
files touched: `notes/_lanes/313-sq/button-film/SCRIPT-v1.md` (new) · this receipt (new)
commit state: UNCOMMITTED, for the #313 conductor
rulings: none

## What landed
Script v1, 15 beats, ~75 s (estimate), built on the Apple "Intention" structure (a question, short lines, motion that answers each line) — original lines, none of Apple's copy. His words verbatim in the script file.

## Said to him
The seat cannot watch video or hear audio; it read the Vimeo page (title, description) and works from knowledge of the film. Offered to step through it in his Chrome for stills.

## Open
Words on screen or not (seat recommends on) · button label · voice-over.

Context gauge at authoring: 🟢 GREEN ~15% (ESTIMATE)

## ADDENDUM — Thu 18:28 BST, by addition

> lines 3 to 8 could become a quick run of single words: Colour. Words. Shape. State. Reason, judgment...  maybe
>
> Maybe we see what this looks like, I wondered if we said or asked something like this makes room for 'the user, their needs, your empathy and your craft' that sense anyway.
>
> words on screen, use univers as its the house font.
>
> tbf I like your initial draught too lets have both to review

LANDED in `notes/_lanes/313-sq/button-film/` (all new, uncommitted): `button-film.src.html` + `build_button_film.py` → `button-film-a.html` (script v1, 76.8 s) and `button-film-b.html` (single-word run + "So you have room for what matters." / The user. / Their needs. / Your empathy. / Your craft., 65.7 s); Univers = HSBC_MtUnivers_Latin Light + Regular embedded from `knowledge/assets/fonts/_desktop/TTF` (`document.fonts.check` true at the seat); simple synthesised score (pad, a bell per idea, a low touch on the press) — not yet listened to. `render_button_stills.py` → `stills-a/` (27) `stills-b/` (26), page errors 0. `build_review.py` → `REVIEW-v1.html` (two columns, no horizontal scroll at 390). Contact sheets `contact-a.png`, `contact-b.png` checked by eye at this seat; one round of fixes after the first look (button no longer goes brown mid-morph; words raised nearer the forms; cut B's room ring smaller, the craft grid kept inside it).
Seat's calls he may reverse: the button reads "Get started"; "Judgement" with the British e; in cut B the red dot sits at the figure's chest (the heart) for the user/needs/empathy beats.
Not done: MP4 (waits for his eye), a listen of the score.

## ADDENDUM — Thu 19:24–19:25 BST, by addition

> I've changed the script md. van I have a new version
>
> can I have a scrub bar for the movie with the option to leave comments at the point I choose

His edit is in `SCRIPT-v1.md` itself (saved 18:23 BST on disk; his changes: the line wording, a plain button with no text, "the red dot always transforms into the subject, it doest remain in the centre on teh beats, everything resolves back into the button", the colour beat in "the colour full palette from supercharge").
Read as: Supercharge's full colour palette = the 2026 supporting palette, `color/supporting/*` in `knowledge/tokens/colour.json` (10 families x 5 steps, its $description: "PREFERRED for all NEW work"), injected at build. "Resolves back into the button" = the close: the red dot grows back into the plain button, with "Apollo" under it. Cut B left as v1.
LANDED (new, uncommitted): `button-film-v2.src.html` + `build_button_film_v2.py` → `button-film-a-v2.html` (77.2 s); stills `stills-a-v2/` (28), `contact-a-v2.png`; `build_review_v2.py` → `REVIEW-v2.html` (A v2 beside B v1). Review chrome in the film: scrub bar with beat ticks, comments pinned to a time (M or "Comment here"), list panel, Copy (markdown to clipboard) and Export .md; comments live in the browser's localStorage under `apollo-button-film-v2-comments`. Driven at the seat: two comments saved, listed, stored, then cleared; page errors 0.
Seat's calls he may reverse: label "Continue" with the red as the i's dot; where the red sits per beat (a corner of each rectangle, the touch point when pressed, the spinner's head, the tip of the tick, one person in the crowd, the last link of the chain, one of the many, one of the islands, the inner shell, the button on the screen).
