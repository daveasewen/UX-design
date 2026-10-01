#!/usr/bin/env python3
"""#311 lane C0 — enact s305-D17, D18, D19, D58 in knowledge/components/*.meta.json (format-preserving).
Run from repo root. --dry prints the plan; default writes. The schema is edited by apply_schema.py."""
import json, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jspan import node_at, scan, col_of, dumps_at, delete_key, rename_key, replace_value, STR

COMP = "knowledge/components"
DRY = "--dry" in sys.argv
LOG = []

# ---- format-preserving helpers beyond jspan -------------------------------------------------
def _oneline(s, n):
    return "\n" not in s[n["s"]:n["e"]]

def append_member(s, path, key, obj):
    par = node_at(s, path)
    keys = sorted(par["kstart"], key=lambda k: par["kstart"][k])
    last = keys[-1]; ve = par["kids"][last]["e"]
    if _oneline(s, par):
        ins = ", " + json.dumps(key) + ": " + json.dumps(obj, ensure_ascii=False)
    else:
        col = col_of(s, par["kstart"][last])
        ins = ",\n" + " " * col + json.dumps(key) + ": " + dumps_at(obj, col)
    return s[:ve] + ins + s[ve:]

def append_elem(s, path, obj):
    arr = node_at(s, path)
    last = arr["kids"][-1]
    col = col_of(s, last["s"])
    if _oneline(s, last):
        txt = json.dumps(obj, ensure_ascii=False)
        if s[last["s"]:last["s"] + 2] == "{ ":      # match the file's '{ "name": ... }' house style
            txt = "{ " + txt[1:-1] + " }"
        ins = ",\n" + " " * col + txt
    else:
        ins = ",\n" + " " * col + dumps_at(obj, col)
    return s[:last["e"]] + ins + s[last["e"]:]

def delete_elem(s, path, i):
    arr = node_at(s, path)
    k = arr["kids"]
    if len(k) == 1:
        return s[:arr["s"]] + "[]" + s[arr["e"]:]
    if i > 0:
        return s[:k[i - 1]["e"]] + s[k[i]["e"]:]
    return s[:k[0]["s"]] + s[k[1]["s"]:]

def prop_index(d, name):
    return [p.get("name") for p in d["props"]].index(name)

# ---- D17: a part's own text is a field on the part ------------------------------------------
D17 = ("s305-D17 (Dave, #305 call 16, \"yes\"): a part's own words are a field on the part, not a separate "
       "text part inside it, so the gate checks them with the part (length, wrap, the 44px target, the name a "
       "screen reader hears). Added #311 lane C0.")
def f(name, typ, what, items=None):
    p = {"name": name, "type": typ, "ownText": True, "$note": what + " " + D17}
    if items: p["$items"] = items
    return p
