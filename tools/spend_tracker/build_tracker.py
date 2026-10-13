"""PnP Paid Media Spend Tracker 2026 – v5, built to be opened in Google Sheets.

Usage (from this folder): python build_tracker.py OUT.xlsx META_EXPORT.csv GOOGLE_EXPORT.csv

Tabs: Dashboard · Update · Weekly · Monthly · By location · Meta export · Google export · Other channels · Settings · Agency check
(+ hidden Calc). About 5,000 formulas, all SUMIFS / INDEX / MATCH / IF / TEXT, so Google Sheets stays fast.
Market and campaign type are read straight from the campaign names with wildcard SUMIFS (no per-row helper formulas).
Charts are plain stacked-column and line charts, which Google Sheets imports as they are.
"""
import sys, os, datetime
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as L
from openpyxl.chart import BarChart, LineChart, Reference
from xlstyle import *
import load_exports as LX

FX_RATE = 1.1177
FX_SOURCE = "Live rate on 13 Oct 2026 (from Felipe). Replace with Finance's monthly rates if they use them."
REGIONS = ["EMEA", "Americas", "Global", "Not specified"]
SLATE, GREENFILL, BLUE_T, PALE = "6B7A8F", "E2EFDA", "0000FF", "F3F7FD"
META_CAP, GOOGLE_CAP = 15000, 7000
NF = 30
MX, GX = "'Meta export'!$A:$AD", "'Google export'!$A:$AD"
OC_FIRST, OC_N = 5, 200
OC = lambda col: f"'Other channels'!${col}${OC_FIRST}:${col}${OC_FIRST + OC_N - 1}"

# Settings cells
S_YEAR, S_BUDGET, S_MAX, S_ORIG, S_STATUS = "Settings!$B$5", "Settings!$B$6", "Settings!$B$7", "Settings!$B$8", "Settings!$B$9"
S_PSTART, S_PEND, S_W1, S_UPTO = "Settings!$B$10", "Settings!$C$10", "Settings!$B$11", "Settings!$B$16"
S_FX, S_FXAVG = "Settings!$B$27:$B$38", "Settings!$B$39"
CHANNELS = [("Meta", 20, "USD"), ("Google Ads", 21, "EUR"), ("ChatGPT Ads", 22, "EUR"), ("LinkedIn Ads", 23, "USD")]
ENDED_FIRST, ENDED_N = 44, 10
LOC_FIRST, LOC_N, MKT_FIRST, MKT_N = 59, 60, 59, 40
# Calc cells
CM_HDR, CM_DATE, CM_END, CM_CAMP, CM_SPEND, CM_CLK, CM_CONV = (f"Calc!$C${r}" for r in range(64, 71))
CG_HDR, CG_CAMP, CG_DAY, CG_COST, CG_CLK, CG_CONV, CG_CUR = (f"Calc!$C${r}" for r in range(76, 83))
CK_FIRST, CK_N, CK_COUNT = 86, 6, "Calc!$C$93"
EN_FIRST = 96
CODE0, MK0, TY0 = 109, 172, 215
M_FIRST = 5    # Monthly tab: first month row (header on row 4)
W_FIRST = 5    # Weekly tab: first week row (header on row 4)
TYPES = ["Meta – lead ads, prospecting", "Meta – lead ads, retargeting", "Meta – traffic", "Meta – other",
         "Google – Search, non-brand", "Google – Search, brand", "Google – Search, coworking", "Google – Performance Max",
         "Google – YouTube video", "Google – Demand Gen / YouTube reach", "Google – other", "ChatGPT Ads", "LinkedIn Ads"]
MARKETS = [("EMEA – multi-country", "EMEA"), ("Western Europe – multi-country", "EMEA"), ("UK", "EMEA"), ("France", "EMEA"),
           ("Germany", "EMEA"), ("Spain", "EMEA"), ("Italy", "EMEA"), ("Middle East", "EMEA"), ("US – national", "Americas"),
           ("US & Canada", "Americas"), ("California", "Americas"), ("US East Coast", "Americas"), ("US South & Central", "Americas"),
           ("New York", "Americas"), ("New Jersey", "Americas"), ("Florida", "Americas"), ("Texas", "Americas"), ("Arizona", "Americas"),
           ("Worldwide", "Global"), ("Not specified", "Not specified")]
LOCATIONS = [("EMEA", "EMEA – multi-country"), ("Global EMEA", "EMEA – multi-country"), ("Western-Europe", "Western Europe – multi-country"),
             ("UK", "UK"), ("FR", "France"), ("DE", "Germany"), ("ES", "Spain"), ("IT", "Italy"), ("Middle-East", "Middle East"),
             ("SA", "Middle East"), ("US", "US – national"), ("Global US", "US – national"), ("USCA", "US & Canada"), ("NA", "US & Canada"),
             ("California", "California"), ("US-California", "California"), ("US-CA", "California"), ("US-SV", "California"),
             ("US-EastCoast", "US East Coast"), ("US-East-Coast", "US East Coast"), ("US-Middle-South", "US South & Central"),
             ("US-South-Central", "US South & Central"), ("New York", "New York"), ("New Jersey", "New Jersey"), ("Florida", "Florida"),
             ("FL", "Florida"), ("Texas", "Texas"), ("TX", "Texas"), ("Arizona", "Arizona"), ("WW", "Worldwide"), ("All", "Worldwide"),
             ("US-UK-FR-IT", "Worldwide"), ("CFA | Amazon US batch 1", "US – national"), ("YT | PSS | US | Pepsi Campaign", "US – national")]
ENDED = [("FR_Alibaba Campaign", "Run by PnP's internal team; last spend 5 Oct 2026."), ("Test 1", "ChatGPT Ads 10-day test, 23 Sep – 2 Oct 2026.")]
OTHER_ROWS = [(datetime.date(2026, 9, 23), "ChatGPT Ads", "Test 1", 229.56, 4021, 43, 0, "Yes", "Not specified",
               "Whole 10-day test (23 Sep – 2 Oct) on one row: counts in September, not in the weekly figures.")]


# ---------------------------------------------------------------- formula helpers
def xsum(X, valcol, datecol, lo, hi, *crit):
    """SUMIFS on an export tab: INDEX(sheet!A:AD,0,col) picks the column found by its header (Calc)."""
    v, d, c = f"INDEX({X},0,{valcol})", f"INDEX({X},0,{datecol})", f"INDEX({X},0,{CM_CAMP if X == MX else CG_CAMP})"
    s = f'SUMIFS({v},{d},">="&{lo},{d},"<="&{hi}'
    for k in crit:
        s += f",{c},{k}"
    return s + ")"


def meta(lo, hi, *crit):
    return xsum(MX, CM_SPEND, CM_DATE, lo, hi, *crit)


def goog(lo, hi, *crit):
    """Google cost in EUR × the rate of the month the period starts in."""
    return f"({xsum(GX, CG_COST, CG_DAY, lo, hi, *crit)})*INDEX({S_FX},MONTH({lo}))"


def other(lo, hi, channel, day=False, col="L"):
    """'Other channels' tab: A date, B channel, G clicks, H conversions, I 'total for more than a week', L spend in USD."""
    s = f'SUMIFS({OC(col)},{OC("A")},">="&{lo},{OC("A")},"<="&{hi},{OC("B")},"{channel}"'
    return s + (f',{OC("I")},"<>Yes")' if day else ")")


def flag(row):
    return f'(Settings!$C${row}="Yes")'


def month(m):
    return f"DATE({S_YEAR},{m},1)", f"EOMONTH(DATE({S_YEAR},{m},1),0)"


def USD(x):
    return f'"$"&TEXT({x},"#,##0")'


# campaign-type rules as SUMIFS criteria on the campaign name; each rule excludes the rules before it
META_EXCL = ['"<>*retargeting*"', '"<>*objective:lead*"']
G1 = ['"<>*pmax*"']
G2 = G1 + ['"<>*demandgen*"', '"<>global*"', '"<>yt |*"', '"<>*universities*"']
G3 = G2 + ['"<>*youtube*"']
G4 = G3 + ['"<>*coworking*"']
TYPE_RULES = {
    "Meta – lead ads, retargeting": [(MX, ['"*retargeting*"'])],
    "Meta – lead ads, prospecting": [(MX, ['"*objective:lead*"', '"<>*retargeting*"'])],
    "Meta – traffic": [(MX, ['"*traffic*"'] + META_EXCL), (MX, ['"*alibaba*"', '"<>*traffic*"'] + META_EXCL)],
    "Google – Performance Max": [(GX, ['"*pmax*"'])],
    "Google – Demand Gen / YouTube reach": [(GX, ['"*demandgen*"'] + G1), (GX, ['"global*"', '"<>*demandgen*"'] + G1),
                                            (GX, ['"yt |*"', '"<>*demandgen*"', '"<>global*"'] + G1),
                                            (GX, ['"*universities*"', '"<>*demandgen*"', '"<>global*"', '"<>yt |*"'] + G1)],
    "Google – YouTube video": [(GX, ['"*youtube*"'] + G2)],
    "Google – Search, brand": [(GX, ['"*brand*"', '"<>*non-brand*"'] + G3)],
    "Google – Search, coworking": [(GX, ['"*coworking*"', '"<>*brand*"'] + G3), (GX, ['"*coworking*"', '"*non-brand*"'] + G3)],
    "Google – Search, non-brand": [(GX, ['"*search*"', '"<>*brand*"'] + G4), (GX, ['"*search*"', '"*non-brand*"'] + G4)],
}


# ---------------------------------------------------------------- build
def build(out, meta_rows, google_rows, agency_weeks=(), agency_totals=(), sources=()):
    wb = Workbook()
    names = ["Dashboard", "Update", "Weekly", "Monthly", "By location", "Meta export", "Google export", "Other channels",
             "Settings", "Agency check", "Calc"]
    ws = {n: (wb.active if i == 0 else wb.create_sheet(n)) for i, n in enumerate(names)}
    ws["Dashboard"].title = "Dashboard"
    colors = {"Dashboard": NAVY, "Update": "1BAF7A", "Weekly": "2A78D6", "Monthly": "2A78D6", "By location": "2A78D6",
              "Meta export": "BF9000", "Google export": "BF9000", "Other channels": "BF9000", "Settings": "BF9000",
              "Agency check": "7F7F7F", "Calc": "7F7F7F"}
    for n, w in ws.items():
        w.sheet_properties.tabColor = colors[n]
    notes = {w["start"]: w.get("notes") for w in agency_weeks}
    settings(ws["Settings"])
    export_tab(ws["Meta export"], meta_rows, META_CAP, "Campaign name")
    export_tab(ws["Google export"], google_rows, GOOGLE_CAP, "Cost")
    other_channels(ws["Other channels"])
    calc(ws["Calc"])
    monthly(ws["Monthly"])
    weekly(ws["Weekly"], notes)
    by_location(ws["By location"])
    agency_tab(ws["Agency check"], agency_weeks, agency_totals)
    dashboard(ws["Dashboard"])
    update_tab(ws["Update"], sources)
    ws["Calc"].sheet_state = "hidden"
    wb.save(out)


