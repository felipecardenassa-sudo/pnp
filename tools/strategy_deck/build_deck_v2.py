"""Paid media audit 2026, deck v2 – Meta, Google Search and ChatGPT Ads, for Raúl and Tereza (16:9 PDF, HTML → Chromium).

Built from the read-only browser audit of 14 Oct 2026 (Claude in Chrome, prompts/browser_audit_paid_media.md; report
saved as reports/audit/paid_media_audit_2026-10-14.md) and the agency's Notion account page (test log empty, 7-day rule). The audience knows paid media: no basics. Each channel gets its structure today as a
diagram with counts (campaigns → ad sets → ads → landing pages), what's going well and wrong marked on it, then the
proposed structure with before → after numbers. Rules (CLAUDE.md): to the point, no charts, no source citations,
no HubSpot data; Meta, Google Search and ChatGPT only; brand design, no logo.
Money in USD: Meta bills in USD; Google Ads and ChatGPT Ads bill in EUR and are converted at FX.

Usage (from the repo root): python3 -I tools/strategy_deck/build_deck_v2.py OUT_DIR [--pdf]
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "brand"))
import brand as B  # noqa: E402

STEM = "Paid_Media_Audit_2026"
CHROMIUM = "/opt/pw-browsers/chromium"
FX = 1.1177          # 1 EUR = 1.1177 USD (CLAUDE.md, live rate 13 Oct 2026)
PERIOD = "1 Jan – 13 Oct 2026"
L30 = "14 Sep – 13 Oct 2026"


def usd(x, d=0):
    return f"${x:,.{d}f}"


def eur(x, d=0):
    """A Google Ads or ChatGPT Ads amount (EUR as billed) shown in USD."""
    return usd(x * FX, d)


# ------------------------------------------------------------------ drawn symbols (Trebuchet MS has no arrows or ticks)
def arrow():
    return (f'<svg class="arrow" viewBox="0 0 30 16" aria-hidden="true"><path d="M2 8h23M19 2l6 6-6 6" fill="none" '
            f'stroke="{B.GRAY}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def tick(color=B.GOOD):
    return (f'<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="{color}"/>'
            '<path d="M4.4 8.3l2.4 2.4 4.8-5" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def bang(color=B.BAD):
    return (f'<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="{color}"/>'
            '<path d="M8 4v5" stroke="#fff" stroke-width="2" stroke-linecap="round"/><circle cx="8" cy="11.8" r="1.1" fill="#fff"/></svg>')


def num(n):
    return f'<span class="n">{n}</span>'


# ------------------------------------------------------------------ structure diagram
def cell(title, sub="", tone="", small=""):
    return (f'<div class="cl {tone}"><div class="ct">{title}</div>' + (f'<div class="cs">{sub}</div>' if sub else "")
            + (f'<div class="cm">{small}</div>' if small else "") + "</div>")


def chips(items, note=""):
    out = "".join(f'<div class="cp {tone}"><b>{name}</b>{f"<span>{sub}</span>" if sub else ""}</div>' for name, sub, tone in items)
    return f'<div class="cps"><div class="cpw">{out}</div>{f"<div class=cpn>{note}</div>" if note else ""}</div>'


def structure(heads, rows, widths):
    """heads = [(count, label)]; rows = [[cell html per level]]; widths = CSS widths per level."""
    cols, hdr = [], []
    for i, (w, (count, label)) in enumerate(zip(widths, heads)):
        if i:
            cols.append("28px")
            hdr.append("<div></div>")
        cols.append(w)
        hdr.append(f'<div class="hd"><b>{count}</b>{label}</div>')
    body = []
    for row in rows:
        for i, c in enumerate(row):
            if i:
                body.append(f'<div class="lk">{arrow()}</div>')
            body.append(c)
    return f'<div class="st" style="grid-template-columns:{" ".join(cols)}">{"".join(hdr)}{"".join(body)}</div>'


def goal(text, tone):
    mark = tick() if tone == "good" else bang()
    return f'<div class="goal {tone}">{mark}<span>{text}</span></div>'


def verdict(well, wrong):
    def col(title, rows, tone):
        mark = tick() if tone == "good" else bang()
        return (f'<div class="card vd"><div class="top {tone}"></div><div class="vh">{title}</div>'
                + "".join(f"<p>{mark}<span>{r}</span></p>" for r in rows) + "</div>")
    return f'<div class="cols2">{col("Going well", well, "good")}{col("Going wrong", wrong, "bad")}</div>'


def changes(rows):
    def row(label, before, after):
        return (f'<div class="chg"><div class="cl2">{label}</div><div class="bf">{before}</div>'
                f'<div class="ca">{arrow()}</div><div class="af">{after}</div></div>')
    half = (len(rows) + 1) // 2
    return ('<div class="card chgs"><div class="vh">What changes</div><div class="cols2 tight">'
            f'<div>{"".join(row(*r) for r in rows[:half])}</div><div>{"".join(row(*r) for r in rows[half:])}</div></div></div>')


# ------------------------------------------------------------------ slides
SLIDES = []


def slide(kicker, title, body, note=""):
    SLIDES.append((kicker, title, body, note))


# 2 · summary
slide("Summary", "The short version", f"""
<div class="cols3">
 <div class="card col"><div class="top good"></div><h3>Going well</h3>
  <p>{tick()}<span><b>Meta Deep Tech report ads</b> bring the cheapest leads: $4–$13 CPL in all 7 locations.</span></p>
  <p>{tick()}<span><b>Meta retargeting</b> with a press quote: $13 CPL. Europe and the Middle East cost $8–$13 CPM vs $33–$44 in the US.</span></p>
  <p>{tick()}<span><b>Google corporate searches and copy</b> convert best: 24% conversion rate in the Innovation ad group.</span></p>
 </div>
 <div class="card col"><div class="top bad"></div><h3>Going wrong</h3>
  <p>{bang()}<span><b>Both platforms optimise to any form fill</b>, students and job seekers included, not qualified leads.</span></p>
  <p>{bang()}<span><b>Meta is spread thin</b>: 9 campaigns, 30 ad sets, 243 ads on $160 a day (about $4 per ad set).</span></p>
  <p>{bang()}<span><b>Google</b>: 60% of Search spend lands on the homepage (no form); 37% buys our own brand name.</span></p>
  <p>{bang()}<span><b>ChatGPT test</b>: {eur(229.56)}, 43 clicks, 0 leads. Homepage, no tracking, US only.</span></p>
 </div>
 <div class="card col"><div class="top blue"></div><h3>Proposal</h3>
  <p>{num(1)}<span><b>Meta</b>: 4 campaigns, 7 ad sets, 3–5 ads each. Scale Deep Tech and AI, test the rest. Same $160 a day.</span></p>
  <p>{num(2)}<span><b>Google</b>: brand in its own campaign, corporate-only ad groups by region, a form behind every ad.</span></p>
  <p>{num(3)}<span><b>All channels</b>: optimise to corporate forms now, qualified leads next. ChatGPT Test 2 with a form page.</span></p>
 </div>