TEXT = {
 "accordion": [f("title", "string", "The header's words: the question or section name the header button reads out (reference snippet: 'How do I set up a standing order?').")],
 "account-card": [f("label", "string", "The account's name and masked number (reference snippet: 'Current account · ···4821')."),
                  f("balance", "number", "The balance the card shows, formatted by the Amount-display primitive (reference snippet: '£3,248.55').")],
 "amount-display": [f("value", "number", "The amount itself; sign and tabular figures are the part's own rules (reference snippet: '3,248.55')."),
                    f("currency", "string", "The currency symbol or code written before the amount, no space (copy-025; reference snippet: 'GBP', '£').")],
 "avatar": [f("name", "string", "The person's or entity's name: the initials variant derives from it and it is the name a screen reader hears (reference snippet: 'JL').")],
 "badge": [f("label", "string", "What the badge says: the count as shown or one short word (reference snippet: '3', '99+', 'New').")],
 "breadcrumbs": [f("trail", "array", "The ancestor path, root first; the last entry is the current page (reference snippet: 'Home / Accounts / Current account / Statements').", "each entry {label, href}; the current page has no href")],
 "button": [f("label", "string", "The button's words (reference snippet: 'Example'; the action bar's 'Confirm payment').")],
 "combobox": [f("label", "string", "The field's label."), f("items", "array", "The options the typed text filters.", "each entry {label, value}")],
 "countdown-timer": [f("label", "string", "What the countdown leads to (reference snippet: 'until session timeout').")],
 "document-row": [f("title", "string", "The document's name (reference snippet: 'June 2026 statement')."),
                  f("detail", "string", "The line under it: period, format and size (reference snippet: '1 Jun – 30 Jun 2026 · PDF · 1.2MB').")],
 "dropdown": [f("label", "string", "The field's label (reference snippet: 'Country of residence')."), f("items", "array", "The options in the list.", "each entry {label, value}; a grouped list adds {group}")],
 "form-layout": [f("title", "string", "The form's heading, the legend of its outer fieldset (reference snippet: 'Add a payee').")],
 "headers": [f("title", "string", "The header's title (reference snippet: 'Statements', 'Good morning, Jordan')."),
             f("subtitle", "string", "The optional line under the title (reference snippet: 'Here's a summary of your accounts.').")],
 "hero": [f("title", "string", "The headline (reference snippet: 'Banking that moves with you.')."), f("intro", "string", "The intro under the headline (reference snippet: 'Manage your money, set goals and get support — all in one place.').")],
 "input-fields": [f("label", "string", "The field's label."), f("help", "string", "The optional help line under the label.")],
 "links": [f("label", "string", "The link's words (reference snippet: 'Open a new account', 'Back to overview').")],
 "list-items": [f("items", "array", "The rows the list shows (reference snippet: 'Amazon · Pending · 22 Jun · Shopping · −1,234.00 HKD').", "each entry {title, detail, value}")],
 "modals": [f("title", "string", "The dialog's title (reference snippet: 'Confirm payment')."), f("body", "string", "The message under the title (reference snippet: 'You're about to send …').")],
 "notifications": [f("title", "string", "The notification's title (reference snippet: 'Notification title.')."), f("message", "string", "The message under it (reference snippet: 'Message description.').")],
 "pagination": [f("page", "number", "The current page (reference snippet: '1')."), f("pages", "number", "How many pages there are (reference snippet: '12').")],
 "popconfirm": [f("title", "string", "The one question the bubble asks (reference snippet: 'Remove Alder Consulting from your payees?').")],
 "quick-actions": [f("items", "array", "The shortcut buttons (reference snippet: 'Transfer', 'Pay bill', 'Top up', 'Send').", "each entry {icon, label}")],
 "reorder": [f("label", "string", "The grab handle's accessible name, naming the item it moves (reference snippet rows: 'Checking', 'Savings', 'ISA').")],
 "secure-entry": [f("label", "string", "The field's label (reference snippet: 'One-time passcode').")],
 "segmented-control": [f("items", "array", "The segments; icon-only segments still carry a label as their accessible name (reference snippet: 'List', 'Grid', 'Table').", "each entry {label, icon?}")],
 "slider": [f("label", "string", "The slider's label (reference snippet: 'Monthly budget').")],
 "status-indicator": [f("label", "string", "The words beside the dot (reference snippet: 'Approved', 'Pending review').")],
 "summary": [f("rows", "array", "The key/value rows (reference snippet: 'To · Jane Smith', 'Amount · £250.00').", "each entry {name, value}")],
 "table": [f("title", "string", "The table's caption (reference snippet: 'Account balances')."), f("rows", "array", "The rows under the header.", "each entry one cell per column, in header order")],
 "tabs": [f("items", "array", "The tabs' labels (reference snippet: 'Overview', 'Transactions', 'Statements').", "each entry {label, icon?}; the `label` switch still decides whether the words show")],
 "tags": [f("label", "string", "The tag's words (reference snippet: 'Savings', '#travel').")],
 "template-auth": [f("title", "string", "The page's title (reference snippet: 'Log on').")],
 "template-confirmation": [f("title", "string", "The page's title (reference snippet: 'Payment sent')."), f("message", "string", "The sentence under it (reference snippet: '£12,480.00 has left the business current account ending 8841.').")],
 "template-create-edit": [f("title", "string", "The page's title, which says whether the record is being created or edited.")],
 "timeline": [f("items", "array", "The entries, newest first (reference snippet: 'Payment to Meridian Supplies · −£1,240.00 · 14:32 · Completed').", "each entry {date, title, value, status}")],
 "tooltip": [f("text", "string", "The tip's words (reference snippet: 'The funds you can spend right now, after …').")],
 "video-player": [f("title", "string", "The video's title (reference snippet: 'How to set up a standing order').")],
 "view-options": [f("items", "array", "The views offered (reference snippet: 'List', 'Grid').", "each entry {label, icon?}")],
}
# a boolean switch that shows words from nowhere becomes the words themselves; absent or empty = no words shown
SWITCH_TO_WORDS = {
 "loading-indicator": ("label", "The caption under the spinner (reference snippet: 'Loading your accounts…'); absent means no visible caption, as the old switch's false did."),
 "search-field": ("label", "The field's label; absent means no visible label, as the old switch's false did (the field still needs an accessible name)."),
 "selection-controls": ("label", "The control's label (reference snippet: 'Email notifications'); absent means no visible label, as the old switch's false did (the control still needs an accessible name)."),
 "popconfirm": ("body", "The consequence sentence beneath the question (reference snippet: 'You can add them again later.'); absent means question-plus-actions only, as the old switch's false did."),
}
MARK_EXISTING = {"meter": "label"}   # the owner of the two alias seats limits-meter and progress-bar

