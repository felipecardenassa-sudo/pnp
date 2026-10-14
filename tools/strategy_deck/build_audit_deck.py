"""Paid media audit 2026 – Meta and Google Search, for Raúl and Tereza (16:9 PDF, HTML → Chromium).

What it shows (Felipe, 14 Oct 2026): very visual, no fluff, no source notes on the slides. For each channel: the campaigns
that work (structure, spend, who we targeted, why), what doesn't and what replaces it, then the proposed structure as
mock-up blocks (campaign → ad sets → creatives → landing page). Meta is framed around Andromeda (post-Andromeda set-up).
Landing pages are drawn as annotated wireframes from the audit's measurements. Ends with a 7/30/60/90-day test plan.

Data: read-only browser audit of 14 Oct 2026 (reports/audit/paid_media_audit_2026-10-14.md; figures match our Meta and
Google exports), the platform exports for dates, the agency's Q1 2026 creative review (cost per lead by format), and
research/Paid_Media_Playbook_2026.md for the Andromeda and Google guidelines (never cited on slides).
Last 30 days = 14 Sep – 13 Oct 2026. Campaigns started in June/July are judged on the last 30 days: Meta and Google
recorded almost no results from 15 Jul to 10 Aug (tracking outage). Google bills in EUR; shown in USD at FX.

Usage (from the repo root): python3 -I tools/strategy_deck/build_audit_deck.py OUT_DIR [--pdf]
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "brand"))
import brand as B  # noqa: E402

STEM = "Paid_Media_Audit_2026"
CHROMIUM = "/opt/pw-browsers/chromium"
FX = 1.1177          # 1 EUR = 1.1177 USD (CLAUDE.md, live rate 13 Oct 2026)


def usd(x, d=0):
    return f"${x:,.{d}f}"


def eur(x, d=0):
    return usd(x * FX, d)


# ------------------------------------------------------------------ numbers (platform figures; see docstring)
# Meta, last 30 days, lead campaigns by region
EU = dict(spend=694.00 + 348.08 + 352.35, leads=105 + 39 + 44)              # EMEA, Middle East, Western Europe
US = dict(spend=883.68 + 707.00 + 532.35 + 356.62, leads=70 + 50 + 44 + 23)  # US East Coast, California, Middle-South, US & Canada
RT = dict(spend=1405.09, leads=108)
CPL_EU, CPL_US = EU["spend"] / EU["leads"], US["spend"] / US["leads"]
LEADS_PER_ADSET_WEEK = (EU["leads"] + US["leads"] + RT["leads"]) / 29 / (30 / 7)   # 28 topic ad sets + 1 retargeting
NEED_EU, NEED_US = 50 * CPL_EU / 7, 50 * CPL_US / 7                               # $/day for ~50 leads a week
NEW_EU, NEW_US = 55 * 7 / CPL_EU, 55 * 7 / CPL_US                                 # leads a week at $55 a day
assert round(CPL_EU, 2) == 7.42 and round(CPL_US, 2) == 13.26 and round(LEADS_PER_ADSET_WEEK) == 4


# ------------------------------------------------------------------ icons (drawn: Trebuchet MS has no symbols)
def svg(inner, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{inner}</svg>'


def stroke(c):
    return f'fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"'


def i_static(c=B.DARK_BLUE):
    return svg(f'<rect x="3" y="4.5" width="18" height="15" rx="2" {stroke(c)}/><circle cx="8.5" cy="9.5" r="1.7" fill="{c}"/>'
               f'<path d="M4 18l5-5 3.5 3.5 3-3 4.5 4.5" {stroke(c)}/>')


def i_carousel(c=B.DARK_BLUE):
    return svg(f'<rect x="6.5" y="5" width="11" height="14" rx="2" {stroke(c)}/><path d="M3 7.5v9M21 7.5v9" {stroke(c)}/>')


def i_video(c=B.DARK_BLUE):
    return svg(f'<rect x="3" y="4.5" width="18" height="15" rx="2" {stroke(c)}/><path d="M10 9v6l5-3z" fill="{c}"/>')


def i_talk(c=B.DARK_BLUE):
    return svg(f'<rect x="3" y="4.5" width="18" height="15" rx="2" {stroke(c)}/><circle cx="12" cy="10.5" r="2.6" {stroke(c)}/>'
               f'<path d="M7.5 18.5c.8-2.6 2.5-3.6 4.5-3.6s3.7 1 4.5 3.6" {stroke(c)}/>')


def i_proof(c=B.DARK_BLUE):
    return svg(f'<circle cx="12" cy="10" r="6" {stroke(c)}/><path d="M9.3 10.1l1.9 1.9 3.6-3.8" {stroke(c)}/>'
               f'<path d="M8.5 15l-1.5 5 5-2 5 2-1.5-5" {stroke(c)}/>')


def i_report(c=B.DARK_BLUE):
    return svg(f'<path d="M6 3h8l4 4v14H6z" {stroke(c)}/><path d="M14 3v4h4M9 12h6M9 15h6M9 18h4" {stroke(c)}/>')


def i_people(c=B.DARK_BLUE):
    return svg(f'<circle cx="9" cy="8" r="3" {stroke(c)}/><path d="M3.5 19c.6-3.3 2.8-5 5.5-5s4.9 1.7 5.5 5" {stroke(c)}/>'
               f'<circle cx="16.5" cy="9" r="2.4" {stroke(c)}/><path d="M16 14.2c2.4 0 4 1.5 4.5 4.3" {stroke(c)}/>')


def i_page(c=B.DARK_BLUE):
    return svg(f'<rect x="3" y="4" width="18" height="16" rx="2" {stroke(c)}/><path d="M3 8.5h18M7 13h6M7 16h4" {stroke(c)}/>'
               f'<rect x="14.5" y="11.5" width="3.5" height="6" rx=".8" fill="{c}"/>')


def i_camp(c=B.DARK_BLUE):
    return svg(f'<path d="M4 9v6h3l6 4V5L7 9z" {stroke(c)}/><path d="M17 9.5c1 .8 1 4.2 0 5M19.5 7.5c2 2 2 7 0 9" {stroke(c)}/>')


def i_search(c=B.DARK_BLUE):
    return svg(f'<circle cx="10.5" cy="10.5" r="6" {stroke(c)}/><path d="M15 15l5.5 5.5" {stroke(c)}/>')


def i_ad(c=B.DARK_BLUE):
    return svg(f'<rect x="3" y="5" width="18" height="14" rx="2" {stroke(c)}/><rect x="5.5" y="7.5" width="5" height="3.2" rx="1" fill="{c}"/>'
               f'<path d="M5.5 13.5h13M5.5 16.5h9" {stroke(c)}/>')


def i_pin(c=B.DARK_BLUE):
    return svg(f'<path d="M12 21s6.5-6.2 6.5-11a6.5 6.5 0 0 0-13 0c0 4.8 6.5 11 6.5 11z" {stroke(c)}/><circle cx="12" cy="10" r="2.4" {stroke(c)}/>')


def i_tag(c=B.DARK_BLUE):
    return svg(f'<path d="M3.5 12.5V4.5h8l9 9-8 8z" {stroke(c)}/><circle cx="8" cy="9" r="1.5" fill="{c}"/>')


def i_cursor(c=B.DARK_BLUE):
    return svg(f'<path d="M6 3.5l12 7.2-5.3 1.3 3.3 6.2-2.6 1.4-3.3-6.3L6 17z" {stroke(c)}/>')


def i_pause(c=B.DARK_BLUE):
    return svg(f'<circle cx="12" cy="12" r="8.5" {stroke(c)}/><path d="M10 8.5v7M14 8.5v7" {stroke(c)}/>')


def i_globe(c=B.DARK_BLUE):
    return svg(f'<circle cx="12" cy="12" r="8.5" {stroke(c)}/><path d="M3.5 12h17M12 3.5c2.6 2.4 3.7 5.3 3.7 8.5s-1.1 6.1-3.7 8.5M12 3.5C9.4 5.9 8.3 8.8 8.3 12s1.1 6.1 3.7 8.5" {stroke(c)}/>')


def i_flask(c=B.DARK_BLUE):
    return svg(f'<path d="M9.5 3.5h5M10.5 3.5v6L5 19a1.2 1.2 0 0 0 1 1.8h12a1.2 1.2 0 0 0 1-1.8l-5.5-9.5v-6" {stroke(c)}/><path d="M7.5 15h9" {stroke(c)}/>')


ICON = dict(static=i_static, carousel=i_carousel, video=i_video, talk=i_talk, proof=i_proof, report=i_report,
            people=i_people, page=i_page, camp=i_camp, search=i_search, ad=i_ad, pin=i_pin, tag=i_tag, cursor=i_cursor,
            pause=i_pause, globe=i_globe, flask=i_flask)


def arrow(cls="arw", c=B.GRAY):
    return (f'<svg class="{cls}" viewBox="0 0 30 16" aria-hidden="true"><path d="M2 8h23M19 2l6 6-6 6" fill="none" stroke="{c}" '
            'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def tick(c=B.GOOD):
    return (f'<svg class="mk" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="{c}"/>'
            '<path d="M4.4 8.3l2.4 2.4 4.8-5" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def bang(c=B.BAD):
    return (f'<svg class="mk" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="{c}"/>'
            '<path d="M8 4v5" stroke="#fff" stroke-width="2" stroke-linecap="round"/><circle cx="8" cy="11.8" r="1.1" fill="#fff"/></svg>')


def go(c=B.BLUE):
    return (f'<svg class="mk" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="{c}"/>'
            '<path d="M4.5 8h6.5M8.5 5l3 3-3 3" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def num(n, tone=""):
    return f'<span class="nm {tone}">{n}</span>'


# ------------------------------------------------------------------ building blocks
def tile(kind, label, count="", tone=""):
    badge = f'<span class="cnt">{count}</span>' if count else ""
    return f'<div class="tl {tone}">{badge}{ICON[kind]()}<span>{label}</span></div>'


def kpis(items):
    return '<div class="kpis">' + "".join(f'<div class="kpi {t}"><b>{v}</b><span>{l}</span></div>' for v, l, t in items) + "</div>"


def bullets(rows, mark):
    return "".join(f'<p class="bl">{mark}<span>{r}</span></p>' for r in rows)


def mini(steps):
    """A horizontal mini structure: [(icon, label)] joined by arrows."""
    out = []
    for i, (kind, label) in enumerate(steps):
        if i:
            out.append(arrow("arw sm"))
        out.append(f'<div class="ms">{ICON[kind]()}<span>{label}</span></div>')
    return f'<div class="mini">{"".join(out)}</div>'


def struct(steps):
    """A structure strip: [(icon, count, label)] boxes joined by arrows, with the count shown big."""
    out = []
    for i, (kind, count, label) in enumerate(steps):
        if i:
            out.append(arrow("arw sm"))
        out.append(f'<div class="sx">{ICON[kind]()}{f"<b>{count}</b>" if count else ""}<span>{label}</span></div>')
    return f'<div class="sxs">{"".join(out)}</div>'


def chip(name, value="", tone=""):
    return f'<div class="chp {tone}"><b>{name}</b>{f"<span>{value}</span>" if value else ""}</div>'


# ------------------------------------------------------------------ wireframes (drawn from the audit's page measurements)
def wf(url, inner, h=220, cls=""):
    return (f'<div class="wf {cls}" style="height:{h}px"><div class="wb"><i></i><i></i><i></i><div class="wu">{url}</div></div>'
            f'<div class="wc">{inner}</div></div>')


def at(x, y, w, h, cls="", text=""):
    hh = f"height:{h}px;" if h else ""
    return f'<div class="w {cls}" style="left:{x}px;top:{y}px;width:{w}px;{hh}">{text}</div>'


def pin(n, x, y, tone):
    return f'<div class="pin {tone}" style="left:{x}px;top:{y}px">{n}</div>'


def lines(x, y, w, n, gap=8, cls="ln"):
    return "".join(at(x, y + i * gap, w if i < n - 1 else int(w * .6), 4, cls) for i in range(n))


def form(x, y, w, n, title, h=None, cls="", step=11, hl=None):
    """A form with n fields; field number hl (0-based) is outlined in red."""
    h = h or 22 + n * step + 16
    fields = "".join(at(8, 18 + i * step, w - 16, step - 4, "fld hl" if i == hl else "fld") for i in range(n))
    return (f'<div class="w frm {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div class="ft">{title}</div>{fields}'
            f'<div class="w btn" style="left:8px;top:{h - 14}px;width:{w - 16}px;height:9px"></div></div>')


def legend(rows):
    return "".join(f'<p class="lgd">{num(n, tone)}<span>{t}</span></p>' for n, t, tone in rows)


# ------------------------------------------------------------------ slides
SLIDES = []


def slide(kicker, title, body, cls=""):
    SLIDES.append((kicker, title, body, cls))


# 2 · the short version
slide("Summary", "The short version", f"""
<div class="g3">
 <div class="card col"><div class="ch good">{tick()}<h3>Working</h3></div>
  {bullets(["<b>Report ads with a data hook</b> (robotics, quantum, energy grid, AI trends): $4–$8 per lead.",
            f"<b>Broad audiences in Europe and the Middle East</b>: {usd(CPL_EU, 2)} per lead in the last 30 days, about half the US.",
            "<b>Google: one campaign per region</b> instead of per state, and corporate searches with a matching page."], tick())}
 </div>
 <div class="card col"><div class="ch bad">{bang()}<h3>Not working</h3></div>
  {bullets(["<b>Meta is built for the old algorithm</b>: 30 ad sets on $160 a day, about 4 leads per ad set a week. Meta needs about 50 to learn.",
            "<b>Splitting by country didn't make us local</b>: the country ad sets ran the same English ads, at $33.07 per lead ($71,634).",
            "<b>Google</b>: 60% of spend lands on the homepage, which has no form, and 37% pays for our own name."], bang())}
 </div>
 <div class="card col"><div class="ch blue">{go()}<h3>What we change</h3></div>
  {bullets(["<b>Meta</b>: 3 campaigns, 5 ad sets, 8–15 creatives each in local languages; students and job seekers stop counting as results.",
            "<b>Google</b>: brand apart, corporate ad groups from new keyword research, a form behind every ad.",
            "<b>Pages and tests</b>: one corporate landing page, and a 90-day plan that tests new formats every two weeks."], go())}
 </div>