</div>""", note=f"CPL = cost per lead (Meta results: forms sent on our pages), last 30 days ({L30}). CPM: this year. Google and ChatGPT converted from EUR at {FX}.")

# 3 · Meta today
slide("Meta · today", "Meta today: 9 campaigns, 30 ad sets, 243 ads on $160 a day", f"""
{goal("Goal of the lead campaigns: any form sent on our pages (“welcome conversion”), students and job seekers included", "bad")}
{structure([("9", "campaigns"), ("30", "live ad sets"), ("243", "live ads")], [
    [cell("7 location campaigns", "$10–$26 a day each · $113 in total", "",
          "US-California · US East Coast · US &amp; Canada · US Middle-South · EMEA · Middle East · Western Europe"),
     chips([("Deep Tech", "$4–$13 CPL", "good"), ("AI", "$8–$56", ""), ("Brand", "up to $140", "bad"),
            ("Health", "up to $51", "bad"), ("Innovation Leader", "off", "off")],
           "Same 4 live topics in every location = 28 ad sets, about $4 a day each"),
     cell("About 8 ads per ad set", "One quantum video exists as 12+ copies", "bad")],
    [cell("1 retargeting campaign", "Worldwide · $41 a day", "good"),
     chips([("Past sign-ups (180 days)", "$13 CPL · Meta may widen it", "good")]),
     cell("53 ads in one ad set", "Best this year: press-quote image, $15.66 CPL")],
    [cell("1 traffic campaign", "US · $5 a day"),
     chips([("1 ad set", "landing-page views", "")]),
     cell("Lands on the AI CoE page", "No form", "bad")],
], ["2.9in", "5.2in", "2.9in"])}
{verdict(["<b>Deep Tech</b> is the cheapest topic in every location ($4–$13 CPL). Best ad this year: the AI &amp; robotics report video, $4.10 CPL in EMEA.",
          "<b>Retargeting</b> works at $13 CPL; the press-quote image is its best ad.",
          "<b>Europe and the Middle East</b> are cheap to reach: $8–$13 CPM vs $33–$44 in the US."],
         ["<b>Too thin to learn</b>: about $4 a day per ad set, about 8 ads each, duplicates splitting the data.",
          "<b>Expensive pockets</b>: Health in the US $36–$51 CPL, Brand in California $140 for 1 lead. The healthcare video marked to pause still runs.",
          "<b>FR_Alibaba</b> (traffic, our internal team) took 41% of the last 30 days' spend: $3,845 for $0.03 clicks in Turkey, Greece and Eastern Europe. Ended 5 Oct."])}
