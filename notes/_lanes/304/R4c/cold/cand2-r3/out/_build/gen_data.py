"""Deterministic placeholder data for the CEO prototype. Every figure on every page derives from this
one object (skill rule 13). Illustrative only — no real entities, rates or balances."""
import json, random, datetime as dt
R = random.Random(20260926)
END = dt.date(2026, 9, 26)
DAYS = [(END - dt.timedelta(days=29 - i)).isoformat() for i in range(30)]
# ILLUSTRATIVE FX: units of currency per 1 GBP, fixed for the 30-day report (stated on every page)
FX = {"GBP": 1.0, "EUR": 1.1690, "USD": 1.2710, "SGD": 1.7120, "HKD": 9.9150, "AED": 4.6680, "INR": 106.25, "JPY": 188.40}
REGIONS = ["UK", "Europe", "Americas", "Asia-Pacific", "Middle East"]
ENT = [
 ("MH-UK", "Meridian Holdings plc", "UK", "GBP"),
 ("MH-DE", "Meridian Europe GmbH", "Europe", "EUR"),
 ("MH-FR", "Meridian France SAS", "Europe", "EUR"),
 ("MH-US", "Meridian Americas Inc.", "Americas", "USD"),
 ("MH-SG", "Meridian Asia Pacific Pte Ltd", "Asia-Pacific", "SGD"),
 ("MH-HK", "Meridian Hong Kong Ltd", "Asia-Pacific", "HKD"),
 ("MH-AE", "Meridian Middle East FZE", "Middle East", "AED"),
 ("MH-IN", "Meridian India Pvt Ltd", "Asia-Pacific", "INR"),
]
entities = [{"id": e[0], "name": e[1], "region": e[2], "ccy": e[3]} for e in ENT]
def gbp(amount, ccy): return round(amount / FX[ccy], 2)

# ---- accounts + 30-day balance series (local currency, millions-scale) ----
ACC_TYPES = ["Operating", "Collections", "Payroll", "Liquidity deposit"]
scale = {"GBP": 1, "EUR": 1.17, "USD": 1.27, "SGD": 1.71, "HKD": 9.9, "AED": 4.67, "INR": 106, "JPY": 188}
accounts = []
n = 0
for e in entities:
    k = 4 if e["id"] in ("MH-UK", "MH-US", "MH-DE") else 3 if e["id"] in ("MH-SG", "MH-HK") else 2
    for j in range(k):
        n += 1
        ccy = e["ccy"] if not (j == 2 and e["ccy"] != "USD") else "USD"
        base = R.uniform(8, 120) * 1e6 * scale[ccy]
        if e["id"] == "MH-UK" and j == 0: base = 310e6
        series, v = [], base
        for d in DAYS:
            v = max(base * 0.35, v * (1 + R.gauss(0.0015, 0.03)))
            series.append(round(v, 0))
        accounts.append({"id": "AC-%03d" % n, "entity": e["id"], "ccy": ccy, "type": ACC_TYPES[j % 4],
                         "iban": "GB%02d HBUK 4005 %04d %04d" % (R.randint(10, 99), R.randint(1000, 9999), R.randint(1000, 9999)) if ccy == "GBP" else "HSBC-%s-%06d" % (ccy, R.randint(100000, 999999)),
                         "series": series})

# ---- transactions (settled, last 30 days) ----
CPTY = {"Receipt": ["Harlow Retail Group", "Kestrel Logistics", "Orchid Pharma", "Northgate Systems", "Brightwater Utilities", "Solent Marine"],
        "Supplier payment": ["Vantage Components", "Pioneer Steel", "Clearview Packaging", "Atlas Freight", "Summit Chemicals", "Harbour Energy"],
        "Payroll": ["Payroll run"], "Intercompany": ["Meridian intercompany"], "FX settlement": ["HSBC Markets"],
        "Tax": ["Tax authority"], "Loan interest": ["HSBC syndicated facility"]}
