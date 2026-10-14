"""Paid media audit & 2027 strategy proposal – 16:9 PDF deck (HTML → Chromium).
Numbers: Meta/Google exports 1 Jan–12 Oct 2026 (USD, EUR at 1.1177), HubSpot ICP audit (1 Oct 2025–30 Sep 2026, aggregates),
agency weekly reports (Notion, as written), Tereza's EMEA H1 deck. Strategy source: Felipe's B2B Lead Gen Paid Media Playbook 2026.
"""
import html, sys
E = html.escape
BLUE, ORANGE, AQUA, NAVY, INK, INK2, MUTED, GRID, RED, GREEN, SLATE, AMBER = (
    "#2a78d6", "#eb6834", "#1baf7a", "#1f3864", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1", "#c42f2f", "#0a7d0a", "#6b7a8f", "#b7791f")
PALE, SUB = "#f3f7fd", "#f7f7f5"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct*"]
META_S = [8093, 28953, 38387, 22242, 22277, 17453, 18957, 10644, 11063, 2700]
GOOG_S = [10839, 11084, 10113, 9972, 12064, 13956, 13148, 12247, 6854, 1222]
META_CPL = [11.26, 18.60, 25.32, 25.39, 35.25, 35.99, 66.75, 21.77, 16.89, 15.52]
GOOG_CPL = [48.37, 73.30, 67.31, 84.10, 84.89, 88.97, 191.78, 44.88, 41.42, 29.79]
META_REG = [719, 1557, 1516, 876, 632, 485, 284, 489, 655, 174]
GOOG_CONV = [224, 151, 150, 119, 142, 157, 69, 273, 165, 41]


def usd(x, k=False):
    if k:
        v = x / 1000
        return f"${v:,.0f}k" if abs(v - round(v)) < 0.05 else f"${v:,.1f}k"
    return f"${x:,.0f}"


# ------------------------------------------------------------------ charts
def spend_chart(w=620, h=215):
    pl, pr, pt, pb = 44, 10, 12, 26
    iw, ih = w - pl - pr, h - pt - pb
    n, ymax = len(MONTHS), 50000
    bw = iw / n * 0.6
    X = lambda i: pl + iw * (i + 0.5) / n
    Y = lambda v: pt + ih * (1 - v / ymax)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%">']
    for t in range(0, ymax + 1, 10000):
        s.append(f'<line x1="{pl}" x2="{pl+iw}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{GRID}"/><text x="{pl-6}" y="{Y(t)+3.5:.1f}" text-anchor="end" class="ax">{usd(t,True) if t else "$0"}</text>')
    for i in range(n):
        base = 0
        for val, col in ((META_S[i], BLUE), (GOOG_S[i], ORANGE)):
            y0, y1 = Y(base), Y(base + val)
            s.append(f'<rect x="{X(i)-bw/2:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(0.5,y0-y1-1):.1f}" fill="{col}" rx="1.5"/>')
            base += val
        s.append(f'<text x="{X(i):.1f}" y="{Y(base)-4:.1f}" text-anchor="middle" class="lbl">{usd(base,True)}</text>')
        s.append(f'<text x="{X(i):.1f}" y="{h-9}" text-anchor="middle" class="ax">{MONTHS[i]}</text>')
    s.append("</svg>")
    return "".join(s)


def cpl_chart(w=620, h=215):
    pl, pr, pt, pb = 44, 10, 14, 26
    iw, ih = w - pl - pr, h - pt - pb
    n, ymax = len(MONTHS), 200
    X = lambda i: pl + iw * (i + 0.5) / n
    Y = lambda v: pt + ih * (1 - min(v, ymax) / ymax)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%">']
    for t in range(0, ymax + 1, 50):
        s.append(f'<line x1="{pl}" x2="{pl+iw}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{GRID}"/><text x="{pl-6}" y="{Y(t)+3.5:.1f}" text-anchor="end" class="ax">${t}</text>')
    s.append(f'<rect x="{X(6)-iw/n*0.5:.1f}" y="{pt}" width="{iw/n:.1f}" height="{ih}" fill="#fbe5e5" opacity=".7"/>')
    s.append(f'<text x="{X(6):.1f}" y="{pt+10}" text-anchor="middle" class="ax" fill="{RED}">tracking down</text>')
    for series, col in ((GOOG_CPL, ORANGE), (META_CPL, BLUE)):
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(series))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.4" stroke-linejoin="round"/>')
        for i, v in enumerate(series):
            s.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="3" fill="{col}" stroke="#fff" stroke-width="1.2"/>')
            if i in (0, 5, 9) or (col == ORANGE and i in (3, 7)):
                s.append(f'<text x="{X(i):.1f}" y="{Y(v)-7:.1f}" text-anchor="middle" class="lbl" fill="{col}">${v:.0f}</text>')
    for i in range(n):
        s.append(f'<text x="{X(i):.1f}" y="{h-9}" text-anchor="middle" class="ax">{MONTHS[i]}</text>')
    s.append("</svg>")
    return "".join(s)