""", note=f"CPL: last 30 days ({L30}); CPM and best ads: this year. Live = delivering on 13 Oct. Account history: 83 campaigns, 272 ad sets, 1,785 ads.")

# 4 · Meta proposal
slide("Meta · proposal", "Meta proposal: 4 campaigns, 7 ad sets, 3–5 ads each, same $160 a day", f"""
{goal("New goal: a corporate form sent (no student or job-seeker answers), then qualified leads from the CRM", "good")}
{structure([("4", "campaigns"), ("7", "ad sets"), ("21–35", "ads")], [
    [cell("Scale · EMEA &amp; Middle East", "CBO · about $45 a day", "good"),
     chips([("Deep Tech reports", "", "good"), ("AI for enterprise", "", "good")]),
     cell("3–5 ads per ad set", "One copy of each ad")],
    [cell("Scale · US &amp; Canada", "CBO · about $45 a day", "good"),
     chips([("Deep Tech reports", "", "good"), ("AI for enterprise", "", "good")]),
     cell("3–5 ads per ad set", "One copy of each ad")],
    [cell("Test", "ABO · about $30 a day (20%)"),
     chips([("New offer or creative", "$15 a day", ""), ("New offer or creative", "$15 a day", "")], "Read on day 7; winners move to Scale"),
     cell("3–5 ads per ad set", "Health, Brand and case studies go here first")],
    [cell("Retargeting · worldwide", "About $40 a day", "good"),
     chips([("Past sign-ups and visitors", "strict audience", "good")]),
     cell("3–5 ads", "Press quotes, case studies")],
], ["2.9in", "5.2in", "2.9in"])}
{changes([("Campaigns", "9", "4"), ("Ad sets", "30", "7"), ("Ads", "243", "21–35"), ("Budget per ad set", "about $4 a day", "$15–$40 a day"),
          ("Goal", "any form", "corporate form, then qualified"), ("Copies of one ad", "up to 12+", "1"),
          ("Tests", "none logged", "2 a month, read on day 7"), ("Total budget", "$160 a day", "same; split by results, weekly")])}