# ---- D19 + D58: a name is a setting or a slot, never both -----------------------------------
SLOT_WINS = {("action-bar", "actions"), ("banner", "actions"), ("confirmation", "actions"), ("drawer", "actions"),
             ("cards", "content"), ("popover", "content"), ("app-shell-nav-rail", "flyout"),
             ("data-grid", "filters"), ("stepper", "steps")}
D58_NAMES = {("data-grid", "columns"), ("data-grid", "filters"), ("modal-lightbox", "items"), ("stepper", "steps"), ("tab-bar", "items")}
def settled(slug, name, as_):
    who = ("s305-D58 (Dave, #305, \"As recommended\")" if (slug, name) in D58_NAMES else "s305-D19 (Dave, #305 call 18, \"yes\")")
    if as_ == "setting":
        return (who + ": data is a setting bound to a data shape; a slot only ever holds another part. This name's slot "
                "named only a data capability, so the name is a setting. The slot is kept below, archived, not deleted. #311 lane C0.")
    return (who + ": a slot only ever holds another part. This name's slot takes a kind of part (accepts.tier), so the name "
            "is a slot. The setting of the same name is kept below, archived, not deleted. #311 lane C0.")

def run():
    counts = {"text_fields_added": 0, "text_metas": 0, "switches_to_words": 0, "marked_existing": 0,
              "settings_won": 0, "slots_won": 0, "bento_slot": 0}
    touched = []
    for path in sorted(glob.glob(os.path.join(COMP, "*.meta.json"))):
        slug = os.path.basename(path)[:-len(".meta.json")]
        s0 = s = open(path, encoding="utf-8").read()
        d = json.loads(s)
        # D17
        if slug in TEXT:
            have = {p.get("name") for p in d.get("props", [])} | set((d.get("slots") or {}).keys())
            for p in TEXT[slug]:
                assert p["name"] not in have, (slug, p["name"], "name already taken")
                s = append_elem(s, ["props"], p); counts["text_fields_added"] += 1
            counts["text_metas"] += 1
        if slug in SWITCH_TO_WORDS:
            name, what = SWITCH_TO_WORDS[slug]
            d = json.loads(s); i = prop_index(d, name); old = d["props"][i]
            assert old["type"] == "boolean", (slug, name)
            new = {"name": name, "type": "string", "ownText": True, "$note": what + " " + D17,
                   "$wasSwitch": {k: v for k, v in old.items()}}
            s = replace_value(s, ["props", i], new); counts["switches_to_words"] += 1
        if slug in MARK_EXISTING:
            d = json.loads(s); i = prop_index(d, MARK_EXISTING[slug])
            assert d["props"][i]["type"] == "string"
            s = append_member(s, ["props", i], "ownText", True)
            s = append_member(s, ["props", i], "$ownText", "s305-D17: the meter's words; they also serve its two alias seats, limits-meter and progress-bar, which cannot carry props (s210-D5). #311 lane C0.")
            counts["marked_existing"] += 1
        # D19 / D58
        d = json.loads(s)
        slots = {k: v for k, v in (d.get("slots") or {}).items() if not k.startswith("$")}
        pnames = [p.get("name") for p in d.get("props", [])]
        for name in sorted(set(pnames) & set(slots)):
            d = json.loads(s)
            slot = d["slots"][name]; i = prop_index(d, name); prop = d["props"][i]
            has_part = bool((slot.get("accepts") or {}).get("tier") or (slot.get("accepts") or {}).get("kind"))
            if (slug, name) in SLOT_WINS:
                assert has_part, (slug, name, "slot-win without a part tier")
                if (slug, name) == ("data-grid", "filters"):
                    # s305-D58's named cost: the applied search terms need a name of their own
                    s = replace_value(s, ["props", i, "name"], "terms")
                    s = append_member(s, ["props", i], "$renamedFrom",
                                      "filters — s305-D58 (Dave, \"As recommended\") made `filters` the slot and named the cost: the applied search terms need a name of their own. `terms` is this lane's plain word for them, Dave's to keep or rename. #311 lane C0.")
                    s = append_member(s, ["slots", name], "$settled", settled(slug, name, "slot") .replace(
                        "The setting of the same name is kept below, archived, not deleted.", "The setting of the same name is renamed `terms`, not deleted."))
                else:
                    s = append_member(s, ["slots", name], "$wasSetting", {"$settled": settled(slug, name, "slot"), "prop": prop})
                    s = delete_elem(s, ["props"], i)
                counts["slots_won"] += 1
            else:
                assert not has_part, (slug, name, "setting-win with a part tier")
                cap = list((slot.get("accepts") or {}).get("capability") or [])
                bd = {"capability": cap}
                if d.get("shape"):
                    bd["shape"] = d["shape"]
                s = append_member(s, ["props", i], "bindsData", bd)
                if (slug, name) == ("tab-bar", "items"):
                    d2 = json.loads(s); p2 = d2["props"][i]
                    new = {"name": "items", "type": "array", "ownText": True, "bindsData": p2["bindsData"],
                           "$note": "3–5 destinations, each an icon and a label. s305-D58 named the cost: the setting must carry each destination's icon and label, not only the count it held. " + D17,
                           "$items": "each entry {icon, label, href}; 3 to 5 entries",
                           "$wasCount": {k: v for k, v in prop.items()}}
                    s = replace_value(s, ["props", i], new)
                s = append_member(s, ["props", i], "$wasSlot", {"$settled": settled(slug, name, "setting"), "slot": slot})
                if len(json.loads(s)["slots"]) == 1:
                    s = delete_key(s, [], "slots")          # the slot was the only member: the key goes, the archive stays on the prop
                else:
                    s = delete_key(s, ["slots"], name)
                counts["settings_won"] += 1
        # D18: the bento wall's tiles slot
        if slug == "template-dashboard-bento":
            d = json.loads(s)
            assert "slots" not in d
            tiles = {"tiles": {
                "accepts": {"provides": ["headline-metric", "status-surface", "chart", "record-list"]},
                "use": "The tiles the wall holds side by side; the wall's own rules place them (spans 3 or 6 of 12, the gutters, no orphan).",
                "required": True, "multiple": True,
                "$status": "s305-D18 (Dave, #305 call 17, \"yes\"): four parts side by side are held by Apollo's bento wall, with a tiles slot that accepts parts by what they provide, not by A2UI's rows and columns. Built #311 lane C0.",
                "$provides": "The four roles are this lane's reading: three are the roles of the parts this template already composes ($composes: kpi-tile/stat-card → headline-metric, chart-bar → chart, summary and status-indicator → status-surface); record-list is the data grid of template-dashboard's $composes and the list of the proposal's worked example. Widening or narrowing the list is Dave's."}}
            s = insert_after(s, "props", "slots", tiles)
            counts["bento_slot"] += 1
        if s != s0:
            json.loads(s)  # still JSON
            touched.append(path)
            if not DRY:
                open(path, "w", encoding="utf-8").write(s)
    print(json.dumps(counts)); print("touched", len(touched))
    for t in touched: print("  ", t)

def insert_after(s, after_key, key, obj):
    from jspan import insert_after_key
    return insert_after_key(s, [], after_key, key, obj)

if __name__ == "__main__":
    run()