# ---------------------------------------------------------------- settings
def settings(s):
    widths(s, {"A": 40, "B": 30, "C": 16, "D": 30, "E": 14, "F": 44})
    title(s, "A1", "Settings", "Yellow cells are the only ones to change. Most weeks you won't need this tab.", "A2")
    section(s, "A4", "BUDGET", "ABCDEF")
    for r, lab, v, fmt, nt in [
        (5, "Year", 2026, "0", "The budget runs 1 Jan – 31 Dec of this year."),
        (6, "Annual budget (USD)", 300000, AMT, "Confirmed by Tereza, 13 Oct 2026."),
        (7, "Maximum – ideally not more (USD)", 320000, AMT, "\"We can spend up to 320k this year, ideally not more.\" (Tereza)"),
        (8, "Original budget (USD)", 350000, AMT, "Reduced because performance wasn't good enough (Tereza)."),
    ]:
        cell(s, f"A{r}", lab, bold=True)
        cell(s, f"B{r}", v, fmt, fill=INPUT, color=BLUE_T, align="center")
        note(s, f"D{r}", nt)
    cell(s, "A9", "Budget status (shown on the Dashboard)", bold=True)
    cell(s, "B9", "Confirmed by Tereza on 13 Oct 2026: $300k for 2026 (originally $350k). We can go up to $320k, ideally not more.",
         fill=INPUT, color=BLUE_T, wrap=True)
    s.merge_cells("B9:F9"); s.row_dimensions[9].height = 30
    cell(s, "A10", "Budget period (calculated)", bold=True)
    cell(s, "B10", "=DATE(B5,1,1)", DATE_F, align="center"); cell(s, "C10", "=DATE(B5,12,31)", DATE_F, align="center")
    cell(s, "A11", "Week 1 starts on (calculated)", bold=True)
    cell(s, "B11", "=B10-WEEKDAY(B10,2)+1", DATE_F, align="center")
    note(s, "D11", "Weeks run Monday to Sunday.")
    section(s, "A13", "DATA DATE", "ABCDEF")
    cell(s, "A14", "Data up to – automatic", bold=True); cell(s, "B14", "=Calc!C52", DATE_F, align="center")
    note(s, "D14", "The last day in both exports (the earlier one if they differ).")
    cell(s, "A15", "Data up to – set by hand (normally empty)", bold=True)
    cell(s, "B15", None, DATE_F, fill=INPUT, color=BLUE_T, align="center")
    note(s, "D15", "Only to report up to an earlier day. Clear it afterwards.")
    cell(s, "A16", "Data up to – used everywhere", bold=True); cell(s, "B16", '=IF(B15<>"",B15,B14)', DATE_F, bold=True, align="center")
    section(s, "A18", "CHANNELS", "ABCDEF")
    header(s, 19, 1, ["Channel", "Billing currency", "Counts toward the budget?", "Note", "", ""]); s.merge_cells("D19:F19")
    for (name, r, cur), nt in zip(CHANNELS, ["Includes FR_Alibaba (run by PnP's internal team) – confirm it belongs in this budget.", "",
                                             "To confirm with Tereza.", "No spend in 2026."]):
        cell(s, f"A{r}", name, bold=True)
        cell(s, f"B{r}", cur, fill=INPUT, color=BLUE_T, align="center")
        cell(s, f"C{r}", "Yes", fill=INPUT, color=BLUE_T, align="center")
        cell(s, f"D{r}", nt, size=9, color=INK2, wrap=True); s.merge_cells(f"D{r}:F{r}")
    section(s, "A25", "EXCHANGE RATE – EUR TO USD (Google Ads and ChatGPT Ads bill in EUR)", "ABCDEF")
    header(s, 26, 1, ["Month", "1 EUR = ? USD", "Source", "", "", ""]); s.merge_cells("C26:F26")
    for i in range(12):
        r = 27 + i
        cell(s, f"A{r}", f"=DATE($B$5,{i + 1},1)", MON_F, bold=True)
        cell(s, f"B{r}", FX_RATE, "0.0000", fill=INPUT, color=BLUE_T, align="center")
        cell(s, f"C{r}", FX_SOURCE if i == 0 else "Same as above", size=8, color=INK2, fill=INPUT); s.merge_cells(f"C{r}:F{r}")
    cell(s, "A39", "Average", bold=True, fill=TOTAL); cell(s, "B39", "=AVERAGE(B27:B38)", "0.0000", bold=True, fill=TOTAL, align="center")
    section(s, "A41", "ENDED CAMPAIGNS – left out of the current pace and the forecast", "ABCDEF")
    note(s, "A42", "When a campaign stops for good, type its name here exactly as in the export. Its spend still counts in 'spent so far'.")
    header(s, 43, 1, ["Campaign name (exactly as in the export)", "Found in the exports?", "Spent in the last 3 full weeks (USD)", "Note", "", ""])
    s.merge_cells("D43:F43")
    for k in range(ENDED_N):
        r = ENDED_FIRST + k
        nm, nt = ENDED[k] if k < len(ENDED) else (None, None)
        cell(s, f"A{r}", nm, fill=INPUT, color=BLUE_T)
        cell(s, f"B{r}", f"=Calc!C{EN_FIRST + k}", align="center")
        cell(s, f"C{r}", f"=Calc!D{EN_FIRST + k}", AMT)
        cell(s, f"D{r}", nt, size=9, fill=INPUT, color=BLUE_T, wrap=True); s.merge_cells(f"D{r}:F{r}")
    s.conditional_formatting.add(f"B{ENDED_FIRST}:B{ENDED_FIRST + ENDED_N - 1}", FormulaRule(formula=[f'B{ENDED_FIRST}="No"'], font=font(bold=True, color=RED)))
    section(s, "A55", "LOCATIONS – how campaign names map to markets and regions", "ABCDEF")
    note(s, "A56", "The tracker reads the location code at the start of each campaign name: 'Geo:XX_…', 'PNP_XX_…', 'XX_…' or 'XX | …'. Capital letters don't matter.")
    note(s, "A57", "New code → add it on the left with its market. No code in the name → type the full campaign name instead. New market → add it on the right with its region.")
    header(s, 58, 1, ["Code, or full campaign name", "Market"]); header(s, 58, 4, ["Market", "Region"])
    for k in range(LOC_N):
        r = LOC_FIRST + k
        key, mk = LOCATIONS[k] if k < len(LOCATIONS) else (None, None)
        cell(s, f"A{r}", key, fill=INPUT, color=BLUE_T); cell(s, f"B{r}", mk, fill=INPUT, color=BLUE_T)
    for k in range(MKT_N):
        r = MKT_FIRST + k
        mk, rg = MARKETS[k] if k < len(MARKETS) else (None, None)
        cell(s, f"D{r}", mk, fill=INPUT, color=BLUE_T); cell(s, f"E{r}", rg, fill=INPUT, color=BLUE_T, align="center")
    note(s, f"D{MKT_FIRST + len(MARKETS)}", "Germany (DE) and Spain (ES) are ready for future campaigns.")
    tr = LOC_FIRST + LOC_N + 2
    section(s, f"A{tr}", "CAMPAIGN TYPES – read from the campaign name (first rule that matches)", "ABCDEF")
    for i, t in enumerate([
        "Meta: 'retargeting' → lead ads, retargeting · 'Objective:lead' → lead ads, prospecting · 'traffic' or 'Alibaba' → traffic · anything else → other.",
        "Google Ads: 'PMax' → Performance Max · 'DemandGen', 'Universities', or a name starting 'Global' or 'YT |' → Demand Gen / YouTube reach · "
        "'YouTube' → YouTube video · 'Brand' (not 'Non-brand') → Search, brand · 'Coworking' → Search, coworking · 'Search' → Search, non-brand · else → other."]):
        cell(s, f"A{tr + 1 + i}", t, size=9, color=INK2, border=False, wrap=True); s.merge_cells(f"A{tr + 1 + i}:F{tr + 1 + i}")
        s.row_dimensions[tr + 1 + i].height = 26
    dv = DataValidation(type="list", formula1='"USD,EUR"', allow_blank=False); s.add_data_validation(dv); dv.add("B20:B23")
    dv2 = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False); s.add_data_validation(dv2); dv2.add("C20:C23")
    dv3 = DataValidation(type="list", formula1=f"$D${MKT_FIRST}:$D${MKT_FIRST + MKT_N - 1}", allow_blank=True)
    s.add_data_validation(dv3); dv3.add(f"B{LOC_FIRST}:B{LOC_FIRST + LOC_N - 1}")
    dv4 = DataValidation(type="list", formula1='"' + ",".join(REGIONS) + '"', allow_blank=True)
    s.add_data_validation(dv4); dv4.add(f"E{MKT_FIRST}:E{MKT_FIRST + MKT_N - 1}")
    s.freeze_panes = "A4"


# ---------------------------------------------------------------- export tabs
def export_tab(w, rows, cap, key):
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            if v is None:
                continue
            c = w.cell(i + 1, j + 1, v)
            if isinstance(v, datetime.date):
                c.number_format = "yyyy-mm-dd"
    hdr = next(i for i, r in enumerate(rows) if key in r) + 1
    for j in range(1, len(rows[hdr - 1]) + 1):
        c = w.cell(hdr, j)
        c.font = Font(name="Arial", size=10, bold=True)
        c.fill = PatternFill("solid", fgColor=INPUT)
        c.alignment = Alignment(wrap_text=True, vertical="center")
        w.column_dimensions[L(j)].width = 14
    w.column_dimensions[L(rows[hdr - 1].index("Campaign name" if key == "Campaign name" else "Campaign") + 1)].width = 52
    w.row_dimensions[hdr].height = 30
    w.freeze_panes = f"A{hdr + 1}"
    w.cell(cap + 2000, 1).fill = PatternFill("solid", fgColor=WHITE)


def other_channels(o):
    title(o, "A1", "Other channels – ChatGPT Ads and LinkedIn Ads (typed by hand)",
          "Only when these channels run. One row per campaign per day, or per week (date = the Monday). Spend as billed – the tracker converts EUR to USD.", "A2")
    note(o, "A3", "'Total for more than a week?' = Yes marks a row covering a longer period (like the ChatGPT test): it counts in its month, not in the weekly figures.")
    header(o, 4, 1, ["Date", "Channel", "Campaign name", "Spend (as billed)", "Currency (auto)", "Impressions", "Clicks", "Conversions",
                     "Total for more than a week?", "Market", "Note", "Spend in USD (auto)"], height=42)
    for k in range(OC_N):
        r = OC_FIRST + k
        d, chn, camp, sp, imp, clk, conv, tot, mk, nt = OTHER_ROWS[k] if k < len(OTHER_ROWS) else (None,) * 10
        cell(o, f"A{r}", d, DATE_F, fill=INPUT, color=BLUE_T, align="center")
        cell(o, f"B{r}", chn, fill=INPUT, color=BLUE_T)
        cell(o, f"C{r}", camp, fill=INPUT, color=BLUE_T)
        cell(o, f"D{r}", sp, AMT2, fill=INPUT, color=BLUE_T)
        cell(o, f"E{r}", f'=IF(B{r}="","",IFERROR(VLOOKUP(B{r},Settings!$A$20:$B$23,2,0),"?"))', align="center", size=9)
        cell(o, f"F{r}", imp, "#,##0", fill=INPUT, color=BLUE_T)
        cell(o, f"G{r}", clk, "#,##0", fill=INPUT, color=BLUE_T)
        cell(o, f"H{r}", conv, "#,##0", fill=INPUT, color=BLUE_T)
        cell(o, f"I{r}", tot, fill=INPUT, color=BLUE_T, align="center")
        cell(o, f"J{r}", mk, fill=INPUT, color=BLUE_T)
        cell(o, f"K{r}", nt, size=8, fill=INPUT, color=BLUE_T, wrap=True)
        cell(o, f"L{r}", f'=IF(OR(A{r}="",D{r}=""),0,D{r}*IF(E{r}="USD",1,INDEX({S_FX},MONTH(A{r}))))', AMT2)
        if nt:
            o.row_dimensions[r].height = 30
    last = OC_FIRST + OC_N - 1
    for col, lst in (("B", '"ChatGPT Ads,LinkedIn Ads"'), ("I", '"Yes"'), ("J", f"Settings!$D${MKT_FIRST}:$D${MKT_FIRST + MKT_N - 1}")):
        dv = DataValidation(type="list", formula1=lst, allow_blank=True); o.add_data_validation(dv); dv.add(f"{col}{OC_FIRST}:{col}{last}")
    o.freeze_panes = f"A{OC_FIRST}"
    widths(o, {"A": 13, "B": 14, "C": 34, "D": 14, "E": 12, "F": 12, "G": 10, "H": 12, "I": 14, "J": 22, "K": 50, "L": 14})


