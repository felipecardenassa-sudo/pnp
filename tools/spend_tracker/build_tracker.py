"""Build the PnP Paid Media Spend Tracker (Google Sheets friendly .xlsx).

Usage: python build_tracker.py OUT.xlsx DATA_UP_TO(YYYY-MM-DD) [data_source]
Data rows: dict(date, channel, campaign, spend, impr, clicks, conv); spend in the billing currency.
"""
import sys, datetime, collections
from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as L
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.label import DataLabelList
from xlstyle import *
import campaign_map as CM

CHANNELS = [  # name, data tab, settings row, billing currency, counts toward budget, budget
    ("Meta", "Meta data", 17, "USD", "Yes", 180000),
    ("Google Ads", "Google data", 18, "EUR", "Yes", 90000),
    ("ChatGPT Ads", "ChatGPT data", 19, "EUR", "No", None),
    ("LinkedIn Ads", "LinkedIn data", 20, "EUR", "No", None),
]
DMAX = 20000          # last row the formulas look at in the data tabs
HELPER_ROWS = 8000    # rows pre-filled with the "in campaign list?" check
CAMP_FIRST, CAMP_LAST = 7, 300
REGIONS = ["EMEA", "Americas", "Global", "Not specified"]
SLATE = "6B7A8F"
DRAFT = False
DRAFT_DASH = ("DRAFT – layout preview built from the Jan–Sep monthly exports. October, the weekly view and the agency figures "
              "are added once the daily exports and the Notion reports are in.")
DRAFT_WEEKLY = "DRAFT: until the daily exports are pasted, each month's spend shows in the week that contains the 1st."
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Settings cells
S_UPTO, S_CUR, S_FX = "Settings!$C$5", "Settings!$C$6", "Settings!$C$7"
S_STATUS, S_PSTART, S_PEND, S_YEAR, S_W1 = "Settings!$C$10", "Settings!$C$11", "Settings!$C$12", "Settings!$C$13", "Settings!$C$14"
S_BTOTAL, S_STRETCH = "Settings!$F$21", "Settings!$F$23"


def conv(row):
    return f"Settings!$G${row}"


def counts(row):
    return f'(Settings!$E${row}="Yes")'


def sumifs(tab, col, lo, hi, extra=""):
    rng = lambda c: f"'{tab}'!${c}$3:${c}${DMAX}"
    return f'SUMIFS({rng(col)},{rng("A")},">="&{lo},{rng("A")},"<="&{hi}{extra})'


def CUR(x):
    return f'IF({S_CUR}="USD","$","€")&TEXT({x},"#,##0")'


# ---------------------------------------------------------------------------------------------
def build(out, upto, rows, agency=None, weekly_notes=None, source_note=""):
    wb = Workbook()
    names = ["Dashboard", "Weekly", "Monthly", "By location & type", "Campaigns", "Agency reports",
             "Settings", "How to update", "Meta data", "Google data", "ChatGPT data", "LinkedIn data", "Calc"]
    ws = {n: (wb.active if i == 0 else wb.create_sheet(n)) for i, n in enumerate(names)}
    ws["Dashboard"].title = "Dashboard"
    tabcol = {"Dashboard": NAVY, "Weekly": "2A78D6", "Monthly": "2A78D6", "By location & type": "2A78D6",
              "Campaigns": "BF9000", "Agency reports": "BF9000", "Settings": "BF9000", "How to update": "7F7F7F",
              "Meta data": "BF9000", "Google data": "BF9000", "ChatGPT data": "BF9000", "LinkedIn data": "BF9000", "Calc": "7F7F7F"}
    for n, w in ws.items():
        w.sheet_properties.tabColor = tabcol[n]

    settings(ws["Settings"], upto)
    data_tabs(ws, rows)
    campaigns(ws["Campaigns"], rows)
    calc(ws["Calc"])
    monthly(ws["Monthly"])
    weekly(ws["Weekly"], weekly_notes or {})
    markets, types = by_location(ws["By location & type"], rows)
    agency_tab(ws["Agency reports"], agency)
    how_to(ws["How to update"], source_note)
    dashboard(ws["Dashboard"], markets)
    wb.save(out)


# ---------------------------------------------------------------------------------------------
def settings(s, upto):
    title(s, "A1", "Settings", "Yellow cells are the only ones to change. The rest of the workbook updates from them.", "A2")
    section(s, "A4", "REPORT", "ABCDEFG")
    rows = [
        (5, "Data up to (last day included)", upto, DATE_F, "Set this to the last day you pasted data for (usually last Sunday)."),
        (6, "Show amounts in", "EUR", None, "EUR or USD. Every tab switches currency."),
        (7, "Exchange rate: 1 EUR = ? USD", 1.16, "0.00", "≈ 2026 average so far. Replace with Finance's rate if they give you one."),
    ]
    for r, lab, val, fmt, nt in rows:
        cell(s, f"A{r}", lab, bold=True)
        s.merge_cells(f"A{r}:B{r}")
        cell(s, f"C{r}", val, fmt, fill=INPUT, color="0000FF", align="center")
        note(s, f"D{r}", nt)
    section(s, "A9", "BUDGET", "ABCDEFG")
    rows = [
        (10, "Budget status", "Waiting for Tereza's confirmation (asked 13 Oct 2026): full-year budget? EUR or USD?", None),
        (11, "Budget period starts", datetime.date(2026, 1, 1), DATE_F),
        (12, "Budget period ends", datetime.date(2026, 12, 31), DATE_F),
    ]
    for r, lab, val, fmt in rows:
        cell(s, f"A{r}", lab, bold=True)
        s.merge_cells(f"A{r}:B{r}")
        cell(s, f"C{r}", val, fmt, fill=INPUT, color="0000FF", align="center" if fmt else "left", wrap=not fmt)
    s.merge_cells("C10:G10")
    s.row_dimensions[10].height = 30
    cell(s, "A13", "Year (calculated)", bold=True); s.merge_cells("A13:B13")
    cell(s, "C13", "=YEAR(C11)", "0", align="center")
    cell(s, "A14", "Week 1 starts on (calculated)", bold=True); s.merge_cells("A14:B14")
    cell(s, "C14", "=DATE(C13,1,1)-WEEKDAY(DATE(C13,1,1),2)+1", DATE_F, align="center")
    note(s, "D14", "Weeks run Monday to Sunday.")
    header(s, 16, 1, ["Channel", "Billing currency", "Annual budget", "Budget currency",
                      "Counts toward the total budget?", "Budget in report currency", "Spend converter (×)"])
    for name, tab, r, bill, cnt, bud in CHANNELS:
        cell(s, f"A{r}", name, bold=True)
        cell(s, f"B{r}", bill, fill=INPUT, color="0000FF", align="center")
        cell(s, f"C{r}", bud, AMT, fill=INPUT, color="0000FF")
        cell(s, f"D{r}", "EUR", fill=INPUT, color="0000FF", align="center")
        cell(s, f"E{r}", cnt, fill=INPUT, color="0000FF", align="center")
        cell(s, f"F{r}", f'=IF(C{r}="","",C{r}*IF(D{r}=$C$6,1,IF(D{r}="USD",1/$C$7,$C$7)))', AMT)
        cell(s, f"G{r}", f'=IF(B{r}=$C$6,1,IF(B{r}="USD",1/$C$7,$C$7))', "0.0000", align="center")
    cell(s, "A21", "Total budget (channels marked Yes)", bold=True, fill=TOTAL)
    s.merge_cells("A21:E21")
    cell(s, "F21", '=SUMIFS(F17:F20,E17:E20,"Yes")', AMT, bold=True, fill=TOTAL)
    cell(s, "A23", "Stretch budget being discussed (total, not confirmed)", bold=True, wrap=True)
    s.merge_cells("A23:B23")
    s.row_dimensions[23].height = 28
    cell(s, "C23", 350000, AMT, fill=INPUT, color="0000FF")
    cell(s, "D23", "EUR", fill=INPUT, color="0000FF", align="center")
    cell(s, "F23", '=IF(C23="","",C23*IF(D23=$C$6,1,IF(D23="USD",1/$C$7,$C$7)))', AMT)
    note(s, "A25", "Budgets as given by Raúl: Google Ads 90k and Meta 180k for 2026, assumed EUR until Tereza confirms. "
                   "Meta bills in USD; Google Ads and ChatGPT Ads bill in EUR.")
    note(s, "A26", "ChatGPT Ads is paid outside the Meta + Google budget. LinkedIn Ads: no spend since October 2025 (billing currency to check).")
    dv = DataValidation(type="list", formula1='"EUR,USD"', allow_blank=False)
    s.add_data_validation(dv)
    for ref in ["C6", "B17", "B18", "B19", "B20", "D17", "D18", "D19", "D20", "D23"]:
        dv.add(ref)
    dv2 = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False)
    s.add_data_validation(dv2)
    dv2.add("E17:E20")
    widths(s, {"A": 26, "B": 14, "C": 16, "D": 16, "E": 18, "F": 18, "G": 16})


