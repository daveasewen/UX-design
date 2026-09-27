"""Deterministic placeholder dataset for the CEO prototype. Fictional group, illustrative FX.
Every KPI, chart, grid and list on every page reads from the object this writes."""
import json, random, datetime as dt, math
R = random.Random(20260925)
ASOF = dt.date(2026, 9, 25)
DAYS = [ASOF - dt.timedelta(days=29 - i) for i in range(30)]          # 27 Aug .. 25 Sep
ISO = lambda d: d.isoformat()
r2 = lambda v: round(v, 2)

# GBP value of ONE unit of each currency — illustrative, as at 25 Sep 2026 16:00 London, not live
FX = {"GBP": 1.0, "USD": 0.7446, "EUR": 0.8547, "HKD": 0.09567, "SGD": 0.5781, "AED": 0.2027,
      "CNY": 0.1046, "BRL": 0.1372, "JPY": 0.005031, "INR": 0.008912}
REGIONS = [{"id": "EUR", "name": "Europe"}, {"id": "AME", "name": "Americas"},
           {"id": "APAC", "name": "Asia Pacific"}, {"id": "MEA", "name": "Middle East and Africa"}]
ENT = [
  ("E1", "Meridian Global Holdings plc", "United Kingdom", "GBP", "EUR"),
  ("E2", "Meridian Industrial GmbH", "Germany", "EUR", "EUR"),
  ("E3", "Meridian Americas Inc.", "United States", "USD", "AME"),
  ("E4", "Meridian Brasil Ltda", "Brazil", "BRL", "AME"),
  ("E5", "Meridian Asia Pacific Ltd", "Hong Kong SAR", "HKD", "APAC"),
  ("E6", "Meridian Singapore Pte Ltd", "Singapore", "SGD", "APAC"),
  ("E7", "Meridian China Trading Co", "China", "CNY", "APAC"),
  ("E8", "Meridian Gulf FZE", "United Arab Emirates", "AED", "MEA"),
]
entities = [{"id": i, "name": n, "country": c, "ccy": ccy, "region": rg} for i, n, c, ccy, rg in ENT]
EBY = {e["id"]: e for e in entities}

# ---------------- accounts + 30-day balances ----------------
TYPES = ["Operating", "Collections", "Payroll", "Deposit"]
accounts = []; aid = 0
for e in entities:
    ccys = [e["ccy"]] + (["USD"] if e["ccy"] != "USD" else ["EUR"])
    if e["id"] in ("E1", "E5"): ccys += ["EUR" if e["id"] == "E5" else "JPY"]
    for k, ccy in enumerate(ccys):
        for t in (TYPES if k == 0 else TYPES[:2]):
            aid += 1
            base_gbp = R.uniform(4e6, 60e6) * (2.2 if e["id"] == "E1" else 1) * (0.5 if t == "Payroll" else 1)
            vol = base_gbp * 0.035
            drift = R.uniform(-0.004, 0.006)
            s = []; v = base_gbp * R.uniform(0.9, 1.05)
            for i in range(30):
                v = max(base_gbp * 0.3, v * (1 + drift) + R.gauss(0, vol))
                s.append(v)
            accounts.append({"id": "A%02d" % aid, "entity": e["id"], "ccy": ccy, "type": t,
                "name": "%s %s account" % (ccy, t.lower()),
                "number": "%s •••• %04d" % ({"GBP": "40-11-62", "EUR": "DE89", "USD": "US021", "HKD": "HK004", "SGD": "SG146", "AED": "AE030", "CNY": "CN8801", "BRL": "BR399", "JPY": "JP0005", "INR": "IN0021"}[ccy], R.randint(1000, 9999)),
                "restricted": (e["ccy"] in ("CNY", "BRL") and t == "Deposit"),
                "balGbp": [r2(x) for x in s], "bal": r2(s[-1] / FX[ccy])})

