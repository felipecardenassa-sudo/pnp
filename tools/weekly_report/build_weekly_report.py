"""Weekly paid performance report for Plug and Play: platform exports + this week's inputs -> branded PDF,
facts.json (every number, for checking and for drafting) and summary.md (text for Slack or email).

Usage (from the repo root):
  python3 -I tools/weekly_report/build_weekly_report.py --week 2026-10-12 \
      --meta META_EXPORT.csv --google GOOGLE_EXPORT.csv \
      --inputs reports/weekly/2026-10-12/inputs.toml --out reports/weekly/2026-10-12 --pdf

--week     Monday of the report week (weeks run Monday to Sunday, as in the tracker).
--meta     Meta Ads Manager export, campaign x day (the same file as the tracker's weekly update).
--google   Google Ads report, campaign x day (the same file as the tracker's weekly update).
--inputs   This week's typed inputs: HubSpot MQLs, notes, actions (see reports/weekly/sample-2026-10-05/).
--other    ChatGPT / LinkedIn rows (default reports/weekly/other_channels.csv), like the tracker's Other channels tab.
--config   Budget, exchange rates, labels and thresholds (default tools/weekly_report/config.toml).
--pdf      Also print the PDF with Chromium.

Text in the inputs can use {{key}} placeholders (for example {{meta.cpl}}); they are filled from the computed
numbers, so the words and the tables always agree. facts.json lists every key under "fmt".

Content to cover each week: .claude/skills/weekly-paid-report/report_spec.md (all of Tereza's report, made clearer).
"""
import argparse, collections, csv, datetime as dt, html, json, os, re, subprocess, sys, tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "spend_tracker"))
import load_exports  # noqa: E402  (reads exports exactly as Google Sheets imports them)

CHROMIUM = "/opt/pw-browsers/chromium"
E = html.escape
MINUS = "−"

# channel key, label, counts as lead generation
CHANNELS = [
    ("meta", "Meta", True),
    ("google_search", "Google Search", True),
    ("pmax", "Google Performance Max", True),
    ("chatgpt", "ChatGPT Ads", True),
    ("linkedin", "LinkedIn Ads", True),
    ("youtube", "YouTube (brand views)", False),
    ("meta_other", "Meta traffic campaigns", False),
]
CH_LABEL = {k: l for k, l, _ in CHANNELS}
LEAD_GEN = [k for k, _, g in CHANNELS if g]
NON_LEAD = [k for k, _, g in CHANNELS if not g]
NON_CONVERSION = ("link_click", "landing_page_view", "video_view", "thruplay", "reach", "post_engagement", "impressions",
                  "page_like", "profile_visit")


class ReportError(Exception):
    pass


# ----------------------------------------------------------------------------------------------- reading
def col(header, *names, prefix=None, required=True, what="export"):
    for n in names:
        if n in header:
            return header.index(n)
    if prefix:
        for i, h in enumerate(header):
            if isinstance(h, str) and h.startswith(prefix):
                return i
    if required:
        raise ReportError(f"{what}: column {names[0]!r} not found. Columns: {header}")
    return None


def fx_rate(cfg, d):
    rates = cfg["budget"]["eur_to_usd"]
    if d.year == cfg["budget"]["year"]:
        return rates[d.month - 1]
    return sum(rates) / len(rates)


def to_usd(cfg, amount, currency, d):
    if currency in (None, "", "USD"):
        return amount
    if currency == "EUR":
        return amount * fx_rate(cfg, d)
    raise ReportError(f"Currency {currency!r} is not set up (only USD and EUR).")


def read_meta(path, cfg):
    rows = load_exports.read(path)
    h = rows[0]
    c_date = col(h, "Reporting starts", "Day", what="Meta export")
    c_name = col(h, "Campaign name", what="Meta export")
    c_spend = col(h, "Amount spent (USD)", prefix="Amount spent", what="Meta export")
    cur = re.search(r"\((\w{3})\)", h[c_spend])
    currency = cur.group(1) if cur else "USD"
    c_res = col(h, "Results", what="Meta export")
    c_ind = col(h, "Result indicator", what="Meta export")
    c_imp = col(h, "Impressions", what="Meta export")
    c_clk = col(h, "Unique link clicks", "Link clicks", what="Meta export")
    raw, inds = [], collections.defaultdict(collections.Counter)
    for r in rows[1:]:
        r = list(r) + [None] * (len(h) - len(r))
        d, name = r[c_date], r[c_name]
        if not isinstance(d, dt.date) or not name:
            continue
        ind = r[c_ind] if isinstance(r[c_ind], str) else ""
        if ind:
            inds[name][ind] += 1
        raw.append((d, name, r[c_spend] or 0, r[c_res] or 0, ind, r[c_imp] or 0, r[c_clk] or 0))
    not_lead = set(cfg.get("meta", {}).get("not_lead", []))

    def is_conversion(ind):
        return bool(ind) and not any(x in ind for x in NON_CONVERSION)

    lead_campaign = {}
    for name in {x[1] for x in raw}:
        if name in not_lead:
            lead_campaign[name] = False
        elif inds[name]:
            lead_campaign[name] = is_conversion(inds[name].most_common(1)[0][0])
        else:
            lead_campaign[name] = bool(re.search(r"Objective:(lead|welcome|conversion)", name))
    recs = []
    for d, name, spend, res, ind, imp, clk in raw:
        lead = lead_campaign[name]
        leads = res if lead and (not ind or is_conversion(ind)) else 0
        recs.append(dict(date=d, channel="meta" if lead else "meta_other", campaign=name, spend_native=spend,
                         currency=currency, spend_usd=to_usd(cfg, spend, currency, d), leads=leads, clicks=clk,
                         impr=imp, weekly=True))
    return recs


def google_channel(name, ctype):
    if ctype:
        t = ctype.lower()
        if "performance max" in t:
            return "pmax"
        if "search" in t:
            return "google_search"
        return "youtube" if ("video" in t or "demand" in t or "display" in t) else "google_search"
    if re.search(r"youtube|video|demandgen|(^|[^a-z])yt([^a-z]|$)", name, re.I):
        return "youtube"
    if re.search(r"pmax", name, re.I):
        return "pmax"
    return "google_search"


def read_google(path, cfg):
    rows = load_exports.read(path)
    hi = next((i for i, r in enumerate(rows[:20]) if "Campaign" in r and ("Day" in r or "Date" in r)), None)
    if hi is None:
        raise ReportError("Google export: no header row with 'Campaign' and 'Day' in the first 20 lines.")
    h = rows[hi]
    c_name, c_date = col(h, "Campaign", what="Google export"), col(h, "Day", "Date", what="Google export")
    c_cost, c_conv = col(h, "Cost", what="Google export"), col(h, "Conversions", what="Google export")
    c_clk, c_imp = col(h, "Clicks", what="Google export"), col(h, "Impr.", "Impressions", what="Google export")
    c_cur = col(h, "Currency code", required=False)
    c_type = col(h, "Campaign type", required=False)
    recs = []
    for r in rows[hi + 1:]:
        r = list(r) + [None] * (len(h) - len(r))
        d, name = r[c_date], r[c_name]
        if not isinstance(d, dt.date) or not name:
            continue
        cur = (r[c_cur] if c_cur is not None else None) or "EUR"
        ch = google_channel(name, r[c_type] if c_type is not None else None)
        cost = r[c_cost] or 0
        recs.append(dict(date=d, channel=ch, campaign=name, spend_native=cost, currency=cur,
                         spend_usd=to_usd(cfg, cost, cur, d), leads=(r[c_conv] or 0) if ch != "youtube" else 0,
                         clicks=r[c_clk] or 0, impr=r[c_imp] or 0, weekly=True))
    return recs


def read_other(path, cfg):
    if not path or not os.path.exists(path):
        return []
    recs = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if not (r.get("Date") or "").strip():
                continue
            d = dt.date.fromisoformat(r["Date"].strip())
            ch = {"chatgpt ads": "chatgpt", "linkedin ads": "linkedin"}.get(r["Channel"].strip().lower())
            if not ch:
                raise ReportError(f"other_channels.csv: unknown channel {r['Channel']!r} (use ChatGPT Ads or LinkedIn Ads).")
            num = lambda k: float((r.get(k) or "0").replace(",", "") or 0)
            cur = (r.get("Currency") or "").strip() or ("EUR" if ch == "chatgpt" else "USD")
            spend = num("Spend (as billed)")
            recs.append(dict(date=d, channel=ch, campaign=r["Campaign name"].strip(), spend_native=spend, currency=cur,
                             spend_usd=to_usd(cfg, spend, cur, d), leads=num("Conversions"), clicks=num("Clicks"),
                             impr=num("Impressions"),
                             weekly=(r.get("Total for more than a week?") or "").strip().lower() not in ("yes", "y")))
    return recs