# ---------------------------------------------------------------------------------------------
def data_tabs(ws, rows):
    spec = {
        "Meta": ("Meta Ads – daily spend by campaign, as billed (USD)",
                 "Export columns, in this order: Day · Campaign name · Amount spent (USD) · Impressions · Link clicks · Website registrations completed"),
        "Google Ads": ("Google Ads – daily spend by campaign, as billed (EUR)",
                       "Export columns, in this order: Day · Campaign · Cost · Impr. · Clicks · Conversions"),
        "ChatGPT Ads": ("ChatGPT Ads – daily spend by campaign, as billed (EUR)",
                        "Export columns, in this order: date · campaign_name · spend · impressions · clicks · conversions"),
        "LinkedIn Ads": ("LinkedIn Ads – daily spend by campaign, as billed",
                         "Export columns, in this order: Start date · Campaign name · Total spent · Impressions · Clicks · Conversions"),
    }
    by_ch = collections.defaultdict(list)
    for r in rows:
        by_ch[r["channel"]].append(r)
    for name, tab, srow, bill, *_ in CHANNELS:
        w = ws[tab]
        t, how = spec[name]
        cell(w, "A1", t + " — paste each week's export under the last row (columns A–F). Column G checks the campaign is listed.",
             bold=True, color=NAVY, border=False)
        w.merge_cells("A1:G1")
        header(w, 2, 1, ["Date", "Campaign", f"Spend ({bill})", "Impressions", "Clicks", "Conversions", "In campaign list?"],
               fill=INPUT, color=INK)
        data = sorted(by_ch.get(name, []), key=lambda r: (r["date"], r["campaign"]))
        for i, r in enumerate(data):
            n = 3 + i
            w.cell(n, 1, r["date"]).number_format = "yyyy-mm-dd"
            w.cell(n, 2, r["campaign"])
            w.cell(n, 3, round(r["spend"], 2)).number_format = "#,##0.00"
            w.cell(n, 4, int(r["impr"])).number_format = "#,##0"
            w.cell(n, 5, int(r["clicks"])).number_format = "#,##0"
            w.cell(n, 6, round(r["conv"], 2)).number_format = "#,##0.##"
        last = HELPER_ROWS if name in ("Meta", "Google Ads") else 2000
        for n in range(3, last + 1):
            w.cell(n, 7, f'=IF(B{n}="","",IF(COUNTIF(Campaigns!$A${CAMP_FIRST}:$A${CAMP_LAST},B{n})>0,"✓","⚠ add to Campaigns tab"))')
        w.conditional_formatting.add(f"G3:G{last}", FormulaRule(formula=[f'LEFT(G3,1)="⚠"'], font=font(bold=True, color=RED)))
        w.freeze_panes = "A3"
        widths(w, {"A": 12, "B": 62, "C": 14, "D": 13, "E": 11, "F": 12, "G": 24})
        note(w, "I2", how)


# ---------------------------------------------------------------------------------------------
def campaigns(c, rows):
    title(c, "A1", "Campaigns – market, region, type and spend by month",
          "Every campaign in the data tabs needs a row here. Yellow = type it in when a new campaign starts. "
          "Market and region come from the location code in the campaign name.", "A2")
    # month boundaries (row 3 = start, row 4 = end)
    for i in range(12):
        col = L(6 + i)
        cell(c, f"{col}3", f"=DATE({S_YEAR},{i + 1},1)", "d mmm", size=8, color=MUTED, border=False, align="center")
        cell(c, f"{col}4", f"=EOMONTH({col}3,0)", "d mmm", size=8, color=MUTED, border=False, align="center")
    cell(c, "A3", "Check – spend in the data tabs that is missing from this list:", bold=True, border=False, size=9)
    cell(c, "D3", f"=Calc!F28-R6", AMT, bold=True, border=False)
    cell(c, "E3", '=IF(ABS(D3)<0.5,"✓ all listed","⚠ add the campaigns flagged in the data tabs")', bold=True, border=False, size=9)
    c.conditional_formatting.add("E3", FormulaRule(formula=['LEFT(E3,1)="⚠"'], font=font(bold=True, color=RED)))
    hdr = ["Campaign", "Channel", "Market", "Region", "Type"] + [f'=TEXT({L(6 + i)}3,"mmm")' for i in range(12)] + \
          [f'="Total ("&{S_CUR}&")"', "Clicks", "Conversions", "Cost per conversion"]
    header(c, 5, 1, hdr)
    cell(c, "A6", "Total – all campaigns listed", bold=True, fill=TOTAL)
    for col in "BCDE":
        cell(c, f"{col}6", "", fill=TOTAL)
    for j in range(6, 22):
        col = L(j)
        f = f"=SUM({col}{CAMP_FIRST}:{col}{CAMP_LAST})" if j <= 21 else ""
        cell(c, f"{col}6", f, AMT if j < 21 else AMT, bold=True, fill=TOTAL)
    cell(c, "U6", '=IF(T6=0,"",R6/T6)', AMT2, bold=True, fill=TOTAL)
    # unique campaigns with spend, sorted by channel then spend
    tot = collections.OrderedDict()
    for r in rows:
        k = (r["channel"], r["campaign"])
        tot[k] = tot.get(k, 0) + r["spend"]
    order = {n: i for i, (n, *_) in enumerate(CHANNELS)}
    camps = sorted(tot, key=lambda k: (order[k[0]], -tot[k]))
    for i in range(CAMP_LAST - CAMP_FIRST + 1):
        r = CAMP_FIRST + i
        if i < len(camps):
            ch, name = camps[i]
            mk, rg = CM.location(name)
            ty = CM.ctype(ch, name)
            vals = [name, ch, mk, rg, ty]
        else:
            vals = [None] * 5
        if i < len(camps) + 40:
            for j, v in enumerate(vals):
                cell(c, f"{L(1 + j)}{r}", v, fill=INPUT, color="0000FF" if v else INK)
            for m in range(12):
                col = L(6 + m)
                parts = []
                for name_, tab, srow, *_ in CHANNELS:
                    parts.append((name_, f"{sumifs(tab, 'C', f'{col}$3', f'{col}$4', f',{chr(39)}{tab}{chr(39)}!$B$3:$B${DMAX},$A{r}')}*{conv(srow)}"))
                f = "0"
                for name_, expr in reversed(parts):
                    f = f'IF($B{r}="{name_}",{expr},{f})'
                cell(c, f"{col}{r}", f'=IF($A{r}="","",{f})', AMT)
            cell(c, f"R{r}", f'=IF($A{r}="","",SUM(F{r}:Q{r}))', AMT, bold=True)
            for colx, src in (("S", "E"), ("T", "F")):
                f = "0"
                for name_, tab, srow, *_ in reversed(CHANNELS):
                    f = f"IF($B{r}=\"{name_}\",SUMIFS('{tab}'!${src}$3:${src}${DMAX},'{tab}'!$B$3:$B${DMAX},$A{r}),{f})"
                cell(c, f"{colx}{r}", f'=IF($A{r}="","",{f})', "#,##0")
            cell(c, f"U{r}", f'=IF(OR($A{r}="",T{r}=0),"",R{r}/T{r})', AMT2)
    dv = DataValidation(type="list", formula1='"Meta,Google Ads,ChatGPT Ads,LinkedIn Ads"', allow_blank=True)
    c.add_data_validation(dv); dv.add(f"B{CAMP_FIRST}:B{CAMP_LAST}")
    dv2 = DataValidation(type="list", formula1='"' + ",".join(REGIONS) + '"', allow_blank=True)
    c.add_data_validation(dv2); dv2.add(f"D{CAMP_FIRST}:D{CAMP_LAST}")
    c.freeze_panes = "B6"
    widths(c, {"A": 58, "B": 12, "C": 26, "D": 13, "E": 32, **{L(6 + i): 9.5 for i in range(12)},
               "R": 12, "S": 10, "T": 12, "U": 12})
    note(c, f"A{CAMP_FIRST + len(camps) + 41}",
         "How market/region were set: from the location code in the campaign name (e.g. 'Geo:EMEA', 'Geo:FR', 'Texas_EN_…'). "
         "Geo:SA is treated as Middle East (Saudi Arabia), as in the 2026/09 location file; Geo:NA as US & Canada; "
         "'Geo:US-UK-FR-IT', 'WW' and 'All' as Worldwide. 'Test 1' (ChatGPT) has no location in its name.")
    return camps