# ---------------- committed facilities ----------------
facilities = [
  {"id": "F1", "entity": "E1", "name": "Syndicated revolving credit facility", "ccy": "GBP", "limit": 900e6, "drawn": 180e6, "maturity": "2029-06-30"},
  {"id": "F2", "entity": "E3", "name": "US commercial paper backstop line", "ccy": "USD", "limit": 400e6, "drawn": 95e6, "maturity": "2028-03-31"},
  {"id": "F3", "entity": "E2", "name": "Euro term loan facility", "ccy": "EUR", "limit": 250e6, "drawn": 250e6, "maturity": "2030-12-15"},
  {"id": "F4", "entity": "E5", "name": "Asia Pacific bilateral facility", "ccy": "HKD", "limit": 1.6e9, "drawn": 420e6, "maturity": "2027-11-30"},
  {"id": "F5", "entity": "E6", "name": "Singapore working-capital line", "ccy": "SGD", "limit": 120e6, "drawn": 38e6, "maturity": "2027-05-31"},
  {"id": "F6", "entity": "E8", "name": "Gulf trade and working-capital line", "ccy": "AED", "limit": 300e6, "drawn": 146e6, "maturity": "2027-09-30"},
  {"id": "F7", "entity": "E4", "name": "Brazil export prepayment facility", "ccy": "BRL", "limit": 350e6, "drawn": 301e6, "maturity": "2027-02-28"},
]
for f in facilities:
    f["limitGbp"] = r2(f["limit"] * FX[f["ccy"]]); f["drawnGbp"] = r2(f["drawn"] * FX[f["ccy"]])
    f["undrawnSeries"] = []
    d = f["drawn"]
    for i in range(30):
        d = min(f["limit"], max(0, d + R.gauss(0, f["limit"] * 0.004)))
        f["undrawnSeries"].append(r2((f["limit"] - d) * FX[f["ccy"]]))
    f["undrawnSeries"][-1] = r2(f["limitGbp"] - f["drawnGbp"])
BUFFER = {"E1": 250e6, "E2": 60e6, "E3": 120e6, "E4": 25e6, "E5": 70e6, "E6": 30e6, "E7": 35e6, "E8": 20e6}

# ---------------- counterparties ----------------
CP_SUPPLIERS = ["Harrowgate Components Ltd", "Norland Steel AG", "Pacific Rim Logistics", "Castellan Chemicals", "Aurora Freight BV",
  "Kestrel Energy plc", "Sable Semiconductors", "Tamarind Packaging Pte", "Veridian Software Inc", "Bellwether Insurance",
  "Qasr Engineering LLC", "Serra Agro Exportadora", "Huaxing Precision Parts", "Lindqvist Maritime AB", "Oakridge Facilities",
  "Marlowe Legal LLP", "Ardent Media Group", "Crescent Utilities", "Northgate Fuel Services", "Stellar Plastics GmbH"]
CP_CUSTOMERS = ["Brightwell Retail Group", "Cobalt Automotive SE", "Evergreen Pharma Inc", "Jadestone Electronics", "Larkspur Hotels",
  "Monarch Rail Systems", "Pinnacle Construction", "Redwood Grocers", "Summit Aerospace", "Tidewater Shipping"]
BANKS = [("Northbridge Bank plc", "EUR", "A+"), ("Lumen Bank AG", "EUR", "A-"), ("Continental Trust NA", "AME", "AA-"),
         ("Pacific Harbour Bank", "APAC", "A"), ("Straits Commercial Bank", "APAC", "AA-"), ("Desert Rose Bank PJSC", "MEA", "A-"),
         ("Banco Meridiano SA", "AME", "BBB"), ("Yangtze Merchant Bank", "APAC", "A-")]

def pick_ccy(e):
    return e["ccy"] if R.random() < 0.62 else R.choice(["USD", "EUR", "GBP"])

# ---------------- transactions (30 days) ----------------
TX_TYPES = [("Customer receipt", 1), ("Supplier payment", -1), ("Payroll", -1), ("Intercompany transfer", 0),
            ("FX conversion", 0), ("Tax payment", -1), ("Interest", 1), ("Bank charges", -1)]