TT = [("Receipt", 0.34, 1), ("Supplier payment", 0.30, -1), ("Payroll", 0.08, -1), ("Intercompany", 0.12, 0), ("FX settlement", 0.08, 0), ("Tax", 0.04, -1), ("Loan interest", 0.04, -1)]
transactions = []
for i in range(260):
    acc = R.choice(accounts); e = next(x for x in entities if x["id"] == acc["entity"])
    r = R.random(); c = 0
    for t, p, s in TT:
        c += p
        if r <= c: break
    sign = s if s else R.choice([1, -1])
    mag = R.lognormvariate(13.2, 1.1) * scale[acc["ccy"]]
    amt = round(sign * mag, 2)
    d = R.choice(DAYS)
    transactions.append({"id": "TX-%05d" % (40000 + i), "date": d, "account": acc["id"], "entity": acc["entity"], "region": e["region"],
                         "ccy": acc["ccy"], "type": t, "cpty": R.choice(CPTY[t]), "ref": "%s-%04d" % (t[:3].upper(), R.randint(1000, 9999)),
                         "amount": amt, "gbp": gbp(amt, acc["ccy"])})
transactions.sort(key=lambda x: x["date"], reverse=True)

# ---- payments awaiting / through approval ----
BEN = ["Vantage Components", "Pioneer Steel", "Clearview Packaging", "Atlas Freight", "Summit Chemicals", "Harbour Energy", "Delta Ports Authority",
       "Kowloon Precision Ltd", "Gulf Industrial Supply", "Tata Engineering Services", "Rhein Maschinenbau AG", "Lyon Logistique SA", "Pacific Semiconductors"]
MAKERS = ["A. Clarke (Group treasury)", "S. Müller (Europe finance)", "J. Ortiz (Americas finance)", "L. Tan (APAC treasury)", "R. Haddad (Middle East finance)"]
payments = []
for i in range(56):
    e = R.choice(entities); ccy = e["ccy"] if R.random() < 0.7 else R.choice(["USD", "EUR", "GBP"])
    amt = round(R.lognormvariate(14.3, 1.0) * scale[ccy], 2)
    created = R.choice(DAYS[-12:])
    st = R.choices(["Pending approval", "Approved", "Released", "Rejected"], [0.34, 0.16, 0.42, 0.08])[0]
    g = gbp(amt, ccy)
    payments.append({"id": "PAY-%05d" % (81200 + i), "date": created, "valueDate": (dt.date.fromisoformat(created) + dt.timedelta(days=R.choice([1, 2, 3]))).isoformat(),
                     "entity": e["id"], "region": e["region"], "ccy": ccy, "amount": amt, "gbp": g, "beneficiary": R.choice(BEN),
                     "method": R.choice(["SWIFT MT103", "Faster Payments", "SEPA credit transfer", "CHAPS", "Fedwire", "RTGS"]),
                     "status": st, "maker": R.choice(MAKERS), "approvals": 2 if g >= 5e6 else 1, "purpose": R.choice(["Supplier invoice", "Capital expenditure", "Dividend to parent", "Intercompany funding", "Tax settlement", "Freight and logistics"])})
# two large pending payments so the two-approver and above-limit rules have real records to bite on
for p_, gbp_target in zip([p for p in payments if p["status"] == "Pending approval"][:2], [12.4e6, 31.7e6]):
    p_["gbp"] = gbp_target; p_["amount"] = round(gbp_target * FX[p_["ccy"]], 2); p_["approvals"] = 2
    p_["purpose"] = "Capital expenditure"
payments.sort(key=lambda x: x["date"], reverse=True)