</div>
<div class="ba5">
 <div><span>Meta campaigns</span><b class="o">9</b>{arrow()}<b class="n">3</b></div>
 <div><span>Meta ad sets</span><b class="o">30</b>{arrow()}<b class="n">5</b></div>
 <div><span>Leads per ad set a week</span><b class="o">≈{LEADS_PER_ADSET_WEEK:.0f}</b>{arrow()}<b class="n">≈{NEW_US:.0f}–{NEW_EU:.0f}</b></div>
 <div><span>Google clicks to the homepage</span><b class="o">60%</b>{arrow()}<b class="n">0%</b></div>
 <div><span>Google spend on our own name, mixed in</span><b class="o">37%</b>{arrow()}<b class="n">0%</b></div>
</div>""", "s-sum")

# 3 · Andromeda
mini_camps = "".join(
    f'<div class="mc"><span>{lab}</span><div class="sq">' + "<i></i>" * 4 + '<i class="off"></i></div></div>'
    for lab in ["US-California", "US East Coast", "US &amp; Canada", "US Middle-South", "EMEA", "Middle East", "Western Europe"])
kinds = ["static", "carousel", "video", "talk", "proof", "static", "carousel", "video", "report", "static"]
big_tiles = "".join(f'<div class="tt">{ICON[k]()}</div>' for k in kinds)
slide("Meta · Andromeda", "Meta changed how it picks who sees our ads. Our set-up didn't.", f"""
<div class="vs">
 <div class="card pnl">
  <div class="ph bad">Our set-up today</div>
  <div class="mcs">{mini_camps}</div>
  <div class="cap">7 location campaigns × the same 5 topic ad sets · $10–$26 a day per campaign · about $4 a day per ad set</div>
  {bullets(["Split by location, job title and interest, with mostly the same English ads in each", "The US &amp; Canada campaign overlaps the three US-state campaigns",
            "About 8 ads per ad set, many of them copies of each other"], bang())}
  {kpis([("30", "ad sets", "bad"), ("≈$4", "a day per ad set", "bad"), ("≈8", "ads per ad set, many copies", "")])}
  <div class="big bad"><b>≈{LEADS_PER_ADSET_WEEK:.0f}</b><span>leads per ad set a week</span></div>
 </div>
 <div class="mid">{arrow("arw lg")}</div>
 <div class="card pnl">
  <div class="ph good">What Meta rewards now</div>
  <div class="bc"><div class="bch">1 prospecting campaign</div>
   <div class="bas"><div class="ba"><div class="bah">Europe &amp; Middle East · broad</div><div class="tts">{big_tiles}</div></div>
   <div class="ba"><div class="bah">US &amp; Canada · broad</div><div class="tts">{big_tiles}</div></div></div></div>
  {bullets(["Few campaigns, 1–3 broad ad sets: location, language, age and exclusions are the only hard limits",
            "8–20 really different creatives per ad set, each one speaking to one persona: the creative picks the people"], tick())}
  {kpis([("2", "broad ad sets", "good"), ("≈$55", "a day per ad set", "good"), ("8–15", "different concepts each", "good")])}
  <div class="big good"><b>≈50</b><span>leads per ad set a week to learn</span></div>
 </div>
</div>
<div class="band"><b>Andromeda</b> is the system Meta has used since December 2024 to match ads to people. It reads the creative itself to
decide who sees it; audience settings are only suggestions. Many small ad sets with small budgets each get too little data to learn.</div>
""")

# 4 · our data: split vs grouped
US_STATE_ADSETS = [("New Jersey", 5097.37), ("New York", 4626.52), ("Texas", 4539.13), ("Florida", 4275.98),
                   ("Washington DC", 3580.62), ("Indiana", 3523.38), ("Arizona", 3236.02)]   # inside EMEA/lead/prospecting/abo/20260210
US_STATE_SPEND = sum(v for _, v in US_STATE_ADSETS)
SPLIT_COUNTRIES = [(12583.08, 547), (12154.89, 333), (10712.39, 306), (6190.08, 193)]   # UK, France, Italy, Saudi Arabia ad sets
CPL_SPLIT_COUNTRIES = sum(v for v, _ in SPLIT_COUNTRIES) / sum(n for _, n in SPLIT_COUNTRIES)
assert round(CPL_SPLIT_COUNTRIES, 2) == 30.20 and round(US_STATE_SPEND) == 28879
slide("Meta · our data", "Our own data: grouping beats splitting, 2.6× cheaper per lead", f"""
<div class="g2">
 <div class="card cmp"><div class="ch bad">{bang()}<h3>Split: one ad set per country, job-title audiences</h3></div>
  {mini([("camp", "EMEA prospecting<br>Feb–Jul"), ("people", "1 ad set per country<br>+ 7 US states"), ("ad", "Report and<br>platform ads"), ("page", "Report pages")])}
  <div class="sub">Country ad sets · cost per lead</div>
  <div class="chps">{chip("UK", "$23.00", "bad")}{chip("France", "$36.50", "bad")}{chip("Italy", "$35.01", "bad")}{chip("Saudi Arabia", "$32.07", "bad")}</div>
  <div class="sub">+ 7 US-state ad sets in this EMEA campaign · {usd(US_STATE_SPEND)} ({US_STATE_SPEND / 71634.18:.0%}) spent</div>
  <div class="chps">{"".join(chip(n, usd(v)) for n, v in US_STATE_ADSETS)}</div>
  <div class="who">{i_people()}<span>Job titles by country (CEO, CTO, CIO, CSO, MD, Head of IT…), age 25+, past leads excluded</span></div>
  {kpis([("$71,634", "spent", ""), ("2,166", "leads", ""), ("$33.07", "per lead", "bad")])}
 </div>
 <div class="card cmp"><div class="ch good">{tick()}<h3>Grouped: 19 countries together, one ad set per report topic</h3></div>
  {mini([("camp", "EMEA prospecting test<br>Jan–Jul"), ("people", "1 ad set<br>per report topic"), ("report", "Report ads<br>with a data hook"), ("page", "Report pages")])}
  <div class="sub">Biggest ad sets · cost per lead</div>
  <div class="chps">{chip("Decarbonisation", "$8.14", "good")}{chip("Spain energy grid", "$8.76", "good")}{chip("Quantum", "$10.47", "good")}{chip("AI &amp; robotics", "$11.07", "good")}{chip("Job titles only", "$50.09", "bad")}</div>
  <div class="who">{i_people()}<span>Tech and C-level leaders with interests that match each report, 19 countries, age 25+</span></div>
  {kpis([("$18,001", "spent", ""), ("1,437", "leads", ""), ("$12.53", "per lead", "good")])}
 </div>
</div>
<div class="band good">Without its US states, the split campaign still cost <b>{usd(CPL_SPLIT_COUNTRIES, 2)} per lead</b> in the UK, France, Italy and
Saudi Arabia, which the grouped campaign also covered. <b>The report topic did the targeting better than country and job-title splits.</b></div>
""", "s-data")

# 5 · local creatives: what the country ad sets ran, and local the Andromeda way
SAME_AD = [   # the same English ad: (ad set, spend, results) in the grouped topic ad set and in the country ad sets
    ("Quantum video", [("Grouped", 1404.34, 188, "good"), ("UK", 6767.35, 332, "bad"), ("France", 4273.87, 118, "bad")]),
    ("Spain grid ad", [("Grouped", 1587.28, 207, "good"), ("UK", 1513.90, 84, "bad"), ("Italy", 2122.82, 73, "bad")]),
]
assert [round(v / n, 2) for _, rows in SAME_AD for _, v, n, _ in rows] == [7.47, 20.38, 36.22, 7.67, 18.02, 29.08]
same_ad_rows = "".join(f'<div class="sar"><b>{name}</b><div class="chps">{"".join(chip(s, usd(v / n, 2), t) for s, v, n, t in rows)}</div></div>'
                       for name, rows in SAME_AD)
lang_badges = '<span class="lb def">EN</span>' + "".join(f'<span class="lb">{x}</span>' for x in ["FR", "DE", "IT", "ES"])
SAME_AD_RATIO = [v / n / (rows[0][1] / rows[0][2]) for _, rows in SAME_AD for _, v, n, _ in rows[1:]]   # country ad set vs grouped
assert f"{min(SAME_AD_RATIO):.1f}–{max(SAME_AD_RATIO):.1f}" == "2.4–4.8"
fan = "".join(f'<div class="fr"><span class="lb{" def" if x == "EN" else ""}">{x}</span><span>{who}</span></div>'
              for x, who in [("FR", "French speakers"), ("DE", "German speakers"), ("IT", "Italian speakers"),
                             ("ES", "Spanish speakers"), ("EN", "everyone else")])
slide("Meta · local creatives", "Going local is right. The country split didn't make our ads local.", f"""
<div class="vs">
 <div class="card pnl">
  <div class="ph bad">What the country ad sets ran</div>
  {struct([("camp", "1", "EMEA campaign"), ("people", "4", "country ad sets:<br>UK, FR, IT, SA"), ("ad", "EN", "the same ads"), ("page", "EN", "the same pages")])}
  <div class="sub">The same English ad · cost per lead</div>
  {same_ad_rows}
  <div class="sub">Our ads by language</div>
  <div class="chps">{chip("English", "~240 live", "")}{chip("French, Italian, German, Arabic, Portuguese", "about 3 in all", "bad")}{chip("Spanish", "0", "bad")}</div>
  <div class="big bad"><b>{min(SAME_AD_RATIO):.1f}–{max(SAME_AD_RATIO):.1f}×</b><span>the cost per lead of the same English ad in a country ad set</span></div>
 </div>
 <div class="mid">{arrow("arw lg")}</div>
 <div class="card pnl">
  <div class="ph good">Local, the Andromeda way</div>
  {struct([("camp", "1", "prospecting campaign"), ("people", "1", "broad ad set<br>per region"), ("ad", "5", "language versions<br>in every ad"), ("page", "", "page in the<br>ad's language")])}
  <div class="lvs"><div class="lva">{i_ad()}<b>One ad</b><span>a version per language</span></div>{arrow()}<div class="fan">{fan}</div>
   <div class="lvc">Meta shows each person the version in their language</div></div>
  {bullets(["<b>Hard limits</b>: countries, languages, age 25+, no past leads",
            "<b>The creative targets</b>: language, persona, local topic and local proof (partners, cases, office events)",
            f"<b>Own ad set for a market</b> only when its budget buys about 50 leads a week ({usd(NEED_EU)} a day at Europe's cost per lead)"], tick())}
 </div>