# ----------------------------------------------------------------------------------------------- labels
def campaign_label(name, cfg):
    if name in cfg.get("campaign_labels", {}):
        return cfg["campaign_labels"][name]
    m = re.match(r"Geo:([^_]+)_", name)
    if not m:
        return name
    code = m.group(1)
    market = cfg.get("markets", {}).get(code, code.replace("-", " "))
    t = re.search(r"Type:([^_]+)", name)
    o = re.search(r"Objective:([^_]+)", name)
    kind = cfg.get("types", {}).get(t.group(1), t.group(1).replace("-", " ")) if t else (o.group(1) if o else "")
    if "Network:pmax" in name:
        kind = "Performance Max"
    if "YouTube" in name and "views" in name:
        kind = "YouTube views"
    return f"{market} · {kind}" if kind else market


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ----------------------------------------------------------------------------------------------- numbers
def monday(d):
    return d - dt.timedelta(days=d.weekday())


def metrics(c, weeks=1):
    spend, leads, clicks, impr = c["spend_usd"], c["leads"], c["clicks"], c["impr"]
    return dict(spend=spend / weeks, leads=leads / weeks, clicks=clicks / weeks, impr=impr / weeks,
                spend_native=c["spend_native"] / weeks,
                cpl=spend / leads if leads else None, cpc=spend / clicks if clicks else None,
                ctr=clicks / impr if impr else None,
                cpl_native=c["spend_native"] / leads if leads else None)


def change(cur, base):
    if cur is None or base in (None, 0):
        return None
    return (cur - base) / base


def add(counter, rec):
    for k in ("spend_usd", "spend_native", "leads", "clicks", "impr"):
        counter[k] += rec[k]


# ----------------------------------------------------------------------------------------------- formatting
def money(x, d=0, sym="$"):
    if x is None:
        return "–"
    s = f"{abs(x):,.{d}f}"
    return f"{MINUS if x < 0 else ''}{sym}{s}"


def money_k(x):
    if x is None:
        return "–"
    v = round(abs(x) / 1000, 1)
    s = f"{v:,.0f}" if v == int(v) else f"{v:,.1f}"
    return f"{MINUS if x < 0 else ''}${s}k"


def num(x, d=0):
    if x is None:
        return "–"
    if d == 0:
        return f"{round(x):,}"
    s = f"{x:,.{d}f}"
    return s[:-2] if s.endswith(".0") and d == 1 else s


def signed_pct(x, d=0):
    if x is None:
        return "–"
    v = round(x * 100, d)
    if v == 0:
        return "0%"
    return f"{'+' if v > 0 else MINUS}{abs(v):.{d}f}%"


def pct(x, d=0):
    return "–" if x is None else f"{x * 100:.{d}f}%"


def crm_count(n, cfg):
    if n is None or n < 0:
        return "n/a"
    lo = cfg["thresholds"]["crm_min_count"]
    return f"<{lo}" if 0 < n < lo else f"{n:,}"


ARROW_UP = '<svg class="ar" viewBox="0 0 8 7" aria-hidden="true"><path d="M4 0 8 7H0z" fill="currentColor"/></svg>'
ARROW_DOWN = '<svg class="ar" viewBox="0 0 8 7" aria-hidden="true"><path d="M0 0h8L4 7z" fill="currentColor"/></svg>'
ARROW_FLAT = '<svg class="ar" viewBox="0 0 8 7" aria-hidden="true"><rect x="0" y="2.5" width="8" height="2" fill="currentColor"/></svg>'


def delta_html(ch, lower_is_better=False, neutral=False, low_volume=False, small=True):
    """Arrow + % change. Colour follows whether the move is good; grey when neutral or low volume.
    Arrows are drawn as shapes (the brand font has no arrow glyphs), so the PDF embeds the brand font only."""
    if ch is None:
        return ""
    v = round(ch * 100)
    if v == 0:
        arrow, cls, txt = ARROW_FLAT, "flat", "0%"
    else:
        arrow = ARROW_UP if v > 0 else ARROW_DOWN
        good = (v < 0) if lower_is_better else (v > 0)
        cls = "flat" if neutral or low_volume else ("good" if good else "bad")
        txt = f"{abs(v)}%"
    return f'<span class="dl {cls}{" lv" if low_volume else ""}{" sm" if small else ""}">{arrow}{txt}</span>'


def date_label(a, b):
    if a.month == b.month:
        return f"{a.day}–{b.day} {b:%b %Y}"
    return f"{a.day} {a:%b} – {b.day} {b:%b %Y}"


def short_range(a, b):
    if a.month == b.month:
        return f"{a.day}–{b.day} {b:%b}"
    return f"{a.day} {a:%b} – {b.day} {b:%b}"


# ----------------------------------------------------------------------------------------------- build
def build(args):
    cfg = tomllib.load(open(args.config, "rb"))
    inp = tomllib.load(open(args.inputs, "rb")) if args.inputs and os.path.exists(args.inputs) else {}
    if args.inputs and "last_actions" not in inp:
        prev_monday = dt.date.fromisoformat(args.week) - dt.timedelta(days=7)
        prev_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(args.inputs))), prev_monday.isoformat(), "inputs.toml")
        if os.path.exists(prev_file):
            prev = tomllib.load(open(prev_file, "rb"))
            inp["last_actions"] = [dict(action=a["action"], status="no update", note=f"({a.get('owner', '')}, {a.get('due', '')})")
                                   for a in prev.get("actions", [])]
    th = cfg["thresholds"]
    W = dt.date.fromisoformat(args.week)
    if W.weekday() != 0:
        raise ReportError(f"--week must be a Monday; {W} is a {W:%A}.")
    W_end = W + dt.timedelta(days=6)
    P = W - dt.timedelta(days=7)
    AVG = [W - dt.timedelta(days=7 * k) for k in (4, 3, 2, 1)]
    SERIES = [W - dt.timedelta(days=7 * k) for k in range(7, -1, -1)]

    meta = read_meta(args.meta, cfg)
    goog = read_google(args.google, cfg)
    other = read_other(args.other, cfg)
    last_meta, last_goog = max(r["date"] for r in meta), max(r["date"] for r in goog)
    data_date = min(last_meta, last_goog)
    if data_date < W_end:
        raise ReportError(f"The exports end on {data_date:%a %d %b}; the report week ends on {W_end:%a %d %b}. "
                          "Export again up to yesterday.")
    recs = meta + goog + other

    # weekly aggregates by channel and by campaign (rows marked as multi-week totals stay out, as in the tracker)
    by_ch = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    by_c = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for r in recs:
        if not r["weekly"] or r["date"] > data_date:
            continue
        w = monday(r["date"])
        add(by_ch[r["channel"]][w], r)
        add(by_c[(r["channel"], r["campaign"])][w], r)

    def window(counters, weeks):
        c = collections.Counter()
        for w in weeks:
            c.update(counters[w])
        return c

    def block(counters):
        return dict(cur=metrics(counters[W]), prev=metrics(counters[P]), avg=metrics(window(counters, AVG), 4),
                    series=[metrics(counters[w]) for w in SERIES])

    channels = {}
    for k, label, lead_gen in CHANNELS:
        b = block(by_ch[k])
        b.update(label=label, lead_gen=lead_gen,
                 active=any(by_ch[k][w]["spend_usd"] > 0 for w in [P, W] + AVG),
                 currency=next((r["currency"] for r in recs if r["channel"] == k), "USD"))
        channels[k] = b

    def combine(keys):
        out = collections.defaultdict(collections.Counter)
        for k in keys:
            for w, c in by_ch[k].items():
                out[w].update(c)
        return out

    leadgen, nonlead, total = block(combine(LEAD_GEN)), block(combine(NON_LEAD)), block(combine(LEAD_GEN + NON_LEAD))
    last_spend = {}
    for r in recs:
        if r["weekly"] and r["spend_usd"] > 0 and r["date"] <= data_date:
            k = r["channel"]
            if k not in last_spend or r["date"] > last_spend[k]:
                last_spend[k] = r["date"]

    # campaign tables
    campaigns = collections.defaultdict(list)
    for (ch, name), counters in by_c.items():
        b = block(counters)
        if not (b["cur"]["spend"] or b["prev"]["spend"]):
            continue
        b.update(name=name, label=campaign_label(name, cfg), channel=ch, ended=name in cfg["budget"]["ended_campaigns"])
        campaigns[ch].append(b)
    for ch in campaigns:
        campaigns[ch].sort(key=lambda b: (-b["cur"]["spend"], -b["prev"]["spend"]))

    groups = {}
    for gname, pattern in cfg.get("groups", {}).items():
        rx = re.compile(pattern)
        g = collections.defaultdict(collections.Counter)
        for (ch, name), counters in by_c.items():
            if rx.search(name):
                for w, c in counters.items():
                    g[w].update(c)
        groups[gname] = block(g)

    # budget, the tracker's way: year to date, pace of the last 3 full weeks without ended campaigns, forecast
    year = cfg["budget"]["year"]
    year_end = dt.date(year, 12, 31)
    ytd = sum(r["spend_usd"] for r in recs if r["date"].year == year and r["date"] <= data_date)
    lfw_end = data_date - dt.timedelta(days=(data_date.weekday() + 1) % 7)
    p_start = lfw_end - dt.timedelta(days=20)
    in_pace = [r for r in recs if r["weekly"] and p_start <= r["date"] <= lfw_end]
    pace_all = sum(r["spend_usd"] for r in in_pace)
    pace_ended = sum(r["spend_usd"] for r in in_pace if r["campaign"] in cfg["budget"]["ended_campaigns"])
    pace = (pace_all - pace_ended) / 3
    days_left = (year_end - data_date).days
    weeks_left = days_left / 7
    budget_usd, max_usd = cfg["budget"]["budget_usd"], cfg["budget"]["maximum_usd"]
    forecast = ytd + pace * weeks_left
    budget = dict(ytd=ytd, budget=budget_usd, maximum=max_usd, pct=ytd / budget_usd, data_date=data_date.isoformat(),
                  pace=pace, pace_window=f"{short_range(p_start, lfw_end)}", forecast=forecast,
                  over=forecast - budget_usd, under_max=max_usd - forecast,
                  allow=(budget_usd - ytd) / weeks_left if weeks_left else None,
                  allow_max=(max_usd - ytd) / weeks_left if weeks_left else None, days_left=days_left,
                  week_spend=total["cur"]["spend"])
    budget["gap"] = budget["pace"] - budget["allow"] if budget["allow"] is not None else None

    crm = build_crm(inp.get("crm"), cfg, W, P, channels, leadgen, by_ch)

    facts = dict(week=dict(start=W.isoformat(), end=W_end.isoformat(), label=date_label(W, W_end),
                           prev_label=short_range(P, P + dt.timedelta(days=6)),
                           avg_label=short_range(AVG[0], AVG[-1] + dt.timedelta(days=6)),
                           series=[w.isoformat() for w in SERIES]),
                 data_date=data_date.isoformat(), exports=dict(meta_last_day=last_meta.isoformat(),
                                                               google_last_day=last_goog.isoformat()),
                 channels=channels, leadgen=leadgen, nonlead=nonlead, total=total, campaigns=campaigns,
                 groups=groups, budget=budget, crm=crm, thresholds=th,
                 last_spend={k: v.isoformat() for k, v in last_spend.items()},
                 fx=dict(eur_to_usd_this_month=fx_rate(cfg, W)))
    facts["flags"] = make_flags(facts, cfg)
    facts["fmt"] = make_fmt(facts, cfg)
    return facts, inp, cfg