""", note="Scale = proven topics. Region budgets start equal and move weekly to the lower CPL.")

# 5 · Google today
slide("Google Search · today", f"Google Search today: 3 campaigns, 9 ad groups, 9 ads on {eur(68)} a day", f"""
{goal("Goal since 28 Sep: any lead form (qualified leads were taken out that day) · keywords: all broad match + AI Max", "bad")}
{structure([("3", "campaigns"), ("9", "ad groups"), ("9", "ads"), ("Where", "clicks land")], [
    [cell("US &amp; Canada", f"{eur(30)} a day · capped by budget", "", "300 keywords"),
     chips([("Brand", "46% of spend", "bad"), ("Startup collaboration", "45%", "bad"), ("Innovation", "6% · 24% conv. rate", "good"),
            ("AI strategy", "3%", "")]),
     cell("4 ads", "1 per ad group"),
     cell("Homepage 56%", "Innovation platform 30% · Supply chain 5%", "bad")],
    [cell("Europe &amp; Middle East", f"{eur(33)} a day · 6 countries"),
     chips([("Startup collaboration", "38%", "bad"), ("Brand", "28%", "bad"), ("Innovation", "23%", ""), ("AI strategy", "12%", "")]),
     cell("4 ads", "1 per ad group"),
     cell("Homepage 65%", "Innovation platform 26%", "bad")],
    [cell("Coworking · Silicon Valley", f"{eur(5)} a day · since 2023"),
     chips([("Coworking", "mostly brand and address searches", "bad")]),
     cell("1 ad"),
     cell("Coworking offer", "Not part of the corporate goal", "off")],
], ["2.5in", "4.6in", "1.25in", "2.4in"])}
{verdict([f"<b>Corporate searches convert</b>: Innovation ad group (supply-chain page), 24% conversion rate, {eur(11.51, 2)} each.",
          f"<b>Corporate copy wins</b>: “Top Corporate Accelerator” ads converted 9–10% at half the generic ad's cost ({eur(29.84)}–{eur(35.87)} vs {eur(49.70)}–{eur(72.91)}).",
          f"<b>Europe &amp; Middle East</b>: {eur(41.36)} per conversion; Saudi Arabia is the cheapest market ({eur(32.26)})."],
         [f"<b>60% of spend lands on the homepage</b>, which has no form ({eur(2969.63 + 2841.09)}).",
          "<b>37% of spend buys our own name</b>, in campaigns capped by budget.",
          f"<b>Startup-side traffic</b>: “Startup collaboration” is 42% of spend; “Venture Capitalist” headline; coworking extras; “startup india certificate” ({eur(166.47)}).",
          "<b>Unstable, broken basics</b>: goal changed twice in two weeks, budgets cut 71–76% in three days; name, logo and 14 of 18 images disapproved."])}
""", note=f"Shares of spend this year ({PERIOD}). Google bills in EUR, shown in USD at {FX}.")

# 6 · Google proposal
slide("Google Search · proposal", "Google proposal: brand apart, corporate only, a form behind every ad", f"""
{goal("New goal: a corporate form sent, then qualified leads (already set up as a conversion in Google)", "good")}
{structure([("4", "campaigns"), ("8", "ad groups"), ("16", "ads"), ("Landing", "pages")], [
    [cell("Brand · all markets", "Own small, capped budget", "good"),
     chips([("“plug and play” searches", "exact and phrase", "good")]),
     cell("2 ads"),
     cell("Corporate page with a form", "", "good")],
    [cell("Corporate · US &amp; Canada", "Phrase and exact match + negatives", "good"),
     chips([("Corporate innovation", "", "good"), ("Startup scouting", "", "good"), ("Industry topics", "supply chain, health…", "good")]),
     cell("2 ads each", "corporate copy"),
     cell("Own page with a form", "", "good")],
    [cell("Corporate · Europe &amp; Middle East", "Same set-up, 6 countries", "good"),
     chips([("Corporate innovation", "", "good"), ("Startup scouting", "", "good"), ("Industry topics", "", "good")]),
     cell("2 ads each", "corporate copy"),
     cell("Own page with a form", "", "good")],
    [cell("Coworking · Silicon Valley", "Review: keep separate or pause", "off"),
     chips([("Coworking", "", "off")]),
     cell("2 ads"),
     cell("Coworking page", "", "off")],
], ["2.5in", "4.6in", "1.25in", "2.4in"])}
{changes([("Brand", "37%, inside non-brand", "own campaign, capped"), ("Startup collab.", "42% of spend", "corporate ad groups only"),
          ("Keywords", "all broad + AI Max", "phrase, exact + negatives"), ("Landing", "homepage 60%", "a form behind every ad"),
          ("Goal", "any lead form", "corporate form, then qualified"), ("Assets", "disapproved items", "fixed; startup extras removed"),
          ("Changes", "daily tweaks", "one owner, weekly review"), ("Total budget", f"{eur(68)} a day", "same, brand capped")])}
