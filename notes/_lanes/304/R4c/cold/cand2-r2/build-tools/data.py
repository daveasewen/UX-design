"""CEO prototype DATA model — deterministic, illustrative only. Writes data.json."""
import json, random, datetime as dt, sys

R = random.Random(20260927)
AS_OF = dt.date(2026, 9, 27)
DAYS = [(AS_OF - dt.timedelta(days=29 - i)).isoformat() for i in range(30)]

# Explicit illustrative FX: GBP per 1 unit of currency (never live rates)
FX = {"GBP": 1.0, "USD": 0.7460, "EUR": 0.8420, "HKD": 0.0957, "SGD": 0.5790,
      "CNY": 0.1046, "AED": 0.2031, "INR": 0.00893, "JPY": 0.00502}

REGIONS = [
    {"id": "UK", "name": "United Kingdom"},
    {"id": "EU", "name": "Europe"},
    {"id": "AM", "name": "Americas"},
    {"id": "AP", "name": "Asia Pacific"},
    {"id": "ME", "name": "Middle East and Africa"},
]
ENTITIES = [
    {"id": "E01", "name": "Northwind Holdings plc", "region": "UK", "ccy": "GBP"},
    {"id": "E02", "name": "Northwind Europe BV", "region": "EU", "ccy": "EUR"},
    {"id": "E03", "name": "Northwind Americas Inc", "region": "AM", "ccy": "USD"},
    {"id": "E04", "name": "Northwind Asia Pacific Ltd", "region": "AP", "ccy": "HKD"},
    {"id": "E05", "name": "Northwind Singapore Pte Ltd", "region": "AP", "ccy": "SGD"},
    {"id": "E06", "name": "Northwind Shanghai Co Ltd", "region": "AP", "ccy": "CNY"},
    {"id": "E07", "name": "Northwind Gulf FZE", "region": "ME", "ccy": "AED"},
    {"id": "E08", "name": "Northwind India Pvt Ltd", "region": "AP", "ccy": "INR"},
]
ENT = {e["id"]: e for e in ENTITIES}

COUNTERPARTIES = ["Atlas Logistics", "Bramble Foods", "Cobalt Mining", "Delta Freight", "Evergreen Paper",
                  "Fairhaven Steel", "Granite Pharma", "Harbour Components", "Ionic Energy", "Juniper Textiles",
                  "Kestrel Aviation", "Lumen Semiconductors", "Meridian Retail", "Northgate Chemicals",
                  "Orchid Electronics", "Pinnacle Packaging", "Quayside Shipping", "Redwood Construction",
                  "Solace Healthcare", "Tidewater Agri"]
BANKS = ["HSBC UK", "HSBC Bank plc Paris", "HSBC Bank USA", "The Hongkong and Shanghai Banking Corporation",
         "HSBC Bank Middle East", "HSBC Singapore"]


def gbp(ccy, amt):
    return round(amt * FX[ccy], 2)


def walk(start, n, vol, drift=0.0):
    v, out = start, []
    for _ in range(n):
        v = max(start * 0.35, v * (1 + drift + R.uniform(-vol, vol)))
        out.append(round(v, 2))
    return out


# ---------------- accounts with 30-day balances (local ccy) ----------------
ACC_TYPES = ["Operating", "Collections", "Concentration", "Term deposit"]
accounts = []
aid = 1
for e in ENTITIES:
    for t in ACC_TYPES[: R.choice([2, 3, 3, 4])]:
        base_gbp = R.uniform(4, 60) * 1e6 * (1.6 if e["id"] == "E01" else 1)
        local = base_gbp / FX[e["ccy"]]
        series = walk(local, 30, 0.035, 0.001)
        accounts.append({"id": "A%02d" % aid, "entity": e["id"], "type": t, "ccy": e["ccy"],
                         "number": "••••%04d" % R.randint(1000, 9999), "bank": R.choice(BANKS),
                         "balances": series})
        aid += 1
    # a USD account for most entities
    if e["ccy"] != "USD" and R.random() < 0.6:
        local = R.uniform(3, 25) * 1e6 / FX["USD"]
        accounts.append({"id": "A%02d" % aid, "entity": e["id"], "type": "Operating", "ccy": "USD",
                         "number": "••••%04d" % R.randint(1000, 9999), "bank": R.choice(BANKS),
                         "balances": walk(local, 30, 0.04)})
        aid += 1