# ---------------------------------------------------------------------------------------------
def calc(k):
    title(k, "A1", "Calculations used by the Dashboard – don't edit", "Shown so every Dashboard number can be checked.", "A2")
    items = [
        (3, "Data up to", f"={S_UPTO}", DATE_F),
        (4, "Budget period starts", f"={S_PSTART}", DATE_F),
        (5, "Budget period ends", f"={S_PEND}", DATE_F),
        (6, "Days in budget period", "=C5-C4+1", "0"),
        (7, "Days gone (up to the data date)", "=MAX(0,MIN(C3,C5)-C4+1)", "0"),
        (8, "Days left", "=MAX(0,C5-MAX(C3,C4-1))", "0"),
        (9, "Share of the period gone", "=IF(C6>0,C7/C6,0)", "0.0%"),
        (10, "Last full month ends", "=IF(C3=EOMONTH(C3,0),C3,EOMONTH(C3,-1))", DATE_F),
        (11, "Last full month starts", "=EOMONTH(C10,-1)+1", DATE_F),
        (12, "Last 3 full months start", "=EOMONTH(C10,-3)+1", DATE_F),
        (13, "Last full week ends (Sunday)", "=C3-MOD(WEEKDAY(C3,2),7)", DATE_F),
        (14, "Last full week starts (Monday)", "=C13-6", DATE_F),
        (15, "Week before ends", "=C14-1", DATE_F),
        (16, "Week before starts", "=C15-6", DATE_F),
        (17, "Months left", "=C8/(365/12)", "0.00"),
        (18, "Days in last full month", "=C10-C11+1", "0"),
        (19, "Days in last 3 full months", "=C10-C12+1", "0"),
    ]
    for r, lab, f, fmt in items:
        cell(k, f"B{r}", lab)
        cell(k, f"C{r}", f, fmt, align="center")
    hdr = ["Channel", "Spend converter", "Counts toward budget?", "Budget", "Spent to date", "Spent last full month",
           "Spent last 3 full months", "Spent last full week", "Spent the week before", "Left", "% used",
           "Forecast – last-3-months pace", "Forecast – last-month pace"]
    header(k, 21, 2, hdr)
    for i, (name, tab, srow, *_) in enumerate(CHANNELS):
        r = 22 + i
        cell(k, f"B{r}", name, bold=True)
        cell(k, f"C{r}", f"=Settings!G{srow}", "0.0000", align="center")
        cell(k, f"D{r}", f"=Settings!E{srow}", align="center")
        cell(k, f"E{r}", f"=Settings!F{srow}", AMT)
        cell(k, f"F{r}", f"={sumifs(tab, 'C', '$C$4', 'MIN($C$3,$C$5)')}*C{r}", AMT)
        cell(k, f"G{r}", f"={sumifs(tab, 'C', '$C$11', '$C$10')}*C{r}", AMT)
        cell(k, f"H{r}", f"={sumifs(tab, 'C', '$C$12', '$C$10')}*C{r}", AMT)
        cell(k, f"I{r}", f"={sumifs(tab, 'C', '$C$14', '$C$13')}*C{r}", AMT)
        cell(k, f"J{r}", f"={sumifs(tab, 'C', '$C$16', '$C$15')}*C{r}", AMT)
        cell(k, f"K{r}", f'=IF(E{r}="","",E{r}-F{r})', AMT)
        cell(k, f"L{r}", f'=IF(OR(E{r}="",E{r}=0),"",F{r}/E{r})', "0.0%")
        cell(k, f"M{r}", f"=F{r}+H{r}/$C$19*$C$8", AMT)
        cell(k, f"N{r}", f"=F{r}+G{r}/$C$18*$C$8", AMT)
    cell(k, "B26", "Total – counts toward budget", bold=True, fill=TOTAL)
    cell(k, "B27", "Total – all channels", bold=True, fill=TOTAL)
    for col in "CD":
        cell(k, f"{col}26", "", fill=TOTAL); cell(k, f"{col}27", "", fill=TOTAL)
    for col in "EFGHIJMN":
        cell(k, f"{col}26", f'=SUMIFS({col}22:{col}25,$D$22:$D$25,"Yes")', AMT, bold=True, fill=TOTAL)
        cell(k, f"{col}27", f"=SUM({col}22:{col}25)" if col != "E" else "", AMT, bold=True, fill=TOTAL)
    cell(k, "K26", "=E26-F26", AMT, bold=True, fill=TOTAL)
    cell(k, "L26", '=IF(E26=0,"",F26/E26)', "0.0%", bold=True, fill=TOTAL)
    cell(k, "K27", "", fill=TOTAL); cell(k, "L27", "", fill=TOTAL)
    cell(k, "B28", "All spend in the data tabs (any date)", bold=True)
    parts = "+".join(f"SUM('{tab}'!$C$3:$C${DMAX})*Settings!$G${srow}" for name, tab, srow, *_ in CHANNELS)
    cell(k, "F28", f"={parts}", AMT, bold=True)
    extra = [
        (30, "Should have spent by now (straight-line plan)", "=E26*C9", AMT),
        (31, "Ahead (+) / behind (−) the straight-line plan", "=F26-C30", AMT),
        (32, "Allowed per month for the rest of the period", "=IF(C17<=0,0,K26/C17)", AMT),
        (33, "Average per month – last 3 full months", "=H26/3", AMT),
        (34, "Spent in the last full month", "=G26", AMT),
        (35, "Stretch budget (not confirmed)", f"={S_STRETCH}", AMT),
        (36, "Left if the stretch budget is approved", '=IF(C35="","",C35-F26)', AMT),
    ]
    for r, lab, f, fmt in extra:
        cell(k, f"B{r}", lab)
        cell(k, f"C{r}", f, fmt)
    widths(k, {"A": 2, "B": 40, "C": 15, **{c: 14 for c in "DEFGHIJKLMN"}})