transactions = []
for n in range(1, 241):
    e = R.choice(entities); t, sign = R.choices(TX_TYPES, weights=[26, 34, 8, 10, 8, 4, 5, 5])[0]
    ccy = pick_ccy(e); day = R.choice(DAYS)
    if sign == 0: sign = R.choice([1, -1])
    mag = {"Payroll": R.uniform(2e6, 14e6), "Tax payment": R.uniform(1e6, 9e6), "Interest": R.uniform(2e4, 6e5),
           "Bank charges": R.uniform(500, 25000)}.get(t, math.exp(R.uniform(math.log(8e4), math.log(2.4e7))))
    cp = {"Customer receipt": R.choice(CP_CUSTOMERS), "Supplier payment": R.choice(CP_SUPPLIERS),
          "Payroll": "Staff payroll — %s" % e["country"], "Intercompany transfer": EBY[R.choice([x for x in EBY if x != e["id"]])]["name"],
          "FX conversion": "HSBC Global Markets", "Tax payment": "Tax authority — %s" % e["country"], "Interest": "HSBC interest credit",
          "Bank charges": "HSBC tariff charges"}[t]
    amt_gbp = sign * mag
    transactions.append({"id": 1000 + n, "date": ISO(day), "entity": e["id"], "ccy": ccy, "type": t, "counterparty": cp,
        "ref": "%s-%05d" % ({"Customer receipt": "RCV", "Supplier payment": "SUP", "Payroll": "PAY", "Intercompany transfer": "ICT",
                               "FX conversion": "FXC", "Tax payment": "TAX", "Interest": "INT", "Bank charges": "CHG"}[t], R.randint(10000, 99999)),
        "amount": r2(amt_gbp / FX[ccy]), "gbp": r2(amt_gbp),
        "status": R.choices(["Settled", "Pending"], weights=[88, 12])[0]})
transactions.sort(key=lambda x: (x["date"], x["id"]), reverse=True)

# ---------------- payments awaiting approval ----------------
METHODS = [("SWIFT", ["USD", "EUR", "HKD", "SGD", "AED", "CNY", "BRL", "JPY"]), ("SEPA credit transfer", ["EUR"]),
           ("CHAPS", ["GBP"]), ("Fedwire", ["USD"]), ("Faster Payments", ["GBP"]), ("Local clearing", ["HKD", "SGD", "AED", "BRL", "CNY"])]
payments = []
STAT = ["Awaiting your approval"] * 20 + ["Awaiting second approver"] * 8 + ["Approved"] * 8 + ["Released"] * 8 + ["Rejected"] * 4
R.shuffle(STAT)
for n, st in enumerate(STAT, 1):
    e = R.choice(entities); ccy = pick_ccy(e)
    meth = next((m for m, cs in METHODS if ccy in cs and R.random() < 0.7), "SWIFT")
    big = st == "Awaiting your approval"
    gbp = math.exp(R.uniform(math.log(1.05e6 if big else 2e5), math.log(4.2e7 if big else 9e6)))
    vd = ASOF + dt.timedelta(days=R.randint(0, 9)) if st.startswith("Await") else ASOF - dt.timedelta(days=R.randint(0, 12))
    flags = []
    if R.random() < 0.22: flags.append("New beneficiary")
    if gbp > 1e7: flags.append("Above £10m")
    if R.random() < 0.08: flags.append("Screening match to review")
    payments.append({"id": 5000 + n, "ref": "PAY-%05d" % (24000 + n * 7), "entity": e["id"], "beneficiary": R.choice(CP_SUPPLIERS + [x["name"] for x in entities if x["id"] != e["id"]]),
        "method": meth, "ccy": ccy, "amount": r2(gbp / FX[ccy]), "gbp": r2(gbp), "valueDate": ISO(vd), "status": st,
        "purpose": R.choice(["Supplier invoice run", "Capital expenditure", "Intercompany funding", "Dividend to parent", "Tax settlement", "Loan repayment", "Acquisition deposit"]),
        "initiator": R.choice(["Priya Natarajan (Group Treasury)", "Tom Okafor (AP Operations)", "Lena Hoffmann (Treasury Europe)", "Marcus Chen (Treasury APAC)", "Ana Ribeiro (Finance Americas)"]),
        "flags": flags, "settleHours": r2(R.lognormvariate(math.log({"EUR": 3, "AME": 5, "APAC": 7, "MEA": 9}[e["region"]]), 0.5))})
# daily outflow history for the payments column chart (GBP)
payHistory = [r2(max(8e6, R.gauss(46e6, 14e6) * (0.35 if d.weekday() >= 5 else 1))) for d in DAYS]