# ---------------- transactions ----------------
TX_TYPES = ["Receipt", "Supplier payment", "Payroll", "Intercompany", "FX settlement", "Tax", "Card settlement"]
transactions = []
for i in range(1, 221):
    a = R.choice(accounts)
    t = R.choice(TX_TYPES)
    sign = 1 if t in ("Receipt", "Card settlement") or (t == "Intercompany" and R.random() < .5) else -1
    local = round(R.uniform(0.05, 4.5) * 1e6 / FX[a["ccy"]] * (0.2 if t == "Tax" else 1), 2)
    d = R.choice(DAYS)
    cp = R.choice(COUNTERPARTIES) if t not in ("Payroll", "Tax", "Intercompany") else (
        "Staff payroll" if t == "Payroll" else "HMRC and local tax" if t == "Tax" else ENT[R.choice([x["id"] for x in ENTITIES if x["id"] != a["entity"]])]["name"])
    transactions.append({"id": "TX%04d" % (5000 + i), "date": d, "entity": a["entity"], "account": a["id"],
                         "counterparty": cp, "ref": "%s-%05d" % (t[:3].upper(), R.randint(10000, 99999)),
                         "type": t, "ccy": a["ccy"], "amount": sign * local, "gbp": sign * gbp(a["ccy"], local)})

# ---------------- facilities (funding) ----------------
FAC_TYPES = ["Revolving credit facility", "Overdraft", "Term loan", "Commercial paper", "Trade line"]
facilities = []
for i, e in enumerate(ENTITIES):
    for k in range(R.choice([1, 2])):
        typ = FAC_TYPES[(i + k) % len(FAC_TYPES)]
        limit = round(R.uniform(40, 220) * 1e6 * (2.2 if e["id"] == "E01" else 1), -5)
        drawn_series = walk(limit * R.uniform(.2, .7), 30, .02)
        drawn_series = [min(x, limit * .97) for x in drawn_series]
        committed = typ in ("Revolving credit facility", "Term loan", "Trade line")
        mat = (AS_OF + dt.timedelta(days=R.randint(40, 1400))).isoformat()
        facilities.append({"id": "F%02d" % (len(facilities) + 1), "entity": e["id"], "type": typ,
                           "lender": R.choice(["HSBC syndicate", "HSBC UK", "HSBC Bank plc", "Club of 6 banks"]),
                           "committed": committed, "limit": limit, "drawn": [round(x, -3) for x in drawn_series],
                           "maturity": mat, "margin": round(R.uniform(0.8, 2.4), 2)})

# ---------------- positions + limits (risk) ----------------
POS_TYPES = ["Deposit", "Receivable", "FX forward", "Loan", "Investment"]
positions = []
for i in range(1, 97):
    e = R.choice(ENTITIES)
    ccy = R.choice([e["ccy"], e["ccy"], "USD", "EUR", "GBP"])
    typ = R.choice(POS_TYPES)
    local = round(R.uniform(2, 70) * 1e6 / FX[ccy], -3)
    positions.append({"id": "POS-%04d" % (3000 + i), "entity": e["id"], "region": e["region"], "ccy": ccy,
                      "type": typ, "counterparty": R.choice(COUNTERPARTIES + BANKS), "notional": local,
                      "gbp": gbp(ccy, local),
                      "maturity": (AS_OF + dt.timedelta(days=R.randint(5, 700))).isoformat(),
                      "opened": R.choice(DAYS[:20])})