</div>
<div class="band"><b>Local content beats generic 3:1 on cost per lead</b> (EMEA, H1 2026). For that, the ad and the page have to be local,
not just the audience.</div>
""", "s-local")


# 6 · what's working
def ccard(title, status, steps, k, who, why, improve):
    return (f'<div class="card cc"><div class="cct"><h3>{title}</h3><span class="st {status[1]}">{status[0]}</span></div>'
            f'{struct(steps)}{kpis(k)}<div class="who">{i_people()}<span>{who}</span></div>'
            f'<div class="sub">Why it works</div>{bullets(why, tick())}<div class="sub">Improve</div>{bullets(improve, go())}</div>')


slide("Meta · working", "What's working on Meta", f"""
<div class="g3">
 {ccard("Broad prospecting · Europe &amp; Middle East", ("Live", "live"),
        [("camp", "3", "campaigns<br>$41 a day"), ("people", "12", "topic ad sets"), ("ad", "≈8", "ads each"), ("page", "", "Report pages")],
        [(usd(EU['spend']), "spent, 30 days", ""), (str(EU['leads']), "leads, 30 days", ""), (usd(CPL_EU, 2), "per lead", "good")],
        "Broad (Advantage+) in 19–20 countries of Europe and the Gulf; past leads excluded",
        ["Cheap reach: $8–$13 per 1,000 views, against $33–$44 in the US", "Deep Tech report ads: $4–$5 per lead here"],
        ["One broad ad set instead of 3 campaigns and 12 ad sets", "More creative variety instead of copies"])}
 {ccard("Report-topic ad sets · 19 countries", ("Ended Jul", "off"),
        [("camp", "1", "campaign<br>$50 a day"), ("people", "1", "ad set per<br>report topic"), ("report", "", "Report ads"), ("page", "", "Report pages")],
        [("$18,001", "spent, Jan–Jul", ""), ("1,437", "leads", ""), ("$12.53", "per lead", "good")],
        "Tech and C-level leaders with interests that match each report",
        ["Each ad set paired one report with the people who care about it", "Quantum, Spain energy grid and decarbonisation reports: $8–$10 per lead"],
        ["Bring these reports back as creatives in one broad ad set"])}
 {ccard("Retargeting · worldwide", ("Live", "live"),
        [("camp", "1", "campaign<br>$41 a day"), ("people", "1", "ad set"), ("proof", "53", "ads"), ("page", "", "Innovation platform page")],
        [(usd(RT['spend']), "spent, 30 days", ""), (str(RT['leads']), "registrations", ""), ("$13.01", "per lead", "good")],
        "People who sent us a form in the last 180 days (Meta may widen it)",
        ["Warm audience that already knows us", "Proof from the press: best ad “Fast-Track Corporate Innovation”, $15.66 per lead this year"],
        ["Audience under 1,000 people seeing ads 5.75 times: $20 a day and 4–6 ads, refreshed every 2–4 weeks"])}
</div>""", "s-work")


# 7 · what's not working → what replaces it
def swap(icon, ptitle, ptext, ftitle, ftext):
    return (f'<div class="sw"><div class="card swp"><div class="swi bad">{ICON[icon](B.BAD)}</div><div><b>{ptitle}</b><span>{ptext}</span></div></div>'
            f'<div class="swa">{arrow("arw")}</div><div class="card swf"><div class="swi good">{ICON[icon](B.GOOD)}</div><div><b>{ftitle}</b><span>{ftext}</span></div></div></div>')


slide("Meta · not working", "What's not working on Meta, and what replaces it", f"""
<div class="swh"><span class="bad">Not working</span><span></span><span class="good">Instead</span></div>
{swap("pin", "The US split into 4 campaigns and 16 ad sets", f"$72 a day in total; {usd(CPL_US, 2)} per lead in the last 30 days, about twice Europe",
      "One US &amp; Canada ad set", "Broad, $55 a day, with the report creatives that work in Europe")}
{swap("tag", "Brand and Health ad sets", "Brand in California $139.57 for 1 lead; Health in the US $36–$51 per lead",
      "Proof and health as creatives, not ad sets", "Press quotes, case results and health reports, tried first in the test campaign")}
{swap("people", "Job-title ad sets", "Innovation Leader job titles $50.09 per lead; country job-title ad sets $23–$37",
      "The ad names the buyer", "Broad audience; the creative says who it is for, e.g. innovation leaders at large companies")}
{swap("cursor", "Traffic campaigns", "FR_Alibaba took 41% of the last 30 days' spend for $0.03 clicks outside our markets; US clicks go to a page with no form",
      "Lead campaigns only", "Traffic money moves to prospecting")}
{swap("pause", "Ads that don't deliver still run", "Healthcare voice-memo video: 3 leads for $174. 2025 report ad: 0 leads after $373",
      "Pause now, then a weekly rule", "After $50 spent, pause any ad 20% above the average cost per lead")}
""")

# 8 · creatives
best = [("static", "Quantum report", "static", "$6.86", "126"), ("video", "Quantum report", "short video", "$7.47", "188"),
        ("report", "AI trend report", "report ad", "$7.48", "56"), ("carousel", "Spain energy grid", "carousel", "$7.67", "207"),
        ("video", "AI &amp; robotics report", "product video, Europe", "$4.10", "73"), ("proof", "Press quote", "retargeting image", "$15.66", "165")]
best_rows = "".join(f'<div class="br">{ICON[k]()}<div class="bn"><b>{n}</b><span>{f}</span></div><div class="bv"><b>{v}</b><span>{l} leads</span></div></div>'
                    for k, n, f, v, l in best)
slide("Meta · creatives", "Which creatives bring leads, and what we make next", f"""
<div class="g3c">
 <div class="card"><div class="sub">Best ads this year · cost per lead</div>{best_rows}</div>
 <div class="card"><div class="sub">By format · Q1 2026 · cost per lead</div>
  <div class="fm">{tile("static", "Static", "$12.91", "good")}{tile("carousel", "Carousel", "$13.77", "good")}{tile("video", "Short video", "$20.54", "bad")}</div>
  <div class="fm2"><div class="good"><b>$9.23</b>video showing the product</div><div class="bad"><b>$20.79</b>video of a person talking</div></div>
  <div class="sub">Stop</div>{bullets(["Event and case-study videos and ebooks in narrow ad sets: $129–$190 per lead",
                                   "One quantum video copied into 12+ separate ads: it splits the learning"], bang())}
 </div>
 <div class="card"><div class="sub">What we make next · 8–15 concepts per ad set</div>
  <div class="nx">{tile("static", "Data-hook static", "×3")}{tile("carousel", "Report carousel", "×2")}{tile("video", "Product explainer", "×2")}
  {tile("proof", "Case result or logos", "×2")}{tile("talk", "Talking head", "test")}{tile("globe", "FR · DE · IT · ES version of each", "")}</div>
  <div class="sub">Each concept speaks to one persona</div>
  <div class="ps"><span>Innovation &amp; R&amp;D leaders</span><span>C-level</span><span>Digital leaders (CDO)</span><span>Governments</span></div>
  <div class="sub">Refresh</div>{bullets(["New ideas start in the test campaign: 2–5 ads each, 7 days", "New concepts every 2–3 weeks; winners stay, losers go"], go())}
 </div>
</div>""", "s-crea")


# 9 · new Meta structure (mock-up)
def gcell(row, col, inner, cls="", span=1):
    return f'<div class="gc {cls}" style="grid-row:{row} / span {span};grid-column:{col}">{inner}</div>'


def garrow(row, col, span=1):
    return f'<div class="ga" style="grid-row:{row} / span {span};grid-column:{col}">{arrow()}</div>'


def camp_block(title, sub, tone=""):
    return f'<div class="cb {tone}">{i_camp("#fff")}<div><b>{title}</b><span>{sub}</span></div></div>'


def set_block(title, sub, tone="good"):
    return f'<div class="sb {tone}">{i_people()}<div><b>{title}</b><span>{sub}</span></div></div>'


def page_block(title, sub=""):
    return f'<div class="pb">{i_page()}<div><b>{title}</b>{f"<span>{sub}</span>" if sub else ""}</div></div>'


meta_mix = (tile("static", "Data hook", "×3") + tile("carousel", "Carousel", "×2") + tile("video", "Product video", "×2")
            + tile("proof", "Proof", "×2") + tile("talk", "Talking head", "×1"))
meta_grid = "".join([
    '<div class="gh" style="grid-column:1">Campaigns</div><div class="gh" style="grid-column:3">Ad sets · who</div>'
    '<div class="gh" style="grid-column:5">Creatives · what they see</div><div class="gh" style="grid-column:7">Landing page</div>',
    gcell(2, 1, camp_block("Prospecting", "CBO · $110 a day"), span=2), garrow(2, 2), garrow(3, 2),
    gcell(2, 3, set_block("Europe &amp; Middle East", "Broad · ≈$55 a day")), gcell(3, 3, set_block("US &amp; Canada", "Broad · ≈$55 a day")),
    garrow(2, 4), garrow(3, 4), gcell(2, 5, f'<div><div class="tls">{meta_mix}</div><div class="lvl">Every ad in {lang_badges}</div></div>'), gcell(3, 5, '<div class="same">The same 8–15 concepts</div>'),
    garrow(2, 6), garrow(3, 6), gcell(2, 7, page_block("Report pages", "in the ad's language"), span=2),
    gcell(4, 1, camp_block("Retargeting", "$20 a day")), garrow(4, 2), gcell(4, 3, set_block("Visitors and past leads", "Last 180 days")),
    garrow(4, 4), gcell(4, 5, '<div class="tls">' + tile("proof", "Press quote") + tile("proof", "Case result") + tile("proof", "Partner logos")
                       + tile("page", "Talk to us") + "</div>"), garrow(4, 6), gcell(4, 7, page_block("Corporate page")),
    gcell(5, 1, camp_block("Creative test", "ABO · $30 a day (20%)", "test")), garrow(5, 2), gcell(5, 3, set_block("2 test ad sets", "$15 a day each", "")),
    garrow(5, 4), gcell(5, 5, '<div class="tls">' + tile("flask", "New idea A", "2–5") + tile("flask", "New idea B", "2–5") + "</div>"),
    garrow(5, 6), gcell(5, 7, '<div class="win">Winners move to Prospecting after 7 days</div>'),
])
slide("Meta · new structure", "New Meta structure: 3 campaigns, 5 ad sets, the creative does the targeting", f"""
<div class="goal">{tick()}<span><b>Goal:</b> a lead form sent, with student and job-seeker answers left out (corporate and government only once there is volume). Every ad set: location, language, age 25+, exclusions, ICP job titles as suggestions.</span></div>
<div class="mg">{meta_grid}</div>
<div class="ba5">
 <div><span>Campaigns</span><b class="o">9</b>{arrow()}<b class="n">3</b></div>
 <div><span>Ad sets</span><b class="o">30</b>{arrow()}<b class="n">5</b></div>
 <div><span>Budget per prospecting ad set</span><b class="o">$4</b>{arrow()}<b class="n">$55</b><em>a day</em></div>
 <div><span>Leads per ad set a week</span><b class="o">≈{LEADS_PER_ADSET_WEEK:.0f}</b>{arrow()}<b class="n">≈{NEW_US:.0f}–{NEW_EU:.0f}</b></div>
 <div><span>Total budget</span><b class="n">$160</b><em>a day, same</em></div>