""", note="Negatives: other accelerators, grants, investors, certificates. Industry topics follow our landing pages (supply chain, health).")

# 7 · ChatGPT
slide("ChatGPT Ads", "ChatGPT Ads: Test 1 had nowhere to convert, Test 2 fixes that", f"""
<div class="tlabel">Test 1 · 23 Sep – 2 Oct · done</div>
{structure([("1", "campaign"), ("1", "ad group"), ("5", "ads"), ("1", "landing page")], [
    [cell("Test 1", f"US only · {eur(25)} a day"),
     chips([("7 topics", "corporate innovation, governments, accelerators, startup pilots", "good")]),
     cell("5 ads", "One got 74% of views; auto-rewrite was on", "bad"),
     cell("Homepage", "No form · no tracking links", "bad")],
], ["2.35in", "4.1in", "2.1in", "2.45in"])}
<div class="cols4">
 <div class="card kp"><b>{eur(229.56)}</b>spent</div><div class="card kp"><b>4,021</b>ad views</div>
 <div class="card kp"><b>43</b>clicks · 1.1% CTR</div><div class="card kp bad"><b>0</b>leads</div>
</div>
<div class="tlabel">Test 2 · 10 days · proposed</div>
{structure([("1", "campaign"), ("2", "ad groups"), ("6", "ads"), ("1", "landing page")], [
    [cell("Test 2: Startup Scouting", "US + Europe · same daily budget", "good"),
     chips([("US", "startup scouting topics", "good"), ("Europe", "startup scouting topics", "good")]),
     cell("3 ads per ad group", "Our copy: auto-rewrite off", "good"),
     cell("Startup Scouting page", "Short form · tracking links", "good")],
], ["2.35in", "4.1in", "2.1in", "2.45in"])}
""", note=f"Test 1 kept: the topics describe our buyers and the budget held. ChatGPT Ads bill in EUR, shown in USD at {FX}.")

# 8 · landing pages
slide("Landing pages", "Landing pages: Meta's work, Google and ChatGPT land on the homepage", f"""
{structure([("", "channel"), ("", "where the clicks land"), ("", "verdict")], [
    [cell("Meta", "Prospecting and retargeting", "good"),
     chips([("Report pages", "AI &amp; robotics, quantum, Spain grid, AI trend…", "good"), ("Innovation platform page", "retargeting", "")]),
     cell("Form next to the headline", "Asks company size and job level; within one phone screen", "good")],
    [cell("Google Search", "US &amp; Canada, Europe &amp; Middle East", "bad"),
     chips([("Homepage", "60% of spend", "bad"), ("Innovation platform page", "28%", "bad"), ("Supply chain page", "5% (US)", "good")]),
     cell("No form / one page for everyone", "Platform page: form 2 screens down on phone, no company-size question", "bad")],
    [cell("ChatGPT Ads", "Test 1", "bad"),
     chips([("Homepage", "100%", "bad")]),
     cell("No form, no tracking", "", "bad")],
], ["2.6in", "5.4in", "3.0in"])}
<div class="cols2">
 <div class="card vd"><div class="top bad"></div><div class="vh">Also wrong on the forms</div>
  <p>{bang()}<span>Report forms offer “student” and “looking for a job”, and those count as Meta leads.</span></p>
  <p>{bang()}<span>Case studies (Mitsubishi Electric, Aeroporti di Roma) sit behind a 10-field form.</span></p></div>
 <div class="card vd"><div class="top blue"></div><div class="vh">Proposal: 3 page types, one short form</div>
  <p>{num(1)}<span><b>Corporate innovation</b> page for Google brand and corporate ad groups.</span></p>
  <p>{num(2)}<span><b>Startup Scouting</b> page for Google and ChatGPT Test 2.</span></p>
  <p>{num(3)}<span><b>Report pages</b> for Meta: keep. Every paid form asks company size and role; no student or job-seeker option.</span></p></div>