# ---------------- cash-flow forecast (next 30 days) ----------------
forecast = []
for n in range(1, 91):
    e = R.choice(entities); t = R.choices(["Customer receipts", "Supplier payments", "Payroll", "Debt service", "Tax", "Dividend", "Capital expenditure"], weights=[30, 30, 8, 6, 5, 2, 6])[0]
    sign = 1 if t == "Customer receipts" else -1
    gbp = sign * math.exp(R.uniform(math.log(3e5), math.log(3.2e7)))
    ccy = pick_ccy(e)
    forecast.append({"id": 8000 + n, "date": ISO(ASOF + dt.timedelta(days=R.randint(1, 30))), "entity": e["id"], "category": t,
        "counterparty": R.choice(CP_CUSTOMERS) if sign > 0 else (R.choice(CP_SUPPLIERS) if t in ("Supplier payments", "Capital expenditure") else {"Payroll": "Staff payroll", "Debt service": "Facility agent", "Tax": "Tax authority", "Dividend": "Shareholders"}[t]),
        "ref": "FCT-%04d" % (3000 + n), "ccy": ccy, "amount": r2(gbp / FX[ccy]), "gbp": r2(gbp),
        "certainty": R.choice(["Committed", "Committed", "Forecast"])})
forecast.sort(key=lambda x: x["date"])
netFlowHistory = [r2(R.gauss(4e6, 28e6)) for _ in DAYS]

# ---------------- FX ----------------
PAIRS = [("GBP/USD", 1 / FX["USD"]), ("EUR/GBP", FX["EUR"]), ("GBP/HKD", 1 / FX["HKD"]), ("GBP/SGD", 1 / FX["SGD"]), ("GBP/CNY", 1 / FX["CNY"]), ("GBP/AED", 1 / FX["AED"])]
fxSeries = {}
for p, last in PAIRS:
    v = [last]
    for i in range(29): v.append(v[-1] * (1 + R.gauss(0, 0.0042)))
    fxSeries[p] = [round(x, 5) for x in reversed(v)]
ohlc = {"open": [], "high": [], "low": [], "close": []}
prev = fxSeries["GBP/USD"][0] * (1 + R.gauss(0, 0.002))
for c in fxSeries["GBP/USD"]:
    o = prev; hi = max(o, c) * (1 + abs(R.gauss(0, 0.0018))); lo = min(o, c) * (1 - abs(R.gauss(0, 0.0018)))
    for k, x in (("open", o), ("high", hi), ("low", lo), ("close", c)): ohlc[k].append(round(x, 4))
    prev = c
deals = []
for n in range(1, 43):
    e = R.choice(entities); ccy = R.choice(["USD", "EUR", "HKD", "SGD", "CNY", "AED", "BRL", "JPY"])
    side = R.choice(["Buy", "Sell"]); kind = R.choices(["Spot", "Forward", "Swap"], weights=[4, 5, 2])[0]
    gbp = math.exp(R.uniform(math.log(5e5), math.log(6e7)))
    deals.append({"id": 7000 + n, "ref": "FX-%06d" % (410000 + n * 13), "entity": e["id"], "trade": ISO(R.choice(DAYS)),
        "value": ISO(ASOF + dt.timedelta(days=R.randint(1, 180))) if kind != "Spot" else ISO(ASOF + dt.timedelta(days=2)),
        "kind": kind, "side": side, "ccy": ccy, "pair": "GBP/%s" % ccy, "notional": r2(gbp / FX[ccy]), "gbp": r2(gbp * (1 if side == "Buy" else -1)),
        "rate": round(1 / FX[ccy] * (1 + R.gauss(0, 0.01)), 4), "counterparty": "HSBC Global Markets"})
deals.sort(key=lambda x: x["trade"], reverse=True)
natural = {c: {"receivables": r2(R.uniform(20e6, 160e6)), "payables": r2(R.uniform(20e6, 160e6))} for c in ["USD", "EUR", "HKD", "CNY", "SGD", "AED"]}
hedgeRatio = {"USD": 78, "EUR": 64, "HKD": 71, "CNY": 52, "SGD": 80, "AED": 69}

# ---------------- risk: positions, limits, exceptions ----------------
positions = []
PK = ["Deposit", "Money-market fund", "FX forward (net MTM)", "Trade receivable", "Short-term investment"]
for n in range(1, 73):
    e = R.choice(entities); ccy = pick_ccy(e); kind = R.choices(PK, weights=[30, 10, 18, 30, 12])[0]
    bank = R.choice([b for b in BANKS if b[1] == e["region"]] or BANKS)
    gbp = math.exp(R.uniform(math.log(1e6), math.log(9e7)))
    cp = bank[0] if kind in ("Deposit", "Money-market fund", "FX forward (net MTM)", "Short-term investment") else R.choice(CP_CUSTOMERS)
    positions.append({"id": 9000 + n, "ref": "POS-%05d" % (51000 + n * 11), "entity": e["id"], "region": e["region"], "ccy": ccy,
        "kind": kind, "counterparty": cp, "maturity": ISO(ASOF + dt.timedelta(days=R.randint(1, 360))), "gbp": r2(gbp), "amount": r2(gbp / FX[ccy])})