# ---- facilities ----
facilities = [
 {"id": "FAC-RCF", "name": "Syndicated revolving credit facility", "lender": "HSBC-led syndicate (7 banks)", "type": "Committed RCF", "ccy": "GBP", "limit": 750e6, "drawn": 185e6, "maturity": "2029-06-30", "committed": True, "entity": "MH-UK", "region": "UK"},
 {"id": "FAC-TLA", "name": "Term loan A", "lender": "HSBC UK Bank plc", "type": "Term loan", "ccy": "USD", "limit": 400e6, "drawn": 400e6, "maturity": "2027-03-31", "committed": True, "entity": "MH-US", "region": "Americas"},
 {"id": "FAC-ECP", "name": "Euro commercial paper programme", "lender": "Dealer panel (HSBC arranger)", "type": "Commercial paper", "ccy": "EUR", "limit": 300e6, "drawn": 120e6, "maturity": "2026-11-14", "committed": False, "entity": "MH-DE", "region": "Europe"},
 {"id": "FAC-SGRCF", "name": "APAC bilateral revolver", "lender": "HSBC Singapore", "type": "Committed RCF", "ccy": "SGD", "limit": 250e6, "drawn": 40e6, "maturity": "2028-09-30", "committed": True, "entity": "MH-SG", "region": "Asia-Pacific"},
 {"id": "FAC-OD-UK", "name": "UK overdraft", "lender": "HSBC UK Bank plc", "type": "Overdraft", "ccy": "GBP", "limit": 50e6, "drawn": 6e6, "maturity": "2027-01-31", "committed": False, "entity": "MH-UK", "region": "UK"},
 {"id": "FAC-OD-AE", "name": "UAE working capital line", "lender": "HSBC Bank Middle East", "type": "Overdraft", "ccy": "AED", "limit": 180e6, "drawn": 72e6, "maturity": "2026-12-31", "committed": False, "entity": "MH-AE", "region": "Middle East"},
 {"id": "FAC-TF-HK", "name": "Trade loan facility", "lender": "HSBC Hong Kong", "type": "Trade loan", "ccy": "HKD", "limit": 900e6, "drawn": 410e6, "maturity": "2027-06-30", "committed": True, "entity": "MH-HK", "region": "Asia-Pacific"},
 {"id": "FAC-IN", "name": "India working capital facility", "lender": "HSBC India", "type": "Committed RCF", "ccy": "INR", "limit": 6.0e9, "drawn": 2.1e9, "maturity": "2027-09-30", "committed": True, "entity": "MH-IN", "region": "Asia-Pacific"},
]
for f in facilities:
    f["limitGbp"] = gbp(f["limit"], f["ccy"]); f["drawnGbp"] = gbp(f["drawn"], f["ccy"])
# drawn history for RCF-like facilities over 30 days (GBP eq, per facility) — small moves
for f in facilities:
    s, v = [], f["drawnGbp"] * 0.9
    for d in DAYS:
        v = min(f["limitGbp"], max(0, v * (1 + R.gauss(0.004, 0.02))))
        s.append(round(v, 0))
    s[-1] = f["drawnGbp"]; f["drawnSeries"] = s

# ---- daily flows (GBP eq, group) ----
flows = []
for d in DAYS:
    tin = sum(t["gbp"] for t in transactions if t["date"] == d and t["gbp"] > 0)
    tout = -sum(t["gbp"] for t in transactions if t["date"] == d and t["gbp"] < 0)
    flows.append({"date": d, "inflow": round(tin, 0), "outflow": round(tout, 0)})

# ---- FX: daily OHLC for GBP/USD and closes for other pairs ----
fxs = {}
for pair, spot in [("GBP/USD", 1.2710), ("GBP/EUR", 1.1690), ("GBP/SGD", 1.7120), ("GBP/HKD", 9.9150), ("GBP/AED", 4.6680)]:
    o = spot * (1 - 0.018); rows = []
    for i, d in enumerate(DAYS):
        c = o * (1 + R.gauss(0.0006, 0.0042))
        if i == len(DAYS) - 1: c = spot
        h = max(o, c) * (1 + abs(R.gauss(0, 0.0018))); l = min(o, c) * (1 - abs(R.gauss(0, 0.0018)))
        rows.append([round(o, 4), round(h, 4), round(l, 4), round(c, 4)]); o = c
    fxs[pair] = rows