# ---------------------------------------------------------------- calc
def calc(k):
    title(k, "A1", "Calculations behind every tab – hidden, don't edit", None)
    for r, lab, f, fmt in [
        (3, "Data up to", f"={S_UPTO}", DATE_F), (4, "Budget period starts", f"={S_PSTART}", DATE_F), (5, "Budget period ends", f"={S_PEND}", DATE_F),
        (6, "Days in budget period", "=C5-C4+1", "0"), (7, "Days gone (up to the data date)", "=MAX(0,MIN(C3,C5)-C4+1)", "0"),
        (8, "Days left", "=MAX(0,C5-MAX(C3,C4-1))", "0"), (9, "Share of the period gone", "=IF(C6>0,C7/C6,0)", "0.0%"),
        (10, "Last full month ends", "=IF(C3=EOMONTH(C3,0),C3,EOMONTH(C3,-1))", DATE_F), (11, "Last full month starts", "=EOMONTH(C10,-1)+1", DATE_F),
        (12, "Last 3 full months start", "=EOMONTH(C10,-3)+1", DATE_F), (13, "Last full week ends (Sunday)", "=C3-MOD(WEEKDAY(C3,2),7)", DATE_F),
        (14, "Last full week starts (Monday)", "=C13-6", DATE_F), (15, "Last 3 full weeks start", "=C13-20", DATE_F),
        (16, "Weeks left", "=C8/7", "0.00"), (17, "Days in last full month", "=C10-C11+1", "0")]:
        cell(k, f"B{r}", lab); cell(k, f"C{r}", f, fmt, align="center")
    header(k, 19, 2, ["Channel", "Counts toward budget?", "Spent to date", "Last full month", "Last 3 full months", "Last full week", "Last 3 full weeks", "Share"])
    mon = lambda col, lo, hi: f'SUMIFS(Monthly!${col}${M_FIRST}:${col}${M_FIRST + 11},Monthly!$A${M_FIRST}:$A${M_FIRST + 11},">="&{lo},Monthly!$A${M_FIRST}:$A${M_FIRST + 11},"<="&{hi})'
    weekf = {"Meta": lambda lo, hi: meta(lo, hi), "Google Ads": lambda lo, hi: goog(lo, hi),
             "ChatGPT Ads": lambda lo, hi: other(lo, hi, "ChatGPT Ads", True), "LinkedIn Ads": lambda lo, hi: other(lo, hi, "LinkedIn Ads", True)}
    for i, (name, srow, cur) in enumerate(CHANNELS):
        r, mc = 20 + i, "BCDE"[i]   # month figures come from the Monthly tab (each month at its own rate)
        cell(k, f"B{r}", name, bold=True); cell(k, f"C{r}", f"=Settings!C{srow}", align="center")
        cell(k, f"D{r}", "=" + mon(mc, "$C$4", "$C$5"), AMT)
        cell(k, f"E{r}", "=" + mon(mc, "$C$11", "$C$10"), AMT)
        cell(k, f"F{r}", "=" + mon(mc, "$C$12", "$C$10"), AMT)
        cell(k, f"G{r}", f"=({weekf[name]('$C$14', '$C$13')})*{flag(srow)}", AMT)
        cell(k, f"H{r}", f"=({weekf[name]('$C$15', '$C$13')})*{flag(srow)}", AMT)
        cell(k, f"I{r}", f'=IF($D$25=0,"",D{r}/$D$25)', "0.0%")
    cell(k, "B24", "Total – counts toward budget", bold=True, fill=TOTAL); cell(k, "B25", "Total – all channels", bold=True, fill=TOTAL)
    for col in "DEFGH":
        cell(k, f"{col}24", f"=SUM({col}20:{col}23)", AMT, bold=True, fill=TOTAL)
        cell(k, f"{col}25", f"=SUM({col}20:{col}23)", AMT, bold=True, fill=TOTAL)
    for r, lab, f, fmt in [
        (27, "Budget", f"={S_BUDGET}", AMT), (28, "Maximum (ideally not more)", f"={S_MAX}", AMT), (29, "Original budget", f"={S_ORIG}", AMT),
        (30, "Spent to date (budget channels)", "=D24", AMT), (31, "Left in the budget", "=C27-C30", AMT), (32, "Left up to the maximum", "=C28-C30", AMT),
        (33, "% of budget used", '=IF(C27=0,"",C30/C27)', "0.0%"), (34, "% of maximum used", '=IF(C28=0,"",C30/C28)', "0.0%"),
        (35, "Should have spent by now (budget spread evenly by day)", "=C27*C9", AMT), (36, "Ahead (+) / behind (−) that even pace", "=C30-C35", AMT),
        (37, "Weekly pace – last 3 full weeks, without ended campaigns", "=(H24-C49)/3", AMT), (38, "Spent in the last 3 full weeks, all campaigns", "=H24", AMT),
        (39, "Current weekly pace used", "=C37", AMT),
        (40, "Source of the current pace", '="last 3 full weeks ("&TEXT(C15,"d mmm")&" – "&TEXT(C13,"d mmm")&"), campaigns still running"', None),
        (41, "Ended campaigns on the Settings list", f'=COUNTIF(Settings!$A${ENDED_FIRST}:$A${ENDED_FIRST + ENDED_N - 1},"?*")', "0"),
        (42, "Forecast year-end at the current pace", "=C30+C39*C16", AMT), (43, "Allowed per week to land on the budget", "=IF(C16<=0,0,C31/C16)", AMT),
        (44, "Allowed per week to land on the maximum", "=IF(C16<=0,0,C32/C16)", AMT), (45, "Last full month (budget channels)", "=E24", AMT),
        (46, "All spend in the exports (any date)", f"=SUM(INDEX({MX},0,{CM_SPEND}))+SUM(INDEX({GX},0,{CG_COST}))*{S_FXAVG}+SUM({OC('L')})", AMT),
        (47, "Forecast year-end at last month's pace", "=C30+E24/C17*C8", AMT), (48, "Last full week (budget channels)", "=G24", AMT),
        (49, "Left out of the pace: ended campaigns, last 3 full weeks", f"=SUM(D{EN_FIRST}:D{EN_FIRST + ENDED_N - 1})", AMT)]:
        cell(k, f"B{r}", lab); cell(k, f"C{r}", f, fmt)
    section(k, "B51", "EXPORTS", "BCDE")
    md, gd = f"INDEX({MX},0,{CM_DATE})", f"INDEX({GX},0,{CG_DAY})"
    for r, lab, f, fmt in [
        (52, "Data up to – automatic", "=IF(AND(C53>0,C54>0),MIN(C53,C54),MAX(C53,C54))", DATE_F),
        (53, "Meta – last day in the export", f"=IF(C65={NF},0,MAX({md}))", DATE_F), (54, "Google Ads – last day in the export", f"=IF(C78={NF},0,MAX({gd}))", DATE_F),
        (55, "Meta – first day", f"=IF(C65={NF},0,MIN({md}))", DATE_F), (56, "Google Ads – first day", f"=IF(C78={NF},0,MIN({gd}))", DATE_F),
        (57, "Meta – rows read", f"=IF(C65={NF},0,COUNT({md}))", "#,##0"), (58, "Google Ads – rows read", f"=IF(C78={NF},0,COUNT({gd}))", "#,##0"),
        (59, f"Meta – filled cells below row {META_CAP}", f"=COUNTA('Meta export'!$A${META_CAP + 1}:$AD${META_CAP + 3000})", "0"),
        (60, f"Google – filled cells below row {GOOGLE_CAP}", f"=COUNTA('Google export'!$A${GOOGLE_CAP + 1}:$AD${GOOGLE_CAP + 3000})", "0"),
        (61, "Last Sunday (from today)", "=TODAY()-WEEKDAY(TODAY(),2)", DATE_F)]:
        cell(k, f"B{r}", lab); cell(k, f"C{r}", f, fmt, align="center")

    def first_row_with(tab, text):
        f = "0"
        for rr in range(5, 0, -1):
            f = f"IF(COUNTIF('{tab}'!$A${rr}:$AD${rr},\"{text}\")>0,{rr},{f})"
        return "=" + f

    def find(tab, hdr_cell, *names):
        rng_ = f"INDEX('{tab}'!$A$1:$AD$5,{hdr_cell},0)"
        f = str(NF)
        for nm in reversed(names):
            f = f'IFERROR(MATCH("{nm}",{rng_},0),{f})'
        return "=" + f

    section(k, "B63", "META EXPORT – COLUMNS FOUND (30 = not found)", "BCDE")
    for r, lab, f in [
        (64, "Header row", first_row_with("Meta export", "Campaign name")), (65, "Reporting starts", find("Meta export", "$C$64", "Reporting starts")),
        (66, "Reporting ends", find("Meta export", "$C$64", "Reporting ends")), (67, "Campaign name", find("Meta export", "$C$64", "Campaign name")),
        (68, "Amount spent", find("Meta export", "$C$64", "Amount spent (USD)", "Amount spent (EUR)", "Amount spent")),
        (69, "Clicks", find("Meta export", "$C$64", "Unique link clicks", "Link clicks")),
        (70, "Conversions", find("Meta export", "$C$64", "Website registrations completed")),
        (71, "Spend header", f"=IF(OR(C64=0,C68={NF}),\"\",INDEX('Meta export'!$A$1:$AD$5,C64,C68)&\"\")"),
        (72, "Currency in the spend header", '=IFERROR(MID(C71,FIND("(",C71)+1,3),"")'),
        (73, "Split by day?", f"=IF(OR(C66={NF},C57=0),TRUE,INDEX({MX},C64+1,C65)=INDEX({MX},C64+1,C66))")]:
        cell(k, f"B{r}", lab); cell(k, f"C{r}", f, align="center")
    section(k, "B75", "GOOGLE ADS EXPORT – COLUMNS FOUND (30 = not found)", "BCDE")
    for r, lab, f in [
        (76, "Header row", first_row_with("Google export", "Cost")), (77, "Campaign", find("Google export", "$C$76", "Campaign")),
        (78, "Day", find("Google export", "$C$76", "Day")), (79, "Cost", find("Google export", "$C$76", "Cost")),
        (80, "Clicks", find("Google export", "$C$76", "Clicks")), (81, "Conversions", find("Google export", "$C$76", "Conversions")),
        (82, "Currency code", find("Google export", "$C$76", "Currency code")),
        (83, "Currency (first data row)", f'=IF(OR(C76=0,C82={NF},C58=0),"",INDEX({GX},C76+1,C82)&"")')]:
        cell(k, f"B{r}", lab); cell(k, f"C{r}", f, align="center")

    section(k, "B85", "CHECKS", "BCDE")
    unassigned = f"SUM(Monthly!$F${M_FIRST}:$F${M_FIRST + 11})-SUM($P${MK0}:$P${MK0 + MKT_N - 1})"
    checks = [
        ("Meta export",
         f'=IF(OR(C65={NF},C67={NF},C68={NF}),"⚠ Columns missing: "&IF(C65={NF},"Reporting starts · ","")&IF(C67={NF},"Campaign name · ","")&IF(C68={NF},"Amount spent",""),'
         f'IF(C57=0,"⚠ No dates found – were they imported as text?",IF(NOT(C73),"⚠ Not split by day",IF(C72<>Settings!$B$20,"⚠ Spend is in "&C72&", Settings says "&Settings!$B$20,'
         f'"✓ "&TEXT(C57,"#,##0")&" rows · "&TEXT(C55,"d mmm")&" – "&TEXT(C53,"d mmm")))))'),
        ("Google Ads export",
         f'=IF(OR(C77={NF},C78={NF},C79={NF}),"⚠ Columns missing: "&IF(C77={NF},"Campaign · ","")&IF(C78={NF},"Day · ","")&IF(C79={NF},"Cost",""),'
         f'IF(C58=0,"⚠ No dates found – were they imported as text?",IF(AND(C82<>{NF},C83<>Settings!$B$21),"⚠ Cost is in "&C83&", Settings says "&Settings!$B$21,'
         f'"✓ "&TEXT(C58,"#,##0")&" rows · "&TEXT(C56,"d mmm")&" – "&TEXT(C54,"d mmm"))))'),
        ("Data is up to date",
         '=IF(OR(C53=0,C54=0),"⚠ One export is empty",IF(C53<>C54,"⚠ Meta ends "&TEXT(C53,"d mmm")&", Google Ads "&TEXT(C54,"d mmm")&" – export both to the same day",'
         'IF(C3>=C61,"✓ Data runs to "&TEXT(C3,"ddd d mmm")&" – includes last week","⚠ Data ends "&TEXT(C3,"d mmm")&" – last Sunday was "&TEXT(C61,"d mmm"))))'),
        ("Every campaign has a market",
         f'=IF(ABS({unassigned})<1,"✓ All campaigns matched to a market","⚠ "&{USD(unassigned)}&" of spend has a location code that isn\'t on Settings → Locations")'),
        ("Exports fit in the tracker",
         f'=IF(C59+C60=0,"✓ Meta "&TEXT(C57,"#,##0")&" of {META_CAP:,} rows · Google "&TEXT(C58,"#,##0")&" of {GOOGLE_CAP:,}","⚠ An export is longer than the tracker reads")'),
        ("Ended campaigns",
         f'=IF(COUNTIF(C{EN_FIRST}:C{EN_FIRST + ENDED_N - 1},"No")=0,"✓ "&C41&" on the list, all found in the exports","⚠ "&COUNTIF(C{EN_FIRST}:C{EN_FIRST + ENDED_N - 1},"No")&" name(s) not found – check the spelling on Settings")'),
    ]
    for i, (lab, f) in enumerate(checks):
        cell(k, f"B{CK_FIRST + i}", lab); cell(k, f"C{CK_FIRST + i}", f)
    cell(k, "B93", "Checks with ⚠", bold=True); cell(k, "C93", f'=COUNTIF(C{CK_FIRST}:C{CK_FIRST + CK_N - 1},"⚠*")', "0", bold=True)
    section(k, "B95", "ENDED CAMPAIGNS", "BCDE")
    for i in range(ENDED_N):
        r, nm = EN_FIRST + i, f"Settings!$A${ENDED_FIRST + i}"
        cell(k, f"B{r}", f'=IF({nm}="","",{nm}&"")')
        cell(k, f"C{r}", f'=IF(B{r}="","",IF(COUNTIF(INDEX({MX},0,{CM_CAMP}),B{r})+COUNTIF(INDEX({GX},0,{CG_CAMP}),B{r})+COUNTIF({OC("C")},B{r})>0,"Yes","No"))', align="center")
        cell(k, f"D{r}", f'=IF(B{r}="",0,{meta("$C$15", "$C$13", f"B{r}")}+{goog("$C$15", "$C$13", f"B{r}")}'
                         f'+SUMIFS({OC("L")},{OC("C")},B{r},{OC("A")},">="&$C$15,{OC("A")},"<="&$C$13,{OC("I")},"<>Yes"))', AMT)

    section(k, f"B{CODE0 - 2}", "LOCATION CODES – USD BY MONTH (5 name patterns × 2 exports)", "BCDEFGHIJKLMNOP")
    header(k, CODE0 - 1, 2, ["Code", "Market"] + [f'=TEXT(DATE({S_YEAR},{m},1),"mmm")' for m in range(1, 13)] + ["Year"])
    for i in range(LOC_N):
        r = CODE0 + i
        cell(k, f"B{r}", f'=Settings!$A${LOC_FIRST + i}&""'); cell(k, f"C{r}", f'=Settings!$B${LOC_FIRST + i}&""')
        pats = [f"$B{r}", f'"Geo:"&$B{r}&"_*"', f'$B{r}&"_*"', f'"PNP_"&$B{r}&"_*"', f'$B{r}&" | *"']
        for m in range(1, 13):
            lo, hi = month(m)
            f = "+".join(meta(lo, hi, p) for p in pats) + "+(" + "+".join(xsum(GX, CG_COST, CG_DAY, lo, hi, p) for p in pats) + f")*INDEX({S_FX},{m})"
            cell(k, f"{L(3 + m)}{r}", f'=IF($B{r}="",0,{f})', AMT)
        cell(k, f"P{r}", f"=SUM(D{r}:O{r})", AMT)

    def matrix(top, n, name_f, region_f, val_f, lab):
        section(k, f"B{top - 2}", lab, "BCDEFGHIJKLMNOPQR")
        header(k, top - 1, 2, ["Name", "Region"] + [f'=TEXT(DATE({S_YEAR},{m},1),"mmm")' for m in range(1, 13)] + ["Year", "Sort key", "Sorted by spend"])
        for i in range(n):
            r = top + i
            cell(k, f"B{r}", name_f(i)); cell(k, f"C{r}", region_f(i, r))
            for m in range(1, 13):
                cell(k, f"{L(3 + m)}{r}", f'=IF($B{r}="",0,{val_f(r, m)})', AMT)
            cell(k, f"P{r}", f"=SUM(D{r}:O{r})", AMT)
            cell(k, f"Q{r}", f"=IF(P{r}>0,P{r}+(1000-ROW())/1000000,0)", "0.000000")
            big = f"LARGE($Q${top}:$Q${top + n - 1},{i + 1})"
            cell(k, f"R{r}", f'=IF({big}<=0,"",INDEX($B${top}:$B${top + n - 1},MATCH({big},$Q${top}:$Q${top + n - 1},0)))')

    codes = lambda m: f"Calc!${L(3 + m)}${CODE0}:${L(3 + m)}${CODE0 + LOC_N - 1}"
    matrix(MK0, MKT_N, lambda i: f'=Settings!$D${MKT_FIRST + i}&""', lambda i, r: f'=IF(B{r}="","",Settings!$E${MKT_FIRST + i}&"")',
           lambda r, m: f'SUMIFS({codes(m)},Calc!$C${CODE0}:$C${CODE0 + LOC_N - 1},$B{r})+SUMIFS({OC("L")},{OC("J")},$B{r},{OC("A")},">="&{month(m)[0]},{OC("A")},"<="&{month(m)[1]})',
           "MARKETS – USD BY MONTH")

    def type_f(r, m):
        t = TYPES[r - TY0]
        lo, hi = month(m)
        if t in TYPE_RULES:
            parts = []
            for X, crit in TYPE_RULES[t]:
                s = xsum(X, CM_SPEND if X == MX else CG_COST, CM_DATE if X == MX else CG_DAY, lo, hi, *crit)
                parts.append(s if X == MX else f"({s})*INDEX({S_FX},{m})")
            return "+".join(parts)
        col = L(3 + m)
        if t == "Meta – other":
            return f"Monthly!$Q${M_FIRST - 1 + m}-SUM({col}{TY0}:{col}{TY0 + 2})"
        if t == "Google – other":
            return f"Monthly!$R${M_FIRST - 1 + m}*INDEX({S_FX},{m})-SUM({col}{TY0 + 4}:{col}{TY0 + 9})"
        return other(lo, hi, t)

    matrix(TY0, len(TYPES), lambda i: TYPES[i], lambda i, r: None, type_f, "CAMPAIGN TYPES – USD BY MONTH")
    widths(k, {"A": 2, "B": 52, "C": 20, **{L(4 + i): 11 for i in range(12)}, "P": 12, "Q": 14, "R": 34})