def hbar_chart(rows, w=560, maxv=None, fmt=lambda v: f"{v:.0%}", colors=None, h_row=22, label_w=190):
    maxv = maxv or max(v for _, v, *_ in rows)
    h = h_row * len(rows) + 6
    bw_max = w - label_w - 70
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%">']
    for i, row in enumerate(rows):
        name, v = row[0], row[1]
        col = (colors[i] if colors else SLATE)
        y = 3 + i * h_row
        s.append(f'<text x="{label_w-8}" y="{y+h_row*0.68:.1f}" text-anchor="end" class="lbl">{E(name)}</text>')
        s.append(f'<rect x="{label_w}" y="{y+4}" width="{bw_max*v/maxv:.1f}" height="{h_row-8}" fill="{col}" rx="2"/>')
        s.append(f'<text x="{label_w+bw_max*v/maxv+6:.1f}" y="{y+h_row*0.68:.1f}" class="lbl">{E(fmt(v))}</text>')
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ helpers
def tbl(head, rows, cls=""):
    th = "".join(f'<th class="{"num" if i and isinstance(h, tuple) else ""}">{E(h[0]) if isinstance(h, tuple) else E(h)}</th>' for i, h in enumerate(head))
    body = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            if isinstance(c, tuple):
                tds.append(f'<td class="{c[1]}">{c[0]}</td>')
            else:
                tds.append(f"<td>{c}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return f'<table class="{cls}"><tr>{th}</tr>{"".join(body)}</table>'


def tag(txt, kind):
    return f'<span class="tag {kind}">{txt}</span>'


def slide(kicker, title, body, n, note=""):
    return f'''<section class="slide"><div class="kicker">{E(kicker)}</div><h1>{title}</h1>{body}
<div class="foot"><span>{E(note)}</span><span>Paid media audit &amp; strategy proposal · Plug and Play · Oct 2026 · {n}</span></div></section>'''


CSS = f"""
@page {{ size: 13.333in 7.5in; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: Inter, 'Liberation Sans', Arial, sans-serif; color: {INK}; font-size: 11pt; line-height: 1.38; }}
.slide {{ width: 13.333in; height: 7.5in; padding: .42in .6in .5in; page-break-after: always; position: relative; overflow: hidden; background: #fff; }}
.slide:last-child {{ page-break-after: auto; }}
.kicker {{ color: {BLUE}; font-weight: 700; font-size: 8.5pt; letter-spacing: .09em; text-transform: uppercase; }}
h1 {{ font-size: 21pt; margin: 2px 0 10px; letter-spacing: -.01em; line-height: 1.15; }}
h2 {{ font-size: 11.5pt; margin: 0 0 5px; color: {NAVY}; }}
h3 {{ font-size: 10pt; margin: 0 0 3px; color: {INK}; }}
p {{ margin: 0 0 6px; }}
.foot {{ position: absolute; left: .6in; right: .6in; bottom: .22in; display: flex; justify-content: space-between; color: {MUTED}; font-size: 7.6pt; }}
.cols {{ display: grid; gap: 16px; }} .c2 {{ grid-template-columns: 1fr 1fr; }} .c3 {{ grid-template-columns: 1fr 1fr 1fr; }}
.c21 {{ grid-template-columns: 2fr 1fr; }} .c12 {{ grid-template-columns: 1fr 2fr; }} .c32 {{ grid-template-columns: 3fr 2fr; }}
.tiles {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px; margin: 4px 0 10px; }}
.tile {{ border: 1px solid {GRID}; border-radius: 8px; padding: 7px 10px; }}
.tile .l {{ color: {INK2}; font-size: 7.6pt; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }}
.tile .v {{ font-size: 17pt; font-weight: 700; line-height: 1.15; margin-top: 2px; }}
.tile .d {{ font-size: 7.8pt; color: {INK2}; margin-top: 2px; }}
.red {{ color: {RED}; }} .green {{ color: {GREEN}; }} .amber {{ color: {AMBER}; }} .muted {{ color: {MUTED}; }} .b {{ font-weight: 700; }}
ul {{ margin: 0; padding-left: 16px; }} li {{ margin: 0 0 4px; }}
ul.list {{ padding: 0; list-style: none; }}
ul.list li {{ padding: 4px 9px 4px 11px; border-left: 3px solid {GRID}; margin: 4px 0; background: {SUB}; border-radius: 0 6px 6px 0; font-size: 10pt; }}
ul.flag li {{ border-left-color: {RED}; }} ul.work li {{ border-left-color: {GREEN}; }} ul.imp li {{ border-left-color: #e0a100; }} ul.blue li {{ border-left-color: {BLUE}; }}
table {{ width: 100%; border-collapse: collapse; }}
th {{ text-align: left; color: {INK2}; font-weight: 600; font-size: 8.3pt; border-bottom: 1.5px solid {INK}; padding: 3px 5px; }}
td {{ border-bottom: 1px solid {GRID}; padding: 3px 5px; font-size: 9.2pt; vertical-align: top; }}
th.num, td.num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
tr.tot td {{ font-weight: 700; border-top: 1.5px solid {INK}; }}
table.small td {{ font-size: 8.6pt; padding: 2px 4px; }} table.small th {{ font-size: 7.9pt; }}
.tag {{ display: inline-block; font-size: 7.4pt; font-weight: 700; padding: 1px 6px; border-radius: 10px; white-space: nowrap; }}
.tag.keep {{ background: #e3f3e3; color: {GREEN}; }} .tag.upd {{ background: #fff1d6; color: {AMBER}; }} .tag.pause {{ background: #fbe5e5; color: {RED}; }} .tag.test {{ background: #e4eefb; color: {BLUE}; }} .tag.done {{ background: #eee; color: {INK2}; }}
.legend {{ font-size: 8pt; color: {INK2}; margin-top: 2px; }}
.sw {{ display: inline-block; width: 9px; height: 9px; border-radius: 2px; margin: 0 4px -1px 10px; }}
.note {{ color: {MUTED}; font-size: 7.8pt; margin-top: 5px; }}
.box {{ border: 1px solid {GRID}; border-radius: 8px; padding: 8px 11px; }}
.box.pale {{ background: {PALE}; border-color: #d6e3f5; }} .box.red {{ background: #fdf3f3; border-color: #f0caca; }} .box.green {{ background: #eef8ee; border-color: #cfe7cf; }}
svg text {{ font-family: Inter, sans-serif; }} svg .ax {{ fill: {MUTED}; font-size: 9.5px; }} svg .lbl {{ fill: {INK2}; font-size: 9.5px; font-weight: 600; }}
.steps {{ counter-reset: s; margin: 0; padding: 0; list-style: none; }}
.steps li {{ counter-increment: s; position: relative; padding: 5px 9px 5px 32px; margin: 4px 0; background: {PALE}; border-radius: 6px; font-size: 9.8pt; }}
.steps li::before {{ content: counter(s); position: absolute; left: 8px; top: 6px; width: 18px; height: 18px; border-radius: 50%; background: {BLUE}; color: #fff; font-weight: 700; font-size: 8pt; text-align: center; line-height: 18px; }}
.title {{ background: {NAVY}; color: #fff; padding: 1.1in .8in; }}
.title .kicker {{ color: #9cc3f5; }} .title h1 {{ font-size: 34pt; color: #fff; margin-top: 14px; max-width: 10in; }}
.title p {{ color: #d5e2f5; font-size: 12pt; max-width: 9.5in; }}
.title .foot {{ color: #9cc3f5; }}
.flow {{ display: flex; align-items: stretch; gap: 6px; }}
.flow .st {{ flex: 1; border: 1px solid {GRID}; border-radius: 8px; padding: 7px 9px; font-size: 9.2pt; background: #fff; }}
.flow .st h3 {{ font-size: 9.3pt; color: {NAVY}; }}
.flow .arrow {{ align-self: center; color: {MUTED}; font-size: 16pt; }}
.st.bad {{ border-color: #f0caca; background: #fdf6f6; }}
.pill {{ display: inline-block; background: {NAVY}; color: #fff; font-size: 7.4pt; font-weight: 700; padding: 1px 7px; border-radius: 10px; margin-right: 4px; }}
.gate {{ background: #fff1d6; border-left: 3px solid #e0a100; padding: 4px 8px; font-size: 8.6pt; margin-top: 6px; border-radius: 0 6px 6px 0; }}
"""

pages = []

# 1 ---------------------------------------------------------------- title
pages.append(f'''<section class="slide title"><div class="kicker">Performance marketing · Paid media</div>
<h1>Paid media audit and strategy proposal: from cheap leads to ICP leads</h1>
<p>Meta, Google Search and ChatGPT Ads · what we ran in 2026, what the data says, and the structure I propose for Q4 2026 and 2027.</p>
<p style="font-size:10pt;margin-top:28px">Felipe Cárdenas · Performance Marketing &amp; CRM · 14 October 2026<br>
Data: platform exports 1 Jan – 12 Oct 2026 (USD; EUR at 1.1177), HubSpot ICP audit (Oct 2025 – Sep 2026, aggregates only), the agency's weekly reports, EMEA H1 deck.<br>
Strategy source: <i>B2B Lead Gen Paid Media Playbook 2026: Meta, Google Search &amp; ChatGPT Ads</i>.</p>
<div class="foot"><span></span><span>1</span></div></section>''')

# 2 ---------------------------------------------------------------- summary
body = f'''
<div class="cols c3">
<div><h2>Where we are</h2><ul class="list blue">
<li><b>$282.5k spent to 12 Oct</b> (94% of the $300k budget): Meta $180.8k, Google $101.5k, ChatGPT $0.3k. Current pace $1.9k/week.</li>
<li><b>8,878 platform leads</b>: 7,387 Meta registrations at $24.5 and 1,491 Google conversions at $68.1.</li>
<li>Meta's best month for cost was January ($11); Google's best is now (Sep–Oct, ≈$30–41) after the August rebuild.</li>
<li>EMEA H1: 954 MQLs, 43 SQLs, $2.1k per SQL, 66 days MQL → SQL.</li>
</ul></div>
<div><h2>What the data says is wrong</h2><ul class="list flag">
<li><b>We optimise to form fills, so we get startups and "Other".</b> Paid social: 61% of all content downloads, 0.2% qualified by sales; 40% of paid-social Contact-us leads are disqualified (organic search: 9%).</li>
<li><b>ICP can't be measured</b>: job title empty for 67% of Contact-us and 83% of download contacts.</li>
<li><b>Structure is pre-Andromeda</b>: 7 Meta prospecting campaigns split by geography, each too small to learn; Google ran 14 country, region and US-state Search campaigns in H1 (NY $614, FL $400 per conversion).</li>
<li><b>Tracking broke twice</b> (welcome event dark 15 Jul – 11 Aug; HubSpot vs platform gaps of 7×); lead definition changed 5 times.</li>
<li><b>$12.1k on YouTube / Demand Gen for 3 conversions.</b></li>
</ul></div>
<div><h2>What I propose</h2><ul class="list work">
<li><b>One qualified signal</b>: define an "ICP lead" in HubSpot (corporate 10,000+ or government, target role), fire the platform conversion only for those, and send it back to Meta and Google.</li>
<li><b>Meta: 7 → 3 campaigns</b> (EMEA, Americas, warm), broad Advantage+ audiences, 8–12 genuinely different creatives per region that say who the ad is for.</li>
<li><b>Google: keep the two non-brand Search engines</b>, rebuild ad groups by intent with exact/phrase, add brand and competitor, qualifier headlines, AI Max and PMax only after offline conversions flow.</li>
<li><b>Stop paying for views</b>: pause YouTube video-view campaigns inside the lead-gen budget.</li>
<li><b>ChatGPT Ads</b>: 60-day test in Q1 2027 once CRM-verified tracking exists; LinkedIn stays off (manager's call).</li>
</ul></div></div>
<div class="box pale" style="margin-top:8px"><b>Target:</b> report and bid on <b>cost per qualified (ICP) lead</b> and cost per SQL instead of CPL. Proposed KPI wording for the −20% Meta CPL goal: −20% cost per <i>qualified</i> lead, because filtering raises raw CPL on purpose.</div>'''
pages.append(slide("Summary", "In one page", body, 2))

# 3 ---------------------------------------------------------------- spend & results
LEG = (f'<div class="legend"><span class="sw" style="background:{BLUE};margin-left:0"></span>Meta<span class="sw" style="background:{ORANGE}"></span>Google Ads'
       f'<span style="margin-left:12px">* October = 1–12 Oct</span></div>')
body = f'''
<div class="tiles">
<div class="tile"><div class="l">Spent to 12 Oct</div><div class="v">$282,524</div><div class="d">94% of $300k · 78% of the year</div></div>
<div class="tile"><div class="l">Meta</div><div class="v">$180,767</div><div class="d">7,387 registrations · $24.5 each</div></div>
<div class="tile"><div class="l">Google Ads</div><div class="v">$101,500</div><div class="d">1,491 conversions · $68.1 each</div></div>
<div class="tile"><div class="l">Last full week</div><div class="v">$1,887</div><div class="d">Meta $11.6 / reg · Google $26.4 / conv</div></div>
<div class="tile"><div class="l">Left to year end</div><div class="v">$17,476</div><div class="d">≈ $1,529 a week · $37.5k to the $320k max</div></div>
<div class="tile"><div class="l">EMEA H1 (Tereza)</div><div class="v">43 SQLs</div><div class="d">954 MQLs · $2.1k per SQL · 66 days MQL→SQL</div></div>
</div>
<div class="cols c2">
<div><h2>Spend by month and channel</h2>{spend_chart()}{LEG}</div>
<div><h2>Cost per platform lead by month</h2>{cpl_chart()}
<div class="legend"><span class="sw" style="background:{BLUE};margin-left:0"></span>Meta: cost per website registration<span class="sw" style="background:{ORANGE}"></span>Google: cost per conversion (the agency's definition changed during the year)</div></div>
</div>
<div class="cols c2" style="margin-top:6px">
<ul class="list work"><li><b>Meta reads cheap</b>: $11–25 per registration most months, $11.6 last week after the September cuts.</li></ul>
<ul class="list flag"><li><b>"Lead" is the platform's word, not sales'.</b> Meta counts a "welcome" page view after a form; Google's conversion action was redefined four times. Neither is an MQL or an SQL. The next slides look at who those leads are.</li></ul>
</div>'''
pages.append(slide("Audit · spend and results", "What we spent and what the platforms call leads", body, 3,
                   "Sources: Meta Ads Manager and Google Ads exports, campaign × day; spend tracker. Google converted from EUR at 1.1177."))

# 4 ---------------------------------------------------------------- structure
meta_live = [("Geo:EMEA prospecting (CBO, 12 Jul)", "$3.3k", "295", "$11.2", tag("Live", "keep")),
             ("Geo:WW retargeting (CBO)", "$12.0k", "507", "$23.6", tag("Live", "keep")),
             ("Geo:US-California prospecting", "$6.6k", "222", "$29.6", tag("Live", "keep")),
             ("Geo:US-East-Coast prospecting", "$5.5k", "250", "$21.9", tag("Live", "keep")),
             ("Geo:USCA prospecting (17 Jun)", "$4.2k", "143", "$29.0", tag("Live", "keep")),
             ("Geo:US-Middle-South prospecting", "$3.2k", "124", "$26.1", tag("Live", "keep")),
             ("Geo:Middle-East prospecting", "$2.6k", "89", "$29.0", tag("Live", "keep")),
             ("Geo:Western-Europe prospecting", "$2.6k", "120", "$21.4", tag("Live", "keep")),
             ("Geo:USCA traffic (cold)", "$0.7k", "3", "$246", tag("Live", "keep")),
             ("Ended: EMEA ABO (Feb–Jul), EMEA test CBO, US-EastCoast, California test, EMEA retargeting, Geo:All welcome, CFA Amazon", "$135.7k", "5,626", "$24", tag("Ended", "done"))]
goog_live = [("Geo:NA non-brand Search (13 Aug)", "€5.2k", "119", "€44", tag("Live", "keep")),
             ("Geo:EMEA non-brand Search (13 Aug)", "€4.3k", "106", "€41", tag("Live", "keep")),
             ("Geo:US-SV coworking Search", "€1.1k", "45", "€25", tag("Live", "keep")),
             ("PNP_EMEA + PNP_US YouTube video views", "€5.9k", "1", "€4.2k", tag("Live", "keep")),
             ("Geo:NA PMax (8 Jun – 10 Sep)", "€3.1k", "288", "€11", tag("Paused", "done")),
             ("9 country / region Search campaigns Jan–Aug (EMEA, US, US-CA, UK, FR, IT, SA, US-South, US-East)", "€50.5k", "688", "€73", tag("Ended", "done")),
             ("5 US state Search (NY, FL, TX, NJ, AZ), Jan–May", "€13.1k", "42", "€312", tag("Ended", "done")),
             ("PMax Quiz EMEA + US (Jan–Apr)", "€1.7k", "168", "€10", tag("Ended", "done")),
             ("YouTube / Demand Gen reach (12 campaigns)", "€4.9k", "2", "–", tag("Ended", "done"))]
body = f'''
<div class="cols c2">
<div><h2>Meta – 9 campaigns live, 18 this year</h2>{tbl(["Campaign", ("Spend",), ("Regs",), ("CPL",), "Status"], [(E(a), (b,"num"), (c,"num"), (d,"num"), e) for a,b,c,d,e in meta_live], "small")}
<div class="note">All prospecting campaigns use the Leads objective and send people to website forms (no Instant Forms). Result = "website registration completed" (a custom conversion on the welcome page).</div></div>
<div><h2>Google – 5 campaigns live, 37 this year</h2>{tbl(["Campaign", ("Cost",), ("Conv.",), ("Per conv.",), "Status"], [(E(a), (b,"num"), (c,"num"), (d,"num"), e) for a,b,c,d,e in goog_live], "small")}
<div class="note">Non-brand Search is 81% of Google spend. No brand campaign since 14 Jan. Conversion goal switched to "HubSpot qualified leads only" on 14 Sep (15 leads at $190.69 that week).</div></div>
</div>
<div class="cols c2" style="margin-top:8px">
<div class="box red"><b>Why this structure under-delivers.</b> Meta needs ~50 optimisation events per ad set per week to leave the learning phase; our regional campaigns get 10–40. Splitting California out of USCA in January "hurt Meta" (agency, 19 Jan); the June split into US region CBOs was followed by a 70% CPL rise. On Google, 14 geo Search campaigns ran in H1: €312 per conversion in the 5 US states, €73 in the 9 country and region campaigns; the two consolidated campaigns since August cost €41–44.</div>
<div class="box green"><b>What the playbook recommends instead.</b> Meta: 3 campaigns maximum (prospecting, optional testing, warm), 1–2 broad ad sets, 8–15 distinct creatives each; separate ad sets by market only where cost per lead differs a lot. Google: 4–5 intent-based campaigns (brand, high intent, competitor, discovery, remarketing), exact/phrase first, broad and AI Max only once offline conversions flow.</div>
</div>'''
pages.append(slide("Audit · structure", "How the accounts are built today, against the 2026 structure", body, 4,
                   "Spend and leads 1 Jan – 12 Oct 2026 as reported by each platform. Google in EUR as billed."))

# 5 ---------------------------------------------------------------- Meta deep dive
meta_rows = [
    ("EMEA – multi-country (4 campaigns)", "$96.2k", "4,238", "$22.7", "1.27%", "The engine. The Feb ABO campaign did 2,238 regs at $32; the Jul CBO does them at $11 with 2.3% CTR."),
    ("US & Canada (USCA, 3 campaigns)", "$16.6k", "846", "$19.6", "1.54%", "Cheapest US market; split into 4 regional CBOs in June, each now too small to learn."),
    ("California (2)", "$18.1k", "695", "$26.1", "0.99%", "Lowest CTR; CPC $3.40 vs $1.24 in EMEA."),
    ("US East Coast (2)", "$21.2k", "600", "$35.3", "1.25%", "Most expensive region; Apr–Jun campaign at $45."),
    ("Worldwide (retargeting + Jan 'welcome' campaign)", "$13.5k", "667", "$20.3", "0.98%", "Retargeting spend tripled Jul–Sep (to $3k/month). Offer is the same content; should carry the demo / JTP ask."),
    ("US South & Central, Middle East, W. Europe (Jun–Jul)", "$8.4k", "333", "$25.2", "1.3–2.5%", "Middle East: 2.5% CTR, $0.36 CPC, $29 CPL."),
    ("FR_Alibaba (traffic, internal team) + USCA traffic", "$5.2k", "11", "$475", "1.5%", "Traffic objective: 130k link clicks, 11 registrations. Not lead gen."),
]
body = f'''
<div class="cols c32">
<div>{tbl(["Market / campaign group", ("Spend",), ("Regs",), ("CPL",), ("CTR",), "What it tells us"], [(E(a),(b,"num"),(c,"num"),(d,"num"),(e,"num"),E(f)) for a,b,c,d,e,f in meta_rows])}
<div class="note">Regs = "website registrations completed". Meta average 2026: $24.5, 1.38% CTR, $0.72 CPC (incl. traffic campaigns). Attribution changed in March 2026 (click-through only), so Jan–Feb CPLs are not like-for-like.</div></div>
<div>
<h2>Working</h2><ul class="list work">
<li>EMEA prospecting, July CBO: $11 per registration, 2.3% CTR, 144 regs in September.</li>
<li>Report-led creative: "Quantum Leap" (4,627 download contacts, 19% corporate) and "Spain's Grid Resilience" (1,585, 21% corporate) were the agency's top ads.</li>
<li>Post-cut efficiency: $1,174 → 101 regs last week ($11.6).</li></ul>
<h2>Not working</h2><ul class="list flag">
<li>Quality: of the leads Meta sends to HubSpot, 0.2% (downloads) and 1.4% (Contact us) get qualified by sales; 40% of Contact-us leads are disqualified.</li>
<li>7 prospecting campaigns for ≈$160/day in total: no ad set reaches 50 events a week.</li>
<li>Ads not aimed at a persona: nothing in the names or offers filters startups out; the "AICOI" ad took a large share of spend at high CPL (May).</li>
<li>Traffic objective campaigns ($5.2k, 11 regs).</li></ul>
</div></div>'''
pages.append(slide("Audit · Meta", "Meta: cheap registrations, mostly not the people we sell to", body, 5,
                   "Sources: Meta export; HubSpot ICP audit (paid social original source); agency weekly notes."))

# 6 ---------------------------------------------------------------- Google deep dive
goog_rows = [
    ("Non-brand Search, consolidated NA + EMEA (since 13 Aug)", "$10.7k", "225", "$47", "9.7%", "Best Search result of the year: €41–44 per conversion, $30 in October. Budget-limited since the 19 Sep cuts (€63/day)."),
    ("Non-brand Search by country, Jan–Aug (EMEA, US, FR, UK, IT, SA)", "$34.1k", "548", "$62", "9.6%", "EMEA $54, FR $59, IT $34, SA $38 — fine. UK $117 and US $74. Google-side CPL rose Apr–Jul as keywords were broadened, then cut."),
    ("Non-brand Search, US regions and states (CA, East, South, NY, FL, TX, NJ, AZ)", "$37.0k", "183", "$202", "1–7%", "CPCs of $10–21 in the states and 1 conversion every 2–3 weeks. 36% of Google spend for 12% of conversions."),
    ("Performance Max (NA Jun–Sep; Quiz EMEA/US Jan–Apr)", "$5.5k", "460", "$12", "3.0%", "Cheapest conversions on the account, which is exactly why the playbook warns about PMax on form fills: no sign they were ICP."),
    ("YouTube video views + Demand Gen (14 campaigns)", "$12.1k", "3", "$4.0k", "0.1–8%", "Branding paid from the lead-gen budget; the agency flagged it on 17 Aug. Two video-view campaigns still run at €10/day each."),
    ("Brand Search (to 14 Jan) · Coworking Search (US-SV)", "$0.9k · $1.2k", "28 · 45", "$34 · $28", "15% · 8%", "Brand has been off since 14 Jan. Coworking is a startup product: keep it out of the corporate lead-gen figures."),
]
body = f'''
<div class="cols c32">
<div>{tbl(["Campaign group", ("Spend",), ("Conv.",), ("Per conv.",), ("CTR",), "What it tells us"], [(E(a),(b,"num"),(c,"num"),(d,"num"),(e,"num"),E(f)) for a,b,c,d,e,f in goog_rows])}
<div class="note">USD at 1.1177. "Conversions" = the account's primary conversion actions: JTP form → welcome page → proxy event (Jul–Aug outage) → HubSpot qualified leads only (from ~15 Sep). Google's own search-term data was not in the exports; 51% of Google spend had no country label in the agency's reporting tool (24 Aug).</div></div>
<div>
<h2>Working</h2><ul class="list work">
<li>Two consolidated non-brand Search campaigns: 225 conversions at $47 in 9 weeks, 10% CTR.</li>
<li>Italy ($34), Middle East ($38), France ($59) when run as country campaigns: local terms convert.</li>
<li>Switching the goal to HubSpot-qualified leads (14 Sep) is the right direction, even if volume dropped.</li></ul>
<h2>Not working</h2><ul class="list flag">
<li>US region and state campaigns: $37.0k for 183 conversions.</li>
<li>Lead quality: paid search Contact-us leads 1.8% qualified, 23% disqualified; 2.6% from corporates with 10,000+ employees.</li>
<li>Video for views: $12.1k, 3 conversions.</li>
<li>No brand campaign, no competitor campaign, no negatives shared with sales' disqualification reasons.</li></ul>
</div></div>'''
pages.append(slide("Audit · Google Ads", "Google: Search works when consolidated, everything else was reach", body, 6,
                   "Sources: Google Ads export; agency logs (budgets, goal changes); HubSpot ICP audit (paid search original source)."))

# 7 ---------------------------------------------------------------- lead quality
jtp = [("Organic search (3,852)", .041), ("Organic social (367)", .035), ("Direct (3,757)", .028), ("Paid search (796)", .018), ("Paid social (665)", .014)]
dq = [("Paid social (665)", .405), ("Paid search (796)", .230), ("Organic social (367)", .150), ("Organic search (3,852)", .093), ("Direct (3,757)", .092)]
body = f'''
<div class="cols c3">
<div><h2>Contact-us leads qualified by sales, by source</h2>{hbar_chart(jtp, w=420, maxv=.05, fmt=lambda v: f"{v:.1%}", colors=[GREEN,GREEN,GREEN,ORANGE,BLUE], label_w=150)}
<div class="note">Share of contacts with Lead Status qualified / converted / SQL (Salesforce). Oct 2025 – Sep 2026.</div></div>
<div><h2>… and disqualified by sales</h2>{hbar_chart(dq, w=420, maxv=.45, fmt=lambda v: f"{v:.0%}", colors=[BLUE,ORANGE,SLATE,SLATE,SLATE], label_w=150)}
<div class="note">Paid social sends the most leads sales throws away: 4× the organic rate.</div></div>
<div><h2>Content downloads: paid social is the firehose</h2>
<div class="tiles" style="grid-template-columns:1fr 1fr;margin:0 0 6px">
<div class="tile"><div class="l">From paid social</div><div class="v">8,214</div><div class="d">61% of all download contacts</div></div>
<div class="tile"><div class="l">Qualified by sales</div><div class="v red">0.2%</div><div class="d">&lt;5 with a deal · 0 customers</div></div>
<div class="tile"><div class="l">Corporate 10,000+</div><div class="v">5.5%</div><div class="d">449 contacts · 355 strict ICP incl. government</div></div>
<div class="tile"><div class="l">Profile "Other / job seeker / student"</div><div class="v">42%</div><div class="d">of all download contacts</div></div>
</div></div>
</div>
<div class="cols c2" style="margin-top:4px">
<div class="box red"><b>The root cause is the signal, not the channels.</b> Both platforms are told that a form fill is the win, so they find the people most likely to fill forms: startups (79% of Contact-us contacts) and students. Corporates with 10,000+ employees are 2% of Contact-us contacts and 6% of downloaders, yet they are the ones who qualify (18%) and get deals (5%). Strict ICP corporates: 24 Contact-us contacts, 46% qualified.</div>
<div class="box green"><b>What this means for the plan.</b> Every structural and creative change on the next slides is in service of one switch: optimise to an ICP-qualified lead instead of a form fill. Before that signal exists, the cheapest fix is a qualifying form plus a thank-you page that only ICP-fit leads reach (the platform conversion fires there). The second fix is making job title and company size mandatory, so quality can be measured at all.</div>
</div>'''
pages.append(slide("Audit · lead quality", "Who the paid leads are: volume from paid social, quality from search", body, 7,
                   "Source: HubSpot read-only audit (PNP_ICP_vs_Conversions), unique contacts, counts under 5 shown as <5. Lifecycle stage not used (95% are 'SQL' in HubSpot)."))

# 8 ---------------------------------------------------------------- Andromeda
body = f'''
<div class="cols c2">
<div>
<p><b>Andromeda</b> is the retrieval stage of Meta's ad system: the step that narrows tens of millions of eligible ads to a few thousand candidates per person, before ranking and the auction. Meta described it on 2 Dec 2024 (10,000× more model complexity, +8% ad quality on tested segments); it was fully global by October 2025, with the GEM ranking model on top (Nov 2025) and Meta's first generative retrieval model in July 2026 (+15.7% conversions in Q2, per Meta).</p>
{tbl(["", "Before (to 2024)", "After Andromeda (2025–26)"], [
 ("Who sees the ad", "Interests, lookalikes and exclusions filtered the audience first", "The system reads the creative and pairs it with the likeliest person; targeting inputs are suggestions"),
 ("Structure", "Many ad sets, one per audience or geography", "One campaign per objective, 1–3 broad ad sets"),
 ("Ads per ad set", "Meta said max 6", "Guidance removed; 8–15 genuinely different concepts"),
 ("What counts as different", "Any variation", "Same look or same opening hook = the same ad (creative diversity label since Aug 2026)"),
 ("Creative fatigue", "6+ weeks", "2–3 weeks; weekly refresh"),
 ("Your job", "Targeting and bidding", "Creative, offer and the conversion signal you send back")], "small")}
<div class="note">Meta's own test: one ad set with 25 diverse creatives beat five ad sets × five creatives by 17% more conversions at 16% lower cost. Source: playbook (Segwise, Ad Advisor, Atria, Chatterbuzz, Relevant Audience, Jon Loomer).</div>
</div>
<div>
<h2>Why it matters for Plug and Play</h2>
<ul class="list flag">
<li><b>Our Meta account is built the old way</b>: 7 prospecting campaigns by geography, few ads each, each ad set far below the 50 events/week needed to learn. That is the pattern Andromeda punishes.</li>
<li><b>Our ads don't say who they are for.</b> Since the creative now does the targeting, "for innovation leaders at 10,000+ employee companies" has to be in the first line and the visual; otherwise the system keeps finding startups.</li>
<li><b>Reports as the only creative concept</b> means Meta treats our ads as near-identical and rotates between the same people.</li>
</ul>
<h2>Other 2026 Meta changes we have to price in</h2>
<ul class="list blue">
<li><b>March 2026 attribution</b>: click-through conversions only count after a link click; CPL baselines before March are not comparable.</li>
<li><b>Location fees since 1 Jul</b>: +3% Spain, France and Italy, +2% UK, on top of budget.</li>
<li><b>Q4 CPM pressure</b>: Meta's price per ad +12% year on year in Q2.</li>
<li><b>New controls</b>: Sequenced Events (lead → booked call) and "qualified leads" optimisation for website leads (6 Oct); placement exclusions moving to account level; automatic pixel events and an AI assistant that can change budgets — keep approvals human.</li>
</ul>
</div></div>'''
pages.append(slide("Context · Meta", "Andromeda: creative is the targeting now, and our account was built for the old system", body, 8,
                   "All platform facts from the playbook's dated sources; our account facts from the Meta export and agency notes."))

# 9 ---------------------------------------------------------------- Search 2026
body = f'''
<div class="cols c2">
<div>
<h2>What changed on Google Search in 2026</h2>
{tbl(["Change", "What to do at PnP"], [
 ("<b>AI Max is switched on for you</b> (1 Sep): campaigns with auto-created assets or campaign-level broad match were upgraded automatically; DSA migrates Feb 2027", "Audit both Search campaigns now; keep AI Max off until offline conversions flow (the agency planned to launch it on 31 Aug)"),
 ("<b>Exact and phrase match now serve in AI Mode</b> for direct-intent queries (9 Sep)", "We don't need AI Max to appear in AI answers for high-intent corporate-innovation terms"),
 ("<b>Enhanced Conversions for Leads + Data Manager</b> (offline import moved 15 Jun); uploads after 7 days are ignored by attribution", "HubSpot → Google daily: MQL, SQL, opportunity, won. Store GCLID on the contact"),
 ("<b>Smart Bidding needs ~30 conversions/month per campaign</b>; value-based bidding fails on low volume", "Max conversions → tCPA on qualified leads once each campaign has 30+/month; no value bidding yet"),
 ("<b>PMax for B2B works only with ~50 qualified conversions/month and offline data</b>", "Keep PMax paused; re-test with the qualified goal, never on form fills (our PMax got $12 'conversions')"),
 ("<b>Business Agent for Leads, lead intent scores</b> (US beta)", "Watch; publish ICP-fit, process and FAQ pages so the agent has material when it reaches the EU"),
 ("<b>Ad language follows the search term</b> (Sep)", "Separate FR / IT / DE / ES ad groups and RSAs; local content beat generic 3:1 on CPL at PnP")], "small")}
</div>
<div>
<h2>Search in the playbook's structure</h2>
{tbl(["Campaign", "Match", "Bidding", "Share"], [
 ("1. Brand", "Exact (+phrase); 'login', 'jobs' negative", "Max conv. / tCPA", "10–15%"),
 ("2. Non-brand high intent (corporate innovation platform, open innovation programme, startup scouting partner, innovation lab…)", "Phrase + exact", "Max conv. → tCPA on qualified lead", "40–50%"),
 ("3. Competitor (alternatives, vs, pricing)", "Exact + phrase", "tCPA, CPC caps", "10–20%"),
 ("4. Problem / discovery ('how to run a corporate venture programme')", "Broad or AI Max only with offline conversions", "Value-based later", "15–20%"),
 ("5. Remarketing / Demand Gen", "Site visitors, Customer Match", "Max conv.", "5–10%")], "small")}
<div class="box pale" style="margin-top:8px"><b>RSA rules that filter leads for free:</b> 10–15 headlines, 2 qualifier headlines ("For corporates with 10,000+ employees", "Innovation programmes for enterprises"), 2 proof headlines (named corporate partners), offer as headline, partial pinning. Negatives from sales' disqualification reasons every week: jobs, students, startup funding, accelerator applications (startups have their own JTP path).</div>
<div class="note">Google's own number: broad match + Smart Bidding ≈ +20% conversions, but B2B specialists see 50–70% of broad spend on non-converting searches without offline data.</div>
</div></div>'''
pages.append(slide("Context · Google Search", "Search in 2026: intent capture, with the AI switches off until the CRM talks back", body, 9,
                   "Source: playbook (Google Ads Help, Common Thread, GrowthSpree, Directive, Lunio, TripleDart); PnP facts from the Google export and agency logs."))

# 10 ---------------------------------------------------------------- ChatGPT
body = f'''
<div class="cols c2">
<div>
<h2>Our 10-day test (23 Sep – 2 Oct)</h2>
<div class="tiles" style="grid-template-columns:repeat(4,1fr);margin:0 0 8px">
<div class="tile"><div class="l">Spend</div><div class="v">€229.56</div><div class="d">$257</div></div>
<div class="tile"><div class="l">Impressions</div><div class="v">4,021</div><div class="d"></div></div>
<div class="tile"><div class="l">Clicks</div><div class="v">43</div><div class="d">1.07% CTR · €5.34 CPC</div></div>
<div class="tile"><div class="l">Conversions</div><div class="v red">0</div><div class="d">as reported by OpenAI</div></div>
</div>
<p>This matches the public B2B tests in the playbook: cheap-ish clicks, real reach, no qualified leads yet (Windmill: $1,470, 0 conversions; Workshop Digital: $2,319, 0 MQLs; another test: 336 clicks → 146 companies, 5 in ICP). One founder saw OpenAI count 57 clicks where GA4 showed under 20 visits.</p>
<h2>Platform facts that limit us</h2>
<ul class="list flag">
<li>Only <b>Free and Go</b> users see ads; Plus, Pro, Business and Enterprise users (a good part of our ICP) are unreachable.</li>
<li><b>No personalised ads in the EEA</b> at launch: matching is on the conversation plus language and rough location; custom audiences unusable for European campaigns.</li>
<li>No keywords, match types, search-term report or schedules: targeting is written as <b>context hints</b> (buyer situations).</li>
</ul></div>
<div>
<h2>How to run the next test (Q1 2027, 60 days)</h2>
<ol class="steps">
<li><b>Gate:</b> OpenAI Pixel + Conversions API live, with the event fired only after HubSpot accepts the lead (ICP-fit), and GA4 reconciliation from day one.</li>
<li><b>Budget:</b> €1,500–2,000 a month, 5–8% of paid media; decide the ceiling first (e.g. cost per qualified lead must stay within 1.5× Google Search).</li>
<li><b>Structure:</b> 2 campaigns (EMEA-EN, US-EN; Spanish later), 3–5 ad groups each by buyer problem: "setting up a corporate innovation programme", "finding startups for a pilot", "benchmarking our innovation function", "open innovation partner evaluation".</li>
<li><b>Context hints</b> as buyer situations, 5–10 per group: "Head of Innovation at a 10,000+ employee manufacturer comparing ways to source and pilot startups" — not a keyword list.</li>
<li><b>Offer:</b> research-stage, not a demo: the Company Performance Report, the Enterprise AI playbook, an innovation maturity assessment. 3–6 literal, benefit-led ads per group.</li>
<li><b>Verdict after 60 days</b> on cost per qualified lead vs Search; otherwise keep as a €300/month awareness line and retest when Sponsored Agents and conversion bidding mature.</li>
</ol>
<div class="note">Also in the plan: HubSpot's native ChatGPT Ads integration (16 Sep) if available on our account; automatic copy localisation for ES/FR/IT.</div>
</div></div>'''
pages.append(slide("Context · ChatGPT Ads", "ChatGPT Ads: worth one disciplined test, not a lead engine yet", body, 10,
                   "Sources: OpenAI Ads export (campaigns_1.csv); playbook (OpenAI Help, Windmill Strategy, Workshop Digital, BCC Interactive, Factors.ai)."))

# 11 ---------------------------------------------------------------- creatives
body = f'''
<div class="cols c2">
<div>
<h2>What I can see from the data</h2>
<ul class="list flag">
<li><b>One concept: the report cover.</b> The two top Meta ads were research downloads (Quantum Leap, Spain's Grid Resilience). Good as cold offers, but 81% of their downloaders are not corporate, and the ads give Meta no persona to aim at.</li>
<li><b>No qualifier in the creative.</b> Nothing says "for corporates" or "for innovation leaders"; startups self-select in.</li>
<li><b>Two-month creative cycles.</b> Agency notes mention new ads in Jul and "case-study statics" on 8 Oct; Andromeda-era fatigue is 2–3 weeks.</li>
<li><b>Formats we never ran:</b> talking-head video (in the 60-day plan), customer story, comparison, native-post style, partnership ads.</li>
</ul>
<div class="box pale"><b>What I could not audit from here:</b> the ads themselves (the agency's Creative Reports were not shared; I have no Ads Manager preview access yet). First task with Thiago before 30 Oct: export the ad-level report with creative names, spend and registrations, and the Meta Ad Library links.</div>
</div>
<div>
<h2>The creative system to build (per region, 8–12 concepts live)</h2>
{tbl(["Concept", "Persona called out", "Format", "Offer / CTA"], [
 ("\"Your innovation programme runs on pilots. Here is how 20+ corporates source them.\"", "Head of Innovation, 10,000+ employees", "Founder / regional MD talking head, 45–60 s, captions", "Corporate innovation guide"),
 ("Named corporate case (Mitsubishi Electric × Kamet AI, SMBC…)", "R&D / CDO", "Customer story static + 15 s cut", "Case study pack"),
 ("Before / after: 'scouting in spreadsheets vs a vetted startup pipeline'", "Innovation manager", "Comparison static", "Book a 20-min scouting call"),
 ("Number-led: '2025 Company Performance Report: X pilots, Y countries'", "C-level", "Report cover + 3 takeaways", "Download (gated, ICP form)"),
 ("Government / public sector: 'How ministries run innovation programmes with us'", "Government innovation lead", "Native post style", "Programme brief"),
 ("Local-language versions for FR, IT, DE, ES (local beat generic 3:1 at PnP)", "Same personas, local MD on camera", "Talking head + static", "Local report")], "small")}
<div class="note">Rules: change at least two of persona / angle / format / hook between concepts; one problem, one promise, one CTA; 9:16 and 4:5 of each; headline = the offer; check Meta's creative diversity label (no ad set at Low); replace the bottom 2–3 ads every two weeks; build new concepts as 3-2-2 flexible ads in their own ad set inside the main CBO. Label any AI-generated photoreal asset (EU AI Act, 2 Dec).</div>
</div></div>'''
pages.append(slide("Audit · creatives", "Creatives: one concept, no persona, slow refresh", body, 11,
                   "Sources: agency weekly notes (top ads, launches); HubSpot ICP audit (downloaders by asset); playbook creative section."))

# 12 ---------------------------------------------------------------- landing pages & funnel
body = f'''
<h2>The funnel as it works today, and where it leaks</h2>
<div class="flow">
<div class="st"><h3>Ad</h3>Report or JTP ad, no persona call-out; Meta and Google both optimise to the welcome page.</div><div class="arrow">→</div>
<div class="st bad"><h3>Landing page / form</h3>Same page for startups and corporates; job title empty on 67–83% of contacts; welcome-page templates broke in Jul–Aug and took tracking down for 4 weeks.</div><div class="arrow">→</div>
<div class="st bad"><h3>Thank-you / welcome page</h3>Fires the platform conversion for <b>everyone</b> who submits: startup founder, student, job seeker, corporate CDO alike.</div><div class="arrow">→</div>
<div class="st bad"><h3>HubSpot</h3>95% of contacts are "SQL" by lifecycle stage, so HubSpot stages can't be used as a signal; Persona and Decision-maker-fit fields empty; HubSpot vs platform lead counts differ by up to 7×.</div><div class="arrow">→</div>
<div class="st"><h3>Salesforce</h3>Lead Status is the only usable quality field (qualified / disqualified); MQL → SQL takes 66 days.</div><div class="arrow">→</div>
<div class="st bad"><h3>Back to the platforms</h3>Nothing. No CAPI for CRM, no offline conversion import. The platforms never learn which leads were good.</div>
</div>
<div class="cols c2" style="margin-top:12px">
<div><h2>Landing page and form rules (from the playbook)</h2>
<ul class="list work">
<li><b>Two paths</b>: a corporate page (ICP wording, named partners, 2-step form: work email + company, then role and company size, then a calendar) and the existing startup JTP path. Separate forms, separate events.</li>
<li><b>Required fields that filter</b>: job title as a dropdown of roles; company size bands; work email only. Turn off autofill on those fields if we use Instant Forms later.</li>
<li><b>Message match</b>: H1 repeats the ad's promise; proof (logos, one result number) next to the form; form above the fold on a 390 px screen; one page per Google ad-group theme.</li>
<li><b>Tracking in the page</b>: capture gclid, fbclid, UTMs and an event ID in hidden fields; fire the lead event from Pixel + Conversions API with the same event ID; consent mode v2.</li>
</ul></div>
<div><h2>The qualified thank-you page: the fastest quality fix</h2>
<ul class="list blue">
<li>After the form, route by answers: ICP-fit (corporate 10,000+ or government, target role) → <b>/thank-you-qualified</b>, where the Meta Lead and Google conversion fire. Everyone else → a resources page with <b>no</b> event.</li>
<li>Both platforms then optimise to ICP leads within days, without waiting for the CRM integration. This is the move Ben Heath paid $235k for in Hormozi's playbook, and it costs us a form rule and one page.</li>
<li>Next step (weeks, not days): HubSpot → Meta Conversions API for CRM (free via Make until Feb 2028) and HubSpot → Google Enhanced Conversions for Leads, sending MQL / SQL / opportunity / won with the click IDs. Meta's 6 Oct "qualified leads" goal and Sequenced Events (lead → booked call) then work for website leads too.</li>
</ul>
<div class="box pale">I have not been able to load the live pages from this environment; this is the checklist I will run page by page with Aly and Rosa (landing pages) next week.</div></div>
</div>'''
pages.append(slide("Audit · landing pages and tracking", "Tracking: the conversion fires for everyone, so the platforms learn nothing", body, 12,
                   "Sources: HubSpot ICP audit; agency notes (3 Aug: 'client web team to fix welcome landing-page templates'; 27 Apr: HubSpot 143 vs 20 tracked); playbook."))

# 13 ---------------------------------------------------------------- new structure
body = f'''
<div class="cols c3">
<div class="box" style="border-top:4px solid {BLUE}"><h2 style="color:{BLUE}">Meta · 3 campaigns (now 9)</h2>
{tbl(["Campaign", "Setup"], [
 ("<b>1. Prospecting EMEA</b> (50% of Meta)", "Leads objective, CBO, 1 broad Advantage+ ad set with ICP suggestions (job-title interests, customer list as signal); countries: UK, FR, DE, ES, IT + rest of EMEA; Middle East as a 2nd ad set only if CPL differs a lot. 8–12 concepts; local-language ad set for FR/IT/DE/ES."),
 ("<b>2. Prospecting Americas</b> (30%)", "Same build, US + Canada in one ad set (state splits ended); control ad set of proven winners + one ad set per new concept (3-2-2 ads)."),
 ("<b>3. Warm</b> (15–25%)", "Site visitors 30–180 d, video viewers 50%+, downloaders who are ICP (CRM list), form openers; offer = named case studies and a 20-min call, not another report. Exclude customers, open opportunities, employees."),
 ("Conversion", "Website, event = qualified thank-you page now; Meta 'qualified leads' / Conversion Leads via CAPI for CRM once stages flow. Cost cap once CPL is stable.")], "small")}</div>
<div class="box" style="border-top:4px solid {ORANGE}"><h2 style="color:{ORANGE}">Google · 5 campaigns (now 5, different ones)</h2>
{tbl(["Campaign", "Setup"], [
 ("<b>1. Brand</b> (10%)", "Exact; negatives: jobs, login, careers. Relaunch (off since 14 Jan)."),
 ("<b>2. Non-brand EMEA</b> (35%)", "Keep the Aug campaign; rebuild ad groups by intent (corporate innovation programme, open innovation, startup scouting, innovation lab/CoE, government innovation); phrase + exact; FR/IT/DE/ES ad groups with local RSAs and pages."),
 ("<b>3. Non-brand Americas</b> (30%)", "Same intents, US + Canada; no state campaigns."),
 ("<b>4. Competitor</b> (10%, test)", "2–3 corporate-innovation competitors, honest comparison pages, CPC caps."),
 ("<b>5. Discovery</b> (later)", "Broad / AI Max as a 50/50 experiment only after SQL import runs; PMax re-test with the qualified goal at 30–50 qualified/month."),
 ("Everything", "Presence targeting, Search only, auto-apply off, 60–90 day window, universal negatives EN + local, observation audiences, 15-headline RSAs with qualifier lines, sitelinks to case studies / programmes / contact.")], "small")}</div>
<div class="box" style="border-top:4px solid {AQUA}"><h2 style="color:{AQUA}">ChatGPT Ads · 1 test</h2>
{tbl(["Item", "Setup"], [("Timing", "Q1 2027, 60 days, after the CRM-verified event exists"), ("Size", "€1.5–2k / month"), ("Structure", "2 campaigns × 3–5 problem ad groups, research-stage offers"), ("Keep if", "cost per qualified lead ≤ 1.5× Google Search")], "small")}
<h2 style="margin-top:10px">Not in scope</h2>
<ul class="list"><li><b>LinkedIn</b>: off for now (too expensive for the leads we get on Search and Meta; manager's decision). Revisit for company-list targeting in 2027 with a small test.</li>
<li><b>YouTube / Demand Gen for views</b>: out of the lead-gen budget. If brand reach is wanted, fund it separately and measure with the Branded Search conversion type.</li>
<li><b>Coworking (US-SV)</b>: a startup product; keep, but report it outside the corporate lead-gen numbers.</li></ul></div>
</div>
<div class="box pale" style="margin-top:8px"><b>Budget split to start 2027</b> (playbook template for a €10–25k/month budget, adapted to our history): Google Search 45–50% · Meta 40% · ChatGPT test 5–10% · reserve 5% for Demand Gen / PMax once offline data qualifies. Rebalance 10–20% a month toward the lowest cost per <i>qualified</i> lead, never below 20% on Meta (it creates the demand Search captures). Q4 2026: hold ≈ $1.5–1.9k/week, Meta 60% / Google 40%, with the YouTube €20/day moved into Search.</div>'''
pages.append(slide("Proposal · structure", "The structure I propose: fewer, bigger learning units, aimed at the ICP", body, 13,
                   "Shares are of each platform's budget. The structure follows the playbook's recommended B2B builds and keeps PnP's EMEA / Americas split."))

# 14 ---------------------------------------------------------------- campaign decisions
dec = [
    ("Meta", "Geo:EMEA prospecting CBO (Jul)", "$11 CPL, 2.3% CTR, 144 regs in Sep", tag("Keep + optimise", "keep"), "Becomes Prospecting EMEA: add 8–12 concepts, ICP suggestions, qualified thank-you event, local ad sets."),
    ("Meta", "Geo:WW retargeting", "$23.6 CPL, spend tripled Jul–Sep", tag("Update", "upd"), "Becomes Warm: swap report offers for case studies + call; add CRM ICP lists; cap at 20% of Meta."),
    ("Meta", "US-California, US-East-Coast, US-Middle-South, USCA prospecting", "$22–30 CPL each, 10–40 regs/week each", tag("Update", "upd"), "Merge into one Prospecting Americas CBO (keep the best ads); one ad set, state-level value rules if CRM shows differences."),
    ("Meta", "Middle-East, Western-Europe prospecting", "$29 / $21 CPL, small", tag("Update", "upd"), "Fold into Prospecting EMEA as ad sets (Middle East keeps its own creative)."),
    ("Meta", "Geo:USCA traffic (cold)", "$737, 3 registrations", tag("Pause", "pause"), "Traffic objective buys clicks, not leads."),
    ("Meta", "FR_Alibaba", "Ended 5 Oct, internal team", tag("Confirm", "done"), "Confirm whether it belongs in this budget; keep out of the lead-gen reporting."),
    ("Google", "Geo:NA non-brand Search", "€44/conv, budget-limited", tag("Keep + optimise", "keep"), "Rebuild ad groups by intent; add qualifier headlines; raise budget from €30/day once the qualified goal has data."),
    ("Google", "Geo:EMEA non-brand Search", "€41/conv, €30 in Oct", tag("Keep + optimise", "keep"), "Same, plus FR / IT / DE / ES ad groups and pages; tCPA €45 only after 30 qualified/month."),
    ("Google", "PNP_EMEA + PNP_US YouTube video views", "€5.9k, 1 conversion", tag("Pause", "pause"), "€20/day back into Search. Fund brand video separately if wanted."),
    ("Google", "Geo:NA PMax (paused)", "€11/conv, quality unknown", tag("Keep paused", "pause"), "Re-test in 2027 with the qualified goal and CRM audience signals, 30–50 qualified/month gate."),
    ("Google", "US state and US-region Search (ended)", "€227–614 per conversion", tag("Don't revive", "pause"), "US demand is covered by the Americas campaign; regions and states were 36% of spend for 12% of conversions."),
    ("Google", "Brand Search", "Off since 14 Jan", tag("Relaunch", "test"), "Exact match, small budget, protects branded demand and gives a clean baseline."),
    ("Google", "Competitor campaign", "Never run", tag("Test", "test"), "2–3 names, comparison pages, 10% of Google."),
    ("Google", "US-SV coworking Search", "€25/conv, 45 conv", tag("Keep (separate)", "keep"), "Startup product; report outside the corporate numbers."),
    ("ChatGPT", "Test 1", "€230, 43 clicks, 0 conversions", tag("Retest Q1", "test"), "60-day test with CRM-verified events, buyer-situation hints, research offers."),
]
body = tbl(["Channel", "Campaign", "Evidence (2026)", "Decision", "What changes"], [(a, E(b), E(c), d, E(e)) for a, b, c, d, e in dec], "small") + \
    f'<div class="note" style="margin-top:6px">Sequence: pauses and the thank-you page first (no extra budget), then the Meta merge and Google ad-group rebuild in one change window each (not during the first 7 days of a learning phase), then the signal integrations.</div>'
pages.append(slide("Proposal · campaign by campaign", "What to optimise, update, pause and test", body, 14,
                   "Evidence from the platform exports to 12 Oct 2026 and the agency logs."))

# 15 ---------------------------------------------------------------- measurement
body = f'''
<div class="cols c2">
<div><h2>The signal we send back, and what we measure</h2>
{tbl(["Stage", "Definition at PnP", "Sent to Meta / Google", "Use"], [
 ("Lead", "Any form submit", "Secondary only", "Volume check"),
 ("<b>ICP lead</b>", "Corporate 10,000+ employees (or government) and target role, from the form fields; same day", "<b>Yes – primary optimisation event</b> (thank-you page now, CAPI for CRM / Enhanced Conversions next)", "Bidding and the −20% KPI"),
 ("MQL", "HubSpot MQL (scoring to be fixed; 'seems off' since January)", "Yes, value 3×", "Weekly report"),
 ("SQL / meeting", "Salesforce Lead Status qualified; 66 days today", "Yes, value 10× (reporting; too slow to bid on alone)", "Cost per SQL, the real KPI"),
 ("Opportunity / won", "SFDC", "Yes, with deal value", "Pipeline : spend")], "small")}
<div class="box pale" style="margin-top:8px"><b>Why a fast proxy:</b> Meta needs the optimised stage within 28 days and at 1–40% of leads; Google attribution ignores uploads older than 7 days. SQL (66 days) can't be the bidding signal; the same-day ICP lead can.</div></div>
<div><h2>Cadence and KPIs</h2>
{tbl(["When", "What"], [
 ("Daily (10 min)", "Spend pacing, broken tracking, disapproved ads, CPL spikes; search terms during any AI Max / broad test"),
 ("Monday (the tracker + this)", "Spend vs budget; leads, ICP leads, cost per ICP lead by campaign; pause losers; launch the week's creative batch; negatives from sales' disqualification reasons"),
 ("Every 2 weeks", "Lead-quality review with sales: 20 random leads per platform scored; MQL fit score check"),
 ("Monthly", "Budget rebalance on cost per SQL and pipeline; concept review (which personas and angles win); leadership summary"),
 ("Quarterly", "Offer refresh, ChatGPT retest, incrementality once spend passes ≈€10k/month per platform")], "small")}
<div class="box green" style="margin-top:8px"><b>KPIs for the end of 2026 / 2027</b>: cost per ICP lead (new, replaces CPL), ICP leads per week by channel, cost per SQL vs the $2.1k H1 baseline, MQLs from paid search +15% counted as corporate MQLs, Meta −20% on cost per <i>qualified</i> lead.</div>
<div class="note">Reporting stays in the weekly tracker plus one HubSpot view by original source and campaign UTM (read-only). All contact-level work stays aggregated (GDPR).</div></div>
</div>'''
pages.append(slide("Proposal · measurement", "Measurement: one qualified signal, one weekly rhythm", body, 15,
                   "Source: playbook (Meta Conversions API for CRM docs, Google Ads Help, Prose Media); PnP numbers from the H1 deck and HubSpot audit."))

# 16 ---------------------------------------------------------------- roadmap
body = f'''
<div class="cols c3">
<div class="box"><div class="pill">Days 1–30</div><b>Foundations · Oct 15 – Nov 15</b><ul>
<li>Thiago handover: ad-level creative report, Ad Library links, location strategy, logs, Ads Manager access.</li>
<li>Pause USCA traffic and the two YouTube view campaigns; move €20/day to Search.</li>
<li>Define the ICP lead with Raúl and sales; make job title (dropdown) and company size required on JTP and download forms (with Aly / Rosa).</li>
<li>Qualified thank-you page live; Meta and Google conversions moved to it; gclid / fbclid / UTM stored in HubSpot.</li>
<li>Audit both Search campaigns for AI Max auto-upgrade; brief the first 8 Meta concepts (2 talking heads).</li></ul>
<div class="gate">Gate: one test lead tracked end to end from ad to Salesforce, and ICP leads counted in HubSpot.</div></div>
<div class="box"><div class="pill">Days 31–60</div><b>Rebuild · Nov 16 – Dec 15</b><ul>
<li>Meta: merge the 4 US campaigns into Prospecting Americas; fold Middle East and Western Europe into EMEA; relaunch Warm with case-study offers. No edits for 7 days after.</li>
<li>Google: ad groups by intent, 15-headline RSAs with qualifier lines, FR/IT/DE/ES groups, brand relaunch, negatives list EN + local.</li>
<li>HubSpot → Meta CAPI for CRM (Make) and → Google Enhanced Conversions for Leads: daily uploads of ICP lead, MQL, SQL.</li>
<li>Weekly creative batches: 3–5 concepts, 2–3 hooks each; retire bottom ads every two weeks.</li></ul>
<div class="gate">Gate: 30+ ICP leads per month per platform before any tCPA / qualified-leads bidding switch.</div></div>
<div class="box"><div class="pill">Days 61–90</div><b>Optimise and test · Dec 16 – Jan 31</b><ul>
<li>Switch Meta to "qualified leads" / Conversion Leads and Google to tCPA on the ICP lead where the gate is met.</li>
<li>Competitor campaign; Advantage+ Leads split test vs the manual build, judged on cost per SQL.</li>
<li>ChatGPT Ads 60-day test (CRM-verified event).</li>
<li>2027 plan: budget by channel on cost per ICP lead; Demand Gen / PMax only if 30–50 qualified a month; LinkedIn retest decision.</li>
<li>First quarterly review: what worked, what didn't, what's next.</li></ul>
<div class="gate">Gate: cost per SQL on target before scaling (+20% every 3–4 days, cost cap on).</div></div>
</div>
<div class="cols c2" style="margin-top:10px">
<div class="box red"><h3>Risks</h3><ul><li>Raw CPL rises when we filter: say it before it happens; the KPI is cost per ICP lead.</li><li>Fewer campaigns = fewer "lines" in reporting; the By-location view in the tracker still breaks results down by market.</li><li>Q4 CPMs +10–15% and the 3% EU location fees.</li><li>Volume: with ≈$1.5k/week left this year, the rebuild's results show in January, not December.</li></ul></div>
<div class="box green"><h3>What I need</h3><ul><li>Decision on the ICP-lead definition and on who owns form changes (web team).</li><li>Meta Ads Manager access via Tereza; Salesforce read access for lead status by campaign.</li><li>One hour with sales every two weeks for the lead review.</li><li>Confirmation: FR_Alibaba and ChatGPT in the $300k; 2027 budget envelope; LinkedIn stays off.</li></ul></div>
</div>'''
pages.append(slide("Proposal · 90-day plan", "The next 90 days, with gates", body, 16,
                   "Follows the playbook's 90-day roadmap (foundations → launch → optimise → scale) adapted to PnP's live accounts and remaining 2026 budget."))

# 17 ---------------------------------------------------------------- sources
body = f'''
<div class="cols c2">
<div><h2>Data used</h2><ul class="list">
<li><b>Platform exports</b>: Meta Ads Manager ('Plug and Play Tech Center – Dollars', USD) and Google Ads (EUR, converted at 1.1177), campaign × day, 1 Jan – 12 Oct 2026. OpenAI Ads campaign export.</li>
<li><b>HubSpot ICP audit</b> (read-only, 8 Oct 2026): JTP Contact-us and content-download contacts, 1 Oct 2025 – 30 Sep 2026; outcome = Salesforce Lead Status; aggregates only, counts under 5 shown as &lt;5.</li>
<li><b>Agency weekly reports</b> (Notion, W/C 29 Dec 2025 – 5 Oct 2026), copied as written: actions, targets, budget logs, lead definitions.</li>
<li><b>EMEA H1 2026 deck</b> (Tereza): MQLs, SQLs, cost per SQL, MQL → SQL time.</li>
<li><b>Spend tracker</b> (PNP_Paid_Media_Spend_Tracker_2026): budget status and pace.</li></ul>
<h2>Definitions</h2><ul class="list">
<li><b>Meta registration</b> = "website registrations completed" (custom conversion on the welcome page). <b>Google conversion</b> = the account's primary conversion action at the time (changed 4 times in 2026).</li>
<li><b>ICP</b> (Buyer Persona 2024): corporates with 10,000+ employees and $100M+ revenue, Head of Innovation / R&amp;D / CDO / C-level, plus governments; startup founders as the secondary group.</li>
<li><b>CPL</b> in this deck = platform cost per platform lead. <b>Cost per ICP lead</b> and <b>cost per SQL</b> are the proposed KPIs.</li></ul></div>
<div><h2>Strategy sources (via the playbook)</h2><ul class="list">
<li>Meta: Meta Engineering (Andromeda, GEM), Meta developer docs (Conversions API for CRM), Jon Loomer, Ben Heath, Professor Charley T, Nick Theriot, Dara Denney, Chatterbuzz, Relevant Audience, SaaS Hero, Flighted, Sotros, Aurelius Media.</li>
<li>Google: Google Ads Help and Ginny Marvin, Common Thread, GrowthSpree, Directive, TripleDart, Lunio B2B panel, Optmyzr (via Webtonic), Surfside PPC, Jyll Saskin Gales (Inside Google Ads).</li>
<li>ChatGPT Ads: OpenAI Help Center and announcements, Windmill Strategy, Workshop Digital, BCC Interactive, Factors.ai, Motainment, Just Global.</li>
<li>Regulation: EU AI Act Article 50 (Usercentrics, Ropes &amp; Gray, s360).</li></ul>
<div class="box pale" style="margin-top:8px"><b>Caveats.</b> Ad-level creatives, search terms, audiences and the live landing pages were not available to me for this audit; the creative and landing-page sections are based on the agency's notes, the HubSpot data and the playbook's rules, and will be completed in the handover with Thiago and with Aly / Rosa. Platform CPLs before March 2026 are not comparable with later months (Meta attribution change). The 2027 budget is not set; splits are percentages.</div></div>
</div>'''
pages.append(slide("Appendix", "Sources, definitions and caveats", body, 17))

html_out = f"<!doctype html><html><head><meta charset='utf-8'><title>Paid media audit and strategy proposal</title><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
open(sys.argv[1], "w", encoding="utf-8").write(html_out)
print("written", sys.argv[1], len(pages), "slides")