limits = []
for b, rg, rating in BANKS:
    lim = {"A+": 420e6, "AA-": 520e6, "A": 380e6, "A-": 300e6, "BBB": 120e6}[rating]
    used = sum(p["gbp"] for p in positions if p["counterparty"] == b)
    limits.append({"id": "L-%s" % b.split()[0].upper(), "kind": "Counterparty", "name": b, "region": rg, "rating": rating, "limit": lim, "used": r2(used)})
for rg in REGIONS:
    used = sum(p["gbp"] for p in positions if p["region"] == rg["id"])
    limits.append({"id": "L-CTRY-%s" % rg["id"], "kind": "Region", "name": rg["name"] + " exposure", "region": rg["id"], "rating": "", "limit": r2(max(used * R.uniform(1.02, 1.6), 5e8)), "used": r2(used)})
# force a breach and a near-breach so the exceptions are true to the data
lb = next(l for l in limits if l["name"] == "Lumen Bank AG"); lb["limit"] = r2(lb["used"] / 1.08)
bm = next(l for l in limits if l["name"] == "Banco Meridiano SA"); bm["limit"] = r2(max(bm["used"], 1e6) / 0.96)
for l in limits:   # every other limit sits inside policy, so the only breaches are the ones the exceptions name
    if l is not lb and l is not bm and l["used"] > 0.9 * l["limit"]:
        l["limit"] = r2(max(l["used"] / 0.84, 1e6))
exceptions = [
  {"id": "EX-301", "severity": "High", "title": "Counterparty limit breached — Lumen Bank AG", "limit": lb["id"], "region": "EUR", "entity": "E2", "raised": "2026-09-24T08:12", "owner": "Group Treasury risk", "detail": "Deposits and forward MTM with Lumen Bank AG stand at 108% of the approved counterparty limit after a large collections sweep. Policy requires CEO acknowledgement and a remediation plan within 2 business days."},
  {"id": "EX-302", "severity": "High", "title": "Payment screening match awaiting decision", "limit": None, "region": "MEA", "entity": "E8", "raised": "2026-09-25T10:40", "owner": "Financial crime compliance", "detail": "A pending SWIFT payment matched a name on a screening list at 82% similarity. The payment is held; compliance has cleared the false-positive assessment but a senior sign-off is required before release."},
  {"id": "EX-303", "severity": "Medium", "title": "Country limit at 96% — Brazil", "limit": bm["id"], "region": "AME", "entity": "E4", "raised": "2026-09-23T15:05", "owner": "Group Treasury risk", "detail": "Exposure to Banco Meridiano SA is at 96% of its limit. No breach yet; further BRL collections this week would breach."},
  {"id": "EX-304", "severity": "Medium", "title": "EUR hedge ratio below policy floor", "limit": None, "region": "EUR", "entity": "E2", "raised": "2026-09-22T09:30", "owner": "FX risk", "detail": "EUR forecast exposure is 64% hedged against a 70% policy floor for the next two quarters."},
  {"id": "EX-305", "severity": "High", "title": "Trapped cash in China above threshold", "limit": None, "region": "APAC", "entity": "E7", "raised": "2026-09-21T11:18", "owner": "Group Treasury", "detail": "Restricted CNY balances exceed the £40m trapped-cash threshold. Repatriation options require board-level approval."},
  {"id": "EX-306", "severity": "Medium", "title": "Facility near fully drawn — Brazil export prepayment", "limit": None, "region": "AME", "entity": "E4", "raised": "2026-09-20T14:02", "owner": "Group Treasury", "detail": "The Brazil export prepayment facility is 86% drawn with a maturity in February 2027. Refinancing discussions should start this quarter."},
  {"id": "EX-307", "severity": "Low", "title": "Signatory list review overdue — Meridian Gulf FZE", "limit": None, "region": "MEA", "entity": "E8", "raised": "2026-09-18T09:00", "owner": "Company secretariat", "detail": "The annual authorised-signatory review is 18 days overdue for Meridian Gulf FZE."},
]
for x in exceptions:
    x["status"] = "Open"; x["audit"] = [{"at": x["raised"], "who": x["owner"], "what": "Exception raised"}]