# ---------------------------------------------------------------- monthly
def monthly(m):
    title(m, "A1", "Monthly spend", None)
    cell(m, "A2", f'="USD · Google Ads and ChatGPT Ads converted from EUR with the Settings rates · data up to "&TEXT({S_UPTO},"d mmm yyyy")',
         size=9, color=INK2, border=False, italic=True)
    cell(m, "S2", "Data up to:", size=8, color=MUTED, border=False, align="right"); cell(m, "T2", f"={S_UPTO}", DATE_F, size=8, color=MUTED, border=False)
    hdr = ["Month", "Meta", "Google Ads", "ChatGPT Ads", "LinkedIn Ads", "Total", "Plan (budget spread evenly)", "Over (+) / under (−) plan",
           "Spent so far (cumulative)", "Plan so far", "% of budget used", "Budget used so far", "Status", "Quarter",
           "", "", "Meta as billed (USD)", "Google as billed (EUR)", "EUR → USD rate", "Label"]
    header(m, M_FIRST - 1, 1, hdr, height=42)
    for col in "OP":
        m[f"{col}{M_FIRST - 1}"].fill = PatternFill(fill_type=None)
    f0 = M_FIRST
    for i in range(12):
        r = f0 + i
        lo, hi = f"$A{r}", f"EOMONTH($A{r},0)"
        cell(m, f"A{r}", f"=DATE({S_YEAR},{i + 1},1)", MON_F, bold=True)
        cell(m, f"B{r}", f"={meta(lo, hi)}*{flag(20)}", AMT)
        cell(m, f"C{r}", f"={goog(lo, hi)}*{flag(21)}", AMT)
        cell(m, f"D{r}", f"={other(lo, hi, 'ChatGPT Ads')}*{flag(22)}", AMT)
        cell(m, f"E{r}", f"={other(lo, hi, 'LinkedIn Ads')}*{flag(23)}", AMT)
        cell(m, f"F{r}", f"=SUM(B{r}:E{r})", AMT, bold=True)
        cell(m, f"G{r}", f"={S_BUDGET}*MAX(0,MIN(EOMONTH($A{r},0),{S_PEND})-MAX($A{r},{S_PSTART})+1)/({S_PEND}-{S_PSTART}+1)", AMT)
        cell(m, f"H{r}", f'=IF(EOMONTH($A{r},0)>{S_UPTO},"",F{r}-G{r})', AMT)
        cell(m, f"I{r}", f'=IF($A{r}>{S_UPTO},"",SUM($F${f0}:F{r}))', AMT, bold=True)
        cell(m, f"J{r}", f"=SUM($G${f0}:G{r})", AMT)
        cell(m, f"K{r}", f'=IF(OR(I{r}="",{S_BUDGET}=0),"",I{r}/{S_BUDGET})', PCT, align="center")
        cell(m, f"L{r}", f'=IF(K{r}="","",REPT("█",ROUND(MIN(K{r},1.2)*25,0))&REPT("░",MAX(0,25-ROUND(K{r}*25,0))))', size=8, color=NAVY)
        cell(m, f"M{r}", f'=IF(EOMONTH($A{r},0)<={S_UPTO},"Complete",IF($A{r}<={S_UPTO},"In progress","Not started"))', align="center", size=9)
        cell(m, f"N{r}", f'="Q"&ROUNDUP(MONTH(A{r})/3,0)', align="center")
        cell(m, f"Q{r}", "=" + meta(lo, hi), AMT)
        cell(m, f"R{r}", "=" + xsum(GX, CG_COST, CG_DAY, lo, hi), AMT)
        cell(m, f"S{r}", f"=INDEX({S_FX},MONTH(A{r}))", "0.0000", align="center", size=9)
        cell(m, f"T{r}", f'=TEXT(A{r},"mmm")', size=8, color=MUTED, align="center")
    tr = f0 + 12
    cell(m, f"A{tr}", "Total", bold=True, fill=TOTAL)
    for col in "BCDEFGHQR":
        cell(m, f"{col}{tr}", f"=SUM({col}{f0}:{col}{tr - 1})", AMT, bold=True, fill=TOTAL)
    for col in "IJKLMNST":
        cell(m, f"{col}{tr}", "", fill=TOTAL)
    note(m, f"A{tr + 1}", "Plan = the annual budget spread evenly over the days of the year. Over/under plan is shown for complete months. "
                          "Bars = % of the annual budget used so far. 'As billed' = the figures to check against the invoices.")
    m.conditional_formatting.add(f"H{f0}:H{tr}", FormulaRule(formula=[f'AND(ISNUMBER(H{f0}),H{f0}>0)'], font=font(bold=True, color=RED)))
    m.conditional_formatting.add(f"L{f0}:L{tr - 1}", FormulaRule(formula=[f'AND(ISNUMBER(K{f0}),K{f0}>=1)'], font=font(8, False, RED)))
    m.conditional_formatting.add(f"A{f0}:T{tr - 1}", FormulaRule(formula=[f'$A{f0}>$T$2'], font=font(color=MUTED)))

    top = 38
    section(m, f"A{top}", "CLICKS, CONVERSIONS AND COSTS – as reported by each platform", "ABCDEFGHIJKLM")
    groups = [("Meta", "B", lambda lo, hi: xsum(MX, CM_CLK, CM_DATE, lo, hi), lambda lo, hi: xsum(MX, CM_CONV, CM_DATE, lo, hi)),
              ("Google Ads", "C", lambda lo, hi: xsum(GX, CG_CLK, CG_DAY, lo, hi), lambda lo, hi: xsum(GX, CG_CONV, CG_DAY, lo, hi)),
              ("ChatGPT Ads", "D", lambda lo, hi: other(lo, hi, "ChatGPT Ads", col="G"), lambda lo, hi: other(lo, hi, "ChatGPT Ads", col="H"))]
    cell(m, f"A{top + 1}", "", fill=NAVY); cell(m, f"A{top + 2}", "Month", bold=True, color=WHITE, fill=NAVY, align="center")
    for g, (name, scol, fclk, fconv) in enumerate(groups):
        c0 = 2 + g * 4
        m.merge_cells(start_row=top + 1, start_column=c0, end_row=top + 1, end_column=c0 + 3)
        cell(m, f"{L(c0)}{top + 1}", name, bold=True, color=WHITE, fill=NAVY, align="center")
        header(m, top + 2, c0, ["Clicks", "Conversions", "Cost per click", "Cost per conversion"])
    for i in range(12):
        r, src = top + 3 + i, f0 + i
        lo, hi = f"$A{src}", f"EOMONTH($A{src},0)"
        cell(m, f"A{r}", f"=A{src}", MON_F, bold=True)
        for g, (name, scol, fclk, fconv) in enumerate(groups):
            c0 = 2 + g * 4
            cl, cv, cpc, cpl = L(c0), L(c0 + 1), L(c0 + 2), L(c0 + 3)
            cell(m, f"{cl}{r}", "=" + fclk(lo, hi), "#,##0")
            cell(m, f"{cv}{r}", "=" + fconv(lo, hi), "#,##0")
            cell(m, f"{cpc}{r}", f'=IF({cl}{r}=0,"",{scol}{src}/{cl}{r})', AMT2)
            cell(m, f"{cpl}{r}", f'=IF({cv}{r}=0,"",{scol}{src}/{cv}{r})', AMT2)
    rt = top + 15
    cell(m, f"A{rt}", "Total", bold=True, fill=TOTAL)
    for g, (name, scol, *_) in enumerate(groups):
        c0 = 2 + g * 4
        cl, cv, cpc, cpl = L(c0), L(c0 + 1), L(c0 + 2), L(c0 + 3)
        cell(m, f"{cl}{rt}", f"=SUM({cl}{top + 3}:{cl}{rt - 1})", "#,##0", bold=True, fill=TOTAL)
        cell(m, f"{cv}{rt}", f"=SUM({cv}{top + 3}:{cv}{rt - 1})", "#,##0", bold=True, fill=TOTAL)
        cell(m, f"{cpc}{rt}", f'=IF({cl}{rt}=0,"",{scol}{tr}/{cl}{rt})', AMT2, bold=True, fill=TOTAL)
        cell(m, f"{cpl}{rt}", f'=IF({cv}{rt}=0,"",{scol}{tr}/{cv}{rt})', AMT2, bold=True, fill=TOTAL)
    note(m, f"A{rt + 1}", "Conversions use each platform's own definition: Meta = 'Website registrations completed' (clicks = unique link clicks); "
                          "Google Ads = 'Conversions' (its primary conversion actions, which the agency changed during the year). Compare each channel with itself.")
    m.conditional_formatting.add(f"A{top + 3}:M{rt - 1}", FormulaRule(formula=[f'$A{top + 3}>$T$2'], font=font(color=MUTED)))
    m.freeze_panes = f"A{f0}"
    widths(m, {"A": 11, **{c: 12 for c in "BCDEFGHIJK"}, "L": 24, "M": 11, "N": 8, "O": 2, "P": 2, "Q": 13, "R": 13, "S": 10, "T": 6})
    section(m, "A20", "SPEND BY MONTH AND CHANNEL", "ABCDEFG"); section(m, "I20", "SPENT SO FAR vs. PLAN", "IJKLMN")
    bar = BarChart(); bar.type = "col"; bar.grouping = "stacked"; bar.overlap = 100; bar.gapWidth = 60
    for j in range(4):
        bar.add_data(Reference(m, min_col=2 + j, min_row=f0 - 1, max_row=f0 + 11), titles_from_data=True)
    bar.set_categories(Reference(m, min_col=20, min_row=f0, max_row=f0 + 11))
    style_bar(bar, [CH_COLORS[n] for n, *_ in CHANNELS])
    bar.width, bar.height = 18, 7.6
    m.add_chart(bar, "A21")
    cum = BarChart(); cum.type = "col"; cum.grouping = "clustered"; cum.gapWidth = 60
    cum.add_data(Reference(m, min_col=9, min_row=f0 - 1, max_row=f0 + 11), titles_from_data=True)
    cum.add_data(Reference(m, min_col=10, min_row=f0 - 1, max_row=f0 + 11), titles_from_data=True)
    cum.set_categories(Reference(m, min_col=20, min_row=f0, max_row=f0 + 11))
    style_bar(cum, [NAVY, "C9D1DC"])
    cum.width, cum.height = 16, 7.6
    m.add_chart(cum, "I21")