def build_crm(c, cfg, W, P, channels, leadgen, by_ch):
    if not c:
        return None
    weeks = [dt.date.fromisoformat(x) for x in c["weeks"]]
    idx = {w: i for i, w in enumerate(weeks)}
    mqls = c.get("mqls", {})
    for src, vals in mqls.items():
        if len(vals) != len(weeks):
            raise ReportError(f"inputs: crm.mqls[{src!r}] has {len(vals)} numbers for {len(weeks)} weeks.")
    paid_map = cfg["crm"]["paid_sources"]

    def tot(i):
        return sum(v[i] for v in mqls.values() if v[i] >= 0)

    def paid(i):
        return sum(v[i] for s, v in mqls.items() if s in paid_map and v[i] >= 0)

    out = dict(note=c.get("note", ""), weeks=[w.isoformat() for w in weeks], sources=list(mqls),
               mqls=mqls, disqualified=c.get("disqualified", {}), extra=c.get("extra", {}), sqls=c.get("sqls", {}),
               paid_sources=[s for s in mqls if s in paid_map])
    for key, w in (("cur", W), ("prev", P)):
        if w not in idx:
            out[key] = None
            continue
        i = idx[w]
        lg_leads = channels_leads(channels, key)
        out[key] = dict(total=tot(i), paid=paid(i), paid_share=paid(i) / tot(i) if tot(i) else None,
                        paid_per100=paid(i) / lg_leads * 100 if lg_leads else None, platform_leads=lg_leads,
                        disqualified=sum(c.get("disqualified", {}).values()) if key == "cur" and c.get("disqualified") else None)
    # cost per paid MQL over the CRM weeks within the last 4 weeks, only when the count is large enough to show
    win = [w for w in weeks if W - dt.timedelta(days=21) <= w <= W]
    spend_paid = 0.0
    paid_chs = sorted(set(paid_map.values()))
    for w in win:
        for ch in paid_chs:
            spend_paid += by_ch[ch][w]["spend_usd"]
    paid_n = sum(paid(idx[w]) for w in win)
    out["window"] = dict(weeks=len(win), start=win[0].isoformat() if win else None, paid=paid_n, spend=spend_paid,
                         cost_per_paid=spend_paid / paid_n if paid_n >= cfg["thresholds"]["crm_min_count"] else None)
    per_src = {}
    for s in out["paid_sources"]:
        ch = paid_map[s]
        n = sum(mqls[s][idx[w]] for w in win if mqls[s][idx[w]] >= 0)
        sp = sum(by_ch[ch][w]["spend_usd"] for w in win)
        leads = sum(by_ch[ch][w]["leads"] for w in win)
        per_src[s] = dict(channel=ch, mqls=n, spend=sp, platform_leads=leads,
                          cost_per_mql=sp / n if n >= cfg["thresholds"]["crm_min_count"] else None,
                          per100=n / leads * 100 if leads and n >= cfg["thresholds"]["crm_min_count"] else None)
    out["per_source"] = per_src
    return out


def channels_leads(channels, key):
    return sum(channels[k][key]["leads"] for k in LEAD_GEN)


# ----------------------------------------------------------------------------------------------- flags
def make_flags(f, cfg):
    th = cfg["thresholds"]
    lim, min_sp, lv = th["change_pct"] / 100, th["min_spend_usd"], th["low_volume_leads"]
    flags = []
    b = f["budget"]
    if b["allow"] is not None:
        if b["pace"] > b["allow"]:
            flags.append(dict(kind="budget", tone="bad",
                              text=f"Pace {money(b['pace'])}/week is {money(b['gap'])} above the {money(b['allow'])}/week that lands on "
                                   f"{money_k(b['budget'])}; forecast {money_k(b['forecast'])} (maximum {money_k(b['maximum'])})."))
        else:
            flags.append(dict(kind="budget", tone="good",
                              text=f"Pace {money(b['pace'])}/week is within the {money(b['allow'])}/week that lands on {money_k(b['budget'])}."))
    for k in LEAD_GEN:
        c = f["channels"][k]
        cur, avg = c["cur"], c["avg"]
        if cur["spend"] >= 150 and cur["leads"] == 0:
            flags.append(dict(kind="tracking", tone="bad", text=f"{c['label']}: {money(cur['spend'])} spent and no leads recorded – check tracking."))
        ch = change(cur["cpl"], avg["cpl"])
        if ch is not None and cur["spend"] >= min_sp and abs(ch) >= lim and min(cur["leads"], avg["leads"]) >= lv:
            flags.append(dict(kind="channel", tone="good" if ch < 0 else "bad",
                              text=f"{c['label']}: cost per lead {money(cur['cpl'], 2)} vs {money(avg['cpl'], 2)} 4-week average ({signed_pct(ch)})."))
    for k in ("meta", "google_search", "pmax"):
        for c in f["campaigns"].get(k, []):
            cur, avg, prev = c["cur"], c["avg"], c["prev"]
            if cur["spend"] >= th["zero_lead_spend_usd"] and cur["leads"] == 0:
                flags.append(dict(kind="campaign", tone="bad", text=f"{c['label']}: {money(cur['spend'])} and no leads this week."))
                continue
            ch = change(cur["cpl"], avg["cpl"])
            if ch is not None and cur["spend"] >= min_sp and abs(ch) >= lim:
                small = min(cur["leads"], avg["leads"]) < 5
                word = "leads" if k == "meta" else "conversions"
                flags.append(dict(kind="campaign", tone="good" if ch < 0 else "bad",
                                  text=f"{c['label']}: {num(cur['leads'], 1)} {word} at {money(cur['cpl'], 2)} vs "
                                       f"{num(avg['leads'], 1)}/week at {money(avg['cpl'], 2)} over 4 weeks ({signed_pct(ch)})"
                                       + (" – low volume" if small else "") + "."))
            if prev["spend"] == 0 and cur["spend"] > 0 and avg["spend"] == 0:
                flags.append(dict(kind="campaign", tone="info", text=f"{c['label']}: new this week ({money(cur['spend'])})."))
            if prev["spend"] > 0 and cur["spend"] == 0:
                flags.append(dict(kind="campaign", tone="info", text=f"{c['label']}: no spend this week ({money(prev['spend'])} last week)."))
    nl = f["nonlead"]["cur"]["spend"]
    if nl:
        flags.append(dict(kind="spend", tone="info", text=f"Spend not aimed at leads: {money(nl)} ({pct(nl / f['total']['cur']['spend'])} of the week)."))
    crm = f["crm"]
    if crm and crm.get("cur") and crm.get("prev"):
        flags.append(dict(kind="crm", tone="bad" if crm["cur"]["paid"] < crm["prev"]["paid"] else "good",
                          text=f"Paid MQLs {crm_count(crm['cur']['paid'], cfg)} vs {crm_count(crm['prev']['paid'], cfg)} last week; "
                               f"{pct(crm['cur']['paid_share'])} of all MQLs ({pct(crm['prev']['paid_share'])} last week)."))
    return flags