# ---------------------------------------------------------------------------------------------
def monthly(m):
    title(m, "A1", "Monthly spend", None)
    cell(m, "A2", f'="Amounts in "&{S_CUR}&" · Meta converted from USD at 1 EUR = "&TEXT({S_FX},"0.00")&" USD · data up to "&TEXT({S_UPTO},"d mmm yyyy")',
         size=9, color=INK2, border=False, italic=True)
    cell(m, "Q2", "Data up to", size=8, color=MUTED, border=False, align="right")
    cell(m, "R2", f"={S_UPTO}", DATE_F, size=8, color=MUTED, border=False)
    hdr = ["Month", "Quarter", "Meta", "Google Ads", "ChatGPT Ads", "LinkedIn Ads", "Total – all channels",
           "Counts toward budget", "Plan (budget spread evenly by day)", "Over (+) / under (−) plan",
           "Cumulative spend (budget channels)", "Cumulative plan", "% of budget used", "Meta as billed (USD)", "Status", "Chart label"]
    header(m, 4, 1, hdr, height=42)
    for i in range(12):
        r = 5 + i
        cell(m, f"A{r}", f"=DATE({S_YEAR},{i + 1},1)", MON_F, bold=True)
        cell(m, f"B{r}", f'="Q"&ROUNDUP(MONTH(A{r})/3,0)', align="center")
        for j, (name, tab, srow, *_) in enumerate(CHANNELS):
            cell(m, f"{L(3 + j)}{r}", f"={sumifs(tab, 'C', f'$A{r}', f'EOMONTH($A{r},0)')}*{conv(srow)}", AMT)
        cell(m, f"G{r}", f"=SUM(C{r}:F{r})", AMT, bold=True)
        cell(m, f"H{r}", "=" + "+".join(f"{L(3 + j)}{r}*{counts(srow)}" for j, (n, t, srow, *_) in enumerate(CHANNELS)), AMT)
        cell(m, f"I{r}", f"={S_BTOTAL}*MAX(0,MIN(EOMONTH($A{r},0),{S_PEND})-MAX($A{r},{S_PSTART})+1)/({S_PEND}-{S_PSTART}+1)", AMT)
        cell(m, f"J{r}", f'=IF(EOMONTH($A{r},0)>{S_UPTO},"",H{r}-I{r})', AMT)
        cell(m, f"K{r}", f'=IF($A{r}>{S_UPTO},"",SUM($H$5:H{r}))', AMT)
        cell(m, f"L{r}", f"=SUM($I$5:I{r})", AMT)
        cell(m, f"M{r}", f'=IF(OR(K{r}="",{S_BTOTAL}=0),"",K{r}/{S_BTOTAL})', PCT, align="center")
        cell(m, f"N{r}", f"={sumifs('Meta data', 'C', f'$A{r}', f'EOMONTH($A{r},0)')}", AMT)
        cell(m, f"O{r}", f'=IF(EOMONTH($A{r},0)<={S_UPTO},"Complete",IF($A{r}<={S_UPTO},"In progress","Not started"))', align="center", size=9)
        cell(m, f"P{r}", f'=TEXT(A{r},"mmm")', size=8, color=MUTED, align="center")
    cell(m, "A17", "Total", bold=True, fill=TOTAL)
    cell(m, "B17", "", fill=TOTAL)
    for col in "CDEFGHIJN":
        cell(m, f"{col}17", f"=SUM({col}5:{col}16)", AMT, bold=True, fill=TOTAL)
    for col in "KLMOP":
        cell(m, f"{col}17", "", fill=TOTAL)
    note(m, "A18", "Over/under plan is shown for complete months only. The plan spreads the total budget evenly over the days of the budget period.")
    m.conditional_formatting.add("J5:J17", FormulaRule(formula=['AND(ISNUMBER(J5),J5>0)'], font=font(bold=True, color=RED)))
    m.conditional_formatting.add("A5:O16", FormulaRule(formula=['$A5>$R$2'], font=font(color=MUTED)))

    # performance block
    section(m, "A21", "CLICKS, CONVERSIONS AND COSTS – as reported by each platform", "ABCDEFGHIJKLMNO")
    groups = [("Meta", "Meta data", 17, "C"), ("Google Ads", "Google data", 18, "D"), ("ChatGPT Ads", "ChatGPT data", 19, "E")]
    cell(m, "A22", "", fill=NAVY); cell(m, "A23", "Month", bold=True, color=WHITE, fill=NAVY, align="center")
    for g, (name, tab, srow, scol) in enumerate(groups):
        c0 = 2 + g * 4
        m.merge_cells(start_row=22, start_column=c0, end_row=22, end_column=c0 + 3)
        cell(m, f"{L(c0)}22", name, bold=True, color=WHITE, fill=NAVY, align="center")
        header(m, 23, c0, ["Clicks", "Conversions", "Cost per click", "Cost per conversion"])
    for i in range(12):
        r = 24 + i
        cell(m, f"A{r}", f"=A{5 + i}", MON_F, bold=True)
        for g, (name, tab, srow, scol) in enumerate(groups):
            c0 = 2 + g * 4
            cl, cv, cpc, cpl = L(c0), L(c0 + 1), L(c0 + 2), L(c0 + 3)
            cell(m, f"{cl}{r}", f"={sumifs(tab, 'E', f'$A{r}', f'EOMONTH($A{r},0)')}", "#,##0")
            cell(m, f"{cv}{r}", f"={sumifs(tab, 'F', f'$A{r}', f'EOMONTH($A{r},0)')}", "#,##0")
            cell(m, f"{cpc}{r}", f'=IF({cl}{r}=0,"",{scol}{5 + i}/{cl}{r})', AMT2)
            cell(m, f"{cpl}{r}", f'=IF({cv}{r}=0,"",{scol}{5 + i}/{cv}{r})', AMT2)
    cell(m, "A36", "Total", bold=True, fill=TOTAL)
    for g, (name, tab, srow, scol) in enumerate(groups):
        c0 = 2 + g * 4
        cl, cv, cpc, cpl = L(c0), L(c0 + 1), L(c0 + 2), L(c0 + 3)
        cell(m, f"{cl}36", f"=SUM({cl}24:{cl}35)", "#,##0", bold=True, fill=TOTAL)
        cell(m, f"{cv}36", f"=SUM({cv}24:{cv}35)", "#,##0", bold=True, fill=TOTAL)
        cell(m, f"{cpc}36", f'=IF({cl}36=0,"",{scol}17/{cl}36)', AMT2, bold=True, fill=TOTAL)
        cell(m, f"{cpl}36", f'=IF({cv}36=0,"",{scol}17/{cv}36)', AMT2, bold=True, fill=TOTAL)
    note(m, "A37", "Conversions use each platform's own definition: Meta = 'Website registrations completed' (the website lead event); "
                   "Google Ads = 'Conversions' (its primary conversion actions). Compare each channel with itself over time, not with each other.")
    m.freeze_panes = "B5"
    widths(m, {"A": 11, "B": 9, **{c: 12 for c in "CDEFGHIJKLMN"}, "O": 12, "P": 8, "Q": 10, "R": 12})
    for r in range(24, 36):
        m.row_dimensions[r].height = 15