region_limits = {"UK": 1200e6, "EU": 700e6, "AM": 650e6, "AP": 900e6, "ME": 260e6}
ccy_limits = {"GBP": 1100e6, "USD": 800e6, "EUR": 650e6, "HKD": 260e6, "SGD": 180e6, "CNY": 200e6, "AED": 150e6, "INR": 120e6}
# 30 days of exposure per region (GBP)
exposure_hist = {}
for r in REGIONS:
    cur = sum(p["gbp"] for p in positions if p["region"] == r["id"])
    series = list(reversed(walk(cur, 30, .025)))
    series[-1] = round(cur, 2)
    exposure_hist[r["id"]] = series

# ---------------- risk exceptions ----------------
EXC_TYPES = ["Limit breach", "Counterparty concentration", "Tenor breach", "Rating downgrade", "Settlement fail"]
exceptions = []
for i in range(1, 25):
    p = R.choice(positions)
    typ = EXC_TYPES[i % len(EXC_TYPES)]
    over = round(R.uniform(0.3, 28) * 1e6, -3)
    material = over > 8e6 or typ in ("Limit breach", "Rating downgrade") and over > 4e6
    status = "Open" if i <= 16 else "Acknowledged"
    d = R.choice(DAYS[10:])
    exceptions.append({"id": "EXC-%03d" % (400 + i), "date": d, "type": typ, "entity": p["entity"], "region": p["region"],
                       "ccy": p["ccy"], "counterparty": p["counterparty"], "position": p["id"], "over": over,
                       "severity": "Material" if material else "Moderate", "status": status,
                       "owner": R.choice(["Group Treasurer", "Head of Credit Risk", "Regional CFO", "Chief Risk Officer"]),
                       "audit": ([{"at": d + "T09:12", "by": "Risk engine", "note": "Exception raised automatically."}] +
                                 ([{"at": d + "T15:40", "by": "Chief Risk Officer", "note": "Acknowledged; remediation plan agreed with the regional CFO."}] if status == "Acknowledged" else []))})

# ---------------- payments ----------------
PAY_STATUS = ["Pending approval"] * 5 + ["Approved", "Released", "Released", "Scheduled", "Rejected"]
payments = []
for i in range(1, 91):
    e = R.choice(ENTITIES)
    ccy = R.choice([e["ccy"], e["ccy"], "USD", "EUR"])
    local = round(R.uniform(0.02, 9) * 1e6 / FX[ccy], 2)
    st = PAY_STATUS[i % len(PAY_STATUS)] if i > 6 else "Pending approval"
    created = R.choice(DAYS[-12:]) if st == "Pending approval" else R.choice(DAYS)
    payments.append({"id": "PAY-%04d" % (1000 + i), "date": created, "entity": e["id"], "region": e["region"],
                     "beneficiary": R.choice(COUNTERPARTIES), "ccy": ccy, "amount": local, "gbp": gbp(ccy, local),
                     "method": R.choice(["SWIFT MT103", "SEPA credit transfer", "CHAPS", "ACH", "RTGS"]),
                     "maker": R.choice(["A. Patel (AP clerk)", "J. Moreno (Treasury analyst)", "L. Chen (Regional finance)"]),
                     "valueDate": (dt.date.fromisoformat(created) + dt.timedelta(days=R.randint(0, 5))).isoformat(),
                     "status": st, "purpose": R.choice(["Supplier invoice", "Capital expenditure", "Intercompany funding", "Dividend", "Tax settlement"]),
                     "audit": [{"at": created + "T08:30", "by": "Maker", "note": "Payment created and submitted for approval."}]})

# ---------------- FX ----------------
fx_pairs = ["USD", "EUR", "HKD", "SGD", "CNY", "AED"]
fx_series = {}
for c in fx_pairs:
    base = 1 / FX[c]   # currency units per GBP
    s = walk(base, 30, .004)
    s[-1] = round(base, 4)
    fx_series[c] = [round(x, 4) for x in s]
ohlc = {"open": [], "high": [], "low": [], "close": []}
prev = fx_series["USD"][0]
for v in fx_series["USD"]:
    o = prev; c = v
    hi = max(o, c) + R.uniform(0.001, 0.009); lo = min(o, c) - R.uniform(0.001, 0.009)
    for k, x in (("open", o), ("high", hi), ("low", lo), ("close", c)):
        ohlc[k].append(round(x, 4))
    prev = c