</div>""", "s-meta")


# 10 · how broad still gets us our ICP
def ctrl(n, kind, name, today, new):
    return (f'<div class="ct"><div class="ctl">{num(n)}{ICON[kind]()}<b>{name}</b></div>'
            f'<div class="card ctx bad">{bang()}<span>{today}</span></div><div class="swa">{arrow()}</div>'
            f'<div class="card ctx good">{tick()}<span>{new}</span></div></div>')


slide("Meta · our ICP", "How broad still gets us our ICP", f"""
<div class="ct cth"><span>Control</span><span class="bad">Today</span><span></span><span class="good">New</span></div>
{ctrl(1, "pin", "Who can see the ad", "Countries and age; CRM exclusion lists may not apply (custom-audience terms not accepted)",
      "Countries, language, age 25+; customers, current leads, students and job seekers excluded")}
{ctrl(2, "people", "Where Meta looks first", "Job titles and interests as suggestions (Advantage+ audience on), split across 30 small ad sets",
      "The same ICP job titles and people like our corporate leads (lookalike) as suggestions, in one broad ad set")}
{ctrl(3, "ad", "What the ad says", "Most-used headlines say what, not who it's for: “Access World-Class Startups”, “Join the Innovation Platform”",
      "Every ad names the buyer: innovation, R&amp;D and digital leaders at 10,000+ companies, or governments")}
{ctrl(4, "tag", "What counts as a result", "Any form sent on a welcome page, students and job seekers included",
      "Now: students and job seekers stop counting. Next, as volume allows: corporate and government only, then CRM-qualified leads")}
{ctrl(5, "report", "How we judge each ad", "Ranked by cost per lead",
      "Every Monday: each ad's share of leads that fit the ICP (the ad name is in every lead's UTM); cut ads whose cheap leads don't")}
<div class="band">Meta can't target company size or a list of companies. It finds more people like the ones who trigger the result,
so <b>what we count as a result is our sharpest targeting</b>.</div>
""", "s-icp")

# 11 · Google findings
# live structure: NA and EMEA Search 20260813 (cost in EUR since they started on 10 Aug) + the coworking campaign
G_COST = 5256.66 + 4366.65
G_AD_GROUPS = [("Brand", 2396.68 + 1208.63, "bad"), ("Startup collaboration", 2350.98 + 1656.44, "bad"),
               ("Innovation", 341.47 + 989.11, "good"), ("AI strategy", 167.53 + 512.47, "")]
G_PAGES = [("Homepage", 2969.63 + 2841.09, "bad"), ("Innovation platform", 1553.73 + 1138.70, ""), ("Supply-chain page", 265.89, "good")]
assert round(sum(v for _, v, _ in G_AD_GROUPS), 2) == round(G_COST, 2)
assert [f"{v / G_COST:.0%}" for _, v, _ in G_AD_GROUPS[:2] + G_PAGES[:1]] == ["37%", "42%", "60%"]


def gcol(kind, count, label, chips=""):
    return f'<div class="gtc"><div class="gtt">{ICON[kind]()}<b>{count}</b><span>{label}</span></div><div class="chps">{chips}</div></div>'


google_today = ('<div class="card gt"><div class="sub">Google today · live campaigns · % of North America and Europe &amp; Middle East spend since 10 Aug</div><div class="gtr">'
                + gcol("camp", "3", "campaigns", chip("North America") + chip("Europe &amp; Middle East") + chip("Coworking, Silicon Valley"))
                + arrow() + gcol("people", "9", "ad groups: the same 4 in each region, plus coworking",
                                 "".join(chip(n, f"{v / G_COST:.0%}", t) for n, v, t in G_AD_GROUPS))
                + arrow() + gcol("ad", "9", "ads: 1 per ad group")
                + arrow() + gcol("page", "3", "main landing pages", "".join(chip(n, f"{v / G_COST:.0%}", t) for n, v, t in G_PAGES))
                + "</div></div>")
states = [("New York", 549.70), ("US East Coast", 327.02), ("Florida", 287.94), ("Texas", 280.30), ("Arizona", 254.04), ("New Jersey", 249.37)]
state_tiles = "".join(f'<div class="stt"><span>{n}</span><b>{eur(v)}</b></div>' for n, v in states)
slide("Google Search", "Google Search: what works and what doesn't", f"""
<div class="card cons"><div class="sub">One campaign per US state or area (Jan–May) vs one per region (Aug–Oct) · cost per conversion</div>
 <div class="cr"><div class="sts">{state_tiles}</div>{arrow("arw lg")}<div class="rgs"><div class="rg"><span>US &amp; Canada</span><b>{eur(44.23)}</b></div>
 <div class="rg"><span>Europe &amp; Middle East</span><b>{eur(41.36)}</b></div></div></div></div>
{google_today}
<div class="g2">
 <div class="card col"><div class="ch good">{tick()}<h3>Working</h3></div>
  {bullets([f"<b>Corporate searches + a matching page</b>: the Innovation ad group sends supply-chain searches to the supply-chain page. 24% of clicks convert, {eur(11.51, 2)} each.",
            f"<b>Corporate ad copy</b>: “Top Corporate Accelerator | Corporate Innovation Lab” converted 9–10% of clicks at {eur(29.84)}–{eur(35.87)}, half the cost of the generic ad.",
            f"<b>Best markets now</b>: Saudi Arabia {eur(32.26)}, Qatar {eur(44.35)}, France {eur(52.75)}, UK {eur(54.02)} per conversion."], tick())}
 </div>
 <div class="card col"><div class="ch bad">{bang()}<h3>Not working</h3></div>
  {bullets(["<b>The homepage has no lead form</b>, only a newsletter sign-up.",
            "<b>Our own name</b> (“plug and play” searches) sits inside campaigns that run out of budget.",
            "<b>Startup-side ad groups</b>: “Venture Capitalist” headline, coworking extras, “startup india certificate”.",
            "<b>Google picks the searches</b> (broad match + AI Max) on $34–$37 a day; budgets cut 71–76% in three days; business name, logo and 14 of 18 images disapproved."], bang())}
 </div>
</div>""", "s-gfind")

# 12 · new Google structure (mock-up)
ag = lambda name: f'<div class="agc">{name}</div>'
corp_groups = ag("Corporate innovation") + ag("Startup scouting") + ag("Open innovation &amp; pilots") + ag("Industry: supply chain, health, energy")
google_grid = "".join([
    '<div class="gh" style="grid-column:1">Campaigns</div><div class="gh" style="grid-column:3">Ad groups · themes</div>'
    '<div class="gh" style="grid-column:5">Ads · 2 each</div><div class="gh" style="grid-column:7">Landing page</div>',
    gcell(2, 1, camp_block("Brand", "All markets · capped budget")), garrow(2, 2), gcell(2, 3, f'<div class="ags one">{ag("“plug and play” searches, exact and phrase")}</div>'),
    garrow(2, 4), gcell(2, 5, '<div class="tls">' + tile("ad", "Ad A") + tile("ad", "Ad B") + "</div>"), garrow(2, 6), gcell(2, 7, page_block("Corporate page")),
    gcell(3, 1, camp_block("Corporate · US &amp; Canada", "Phrase and exact")), garrow(3, 2), gcell(3, 3, f'<div class="ags">{corp_groups}</div>'),
    garrow(3, 4), gcell(3, 5, '<div class="tls">' + tile("ad", "Ad A") + tile("ad", "Ad B") + "</div>"), garrow(3, 6),
    gcell(3, 7, page_block("Matching page", "with a form")),
    gcell(4, 1, camp_block("Corporate · Europe &amp; Middle East", "Phrase and exact")), garrow(4, 2), gcell(4, 3, f'<div class="ags">{corp_groups}</div>'),
    garrow(4, 4), gcell(4, 5, '<div class="tls">' + tile("ad", "Ad A") + tile("ad", "Ad B") + "</div>"), garrow(4, 6),
    gcell(4, 7, page_block("Matching page", "with a form")),
])
slide("Google Search · new structure", "New Google structure: brand apart, corporate themes, a form behind every ad", f"""
<div class="rs">{i_search()}<div><b>Step 1 · Keyword research in Semrush</b><span>Corporate themes, search volume and cost per click for the US, UK, France, Germany, Spain and Italy; competitor terms; negatives.</span></div></div>
<div class="mg gg">{google_grid}</div>
<div class="goal">{tick()}<span><b>Rules:</b> standing negatives (jobs, careers, apply, funding for my startup, pitch, grants, education, free) · location “presence” · goal: corporate form (downloads count as secondary) · AI Max later, as a test.</span></div>
<div class="ba5">
 <div><span>Brand spend inside non-brand</span><b class="o">37%</b>{arrow()}<b class="n">0%</b></div>
 <div><span>Startup-side ad groups</span><b class="o">42%</b>{arrow()}<b class="n">0%</b></div>
 <div><span>Clicks to the homepage</span><b class="o">60%</b>{arrow()}<b class="n">0%</b></div>
 <div><span>Broad-match keywords</span><b class="o">all</b>{arrow()}<b class="n">none</b></div>
 <div><span>Total budget</span><b class="n">{eur(68)}</b><em>a day, same</em></div>