# ---------------------------------------------------------------------------------------------
def weekly(w, notes):
    title(w, "A1", "Weekly spend", None)
    cell(w, "A2", f'="Weeks run Monday to Sunday · amounts in "&{S_CUR}&" · data up to "&TEXT({S_UPTO},"ddd d mmm yyyy")&". Yellow columns are typed by you."',
         size=9, color=INK2, border=False, italic=True)
    hdr = ["Week", "Starts (Mon)", "Ends (Sun)", "Meta", "Google Ads", "ChatGPT Ads", "LinkedIn Ads", "Total – all channels",
           "Counts toward budget", "Plan (budget spread evenly by day)", "Over (+) / under (−) plan", "Cumulative spend (budget channels)",
           "Cumulative plan", "Meta conversions", "Meta cost per conversion", "Google conversions", "Google cost per conversion",
           "MQLs – paid social (HubSpot, optional)", "MQLs – paid search (HubSpot, optional)", "Notes – what happened this week"]
    header(w, 4, 1, hdr + ["Chart label"], height=54)
    cell(w, "A3", "Data up to:", size=8, color=MUTED, border=False)
    cell(w, "C3", f"={S_UPTO}", DATE_F, size=8, color=MUTED, border=False)
    cell(w, "D3", "Last full week ends:", size=8, color=MUTED, border=False)
    cell(w, "F3", "=Calc!C13", DATE_F, size=8, color=MUTED, border=False)
    if DRAFT:
        cell(w, "H3", DRAFT_WEEKLY, size=9, bold=True, color=RED, border=False)
    for col in "RST":
        w[f"{col}4"].fill = PatternFill("solid", fgColor=INPUT)
        w[f"{col}4"].font = font(9, True, INK)
    for i in range(53):
        r = 5 + i
        cell(w, f"A{r}", i + 1, "0", bold=True, align="center")
        cell(w, f"B{r}", f"={S_W1}+7*(A{r}-1)", DAY_F)
        cell(w, f"C{r}", f"=B{r}+6", DAY_F)
        for j, (name, tab, srow, *_) in enumerate(CHANNELS):
            cell(w, f"{L(4 + j)}{r}", f"={sumifs(tab, 'C', f'$B{r}', f'$C{r}')}*{conv(srow)}", AMT)
        cell(w, f"H{r}", f"=SUM(D{r}:G{r})", AMT, bold=True)
        cell(w, f"I{r}", "=" + "+".join(f"{L(4 + j)}{r}*{counts(srow)}" for j, (n, t, srow, *_) in enumerate(CHANNELS)), AMT)
        cell(w, f"J{r}", f"={S_BTOTAL}*MAX(0,MIN(C{r},{S_PEND})-MAX(B{r},{S_PSTART})+1)/({S_PEND}-{S_PSTART}+1)", AMT)
        cell(w, f"K{r}", f'=IF(C{r}>{S_UPTO},"",I{r}-J{r})', AMT)
        prev = f"L{r - 1}+" if i else ""
        cell(w, f"L{r}", f'=IF(B{r}>{S_UPTO},"",{prev}I{r})', AMT)
        cell(w, f"M{r}", f"=SUM($J$5:J{r})", AMT)
        cell(w, f"N{r}", f"={sumifs('Meta data', 'F', f'$B{r}', f'$C{r}')}", "#,##0")
        cell(w, f"O{r}", f'=IF(N{r}=0,"",D{r}/N{r})', AMT2)
        cell(w, f"P{r}", f"={sumifs('Google data', 'F', f'$B{r}', f'$C{r}')}", "#,##0")
        cell(w, f"Q{r}", f'=IF(P{r}=0,"",E{r}/P{r})', AMT2)
        cell(w, f"R{r}", None, "#,##0", fill=INPUT, color="0000FF")
        cell(w, f"S{r}", None, "#,##0", fill=INPUT, color="0000FF")
        cell(w, f"T{r}", notes.get(i + 1), fill=INPUT, color="0000FF", wrap=True, size=9)
        cell(w, f"U{r}", f'=TEXT(B{r},"d mmm")', size=8, color=MUTED, align="center")
    cell(w, "A58", "Total", bold=True, fill=TOTAL)
    for col in "BC":
        cell(w, f"{col}58", "", fill=TOTAL)
    for col in "DEFGHIJKNPRS":
        cell(w, f"{col}58", f"=SUM({col}5:{col}57)", AMT if col not in "NPRS" else "#,##0", bold=True, fill=TOTAL)
    for col in "LMOQT":
        cell(w, f"{col}58", "", fill=TOTAL)
    cell(w, "O58", '=IF(N58=0,"",D58/N58)', AMT2, bold=True, fill=TOTAL)
    cell(w, "Q58", '=IF(P58=0,"",E58/P58)', AMT2, bold=True, fill=TOTAL)
    note(w, "A59", "Week 1 includes the last days of the previous year (no data there). Over/under plan is shown for complete weeks only.")
    w.conditional_formatting.add("A5:S57", FormulaRule(formula=["$B5>$C$3"], font=font(color=MUTED)))
    w.conditional_formatting.add("A5:Q57", FormulaRule(formula=["$C5=$F$3"], fill=PatternFill("solid", fgColor="E2EFDA"),
                                                       font=font(bold=True)))
    w.conditional_formatting.add("K5:K57", FormulaRule(formula=["AND(ISNUMBER(K5),K5>0)"], font=font(bold=True, color=RED)))
    w.freeze_panes = "D5"
    widths(w, {"A": 6, "B": 11, "C": 11, **{c: 11 for c in "DEFGHIJKLMNOPQ"}, "R": 12, "S": 12, "T": 60, "U": 8})
    # weekly chart under the table
    ch = BarChart(); ch.type = "col"; ch.grouping = "stacked"; ch.overlap = 100; ch.gapWidth = 40
    for j, (name, tab, srow, *_) in enumerate(CHANNELS):
        ref = Reference(w, min_col=4 + j, min_row=4, max_row=57)
        ch.add_data(ref, titles_from_data=True)
    ch.set_categories(Reference(w, min_col=21, min_row=5, max_row=57))
    style_bar(ch, [CH_COLORS[n] for n, *_ in CHANNELS])
    ch.width, ch.height = 30, 9
    section(w, "A61", "WEEKLY SPEND BY CHANNEL", "ABCDEFGHIJ")
    w.add_chart(ch, "A62")


# ---------------------------------------------------------------------------------------------
def style_axes(ch, yfmt="#,##0"):
    ch.y_axis.numFmt = yfmt
    ch.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="E1E0D9", w=6350))
    ch.y_axis.spPr = GraphicalProperties(ln=LineProperties(noFill=True))
    ch.x_axis.spPr = GraphicalProperties(ln=LineProperties(solidFill="C3C2B7", w=9525))
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.legend.position = "b"


def style_bar(ch, colors):
    for s, col in zip(ch.series, colors):
        s.graphicalProperties.solidFill = col
        s.graphicalProperties.line.solidFill = "FFFFFF"
        s.graphicalProperties.line.width = 12700
    style_axes(ch)


# ---------------------------------------------------------------------------------------------
def by_location(b, rows):
    title(b, "A1", "Spend by region, market and campaign type", None)
    cell(b, "A2", f'="Amounts in "&{S_CUR}&" · location and type come from the Campaigns tab (based on the campaign names) · data up to "&TEXT({S_UPTO},"d mmm yyyy")',
         size=9, color=INK2, border=False, italic=True)
    months = [f'=TEXT(Campaigns!{L(6 + i)}3,"mmm")' for i in range(12)]
    camp = lambda col: f"Campaigns!{col}${CAMP_FIRST}:{col}${CAMP_LAST}"

    def block(top, label, key_col, keys, first, region_col=False):
        section(b, f"A{top}", label, "ABCDEFGHIJKLMNOPQ")
        cols = ["Region"] if region_col else []
        first_m = 2 + len(cols)
        header(b, top + 1, 1, [first] + cols + months + ["Total", "Share", "Share of spend"])
        r0 = top + 2
        for i, k in enumerate(keys):
            r = r0 + i
            name = k[0] if isinstance(k, tuple) else k
            cell(b, f"A{r}", name, bold=True)
            if region_col:
                cell(b, f"B{r}", k[1], align="center", size=9)
            for mth in range(12):
                col = L(first_m + mth)
                cell(b, f"{col}{r}", f"=SUMIFS({camp(L(6 + mth))},{camp(key_col)},$A{r})", AMT)
        rl = r0 + len(keys)          # "not listed" row
        rt = rl + 1                  # total row
        cell(b, f"A{rl}", "Other / not listed above", italic=True)
        if region_col:
            cell(b, f"B{rl}", "")
        for mth in range(12):
            col = L(first_m + mth)
            cell(b, f"{col}{rl}", f"=Campaigns!{L(6 + mth)}$6-SUM({col}{r0}:{col}{rl - 1})", AMT)
            cell(b, f"{col}{rt}", f"=SUM({col}{r0}:{col}{rl})", AMT, bold=True, fill=TOTAL)
        cell(b, f"A{rt}", "Total", bold=True, fill=TOTAL)
        if region_col:
            cell(b, f"B{rt}", "", fill=TOTAL)
        tc, sc, bc = L(first_m + 12), L(first_m + 13), L(first_m + 14)
        for r in range(r0, rt + 1):
            is_t = r == rt
            cell(b, f"{tc}{r}", f"=SUM({L(first_m)}{r}:{L(first_m + 11)}{r})", AMT, bold=True, fill=TOTAL if is_t else None)
            cell(b, f"{sc}{r}", f'=IF(${tc}${rt}=0,"",{tc}{r}/${tc}${rt})', PCT, fill=TOTAL if is_t else None, align="center")
            cell(b, f"{bc}{r}", "" if is_t else f'=IF({sc}{r}="","",REPT("█",ROUND({sc}{r}*40,0)))',
                 fill=TOTAL if is_t else None, color=INK2, size=8)
        return r0, rl, rt, tc

    # totals per key from the python side, to order the lists (largest first)
    tot_m, tot_t, reg_of = collections.Counter(), collections.Counter(), {}
    for r in rows:
        eur = r["spend"] / 1.16 if r["channel"] == "Meta" else r["spend"]
        mk, rg = CM.location(r["campaign"])
        tot_m[mk] += eur; reg_of[mk] = rg
        tot_t[CM.ctype(r["channel"], r["campaign"])] += eur
    markets = [(m, reg_of[m]) for m, _ in tot_m.most_common()]
    types = [t for t, _ in tot_t.most_common()]
    reg = block(4, "BY REGION", "D", REGIONS, "Region")
    mkt = block(reg[2] + 3, "BY MARKET", "C", markets, "Market", region_col=True)
    typ = block(mkt[2] + 3, "BY CAMPAIGN TYPE", "E", types, "Campaign type")
    b.freeze_panes = "B4"
    widths(b, {"A": 32, "B": 13, **{L(3 + i): 9.5 for i in range(12)}, "O": 11, "P": 11, "Q": 9, "R": 30})
    b.column_dimensions["B"].width = 12
    b._loc = dict(region=reg, market=mkt, type=typ, n_markets=len(markets))
    return reg, mkt


