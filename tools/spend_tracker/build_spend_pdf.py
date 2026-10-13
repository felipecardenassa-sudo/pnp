"""Short visual PDF: Paid Media Spend 2026 vs the $300k budget. Numbers are read from the recalculated tracker workbook.
Usage: python build_spend_pdf.py TRACKER_RECALCULATED.xlsx OUT.html
"""
import sys, html, datetime
import openpyxl

E = html.escape
BLUE, ORANGE, AQUA, NAVY, INK, INK2, MUTED, GRID, RED, GREEN, SLATE = (
    "#2a78d6", "#eb6834", "#1baf7a", "#1f3864", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1", "#c42f2f", "#0a7d0a", "#6b7a8f")
VIOLET = "#6250d6"

wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
calc, mon, dash, agency, loc = wb["Calc"], wb["Monthly"], wb["Dashboard"], wb["Agency reports"], wb["By location & type"]
C = lambda r: calc[f"C{r}"].value
budget, maxi, orig, spent = C(27), C(28), C(29), C(30)
left_b, left_m, even, ahead = C(31), C(32), C(35), C(36)
pace, fc, allow_b, allow_m = C(39), C(42), C(43), C(44)
fx = wb["Settings"]["B41"].value
upto = C(3)
months = [mon[f"A{r}"].value for r in range(5, 17)]
meta_m = [mon[f"C{r}"].value or 0 for r in range(5, 17)]
goog_m = [mon[f"D{r}"].value or 0 for r in range(5, 17)]
gpt_m = [mon[f"E{r}"].value or 0 for r in range(5, 17)]
plan_m = [mon[f"I{r}"].value or 0 for r in range(5, 17)]
tot_m = [a + b + c for a, b, c in zip(meta_m, goog_m, gpt_m)]
nmon = sum(1 for m in months if m <= upto)
q = [(sum(meta_m[i:i + 3]), sum(goog_m[i:i + 3]), sum(gpt_m[i:i + 3]), sum(plan_m[i:i + 3])) for i in (0, 3, 6, 9)]
meta_t, goog_t, gpt_t = calc["D20"].value, calc["D21"].value, calc["D22"].value
regions = [(loc[f"A{r}"].value, loc[f"N{r}"].value, loc[f"O{r}"].value) for r in range(6, 9)]

# platform weeks around the September cuts (W/C 31 Aug – 5 Oct), from the Agency tab's platform columns:
# N = Meta excl. FR_Alibaba (USD), M − N = FR_Alibaba (USD), P = Google (EUR, converted here)
aw, meta_n, meta_ok, gq = [], 0, 0, []
for r in range(6, 200):
    a = agency[f"A{r}"].value
    if not isinstance(a, datetime.datetime):
        continue
    M, N, P = agency[f"M{r}"].value or 0, agency[f"N{r}"].value or 0, agency[f"P{r}"].value or 0
    if a.date() >= datetime.date(2026, 8, 31):
        aw.append((a.date(), N, M - N, P * fx))
    if isinstance(agency[f"C{r}"].value, (int, float)) and N:
        meta_n += 1
        meta_ok += abs(agency[f"O{r}"].value) <= 5
    if isinstance(agency[f"Q{r}"].value, (int, float)):
        gq.append(agency[f"Q{r}"].value)
g_same = sum(1 for x in gq if abs(x - 1) < 0.01)
g_double = sum(1 for x in gq if abs(x - 2) < 0.02)
g_conv = sum(1 for x in gq if 1.1 < x < 1.2)
g_lower = sum(1 for x in gq if x < 0.99)
fr_weeks = [(m, f, g) for d, m, f, g in aw if datetime.date(2026, 9, 7) <= d <= datetime.date(2026, 9, 28)]
fr_4w, all_4w = sum(f for m, f, g in fr_weeks), sum(m + f + g for m, f, g in fr_weeks)
fr_total = sum(f for d, m, f, g in aw)
h1_platform = sum(mon[f"G{r}"].value or 0 for r in range(5, 11))
tot_rows = []
for r in range(40, 80):
    p = agency[f"A{r}"].value
    if p and isinstance(agency[f"E{r}"].value, (int, float)) and agency[f"H{r}"].value is not None and isinstance(p, str) and "20" in p:
        tot_rows.append((p, agency[f"E{r}"].value, agency[f"H{r}"].value, agency[f"I{r}"].value, agency[f"K{r}"].value))


def usd(x, k=False):
    if k:
        v = x / 1000
        return f"${v:,.0f}k" if abs(v - round(v)) < 0.05 else f"${v:,.1f}k"
    return f"${x:,.0f}"


def pct(x):
    return f"{x * 100:.0f}%"


# ---------------------------------------------------------------- charts (inline SVG)
def budget_bar(w=700, h=118):
    pl, pr = 10, 10
    iw = w - pl - pr
    top, bh = 46, 26
    X = lambda v: pl + iw * v / 350000
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Spend vs budget">']
    s.append(f'<rect x="{pl}" y="{top}" width="{iw}" height="{bh}" rx="4" fill="#f1f0ec"/>')
    s.append(f'<rect x="{pl}" y="{top}" width="{X(spent) - pl:.1f}" height="{bh}" rx="4" fill="{NAVY}"/>')
    s.append(f'<rect x="{X(spent) + 1.5:.1f}" y="{top}" width="{X(fc) - X(spent) - 1.5:.1f}" height="{bh}" fill="{NAVY}" opacity=".35"/>')
    for v, lab, col, dash, anchor, dy in [(even, f"Even pace by {upto:%-d %b}: {usd(even, True)}", INK2, "2,2", "middle", bh + 18),
                                          (budget, f"Budget {usd(budget, True)}", INK, "", "end", -22),
                                          (maxi, f"Maximum {usd(maxi, True)}", RED, "3,2", "end", -8)]:
        s.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{top - 4}" y2="{top + bh + 4}" stroke="{col}" stroke-width="2" stroke-dasharray="{dash}"/>')
        s.append(f'<text x="{X(v) + (4 if anchor == "start" else -4 if anchor == "end" else 0):.1f}" y="{top + dy}" text-anchor="{anchor}" class="lbl" fill="{col}">{E(lab)}</text>')
    s.append(f'<text x="{pl + 8}" y="{top + 17}" class="in">Spent to {upto:%-d %b}: {usd(spent)}</text>')
    s.append(f'<text x="{X(fc) + 4:.1f}" y="{top + bh + 18}" text-anchor="middle" class="lbl" fill="{NAVY}">Forecast ≈ {usd(fc, True)}</text>')
    for v in (0, 100000, 200000):
        s.append(f'<text x="{X(v):.1f}" y="{h - 4}" text-anchor="{"start" if v == 0 else "middle"}" class="ax">{usd(v, True) if v else "$0"}</text>')
    s.append(f'<text x="{X(orig):.1f}" y="{h - 4}" text-anchor="end" class="ax">{usd(orig, True)} (original budget)</text>')
    s.append("</svg>")
    return "".join(s)


def monthly_chart(w=700, h=230):
    pl, pr, pt, pb = 46, 12, 14, 30
    iw, ih = w - pl - pr, h - pt - pb
    ymax = 50000
    n = 12
    bw = iw / n * 0.62
    X = lambda i: pl + iw * (i + 0.5) / n
    Y = lambda v: pt + ih * (1 - v / ymax)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Monthly spend by channel">']
    for t in range(0, ymax + 1, 10000):
        s.append(f'<line x1="{pl}" x2="{pl + iw}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{GRID}" stroke-width="1"/>'
                 f'<text x="{pl - 6}" y="{Y(t) + 3.5:.1f}" text-anchor="end" class="ax">{usd(t, True) if t else "$0"}</text>')
    for i in range(n):
        base = 0
        for val, col in ((meta_m[i], BLUE), (goog_m[i], ORANGE), (gpt_m[i], AQUA)):
            if val > 0:
                y0, y1 = Y(base), Y(base + val)
                s.append(f'<rect x="{X(i) - bw / 2:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(0.8, y0 - y1 - 1.5):.1f}" fill="{col}" rx="1.5"/>')
                base += val
        s.append(f'<text x="{X(i):.1f}" y="{h - 12}" text-anchor="middle" class="ax">{months[i]:%b}</text>')
        if i < nmon and (tot_m[i] == max(tot_m[:nmon]) or i == nmon - 1):
            part = "*" if i == nmon - 1 and upto.day < 28 else ""
            s.append(f'<text x="{X(i):.1f}" y="{Y(tot_m[i]) - 5:.1f}" text-anchor="middle" class="lbl">{usd(tot_m[i], True)}{part}</text>')
    pts = " ".join(f"{X(i):.1f},{Y(plan_m[i]):.1f}" for i in range(n))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{INK2}" stroke-width="1.8" stroke-dasharray="5,4"/>')
    s.append(f'<text x="{X(n - 1) + 2:.1f}" y="{Y(plan_m[-1]) - 6:.1f}" text-anchor="end" class="lbl" fill="{INK2}">Even pace ≈ {usd(plan_m[-1], True)}/month</text>')
    s.append("</svg>")
    return "".join(s)


def cumulative_chart(w=700, h=270):
    pl, pr, pt, pb = 46, 118, 14, 28
    iw, ih = w - pl - pr, h - pt - pb
    ymax = 350000
    X = lambda d: pl + iw * (d - datetime.date(2026, 1, 1)).days / 364
    Y = lambda v: pt + ih * (1 - v / ymax)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Cumulative spend vs budget">']
    for t in range(0, ymax + 1, 50000):
        s.append(f'<line x1="{pl}" x2="{pl + iw}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{GRID}"/>'
                 f'<text x="{pl - 6}" y="{Y(t) + 3.5:.1f}" text-anchor="end" class="ax">{usd(t, True) if t else "$0"}</text>')
    for i, m in enumerate(months):
        s.append(f'<text x="{X(m.date()):.1f}" y="{h - 10}" text-anchor="start" class="ax">{m:%b}</text>')
    s.append(f'<line x1="{X(datetime.date(2026, 1, 1)):.1f}" y1="{Y(0):.1f}" x2="{X(datetime.date(2026, 12, 31)):.1f}" y2="{Y(budget):.1f}" stroke="{INK2}" stroke-width="1.6" stroke-dasharray="5,4"/>')
    s.append(f'<line x1="{pl}" x2="{pl + iw}" y1="{Y(maxi):.1f}" y2="{Y(maxi):.1f}" stroke="{RED}" stroke-width="1.4" stroke-dasharray="3,3"/>')
    pts, cum = [(X(datetime.date(2026, 1, 1)), Y(0))], 0
    for i in range(nmon):
        cum += tot_m[i]
        end = (months[i].replace(month=months[i].month % 12 + 1, day=1) - datetime.timedelta(days=1)) if months[i].month < 12 else datetime.date(2026, 12, 31)
        end = end.date() if hasattr(end, "date") else end
        pts.append((X(min(end, upto.date())), Y(cum)))
    s.append(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{NAVY}" stroke-width="2.6" stroke-linejoin="round"/>')
    for a, b in pts[1:]:
        s.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3" fill="{NAVY}" stroke="#fff" stroke-width="1.5"/>')
    x0, y0 = pts[-1]
    x1, y1 = X(datetime.date(2026, 12, 31)), Y(fc)
    s.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{NAVY}" stroke-width="2.4" stroke-dasharray="2,3"/>')
    s.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="3.5" fill="#fff" stroke="{NAVY}" stroke-width="2"/>')
    labels = sorted([(Y(maxi), f"Maximum {usd(maxi, True)}", RED), (y1, f"Forecast ≈ {usd(fc, True)}", NAVY),
                     (Y(budget), f"Budget {usd(budget, True)}", INK2)])
    last = -99
    for yy, lab, col in labels:
        yb = max(yy + 4, last + 13)
        s.append(f'<text x="{pl + iw + 8}" y="{yb:.1f}" class="lbl" fill="{col}">{E(lab)}</text>')
        last = yb
    s.append(f'<text x="{x0 + 4:.1f}" y="{y0 + 17:.1f}" class="lbl" fill="{NAVY}">{usd(spent, True)}</text>')
    s.append(f'<text x="{X(datetime.date(2026, 7, 10)):.1f}" y="{Y(150000):.1f}" class="ax" fill="{INK2}">Even pace to the budget</text>')
    s.append("</svg>")
    return "".join(s)


def weekly_chart(w=700, h=200):
    pl, pr, pt, pb = 46, 12, 22, 30
    iw, ih = w - pl - pr, h - pt - pb
    ymax = 6000
    n = len(aw)
    bw = iw / n * 0.55
    X = lambda i: pl + iw * (i + 0.5) / n
    Y = lambda v: pt + ih * (1 - v / ymax)
    s = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Weekly spend around the September cuts">']
    for t in range(0, ymax + 1, 1000):
        s.append(f'<line x1="{pl}" x2="{pl + iw}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" stroke="{GRID}"/>'
                 f'<text x="{pl - 6}" y="{Y(t) + 3.5:.1f}" text-anchor="end" class="ax">{usd(t, True) if t else "$0"}</text>')
    cut_i = next(i for i, (d, *_) in enumerate(aw) if d >= datetime.date(2026, 9, 21))
    xc = (X(cut_i - 1) + X(cut_i)) / 2
    s.append(f'<line x1="{xc:.1f}" x2="{xc:.1f}" y1="{pt - 6}" y2="{pt + ih}" stroke="{RED}" stroke-width="1.4" stroke-dasharray="3,3"/>'
             f'<text x="{xc + 5:.1f}" y="{pt + 2}" class="lbl" fill="{RED}">Budgets cut 18–21 Sep</text>')
    for i, (d, m, f, g) in enumerate(aw):
        base = 0
        for val, col in ((m, BLUE), (f, VIOLET), (g, ORANGE)):
            if val <= 0:
                continue
            y0, y1 = Y(base), Y(base + val)
            s.append(f'<rect x="{X(i) - bw / 2:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(0.8, y0 - y1 - 1.5):.1f}" fill="{col}" rx="1.5"/>')
            base += val
        s.append(f'<text x="{X(i):.1f}" y="{Y(base) - 5:.1f}" text-anchor="middle" class="lbl">{usd(base, True)}</text>')
        s.append(f'<text x="{X(i):.1f}" y="{h - 12}" text-anchor="middle" class="ax">W/C {d:%-d %b}</text>')
    s.append("</svg>")
    return "".join(s)


def region_bars():
    tot = sum(v for _, v, _ in regions)
    rows = []
    for name, v, sh in regions:
        rows.append(f'<tr><td>{E(name)}</td><td><div class="mb"><div class="mbf" style="width:{v / regions[0][1] * 100:.0f}%"></div></div></td>'
                    f'<td class="num">{usd(v)}</td><td class="num">{pct(sh)}</td></tr>')
    return "".join(rows)


CSS = f"""
@page {{ size: A4; margin: 14mm 15mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: Inter, 'Liberation Sans', Arial, sans-serif; color: {INK}; font-size: 10pt; line-height: 1.42; margin: 0; }}
.page {{ page-break-after: always; }} .page:last-child {{ page-break-after: auto; }}
.kicker {{ color: {BLUE}; font-weight: 700; font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; }}
h1 {{ font-size: 21pt; margin: 3px 0 2px; letter-spacing: -.01em; }}
h2 {{ font-size: 12.5pt; margin: 14px 0 5px; }}
.meta {{ color: {MUTED}; font-size: 8.6pt; }}
.tiles {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 12px 0 2px; }}
.tile {{ border: 1px solid {GRID}; border-radius: 9px; padding: 8px 11px; }}
.tile .l {{ color: {INK2}; font-size: 8pt; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }}
.tile .v {{ font-size: 18pt; font-weight: 700; line-height: 1.15; margin-top: 2px; }}
.tile .d {{ font-size: 8.2pt; color: {INK2}; margin-top: 2px; }}
.red {{ color: {RED}; }} .green {{ color: {GREEN}; }}
ul.list {{ margin: 0; padding: 0; list-style: none; }}
ul.list li {{ padding: 4px 10px 4px 12px; border-left: 3px solid {GRID}; margin: 4px 0; background: #fafaf8; border-radius: 0 6px 6px 0; font-size: 9.4pt; }}
ul.flag li {{ border-left-color: {RED}; }} ul.work li {{ border-left-color: {GREEN}; }} ul.imp li {{ border-left-color: #e0a100; }}
ol.steps {{ margin: 0; padding: 0; list-style: none; counter-reset: s; }}
ol.steps li {{ counter-increment: s; position: relative; padding: 6px 10px 6px 38px; margin: 5px 0; background: #f3f7fd; border-radius: 6px; font-size: 9.4pt; }}
ol.steps li::before {{ content: counter(s); position: absolute; left: 10px; top: 6px; width: 20px; height: 20px; border-radius: 50%;
  background: {BLUE}; color: #fff; font-weight: 700; font-size: 8.5pt; text-align: center; line-height: 20px; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 3px; }}
th {{ text-align: left; color: {INK2}; font-weight: 600; font-size: 8.3pt; border-bottom: 1.5px solid {INK}; padding: 4px 6px; }}
td {{ border-bottom: 1px solid {GRID}; padding: 3px 6px; font-size: 8.9pt; vertical-align: top; }}
th.num, td.num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
tr.tot td {{ font-weight: 700; border-top: 1.5px solid {INK}; }}
td:first-child {{ white-space: nowrap; }}
.mb {{ height: 11px; background: #f1f0ec; border-radius: 4px; width: 210px; }}
.mbf {{ height: 11px; background: {SLATE}; border-radius: 4px; }}
.legend {{ font-size: 8.3pt; color: {INK2}; margin: 2px 0 0; }}
.sw {{ display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin: 0 4px -1px 10px; }}
.note {{ color: {MUTED}; font-size: 7.9pt; margin-top: 4px; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
svg text {{ font-family: Inter, sans-serif; }}
svg .ax {{ fill: {MUTED}; font-size: 10px; }}
svg .lbl {{ fill: {INK2}; font-size: 10.5px; font-weight: 600; }}
svg .in {{ fill: #fff; font-size: 11px; font-weight: 700; }}
"""

over_b = fc - budget
under_m = maxi - fc
LEG = (f'<div class="legend"><span class="sw" style="background:{BLUE};margin-left:0"></span>Meta'
       f'<span class="sw" style="background:{ORANGE}"></span>Google Ads<span class="sw" style="background:{AQUA}"></span>ChatGPT Ads'
       f'<span class="sw" style="background:none;border-top:2px dashed {INK2};height:0;border-radius:0;margin-bottom:3px"></span>Even pace for {usd(budget, True)}'
       f'<span style="margin-left:12px">* {upto:%B} = 1–{upto:%-d %b} only</span></div>')

p1 = f"""
<div class="page">
<div class="kicker">Paid media · budget check</div>
<h1>Paid Media Spend 2026 vs. the {usd(budget, True)} budget</h1>
<div class="meta">Platform data to {upto:%-d %b %Y} (Meta and Google Ads exports, day by day) · USD (Google Ads converted at 1 EUR = {fx:.4f} USD) · prepared 13 Oct 2026 by Felipe Cárdenas</div>
<div class="tiles">
 <div class="tile"><div class="l">Budget 2026</div><div class="v">{usd(budget)}</div><div class="d">Maximum {usd(maxi)} · originally {usd(orig)}</div></div>
 <div class="tile"><div class="l">Spent to {upto:%-d %b}</div><div class="v">{usd(spent)}</div><div class="d">{pct(spent / budget)} of the budget · {pct(C(9))} of the year gone</div></div>
 <div class="tile"><div class="l">Left in the budget</div><div class="v">{usd(left_b)}</div><div class="d">≈ {usd(allow_b)} a week to 31 Dec</div></div>
 <div class="tile"><div class="l">Left up to the maximum</div><div class="v">{usd(left_m)}</div><div class="d">≈ {usd(allow_m)} a week to 31 Dec</div></div>
 <div class="tile"><div class="l">Current pace</div><div class="v">{usd(pace)}<span style="font-size:10pt;font-weight:600"> /week</span></div><div class="d">Last 3 full weeks ({C(15):%-d %b} – {C(13):%-d %b}), campaigns still running</div></div>
 <div class="tile"><div class="l">Forecast year-end</div><div class="v">{usd(fc)}</div><div class="d"><span class="red">≈ {usd(over_b)} over the budget</span> · ≈ {usd(under_m)} under the maximum</div></div>
</div>
{budget_bar()}
<h2>What's flagged</h2>
<ul class="list flag">
 <li><b>Spending ran ahead of an even pace.</b> {usd(spent)} was spent by {upto:%-d %b}, {usd(ahead)} more than spreading {usd(budget, True)} evenly over the year ({usd(even)}). Q1 was the biggest quarter ({usd(sum(q[0][:3]))}).</li>
 <li><b>At the current pace, 2026 ends at ≈ {usd(fc)}</b>: ≈ {usd(over_b)} over the budget and ≈ {usd(under_m)} under the maximum. Landing exactly on {usd(budget, True)} means ≈ {usd(allow_b)} a week ({pct(1 - allow_b / pace)} less than now).</li>
 <li><b>The agency's Google figures don't match the platform.</b> Checked week by week, they matched in only {g_same} of {len(gq)} weeks: {g_conv} look converted to dollars, {g_double} are exactly doubled and {g_lower} are lower. Their H1 total is $182,516; the platforms show {usd(h1_platform)}.</li>
 <li><b>Lead numbers can't be compared over time.</b> The agency changed the lead definition several times (leads, welcome conversions, proxy events), tracking was down ~15 Jul–11 Aug, and MQL/SQL reporting stopped after January.</li>
 <li><b>FR_Alibaba, run by PnP's internal team, spent {usd(fr_total)} on Meta from 10 Sep to 5 Oct</b>, {pct(fr_4w / all_4w)} of all spend in W/C 7–28 Sep. It counts in spend so far but is left out of the current pace because it has ended. Open: do FR_Alibaba and ChatGPT Ads ({usd(gpt_t)}) count toward the {usd(budget, True)}?</li>
</ul>
</div>
"""

qs = []
for i, (m, g, c, p) in enumerate(q):
    qstart = datetime.date(2026, 3 * i + 1, 1)
    if qstart > upto.date():
        continue
    qend = (datetime.date(2026, 3 * i + 4, 1) - datetime.timedelta(days=1)) if i < 3 else datetime.date(2026, 12, 31)
    lab = f"Q{i + 1}"
    if upto.date() < qend:
        p = budget * ((upto.date() - qstart).days + 1) / 365
        lab = f"Q{i + 1} (to {upto:%-d %b})"
    qs.append((lab, m, g, c, p))
qrows = "".join(
    f'<tr><td>{lab}</td><td class="num">{usd(m)}</td><td class="num">{usd(g)}</td><td class="num">{usd(c) if c else "–"}</td>'
    f'<td class="num"><b>{usd(m + g + c)}</b></td><td class="num">{usd(p)}</td><td class="num {"red" if m + g + c - p > 0 else ""}">'
    f'{("+" if m + g + c - p > 0 else "−") + usd(abs(m + g + c - p))}</td></tr>'
    for lab, m, g, c, p in qs)
qrows += (f'<tr class="tot"><td>Total</td><td class="num">{usd(meta_t)}</td><td class="num">{usd(goog_t)}</td><td class="num">{usd(gpt_t)}</td>'
          f'<td class="num">{usd(spent)}</td><td class="num">{usd(even)}</td><td class="num red">+{usd(ahead)}</td></tr>')

p2 = f"""
<div class="page">
<h2 style="margin-top:0">Spend by month and channel</h2>
{monthly_chart()}
{LEG}
<h2>Spend so far vs. budget and maximum</h2>
{cumulative_chart()}
<div class="legend"><span class="sw" style="background:{NAVY};margin-left:0"></span>Spent (platforms)
<span class="sw" style="background:none;border-top:2px dotted {NAVY};height:0;border-radius:0;margin-bottom:3px"></span>Forecast at the current pace
<span class="sw" style="background:none;border-top:2px dashed {INK2};height:0;border-radius:0;margin-bottom:3px"></span>Even pace</div>
<div class="two">
 <div>
  <h2>Quarter by quarter</h2>
  <table><tr><th>Quarter</th><th class="num">Meta</th><th class="num">Google</th><th class="num">ChatGPT</th><th class="num">Total</th><th class="num">Even pace</th><th class="num">Difference</th></tr>{qrows}</table>
 </div>
 <div>
  <h2>Where it went, by region</h2>
  <table><tr><th>Region</th><th></th><th class="num">Spent</th><th class="num">Share</th></tr>{region_bars()}</table>
  <div class="note">Region comes from the location code in each campaign name. Meta is {pct(meta_t / spent)} of all spend, Google Ads {pct(goog_t / spent)}.</div>
 </div>
</div>
</div>
"""

trows = "".join(
    f'<tr><td>{E(p)}</td><td class="num">{usd(a)}</td><td class="num">{usd(pl)}</td><td class="num {"red" if abs(dfx) > 100 else ""}">'
    f'{("+" if dfx > 0 else "−") + usd(abs(dfx)) if abs(dfx) >= 0.5 else "0"}</td><td>{E(nt)}</td></tr>'
    for p, a, pl, dfx, nt in tot_rows)

before = sum(m + g for d, m, f, g in aw if d < datetime.date(2026, 9, 21)) / max(1, sum(1 for d, *_ in aw if d < datetime.date(2026, 9, 21)))
p3 = f"""
<div class="page">
<h2 style="margin-top:0">Weekly spend around the September cuts (platform data)</h2>
{weekly_chart()}
<div class="legend"><span class="sw" style="background:{BLUE};margin-left:0"></span>Meta (without FR_Alibaba)<span class="sw" style="background:{VIOLET}"></span>FR_Alibaba (Meta, PnP's internal team)<span class="sw" style="background:{ORANGE}"></span>Google Ads (€ converted at {fx:.4f})</div>
<h2>The agency's totals vs. the platform exports</h2>
<table class="tight"><tr><th>Period</th><th class="num">Agency said</th><th class="num">Platforms</th><th class="num">Difference</th><th>Note</th></tr>{trows}</table>
<div class="two" style="margin-top:6px">
 <div>
  <h2>What's working</h2>
  <ul class="list work">
   <li>The 18–21 Sep budget cuts took weekly spend (without FR_Alibaba) from ≈ {usd(before)} to ≈ {usd(pace)}.</li>
   <li>The agency's weekly Meta figures match Meta's own numbers within $5 in {meta_ok} of {meta_n} weeks, so the Meta history is solid.</li>
   <li>The new tracker uses one source (the platform exports), one currency (USD) and one budget, and will be updated every Monday.</li>
  </ul>
  <h2>What can be improved</h2>
  <ul class="list imp">
   <li>Agree one exchange rate with Finance (this report uses the 13 Oct live rate for all months).</li>
   <li>Fix one lead definition per channel and report HubSpot MQLs/SQLs by channel every week.</li>
   <li>Write down the monthly cap per channel and territory (the agency's location plan sits in an external sheet we haven't seen).</li>
  </ul>
 </div>
 <div>
  <h2>Next steps</h2>
  <ol class="steps">
   <li>Decide the Q4 pace with Tereza and Raúl: hold ≈ {usd(pace)}/week (≈ {usd(fc, True)}), trim to ≈ {usd(allow_b)}/week ({usd(budget, True)}), or go up to ≈ {usd(allow_m)}/week ({usd(maxi, True)}) where results justify it.</li>
   <li>Confirm whether FR_Alibaba and ChatGPT Ads count toward the budget.</li>
   <li>Ask Thiago before 30 Oct: Google's currency before 21 Sep, the doubled weeks, which H1 total is right, and the approved monthly caps.</li>
   <li>Update the tracker every Monday from the platform exports (about 15 minutes) and send Raúl the dashboard.</li>
  </ol>
 </div>
</div>
<div class="note" style="margin-top:10px">Sources: Meta Ads Manager ('Plug and Play Tech Center – Dollars' ad account, USD) and Google Ads (EUR) exports by campaign and day, 1 Jan – 12 Oct 2026 (they match the earlier monthly exports for Jan–Sep); ChatGPT Ads 'Test 1' (23 Sep – 2 Oct, €229.56).
Agency figures: weekly reports in Notion (W/C 29 Dec 2025 – 5 Oct 2026), copied as written and compared with the platforms week by week.
Budget: Tereza, 13 Oct 2026. Forecast = spent to {upto:%-d %b} + current weekly pace × {C(16):.1f} weeks left; the pace leaves out campaigns that have ended (FR_Alibaba, ChatGPT 'Test 1'). Full detail: PNP_Paid_Media_Spend_Tracker_2026.xlsx.</div>
</div>
"""

open(sys.argv[2], "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset='utf-8'><title>Paid Media Spend 2026</title><style>{CSS}</style></head><body>{p1}{p2}{p3}</body></html>")
print("written", sys.argv[2])