</div>""", "s-goog")

# 13 · landing pages today (annotated wireframes)
report_wf = wf("welcome…/embedded-ai-robotics",
               at(10, 6, 34, 7, "nav") + at(26, 30, 150, None, "hd", "How Embedded AI Robotics is Transforming Industries &amp; Daily Life")
               + lines(26, 84, 145, 3) + at(26, 116, 150, 144, "img") + form(186, 22, 148, 10, "Download now", step=20, hl=5)
               + pin(1, 4, 30, "good") + pin(2, 322, 13, "good") + pin(3, 322, 140, "bad"), h=300)
uip_wf = wf("welcome…/ultimate-innovation-platform",
            at(10, 6, 34, 7, "nav") + "".join(at(190 + i * 30, 6, 22, 6, "nav") for i in range(5))
            + at(30, 34, 290, None, "hd c xl", "Start Your Innovation Journey") + lines(105, 60, 130, 2)
            + "".join(at(26 + i * 74, 92, 62, 34, "stat", s) for i, s in enumerate(["550+", "60+", "100K+", "35+"]))
            + "".join(at(26 + i * 49, 146, 40, 14, "lg") for i in range(6)) + lines(60, 182, 226, 3)
            + at(0, 232, 346, 1, "fold") + at(250, 219, 90, None, "fl", "end of first screen")
            + form(70, 244, 200, 4, "Get in touch", h=60, cls="cut", step=13, hl=0)
            + pin(1, 40, 34, "bad") + pin(2, 6, 100, "good") + pin(3, 324, 238, "bad") + pin(4, 278, 258, "bad"), h=300)
home_wf = wf("plugandplaytechcenter.com",
             at(10, 6, 34, 7, "nav") + "".join(at(110 + i * 28, 6, 22, 6, "nav") for i in range(8))
             + at(60, 34, 220, None, "hd c xl", "We Drive Innovation") + lines(85, 60, 170, 2) + at(140, 82, 60, 14, "cta")
             + "".join(at(14 + i * 108, 114, 96, 64, "img") for i in range(3)) + at(300, 150, 22, 22, "chat") + at(272, 158, 18, 18, "chat")
             + at(14, 196, 316, 44, "brk", "the page goes on: 8,769 px in all")
             + at(14, 254, 316, 18, "nl", "Newsletter sign-up (the only form)")
             + pin(1, 72, 34, "bad") + pin(2, 4, 255, "bad") + pin(3, 324, 134, "bad") + pin(4, 96, 2, "bad"), h=300)
slide("Landing pages", "Our landing pages today", f"""
<div class="g3">
 <div class="card lp"><div class="lph"><h3>Report page</h3><span class="st live">Meta · works</span></div>{report_wf}
  {legend([(1, "One topic, clear headline", "good"), (2, "Form next to the headline; asks company size and job level", "good"),
           (3, "“Student” and “looking for a job” can submit, and count as leads", "bad")])}</div>
 <div class="card lp"><div class="lph"><h3>Innovation platform page</h3><span class="st warn">Google + retargeting</span></div>{uip_wf}
  {legend([(1, "One message for corporates, startups, governments and investors", "bad"), (2, "Strong stats: 550+ partners, 60+ locations", "good"),
           (3, "Form below the first screen; on phone, 2 screens down", "bad"), (4, "Profile dropdown first; corporate path has 12 fields and no company size", "bad")])}</div>
 <div class="card lp"><div class="lph"><h3>Homepage</h3><span class="st off">60% of Google spend</span></div>{home_wf}
  {legend([(1, "Message for everyone", "bad"), (2, "No lead form: only a newsletter sign-up at the bottom", "bad"),
           (3, "On phone, two chat pop-ups cover the headline", "bad"), (4, "156 links to leave the page", "bad")])}</div>
</div>""")

# 14 · proposed landing page
prop_wf = wf("welcome.plugandplaytechcenter.com/corporate-innovation",
             at(26, 12, 52, 10, "nav") + pin("A", 4, 8, "blue")
             + at(26, 50, 290, None, "hd xl", "Headline that names the buyer and the result") + lines(26, 120, 270, 3, gap=12)
             + at(26, 172, 130, 24, "cta") + form(340, 48, 196, 6, "Short form · 6 fields", step=23) + pin("B", 518, 38, "blue")
             + "".join(at(26 + i * 50, 256, 42, 24, "lg") for i in range(6)) + at(340, 256, 196, 24, "res", "1 result in numbers")
             + pin("C", 4, 259, "blue")
             + "".join(at(26 + i * 170, 316, 158, 96, "card3", t) for i, t in enumerate(["Startup scouting", "Pilots", "Innovation programs"]))
             + pin("D", 4, 316, "blue") + at(26, 436, 330, 70, "case", "Case study, open") + pin("E", 4, 436, "blue")
             + at(370, 436, 166, 70, "cta2", "Form again") + pin("F", 518, 426, "blue"), h=536)
phone_wf = ('<div class="ph1"><div class="ph1c">' + at(10, 12, 100, None, "hd", "Headline") + lines(10, 32, 100, 2)
            + form(10, 54, 100, 6, "Short form", step=18) + "".join(at(10 + i * 34, 212, 28, 12, "lg") for i in range(3))
            + at(0, 250, 116, 1, "fold ok") + at(10, 238, 106, None, "fl ok", "end of first screen")
            + at(10, 260, 100, 46, "card3") + at(10, 314, 100, 38, "case") + at(10, 360, 100, 16, "cta2") + "</div></div>")
lp_before_after = [("Fields on the corporate form", "12", "6"), ("Company size asked", "no", "yes"),
                   ("Student option", "yes", "no"), ("Form on phone", "2 screens down", "first screen")]
slide("Landing pages · proposal", "The corporate landing page we propose", f"""
<div class="pp">
 <div class="card ppw">{prop_wf}</div>
 <div class="card ppp"><div class="sub">On phone</div>{phone_wf}<p class="cap">Form within the first screen</p></div>
 <div class="card ppl">
  {legend([("A", "<b>No main menu</b>: one page, one goal. Startups get their own page", "blue"),
           ("B", "<b>Short form at the top</b>: name, work email, company, company size, role, country. No student or job-seeker option", "blue"),
           ("C", "<b>Proof next to the form</b>: partner logos and one result in numbers", "blue"),
           ("D", "<b>Three things we do</b>: startup scouting, pilots, innovation programs", "blue"),
           ("E", "<b>A case study, open</b>, not behind a form", "blue"),
           ("F", "<b>The form again</b> at the end", "blue")])}
  <div class="sub">Before and after · innovation platform page</div>
  <div class="bar">{"".join(f'<div><span>{l}</span><b class="o">{o}</b>{arrow()}<b class="n">{n}</b></div>' for l, o, n in lp_before_after)}</div>
  <div class="sub">Same template for</div>
  <div class="ps"><span>Corporate innovation</span><span>Startup scouting</span><span>Each Google theme</span></div>
 </div>
</div>""")


# 15 · 90-day plan
def tag(t):
    return f'<span class="tg {t.lower()}">{t}</span>'


def phase(days, name, tone, items):
    rows = "".join(f'<p class="pi">{"".join(tag(t) for t in tg)}<span class="tx">{x}</span></p>' for tg, x in items)
    return f'<div class="card phs"><div class="phh {tone}"><b>{days}</b><span>{name}</span></div>{rows}</div>'


slide("Plan", "90-day plan: build, learn, test, scale", f"""
<div class="g4">
 {phase("Days 1–7", "Build", "y", [
     (["Meta"], "New 3-campaign structure with the proven ads; pause old campaigns, traffic and losing ads"),
     (["Meta", "Google"], "Students and job seekers stop counting as results"),
     (["Google"], "Brand campaign apart, negatives, no startup or coworking extras, no homepage traffic"),
     (["Google"], "Semrush keyword research: US, UK, FR, DE, ES, IT"),
     (["Pages"], "Paid forms: drop student and job-seeker options; add company size")])}
 {phase("Days 8–30", "Learn", "b", [
     (["Meta"], "No changes for 7 days, then budget moves of 20% at most"),
     (["Meta"], "FR, DE, IT and ES versions of the best 3–4 ads, inside the same ads"),
     (["Meta"], "Test 1: the same report as static, carousel and video"),
     (["Google"], "Corporate ad groups from the research; weekly search-term review"),
     (["Pages"], "Build the corporate landing page"),
     (["Data"], "Weekly: ICP share of each ad's leads")])}
 {phase("Days 31–60", "Test", "p", [
     (["Meta"], "Test 2: talking head vs proof (case results, logos)"),
     (["Meta"], "Test 3: local topic and proof per market (partners, cases, events) vs global"),
     (["Pages"], "Local-language versions of the best report page"),
     (["Google"], "AI Max test once there are 30+ qualified conversions a month"),
     (["Data"], "Send qualified leads from the CRM to Meta and Google")])}
 {phase("Days 61–90", "Scale", "g", [
     (["Meta", "Google"], "Scale the winners in 20% steps; new creatives every 2–3 weeks"),
     (["Meta", "Google"], "Bid on qualified leads, not form fills"),
     (["Pages"], "Test an interactive assessment instead of a PDF"),
     (["Plan"], "2027 plan built on the results")])}
</div>
<div class="card dec"><div class="sub">To start, we need</div>
 <div class="g4 tight">
  <p class="bl">{num(1)}<span><b>A yes to the new Meta and Google structures</b>, same total budget.</span></p>
  <p class="bl">{num(2)}<span><b>US budget</b>: the US ad set needs about {usd(NEED_US)} a day to learn ({usd(NEED_EU)} in Europe); the plan gives it $55.</span></p>
  <p class="bl">{num(3)}<span><b>Web team time</b> in weeks 2–4 for the corporate landing page.</span></p>
  <p class="bl">{num(4)}<span><b>Local teams</b> to write or check the French, German, Italian and Spanish versions.</span></p>
 </div>
</div>""")


# ------------------------------------------------------------------ page
CSS = B.BASE_CSS + f"""
@page {{ size: 13.333in 7.5in; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ font-size: 12.5pt; line-height: 1.3; }}
.slide {{ width: 13.333in; height: 7.5in; padding: .36in .5in .42in; position: relative; overflow: hidden; background: {B.BG};
  break-after: page; display: flex; flex-direction: column; gap: .14in; }}