# ----------------------------------------------------------------------------------------------- placeholders
def make_fmt(f, cfg):
    out = {"week": f["week"]["label"], "prev_week": f["week"]["prev_label"], "avg_weeks": f["week"]["avg_label"],
           "data_date": dt.date.fromisoformat(f["data_date"]).strftime("%-d %b")}

    def put(prefix, b, currency="USD"):
        for per, tag in (("cur", ""), ("prev", "prev_"), ("avg", "avg_")):
            m = b[per]
            out[f"{prefix}.{tag}spend"] = money(m["spend"])
            out[f"{prefix}.{tag}leads"] = num(m["leads"], 1) if m["leads"] % 1 else num(m["leads"])
            out[f"{prefix}.{tag}cpl"] = money(m["cpl"], 2)
            out[f"{prefix}.{tag}cpc"] = money(m["cpc"], 2)
            out[f"{prefix}.{tag}ctr"] = pct(m["ctr"], 2)
            out[f"{prefix}.{tag}clicks"] = num(m["clicks"])
            if currency == "EUR":
                out[f"{prefix}.{tag}spend_eur"] = money(m["spend_native"], 2, "€")
                out[f"{prefix}.{tag}cpl_eur"] = money(m["cpl_native"], 2, "€")
        for metric in ("spend", "leads", "cpl", "cpc", "clicks"):
            for tag, base in (("prev", b["prev"][metric]), ("avg", b["avg"][metric])):
                ch = change(b["cur"][metric], base)
                out[f"{prefix}.{metric}_vs_{tag}"] = signed_pct(ch)
                out[f"{prefix}.{metric}_vs_{tag}_abs"] = "–" if ch is None else f"{abs(round(ch * 100)):.0f}%"

    for k, c in f["channels"].items():
        put(k, c, c["currency"])
    put("leadgen", f["leadgen"])
    put("nonlead", f["nonlead"])
    put("total", f["total"])
    for ch, lst in f["campaigns"].items():
        for c in lst:
            put(f"camp.{slug(c['label'])}", c, "EUR" if ch in ("google_search", "pmax", "youtube") else "USD")
    for g, b in f["groups"].items():
        put(f"group.{g}", b)
    b = f["budget"]
    out.update({"budget.ytd": money(b["ytd"]), "budget.ytd_k": money_k(b["ytd"]), "budget.pct": pct(b["pct"]),
                "budget.forecast": money(b["forecast"]), "budget.forecast_k": money_k(b["forecast"]),
                "budget.over": money(abs(b["over"])), "budget.over_k": money_k(abs(b["over"])),
                "budget.under_max_k": money_k(b["under_max"]), "budget.allow": money(b["allow"]),
                "budget.allow_max": money(b["allow_max"]), "budget.pace": money(b["pace"]),
                "budget.gap": money(abs(b["gap"])) if b["gap"] is not None else "–", "budget.budget_k": money_k(b["budget"]),
                "budget.max_k": money_k(b["maximum"]), "budget.data_date": dt.date.fromisoformat(b["data_date"]).strftime("%-d %b"),
                "budget.week_spend": money(b["week_spend"])})
    crm = f["crm"]
    if crm:
        for key, tag in (("cur", ""), ("prev", "prev_")):
            m = crm.get(key)
            if not m:
                continue
            out[f"crm.{tag}total"] = crm_count(m["total"], cfg)
            out[f"crm.{tag}paid"] = crm_count(m["paid"], cfg)
            out[f"crm.{tag}paid_share"] = pct(m["paid_share"])
            out[f"crm.{tag}paid_per100"] = num(m["paid_per100"], 1)
            out[f"crm.{tag}platform_leads"] = num(m["platform_leads"])
        if crm["cur"] and crm["cur"].get("disqualified") is not None:
            out["crm.disqualified"] = crm_count(crm["cur"]["disqualified"], cfg)
            out["crm.disqualified_share"] = pct(crm["cur"]["disqualified"] / crm["cur"]["total"]) if crm["cur"]["total"] else "–"
        w = crm["window"]
        out["crm.window_weeks"] = f"{w['weeks']} week{'s' if w['weeks'] != 1 else ''}"
        out["crm.window_paid"] = crm_count(w["paid"], cfg)
        out["crm.cost_per_paid"] = money(w["cost_per_paid"])
        for s, v in crm["per_source"].items():
            out[f"crm.src.{slug(s)}.mqls"] = crm_count(v["mqls"], cfg)
            out[f"crm.src.{slug(s)}.cost_per_mql"] = money(v["cost_per_mql"])
            out[f"crm.src.{slug(s)}.per100"] = num(v["per100"], 1)
        weeks = [dt.date.fromisoformat(x) for x in crm["weeks"]]
        for s, vals in crm["mqls"].items():
            for wk, v in zip(weeks, vals):
                tag = "cur" if wk == dt.date.fromisoformat(f["week"]["start"]) else ("prev" if wk == dt.date.fromisoformat(f["week"]["start"]) - dt.timedelta(days=7) else wk.isoformat())
                out[f"crm.mql.{slug(s)}.{tag}"] = crm_count(v, cfg)
    return out


def fill(text, fmt):
    def rep(m):
        k = m.group(1).strip()
        if k not in fmt:
            raise ReportError(f"Unknown placeholder {{{{{k}}}}} in the inputs. See facts.json → fmt for the keys.")
        return fmt[k]
    return re.sub(r"\{\{([^}]+)\}\}", rep, text)


def rich(text, fmt):
    s = E(fill(text, fmt))
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


# ----------------------------------------------------------------------------------------------- HTML (brand)
sys.path.insert(0, os.path.join(HERE, "..", "brand"))
import brand as B  # noqa: E402  (Plug and Play brand colours, fonts, logo, card style)