# ---------------------------------------------------------------------------------------------
def agency_tab(a, agency):
    title(a, "A1", "Agency weekly reports vs. platform data", None)
    note(a, "A2", "Figures the agency reported in its weekly Notion reports, next to what the platform exports show for the same week. "
                  "Pending: filled in from the Notion extraction.")
    hdr = ["Week starts", "Week ends", "Period type", "Meta – agency", "Meta – platform (USD, as billed)", "Difference",
           "Google – agency", "Google – platform (EUR, as billed)", "Difference", "Leads – agency", "What the agency did or recommended", "Link"]
    header(a, 4, 1, hdr, height=42)
    rows = agency or []
    for i, ag in enumerate(rows):
        r = 5 + i
        cell(a, f"A{r}", ag["start"], DATE_F)
        cell(a, f"B{r}", ag["end"], DATE_F)
        cell(a, f"C{r}", ag.get("period", "week"), align="center")
        cell(a, f"D{r}", ag.get("meta"), AMT2, color="0000FF")
        cell(a, f"E{r}", f"={sumifs('Meta data', 'C', f'$A{r}', f'$B{r}')}", AMT2)
        cell(a, f"F{r}", f'=IF(D{r}="","",D{r}-E{r})', AMT2)
        cell(a, f"G{r}", ag.get("google"), AMT2, color="0000FF")
        cell(a, f"H{r}", f"={sumifs('Google data', 'C', f'$A{r}', f'$B{r}')}", AMT2)
        cell(a, f"I{r}", f'=IF(G{r}="","",G{r}-H{r})', AMT2)
        cell(a, f"J{r}", ag.get("leads"), "#,##0", color="0000FF")
        cell(a, f"K{r}", ag.get("notes"), wrap=True, size=9)
        cell(a, f"L{r}", ag.get("link"), size=8)
    a.freeze_panes = "C5"
    widths(a, {"A": 12, "B": 12, "C": 10, "D": 12, "E": 14, "F": 11, "G": 12, "H": 14, "I": 11, "J": 10, "K": 70, "L": 30})


# ---------------------------------------------------------------------------------------------
def how_to(h, source_note):
    title(h, "A1", "How to update this tracker", None)
    lines = [
        ("EVERY MONDAY (about 15 minutes)", None),
        ("1", "Google Ads → Reports → open the saved report 'PnP spend tracker' (Campaign × Day: Cost, Impr., Clicks, Conversions). "
              "Date range: last week (Mon–Sun). Download as CSV."),
        ("2", "Copy the rows (without the header) and paste them under the last row of the 'Google data' tab, starting in column A."),
        ("3", "Meta Ads Manager → Campaigns → same date range → Breakdown: By time → Day → saved columns 'PnP spend tracker' "
              "(Campaign name, Amount spent, Impressions, Link clicks, Website registrations completed) → Export table data (CSV). "
              "Paste under the last row of 'Meta data'."),
        ("4", "If ChatGPT Ads or LinkedIn Ads ran, do the same for their tabs."),
        ("5", "Settings tab → change 'Data up to' to last Sunday."),
        ("6", "In the data tabs, column G must show ✓. If it says '⚠ add to Campaigns tab', add that campaign at the bottom of the "
              "Campaigns tab with its channel, market, region and type."),
        ("7", "Weekly tab → write 1–2 lines in 'Notes' for the week (launches, pauses, budget changes, anything unusual). "
              "Optional: add MQLs by channel from HubSpot."),
        ("8", "Dashboard → check the status column and the forecast. Flag anything red to Raúl."),
        ("ONCE A MONTH (first Monday)", None),
        ("9", "Check last month's totals on the Monthly tab against the invoices or billing pages (Meta: Billing & payments; Google Ads: Billing → Summary)."),
        ("10", "If Finance gives a new EUR/USD rate, update it on the Settings tab."),
        ("ONE-TIME SETUP", None),
        ("11", "Save the two reports described in steps 1 and 3, with the columns in exactly that order, so every week the export pastes straight in."),
        ("RULES OF THE WORKBOOK", None),
        ("•", "Yellow cells = typed by you. White cells = formulas; don't type over them."),
        ("•", "Paste spend exactly as each platform bills it (Meta in USD, Google Ads and ChatGPT Ads in EUR). The workbook converts."),
        ("•", "Never paste the same week twice. If you need to redo a week, delete its rows in the data tab first."),
        ("SOURCES AND NOTES", None),
    ]
    r = 3
    for a, b in lines:
        if b is None:
            section(h, f"A{r}", a, "AB"); r += 1; continue
        cell(h, f"A{r}", a, bold=True, align="center", border=False)
        cell(h, f"B{r}", b, wrap=True, border=False)
        h.row_dimensions[r].height = 30 if len(b) > 110 else 16
        r += 1
    for t in source_note.split("\n"):
        if t.strip():
            cell(h, f"B{r}", t, wrap=True, border=False, size=9, color=INK2)
            h.row_dimensions[r].height = 28 if len(t) > 120 else 15
            r += 1
    widths(h, {"A": 6, "B": 130})