# ---------------------------------------------------------------- weekly
def weekly(w, notes):
    title(w, "A1", "Weekly spend", None)
    cell(w, "A2", '="Weeks run Monday to Sunday · USD · from the platform exports · green row = the last full week · yellow = typed by you"',
         size=9, color=INK2, border=False, italic=True)
    cell(w, "A3", "Data up to:", size=8, color=MUTED, border=False); cell(w, "C3", f"={S_UPTO}", DATE_F, size=8, color=MUTED, border=False)
    cell(w, "D3", "Last full week ends:", size=8, color=MUTED, border=False); cell(w, "F3", "=Calc!C13", DATE_F, size=8, color=MUTED, border=False)
    hdr = ["Week", "Starts", "Ends", "Meta", "Google Ads", "ChatGPT Ads", "LinkedIn Ads", "Total", "Plan per week", "Over (+) / under (−) plan", "Spend",
           "Meta registrations", "Meta cost per registration", "Google conversions", "Google cost per conversion",
           "MQLs – paid social (HubSpot, optional)", "MQLs – paid search (HubSpot, optional)", "Notes – what happened this week", "Label"]
    header(w, W_FIRST - 1, 1, hdr, height=54)
    for col in "PQR":
        w[f"{col}{W_FIRST - 1}"].fill = PatternFill("solid", fgColor=INPUT); w[f"{col}{W_FIRST - 1}"].font = font(9, True, INK)
    for i in range(53):
        r = W_FIRST + i
        lo, hi = f"$B{r}", f"$C{r}"
        cell(w, f"A{r}", i + 1, "0", bold=True, align="center")
        cell(w, f"B{r}", f"={S_W1}+7*(A{r}-1)", DAY_F); cell(w, f"C{r}", f"=B{r}+6", DAY_F)
        cell(w, f"D{r}", f"={meta(lo, hi)}*{flag(20)}", AMT)
        cell(w, f"E{r}", f"={goog(lo, hi)}*{flag(21)}", AMT)
        cell(w, f"F{r}", f"={other(lo, hi, 'ChatGPT Ads', True)}*{flag(22)}", AMT)
        cell(w, f"G{r}", f"={other(lo, hi, 'LinkedIn Ads', True)}*{flag(23)}", AMT)
        cell(w, f"H{r}", f"=SUM(D{r}:G{r})", AMT, bold=True)
        cell(w, f"I{r}", f"={S_BUDGET}*MAX(0,MIN(C{r},{S_PEND})-MAX(B{r},{S_PSTART})+1)/({S_PEND}-{S_PSTART}+1)", AMT)
        cell(w, f"J{r}", f'=IF(OR(C{r}>{S_UPTO},H{r}=0),"",H{r}-I{r})', AMT)
        cell(w, f"K{r}", f'=IF(H{r}=0,"",REPT("█",ROUND(H{r}/MAX($H${W_FIRST}:$H${W_FIRST + 52})*30,0)))', size=8, color=NAVY)
        cell(w, f"L{r}", "=" + xsum(MX, CM_CONV, CM_DATE, lo, hi), "#,##0")
        cell(w, f"M{r}", f'=IF(L{r}=0,"",D{r}/L{r})', AMT2)
        cell(w, f"N{r}", "=" + xsum(GX, CG_CONV, CG_DAY, lo, hi), "#,##0")
        cell(w, f"O{r}", f'=IF(N{r}=0,"",E{r}/N{r})', AMT2)
        cell(w, f"P{r}", None, "#,##0", fill=INPUT, color=BLUE_T); cell(w, f"Q{r}", None, "#,##0", fill=INPUT, color=BLUE_T)
        txt = notes.get(datetime.date(2025, 12, 29) + datetime.timedelta(days=7 * i))
        cell(w, f"R{r}", ("Agency: " + txt) if txt else None, fill=INPUT, color=BLUE_T, wrap=True, size=8)
        cell(w, f"S{r}", f'=TEXT(B{r},"d mmm")', size=8, color=MUTED, align="center")
        w.row_dimensions[r].height = 36 if txt else 15
    note(w, f"A{W_FIRST + 53}", "Week 1 includes the last days of the previous year. Plan per week = the annual budget spread evenly over the year. "
                   "Notes marked 'Agency:' summarise the agency's weekly reports (until W/C 5 Oct) – add your own from W/C 12 Oct.")
    a, z = W_FIRST, W_FIRST + 52
    w.conditional_formatting.add(f"A{a}:O{z}", FormulaRule(formula=[f"$B{a}>$C$3"], font=font(color=MUTED)))
    w.conditional_formatting.add(f"A{a}:O{z}", FormulaRule(formula=[f"$C{a}=$F$3"], fill=PatternFill("solid", fgColor=GREENFILL), font=font(bold=True)))
    w.conditional_formatting.add(f"J{a}:J{z}", FormulaRule(formula=[f"AND(ISNUMBER(J{a}),J{a}>0)"], font=font(bold=True, color=RED)))
    w.freeze_panes = f"D{W_FIRST}"
    widths(w, {"A": 6, "B": 11, "C": 11, **{c: 11 for c in "DEFGHIJ"}, "K": 26, **{c: 11 for c in "LMNO"}, "P": 12, "Q": 12, "R": 64, "S": 7})
    section(w, f"A{z + 3}", "SPEND BY WEEK AND CHANNEL", "ABCDEFGHIJKLMNOP")
    c = BarChart(); c.type = "col"; c.grouping = "stacked"; c.overlap = 100; c.gapWidth = 40
    for j in range(4):
        c.add_data(Reference(w, min_col=4 + j, min_row=a - 1, max_row=z), titles_from_data=True)
    c.set_categories(Reference(w, min_col=19, min_row=a, max_row=z))
    style_bar(c, [CH_COLORS[n] for n, *_ in CHANNELS])
    c.width, c.height = 34, 8
    w.add_chart(c, f"A{z + 4}")


def style_bar(c, colors):
    for s, col in zip(c.series, colors):
        s.graphicalProperties.solidFill = col
    c.y_axis.numFmt = "#,##0"
    c.x_axis.delete = False; c.y_axis.delete = False
    c.legend.position = "b"


def style_line(c, colors):
    for s, col in zip(c.series, colors):
        s.graphicalProperties.line.solidFill = col
        s.graphicalProperties.line.width = 28575
        s.marker.symbol = "none"
        s.smooth = False
    c.y_axis.numFmt = "#,##0"
    c.x_axis.delete = False; c.y_axis.delete = False
    c.legend.position = "b"


# ---------------------------------------------------------------- by location
def by_location(b):
    title(b, "A1", "Spend by region, market and campaign type", None)
    cell(b, "A2", f'="USD · read from the campaign names (Settings → Locations) · sorted by spend this year · data up to "&TEXT({S_UPTO},"d mmm yyyy")',
         size=9, color=INK2, border=False, italic=True)
    months = [f'=TEXT(DATE({S_YEAR},{m},1),"mmm")' for m in range(1, 13)]
    mcol = lambda m: L(4 + m)   # Calc month columns D..O

    def block(top, label, n, first, name_f, val_f, region_f=None):
        section(b, f"A{top}", label, "ABCDEFGHIJKLMNOPQ")
        fm = 3 if region_f else 2
        header(b, top + 1, 1, [first] + (["Region"] if region_f else []) + months + ["Year", "Share", "Share of spend"])
        r0 = top + 2
        for i in range(n):
            r = r0 + i
            cell(b, f"A{r}", name_f(i), bold=True)
            if region_f:
                cell(b, f"B{r}", region_f(r), align="center", size=9)
            for m in range(12):
                cell(b, f"{L(fm + m)}{r}", val_f(r, m), AMT)
        rt = r0 + n
        cell(b, f"A{rt}", "Total", bold=True, fill=TOTAL)
        if region_f:
            cell(b, f"B{rt}", "", fill=TOTAL)
        for m in range(12):
            col = L(fm + m)
            cell(b, f"{col}{rt}", f"=SUM({col}{r0}:{col}{rt - 1})", AMT, bold=True, fill=TOTAL)
        tc, sc, bc = L(fm + 12), L(fm + 13), L(fm + 14)
        for r in range(r0, rt + 1):
            t = r == rt
            cell(b, f"{tc}{r}", f'=IF($A{r}="","",SUM({L(fm)}{r}:{L(fm + 11)}{r}))', AMT, bold=True, fill=TOTAL if t else None)
            cell(b, f"{sc}{r}", f'=IF(OR($A{r}="",${tc}${rt}=0),"",{tc}{r}/${tc}${rt})', PCT, fill=TOTAL if t else None, align="center")
            cell(b, f"{bc}{r}", "" if t else f'=IF({sc}{r}="","",REPT("█",ROUND({sc}{r}*40,0)))', fill=TOTAL if t else None, color=SLATE, size=8)
        return r0, rt

    mk_rng = lambda m: f"Calc!${mcol(m)}${MK0}:${mcol(m)}${MK0 + MKT_N - 1}"
    reg = block(4, "BY REGION", len(REGIONS), "Region", lambda i: REGIONS[i],
                lambda r, m: f"=SUMIFS({mk_rng(m)},Calc!$C${MK0}:$C${MK0 + MKT_N - 1},$A{r})")
    mkt = block(reg[1] + 3, "BY MARKET", 22, "Market", lambda i: f"=Calc!$R${MK0 + i}",
                lambda r, m: f'=IF($A{r}="","",SUMIFS({mk_rng(m)},Calc!$B${MK0}:$B${MK0 + MKT_N - 1},$A{r}))',
                region_f=lambda r: f'=IF($A{r}="","",IFERROR(VLOOKUP($A{r},Calc!$B${MK0}:$C${MK0 + MKT_N - 1},2,0),""))')
    typ = block(mkt[1] + 3, "BY CAMPAIGN TYPE", len(TYPES), "Campaign type", lambda i: f"=Calc!$R${TY0 + i}",
                lambda r, m: f'=IF($A{r}="","",SUMIFS(Calc!${mcol(m)}${TY0}:${mcol(m)}${TY0 + len(TYPES) - 1},Calc!$B${TY0}:$B${TY0 + len(TYPES) - 1},$A{r}))')
    note(b, f"A{typ[1] + 2}", "Market = the location code at the start of the campaign name (Geo:SA = Middle East, Geo:NA = US & Canada, 'US-UK-FR-IT', 'WW' and 'All' = Worldwide). "
                              "If the Update tab says some spend has no market, add the new code on Settings → Locations.")
    b.freeze_panes = "B4"
    widths(b, {"A": 32, "B": 12, **{L(3 + i): 9.5 for i in range(12)}, "O": 11, "P": 9, "Q": 30})
    b.parent._loc = dict(region=reg, market=mkt)