# ---------------- trade finance ----------------
instruments = []
IT = [("Import letter of credit", "ILC"), ("Export letter of credit", "ELC"), ("Standby letter of credit", "SBLC"), ("Bank guarantee", "BG"), ("Documentary collection", "DC")]
for n in range(1, 39):
    e = R.choice(entities); kind, pre = R.choices(IT, weights=[10, 8, 4, 6, 5])[0]; ccy = pick_ccy(e)
    gbp = math.exp(R.uniform(math.log(2e5), math.log(2.8e7)))
    exp = ASOF + dt.timedelta(days=R.randint(-5, 300))
    st = "Expired" if exp < ASOF else R.choices(["Issued", "Amendment pending", "Documents presented", "Discrepancies noted", "Awaiting acceptance"], weights=[12, 3, 4, 2, 3])[0]
    instruments.append({"id": 6000 + n, "ref": "%s-%06d" % (pre, 120000 + n * 37), "entity": e["id"], "kind": kind,
        "counterparty": R.choice(CP_SUPPLIERS + CP_CUSTOMERS), "ccy": ccy, "amount": r2(gbp / FX[ccy]), "gbp": r2(gbp),
        "issued": ISO(ASOF - dt.timedelta(days=R.randint(10, 200))), "expiry": ISO(exp), "status": st})