</div>""", note="Shares of Google Search spend this year, US & Canada and Europe & Middle East campaigns together.")

# 9 · next steps and decisions
slide("Next steps", "Next steps and what we need from you", f"""
<div class="plan">
 <div class="card col"><div class="top yellow"></div><h3>Now, before 30 Oct</h3>
  <p>{num(1)}<span><b>Handover from the agency</b>: access, change log, audiences, creatives.</span></p>
  <p>{num(2)}<span><b>Pause</b> Health (US), Brand (California), the healthcare video and the 2025 report ad (0 leads).</span></p>
  <p>{num(3)}<span><b>Clean Google</b>: negatives, remove startup and coworking extras, fix name, logo, images.</span></p></div>
 <div class="card col"><div class="top blue"></div><h3>Next 30 days</h3>
  <p>{num(4)}<span><b>Meta</b>: move to 4 campaigns, 7 ad sets.</span></p>
  <p>{num(5)}<span><b>Google</b>: brand campaign, corporate ad groups, a form behind every ad.</span></p>
  <p>{num(6)}<span><b>Goals</b>: corporate forms on both; start the CRM link for qualified leads.</span></p></div>
 <div class="card col"><div class="top dark"></div><h3>Next 60 days</h3>
  <p>{num(7)}<span><b>Two pages</b>: corporate innovation and Startup Scouting, short form.</span></p>
  <p>{num(8)}<span><b>ChatGPT Test 2</b>: 10 days, US and Europe.</span></p>
  <p>{num(9)}<span><b>Test plan</b>: 2 Meta tests a month, read on day 7.</span></p></div>
 <div class="card col ask"><div class="top bad"></div><h3>We need from you</h3>
  <p>{num("A")}<span><b>Agree on success</b>: qualified corporate and government leads, even if lead volume drops and CPL rises at first.</span></p>
  <p>{num("B")}<span><b>Web team time</b> in November for the two pages and the form changes.</span></p>
  <p>{num("C")}<span><b>One owner</b> for ad-account changes from 1 Nov: Felipe, every change logged.</span></p></div>
</div>""")


# ------------------------------------------------------------------ page
CSS = B.BASE_CSS + f"""
@page {{ size: 13.333in 7.5in; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ font-size: 13pt; line-height: 1.3; }}
.slide {{ width: 13.333in; height: 7.5in; padding: .4in .55in .5in; position: relative; overflow: hidden; background: {B.BG};
  break-after: page; display: flex; flex-direction: column; gap: .15in; }}
.slide:last-child {{ break-after: auto; }}
.kicker {{ color: {B.GRAY}; font-size: 10pt; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; }}
h1 {{ color: {B.DARK_BLUE}; font-size: 25pt; font-weight: 400; margin: 2px 0 0; line-height: 1.12; }}
h1::after {{ content: ""; display: block; width: 46px; height: 4px; border-radius: 2px; background: {B.YELLOW}; margin-top: 7px; }}
h3 {{ color: {B.DARK_BLUE}; font-size: 16pt; margin: 0 0 .12in; }}
b {{ color: {B.DARK_BLUE}; }}
.foot {{ position: absolute; left: .55in; right: .55in; bottom: .2in; display: flex; justify-content: space-between; color: {B.GRAY}; font-size: 8.5pt; }}
.card {{ padding: .13in .17in; }}
.ic {{ width: 16px; height: 16px; flex: none; margin-top: 2px; }}
.n {{ display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px; border-radius: 50%; background: {B.DARK_BLUE};
  color: #fff; font-size: 10pt; font-weight: 700; flex: none; margin-top: 1px; }}
.cols2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: .15in; }}
.cols3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: .16in; }}
.cols4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: .14in; }}
.tight {{ gap: .1in .3in; }}
.top {{ width: 34px; height: 4px; border-radius: 2px; margin-bottom: 7px; background: {B.DARK_BLUE}; }}
.top.good {{ background: {B.GOOD}; }} .top.bad {{ background: {B.BAD}; }} .top.blue {{ background: {B.BLUE}; }}
.top.yellow {{ background: {B.YELLOW}; }} .top.dark {{ background: {B.DARK_BLUE}; }}
.col p {{ display: flex; gap: 9px; margin: 0 0 .15in; font-size: 14pt; }}
.col p:last-child {{ margin-bottom: 0; }}
/* goal bar */
.goal {{ display: flex; gap: 9px; align-items: flex-start; font-size: 12.5pt; padding: 7px 12px; border-radius: 8px; background: #fff;
  border-left: 5px solid {B.GRAY}; box-shadow: {B.SHADOW}; }}