# ---------------------------------------------------------------------------------------------
def dashboard(d, markets):
    d.sheet_view.showGridLines = False
    widths(d, {"A": 2, **{L(2 + i): 12.5 for i in range(12)}, "N": 2})
    d.merge_cells("B1:M1")
    cell(d, "B1", '="Paid Media Spend "&' + S_YEAR + '&" – Year Overview"', size=18, bold=True, color=NAVY, border=False)
    d.row_dimensions[1].height = 30
    d.merge_cells("B2:M2")
    cell(d, "B2", f'="Data up to "&TEXT({S_UPTO},"d mmm yyyy")&" · amounts in "&{S_CUR}&" · Meta converted from USD at 1 EUR = "&TEXT({S_FX},"0.00")&" USD · budget channels: Meta + Google Ads"',
         size=9, color=INK2, border=False, italic=True)
    d.merge_cells("B3:M3")
    cell(d, "B3", f'="Budget status: "&{S_STATUS}', size=9, bold=True, color="7F5F00", fill=BANNER, border=False)
    d.row_dimensions[3].height = 20
    if DRAFT:
        d.merge_cells("B4:M4")
        cell(d, "B4", DRAFT_DASH, size=9, bold=True, color=RED, border=False)
    cell(d, "P1", "Helper cells for formatting – don't edit", size=8, color=MUTED, border=False)
    cell(d, "P2", "=Calc!C9", "0.0%", size=8, color=MUTED, border=False)

    tiles = [
        (f'="BUDGET "&{S_YEAR}', f"={CUR('Calc!E26')}", f'="Meta "&{CUR("Calc!E22")}&" · Google "&{CUR("Calc!E23")}'),
        ('="SPENT SO FAR"', f"={CUR('Calc!F26')}", f'=TEXT(Calc!L26,"0%")&" of budget · "&TEXT(Calc!C9,"0%")&" of the year gone"'),
        ('="LEFT TO SPEND"', f'=IF(Calc!K26<0,"–"&{CUR("-Calc!K26")},{CUR("Calc!K26")})',
         f'=IF(Calc!K26<0,"Budget already exceeded","≈ "&{CUR("Calc!C32")}&" a month until "&TEXT(Calc!C5,"d mmm"))'),
        ('="FORECAST YEAR-END"', f"={CUR('Calc!M26')}",
         f'=IF(Calc!M26>Calc!E26,"▲ "&{CUR("Calc!M26-Calc!E26")}&" over budget","▼ "&{CUR("Calc!E26-Calc!M26")}&" under budget")&" (last-3-months pace)"'),
        ('="LAST FULL MONTH ("&UPPER(TEXT(Calc!C11,"mmm"))&")"', f"={CUR('Calc!G26')}",
         f'="Allowed a month from now on: "&IF(Calc!C32<0,"none",{CUR("Calc!C32")})'),
        ('="LAST FULL WEEK (FROM "&UPPER(TEXT(Calc!C14,"d mmm"))&")"', f'=IF(Calc!I26=0,"—",{CUR("Calc!I26")})',
         f'=IF(Calc!J26=0,"No data for the week before","vs "&{CUR("Calc!J26")}&" the week before")'),
    ]
    for i, (lab, val, sub) in enumerate(tiles):
        c1, c2 = L(2 + 2 * i), L(3 + 2 * i)
        for r in (5, 6, 7):
            d.merge_cells(f"{c1}{r}:{c2}{r}")
        cell(d, f"{c1}5", lab, size=8, bold=True, color=INK2, fill=SUBTLE, border=False, align="left")
        cell(d, f"{c1}6", val, size=18, bold=True, color=INK, fill=SUBTLE, border=False, align="left")
        cell(d, f"{c1}7", sub, size=8, color=INK2, fill=SUBTLE, border=False, align="left", wrap=True)
        for r in (5, 6, 7):
            d[f"{c2}{r}"].fill = PatternFill("solid", fgColor=SUBTLE)
    d.row_dimensions[5].height = 18; d.row_dimensions[6].height = 30; d.row_dimensions[7].height = 30
    d.conditional_formatting.add("H7", FormulaRule(formula=["$K$15>$D$15"], font=font(8, True, RED)))
    d.conditional_formatting.add("F6", FormulaRule(formula=["$F$15<0"], font=font(18, True, RED)))

    # channel table
    section(d, "B9", "BUDGET VS. SPEND BY CHANNEL", [L(2 + i) for i in range(12)])
    d.merge_cells("B10:C10"); d.merge_cells("H10:J10"); d.merge_cells("L10:M10")
    hdr = {"B": "Channel", "D": f'="Budget ("&{S_CUR}&")"', "E": f'="Spent ("&{S_CUR}&")"', "F": "Left", "G": "% used",
           "H": '="Progress  (year gone: "&TEXT(Calc!C9,"0%")&")"', "K": "Forecast year-end", "L": "Status"}
    for col in "BCDEFGHIJKLM":
        cell(d, f"{col}10", hdr.get(col), bold=True, color=WHITE, fill=NAVY, align="center", wrap=True, size=9)
    d.row_dimensions[10].height = 28
    rows = [(n, 22 + i) for i, (n, *_) in enumerate(CHANNELS)] + [("Total – budget channels", 26)]
    for i, (name, cr) in enumerate(rows):
        r = 11 + i
        tot = name.startswith("Total")
        fill = TOTAL if tot else None
        d.merge_cells(f"B{r}:C{r}"); d.merge_cells(f"H{r}:J{r}"); d.merge_cells(f"L{r}:M{r}")
        yes = "TRUE" if tot else f'Calc!D{cr}="Yes"'
        cell(d, f"B{r}", name, bold=True, fill=fill)
        cell(d, f"C{r}", None, fill=fill)
        cell(d, f"D{r}", f'=IF({yes},Calc!E{cr},"Not in budget")', AMT, fill=fill, align="right", bold=tot)
        cell(d, f"E{r}", f"=Calc!F{cr}", AMT, fill=fill, bold=tot)
        cell(d, f"F{r}", f'=IF({yes},Calc!K{cr},"")', AMT, fill=fill, bold=tot)
        cell(d, f"G{r}", f'=IF({yes},Calc!L{cr},"")', PCT, fill=fill, align="center", bold=tot)
        cell(d, f"H{r}", f'=IF(G{r}="","",REPT("█",ROUND(MIN(G{r},1)*24,0))&REPT("░",24-ROUND(MIN(G{r},1)*24,0)))',
             fill=fill, color=INK2, size=8, align="left")
        for col in "IJ":
            cell(d, f"{col}{r}", None, fill=fill)
        cell(d, f"K{r}", f'=IF({yes},Calc!M{cr},"")', AMT, fill=fill, bold=tot)
        cell(d, f"L{r}", f'=IF(NOT({yes}),"Outside budget",IF(Calc!F{cr}>=Calc!E{cr},"▲ Budget used up",'
                         f'IF(Calc!M{cr}>Calc!E{cr}*1.02,"▲ Over budget at current pace",IF(Calc!M{cr}<Calc!E{cr}*0.9,"▼ Under-spending","● On track"))))',
             fill=fill, bold=True, size=9)
        cell(d, f"M{r}", None, fill=fill)
    note(d, "B16", "Forecast = spent so far + the average daily spend of the last 3 full months × the days left. "
                   "ChatGPT Ads and LinkedIn Ads are outside the budget (Settings tab).")
    d.conditional_formatting.add("L11:L15", FormulaRule(formula=['LEFT(L11,1)="▲"'], font=font(9, True, RED)))
    d.conditional_formatting.add("L11:L15", FormulaRule(formula=['LEFT(L11,1)="▼"'], font=font(9, True, AMBER)))
    d.conditional_formatting.add("L11:L15", FormulaRule(formula=['LEFT(L11,1)="●"'], font=font(9, True, GREEN)))
    d.conditional_formatting.add("H11:H15", FormulaRule(formula=["AND(ISNUMBER(G11),G11>=1)"], font=font(8, False, RED)))
    d.conditional_formatting.add("H11:H15", FormulaRule(formula=["AND(ISNUMBER(G11),G11>$P$2+0.05,G11<1)"], font=font(8, False, AMBER)))

    # charts: monthly by channel + plan, cumulative vs plan
    m = d.parent["Monthly"]
    section(d, "B18", "SPEND BY MONTH AND CHANNEL vs. PLAN", ["B", "C", "D", "E", "F", "G"])
    section(d, "H18", "SPEND SO FAR vs. PLAN (CUMULATIVE)", ["H", "I", "J", "K", "L", "M"])
    bar = BarChart(); bar.type = "col"; bar.grouping = "stacked"; bar.overlap = 100; bar.gapWidth = 60
    for j in range(4):
        bar.add_data(Reference(m, min_col=3 + j, min_row=4, max_row=16), titles_from_data=True)
    bar.set_categories(Reference(m, min_col=16, min_row=5, max_row=16))
    style_bar(bar, [CH_COLORS[n] for n, *_ in CHANNELS])
    ln = LineChart()
    ln.add_data(Reference(m, min_col=9, min_row=4, max_row=16), titles_from_data=True)
    plan_line(ln.series[0])
    bar += ln
    bar.x_axis.tickLblSkip = 1
    bar.width, bar.height = 16.2, 8.2
    d.add_chart(bar, "B19")
    cum = BarChart(); cum.type = "col"; cum.gapWidth = 60
    cum.add_data(Reference(m, min_col=11, min_row=4, max_row=16), titles_from_data=True)
    cum.set_categories(Reference(m, min_col=16, min_row=5, max_row=16))
    style_bar(cum, [NAVY])
    ln2 = LineChart()
    ln2.add_data(Reference(m, min_col=12, min_row=4, max_row=16), titles_from_data=True)
    plan_line(ln2.series[0])
    cum += ln2
    cum.x_axis.tickLblSkip = 1
    cum.width, cum.height = 16.2, 8.2
    d.add_chart(cum, "H19")

    # quarters
    top = 36
    section(d, f"B{top}", "QUARTER BY QUARTER", [L(2 + i) for i in range(12)])
    d.merge_cells(f"B{top + 1}:C{top + 1}"); d.merge_cells(f"K{top + 1}:M{top + 1}")
    qh = {"B": "Quarter", "D": "Meta", "E": "Google Ads", "F": "ChatGPT Ads", "G": "LinkedIn Ads", "H": "Total – all channels",
          "I": "Counts toward budget", "J": "Plan", "K": "Status"}
    for col in "BCDEFGHIJKLM":
        cell(d, f"{col}{top + 1}", qh.get(col), bold=True, color=WHITE, fill=NAVY, align="center", wrap=True, size=9)
    d.row_dimensions[top + 1].height = 28
    for q in range(4):
        r = top + 2 + q
        a, z = 5 + 3 * q, 7 + 3 * q
        d.merge_cells(f"B{r}:C{r}"); d.merge_cells(f"K{r}:M{r}")
        cell(d, f"B{r}", f'="Q{q + 1}  ("&TEXT(Monthly!A{a},"mmm")&"–"&TEXT(Monthly!A{z},"mmm")&")"', bold=True)
        cell(d, f"C{r}", None)
        for j, col in enumerate("DEFG"):
            cell(d, f"{col}{r}", f"=SUM(Monthly!{L(3 + j)}{a}:{L(3 + j)}{z})", AMT)
        cell(d, f"H{r}", f"=SUM(D{r}:G{r})", AMT, bold=True)
        cell(d, f"I{r}", f"=SUM(Monthly!H{a}:H{z})", AMT)
        cell(d, f"J{r}", f"=SUM(Monthly!I{a}:I{z})", AMT)
        nxt = f'IF({S_UPTO}<EOMONTH(Monthly!A{z + 3},0),"Complete · last quarter","Complete")' if q < 3 else '"Complete"'
        cell(d, f"K{r}", f'=IF({S_UPTO}>=EOMONTH(Monthly!A{z},0),{nxt},IF({S_UPTO}>=Monthly!A{a},"In progress","Not started"))',
             align="center", size=9)
        for col in "LM":
            cell(d, f"{col}{r}", None)
    r = top + 6
    d.merge_cells(f"B{r}:C{r}"); d.merge_cells(f"K{r}:M{r}")
    cell(d, f"B{r}", "Total", bold=True, fill=TOTAL); cell(d, f"C{r}", None, fill=TOTAL)
    for col in "DEFGHIJ":
        cell(d, f"{col}{r}", f"=SUM({col}{top + 2}:{col}{top + 5})", AMT, bold=True, fill=TOTAL)
    for col in "KLM":
        cell(d, f"{col}{r}", None, fill=TOTAL)
    d.conditional_formatting.add(f"B{top + 2}:M{top + 5}", FormulaRule(formula=[f'ISNUMBER(SEARCH("last quarter",$K{top + 2}))'],
                                                                       fill=PatternFill("solid", fgColor="E2EFDA")))

    # outlook
    top = 44
    section(d, f"B{top}", "YEAR-END OUTLOOK (budget channels)", [L(2 + i) for i in range(12)])
    for rr in range(top + 1, top + 6):
        d.merge_cells(f"B{rr}:E{rr}"); d.merge_cells(f"I{rr}:M{rr}")
    oh = {"B": "If spending continues at…", "F": '="Per month ("&' + S_CUR + '&")"', "G": "Year-end total", "H": "vs. budget", "I": "What it means"}
    for col in "BCDEFGHIJKLM":
        cell(d, f"{col}{top + 1}", oh.get(col), bold=True, color=WHITE, fill=NAVY, align="center", wrap=True, size=9)
    d.row_dimensions[top + 1].height = 24
    rows = [
        ('="…last month\'s pace ("&TEXT(Calc!C11,"mmmm")&")"', "=Calc!C34", "=Calc!N26"),
        ('="…the pace of the last 3 months ("&TEXT(Calc!C12,"mmm")&"–"&TEXT(Calc!C10,"mmm")&")"', "=Calc!C33", "=Calc!M26"),
        ('="…a pace that lands exactly on budget"', "=MAX(0,Calc!C32)", "=Calc!E26"),
    ]
    for i, (lab, pm, ye) in enumerate(rows):
        r = top + 2 + i
        cell(d, f"B{r}", lab, bold=True)
        for col in "CDE":
            cell(d, f"{col}{r}", None)
        cell(d, f"F{r}", pm, AMT)
        cell(d, f"G{r}", ye, AMT, bold=True)
        cell(d, f"H{r}", f"=G{r}-Calc!$E$26", AMT)
        if i < 2:
            what = f'=IF(H{r}>0,"Over budget by "&{CUR(f"H{r}")},"Under budget by "&{CUR(f"-H{r}")})'
        else:
            what = ('=IF(Calc!K26<=0,"The budget is already used up",IF(Calc!C34=0,"",IF(Calc!C32<Calc!C34,'
                    'TEXT(1-Calc!C32/Calc!C34,"0%")&" less per month than last month",TEXT(Calc!C32/Calc!C34-1,"0%")&" more per month than last month")))')
        cell(d, f"I{r}", what, size=9)
        for col in "JKLM":
            cell(d, f"{col}{r}", None)
    r = top + 5
    cell(d, f"B{r}", f'="If the stretch budget of "&{CUR(S_STRETCH)}&" is approved"', bold=True)
    for col in "CDE":
        cell(d, f"{col}{r}", None)
    cell(d, f"F{r}", '=IF(Calc!C36="","",MAX(0,Calc!C36)/MAX(Calc!C17,0.01))', AMT)
    cell(d, f"G{r}", f"={S_STRETCH}", AMT, bold=True)
    cell(d, f"H{r}", "", AMT)
    cell(d, f"I{r}", f'=IF(Calc!C36="","","Left to spend: "&{CUR("Calc!C36")}&" (≈ per month shown on the left)")', size=9)
    for col in "JKLM":
        cell(d, f"{col}{r}", None)
    d.conditional_formatting.add(f"H{top + 2}:H{top + 3}", FormulaRule(formula=[f"H{top + 2}>0"], font=font(10, True, RED)))

    # region + market charts
    top = 51
    b = d.parent["By location & type"]
    loc = b._loc
    section(d, f"B{top}", "WHERE THE MONEY WENT – BY REGION", ["B", "C", "D", "E", "F", "G"])
    section(d, f"H{top}", "TOP MARKETS (year to date)", ["H", "I", "J", "K", "L", "M"])
    r0, rl, rt, tc = loc["region"]
    reg = BarChart(); reg.type = "bar"; reg.gapWidth = 50
    reg.add_data(Reference(b, min_col=14, min_row=r0, max_row=rl - 1), titles_from_data=False)
    reg.set_categories(Reference(b, min_col=1, min_row=r0, max_row=rl - 1))
    style_bar(reg, [SLATE]); reg.legend = None
    value_labels(reg)
    reg.y_axis.delete = False
    reg.x_axis.scaling.orientation = "maxMin"
    reg.width, reg.height = 16.2, 7
    d.add_chart(reg, f"B{top + 1}")
    m0, ml, mt, mtc = loc["market"]
    nshow = min(10, loc["n_markets"])
    mk = BarChart(); mk.type = "bar"; mk.gapWidth = 40
    mk.add_data(Reference(b, min_col=15, min_row=m0, max_row=m0 + nshow - 1), titles_from_data=False)
    mk.set_categories(Reference(b, min_col=1, min_row=m0, max_row=m0 + nshow - 1))
    style_bar(mk, [SLATE]); mk.legend = None
    value_labels(mk)
    mk.x_axis.scaling.orientation = "maxMin"
    mk.width, mk.height = 16.2, 7
    d.add_chart(mk, f"H{top + 1}")
    note(d, f"B{top + 16}", "Region and market come from the location code in each campaign name – see the 'By location & type' and 'Campaigns' tabs. "
                            "Sources, exchange rate and how to update: 'How to update' tab.")
    d.column_dimensions["P"].hidden = True
    d.print_area = "A1:N68"
    d.print_options.horizontalCentered = True
    d.page_setup.orientation = "landscape"
    d.page_setup.fitToWidth = 1
    d.sheet_properties.pageSetUpPr.fitToPage = True
    d.page_setup.fitToHeight = 0


def value_labels(ch):
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ch.dataLabels.showSerName = ch.dataLabels.showCatName = ch.dataLabels.showLegendKey = False
    ch.dataLabels.numFmt = "#,##0"
    ch.dataLabels.position = "outEnd"


def plan_line(s):
    s.graphicalProperties.line.solidFill = INK2
    s.graphicalProperties.line.width = 22225
    s.graphicalProperties.line.dashStyle = "dash"
    s.marker.symbol = "none"
    s.smooth = False


if __name__ == "__main__":
    import load_monthly as LM
    out, upto = sys.argv[1], datetime.date.fromisoformat(sys.argv[2])
    DRAFT = "--draft" in sys.argv
    rows = LM.all_rows()
    src = ("Test build: platform exports by campaign and month (1 Jan – 30 Sep 2026), so each month's spend sits on the 1st of the month.\n")
    build(out, upto, rows, source_note=src)
    print("saved", out)