# ---------------- messages + service requests ----------------
messages = [
  ("Your relationship team", "Relationship", "Quarterly review — agenda and liquidity outlook", "Ahead of our quarterly review on 8 October we have attached the agenda. We would like to cover the refinancing window for the Brazil facility and your APAC cash-pooling structure."),
  ("HSBC Global Payments Solutions", "Service update", "Faster cut-off times for EUR payments from 1 October", "From 1 October the same-day cut-off for SEPA credit transfers moves to 16:30 CET. No action is needed."),
  ("Financial crime compliance", "Compliance request", "Know-your-customer refresh — Meridian Gulf FZE", "Please provide updated ultimate beneficial ownership documents for Meridian Gulf FZE by 15 October to avoid service restrictions."),
  ("HSBC Global Research", "Market insight", "Sterling outlook: rates on hold into year end", "Our economists expect the Bank of England to hold rates at its November meeting. Sterling volatility has eased this month."),
  ("Your relationship team", "Relationship", "Term sheet — revolving credit facility extension", "Please find an indicative term sheet for a one-year extension of the syndicated revolving credit facility."),
  ("HSBC Trade Services", "Service update", "Documents received — ELC-120185", "Documents under export letter of credit ELC-120185 have been received and are being checked."),
  ("Service desk", "Service update", "Planned maintenance — Sunday 5 October", "Online banking will be unavailable from 01:00 to 03:00 UK time for planned maintenance."),
  ("HSBC Global Markets", "Market insight", "USD liquidity: month-end funding conditions", "Month-end funding conditions in USD are expected to tighten slightly; consider pre-funding Fedwire payments."),
  ("Financial crime compliance", "Compliance request", "Screening match — PAY-24651 requires senior sign-off", "A payment from Meridian Gulf FZE is held pending senior sign-off following a screening match assessed as a false positive."),
  ("Your relationship team", "Relationship", "Invitation — HSBC treasury leaders forum", "You are invited to the treasury leaders forum in London on 22 October."),
  ("HSBC Liquidity Management", "Service update", "APAC notional pool — interest optimisation report", "Your September interest optimisation report for the APAC notional pool is ready to download."),
  ("HSBC Global Research", "Market insight", "China onshore liquidity and repatriation routes", "A summary of current routes for repatriating onshore CNY, including cross-border sweeping."),
  ("Service desk", "Service update", "New user entitlement approved", "The entitlement request for Lena Hoffmann (payments approver, Europe) has been approved."),
  ("HSBC Trade Services", "Compliance request", "Discrepancy notice — ILC-120296", "Documents presented under ILC-120296 show a discrepancy in the bill of lading date. Please advise whether to waive."),
  ("Your relationship team", "Relationship", "Follow-up: supply-chain finance programme sizing", "Following our call, we have sized a supply-chain finance programme for your top 40 suppliers."),
  ("HSBC Global Payments Solutions", "Service update", "Payment returned — beneficiary account closed", "Payment PAY-24098 was returned because the beneficiary account is closed. Funds have been credited back."),
]
msgs = []
for n, (frm, cat, subj, body) in enumerate(messages, 1):
    msgs.append({"id": "M-%03d" % n, "from": frm, "category": cat, "subject": subj, "body": body,
                 "date": ISO(ASOF - dt.timedelta(days=(n * 2) // 3)), "unread": n % 3 != 0, "thread": []})
SRC = ["Payment investigation", "Account maintenance", "Facility request", "Trade documents", "User entitlements", "Statement request"]
requests = []
for n in range(1, 15):
    st = R.choices(["Submitted", "In progress", "Awaiting your input", "Resolved"], weights=[2, 4, 2, 6])[0]
    op = ASOF - dt.timedelta(days=R.randint(0, 34))
    requests.append({"id": "SR-%05d" % (40200 + n * 17), "category": R.choice(SRC), "entity": R.choice(entities)["id"],
        "subject": R.choice(["Trace SWIFT payment to supplier", "Close dormant EUR collections account", "Increase APAC facility headroom",
                              "Amend LC expiry date", "Add payments approver", "Duplicate statement for audit", "Recall a duplicated payment",
                              "Update authorised signatories", "Open USD sub-account", "Query tariff charges"]),
        "opened": ISO(op), "status": st, "priority": R.choice(["Normal", "Normal", "High"]),
        "resolvedHours": r2(R.uniform(4, 120)) if st == "Resolved" else None})

reports = [
  {"id": "RPT-01", "name": "Daily cash position", "family": "Liquidity", "frequency": "Daily", "source": "accounts"},
  {"id": "RPT-02", "name": "30-day liquidity forecast", "family": "Liquidity", "frequency": "Daily", "source": "forecast"},
  {"id": "RPT-03", "name": "Committed facilities utilisation", "family": "Funding", "frequency": "Weekly", "source": "facilities"},
  {"id": "RPT-04", "name": "Transaction ledger", "family": "Accounts", "frequency": "Daily", "source": "transactions"},
  {"id": "RPT-05", "name": "Payments approval audit", "family": "Payments", "frequency": "Daily", "source": "payments"},
  {"id": "RPT-06", "name": "FX deal blotter", "family": "FX", "frequency": "Daily", "source": "deals"},
  {"id": "RPT-07", "name": "Counterparty and region limits", "family": "Risk", "frequency": "Daily", "source": "limits"},
  {"id": "RPT-08", "name": "Risk exceptions audit trail", "family": "Risk", "frequency": "On demand", "source": "exceptions"},
  {"id": "RPT-09", "name": "Positions by counterparty", "family": "Risk", "frequency": "Weekly", "source": "positions"},
  {"id": "RPT-10", "name": "Trade finance maturity ladder", "family": "Trade", "frequency": "Weekly", "source": "instruments"},
  {"id": "RPT-11", "name": "Service request log", "family": "Service", "frequency": "Monthly", "source": "requests"},
  {"id": "RPT-12", "name": "Cash-flow forecast items", "family": "Liquidity", "frequency": "Daily", "source": "forecast"},
]
for rp in reports:
    rp["last"] = ISO(ASOF - dt.timedelta(days=R.choice([0, 0, 1, 2, 6])))
reportRuns = [R.randint(6, 30) if d.weekday() < 5 else R.randint(0, 5) for d in DAYS]

DATA = {"asOf": ISO(ASOF), "asOfLabel": "25 Sep 2026, 16:00 London", "days": [ISO(d) for d in DAYS], "fx": FX,
  "fxNote": "Illustrative rates for GBP reporting, as at 25 Sep 2026 16:00 London. Not live, not tradeable.",
  "regions": REGIONS, "entities": entities, "accounts": accounts, "facilities": facilities, "buffers": BUFFER,
  "transactions": transactions, "payments": payments, "payHistory": payHistory, "forecast": forecast, "netFlowHistory": netFlowHistory,
  "fxSeries": fxSeries, "ohlc": ohlc, "deals": deals, "natural": natural, "hedgeRatio": hedgeRatio,
  "positions": positions, "limits": limits, "exceptions": exceptions, "instruments": instruments,
  "messages": msgs, "requests": requests, "reports": reports, "reportRuns": reportRuns,
  "approvalThreshold": 1000000, "noteThreshold": 10000000}
if __name__ == "__main__":
    s = json.dumps(DATA, separators=(",", ":"))
    print(len(s), len(transactions), len(payments), len(positions), len(accounts))