.goal.bad {{ border-left-color: {B.BAD}; }} .goal.good {{ border-left-color: {B.GOOD}; }}
/* structure diagram */
.st {{ display: grid; row-gap: .09in; align-items: stretch; }}
.st .hd {{ display: flex; align-items: baseline; gap: 6px; color: {B.GRAY}; font-size: 10pt; font-weight: 700; letter-spacing: .06em;
  text-transform: uppercase; border-bottom: 2px solid {B.DARK_BLUE}; padding-bottom: 2px; }}
.st .hd b {{ font-size: 19pt; letter-spacing: 0; }}
.lk {{ display: flex; align-items: center; justify-content: center; }}
.arrow {{ width: 22px; height: 13px; }}
.cl {{ background: #fff; border-radius: 8px; box-shadow: {B.SHADOW}; border-left: 5px solid {B.TINT_2}; padding: 6px 10px; }}
.cl.good {{ border-left-color: {B.GOOD}; }} .cl.bad {{ border-left-color: {B.BAD}; }} .cl.off {{ border-left-color: {B.TINT}; opacity: .75; }}
.cl .ct {{ color: {B.DARK_BLUE}; font-weight: 700; font-size: 12.5pt; line-height: 1.2; }}
.cl .cs {{ font-size: 10.5pt; margin-top: 1px; }}
.cl .cm {{ font-size: 9.5pt; color: {B.GRAY}; margin-top: 2px; line-height: 1.25; }}
.cl.bad .cs {{ color: {B.BAD}; }}
.cps {{ display: flex; flex-direction: column; justify-content: center; }}
.cpw {{ display: flex; flex-wrap: wrap; gap: 5px; }}
.cp {{ background: #fff; border-radius: 7px; box-shadow: {B.SHADOW}; border-left: 4px solid {B.TINT_2}; padding: 4px 8px; font-size: 11pt; line-height: 1.2; }}
.cp b {{ display: block; font-size: 11.5pt; }}
.cp span {{ font-size: 9.5pt; color: {B.TEXT}; }}
.cp.good {{ border-left-color: {B.GOOD}; }} .cp.good span {{ color: {B.GOOD}; font-weight: 700; }}
.cp.bad {{ border-left-color: {B.BAD}; }} .cp.bad span {{ color: {B.BAD}; font-weight: 700; }}
.cp.off {{ opacity: .6; }} .cp.off b {{ color: {B.GRAY}; }}
.cpn {{ font-size: 9.5pt; color: {B.GRAY}; margin-top: 4px; }}
/* verdict and changes */
.vd p {{ display: flex; gap: 8px; margin: 0 0 5px; font-size: 11.5pt; }}
.vd p:last-child {{ margin-bottom: 0; }}
.vh {{ color: {B.DARK_BLUE}; font-weight: 700; font-size: 13.5pt; margin-bottom: 6px; }}
.chg {{ display: grid; grid-template-columns: 1.4in 1.75in 24px 1fr; align-items: center; padding: 3px 0; border-bottom: 1px solid {B.TINT}; font-size: 11pt; }}
.chg:last-child {{ border-bottom: none; }}
.chg .cl2 {{ color: {B.GRAY}; font-weight: 700; }}
.chg .bf {{ color: {B.BAD}; }}
.chg .af {{ color: {B.GOOD}; font-weight: 700; }}
.chg .ca {{ display: flex; justify-content: center; }}
/* chatgpt */
.tlabel {{ color: {B.GRAY}; font-size: 10pt; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; margin-bottom: -6px; }}
.kp {{ font-size: 11.5pt; color: {B.GRAY}; padding: .08in .17in; }}
.kp b {{ display: block; font-size: 22pt; }}
.kp.bad b {{ color: {B.BAD}; }}
/* plan */
.plan {{ display: grid; grid-template-columns: 1fr 1fr 1fr 1.15fr; gap: .15in; }}
.plan .col p {{ font-size: 12.5pt; margin-bottom: .13in; gap: 8px; }}
.plan h3 {{ font-size: 14.5pt; }}
.ask {{ border: 2px solid {B.BAD}; }}
/* cover */
.cover {{ background: {B.DARK_BLUE}; justify-content: center; padding: .8in .9in; }}
.cover .ck {{ color: {B.TINT_2}; font-size: 11pt; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }}
.cover .ctt {{ color: #fff; font-size: 46pt; line-height: 1.05; margin: .12in 0 .1in; }}
.cover .ctt::after {{ content: ""; display: block; width: 70px; height: 5px; border-radius: 3px; background: {B.YELLOW}; margin-top: .16in; }}
.cover .csub {{ color: {B.TINT}; font-size: 17pt; max-width: 10in; }}
.cover .scope {{ display: flex; gap: .45in; margin-top: .55in; }}
.cover .scope div {{ color: {B.TINT_2}; font-size: 11pt; }}
.cover .scope b {{ display: block; color: #fff; font-size: 22pt; }}
.cover .by {{ position: absolute; left: .9in; bottom: .55in; color: {B.TINT_2}; font-size: 11.5pt; }}
"""

COVER = ('<section class="slide cover"><div class="ck">Plug and Play · Paid media · October 2026</div>'
         '<div class="ctt">Paid media audit</div>'
         '<div class="csub">Meta, Google Search and ChatGPT Ads: what is going well, what is going wrong, and the structure we propose</div>'
         f'<div class="scope"><div><b>{usd(180940.06)}</b>Meta</div><div><b>{eur(80055.62)}</b>Google Search</div>'
         f'<div><b>{eur(229.56)}</b>ChatGPT Ads test</div><div><b>{PERIOD}</b>spend covered</div></div>'
         '<div class="by">Felipe Cárdenas · Performance Marketing &amp; CRM</div></section>')


def render():
    total = len(SLIDES) + 1
    out = [COVER]
    for i, (kicker, title, body, note) in enumerate(SLIDES, 2):
        foot = f'<div class="foot"><span>{note}</span><span>Paid media audit · {i} / {total}</span></div>'
        out.append(f'<section class="slide"><div><div class="kicker">{kicker}</div><h1>{title}</h1></div>{body}{foot}</section>')
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Paid media audit 2026</title>"
            f"<style>{CSS}</style></head><body>{''.join(out)}</body></html>")


FIT_JS = """<script>window.addEventListener('load', () => {
  const out = [];
  document.querySelectorAll('.slide').forEach((s, i) => {
    const foot = s.querySelector('.foot'), limit = foot ? foot.getBoundingClientRect().top : s.getBoundingClientRect().bottom;
    let low = 0;
    s.querySelectorAll('*').forEach(el => { if (!foot || !foot.contains(el)) { const r = el.getBoundingClientRect(); if (r.height) low = Math.max(low, r.bottom); } });
    out.push((i + 1) + ':' + Math.round(limit - low));
  });
  document.body.setAttribute('data-fit', out.join(' '));
});</script>"""


def check_fit(html_path):
    """Free space (px) between each slide's lowest element and its footer; negative = content clipped."""
    check = html_path.replace(".html", ".check.html")
    open(check, "w", encoding="utf-8").write(open(html_path, encoding="utf-8").read().replace("</body>", FIT_JS + "</body>"))
    dom = subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--window-size=1280,720",
                          "--virtual-time-budget=3000", "--dump-dom", "file://" + os.path.abspath(check)],
                         capture_output=True, text=True).stdout
    os.remove(check)
    fit = re.search(r'data-fit="([^"]*)"', dom)
    pairs = [p.split(":") for p in fit.group(1).split()] if fit else []
    tight = [f"slide {n} ({v}px)" for n, v in pairs if int(v) < 4]
    print("free space under each slide (px):", " ".join(f"{n}:{v}" for n, v in pairs))
    if tight:
        print("WARNING: content clipped or touching the footer on", ", ".join(tight))


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    html_path = os.path.join(out_dir, STEM + ".html")
    open(html_path, "w", encoding="utf-8").write(render())
    print("written", html_path, "·", len(SLIDES) + 1, "slides")
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