CSS = B.BASE_CSS + f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ font-size: 8.3pt; line-height: 1.33; }}
.page {{ width: 210mm; min-height: 296mm; padding: 8mm 10mm 6mm; display: flex; flex-direction: column; gap: 2.6mm; break-after: page; }}
.page:last-child {{ break-after: auto; }}
.hdr {{ display: flex; justify-content: space-between; align-items: flex-start; }}
.logo {{ width: 38mm; height: auto; display: block; margin: 1mm 0 2.8mm; }}
.hdr-r {{ text-align: right; }}
.kicker {{ color: {B.GRAY}; font-size: 7.6pt; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }}
.wk {{ color: {B.DARK_BLUE}; font-size: 20pt; line-height: 1.1; margin-top: 1px; }}
.cmp {{ color: {B.GRAY}; font-size: 7.6pt; margin-top: 2px; }}
.card {{ padding: 2.7mm 3.6mm; }}
.headline .bar {{ width: 34px; height: 4px; border-radius: 2px; background: {B.YELLOW}; margin-bottom: 6px; }}
.headline .h {{ color: {B.DARK_BLUE}; font-size: 12pt; font-weight: 700; line-height: 1.26; }}
.headline .s {{ margin-top: 2px; font-size: 8.6pt; }}
h2 {{ color: {B.DARK_BLUE}; font-size: 10pt; margin: 0 0 1.8mm; font-weight: 700; display: flex; align-items: baseline; gap: 7px; flex-wrap: wrap; }}
h2 .hint {{ color: {B.GRAY}; font-size: 7.3pt; font-weight: 400; }}
h2.uline {{ display: block; }}
h2.uline .hint {{ margin-left: 6px; }}
.tiles {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 2.6mm; }}
.tile {{ padding: 2.5mm 3mm 2mm; display: flex; flex-direction: column; min-height: 25mm; }}
.tile .l {{ color: {B.GRAY}; font-size: 6.9pt; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }}
.tile .v {{ color: {B.DARK_BLUE}; font-size: 17pt; font-weight: 700; line-height: 1.12; margin-top: 2px; white-space: nowrap; }}
.tile .v small {{ font-size: 8.6pt; color: {B.GRAY}; font-weight: 700; }}
.tile .d {{ font-size: 7.6pt; margin-top: 2px; }}
.tile .c {{ color: {B.GRAY}; font-size: 7.1pt; margin-top: 1px; }}
.tile .spark {{ margin-top: auto; padding-top: 3px; display: block; }}
.meter {{ height: 5px; border-radius: 3px; background: {B.TINT}; margin: 5px 0 4px; position: relative; }}
.meter span {{ position: absolute; left: 0; top: 0; bottom: 0; border-radius: 3px; background: {B.DARK_BLUE}; }}
.meter i {{ position: absolute; top: -3px; bottom: -3px; width: 2px; background: {B.BAD}; }}
.legend {{ color: {B.GRAY}; font-size: 6.9pt; }}
table {{ width: 100%; border-collapse: collapse; }}
th {{ text-align: right; color: {B.GRAY}; font-weight: 700; font-size: 6.9pt; border-bottom: 1.3px solid {B.DARK_BLUE}; padding: 2px 4px 3px; white-space: nowrap; }}
th:first-child, td:first-child {{ text-align: left; }}
td {{ border-bottom: 1px solid {B.TINT}; padding: 1.8px 4px; font-size: 7.8pt; text-align: right; white-space: nowrap; }}
td.wrap {{ white-space: normal; text-align: left; }}
tr.sub td {{ font-weight: 700; color: {B.DARK_BLUE}; background: {B.BG}; }}
tr.total td {{ font-weight: 700; color: {B.DARK_BLUE}; border-top: 1.3px solid {B.DARK_BLUE}; border-bottom: none; }}
tr.muted td {{ color: {B.GRAY}; }}
tr.grp td {{ font-size: 6.7pt; color: {B.GRAY}; font-weight: 700; letter-spacing: .05em; text-transform: uppercase; border-bottom: none; padding-top: 5px; }}
.dl {{ font-weight: 700; white-space: nowrap; }}
.ar {{ width: .62em; height: .55em; margin-right: 2px; vertical-align: .02em; }}
.dl.sm {{ font-size: 7pt; margin-left: 3px; }}
.dl.good {{ color: {B.GOOD}; }} .dl.bad {{ color: {B.BAD}; }} .dl.flat {{ color: {B.GRAY}; }}
.dl.lv {{ font-style: italic; font-weight: 400; }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2.6mm; }}
.cols.wide {{ grid-template-columns: 1.5fr 1fr; }}
.top-line {{ width: 26px; height: 3px; border-radius: 2px; margin-bottom: 4px; }}
.list {{ list-style: none; padding: 0; margin: 0; }}
.list li {{ position: relative; padding: 0 0 0 14px; margin: 0 0 1.6mm; font-size: 8.1pt; line-height: 1.33; }}
.list li:last-child {{ margin-bottom: 0; }}
.list li::before {{ position: absolute; left: 0; top: 0; font-weight: 700; }}
.list.good li::before {{ content: ""; width: 9px; height: 9px; top: 2.5px; background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 10'><path d='M1 5.6 3.9 8.4 9 1.6' fill='none' stroke='%231E862F' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg>") no-repeat center / contain; }}
.list.bad li::before {{ content: "!"; color: {B.BAD}; left: 3px; }}
.list li b {{ color: {B.DARK_BLUE}; }}
.acts td {{ white-space: normal; text-align: left; vertical-align: top; font-size: 7.9pt; }}
.acts td.n {{ width: 14px; color: {B.DARK_BLUE}; font-weight: 700; }}
.acts td.o {{ width: 70px; color: {B.GRAY}; }}
.acts td.due {{ width: 50px; color: {B.GRAY}; white-space: nowrap; }}
.chip {{ display: inline-block; font-size: 6.8pt; font-weight: 700; padding: 0 6px; border-radius: 8px; white-space: nowrap; border: 1px solid; }}
.chip.done {{ color: {B.GOOD}; }} .chip.prog {{ color: {B.GRAY}; }} .chip.not {{ color: {B.BAD}; }}
.decision {{ font-size: 8pt; }}
.right-stack h2 + .decision {{ margin-top: 0; }}
.decision b {{ color: {B.DARK_BLUE}; }}
.empty {{ color: {B.GRAY}; font-size: 8pt; margin: 0; }}
.crm {{ display: grid; grid-template-columns: 1.55fr 1fr; gap: 4mm; align-items: start; }}
.ratio {{ background: {B.BG}; border-radius: {B.RADIUS}; padding: 2mm 3mm; margin-bottom: 2mm; }}
.ratio:last-child {{ margin-bottom: 0; }}
.ratio .v {{ color: {B.DARK_BLUE}; font-size: 12pt; font-weight: 700; }}
.ratio .l {{ color: {B.GRAY}; font-size: 7.2pt; }}
.notes {{ color: {B.GRAY}; font-size: 6.9pt; line-height: 1.36; margin: 0; padding-left: 12px; columns: 2; column-gap: 7mm; }}
.notes li {{ margin: 0 0 1.5px; break-inside: avoid; }}
.neg {{ font-size: 7.8pt; margin-top: 2mm; }}
.neg span {{ display: inline-block; background: {B.BG}; border-radius: 6px; padding: 0 5px; margin: 1px 2px 1px 0; color: {B.TEXT}; }}
.foot {{ margin-top: auto; color: {B.GRAY}; font-size: 6.8pt; display: flex; justify-content: space-between; }}
.p2hdr {{ display: flex; justify-content: space-between; align-items: baseline; }}
.p2hdr .t {{ color: {B.DARK_BLUE}; font-size: 13pt; }}
.p2 {{ padding-top: 6.5mm; padding-bottom: 5mm; gap: 2.2mm; }}
.p2 td {{ padding: 1.3px 4px; }}
.p2 th {{ padding-bottom: 2px; }}
.p2 .card {{ padding: 2.2mm 3.4mm; }}
.p2 h2 {{ margin-bottom: 1.4mm; }}
"""


def tile(label, value, delta="", context="", spark=""):
    return (f'<div class="card tile"><div class="l">{label}</div><div class="v">{value}</div>'
            f'<div class="d">{delta}</div><div class="c">{context}</div>{spark}</div>')


def lv(m1, m2, th):
    return min(m1["leads"], m2["leads"]) < th["low_volume_leads"]


def paid_mqls_by_channel(f, cfg, key):
    """HubSpot paid MQLs mapped to each lead channel for the report week (key='cur') or the week before ('prev')."""
    crm = f["crm"]
    if not crm or not crm.get(key):
        return None
    wk = dt.date.fromisoformat(f["week"]["start"]) - (dt.timedelta(days=7) if key == "prev" else dt.timedelta(0))
    weeks = [dt.date.fromisoformat(x) for x in crm["weeks"]]
    if wk not in weeks:
        return None
    i = weeks.index(wk)
    out = collections.Counter()
    for s, ch in cfg["crm"]["paid_sources"].items():
        if s in crm["mqls"] and crm["mqls"][s][i] >= 0:
            out[ch] += crm["mqls"][s][i]
    return out


def channel_rows(f, cfg):
    th = cfg["thresholds"]
    mq = paid_mqls_by_channel(f, cfg, "cur")
    rows = []

    def row(label, b, cls="", lead=True, mql="–"):
        cur, prev, avg = b["cur"], b["prev"], b["avg"]
        low = lv(cur, prev, th)
        sp = money(cur["spend"]) + delta_html(change(cur["spend"], prev["spend"]), neutral=True)
        if lead:
            ld = num(cur["leads"], 1 if cur["leads"] % 1 else 0) + delta_html(change(cur["leads"], prev["leads"]), low_volume=low)
            cpl = money(cur["cpl"], 2) + delta_html(change(cur["cpl"], prev["cpl"]), lower_is_better=True, low_volume=low)
            cells = [ld, cpl, money(avg["cpl"], 2), money(cur["cpc"], 2)]
        else:
            cells = ["–", "–", "–", "–"]
        mq_cell = f"<td>{mql}</td>" if mq is not None else ""
        rows.append(f'<tr class="{cls}"><td>{E(label)}</td><td>{sp}</td>' + "".join(f"<td>{c}</td>" for c in cells) + mq_cell + "</tr>")

    for k in LEAD_GEN:
        c = f["channels"][k]
        if c["cur"]["spend"] or c["prev"]["spend"]:
            row(c["label"], c, mql=crm_count(mq[k], cfg) if mq is not None and k in mq else "–")
    row("Lead generation", f["leadgen"], "sub", mql=crm_count(sum(mq.values()), cfg) if mq is not None else "–")
    shown = False
    for k in NON_LEAD:
        c = f["channels"][k]
        if c["cur"]["spend"] or c["prev"]["spend"]:
            if not shown:
                rows.append(f'<tr class="grp"><td colspan="{7 if mq is not None else 6}">Not aimed at leads · counts toward the budget</td></tr>')
                shown = True
            row(c["label"], c, "muted", lead=False)
    row("Total spend", f["total"], "total", lead=False)
    head = ("<tr><th>Channel</th><th>Spend</th><th>Leads</th><th>Cost per lead</th><th>4-wk avg cost per lead</th>"
            "<th>Cost per click</th>" + ("<th>Paid MQLs</th>" if mq is not None else "") + "</tr>")
    return "<table>" + head + "".join(rows) + "</table>"


def auto_channel_notes(f):
    notes = []
    for k in LEAD_GEN:
        c = f["channels"][k]
        last = f["last_spend"].get(k)
        if not (c["cur"]["spend"] or c["prev"]["spend"]) and last:
            notes.append(f"{c['label']}: no spend since {dt.date.fromisoformat(last):%-d %b}.")
    return notes


def campaign_table(f, cfg, ch_keys, google=False):
    th = cfg["thresholds"]
    out = [("<tr><th>Campaign</th><th>Spend</th><th>Clicks</th><th>Cost per click</th><th>Conversions</th>"
            "<th>Cost per conversion</th><th>Last week</th><th>4-wk average</th></tr>") if google else
           ("<tr><th>Campaign</th><th>Spend</th><th>Leads</th><th>Cost per lead</th><th>Last week</th>"
            "<th>4-wk average</th><th>4-wk leads/week</th><th>Click rate</th></tr>")]
    for ck in ch_keys:
        lst = f["campaigns"].get(ck, [])
        if not lst:
            continue
        lead = ck in LEAD_GEN
        if not lead:
            out.append(f'<tr class="grp"><td colspan="8">{E(CH_LABEL[ck])} · not aimed at leads</td></tr>')
            if google:
                cur = collections.Counter()
                for c in lst:
                    for k2 in ("spend", "clicks"):
                        cur[k2] += c["cur"][k2]
                n = sum(1 for c in lst if c["cur"]["spend"])
                out.append(f'<tr class="muted"><td>{E(CH_LABEL[ck])} · {n} campaign{"s" if n != 1 else ""} this week</td>'
                           f'<td>{money(cur["spend"])}</td><td>{num(cur["clicks"])}</td>'
                           f'<td>{money(cur["spend"] / cur["clicks"], 2) if cur["clicks"] else "–"}</td><td>–</td><td>–</td><td>–</td><td>–</td></tr>')
                continue
        for c in lst:
            cur, prev, avg = c["cur"], c["prev"], c["avg"]
            name = E(c["label"]) + (' <span class="dl flat sm">ended</span>' if c["ended"] else "")
            if not lead:
                out.append(f'<tr class="muted"><td>{name}</td><td>{money(cur["spend"])}</td><td>–</td><td>–</td><td>–</td>'
                           f'<td>–</td><td>–</td><td>{pct(cur["ctr"], 2)}</td></tr>')
                continue
            vs4 = delta_html(change(cur["cpl"], avg["cpl"]), lower_is_better=True,
                             low_volume=min(cur["leads"], avg["leads"]) < th["low_volume_leads"])
            if google:
                conv = num(cur["leads"], 1) if cur["leads"] % 1 else num(cur["leads"])
                out.append(f'<tr><td>{name}</td><td>{money(cur["spend"])}</td><td>{num(cur["clicks"])}</td>'
                           f'<td>{money(cur["cpc"], 2)}</td><td>{conv}</td><td>{money(cur["cpl"], 2)}{vs4}</td>'
                           f'<td>{money(prev["cpl"], 2)}</td><td>{money(avg["cpl"], 2)}</td></tr>')
            else:
                out.append(f'<tr><td>{name}</td><td>{money(cur["spend"])}</td><td>{num(cur["leads"])}</td>'
                           f'<td>{money(cur["cpl"], 2)}{vs4}</td><td>{money(prev["cpl"], 2)}</td><td>{money(avg["cpl"], 2)}</td>'
                           f'<td>{num(avg["leads"], 1)}</td><td>{pct(cur["ctr"], 2)}</td></tr>')
    return "<table>" + "".join(out) + "</table>"


def items_table(items, cfg, fmt, W):
    rows = ["<colgroup><col style='width:31%'><col style='width:17%'><col style='width:8%'><col style='width:7%'>"
            "<col style='width:10%'><col style='width:27%'></colgroup>"
            "<tr><th>Ad, ad group or keyword</th><th style='text-align:left'>Where</th><th>Spend</th><th>Leads</th>"
            "<th>Cost per lead</th><th style='text-align:left'>Note</th></tr>"]
    for it in items:
        sp = to_usd(cfg, it["spend"], it.get("currency", "USD"), W) if it.get("spend") is not None else None
        leads = it.get("leads")
        cpl = sp / leads if sp is not None and leads else None
        rows.append(f'<tr><td class="wrap">{rich(it["item"], fmt)}</td><td class="wrap">{rich(it.get("where", ""), fmt)}</td>'
                    f'<td>{money(sp)}</td><td>{num(leads) if leads is not None else "–"}</td><td>{money(cpl, 2)}</td>'
                    f'<td class="wrap">{rich(it.get("note", ""), fmt)}</td></tr>')
    return "<table>" + "".join(rows) + "</table>"


def crm_section(f, cfg, fmt):
    crm = f["crm"]
    if not crm:
        return '<p class="empty">No HubSpot numbers this week: add them to the crm section of the inputs file.</p>'
    weeks = [dt.date.fromisoformat(x) for x in crm["weeks"]]
    W = dt.date.fromisoformat(f["week"]["start"])
    show = [w for w in weeks if w <= W][-4:]
    idx = {w: i for i, w in enumerate(weeks)}
    has_dq = bool(crm["disqualified"])
    hdr = "".join(f"<th>{short_range(w, w + dt.timedelta(days=6))}</th>" for w in show)
    rows = [f"<tr><th>MQLs by original source</th>{hdr}" + ("<th>Disqualified this week</th>" if has_dq else "") + "</tr>"]
    for s in crm["sources"]:
        paid = s in crm["paid_sources"]
        cells = "".join(f"<td>{crm_count(crm['mqls'][s][idx[w]], cfg)}</td>" for w in show)
        dq = f"<td>{crm_count(crm['disqualified'].get(s, -1), cfg)}</td>" if has_dq else ""
        label = f"<b style='color:{B.DARK_BLUE}'>{E(s)}</b>" if paid else E(s)
        rows.append(f"<tr><td>{label}</td>{cells}{dq}</tr>")
    tot = "".join(f"<td>{crm_count(sum(v[idx[w]] for v in crm['mqls'].values() if v[idx[w]] >= 0), cfg)}</td>" for w in show)
    rows.append(f'<tr class="total"><td>All MQLs</td>{tot}' + (f"<td>{crm_count(sum(crm['disqualified'].values()), cfg)}</td>" if has_dq else "") + "</tr>")
    paid_cells = "".join(f"<td>{crm_count(sum(crm['mqls'][s][idx[w]] for s in crm['paid_sources'] if crm['mqls'][s][idx[w]] >= 0), cfg)}</td>" for w in show)
    rows.append(f'<tr class="sub"><td>Paid MQLs (sources in bold)</td>{paid_cells}' + ("<td></td>" if has_dq else "") + "</tr>")
    for lab, vals in crm["extra"].items():
        cells = "".join(f"<td>{crm_count(vals[idx[w]], cfg)}</td>" for w in show)
        rows.append(f'<tr class="muted"><td>{E(lab)}</td>{cells}' + ("<td></td>" if has_dq else "") + "</tr>")
    table = "<table>" + "".join(rows) + "</table>"
    c = crm.get("cur")
    ratios = ""
    if c:
        ratios += (f'<div class="ratio"><div class="v">{fmt["crm.paid_share"]}</div><div class="l">of all MQLs came from paid'
                   + (f' ({fmt["crm.prev_paid_share"]} last week)' if crm.get("prev") else "") + "</div></div>")
        ratios += (f'<div class="ratio"><div class="v">{fmt["crm.paid_per100"]}</div><div class="l">paid MQLs per 100 platform leads'
                   + (f' ({fmt["crm.prev_paid_per100"]} last week)' if crm.get("prev") else "") + "</div></div>")
    ratios += (f'<div class="ratio"><div class="v">{fmt["crm.cost_per_paid"]}</div><div class="l">cost per paid MQL over the last '
               f'{fmt["crm.window_weeks"]} ({fmt["crm.window_paid"]} paid MQLs)</div></div>')
    note = f'<div class="legend" style="margin-top:2mm">{E(crm["note"])}</div>' if crm.get("note") else ""
    return f'<div class="crm"><div>{table}</div><div>{ratios}{note}</div></div>'


def actions_table(acts, fmt):
    if not acts:
        return '<p class="empty">No actions yet.</p>'
    rows = [f'<tr><td class="n">{i}</td><td>{rich(a["action"], fmt)}</td><td class="o">{E(a.get("owner", ""))}</td>'
            f'<td class="due">{E(a.get("due", ""))}</td></tr>' for i, a in enumerate(acts, 1)]
    return '<table class="acts">' + "".join(rows) + "</table>"


def last_actions(acts, fmt):
    if not acts:
        return ('<p class="empty">First report in this format. From next week, this box shows what happened to each '
                'action from the week before.</p>')
    chip = {"done": ("done", "Done"), "in progress": ("prog", "In progress"), "not done": ("not", "Not done"),
            "no update": ("prog", "No update")}
    rows = []
    for a in acts:
        k, lab = chip.get(a.get("status", "").lower(), ("prog", a.get("status", "")))
        note = f' <span style="color:{B.GRAY}">{rich(a["note"], fmt)}</span>' if a.get("note") else ""
        rows.append(f'<tr><td style="width:72px"><span class="chip {k}">{lab}</span></td><td>{rich(a["action"], fmt)}{note}</td></tr>')
    return '<table class="acts">' + "".join(rows) + "</table>"


def decisions(inp, fmt):
    d = inp.get("decisions") or []
    if not d:
        return ""
    return (f'<div class="top-line" style="background:{B.YELLOW}"></div><h2>Decision needed</h2>'
            + "".join(f'<div class="decision">{rich(x, fmt)}</div>' for x in d) + '<div style="height:2.6mm"></div>')


def draft_lists(f):
    good = [x["text"] for x in f["flags"] if x["tone"] == "good"][:3]
    bad = [x["text"] for x in f["flags"] if x["tone"] == "bad"][:3]
    return good, bad


def spark(values):
    pts = [v for v in values]
    good = [v for v in pts if v is not None]
    if len(good) < 2:
        return ""
    w, h = 120, 18
    lo, hi = min(good), max(good)
    rng = (hi - lo) or 1
    xy = [(2 + (w - 4) * i / (len(pts) - 1), 2 + (h - 4) * (1 - (v - lo) / rng)) for i, v in enumerate(pts) if v is not None]
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in xy)
    lx, ly = xy[-1]
    return (f'<svg class="spark" viewBox="0 0 {w} {h}" width="100%" height="{h}" preserveAspectRatio="none" aria-hidden="true">'
            f'<polyline points="{path}" fill="none" stroke="{B.BLUE_LIGHT}" stroke-width="1.5" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="2.4" fill="{B.DARK_BLUE}"/></svg>')


def render(f, inp, cfg):
    fmt = f["fmt"]
    W = dt.date.fromisoformat(f["week"]["start"])
    th = cfg["thresholds"]
    tot, lg, b = f["total"], f["leadgen"], f["budget"]
    ser = lambda blk, k: [m[k] for m in blk["series"]]
    low = lv(lg["cur"], lg["prev"], th)
    t1 = tile("Total spend", money(tot["cur"]["spend"]),
              delta_html(change(tot["cur"]["spend"], tot["prev"]["spend"]), neutral=True, small=False) + " vs last week",
              f"4-week average {money(tot['avg']['spend'])}", spark(ser(tot, "spend")))
    t2 = tile("Leads", num(lg["cur"]["leads"]),
              delta_html(change(lg["cur"]["leads"], lg["prev"]["leads"]), low_volume=low, small=False) + " vs last week",
              f"4-week average {num(lg['avg']['leads'])}", spark(ser(lg, "leads")))
    t3 = tile("Cost per lead", money(lg["cur"]["cpl"], 2),
              delta_html(change(lg["cur"]["cpl"], lg["prev"]["cpl"]), lower_is_better=True, low_volume=low, small=False) + " vs last week",
              f"4-week average {money(lg['avg']['cpl'], 2)}", spark(ser(lg, "cpl")))
    crm = f["crm"]
    if crm and crm.get("cur"):
        t4 = tile("Paid MQLs", fmt["crm.paid"], f"{fmt['crm.prev_paid']} last week" if crm.get("prev") else "",
                  f"{fmt['crm.paid_share']} of all {fmt['crm.total']} MQLs in HubSpot")
    else:
        t4 = tile("Paid MQLs", "–", "HubSpot numbers not supplied", "")
    fill_pct = min(b["ytd"] / b["maximum"], 1) * 100
    mark = b["budget"] / b["maximum"] * 100
    t5 = tile(f"Budget {cfg['budget']['year']}", f"{money_k(b['ytd'])} <small>{pct(b['pct'])}</small>",
              f'<div class="meter"><span style="width:{fill_pct:.1f}%"></span><i style="left:{mark:.1f}%"></i></div>'
              f"Forecast <b>{money_k(b['forecast'])}</b>",
              f"Budget {money_k(b['budget'])} · maximum {money_k(b['maximum'])}")

    headline = rich(inp["headline"], fmt) if inp.get("headline") else \
        f"DRAFT: write the headline. {num(lg['cur']['leads'])} leads at {money(lg['cur']['cpl'], 2)} each; spend {money(tot['cur']['spend'])}."
    sub = f'<div class="s">{rich(inp["subhead"], fmt)}</div>' if inp.get("subhead") else ""
    dg, db = draft_lists(f)

    def li(items, drafts):
        if items:
            return "".join(f"<li>{('<b>' + rich(i['title'], fmt) + '</b> ') if i.get('title') else ''}{rich(i.get('text', ''), fmt)}</li>" for i in items)
        return "".join(f"<li>DRAFT: {E(t)}</li>" for t in drafts) or "<li>Nothing to report.</li>"

    notes = auto_channel_notes(f) + [fill(n, fmt) for n in inp.get("channel_notes", [])]
    notes_html = "".join(f"<div class='legend' style='margin-top:2px'>{E(n)}</div>" for n in notes)
    week_label = E(f["week"]["label"])
    p1 = f"""<section class="page">
<div class="hdr"><img class="logo" src="{B.wordmark_data_uri()}" alt="Plug and Play">
<div class="hdr-r"><div class="kicker">Paid media · weekly report</div><div class="wk">{week_label}</div>
<div class="cmp">vs {E(f['week']['prev_label'])} and the 4 weeks {E(f['week']['avg_label'])} · USD · data to {E(fmt['data_date'])}</div></div></div>
<div class="card headline"><div class="bar"></div><div class="h">{headline}</div>{sub}</div>
<div class="tiles">{t1}{t2}{t3}{t4}{t5}</div>
<div class="legend">Arrows: vs last week (green better, wine worse, grey neutral or under {th['low_volume_leads']} leads). Lines: last 8 weeks. Leads = form fills counted by Meta and Google; MQLs = qualified in HubSpot.</div>
<div class="card"><h2 class="uline">By channel<span class="hint">lead generation first, then spend not aimed at leads</span></h2>
{channel_rows(f, cfg)}{notes_html}</div>
<div class="cols">
<div class="card"><div class="top-line" style="background:{B.GOOD}"></div><h2>What worked</h2><ul class="list good">{li(inp.get('worked') or [], dg)}</ul></div>
<div class="card"><div class="top-line" style="background:{B.BAD}"></div><h2>What to fix</h2><ul class="list bad">{li(inp.get('fix') or [], db)}</ul></div>
</div>
<div class="cols wide">
<div class="card"><div class="top-line" style="background:{B.DARK_BLUE}"></div><h2>Next week <span class="hint">owner · due</span></h2>{actions_table(inp.get('actions'), fmt)}</div>
<div class="card right-stack">{decisions(inp, fmt)}<div class="top-line" style="background:{B.PURPLE}"></div><h2>Last week's actions</h2>{last_actions(inp.get('last_actions'), fmt)}</div>
</div>
<div class="foot"><span>Plug and Play · Paid media weekly · {week_label} · internal{" · " + E(inp["prepared_by"]) if inp.get("prepared_by") else ""}</span><span>1 / 2</span></div>
</section>"""

    items = inp.get("items") or []
    negs = inp.get("negatives") or []
    items_html = ""
    if items or negs:
        neg_html = ""
        if negs:
            neg_html = '<div class="neg">Search terms to add as negatives: ' + "".join(
                f"<span>{E(n['term'])}{(' · ' + money(to_usd(cfg, n['spend'], n.get('currency', 'USD'), W), 2)) if n.get('spend') is not None else ''}</span>"
                for n in negs) + "</div>"
        items_html = (f'<div class="card"><h2 class="uline">Ads, ad groups and search terms<span class="hint">{E(inp.get("items_source", ""))}</span></h2>'
                      + (items_table(items, cfg, fmt, W) if items else "") + neg_html + "</div>")
    data_notes = auto_notes(f, cfg) + [fill(n, fmt) for n in inp.get("data_notes", [])]
    p2 = f"""<section class="page p2">
<div class="p2hdr"><div class="t">Details: campaigns, lead quality and data notes</div><div class="kicker">{week_label}</div></div>
<div class="card"><h2 class="uline">Meta<span class="hint">cost per lead with its change against the 4-week average ({E(f['week']['avg_label'])})</span></h2>
{campaign_table(f, cfg, ['meta', 'meta_other'])}</div>
<div class="card"><h2 class="uline">Google Ads<span class="hint">conversions as counted by Google · change against the 4-week average</span></h2>
{campaign_table(f, cfg, ['google_search', 'pmax', 'youtube'], google=True)}</div>
{items_html}
<div class="card"><h2 class="uline">Lead quality (HubSpot)<span class="hint">MQLs by original source</span></h2>{crm_section(f, cfg, fmt)}</div>
<div class="card"><h2 class="uline">Data notes</h2><ul class="notes">{''.join('<li>' + E(n) + '</li>' for n in data_notes)}</ul></div>
<div class="foot"><span>Plug and Play · Paid media weekly · {week_label} · internal</span><span>2 / 2</span></div>
</section>"""
    title = f"Paid Media Weekly · {f['week']['label']}"
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{E(title)}</title><style>{CSS}</style></head>"
            f"<body>{p1}{p2}</body></html>")


def auto_notes(f, cfg):
    fx = cfg["budget"]["eur_to_usd"]
    rate = f["fx"]["eur_to_usd_this_month"]
    lo = cfg["thresholds"]["crm_min_count"]
    return [
        f"Sources: Meta and Google exports (campaign × day, data to {dt.date.fromisoformat(f['data_date']):%-d %b %Y}), "
        "the Other channels list and the HubSpot numbers in the week's inputs. USD; EUR at 1 EUR = "
        f"{rate} USD" + ("." if len(set(fx)) == 1 else " (monthly rates from the tracker)."),
        "Leads: Meta = Results of lead campaigns; Google = Conversions of Search and Performance Max.",
        f"4-week average = {f['week']['avg_label']}. Budget as in the spend tracker: pace of the last 3 full weeks "
        f"({f['budget']['pace_window']}) without ended campaigns.",
        (f"HubSpot counts of 1–{lo - 1} show as <{lo} (GDPR). " if lo > 1 else "")
        + "No ROAS: revenue isn't tracked by ad source.",
    ]


def summary_md(f, inp, cfg):
    fmt = f["fmt"]
    tot, b = f["total"], f["budget"]
    lines = [f"*Paid media weekly · {f['week']['label']}* (vs {f['week']['prev_label']})", ""]
    if inp.get("headline"):
        lines += [fill(inp["headline"], fmt).replace("**", "*"), ""]
    lines.append(f"• Spend {money(tot['cur']['spend'])} ({fmt['total.spend_vs_prev']}) · Leads {fmt['leadgen.leads']} ({fmt['leadgen.leads_vs_prev']}) · "
                 f"Cost per lead {fmt['leadgen.cpl']} ({fmt['leadgen.cpl_vs_prev']})"
                 + (f" · Paid MQLs {fmt['crm.paid']} ({fmt['crm.prev_paid']} last week)" if f["crm"] and f["crm"].get("cur") else ""))
    lines.append(f"• Budget: {money_k(b['ytd'])} spent ({pct(b['pct'])} of {money_k(b['budget'])}) · forecast {money_k(b['forecast'])} · "
                 f"{money_k(b['budget'])} needs {money(b['allow'])}/week, now {money(b['pace'])}/week")
    for title, key in (("Worked", "worked"), ("To fix", "fix")):
        if inp.get(key):
            lines += ["", f"*{title}*"] + [f"• {fill((i.get('title', '') + ' ' + i.get('text', '')).strip(), fmt).replace('**', '*')}" for i in inp[key]]
    if inp.get("actions"):
        lines += ["", "*Next week*"] + [f"{n}. {fill(a['action'], fmt).replace('**', '*')} ({a.get('owner', '')}, {a.get('due', '')})"
                                        for n, a in enumerate(inp["actions"], 1)]
    if inp.get("decisions"):
        lines += ["", "*Decision needed*"] + [f"• {fill(d, fmt).replace('**', '*')}" for d in inp["decisions"]]
    return "\n".join(lines) + "\n"


def to_jsonable(o):
    if isinstance(o, dict):
        return {k: to_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [to_jsonable(v) for v in o]
    if isinstance(o, float):
        return round(o, 4)
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()
    return o


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--google", required=True)
    ap.add_argument("--inputs")
    ap.add_argument("--other", default=os.path.join(ROOT, "reports", "weekly", "other_channels.csv"))
    ap.add_argument("--config", default=os.path.join(HERE, "config.toml"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--pdf", action="store_true")
    args = ap.parse_args()
    try:
        facts, inp, cfg = build(args)
        os.makedirs(args.out, exist_ok=True)
        stem = f"Paid_Media_Weekly_{facts['week']['start']}"
        html_path = os.path.join(args.out, stem + ".html")
        open(html_path, "w", encoding="utf-8").write(render(facts, inp, cfg))
        json.dump(to_jsonable(facts), open(os.path.join(args.out, "facts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        open(os.path.join(args.out, "summary.md"), "w", encoding="utf-8").write(summary_md(facts, inp, cfg))
        print(f"Week {facts['week']['label']} · data to {facts['data_date']}")
        print(f"Spend {money(facts['total']['cur']['spend'], 2)} · leads {facts['leadgen']['cur']['leads']:.1f} · "
              f"cost per lead {money(facts['leadgen']['cur']['cpl'], 2)}")
        b = facts["budget"]
        print(f"Budget: YTD {money(b['ytd'], 2)} · pace {money(b['pace'], 2)}/week · forecast {money(b['forecast'], 2)} · "
              f"allowance {money(b['allow'], 2)}/week")
        print("Flags:")
        for x in facts["flags"]:
            print(f"  [{x['tone']}] {x['text']}")
        if args.pdf:
            font = B.font_in_use()
            pdf = os.path.join(args.out, stem + ".pdf")
            subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf}", "file://" + os.path.abspath(html_path)],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
            pages = int(re.search(r"Pages:\s+(\d+)", info).group(1)) if "Pages:" in info else None
            fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
            print(f"PDF: {pdf} · {pages} pages · font {font}")
            if pages not in (None, 2):
                print(f"WARNING: the report should be 2 pages, not {pages}. Shorten the text in the inputs.")
            names = [ln.split()[0] for ln in fonts.splitlines()[2:] if ln.strip()]
            brand_key = font.lower().replace(" ", "")
            others = sorted({re.sub(r"^[A-Z]{6}\+", "", n) for n in names if brand_key not in n.lower()})
            if not any(brand_key in n.lower() for n in names):
                print(f"WARNING: {font} is not embedded in the PDF; check the fonts.")
            if others:
                print(f"WARNING: non-brand fonts in the PDF ({', '.join(others)}): some character in the text is not in "
                      f"{font}. Replace it (arrows, ticks and similar symbols are the usual cause).")
    except (ReportError, RuntimeError) as e:
        sys.exit(f"Stopped: {e}")


if __name__ == "__main__":
    main()