deals = []
for i in range(44):
    e = R.choice(entities); pair = R.choice(["GBP/USD", "GBP/EUR", "GBP/SGD", "GBP/HKD", "GBP/AED", "EUR/USD", "USD/INR"])
    notional = round(R.lognormvariate(15.4, 0.8), -3)
    kind = R.choices(["Spot", "Forward", "Swap"], [0.35, 0.45, 0.2])[0]
    base = pair.split("/")[0]; g = gbp(notional * {"GBP": 1, "EUR": 1.169, "USD": 1.271}.get(base, 1) / {"GBP": 1, "EUR": 1.169, "USD": 1.271}.get(base, 1), "GBP") if base == "GBP" else gbp(notional, base)
    d = R.choice(DAYS)
    deals.append({"id": "FXD-%05d" % (70100 + i), "date": d, "pair": pair, "side": R.choice(["Buy", "Sell"]), "kind": kind, "notional": notional, "base": base,
                  "gbp": g, "entity": e["id"], "region": e["region"],
                  "maturity": (dt.date.fromisoformat(d) + dt.timedelta(days=2 if kind == "Spot" else R.choice([30, 60, 90, 180]))).isoformat(),
                  "status": "Settled" if kind == "Spot" and d < DAYS[-3] else R.choice(["Confirmed", "Open", "Confirmed"])})
deals.sort(key=lambda x: x["date"], reverse=True)

# ---- exposures / limits ----
BANKS = ["HSBC Bank plc", "HSBC Bank USA", "HSBC Continental Europe", "HSBC Singapore", "HSBC Hong Kong", "HSBC Middle East", "Counterparty bank A", "Counterparty bank B", "Money market fund C"]
INSTR = ["Deposit", "FX forward", "Trade loan", "Guarantee", "Derivative MTM"]
positions = []
for i in range(46):
    e = R.choice(entities); ccy = e["ccy"] if R.random() < 0.65 else R.choice(["USD", "EUR"])
    inst = R.choice(INSTR)
    lim = round(R.choice([25, 40, 50, 75, 100, 150, 200]) * 1e6, 0)
    util = R.choice([R.uniform(0.2, 0.85)] * 5 + [R.uniform(0.9, 1.0), R.uniform(1.0, 1.18)])
    positions.append({"id": "POS-%04d" % (3100 + i), "date": R.choice(DAYS[-5:]), "entity": e["id"], "region": e["region"], "ccy": ccy, "instrument": inst,
                      "cpty": R.choice(BANKS), "exposure": round(lim * util, 0), "limit": lim, "util": round(util * 100, 1)})
exceptions = []
for p in sorted(positions, key=lambda x: -x["util"]):
    if p["util"] >= 92:
        exceptions.append({"id": "EXC-%04d" % (500 + len(exceptions)), "position": p["id"], "date": p["date"], "region": p["region"], "entity": p["entity"],
                           "ccy": p["ccy"], "cpty": p["cpty"], "instrument": p["instrument"], "util": p["util"], "exposure": p["exposure"], "limit": p["limit"],
                           "severity": "Breach" if p["util"] > 100 else "Near limit", "status": "Open"})

# ---- trade finance ----
TI = ["Import LC", "Export LC", "Standby LC", "Bank guarantee", "Documentary collection", "Supply chain finance"]
trade = []
for i in range(40):
    e = R.choice(entities); ccy = R.choice([e["ccy"], "USD", "USD", "EUR"])
    amt = round(R.lognormvariate(14.2, 0.9) * scale[ccy], -2)
    issued = (END - dt.timedelta(days=R.randint(5, 200))).isoformat()
    expiry = (END + dt.timedelta(days=R.randint(-3, 240))).isoformat()
    t = R.choice(TI)
    trade.append({"id": "TF-%05d" % (22000 + i), "date": issued, "expiry": expiry, "type": t, "entity": e["id"], "region": e["region"], "ccy": ccy,
                  "amount": amt, "gbp": gbp(amt, ccy), "cpty": R.choice(BEN), "status": R.choice(["Issued", "Issued", "Documents presented", "Amendment pending", "Settled"])})
trade.sort(key=lambda x: x["date"], reverse=True)