fx_deals = []
for i in range(1, 61):
    e = R.choice(ENTITIES)
    c = R.choice(fx_pairs)
    local = round(R.uniform(0.5, 25) * 1e6 / FX[c], -3)
    side = R.choice(["Buy", "Sell"])
    d = R.choice(DAYS)
    fx_deals.append({"id": "FX-%05d" % (70000 + i), "date": d, "entity": e["id"], "region": e["region"],
                     "pair": "GBP/" + c, "ccy": c, "side": side, "amount": local, "gbp": gbp(c, local),
                     "rate": fx_series[c][DAYS.index(d)], "type": R.choice(["Spot", "Forward", "Forward", "Swap"]),
                     "bank": R.choice(BANKS), "valueDate": (dt.date.fromisoformat(d) + dt.timedelta(days=R.choice([2, 30, 90, 180]))).isoformat(),
                     "status": R.choice(["Confirmed", "Confirmed", "Settled", "Awaiting confirmation"])})

# ---------------- trade finance ----------------
TF_TYPES = ["Import letter of credit", "Export letter of credit", "Bank guarantee", "Standby letter of credit", "Documentary collection"]
TF_STATUS = ["Issued", "Documents presented", "Amendment requested", "Settled", "Draft"]
trade = []
for i in range(1, 49):
    e = R.choice(ENTITIES)
    ccy = R.choice(["USD", "USD", "EUR", e["ccy"]])
    local = round(R.uniform(0.1, 12) * 1e6 / FX[ccy], -3)
    d = R.choice(DAYS)
    trade.append({"id": "TF-%05d" % (21000 + i), "date": d, "entity": e["id"], "region": e["region"],
                  "type": TF_TYPES[i % len(TF_TYPES)], "party": R.choice(COUNTERPARTIES), "ccy": ccy, "amount": local,
                  "gbp": gbp(ccy, local), "expiry": (dt.date.fromisoformat(d) + dt.timedelta(days=R.randint(30, 360))).isoformat(),
                  "status": TF_STATUS[(i * 7) % len(TF_STATUS)], "direction": "Import" if i % 2 else "Export"})

# ---------------- reports ----------------
REPORTS = [("Group cash position", "Liquidity", "Daily"), ("Liquidity forecast, 13 weeks", "Liquidity", "Weekly"),
           ("Facility utilisation", "Funding", "Weekly"), ("Covenant compliance pack", "Funding", "Monthly"),
           ("Counterparty exposure", "Risk", "Daily"), ("Limit utilisation by region", "Risk", "Daily"),
           ("FX exposure and hedge ratio", "Markets", "Daily"), ("FX deal blotter", "Markets", "Daily"),
           ("Payments released", "Payments", "Daily"), ("Approvals audit trail", "Payments", "Weekly"),
           ("Trade finance instruments", "Trade", "Weekly"), ("Guarantee expiry schedule", "Trade", "Monthly"),
           ("Bank fees analysis", "Service", "Monthly"), ("Service request SLA", "Service", "Monthly"),
           ("Board treasury summary", "Board", "Monthly"), ("Intercompany netting", "Liquidity", "Monthly"),
           ("Interest income and expense", "Funding", "Monthly"), ("Sanctions screening summary", "Risk", "Weekly")]
reports = []
for i, (n, c, f) in enumerate(REPORTS, 1):
    d = R.choice(DAYS[-7:]) if f == "Daily" else R.choice(DAYS)
    reports.append({"id": "RPT-%03d" % (100 + i), "date": d, "name": n, "category": c, "frequency": f,
                    "format": R.choice(["CSV", "PDF", "XLSX"]), "owner": R.choice(["Group Treasury", "Risk", "Finance"]),
                    "scheduled": R.random() < .6, "rows": R.randint(40, 4000)})
report_runs = [R.randint(4, 19) for _ in DAYS]