# ---------------------------------------------------------------- agency check
def agency_tab(a, weeks, totals):
    title(a, "A1", "Agency check – the agency's weekly reports (Notion) against the platform exports", None)
    note(a, "A2", "Reference only. Spend, leads and CPL are copied as the agency wrote them (read 13 Oct 2026). The official spend numbers are the platform exports.")
    hdr = ["Week starts", "Week ends", "Meta spend (agency, $)", "Meta leads (agency)", "Meta lead definition", "Meta CPL (agency)",
           "Google spend (agency, as written)", "Google currency (as written)", "Google leads (agency)", "Google CPL (agency)",
           "Issues found", "What the agency did or recommended", "Meta – platform (USD)", "Meta – platform excl. FR_Alibaba (USD)",
           "Meta: agency − platform excl. FR_Alibaba", "Google – platform (EUR)", "Google: agency ÷ platform", "What the Google difference looks like", "Label"]
    header(a, 4, 1, hdr, height=54)
    first = 5
    for i, w in enumerate(weeks):
        r = first + i
        cell(a, f"A{r}", w["start"], DATE_F); cell(a, f"B{r}", w["end"], DATE_F)
        cell(a, f"C{r}", w.get("meta_spend"), AMT2, color=BLUE_T); cell(a, f"D{r}", w.get("meta_leads"), "#,##0.##")
        cell(a, f"E{r}", w.get("meta_def"), size=8, wrap=True); cell(a, f"F{r}", w.get("meta_cpl"), size=9, align="right")
        cell(a, f"G{r}", w.get("google_spend"), AMT2, color=BLUE_T); cell(a, f"H{r}", w.get("google_cur"), align="center", size=9)
        cell(a, f"I{r}", w.get("google_leads"), "#,##0.##"); cell(a, f"J{r}", w.get("google_cpl"), size=9, align="right")
        cell(a, f"K{r}", w.get("flags"), size=8, wrap=True, color=RED if w.get("flags") else INK)
        cell(a, f"L{r}", w.get("notes"), size=8, wrap=True)
        cell(a, f"M{r}", "=" + meta(f"$A{r}", f"$B{r}"), AMT2)
        cell(a, f"N{r}", f"=M{r}-" + meta(f"$A{r}", f"$B{r}", '"FR_Alibaba Campaign"'), AMT2)
        cell(a, f"O{r}", f'=IF(OR(C{r}="",N{r}=0),"",C{r}-N{r})', AMT2)
        cell(a, f"P{r}", "=" + xsum(GX, CG_COST, CG_DAY, f"$A{r}", f"$B{r}"), AMT2)
        cell(a, f"Q{r}", f'=IF(OR(G{r}="",P{r}=0),"",G{r}/P{r})', "0.00", align="center")
        cell(a, f"R{r}", f'=IF(Q{r}="","",IF(ABS(Q{r}-1)<0.01,"Same as the platform (so the figure is in euros)",IF(ABS(Q{r}-2)<0.02,"Exactly double the platform",'
                         f'IF(AND(Q{r}>1.1,Q{r}<1.2),"About ×"&TEXT(Q{r},"0.00")&": looks converted to dollars",IF(Q{r}<1,TEXT(1-Q{r},"0%")&" lower than the platform",TEXT(Q{r}-1,"0%")&" higher than the platform")))))',
             size=8, wrap=True)
        cell(a, f"S{r}", f'=TEXT(A{r},"d mmm")', size=8, color=MUTED, align="center")
        a.row_dimensions[r].height = 54
    last = first + len(weeks) - 1
    a.conditional_formatting.add(f"O{first}:O{last}", FormulaRule(formula=[f"AND(ISNUMBER(O{first}),ABS(O{first})>5)"], font=font(bold=True, color=RED)))
    a.conditional_formatting.add(f"Q{first}:R{last}", FormulaRule(formula=[f"AND(ISNUMBER($Q{first}),ABS($Q{first}-1)>=0.01)"], font=font(9, True, RED)))
    note(a, f"A{last + 1}", "From W/C 7 Sep the agency left FR_Alibaba out of its Meta figures, so compare its Meta figure with the 'excl. FR_Alibaba' column.")
    top = last + 3
    section(a, f"A{top}", "WHAT THE AGENCY SAID IN TOTAL vs. THE PLATFORM EXPORTS", "ABCDEFGHIJKLMNO")
    header(a, top + 1, 1, ["Period", "", "What the agency wrote", "", "Agency figure ($)", "Platform – Meta (USD)", "Platform – Google (EUR)",
                           "Platform – total (USD)", "Agency − platform", "Difference", "Note", "", "", "", ""], height=36)
    for i, t in enumerate(totals):
        r = top + 2 + i
        a.merge_cells(f"A{r}:B{r}"); a.merge_cells(f"C{r}:D{r}"); a.merge_cells(f"K{r}:O{r}")
        cell(a, f"A{r}", t["period"], bold=True); cell(a, f"B{r}", None)
        cell(a, f"C{r}", t["quote"], size=8, wrap=True); cell(a, f"D{r}", None)
        cell(a, f"E{r}", t["agency"], AMT2, color=BLUE_T)
        lo, hi = t["lo"], t["hi"]
        dlo, dhi = f"DATE({lo.year},{lo.month},{lo.day})", f"DATE({hi.year},{hi.month},{hi.day})"
        has_m, has_g = t["chan"] in ("both", "meta"), t["chan"] in ("both", "google")
        gm = f'SUMIFS(Monthly!$C${M_FIRST}:$C${M_FIRST + 11},Monthly!$A${M_FIRST}:$A${M_FIRST + 11},">="&{dlo},Monthly!$A${M_FIRST}:$A${M_FIRST + 11},"<="&{dhi})'
        cell(a, f"F{r}", "=" + meta(dlo, dhi) if has_m else None, AMT2)
        cell(a, f"G{r}", "=" + xsum(GX, CG_COST, CG_DAY, dlo, dhi) if has_g else None, AMT2)
        cell(a, f"H{r}", "=" + "+".join(([meta(dlo, dhi)] if has_m else []) + ([gm] if has_g else [])), AMT2, bold=True)
        cell(a, f"I{r}", f"=E{r}-H{r}", AMT2, bold=True)
        cell(a, f"J{r}", f'=IF(H{r}=0,"",E{r}/H{r}-1)', '+0%;-0%;0%', align="center", size=9)
        cell(a, f"K{r}", t["note"], size=8, wrap=True)
        for col in "LMNO":
            cell(a, f"{col}{r}", None)
        a.row_dimensions[r].height = 42
    a.conditional_formatting.add(f"I{top + 2}:J{top + 1 + len(totals)}", FormulaRule(formula=[f"AND(ISNUMBER($I{top + 2}),ABS($I{top + 2})>100)"], font=font(bold=True, color=RED)))
    nr = top + 2 + len(totals)
    note(a, f"A{nr}", "Platform totals: Meta in USD as billed; Google in EUR as billed, converted with the Settings rate. "
                      "The agency's July report converted Google with \"£1 = $1.28\" although the Google Ads account is in euros.")
    ctop = nr + 3
    section(a, f"A{ctop}", "GOOGLE ADS: WHAT THE AGENCY REPORTED vs. THE PLATFORM, WEEK BY WEEK", "ABCDEFGHIJ")
    c = BarChart(); c.type = "col"; c.grouping = "clustered"; c.gapWidth = 40
    c.add_data(Reference(a, min_col=7, min_row=4, max_row=last), titles_from_data=True)
    c.add_data(Reference(a, min_col=16, min_row=4, max_row=last), titles_from_data=True)
    c.set_categories(Reference(a, min_col=19, min_row=first, max_row=last))
    style_bar(c, [CH_COLORS["Google Ads"], SLATE])
    c.width, c.height = 30, 9
    a.add_chart(c, f"A{ctop + 1}")
    a.freeze_panes = "C5"
    widths(a, {"A": 12, "B": 12, "C": 12, "D": 10, "E": 16, "F": 12, "G": 13, "H": 12, "I": 12, "J": 10, "K": 34, "L": 52,
               "M": 13, "N": 13, "O": 12, "P": 13, "Q": 10, "R": 26, "S": 8})