reports = [{"id": "RPT-%03d" % (i + 1), "name": n_, "category": c_, "frequency": f_, "date": R.choice(DAYS[-6:]), "format": "CSV"} for i, (n_, c_, f_) in enumerate([
 ("Group cash position", "Liquidity", "Daily"), ("Liquidity and funding headroom", "Liquidity", "Daily"), ("Facility utilisation", "Funding", "Weekly"),
 ("Payments released", "Payments", "Daily"), ("Payments awaiting approval", "Payments", "Daily"), ("FX deals and hedges", "Markets", "Daily"),
 ("Counterparty exposure and limits", "Risk", "Daily"), ("Limit exceptions and acknowledgements", "Risk", "Weekly"), ("Trade finance outstanding", "Trade", "Weekly"),
 ("Expiring trade instruments", "Trade", "Weekly"), ("Account balances by entity", "Accounts", "Daily"), ("Transactions by type", "Accounts", "Monthly"),
 ("Service requests", "Service", "Monthly"), ("Regional exposure summary", "Risk", "Monthly")])]

MSG = [("Relationship team", "Your quarterly relationship review — proposed agenda", "Relationship"),
       ("Global Liquidity and Cash Management", "Notional pooling: EUR header account now live", "Liquidity"),
       ("Trade Services", "Documents presented under TF-22007 — discrepancies noted", "Trade"),
       ("HSBC Markets", "GBP outlook ahead of the MPC decision", "Markets"),
       ("Client Services", "Scheduled maintenance: HSBCnet, Saturday 03:00–05:00 UK", "Service"),
       ("Relationship team", "RCF extension option — indicative terms", "Funding"),
       ("Trade Services", "Standby LC renewal due in 21 days", "Trade"),
       ("Global Liquidity and Cash Management", "Interest rate change on GBP liquidity deposits", "Liquidity"),
       ("Client Services", "New sanctions screening fields for SWIFT payments", "Payments"),
       ("HSBC Markets", "Hedge effectiveness pack for Q3 is ready", "Markets"),
       ("Relationship team", "Invitation: HSBC treasury leaders forum, London", "Relationship"),
       ("Client Services", "User entitlement review due for 4 users", "Service"),
       ("Trade Services", "Supply chain finance programme — onboarding of 3 suppliers", "Trade"),
       ("Global Liquidity and Cash Management", "Payment cut-off times change for HKD RTGS", "Payments"),
       ("HSBC Markets", "INR forward points widened this week", "Markets"),
       ("Client Services", "Your service request SR-1043 has been resolved", "Service")]
messages = [{"id": "MSG-%04d" % (900 + i), "date": DAYS[-1 - (i * 2 % 29)], "from": f, "subject": s, "category": c, "read": i % 3 == 2,
             "body": "Illustrative message from %s. %s. This prototype holds no real correspondence; reply to raise a simulated service request." % (f, s)}
            for i, (f, s, c) in enumerate(MSG)]
messages.sort(key=lambda x: x["date"], reverse=True)
SRT = ["Payment investigation", "User entitlement change", "Account opening", "Statement request", "Facility query", "Trade instrument amendment"]
requests = [{"id": "SR-%04d" % (1040 + i), "date": DAYS[R.randint(0, 29)], "type": R.choice(SRT), "subject": s_, "status": R.choice(["Open", "In progress", "Awaiting you", "Closed", "Closed"]),
             "entity": R.choice(entities)["id"], "priority": R.choice(["Normal", "High"])} for i, s_ in enumerate([
    "Recall of duplicate supplier payment", "Add approver for Americas entity", "Open EUR collections account", "Nine-month statements for audit",
    "Clarify RCF commitment fee", "Amend expiry on import LC", "Trace inbound USD receipt", "Remove leaver entitlements", "HKD account signing mandate", "Duplicate interest charge query"])]

MIN_BUFFER = 600e6
data = {"asOf": DAYS[-1], "days": DAYS, "fx": FX, "fxNote": "Illustrative FX, units per 1 GBP, fixed for this 30-day view — not market rates.",
        "regions": REGIONS, "entities": entities, "accounts": accounts, "transactions": transactions, "payments": payments,
        "facilities": facilities, "flows": flows, "fxSeries": fxs, "deals": deals, "positions": positions, "exceptions": exceptions,
        "trade": trade, "reports": reports, "messages": messages, "requests": requests, "minBuffer": MIN_BUFFER,
        "user": {"name": "Eleanor Hart", "role": "Group chief executive", "entity": "MH-UK", "limitGbp": 25e6}}
print("const CEO_DATA = " + json.dumps(data, separators=(",", ":")) + ";")