# ---------------- messages + service requests ----------------
MSG = [("Your quarterly relationship review", "Relationship"), ("Updated cut-off times for CNY payments", "Payments"),
       ("Facility renewal: indicative terms attached", "Funding"), ("Sanctions list update affecting two beneficiaries", "Compliance"),
       ("New FX forward pricing tool available", "Markets"), ("Planned maintenance on Sunday 4 October", "Service"),
       ("Trade documents received for TF-21007", "Trade"), ("Annual KYC refresh due for Northwind Gulf FZE", "Compliance"),
       ("Bank holiday calendar for Q4", "Service"), ("Market update: sterling outlook", "Markets"),
       ("Your liquidity sweep has been reconfigured", "Liquidity"), ("Guarantee expiry reminder", "Trade"),
       ("Confirmation of mandate change", "Compliance"), ("Invitation: HSBC treasury forum", "Relationship")]
messages = []
for i, (s, c) in enumerate(MSG, 1):
    d = DAYS[-1 - (i * 2) % 29]
    messages.append({"id": "MSG-%03d" % i, "date": d, "subject": s, "category": c,
                     "from": R.choice(["Sarah Whitfield, Relationship Director", "HSBC Global Payments", "HSBC Markets", "HSBC Client Service"]),
                     "body": "Dear Northwind Group treasury team, this is an illustrative message about: %s. Please reply here if you need anything further." % s.lower(),
                     "read": i > 5})
SR_CATS = ["Payments investigation", "Account maintenance", "Mandate change", "Statement request", "Trade documents", "Digital access"]
SR_STATUS = ["Open", "In progress", "Awaiting you", "Resolved", "Resolved"]
requests = []
for i in range(1, 37):
    d = R.choice(DAYS)
    st = SR_STATUS[i % len(SR_STATUS)]
    requests.append({"id": "SR-%05d" % (88000 + i), "date": d, "category": SR_CATS[i % len(SR_CATS)], "entity": R.choice(ENTITIES)["id"],
                     "subject": R.choice(["Trace payment to supplier", "Add authorised signatory", "Close dormant account",
                                          "Copy of SWIFT confirmation", "Amend LC expiry", "Reset token for user",
                                          "Change daily payment limit", "Statement for audit"]),
                     "priority": R.choice(["High", "Normal", "Normal", "Low"]), "status": st,
                     "hours": round(R.uniform(2, 60), 1), "audit": [{"at": d + "T10:00", "by": "You", "note": "Request raised."}]})
resp_hours = [round(R.uniform(6, 22), 1) for _ in DAYS]

# ---------------- approvers (settings) ----------------
approvers = [{"name": n, "limit": l, "used": round(l * R.uniform(.2, .95), -5)} for n, l in
             [("Chief Executive Officer", 50e6), ("Chief Financial Officer", 40e6), ("Group Treasurer", 25e6),
              ("Deputy Treasurer", 10e6), ("Regional CFO, Asia Pacific", 8e6), ("Regional CFO, Europe", 8e6)]]
logins = [R.randint(1, 9) for _ in DAYS]

DATA = {"meta": {"asOf": AS_OF.isoformat(), "reporting": "GBP", "client": "Northwind Group (illustrative)",
                 "fxNote": "Illustrative FX rates, GBP per one unit of currency, fixed for this prototype. Not live rates.",
                 "policyMinLiquidity": 400e6},
        "fx": FX, "days": DAYS, "regions": REGIONS, "entities": ENTITIES, "accounts": accounts,
        "transactions": transactions, "facilities": facilities, "positions": positions,
        "regionLimits": region_limits, "ccyLimits": ccy_limits, "exposureHist": exposure_hist,
        "exceptions": exceptions, "payments": payments, "fxSeries": fx_series, "gbpusdOhlc": ohlc,
        "fxDeals": fx_deals, "trade": trade, "reports": reports, "reportRuns": report_runs,
        "messages": messages, "requests": requests, "respHours": resp_hours, "approvers": approvers, "logins": logins}
json.dump(DATA, open(sys.argv[1], "w"), separators=(",", ":"))
print("rows:", {k: len(v) for k, v in DATA.items() if isinstance(v, list)})