# ---------------------------------------------------------------- dashboard
def dashboard(d):
    d.sheet_view.showGridLines = False
    widths(d, {"A": 2, **{L(2 + i): 12.5 for i in range(12)}, "N": 2})
    d.merge_cells("B1:M1")
    cell(d, "B1", '="Paid Media Spend "&' + S_YEAR + '&" – Year Overview"', size=18, bold=True, color=NAVY, border=False)
    d.row_dimensions[1].height = 30
    d.merge_cells("B2:M2")
    cell(d, "B2", f'="Platform data up to "&TEXT({S_UPTO},"d mmm yyyy")&" · USD · Google Ads converted from EUR at "&TEXT({S_FXAVG},"0.0000")&" · Meta, Google Ads and ChatGPT Ads"',
         size=9, color=INK2, border=False, italic=True)
    d.merge_cells("B3:M3")
    cell(d, "B3", f'="Budget: "&{S_STATUS}', size=9, bold=True, color=NAVY, fill="E8EEF7", border=False)
    d.row_dimensions[3].height = 20
    tiles = [
        (f'="BUDGET "&{S_YEAR}', f"={USD('Calc!C27')}", f'="Maximum "&{USD("Calc!C28")}&" · originally "&{USD("Calc!C29")}'),
        ('="SPENT SO FAR"', f"={USD('Calc!C30')}", '=TEXT(Calc!C33,"0%")&" of the budget · "&TEXT(Calc!C9,"0%")&" of the year gone"'),
        ('="LEFT IN THE BUDGET"', f'=IF(Calc!C31<0,"–"&{USD("-Calc!C31")},{USD("Calc!C31")})',
         f'=IF(Calc!C31<0,"Budget already used up","≈ "&{USD("Calc!C43")}&" a week until "&TEXT(Calc!C5,"d mmm"))'),
        ('="LEFT UP TO THE MAXIMUM"', f'=IF(Calc!C32<0,"–"&{USD("-Calc!C32")},{USD("Calc!C32")})',
         f'=IF(Calc!C32<0,"Maximum already passed","≈ "&{USD("Calc!C44")}&" a week until "&TEXT(Calc!C5,"d mmm"))'),
        ('="CURRENT PACE PER WEEK"', f"={USD('Calc!C39')}", '="Last 3 full weeks ("&TEXT(Calc!C15,"d mmm")&" – "&TEXT(Calc!C13,"d mmm")&"), campaigns still running"'),
        ('="FORECAST YEAR-END"', f"={USD('Calc!C42')}",
         f'=IF(Calc!C42>Calc!C27,"▲ "&{USD("Calc!C42-Calc!C27")}&" over budget","▼ "&{USD("Calc!C27-Calc!C42")}&" under budget")&" · "&IF(Calc!C42>Calc!C28,"over","within")&" the maximum"'),
    ]
    for i, (lab, val, sub) in enumerate(tiles):
        c1, c2 = L(2 + 2 * i), L(3 + 2 * i)
        for r in (5, 6, 7):
            d.merge_cells(f"{c1}{r}:{c2}{r}")
            d[f"{c2}{r}"].fill = PatternFill("solid", fgColor=SUBTLE)
        cell(d, f"{c1}5", lab, size=8, bold=True, color=INK2, fill=SUBTLE, border=False)
        cell(d, f"{c1}6", val, size=18, bold=True, color=INK, fill=SUBTLE, border=False)
        cell(d, f"{c1}7", sub, size=8, color=INK2, fill=SUBTLE, border=False, wrap=True)
    d.row_dimensions[5].height = 18; d.row_dimensions[6].height = 30; d.row_dimensions[7].height = 30
    cell(d, "P1", "Helper cells – don't edit", size=8, color=MUTED, border=False)
    cell(d, "P2", "=Calc!C9", "0.0%", size=8, color=MUTED, border=False)
    cell(d, "P3", "=Calc!C42-Calc!C27", AMT, size=8, color=MUTED, border=False)
    d.conditional_formatting.add("L7", FormulaRule(formula=["$P$3>0"], font=font(8, True, RED)))
    d.conditional_formatting.add("F6", FormulaRule(formula=['LEFT(F6,1)="–"'], font=font(18, True, RED)))

    section(d, "B9", "BUDGET CHECK", [L(2 + i) for i in range(12)])
    for a_, z_ in (("B", "C"), ("H", "J"), ("K", "M")):
        d.merge_cells(f"{a_}10:{z_}10")
    hdr = {"B": "Measure", "D": "Amount", "E": "Spent so far", "F": "Left", "G": "% used",
           "H": '="Progress  (year gone: "&TEXT(Calc!C9,"0%")&")"', "K": "Status at the current pace"}
    for col in "BCDEFGHIJKLM":
        cell(d, f"{col}10", hdr.get(col), bold=True, color=WHITE, fill=NAVY, align="center", wrap=True, size=9)
    d.row_dimensions[10].height = 26
    checks = [
        ("Budget", "Calc!C27", "Calc!C31", "Calc!C33",
         '=IF(Calc!C30>=Calc!C27,"▲ Budget used up",IF(Calc!C42>Calc!C27,"▲ Ends ≈ "&' + USD("Calc!C42-Calc!C27") + '&" over budget","● Ends within budget"))'),
        ("Maximum (ideally not more)", "Calc!C28", "Calc!C32", "Calc!C34",
         '=IF(Calc!C30>=Calc!C28,"▲ Maximum passed",IF(Calc!C42>Calc!C28,"▲ Ends ≈ "&' + USD("Calc!C42-Calc!C28") + '&" over the maximum","● Ends ≈ "&' + USD("Calc!C28-Calc!C42") + '&" under the maximum"))'),
    ]
    for i, (lab, amt, left, pct, status) in enumerate(checks):
        r = 11 + i
        d.merge_cells(f"B{r}:C{r}"); d.merge_cells(f"H{r}:J{r}"); d.merge_cells(f"K{r}:M{r}")
        cell(d, f"B{r}", lab, bold=True); cell(d, f"C{r}", None)
        cell(d, f"D{r}", f"={amt}", AMT); cell(d, f"E{r}", "=Calc!C30", AMT, bold=True); cell(d, f"F{r}", f"={left}", AMT)
        cell(d, f"G{r}", f"={pct}", PCT, align="center", bold=True)
        cell(d, f"H{r}", f'=REPT("█",ROUND(MIN(G{r},1)*26,0))&REPT("░",26-ROUND(MIN(G{r},1)*26,0))', color=INK2, size=8)
        for col in "IJ":
            cell(d, f"{col}{r}", None)
        cell(d, f"K{r}", status, bold=True, size=9)
        for col in "LM":
            cell(d, f"{col}{r}", None)
    d.merge_cells("B13:M13")
    cell(d, "B13", f'="By "&TEXT(Calc!C3,"d mmm")&", "&{USD("Calc!C30")}&" was spent: "&{USD("ABS(Calc!C36)")}&IF(Calc!C36>=0," more"," less")&" than an even pace through the year ("&{USD("Calc!C35")}&"). Current pace = "&Calc!C40&"."',
         size=9, color=INK2, border=False, italic=True, wrap=True)
    d.row_dimensions[13].height = 26
    d.conditional_formatting.add("K11:K12", FormulaRule(formula=['LEFT(K11,1)="▲"'], font=font(9, True, RED)))
    d.conditional_formatting.add("K11:K12", FormulaRule(formula=['LEFT(K11,1)="●"'], font=font(9, True, GREEN)))
    d.conditional_formatting.add("H11:H12", FormulaRule(formula=["G11>=1"], font=font(8, False, RED)))
    d.conditional_formatting.add("H11:H12", FormulaRule(formula=["AND(G11<1,G11>$P$2+0.05)"], font=font(8, False, AMBER)))

    section(d, "B15", "SPEND BY CHANNEL", [L(2 + i) for i in range(12)])
    d.merge_cells("B16:C16"); d.merge_cells("K16:M16")
    hdr = {"B": "Channel", "D": "Spent (USD)", "E": "Share", "F": "Last full month", "G": "Last 3 full months", "H": "Last full week",
           "I": "Counts toward budget?", "J": "Billing currency", "K": "Note"}
    for col in "BCDEFGHIJKLM":
        cell(d, f"{col}16", hdr.get(col), bold=True, color=WHITE, fill=NAVY, align="center", wrap=True, size=9)
    d.row_dimensions[16].height = 26
    for i, (name, srow, cur) in enumerate(CHANNELS):
        r, cr = 17 + i, 20 + i
        d.merge_cells(f"B{r}:C{r}"); d.merge_cells(f"K{r}:M{r}")
        cell(d, f"B{r}", name, bold=True); cell(d, f"C{r}", None)
        cell(d, f"D{r}", f"=Calc!D{cr}", AMT); cell(d, f"E{r}", f"=Calc!I{cr}", PCT, align="center")
        cell(d, f"F{r}", f"=Calc!E{cr}", AMT); cell(d, f"G{r}", f"=Calc!F{cr}", AMT)
        cell(d, f"H{r}", f'=IF(Calc!G{cr}=0,"–",Calc!G{cr})', AMT, align="right")
        cell(d, f"I{r}", f"=Settings!C{srow}", align="center"); cell(d, f"J{r}", f"=Settings!B{srow}", align="center")
        cell(d, f"K{r}", f'=IF(Settings!D{srow}="","",Settings!D{srow})', size=8, wrap=True)
        for col in "LM":
            cell(d, f"{col}{r}", None)
        d.row_dimensions[r].height = 24 if i == 0 else 16
    d.merge_cells("B21:C21"); d.merge_cells("K21:M21")
    cell(d, "B21", "Total", bold=True, fill=TOTAL); cell(d, "C21", None, fill=TOTAL)
    for col, f in zip("DEFGH", ["=Calc!D25", '=IF(Calc!D25=0,"",1)', "=Calc!E25", "=Calc!F25", '=IF(Calc!G25=0,"–",Calc!G25)']):
        cell(d, f"{col}21", f, PCT if col == "E" else AMT, bold=True, fill=TOTAL, align="center" if col == "E" else "right")
    for col in "IJKLM":
        cell(d, f"{col}21", None, fill=TOTAL)
    d.merge_cells("B22:M22")
    cell(d, "B22", f'="Last full week = "&TEXT(Calc!C14,"d mmm")&" – "&TEXT(Calc!C13,"d mmm")&". Left out of the current pace: "&{USD("Calc!C49")}&" spent in the last 3 full weeks by the campaigns on the Ended list (Settings)."',
         size=9, color=INK2, border=False, italic=True)

    m = d.parent["Monthly"]
    section(d, "B24", "SPEND BY MONTH AND CHANNEL", ["B", "C", "D", "E", "F", "G"])
    section(d, "H24", "SPENT SO FAR vs. PLAN (CUMULATIVE)", ["H", "I", "J", "K", "L", "M"])
    bar = BarChart(); bar.type = "col"; bar.grouping = "stacked"; bar.overlap = 100; bar.gapWidth = 60
    for j in range(4):
        bar.add_data(Reference(m, min_col=2 + j, min_row=M_FIRST - 1, max_row=M_FIRST + 11), titles_from_data=True)
    bar.set_categories(Reference(m, min_col=20, min_row=M_FIRST, max_row=M_FIRST + 11))
    style_bar(bar, [CH_COLORS[n] for n, *_ in CHANNELS])
    bar.width, bar.height = 16.2, 8.2
    d.add_chart(bar, "B25")
    cum = BarChart(); cum.type = "col"; cum.grouping = "clustered"; cum.gapWidth = 60
    cum.add_data(Reference(m, min_col=9, min_row=M_FIRST - 1, max_row=M_FIRST + 11), titles_from_data=True)
    cum.add_data(Reference(m, min_col=10, min_row=M_FIRST - 1, max_row=M_FIRST + 11), titles_from_data=True)
    cum.set_categories(Reference(m, min_col=20, min_row=M_FIRST, max_row=M_FIRST + 11))
    style_bar(cum, [NAVY, "C9D1DC"])
    cum.width, cum.height = 16.2, 8.2
    d.add_chart(cum, "H25")

    top = 42
    section(d, f"B{top}", "QUARTER BY QUARTER", [L(2 + i) for i in range(12)])
    d.merge_cells(f"B{top + 1}:C{top + 1}"); d.merge_cells(f"K{top + 1}:M{top + 1}")
    qh = {"B": "Quarter", "D": "Meta", "E": "Google Ads", "F": "ChatGPT Ads", "G": "LinkedIn Ads", "H": "Total", "I": "Plan", "J": "Over (+) / under (−)", "K": "Status"}
    for col in "BCDEFGHIJKLM":
        cell(d, f"{col}{top + 1}", qh.get(col), bold=True, color=WHITE, fill=NAVY, align="center", wrap=True, size=9)
    d.row_dimensions[top + 1].height = 28
    for q in range(4):
        r = top + 2 + q
        a, z = M_FIRST + 3 * q, M_FIRST + 2 + 3 * q
        d.merge_cells(f"B{r}:C{r}"); d.merge_cells(f"K{r}:M{r}")
        cell(d, f"B{r}", f'="Q{q + 1}  ("&TEXT(Monthly!A{a},"mmm")&"–"&TEXT(Monthly!A{z},"mmm")&")"', bold=True); cell(d, f"C{r}", None)
        for j, col in enumerate("DEFG"):
            cell(d, f"{col}{r}", f"=SUM(Monthly!{L(2 + j)}{a}:{L(2 + j)}{z})", AMT)
        cell(d, f"H{r}", f"=SUM(D{r}:G{r})", AMT, bold=True)
        cell(d, f"I{r}", f"=SUM(Monthly!G{a}:G{z})", AMT)
        cell(d, f"J{r}", f'=IF({S_UPTO}<EOMONTH(Monthly!A{z},0),"",H{r}-I{r})', AMT)
        nxt = f'IF({S_UPTO}<EOMONTH(Monthly!A{z + 3},0),"Complete · last quarter","Complete")' if q < 3 else '"Complete"'
        cell(d, f"K{r}", f'=IF({S_UPTO}>=EOMONTH(Monthly!A{z},0),{nxt},IF({S_UPTO}>=Monthly!A{a},"In progress","Not started"))', align="center", size=9)
        for col in "LM":
            cell(d, f"{col}{r}", None)
    r = top + 6
    d.merge_cells(f"B{r}:C{r}"); d.merge_cells(f"K{r}:M{r}")
    cell(d, f"B{r}", "Total", bold=True, fill=TOTAL); cell(d, f"C{r}", None, fill=TOTAL)
    for col in "DEFGHI":
        cell(d, f"{col}{r}", f"=SUM({col}{top + 2}:{col}{top + 5})", AMT, bold=True, fill=TOTAL)
    for col in "JKLM":
        cell(d, f"{col}{r}", None, fill=TOTAL)
    d.conditional_formatting.add(f"J{top + 2}:J{top + 5}", FormulaRule(formula=[f"AND(ISNUMBER(J{top + 2}),J{top + 2}>0)"], font=font(10, True, RED)))
    d.conditional_formatting.add(f"B{top + 2}:M{top + 5}", FormulaRule(formula=[f'ISNUMBER(SEARCH("last quarter",$K{top + 2}))'], fill=PatternFill("solid", fgColor=GREENFILL)))

    top = 50
    section(d, f"B{top}", "YEAR-END OUTLOOK", [L(2 + i) for i in range(12)])
    for rr in range(top + 1, top + 6):
        d.merge_cells(f"B{rr}:E{rr}"); d.merge_cells(f"J{rr}:M{rr}")
    oh = {"B": "If we spend from now on at…", "F": "Per week (USD)", "G": "Year-end total", "H": "vs. budget", "I": "vs. maximum", "J": "What it means"}
    for col in "BCDEFGHIJKLM":
        cell(d, f"{col}{top + 1}", oh.get(col), bold=True, color=WHITE, fill=NAVY, align="center", wrap=True, size=9)
    d.row_dimensions[top + 1].height = 24
    rows = [
        ('="…the current pace"', "=Calc!C39", "=Calc!C42", '="Source: "&Calc!C40'),
        ('="…a pace that lands exactly on the budget"', "=MAX(0,Calc!C43)", "=Calc!C27",
         '=IF(Calc!C31<=0,"The budget is already used up",IF(Calc!C39=0,"",IF(Calc!C43<Calc!C39,TEXT(1-Calc!C43/Calc!C39,"0%")&" less per week than now",TEXT(Calc!C43/Calc!C39-1,"0%")&" more per week than now")))'),
        ('="…a pace that uses the maximum"', "=MAX(0,Calc!C44)", "=Calc!C28",
         '=IF(Calc!C32<=0,"The maximum is already passed",IF(Calc!C39=0,"",IF(Calc!C44<Calc!C39,TEXT(1-Calc!C44/Calc!C39,"0%")&" less per week than now",TEXT(Calc!C44/Calc!C39-1,"0%")&" more per week than now")))'),
        ('="…last month\'s pace ("&TEXT(Calc!C11,"mmmm")&", before the cuts)"', "=Calc!C45/Calc!C17*7", "=Calc!C47", '="For reference"'),
    ]
    for i, (lab, pw, ye, what) in enumerate(rows):
        r = top + 2 + i
        cell(d, f"B{r}", lab, bold=True)
        for col in "CDE":
            cell(d, f"{col}{r}", None)
        cell(d, f"F{r}", pw, AMT); cell(d, f"G{r}", ye, AMT, bold=True)
        cell(d, f"H{r}", f"=G{r}-Calc!$C$27", AMT); cell(d, f"I{r}", f"=G{r}-Calc!$C$28", AMT)
        cell(d, f"J{r}", what, size=8, wrap=True)
        for col in "KLM":
            cell(d, f"{col}{r}", None)
        d.row_dimensions[r].height = 26 if i == 0 else 16
    d.conditional_formatting.add(f"H{top + 2}:I{top + 5}", FormulaRule(formula=[f"H{top + 2}>0.5"], font=font(10, True, RED)))

    top = 57
    r0, rt = d.parent._loc["region"]
    m0, mt = d.parent._loc["market"]
    section(d, f"B{top}", "WHERE THE MONEY WENT – BY REGION", ["B", "C", "D", "E", "F", "G"])
    section(d, f"H{top}", "TOP MARKETS (year to date)", ["H", "I", "J", "K", "L", "M"])
    for i in range(10):
        r = top + 1 + i
        if i < 4:
            d.merge_cells(f"B{r}:C{r}"); d.merge_cells(f"F{r}:G{r}")
            cell(d, f"B{r}", f"='By location'!A{r0 + i}", bold=True, size=9); cell(d, f"C{r}", None)
            cell(d, f"D{r}", f"='By location'!N{r0 + i}", AMT); cell(d, f"E{r}", f"='By location'!O{r0 + i}", PCT, align="center")
            cell(d, f"F{r}", f'=IF(\'By location\'!O{r0 + i}="","",REPT("█",ROUND(\'By location\'!O{r0 + i}*24,0)))', size=8, color=SLATE); cell(d, f"G{r}", None)
        d.merge_cells(f"H{r}:I{r}"); d.merge_cells(f"L{r}:M{r}")
        cell(d, f"H{r}", f"='By location'!A{m0 + i}", bold=True, size=9); cell(d, f"I{r}", None)
        cell(d, f"J{r}", f"=IF('By location'!A{m0 + i}=\"\",\"\",'By location'!O{m0 + i})", AMT)
        cell(d, f"K{r}", f"=IF('By location'!A{m0 + i}=\"\",\"\",'By location'!P{m0 + i})", PCT, align="center")
        cell(d, f"L{r}", f'=IF(\'By location\'!P{m0 + i}="","",REPT("█",ROUND(\'By location\'!P{m0 + i}*24,0)))', size=8, color=SLATE); cell(d, f"M{r}", None)
    note(d, f"B{top + 12}", "Region and market come from the location code in each campaign name – full detail on 'By location'. How to update: the 'Update' tab.")
    d.column_dimensions["P"].hidden = True
    d.print_area = "A1:N70"
    d.print_options.horizontalCentered = True
    d.page_setup.orientation = "landscape"
    d.page_setup.fitToWidth = 1
    d.sheet_properties.pageSetUpPr.fitToPage = True
    d.page_setup.fitToHeight = 0