.slide:last-child {{ break-after: auto; }}
.kicker {{ color: {B.GRAY}; font-size: 10pt; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; }}
h1 {{ color: {B.DARK_BLUE}; font-size: 24pt; font-weight: 400; margin: 2px 0 0; line-height: 1.12; }}
h1::after {{ content: ""; display: block; width: 46px; height: 4px; border-radius: 2px; background: {B.YELLOW}; margin-top: 7px; }}
h3 {{ color: {B.DARK_BLUE}; font-size: 14pt; margin: 0; line-height: 1.2; }}
b {{ color: {B.DARK_BLUE}; }}
.pg {{ position: absolute; right: .5in; bottom: .18in; color: {B.GRAY}; font-size: 8.5pt; }}
.card {{ padding: .13in .16in; }}
.g2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: .15in; }}
.g3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: .15in; }}
.g3c {{ display: grid; grid-template-columns: 1.05fr .95fr 1.1fr; gap: .15in; }}
.g4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: .13in; }}
.tight {{ gap: .1in .2in; }}
.mk {{ width: 16px; height: 16px; flex: none; margin-top: 2px; }}
.nm {{ display: inline-flex; align-items: center; justify-content: center; min-width: 20px; height: 20px; border-radius: 10px; padding: 0 5px;
  background: {B.DARK_BLUE}; color: #fff; font-size: 10pt; font-weight: 700; flex: none; }}
.nm.good {{ background: {B.GOOD}; }} .nm.bad {{ background: {B.BAD}; }} .nm.blue {{ background: {B.BLUE}; }}
.bl {{ display: flex; gap: 8px; margin: 0 0 7px; font-size: 12pt; }}
.bl:last-child {{ margin-bottom: 0; }}
.ico {{ width: 22px; height: 22px; flex: none; }}
.arw {{ width: 24px; height: 13px; flex: none; }}
.arw.sm {{ width: 14px; height: 9px; }}
.arw.lg {{ width: 44px; height: 22px; }}
.ch {{ display: flex; align-items: center; gap: 8px; margin-bottom: 9px; padding-bottom: 6px; border-bottom: 2px solid {B.TINT}; }}
.ch.good {{ border-bottom-color: {B.GOOD}; }} .ch.bad {{ border-bottom-color: {B.BAD}; }} .ch.blue {{ border-bottom-color: {B.BLUE}; }}
.ch .mk {{ width: 20px; height: 20px; margin: 0; }}
.col .bl {{ font-size: 14pt; margin-bottom: 12px; }}
.sub {{ color: {B.GRAY}; font-size: 9.5pt; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; margin: 8px 0 5px; }}
.sub:first-child {{ margin-top: 0; }}
.cap {{ color: {B.GRAY}; font-size: 10pt; margin: 4px 0 8px; }}
.band {{ background: #fff; border-radius: {B.RADIUS}; box-shadow: {B.SHADOW}; border-left: 5px solid {B.YELLOW}; padding: .1in .16in; font-size: 12pt; }}
.band.good {{ border-left-color: {B.GOOD}; }}
/* Andromeda */
.vs {{ display: grid; grid-template-columns: 1fr 50px 1fr; align-items: stretch; flex: 1; }}
.mid {{ display: flex; align-items: center; justify-content: center; }}
.pnl {{ display: flex; flex-direction: column; }}
.ph {{ font-size: 15pt; font-weight: 700; margin-bottom: 8px; }}
.ph.bad {{ color: {B.BAD}; }} .ph.good {{ color: {B.GOOD}; }}
.mcs {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }}
.mc {{ background: {B.BG}; border-radius: 6px; padding: 6px 8px; }}
.mc span {{ display: block; font-size: 9.5pt; font-weight: 700; color: {B.TEXT}; margin-bottom: 5px; white-space: nowrap; overflow: hidden; }}
.sq {{ display: flex; gap: 3px; }}
.sq i {{ width: 20px; height: 20px; border-radius: 4px; background: {B.BLUE_LIGHT}; display: block; }}
.sq i.off {{ background: {B.TINT}; }}
.big {{ margin-top: auto; display: flex; align-items: baseline; gap: 10px; padding-top: 8px; border-top: 1px solid {B.TINT}; }}
.big b {{ font-size: 34pt; line-height: 1; }}
.big span {{ font-size: 13pt; }}
.big.bad b {{ color: {B.BAD}; }} .big.good b {{ color: {B.GOOD}; }}
.bc {{ border-radius: 8px; border: 2px solid {B.DARK_BLUE}; overflow: hidden; margin-bottom: 9px; }}
.bch {{ background: {B.DARK_BLUE}; color: #fff; font-weight: 700; font-size: 11pt; padding: 3px 9px; }}
.bas {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6px; padding: 6px; }}
.ba {{ background: {B.BG}; border-radius: 6px; padding: 5px; }}
.bah {{ font-size: 10pt; font-weight: 700; color: {B.TEXT}; margin-bottom: 5px; }}
.tts {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 3px; }}
.tt {{ background: #fff; border-radius: 4px; display: flex; align-items: center; justify-content: center; padding: 5px 2px; }}
.tt .ico {{ width: 22px; height: 22px; }}
/* split vs grouped */
.cmp {{ display: flex; flex-direction: column; gap: 8px; }}
.cmp .ch {{ margin-bottom: 0; }}
.mini {{ display: flex; align-items: center; gap: 4px; }}
.ms {{ flex: 1; display: flex; align-items: center; gap: 5px; background: {B.BG}; border-radius: 6px; padding: 4px 6px; font-size: 9pt; line-height: 1.15; min-height: 34px; }}
.ms .ico {{ width: 18px; height: 18px; }}
.chps {{ display: flex; flex-wrap: wrap; gap: 5px; }}
.chp {{ background: {B.BG}; border-left: 4px solid {B.TINT_2}; border-radius: 6px; padding: 3px 8px; font-size: 10.5pt; }}
.chp b {{ display: block; font-size: 10.5pt; color: {B.TEXT}; }}
.chp span {{ font-weight: 700; color: {B.DARK_BLUE}; }}
.chp.good {{ border-left-color: {B.GOOD}; }} .chp.good span {{ color: {B.GOOD}; }}
.chp.bad {{ border-left-color: {B.BAD}; }} .chp.bad span {{ color: {B.BAD}; }}
.who {{ display: flex; gap: 7px; align-items: flex-start; font-size: 11.5pt; color: {B.TEXT}; }}
.who .ico {{ width: 18px; height: 18px; }}
.kpis {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }}
.kpi {{ background: {B.BG}; border-radius: 6px; padding: 5px 8px; }}
.kpi b {{ display: block; font-size: 19pt; line-height: 1.05; }}
.kpi span {{ font-size: 9.5pt; color: {B.GRAY}; }}
.kpi.good b {{ color: {B.GOOD}; }} .kpi.bad b {{ color: {B.BAD}; }}
/* campaign cards */
.cc {{ display: flex; flex-direction: column; gap: 7px; }}
.cct {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 6px; }}
.cct h3 {{ font-size: 13pt; }}
.st {{ font-size: 8.5pt; font-weight: 700; border-radius: 9px; padding: 1px 8px; white-space: nowrap; }}
.st.live {{ background: {B.GOOD}; color: #fff; }} .st.off {{ background: {B.TINT}; color: {B.GRAY}; }} .st.warn {{ background: {B.BAD}; color: #fff; }}
.cc .ms {{ font-size: 9pt; padding: 4px 5px; gap: 3px; }}
.cc .ms .ico {{ width: 15px; height: 15px; }}
.cc .kpi b {{ font-size: 18pt; }}
.cc .sub {{ margin: 2px 0 0; }}
.cc .bl {{ font-size: 11.5pt; margin-bottom: 4px; }}
.cc .mk {{ width: 14px; height: 14px; }}
/* swaps */
.swh {{ display: grid; grid-template-columns: 1fr 40px 1fr; font-size: 10pt; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; margin-bottom: -6px; }}
.swh .bad {{ color: {B.BAD}; }} .swh .good {{ color: {B.GOOD}; }}
.sw {{ display: grid; grid-template-columns: 1fr 40px 1fr; align-items: stretch; }}
.swa {{ display: flex; align-items: center; justify-content: center; }}
.swp, .swf {{ display: flex; gap: 12px; align-items: center; padding: .12in .16in; border-left: 5px solid {B.BAD}; }}
.swf {{ border-left-color: {B.GOOD}; }}
.swi {{ width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex: none; }}
.swi.bad {{ background: #F3E3E8; }} .swi.good {{ background: #E2F0E4; }}
.sw b {{ display: block; font-size: 14pt; }}
.sw span {{ font-size: 12pt; }}
/* creatives */
.br {{ display: grid; grid-template-columns: 26px 1fr auto; gap: 8px; align-items: center; padding: 8px 0; border-bottom: 1px solid {B.TINT}; }}
.br:last-child {{ border-bottom: none; }}
.bn b {{ display: block; font-size: 12.5pt; color: {B.TEXT}; }}
.bn span, .bv span {{ font-size: 9.5pt; color: {B.GRAY}; }}
.bv {{ text-align: right; }}
.bv b {{ display: block; font-size: 17pt; color: {B.GOOD}; }}
.tl {{ position: relative; background: {B.BG}; border-radius: 7px; padding: 7px 5px 5px; display: flex; flex-direction: column; align-items: center;
  gap: 3px; text-align: center; font-size: 9pt; line-height: 1.15; color: {B.TEXT}; }}
.tl .ico {{ width: 24px; height: 24px; }}
.cnt {{ position: absolute; top: -6px; right: -4px; background: {B.DARK_BLUE}; color: #fff; font-size: 8pt; font-weight: 700; border-radius: 8px; padding: 0 5px; }}
.tl.good .cnt {{ background: {B.GOOD}; font-size: 10pt; }} .tl.bad .cnt {{ background: {B.BAD}; font-size: 10pt; }}
.fm {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 10px 0; }}
.fm .tl {{ padding-top: 12px; font-size: 10.5pt; }}
.fm .cnt {{ top: -9px; right: 50%; transform: translateX(50%); }}
.fm2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
.fm2 div {{ background: {B.BG}; border-radius: 6px; padding: 6px 8px; font-size: 10pt; border-left: 4px solid; }}
.fm2 .good {{ border-left-color: {B.GOOD}; }} .fm2 .bad {{ border-left-color: {B.BAD}; }}
.fm2 b {{ display: block; font-size: 16pt; }}
.fm2 .good b {{ color: {B.GOOD}; }} .fm2 .bad b {{ color: {B.BAD}; }}
.nx {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 9px 8px; margin-top: 10px; }}
.ps {{ display: flex; flex-wrap: wrap; gap: 5px; }}
.ps span {{ background: {B.TINT}; color: {B.DARK_BLUE}; font-weight: 700; font-size: 10pt; border-radius: 12px; padding: 2px 9px; }}
/* mock-up grids */
.goal {{ display: flex; gap: 8px; align-items: flex-start; background: #fff; border-radius: 8px; box-shadow: {B.SHADOW};
  border-left: 5px solid {B.GOOD}; padding: 6px 12px; font-size: 11.5pt; }}
.mg {{ display: grid; grid-template-columns: 2.3in 30px 2.3in 30px 1fr 30px 1.6in; row-gap: 8px; align-items: stretch; }}
.gh {{ grid-row: 1; color: {B.GRAY}; font-size: 9.5pt; font-weight: 700; letter-spacing: .06em; text-transform: uppercase;
  border-bottom: 2px solid {B.DARK_BLUE}; padding-bottom: 2px; }}
.gc {{ display: flex; }}
.gc > * {{ flex: 1; }}
.ga {{ display: flex; align-items: center; justify-content: center; }}
.cb {{ background: {B.DARK_BLUE}; color: #fff; border-radius: 8px; padding: 8px 10px; display: flex; gap: 8px; align-items: center; }}
.cb.test {{ background: {B.PURPLE}; }}
.cb b {{ color: #fff; display: block; font-size: 12.5pt; }}
.cb span {{ font-size: 10pt; color: {B.TINT_2}; }}
.sb {{ background: #fff; border-radius: 8px; box-shadow: {B.SHADOW}; border-left: 5px solid {B.TINT_2}; padding: 6px 10px; display: flex; gap: 8px; align-items: center; }}
.sb.good {{ border-left-color: {B.GOOD}; }}
.sb b {{ display: block; font-size: 12pt; }}
.sb span {{ font-size: 10pt; color: {B.GRAY}; }}
.pb {{ background: #fff; border-radius: 8px; box-shadow: {B.SHADOW}; padding: 6px 10px; display: flex; gap: 8px; align-items: center; }}
.pb b {{ display: block; font-size: 11.5pt; }}
.pb span {{ font-size: 9.5pt; color: {B.GRAY}; }}
.tls {{ display: flex; gap: 7px; align-items: stretch; flex-wrap: wrap; }}
.tls .tl {{ min-width: 64px; flex: 1; background: #fff; box-shadow: {B.SHADOW}; padding-top: 8px; }}
.same {{ display: flex; align-items: center; justify-content: center; border: 2px dashed {B.TINT_2}; border-radius: 8px; color: {B.GRAY}; font-size: 11pt; }}
.win {{ display: flex; align-items: center; background: #E2F0E4; color: {B.GOOD}; border-radius: 8px; padding: 6px 10px; font-size: 10.5pt; font-weight: 700; }}
.ba5 {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }}
.ba5 > div {{ background: #fff; border-radius: 8px; box-shadow: {B.SHADOW}; padding: 6px 10px; display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }}
.ba5 span {{ width: 100%; font-size: 9.5pt; color: {B.GRAY}; font-weight: 700; }}
.ba5 b.o {{ color: {B.BAD}; font-size: 16pt; text-decoration: line-through; text-decoration-thickness: 1.5px; }}
.ba5 b.n {{ color: {B.GOOD}; font-size: 16pt; }}
.ba5 em {{ font-style: normal; font-size: 10pt; color: {B.GRAY}; }}
.rs {{ display: flex; gap: 10px; align-items: center; background: #fff; border-radius: 8px; box-shadow: {B.SHADOW}; border-left: 5px solid {B.BLUE}; padding: 7px 12px; }}
.rs .ico {{ width: 26px; height: 26px; }}
.rs b {{ display: block; font-size: 12.5pt; }}
.rs span {{ font-size: 11pt; }}
.gg {{ grid-template-columns: 2.6in 30px 1fr 30px 2.1in 30px 2.1in; }}
.ags {{ display: flex; flex-wrap: wrap; gap: 5px; align-items: center; }}
.agc {{ background: #fff; box-shadow: {B.SHADOW}; border-left: 4px solid {B.GOOD}; border-radius: 6px; padding: 4px 8px; font-size: 10.5pt; font-weight: 700; color: {B.TEXT}; }}
/* Google findings */
.cons {{ padding: .1in .16in; }}
.cr {{ display: flex; align-items: center; gap: 14px; }}
.sts {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; flex: 1; }}
.stt {{ background: {B.BG}; border-left: 4px solid {B.BAD}; border-radius: 6px; padding: 4px 8px; }}
.stt span {{ display: block; font-size: 9.5pt; color: {B.TEXT}; }}
.stt b {{ color: {B.BAD}; font-size: 16pt; }}
.rgs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6px; width: 3.4in; }}
.rg {{ background: #E2F0E4; border-left: 4px solid {B.GOOD}; border-radius: 6px; padding: 4px 8px; }}
.rg span {{ display: block; font-size: 9.5pt; color: {B.TEXT}; }}
.rg b {{ color: {B.GOOD}; font-size: 20pt; }}
/* wireframes */
.wf {{ position: relative; background: #fff; border: 1.5px solid {B.TINT_2}; border-radius: 6px; overflow: hidden; margin: 6px 0 8px; }}
.wb {{ background: {B.TINT}; height: 16px; display: flex; align-items: center; gap: 3px; padding: 0 6px; }}
.wb i {{ width: 5px; height: 5px; border-radius: 50%; background: #fff; display: block; }}
.wu {{ margin-left: 5px; background: #fff; border-radius: 4px; font-size: 7pt; color: {B.GRAY}; padding: 0 6px; line-height: 11px; white-space: nowrap; overflow: hidden; }}
.wc {{ position: relative; height: calc(100% - 16px); }}
.w {{ position: absolute; }}
.w.hd {{ font-size: 9.5pt; font-weight: 700; color: {B.DARK_BLUE}; line-height: 1.15; }}
.w.hd.c {{ text-align: center; }}
.w.hd.xl {{ font-size: 12pt; }}
.ppw .w.hd.xl {{ font-size: 17pt; }}
.w.fld.hl {{ border-color: {B.BAD}; border-width: 1.5px; }}
.w.fl {{ font-size: 7pt; color: {B.BAD}; text-align: right; }}
.w.ln {{ background: {B.TINT}; border-radius: 2px; }}
.w.img {{ background: {B.TINT}; border-radius: 4px; }}
.w.frm {{ background: {B.BG}; border: 1px solid {B.TINT_2}; border-radius: 5px; }}
.w.frm.cut {{ border-bottom: none; }}
.ft {{ position: absolute; left: 8px; top: 4px; font-size: 8pt; font-weight: 700; color: {B.DARK_BLUE}; }}
.w.fld {{ background: #fff; border: 1px solid {B.TINT_2}; border-radius: 2px; }}
.w.btn {{ background: {B.DARK_BLUE}; border-radius: 3px; }}
.w.stat {{ background: {B.BG}; border-radius: 4px; font-size: 9pt; font-weight: 700; color: {B.DARK_BLUE}; text-align: center; line-height: 34px; }}
.w.lg {{ background: {B.TINT_2}; border-radius: 6px; }}
.w.fold {{ border-top: 1.5px dashed {B.BAD}; height: 0 !important; }}
.w.fold.ok {{ border-top-color: {B.GOOD}; }} .w.fl.ok {{ color: {B.GOOD}; }}
.w.nav {{ background: {B.TINT_2}; border-radius: 3px; }}
.w.cta {{ background: {B.DARK_BLUE}; border-radius: 4px; }}
.w.nl {{ background: {B.BG}; border: 1px dashed {B.TINT_2}; border-radius: 4px; font-size: 7.5pt; color: {B.GRAY}; text-align: center; line-height: 14px; }}
.w.brk {{ border-top: 1.5px dashed {B.TINT_2}; border-bottom: 1.5px dashed {B.TINT_2}; font-size: 7.5pt; color: {B.GRAY};
  display: flex; align-items: center; justify-content: center; }}
.w.chat {{ background: {B.BLUE}; border-radius: 50%; }}
.w.res {{ background: #E2F0E4; border-radius: 4px; font-size: 8pt; color: {B.GOOD}; font-weight: 700; display: flex; align-items: center; justify-content: center; }}
.w.card3 {{ background: {B.BG}; border-radius: 5px; font-size: 9.5pt; font-weight: 700; color: {B.DARK_BLUE}; padding: 8px 10px; }}
.w.case {{ background: {B.TINT}; border-radius: 5px; font-size: 8.5pt; font-weight: 700; color: {B.DARK_BLUE}; padding: 8px 10px; }}
.w.cta2 {{ background: {B.BG}; border: 1px solid {B.TINT_2}; border-radius: 5px; font-size: 8.5pt; font-weight: 700; color: {B.DARK_BLUE}; padding: 8px 10px; }}
.pin {{ position: absolute; width: 17px; height: 17px; border-radius: 50%; color: #fff; font-size: 8.5pt; font-weight: 700; text-align: center; line-height: 17px;
  box-shadow: 0 0 0 2px #fff; }}
.pin.good {{ background: {B.GOOD}; }} .pin.bad {{ background: {B.BAD}; }} .pin.blue {{ background: {B.BLUE}; }}
.lp {{ display: flex; flex-direction: column; }}
.lph {{ display: flex; justify-content: space-between; align-items: center; gap: 6px; }}
.lph h3 {{ font-size: 13pt; }}
.lgd {{ display: flex; gap: 7px; margin: 0 0 7px; font-size: 11.5pt; align-items: flex-start; }}
.lgd .nm {{ min-width: 18px; height: 18px; font-size: 9pt; }}
.pp {{ display: grid; grid-template-columns: 6.1in 1.75in 1fr; gap: .14in; flex: 1; }}
.ppw .wf {{ margin: 0; }}
.ph1 {{ width: 132px; height: 400px; border: 2px solid {B.TINT_2}; border-radius: 16px; padding: 8px 6px; margin: 4px auto 0; background: #fff; }}
.ph1c {{ position: relative; height: 100%; }}
.ppl .lgd {{ font-size: 11pt; margin-bottom: 8px; }}
.bar > div {{ display: grid; grid-template-columns: 1fr auto 24px auto; gap: 8px; align-items: center; padding: 5px 0; border-bottom: 1px solid {B.TINT}; }}
.bar > div:last-child {{ border-bottom: none; }}
.bar span {{ font-size: 11pt; }}
.bar b {{ font-size: 12pt; }}
.bar b.o {{ color: {B.BAD}; text-decoration: line-through; text-decoration-thickness: 1.5px; }} .bar b.n {{ color: {B.GOOD}; }}
/* plan */
.phs {{ display: flex; flex-direction: column; gap: 6px; }}
.phh {{ border-radius: 7px; padding: 6px 10px; margin-bottom: 4px; }}
.phh b {{ display: block; font-size: 14pt; }}
.phh span {{ font-size: 10.5pt; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }}
.phh.y {{ background: #FBF8D0; }} .phh.b {{ background: {B.TINT}; }} .phh.p {{ background: #E7E7F7; }} .phh.g {{ background: #E2F0E4; }}
.pi {{ margin: 0 0 2px; font-size: 10.8pt; line-height: 1.24; }}
.pi .tx {{ display: block; margin-top: 2px; }}
.tg {{ display: inline-block; font-size: 8pt; font-weight: 700; border-radius: 8px; padding: 0 6px; margin-right: 3px; color: #fff; background: {B.GRAY}; }}
.tg.meta {{ background: {B.BLUE}; }} .tg.google {{ background: {B.DARK_BLUE}; }} .tg.pages {{ background: {B.PURPLE}; }}
.tg.data {{ background: {B.GOOD}; }} .tg.plan {{ background: {B.GRAY}; }}
.dec {{ border-left: 5px solid {B.YELLOW}; }}
.dec .bl {{ font-size: 11.5pt; }}
/* cover */
.cover {{ background: {B.DARK_BLUE}; justify-content: center; padding: .8in .9in; }}
.cover .ck {{ color: {B.TINT_2}; font-size: 11pt; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }}
.cover .ctt {{ color: #fff; font-size: 44pt; line-height: 1.05; margin: .12in 0 .1in; }}
.cover .ctt::after {{ content: ""; display: block; width: 70px; height: 5px; border-radius: 3px; background: {B.YELLOW}; margin-top: .16in; }}
.cover .csub {{ color: {B.TINT}; font-size: 17pt; max-width: 10.5in; }}
.cover .scope {{ display: flex; gap: .5in; margin-top: .55in; }}
.cover .scope div {{ color: {B.TINT_2}; font-size: 11pt; }}
.cover .scope b {{ display: block; color: #fff; font-size: 22pt; }}
.cover .by {{ position: absolute; left: .9in; bottom: .55in; color: {B.TINT_2}; font-size: 11.5pt; }}
/* ICP controls */
.ct {{ display: grid; grid-template-columns: 2.05in 1fr 30px 1.12fr; gap: 0 10px; align-items: stretch; }}
.cth {{ font-size: 10pt; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; color: {B.GRAY}; margin-bottom: -6px; }}
.cth .bad {{ color: {B.BAD}; }} .cth .good {{ color: {B.GOOD}; }}
.ctl {{ display: flex; align-items: center; gap: 9px; }}
.ctl .ico {{ width: 26px; height: 26px; }}
.ctl b {{ font-size: 14.5pt; line-height: 1.15; }}
.ctx {{ display: flex; gap: 10px; align-items: center; padding: .1in .14in; border-left: 5px solid {B.BAD}; font-size: 13pt; line-height: 1.25; }}
.ctx.good {{ border-left-color: {B.GOOD}; }}
/* local slide */
.s-local .pnl {{ gap: 9px; }}
.s-local .ph {{ margin-bottom: 0; }}
.s-local .sub {{ margin: 4px 0 -3px; }}
.s-local .bl {{ font-size: 12.5pt; margin-bottom: 6px; }}
.s-local .big b {{ font-size: 30pt; white-space: nowrap; }}
.s-local .big span {{ font-size: 12.5pt; }}
.s-local .chp, .s-local .chp b {{ font-size: 11.5pt; }}
.sar {{ display: grid; grid-template-columns: 1.6in 1fr; align-items: center; gap: 8px; }}
.sar > b {{ font-size: 12.5pt; }}
.lvs {{ display: grid; grid-template-columns: 1.5in 30px 1fr; align-items: center; gap: 6px 10px; background: {B.BG}; border-radius: 8px; padding: 10px 12px; }}
.lva {{ background: #fff; border-radius: 8px; box-shadow: {B.SHADOW}; padding: 10px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 3px; }}
.lva .ico {{ width: 28px; height: 28px; }}
.lva b {{ font-size: 13pt; }}
.lva span {{ font-size: 10pt; color: {B.GRAY}; }}
.fan {{ display: grid; gap: 5px; }}
.fr {{ display: flex; align-items: center; gap: 8px; font-size: 11.5pt; }}
.fr .lb {{ width: 34px; text-align: center; }}
.lvc {{ grid-column: 1 / -1; font-size: 11pt; color: {B.TEXT}; }}
.lb {{ display: inline-block; font-size: 10pt; font-weight: 700; color: {B.DARK_BLUE}; background: {B.TINT}; border-radius: 6px; padding: 2px 7px; }}
.lb.def {{ background: {B.DARK_BLUE}; color: #fff; }}
.lvl {{ display: flex; align-items: center; gap: 4px; margin-top: 5px; font-size: 10pt; color: {B.GRAY}; font-weight: 700; }}
/* per-slide sizing: fill the page with bigger visuals */
.s-sum .col .bl {{ font-size: 15.5pt; margin-bottom: 16px; }}
.s-sum .ch h3 {{ font-size: 16pt; }}
.s-sum .ba5 > div, .s-meta .ba5 > div, .s-goog .ba5 > div {{ padding: 10px 14px; }}
.s-sum .ba5 span, .s-meta .ba5 span, .s-goog .ba5 span {{ font-size: 10.5pt; }}
.s-sum .ba5 b.o, .s-sum .ba5 b.n, .s-meta .ba5 b.o, .s-meta .ba5 b.n, .s-goog .ba5 b.o, .s-goog .ba5 b.n {{ font-size: 23pt; }}
.s-data .g2 {{ flex: 1; }}
.s-data .cmp {{ gap: 11px; }}
.s-data .cmp .sub {{ margin: 0 0 -5px; }}
.s-data .cmp .ch h3 {{ font-size: 15pt; }}
.s-data .cmp .kpis {{ margin-top: auto; }}
.s-data .ms {{ font-size: 10.5pt; min-height: 50px; }}
.s-data .ms .ico {{ width: 22px; height: 22px; }}
.s-data .chp, .s-data .chp b {{ font-size: 12pt; }}
.s-data .chp {{ padding: 5px 10px; }}
.s-data .who {{ font-size: 12.5pt; }}
.s-data .kpi {{ padding: 8px 12px; }}
.s-data .kpi b {{ font-size: 28pt; }}
.s-data .kpi span {{ font-size: 11pt; }}
.s-data .band {{ font-size: 13pt; }}
.sxs {{ display: flex; align-items: stretch; gap: 4px; }}
.sxs .arw {{ align-self: center; }}
.sx {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 2px;
  background: {B.BG}; border-radius: 7px; padding: 7px 4px 6px; }}
.sx .ico {{ width: 20px; height: 20px; }}
.sx b {{ font-size: 19pt; line-height: 1; }}
.sx span {{ font-size: 9pt; line-height: 1.15; color: {B.TEXT}; }}
.s-work .g3 {{ flex: 1; }}
.s-work .cc {{ gap: 9px; }}
.s-work .cct h3 {{ font-size: 14pt; }}
.s-work .cc .kpi b {{ font-size: 23pt; }}
.s-work .who {{ font-size: 12pt; }}
.s-work .cc .sub {{ margin-top: 4px; }}
.s-work .cc .bl {{ font-size: 12.5pt; margin-bottom: 6px; }}
.s-crea .g3c {{ flex: 1; }}
.s-crea .br {{ padding: 11px 0; }}
.s-crea .br .ico {{ width: 26px; height: 26px; }}
.s-crea .bn b {{ font-size: 13.5pt; }}
.s-crea .bn span, .s-crea .bv span {{ font-size: 10pt; }}
.s-crea .bv b {{ font-size: 20pt; }}
.s-crea .fm {{ gap: 12px; margin: 18px 0 14px; }}
.s-crea .fm .tl {{ font-size: 13.5pt; padding: 26px 6px 16px; }}
.s-crea .fm .tl .ico {{ width: 48px; height: 48px; }}
.s-crea .fm .cnt {{ font-size: 12pt; top: -11px; }}
.s-crea .fm2 div {{ font-size: 12.5pt; padding: 14px 12px; }}
.s-crea .fm2 b {{ font-size: 28pt; }}
.s-crea .nx {{ gap: 14px 10px; margin-top: 16px; }}
.s-crea .nx .tl {{ font-size: 11.5pt; padding: 18px 6px 12px; }}
.s-crea .nx .tl .ico {{ width: 36px; height: 36px; }}
.s-crea .nx .cnt {{ font-size: 9.5pt; }}
.s-crea .bl {{ font-size: 13pt; margin-bottom: 8px; }}
.loc {{ display: flex; align-items: center; gap: 12px; background: {B.BG}; border-left: 4px solid {B.GOOD}; border-radius: 6px; padding: 8px 12px; margin-top: 10px; }}
.loc b {{ font-size: 25pt; color: {B.GOOD}; line-height: 1; }}
.loc span {{ font-size: 12pt; }}
.s-crea .ps {{ gap: 7px; }}
.s-crea .ps span {{ font-size: 12pt; padding: 3px 11px; }}
.s-crea .sub {{ margin-top: 18px; }}
.s-crea .sub:first-child {{ margin-top: 0; }}
.s-meta .goal {{ font-size: 12.5pt; padding: 9px 14px; }}
.s-meta .mg {{ row-gap: 10px; }}
.s-meta .cb {{ padding: 14px; }}
.s-meta .cb .ico {{ width: 26px; height: 26px; }}
.s-meta .cb b {{ font-size: 15pt; }}
.s-meta .cb span {{ font-size: 11pt; }}
.s-meta .sb {{ padding: 12px; }}
.s-meta .sb b {{ font-size: 13.5pt; }}
.s-meta .sb span {{ font-size: 11pt; }}
.s-meta .tls .tl {{ padding: 15px 5px 9px; font-size: 10pt; }}
.s-meta .tls .tl .ico {{ width: 28px; height: 28px; }}
.s-meta .pb {{ padding: 10px 12px; }}
.s-meta .pb b {{ font-size: 13pt; }}
.s-meta .same {{ font-size: 12pt; }}
.s-meta .win {{ font-size: 11.5pt; }}
.s-gfind .g2 {{ flex: 1; }}
.s-goog .rs b {{ font-size: 13.5pt; }}
.s-goog .rs span {{ font-size: 12pt; }}
.s-goog .rs {{ padding: 9px 14px; }}
.s-goog .mg {{ row-gap: 12px; }}
.s-goog .cb {{ padding: 12px 14px; }}
.s-goog .cb b {{ font-size: 14pt; }}
.s-goog .cb span {{ font-size: 11pt; }}
.s-goog .agc {{ font-size: 11.5pt; padding: 6px 10px; }}
.s-goog .ags {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7px; align-content: center; }}
.s-goog .ags.one {{ display: flex; }}
.s-goog .tls .tl {{ padding: 14px 5px 9px; font-size: 10.5pt; }}
.s-goog .tls .tl .ico {{ width: 28px; height: 28px; }}
.s-goog .pb {{ padding: 10px 12px; }}
.s-goog .pb b {{ font-size: 13pt; }}
.s-goog .goal {{ font-size: 12.5pt; padding: 9px 14px; }}
.gt {{ padding: .09in .16in .11in; }}
.gtr {{ display: grid; grid-template-columns: 1.25fr 26px 1.45fr 26px .55fr 26px 1.25fr; align-items: start; }}
.gtr > .arw {{ justify-self: center; margin-top: 8px; }}
.gtt {{ display: flex; align-items: center; gap: 7px; margin-bottom: 6px; }}
.gtt .ico {{ width: 24px; height: 24px; }}
.gtt b {{ font-size: 22pt; line-height: 1; }}
.gtt span {{ font-size: 10.5pt; line-height: 1.15; color: {B.TEXT}; }}
.gt .chps {{ gap: 4px; }}
.gt .chp, .gt .chp b {{ font-size: 10.5pt; }}
.gt .chp {{ padding: 2px 7px; }}
.gt .chp b {{ display: inline; margin-right: 4px; }}
.s-gfind .cons .sub {{ font-size: 10.5pt; }}
.s-gfind .stt {{ padding: 7px 10px; }}
.s-gfind .stt span, .s-gfind .rg span {{ font-size: 10.5pt; }}
.s-gfind .stt b {{ font-size: 19pt; }}
.s-gfind .rg {{ padding: 7px 10px; }}
.s-gfind .rg b {{ font-size: 24pt; }}
.s-gfind .col .bl {{ font-size: 13pt; margin-bottom: 8px; }}
.s-gfind .ch {{ margin-bottom: 7px; }}
"""

COVER = ('<section class="slide cover"><div class="ck">Plug and Play · Paid media · October 2026</div>'
         '<div class="ctt">Paid media audit and new structure</div>'
         '<div class="csub">Meta and Google Search: what works, what doesn\'t, and how we rebuild for post-Andromeda Meta</div>'
         f'<div class="scope"><div><b>{usd(180940.06)}</b>Meta</div><div><b>{eur(80055.62)}</b>Google Search</div>'
         '<div><b>1 Jan – 13 Oct 2026</b>spend covered</div></div>'
         '<div class="by">Felipe Cárdenas · Performance Marketing &amp; CRM</div></section>')


def render():
    total = len(SLIDES) + 1
    out = [COVER]
    for i, (kicker, title, body, cls) in enumerate(SLIDES, 2):
        out.append(f'<section class="slide {cls}"><div><div class="kicker">{kicker}</div><h1>{title}</h1></div>{body}'
                   f'<div class="pg">{i} / {total}</div></section>')
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Paid media audit 2026</title>"
            f"<style>{CSS}</style></head><body>{''.join(out)}</body></html>")


FIT_JS = """<script>window.addEventListener('load', () => {
  const out = [];
  document.querySelectorAll('.slide').forEach((s, i) => {
    const pg = s.querySelector('.pg'), limit = pg ? pg.getBoundingClientRect().top : s.getBoundingClientRect().bottom;
    let low = 0;
    s.querySelectorAll('*').forEach(el => { if (!pg || !pg.contains(el)) { const r = el.getBoundingClientRect(); if (r.height) low = Math.max(low, r.bottom); } });
    out.push((i + 1) + ':' + Math.round(limit - low));
  });
  document.body.setAttribute('data-fit', out.join(' '));
});</script>"""


def check_fit(html_path):
    """Free space (px) between each slide's lowest element and the page number; negative = content clipped."""
    check = html_path.replace(".html", ".check.html")
    open(check, "w", encoding="utf-8").write(open(html_path, encoding="utf-8").read().replace("</body>", FIT_JS + "</body>"))
    dom = subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--window-size=1280,720",
                          "--virtual-time-budget=3000", "--dump-dom", "file://" + os.path.abspath(check)],
                         capture_output=True, text=True).stdout
    os.remove(check)
    fit = re.search(r'data-fit="([^"]*)"', dom)
    pairs = [p.split(":") for p in fit.group(1).split()] if fit else []
    tight = [f"slide {n} ({v}px)" for n, v in pairs if int(v) < 2]
    print("free space under each slide (px):", " ".join(f"{n}:{v}" for n, v in pairs))
    if tight:
        print("WARNING: content clipped or touching the page number on", ", ".join(tight))


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    html_path = os.path.join(out_dir, STEM + ".html")
    open(html_path, "w", encoding="utf-8").write(render())
    print("written", html_path, "·", len(SLIDES) + 1, "slides")
    print(f"numbers: CPL Europe {CPL_EU:.2f} · US {CPL_US:.2f} · leads per ad set a week {LEADS_PER_ADSET_WEEK:.2f} · "
          f"learning budget EU {NEED_EU:.0f} US {NEED_US:.0f} · new leads a week EU {NEW_EU:.0f} US {NEW_US:.0f}")
    check_fit(html_path)
    if "--pdf" in sys.argv:
        font = B.font_in_use()
        pdf = os.path.join(out_dir, STEM + ".pdf")
        subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", "file://" + os.path.abspath(html_path)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
        fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
        names = {re.sub(r"^[A-Z]{6}\+", "", ln.split()[0]) for ln in fonts.splitlines()[2:] if ln.strip()}
        other = sorted(n for n in names if font.replace(" ", "").lower() not in n.lower())
        print(f"PDF: {pdf} · {pages} pages · font {font}"
              + (f" · WARNING: {pages} pages for {len(SLIDES) + 1} slides" if pages != len(SLIDES) + 1 else "")
              + (f" · WARNING non-brand fonts: {other}" if other else ""))


if __name__ == "__main__":
    main()