# ---------------------------------------------------------------- update tab
def update_tab(u, sources):
    u.sheet_view.showGridLines = False
    widths(u, {"A": 2, **{L(2 + i): 12.5 for i in range(12)}, "N": 2})
    u.merge_cells("B1:M1"); cell(u, "B1", "Weekly update – every Monday, about 10 minutes", size=18, bold=True, color=NAVY, border=False)
    u.row_dimensions[1].height = 30
    u.merge_cells("B2:M2")
    cell(u, "B2", "Replace the two exports, check the ticks, write one note. Every other tab updates by itself.", size=9, color=INK2, border=False, italic=True)
    tiles = [
        ("DATA UP TO", '=TEXT(Calc!C3,"ddd d mmm yyyy")', f"=Calc!C{CK_FIRST + 2}"),
        ("META EXPORT", '=TEXT(Calc!C57,"#,##0")&" rows"', f"=Calc!C{CK_FIRST}"),
        ("GOOGLE ADS EXPORT", '=TEXT(Calc!C58,"#,##0")&" rows"', f"=Calc!C{CK_FIRST + 1}"),
        ("STATUS", f'=IF({CK_COUNT}=0,"✓ All good","⚠ "&{CK_COUNT}&" to fix")', f'=IF({CK_COUNT}=0,"All {CK_N} checks passed","See the checks below")'),
    ]
    for i, (lab, val, sub) in enumerate(tiles):
        c1, c3 = L(2 + 3 * i), L(4 + 3 * i)
        for r in (4, 5, 6):
            u.merge_cells(f"{c1}{r}:{c3}{r}")
            for col in (L(2 + 3 * i), L(3 + 3 * i), c3):
                u[f"{col}{r}"].fill = PatternFill("solid", fgColor=SUBTLE)
        cell(u, f"{c1}4", lab, size=8, bold=True, color=INK2, fill=SUBTLE, border=False)
        cell(u, f"{c1}5", val, size=16, bold=True, color=INK, fill=SUBTLE, border=False)
        cell(u, f"{c1}6", sub, size=8, color=INK2, fill=SUBTLE, border=False, wrap=True)
    u.row_dimensions[4].height = 18; u.row_dimensions[5].height = 28; u.row_dimensions[6].height = 30
    u.conditional_formatting.add("B6:M6", FormulaRule(formula=['LEFT(B6,1)="⚠"'], font=font(8, True, RED)))
    u.conditional_formatting.add("B6:M6", FormulaRule(formula=['LEFT(B6,1)="✓"'], font=font(8, True, GREEN)))
    u.conditional_formatting.add("K5", FormulaRule(formula=['LEFT(K5,1)="⚠"'], font=font(16, True, RED)))
    u.conditional_formatting.add("K5", FormulaRule(formula=['LEFT(K5,1)="✓"'], font=font(16, True, GREEN)))

    section(u, "B8", "THE 3 STEPS", [L(2 + i) for i in range(12)])
    steps = [
        ("Meta → 'Meta export' tab",
         "Ads Manager: Campaigns → dates 1 Jan – yesterday → Breakdown: By time → Day → Reports → Export table data → .csv.\n"
         "Here: open 'Meta export' → select all (Ctrl/Cmd+A) → Delete → click A1 → File → Import → Upload the file → Import location: "
         "'Replace data at selected cell' → Import data."),
        ("Google Ads → 'Google export' tab",
         "Google Ads: Reports → your saved spend report (Campaign, Day, Currency code, Cost, Impr., Clicks, Conversions) → dates 1 Jan – yesterday → "
         "Download → .csv.\nHere: open 'Google export' → select all → Delete → click A1 → File → Import → Upload → 'Replace data at selected cell' → Import data."),
        ("Check the ticks, write last week's note",
         '="Status above should say ✓ All good. Then on the Weekly tab write 1–2 lines in Notes for W/C "&TEXT(Calc!C14,"d mmm")&" (launches, pauses, budget changes). Then open the Dashboard."'),
    ]
    r = 9
    for n, (head, how) in enumerate(steps, 1):
        u.merge_cells(f"B{r}:B{r + 2}")
        cell(u, f"B{r}", n, size=20, bold=True, color=WHITE, fill="2A78D6", border=False, align="center")
        u.merge_cells(f"C{r}:M{r}"); cell(u, f"C{r}", head, size=11, bold=True, color=NAVY, fill=PALE, border=False)
        u.merge_cells(f"C{r + 1}:M{r + 2}"); cell(u, f"C{r + 1}", how, size=9, color=INK, fill=PALE, border=False, wrap=True, valign="top")
        for rr in range(r, r + 3):
            for col in "CDEFGHIJKLM":
                u[f"{col}{rr}"].fill = PatternFill("solid", fgColor=PALE)
        u.row_dimensions[r].height = 20; u.row_dimensions[r + 1].height = 22; u.row_dimensions[r + 2].height = 22
        r += 4

    top = 21
    section(u, f"B{top}", "CHECKS", [L(2 + i) for i in range(12)])
    header(u, top + 1, 2, ["Check", "", "Result", "", "", "", "", "", "If it shows ⚠", "", "", ""], height=20)
    for a_, z_ in (("B", "C"), ("D", "I"), ("J", "M")):
        u.merge_cells(f"{a_}{top + 1}:{z_}{top + 1}")
    todo = ["Export by day with the same columns as before, then import again.",
            "Use the saved report (Campaign, Day, Cost …), then import again.",
            "Export both to the same day (1 Jan – yesterday) and import again.",
            "Settings → Locations: add the new code with its market.",
            "Ask Claude to make the tracker read more rows.",
            "Settings → Ended campaigns: copy the name exactly from the export."]
    for i in range(CK_N):
        rr = top + 2 + i
        for a_, z_ in (("B", "C"), ("D", "I"), ("J", "M")):
            u.merge_cells(f"{a_}{rr}:{z_}{rr}")
        cell(u, f"B{rr}", f"=Calc!B{CK_FIRST + i}", bold=True, size=9)
        cell(u, f"D{rr}", f"=Calc!C{CK_FIRST + i}", size=9)
        cell(u, f"J{rr}", todo[i], size=8, color=INK2, wrap=True)
        for col in "CEFGHIKLM":
            cell(u, f"{col}{rr}", None)
        u.row_dimensions[rr].height = 22
    ck0, ck1 = top + 2, top + 1 + CK_N
    u.conditional_formatting.add(f"D{ck0}:I{ck1}", FormulaRule(formula=[f'LEFT($D{ck0},1)="⚠"'], font=font(9, True, RED), fill=PatternFill("solid", fgColor="FBE5E5")))
    u.conditional_formatting.add(f"D{ck0}:I{ck1}", FormulaRule(formula=[f'LEFT($D{ck0},1)="✓"'], font=font(9, False, GREEN)))

    top = ck1 + 2
    section(u, f"B{top}", "LAST FULL WEEK", [L(2 + i) for i in range(12)])
    u.merge_cells(f"B{top + 1}:M{top + 1}")
    cell(u, f"B{top + 1}", '="W/C "&TEXT(Calc!C14,"d mmm")&": "&' + USD("Calc!G24") + '&" spent (Meta "&' + USD("Calc!G20") + '&", Google Ads "&' + USD("Calc!G21") +
         '&") · to land on the budget we can spend ≈ "&' + USD("Calc!C43") + '&" a week from now on · full detail on the Weekly tab."', size=10, border=False, wrap=True)
    u.row_dimensions[top + 1].height = 30
    top += 3
    section(u, f"B{top}", "ONLY WHEN NEEDED", [L(2 + i) for i in range(12)])
    extra = [("ChatGPT Ads or LinkedIn Ads ran", "'Other channels' tab → one row per campaign per day or week, spend as billed."),
             ("A campaign stopped for good", "Settings → Ended campaigns → add its name, so the forecast stops counting it."),
             ("A check says some spend has no market", "Settings → Locations → add the new code (or the full campaign name) with its market."),
             ("Finance gives monthly EUR → USD rates", "Settings → Exchange rate → type each month's rate."),
             ("First Monday of the month", "Monthly tab → compare the 'as billed' columns with the Meta and Google Ads invoices.")]
    for i, (when, what) in enumerate(extra):
        rr = top + 1 + i
        u.merge_cells(f"B{rr}:D{rr}"); u.merge_cells(f"E{rr}:M{rr}")
        cell(u, f"B{rr}", when, bold=True, size=9); cell(u, f"E{rr}", what, size=9)
        for col in "CDFGHIJKLM":
            cell(u, f"{col}{rr}", None)
    top = top + len(extra) + 2
    section(u, f"B{top}", "SOURCES", [L(2 + i) for i in range(12)])
    for i, t in enumerate(sources):
        rr = top + 1 + i
        u.merge_cells(f"B{rr}:M{rr}")
        cell(u, f"B{rr}", t, size=8, color=INK2, border=False, wrap=True)
        u.row_dimensions[rr].height = 24 if len(t) > 170 else 13


AGENCY_TOTALS = [
    dict(period="February 2026", quote="\"We've spent $38,762 last month\" (2026 February monthly)", agency=38762,
         lo=datetime.date(2026, 2, 1), hi=datetime.date(2026, 2, 28), chan="both", note="Close to the platforms, but not equal."),
    dict(period="April 2026 – Meta", quote="Meta spend $24,586.06 (July monthly report, April–June comparison)", agency=24586.06,
         lo=datetime.date(2026, 4, 1), hi=datetime.date(2026, 4, 30), chan="meta", note="Higher than Meta's own figure for April."),
    dict(period="April 2026 – Google", quote="Google $11,420.33 (July monthly report)", agency=11420.33,
         lo=datetime.date(2026, 4, 1), hi=datetime.date(2026, 4, 30), chan="google", note="Equals Google's euros × 1.28 (a £→$ rate)."),
    dict(period="May 2026 – Meta", quote="Meta spend $22,276.50 (July monthly report)", agency=22276.50,
         lo=datetime.date(2026, 5, 1), hi=datetime.date(2026, 5, 31), chan="meta", note="Matches Meta."),
    dict(period="May 2026 – Google", quote="Google $13,815.37 (July monthly report)", agency=13815.37,
         lo=datetime.date(2026, 5, 1), hi=datetime.date(2026, 5, 31), chan="google", note="Equals Google's euros × 1.28."),
    dict(period="June 2026 – Meta", quote="Meta spend $17,453.29 (July monthly report)", agency=17453.29,
         lo=datetime.date(2026, 6, 1), hi=datetime.date(2026, 6, 30), chan="meta", note="Matches Meta."),
    dict(period="June 2026 – Google", quote="Google $15,982.98 (July monthly report)", agency=15982.98,
         lo=datetime.date(2026, 6, 1), hi=datetime.date(2026, 6, 30), chan="google", note="Equals Google's euros × 1.28."),
    dict(period="July 2026 – total", quote="\"Total Spend: $34,014.08\" (Meta $18,956.66, Google $15,057.42) – July monthly report", agency=34014.08,
         lo=datetime.date(2026, 7, 1), hi=datetime.date(2026, 7, 31), chan="both", note="Meta matches; Google = euros × 1.28."),
    dict(period="H1 2026 (Jan–Jun)", quote="\"invested a total of $182,515.62\" against a $175,000 H1 target ($350,000 annual) – Client H1 2026 Report",
         agency=182515.62, lo=datetime.date(2026, 1, 1), hi=datetime.date(2026, 6, 30), chan="both",
         note="A second H1 page says $96,486.65, with data only to 24 Mar."),
]

SOURCES = [
    "Platform data: Meta Ads Manager export ('Plug and Play Tech Center – Dollars' ad account, USD) and Google Ads report (EUR), campaign × day, "
    "1 Jan – 12 Oct 2026, exported 13 Oct 2026. ChatGPT Ads: 'Test 1', 23 Sep – 2 Oct 2026, €229.56, typed on 'Other channels'.",
    "Current pace: last 3 full weeks of all channels, without the campaigns on the Ended list (FR_Alibaba, run by PnP's internal team, last spend 5 Oct; ChatGPT 'Test 1', ended 2 Oct).",
    "Budget: Tereza, 13 Oct 2026 – $300k for 2026 (originally $350k), up to $320k at most. Exchange rate: 1 EUR = 1.1177 USD (live rate on 13 Oct 2026). "
    "Agency figures: the agency's weekly reports in Notion, copied as written ('Agency check' tab).",
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "agency") if os.path.isdir(os.path.join(here, "agency")) else os.path.join(here, "..", "agency"))
    import agency_weeks as AW
    out, meta_csv, google_csv = sys.argv[1], sys.argv[2], sys.argv[3]
    build(out, LX.read(meta_csv), LX.read(google_csv), AW.weeks(), AGENCY_TOTALS, SOURCES)
    print("saved", out)
