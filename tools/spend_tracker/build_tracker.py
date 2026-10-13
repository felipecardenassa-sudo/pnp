"""Build the PnP Paid Media Spend Tracker 2026 (Google Sheets friendly .xlsx) - v4, built for a 10-minute weekly update.

Usage (from this folder): python build_tracker.py OUT.xlsx META_EXPORT.csv GOOGLE_EXPORT.csv

How the workbook works
- 'Meta export' and 'Google export' hold this year's platform exports (campaign x day) exactly as exported.
  Every week they are replaced, not appended, so nothing has to be kept in order and nothing can be pasted twice.
- The hidden 'Data' tab reads both exports by column name (a moved column doesn't break anything), converts EUR to USD
  with the Settings rates, and gives each row a market (location code in the campaign name -> Settings > Locations)
  and a campaign type (naming rules). ChatGPT Ads / LinkedIn Ads rows are typed on 'Other channels'.
- Weekly, Monthly, By location & type, the Dashboard and the hidden 'Calc' tab are SUMIFS over 'Data'.
- Plain functions only (SUMIFS, INDEX, MATCH, VLOOKUP, IF, TEXT, LARGE ...): same results in Google Sheets, Excel, LibreOffice.
"""
import sys, os, datetime
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as L
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.label import DataLabelList
from xlstyle import *
import campaign_map as CM
import load_exports as LX

CHANNELS = [  # name, Settings row, billing currency, counts toward the budget, note
    ("Meta", 20, "USD", "Yes", "Includes FR_Alibaba (run by PnP's internal team) – confirm it belongs in this budget."),
    ("Google Ads", 21, "EUR", "Yes", ""),
    ("ChatGPT Ads", 22, "EUR", "Yes", "To confirm with Tereza."),
    ("LinkedIn Ads", 23, "USD", "Yes", "No spend in 2026. Billing currency to check."),
]
FX_RATE = 1.1177
FX_SOURCE = "Live rate on 13 Oct 2026 (from Felipe). Replace with Finance's monthly rates if they use them."
REGIONS = ["EMEA", "Americas", "Global", "Not specified"]
SLATE, GREENFILL = "6B7A8F", "E2EFDA"
BLUE_T = "0000FF"

# How many export rows the tracker reads (Meta: 30 rows a day today -> about 11,000 by 31 Dec; Google: 5 a day)
META_CAP, GOOGLE_CAP, OTHER_CAP = 15000, 7000, 300
D_META0 = 2                          # Data row that reads Meta export row 1
D_GOOG0 = D_META0 + META_CAP         # Data row that reads Google export row 1
D_OTH0 = D_GOOG0 + GOOGLE_CAP        # Data row that reads Other channels row OC_FIRST
D_LAST = D_OTH0 + OTHER_CAP - 1
OC_FIRST = 5
NF = 30                              # column AD: always empty, so a column that isn't found reads as empty
MX, GX = "'Meta export'!$A:$AD", "'Google export'!$A:$AD"
OCR = f"'Other channels'!$A${OC_FIRST}:$J${OC_FIRST + OTHER_CAP - 1}"

# Settings cells
S_YEAR, S_BUDGET, S_MAX, S_ORIG, S_STATUS = "Settings!$B$5", "Settings!$B$6", "Settings!$B$7", "Settings!$B$8", "Settings!$B$9"
S_PSTART, S_PEND, S_W1 = "Settings!$B$10", "Settings!$C$10", "Settings!$B$11"
S_UPTO = "Settings!$B$16"
S_FX, S_FXAVG = "Settings!$B$27:$B$38", "Settings!$B$39"
S_CHAN = "Settings!$A$20:$C$23"
ENDED_FIRST, ENDED_N = 44, 10
LOC_FIRST, LOC_N, MKT_FIRST, MKT_N = 59, 60, 59, 40
S_LOC = f"Settings!$A${LOC_FIRST}:$B${LOC_FIRST + LOC_N - 1}"

# Calc cells
CM_HDR, CM_DATE, CM_END, CM_CAMP, CM_SPEND, CM_CLK, CM_CONV = (f"Calc!$C${r}" for r in range(64, 71))
CG_HDR, CG_CAMP, CG_DAY, CG_COST, CG_CLK, CG_CONV, CG_CUR = (f"Calc!$C${r}" for r in range(76, 83))
CK_FIRST, CK_LAST, CK_COUNT = 86, 95, "Calc!$C$97"
EN_FIRST = 100
MK0, TY0 = 113, 156                  # first rows of the market and type tables in Calc
TY_N = 15

MARKETS = [("EMEA – multi-country", "EMEA"), ("Western Europe – multi-country", "EMEA"), ("UK", "EMEA"), ("France", "EMEA"),
           ("Germany", "EMEA"), ("Spain", "EMEA"), ("Italy", "EMEA"), ("Middle East", "EMEA"), ("US – national", "Americas"),
           ("US & Canada", "Americas"), ("California", "Americas"), ("US East Coast", "Americas"), ("US South & Central", "Americas"),
           ("New York", "Americas"), ("New Jersey", "Americas"), ("Florida", "Americas"), ("Texas", "Americas"), ("Arizona", "Americas"),
           ("Worldwide", "Global"), ("Not specified", "Not specified"), ("No location found", "Not specified")]
LOCATIONS = [("EMEA", "EMEA – multi-country"), ("Global EMEA", "EMEA – multi-country"), ("Western-Europe", "Western Europe – multi-country"),
             ("UK", "UK"), ("FR", "France"), ("DE", "Germany"), ("ES", "Spain"), ("IT", "Italy"), ("Middle-East", "Middle East"),
             ("SA", "Middle East"), ("US", "US – national"), ("Global US", "US – national"), ("USCA", "US & Canada"), ("NA", "US & Canada"),
             ("California", "California"), ("US-California", "California"), ("US-CA", "California"), ("US-SV", "California"),
             ("US-EastCoast", "US East Coast"), ("US-East-Coast", "US East Coast"), ("US-Middle-South", "US South & Central"),
             ("US-South-Central", "US South & Central"), ("New York", "New York"), ("New Jersey", "New Jersey"), ("Florida", "Florida"),
             ("FL", "Florida"), ("Texas", "Texas"), ("TX", "Texas"), ("Arizona", "Arizona"), ("WW", "Worldwide"), ("All", "Worldwide"),
             ("US-UK-FR-IT", "Worldwide"),
             ("CFA | Amazon US batch 1", "US – national"), ("YT | PSS | US | Pepsi Campaign", "US – national"), ("Test 1", "Not specified")]
TYPES = ["Meta – lead ads, prospecting", "Meta – lead ads, retargeting", "Meta – traffic", "Meta – other",
         "Google – Search, non-brand", "Google – Search, brand", "Google – Search, coworking", "Google – Performance Max",
         "Google – YouTube video", "Google – Demand Gen / YouTube reach", "Google – other", "ChatGPT Ads", "LinkedIn Ads"]
ENDED = [("FR_Alibaba Campaign", "Run by PnP's internal team; last spend 5 Oct 2026."),
         ("Test 1", "ChatGPT Ads 10-day test, 23 Sep – 2 Oct 2026.")]
OTHER_ROWS = [(datetime.date(2026, 9, 23), "ChatGPT Ads", "Test 1", 229.56, 43, 0, "Yes",
               "Total for the 10-day test, 23 Sep – 2 Oct 2026 (4,021 impressions). One row, so it counts in September but not in the weekly figures.")]

# the location table must cover the same codes as campaign_map (used for the checks in Python)
_codes = {k.upper(): m for k, m in LOCATIONS}
assert all(_codes.get(k) == m for k, (m, _) in CM.GEO.items()), "LOCATIONS out of step with campaign_map.GEO"
assert all(_codes.get(k.upper()) == m for k, (m, _) in CM.OVERRIDE.items()), "LOCATIONS out of step with campaign_map.OVERRIDE"
assert set(m for _, m in LOCATIONS) <= set(m for m, _ in MARKETS)


def DR(col):
    return f"Data!${col}$2:${col}${D_LAST}"


DCH, DDATE, DCAMP, DUSD, DMKT, DTYPE, DKIND = (DR(c) for c in "ABCDEFG")


def dsum(lo, hi, *crit, day=False):
    """USD spend in Data between two dates (inclusive), with extra (range, value) criteria. day=True skips 'Total' rows."""
    s = f'SUMIFS({DUSD},{DDATE},">="&{lo},{DDATE},"<="&{hi}'
    for r_, v in crit:
        s += f",{r_},{v}"
    return s + (f',{DKIND},"Day"' if day else "") + ")"


def ch(name):
    return (DCH, f'"{name}"')


def xsum(X, valcol, datecol, lo, hi):
    """Sum of an export column (as billed / as reported) between two dates, straight from the export tab."""
    v, d = f"INDEX({X},0,{valcol})", f"INDEX({X},0,{datecol})"
    return f'SUMIFS({v},{d},">="&{lo},{d},"<="&{hi})'


def counts(row):
    return f'(Settings!$C${row}="Yes")'


def USD(x):
    return f'"$"&TEXT({x},"#,##0")'


# ---------------------------------------------------------------------------------------------
def build(out, meta_rows, google_rows, agency_weeks=(), agency_totals=(), sources=()):
    wb = Workbook()
    names = ["Dashboard", "Update", "Weekly", "Monthly", "By location & type", "Meta export", "Google export",
             "Other channels", "Settings", "Agency reports", "Data", "Calc"]
    ws = {n: (wb.active if i == 0 else wb.create_sheet(n)) for i, n in enumerate(names)}
    ws["Dashboard"].title = "Dashboard"
    colors = {"Dashboard": NAVY, "Update": "1BAF7A", "Weekly": "2A78D6", "Monthly": "2A78D6", "By location & type": "2A78D6",
              "Meta export": "BF9000", "Google export": "BF9000", "Other channels": "BF9000", "Settings": "BF9000",
              "Agency reports": "7F7F7F", "Data": "7F7F7F", "Calc": "7F7F7F"}
    for n, w in ws.items():
        w.sheet_properties.tabColor = colors[n]
    notes = {w["start"]: w.get("notes") for w in agency_weeks}
    settings(ws["Settings"])
    export_tab(ws["Meta export"], meta_rows, META_CAP, "Campaign name")
    export_tab(ws["Google export"], google_rows, GOOGLE_CAP, "Cost")
    other_channels(ws["Other channels"])
    data_tab(ws["Data"])
    agency_tab(ws["Agency reports"], agency_weeks, agency_totals)
    calc(ws["Calc"])
    monthly(ws["Monthly"])
    weekly(ws["Weekly"], notes)
    by_location(ws["By location & type"])
    dashboard(ws["Dashboard"])
    update_tab(ws["Update"], sources)
    ws["Data"].sheet_state = "hidden"
    ws["Calc"].sheet_state = "hidden"
    wb.save(out)


# ---------------------------------------------------------------------------------------------
def settings(s):
    widths(s, {"A": 44, "B": 30, "C": 16, "D": 30, "E": 16, "F": 40})
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
    cell(s, "A9", "Budget status", bold=True)
    cell(s, "B9", "Confirmed by Tereza on 13 Oct 2026: $300k for 2026 (originally $350k). We can go up to $320k, ideally not more.",
         fill=INPUT, color=BLUE_T, wrap=True)
    s.merge_cells("B9:F9"); s.row_dimensions[9].height = 30
    cell(s, "A10", "Budget period (calculated)", bold=True)
    cell(s, "B10", "=DATE(B5,1,1)", DATE_F, align="center")
    cell(s, "C10", "=DATE(B5,12,31)", DATE_F, align="center")
    cell(s, "A11", "Week 1 starts on (calculated)", bold=True)
    cell(s, "B11", "=B10-WEEKDAY(B10,2)+1", DATE_F, align="center")
    note(s, "D11", "Weeks run Monday to Sunday.")

    section(s, "A13", "DATA DATE", "ABCDEF")
    cell(s, "A14", "Data up to – automatic", bold=True)
    cell(s, "B14", "=Calc!C52", DATE_F, align="center")
    note(s, "D14", "The last day in both exports (the earlier one if they differ).")
    cell(s, "A15", "Data up to – set by hand (normally empty)", bold=True)
    cell(s, "B15", None, DATE_F, fill=INPUT, color=BLUE_T, align="center")
    note(s, "D15", "Only to report up to an earlier day. Clear it afterwards.")
    cell(s, "A16", "Data up to – used everywhere", bold=True)
    cell(s, "B16", '=IF(B15<>"",B15,B14)', DATE_F, bold=True, align="center")

    section(s, "A18", "CHANNELS", "ABCDEF")
    header(s, 19, 1, ["Channel", "Billing currency", "Counts toward the budget?", "Note", "", ""])
    s.merge_cells("D19:F19")
    for name, r, cur, cnt, nt in CHANNELS:
        cell(s, f"A{r}", name, bold=True)
        cell(s, f"B{r}", cur, fill=INPUT, color=BLUE_T, align="center")
        cell(s, f"C{r}", cnt, fill=INPUT, color=BLUE_T, align="center")
        cell(s, f"D{r}", nt, size=9, color=INK2, wrap=True)
        s.merge_cells(f"D{r}:F{r}")

    section(s, "A25", "EXCHANGE RATE – EUR TO USD (Google Ads and ChatGPT Ads bill in EUR)", "ABCDEF")
    header(s, 26, 1, ["Month", "1 EUR = ? USD", "Source", "", "", ""])
    s.merge_cells("C26:F26")
    for i in range(12):
        r = 27 + i
        cell(s, f"A{r}", f"=DATE($B$5,{i + 1},1)", MON_F, bold=True)
        cell(s, f"B{r}", FX_RATE, "0.0000", fill=INPUT, color=BLUE_T, align="center")
        cell(s, f"C{r}", FX_SOURCE if i == 0 else "Same as above", size=8, color=INK2, fill=INPUT)
        s.merge_cells(f"C{r}:F{r}")
    cell(s, "A39", "Average", bold=True, fill=TOTAL)
    cell(s, "B39", "=AVERAGE(B27:B38)", "0.0000", bold=True, fill=TOTAL, align="center")

    section(s, "A41", "ENDED CAMPAIGNS – left out of the current pace", "ABCDEF")
    note(s, "A42", "When a campaign stops for good, add its name here exactly as in the export. Its spend still counts in 'spent so far', "
                   "but the forecast stops counting it.")
    header(s, 43, 1, ["Campaign name (exactly as in the export)", "Channel (automatic)", "Found in the data?",
                      "Spent in the last 3 full weeks (USD)", "Note", ""])
    s.merge_cells("E43:F43")
    for k in range(ENDED_N):
        r = ENDED_FIRST + k
        nm, nt = ENDED[k] if k < len(ENDED) else (None, None)
        cell(s, f"A{r}", nm, fill=INPUT, color=BLUE_T)
        cell(s, f"B{r}", f"=Calc!C{EN_FIRST + k}", align="center")
        cell(s, f"C{r}", f"=Calc!D{EN_FIRST + k}", align="center")
        cell(s, f"D{r}", f"=Calc!E{EN_FIRST + k}", AMT)
        cell(s, f"E{r}", nt, size=9, fill=INPUT, color=BLUE_T, wrap=True)
        s.merge_cells(f"E{r}:F{r}")
    s.conditional_formatting.add(f"C{ENDED_FIRST}:C{ENDED_FIRST + ENDED_N - 1}",
                                 FormulaRule(formula=[f'C{ENDED_FIRST}="No"'], font=font(bold=True, color=RED)))

    section(s, "A55", "LOCATIONS – how campaign names map to markets and regions", "ABCDEF")
    note(s, "A56", "The tracker reads the location code at the start of each campaign name: 'Geo:XX_…', 'PNP_XX_…', or the first word "
                   "before '_' or '|' (e.g. 'Texas_EN_…', 'WW | …'). Capital letters don't matter.")
    note(s, "A57", "A new code → add it on the left. No code in the name → put the full campaign name on the left instead (like 'Test 1'). "
                   "A new market → also add it on the right with its region.")
    header(s, 58, 1, ["Code, or full campaign name", "Market"])
    header(s, 58, 4, ["Market", "Region"])
    for k in range(LOC_N):
        r = LOC_FIRST + k
        key, mk = LOCATIONS[k] if k < len(LOCATIONS) else (None, None)
        cell(s, f"A{r}", key, fill=INPUT, color=BLUE_T)
        cell(s, f"B{r}", mk, fill=INPUT, color=BLUE_T)
    for k in range(MKT_N):
        r = MKT_FIRST + k
        mk, rg = MARKETS[k] if k < len(MARKETS) else (None, None)
        cell(s, f"D{r}", mk, fill=INPUT, color=BLUE_T)
        cell(s, f"E{r}", rg, fill=INPUT, color=BLUE_T, align="center")
    note(s, f"D{MKT_FIRST + len(MARKETS)}", "Germany (DE) and Spain (ES) are set up for future campaigns.")
    tr = LOC_FIRST + LOC_N + 2
    section(s, f"A{tr}", "CAMPAIGN TYPES – set from the campaign name (the first rule that matches)", "ABCDEF")
    for i, t in enumerate([
        "Meta: 'retargeting' → lead ads, retargeting · 'Objective:lead' → lead ads, prospecting · 'traffic' or 'Alibaba' → traffic · anything else → other.",
        "Google Ads: 'PMax' → Performance Max · 'DemandGen', 'Universities', or a name starting 'Global' or 'YT |' → Demand Gen / YouTube reach · "
        "'YouTube' → YouTube video · 'Brand' (not 'Non-brand') → Search, brand · 'Coworking' → Search, coworking · 'Search' → Search, non-brand · "
        "anything else → other.",
        "ChatGPT Ads and LinkedIn Ads: the channel name.",
    ]):
        cell(s, f"A{tr + 1 + i}", t, size=9, color=INK2, border=False, wrap=True)
        s.merge_cells(f"A{tr + 1 + i}:F{tr + 1 + i}")
        s.row_dimensions[tr + 1 + i].height = 26 if len(t) > 150 else 15

    dv = DataValidation(type="list", formula1='"USD,EUR"', allow_blank=False); s.add_data_validation(dv); dv.add("B20:B23")
    dv2 = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False); s.add_data_validation(dv2); dv2.add("C20:C23")
    dv3 = DataValidation(type="list", formula1=f"$D${MKT_FIRST}:$D${MKT_FIRST + MKT_N - 1}", allow_blank=True)
    s.add_data_validation(dv3); dv3.add(f"B{LOC_FIRST}:B{LOC_FIRST + LOC_N - 1}")
    dv4 = DataValidation(type="list", formula1='"' + ",".join(REGIONS) + '"', allow_blank=True)
    s.add_data_validation(dv4); dv4.add(f"E{MKT_FIRST}:E{MKT_FIRST + MKT_N - 1}")
    s.freeze_panes = "A4"


# ---------------------------------------------------------------------------------------------
def export_tab(w, rows, cap, key):
    """The export exactly as imported (header found by `key`), plus a formatted empty cell far below so the grid stays big."""
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            if v is None:
                continue
            c = w.cell(i + 1, j + 1, v)
            if isinstance(v, datetime.date):
                c.number_format = "yyyy-mm-dd"
    hdr = next(i for i, r in enumerate(rows) if key in r) + 1
    ncol = len(rows[hdr - 1])
    for j in range(1, ncol + 1):
        c = w.cell(hdr, j)
        c.font = Font(name="Arial", size=10, bold=True)
        c.fill = PatternFill("solid", fgColor=INPUT)
        c.alignment = Alignment(wrap_text=True, vertical="center")
        w.column_dimensions[L(j)].width = 14
    w.column_dimensions[L(rows[hdr - 1].index("Campaign name" if key == "Campaign name" else "Campaign") + 1)].width = 52
    w.row_dimensions[hdr].height = 30
    w.freeze_panes = f"A{hdr + 1}"
    w.cell(cap + 5000, 1).fill = PatternFill("solid", fgColor=WHITE)


# ---------------------------------------------------------------------------------------------
def other_channels(o):
    title(o, "A1", "Other channels – ChatGPT Ads and LinkedIn Ads (typed by hand)",
          "Only when these channels run. One row per campaign per day, or per week (date = the Monday). Spend exactly as billed – "
          "the tracker converts EUR to USD. Yellow = typed by you; white = automatic.", "A2")
    header(o, 4, 1, ["Date", "Channel", "Campaign name", "Spend (as billed)", "Currency (automatic)", "Clicks", "Conversions",
                     "Total for more than a week?", "Note", "Spend in USD (automatic)"], height=42)
    for k in range(OTHER_CAP):
        r = OC_FIRST + k
        v = OTHER_ROWS[k] if k < len(OTHER_ROWS) else (None,) * 8
        d, chn, camp, sp, clk, conv, tot, nt = v
        cell(o, f"A{r}", d, DATE_F, fill=INPUT, color=BLUE_T, align="center")
        cell(o, f"B{r}", chn, fill=INPUT, color=BLUE_T)
        cell(o, f"C{r}", camp, fill=INPUT, color=BLUE_T)
        cell(o, f"D{r}", sp, AMT2, fill=INPUT, color=BLUE_T)
        cell(o, f"E{r}", f'=IF(B{r}="","",IFERROR(VLOOKUP(B{r},{S_CHAN},2,0),"?"))', align="center", size=9)
        cell(o, f"F{r}", clk, "#,##0", fill=INPUT, color=BLUE_T)
        cell(o, f"G{r}", conv, "#,##0", fill=INPUT, color=BLUE_T)
        cell(o, f"H{r}", tot, fill=INPUT, color=BLUE_T, align="center")
        cell(o, f"I{r}", nt, size=8, fill=INPUT, color=BLUE_T, wrap=True)
        cell(o, f"J{r}", f'=IF(OR(A{r}="",D{r}=""),"",D{r}*IF(E{r}="USD",1,INDEX({S_FX},MONTH(A{r}))))', AMT2)
        if nt:
            o.row_dimensions[r].height = 30
    last = OC_FIRST + OTHER_CAP - 1
    dv = DataValidation(type="list", formula1='"ChatGPT Ads,LinkedIn Ads"', allow_blank=True); o.add_data_validation(dv); dv.add(f"B{OC_FIRST}:B{last}")
    dv2 = DataValidation(type="list", formula1='"Yes"', allow_blank=True); o.add_data_validation(dv2); dv2.add(f"H{OC_FIRST}:H{last}")
    note(o, "A3", "'Total for more than a week?' = Yes: the row is a total (like the ChatGPT test) – it counts in its month, not in the weekly figures.")
    o.freeze_panes = f"A{OC_FIRST}"
    widths(o, {"A": 13, "B": 14, "C": 40, "D": 14, "E": 12, "F": 10, "G": 12, "H": 14, "I": 60, "J": 14})


# ---------------------------------------------------------------------------------------------
def _code(c):
    return (f'IF(LEFT({c},4)="Geo:",MID({c},5,FIND("_",{c}&"_",5)-5),IF(LEFT({c},4)="PNP_",MID({c},5,FIND("_",{c}&"_",5)-5),'
            f'TRIM(LEFT({c},FIND("_",SUBSTITUTE({c},"|","_")&"_")-1))))')


def _market(r):
    return f'=IF(D{r}=0,"",IFERROR(VLOOKUP(C{r},{S_LOC},2,0),IFERROR(VLOOKUP({_code(f"C{r}")},{S_LOC},2,0),"No location found")))'


def _has(word, r):
    return f'ISNUMBER(SEARCH("{word}",C{r}))'


def _meta_type(r):
    return (f'=IF(D{r}=0,"",IF({_has("retargeting", r)},"Meta – lead ads, retargeting",IF({_has("objective:lead", r)},"Meta – lead ads, prospecting",'
            f'IF(OR({_has("traffic", r)},{_has("alibaba", r)}),"Meta – traffic","Meta – other"))))')


def _google_type(r):
    return (f'=IF(D{r}=0,"",IF({_has("pmax", r)},"Google – Performance Max",'
            f'IF(OR({_has("demandgen", r)},LEFT(C{r},6)="global",LEFT(C{r},4)="yt |",{_has("universities", r)}),"Google – Demand Gen / YouTube reach",'
            f'IF({_has("youtube", r)},"Google – YouTube video",IF(AND({_has("brand", r)},NOT({_has("non-brand", r)})),"Google – Search, brand",'
            f'IF({_has("coworking", r)},"Google – Search, coworking",IF({_has("search", r)},"Google – Search, non-brand","Google – other")))))))')


def data_tab(d):
    for j, h in enumerate(["Channel", "Date", "Campaign", "Spend (USD)", "Market", "Type", "Row covers"]):
        c = d.cell(1, j + 1, h)
        c.font = Font(name="Arial", size=10, bold=True)
    d["I1"] = (f"Formulas only – don't edit. Rows {D_META0}–{D_GOOG0 - 1} read 'Meta export' rows 1–{META_CAP}; rows {D_GOOG0}–{D_OTH0 - 1} read "
               f"'Google export' rows 1–{GOOGLE_CAP}; rows {D_OTH0}–{D_LAST} read 'Other channels' rows {OC_FIRST}–{OC_FIRST + OTHER_CAP - 1}.")
    for X, cap, r0, chname, srow, cdate, ccamp, cspend, typ in (
            (MX, META_CAP, D_META0, "Meta", 20, CM_DATE, CM_CAMP, CM_SPEND, _meta_type),
            (GX, GOOGLE_CAP, D_GOOG0, "Google Ads", 21, CG_DAY, CG_CAMP, CG_COST, _google_type)):
        for i in range(1, cap + 1):
            r = r0 + i - 1
            x = f"INDEX({X},{i},{cdate})"
            d.cell(r, 1, chname)
            d.cell(r, 2, f'=IFERROR(IF(ISNUMBER({x}),{x},DATEVALUE({x})),"")')
            d.cell(r, 3, f'=IF(B{r}="","",INDEX({X},{i},{ccamp})&"")')
            d.cell(r, 4, f'=IF(B{r}="",0,IFERROR(INDEX({X},{i},{cspend})*1,0)*IF(Settings!$B${srow}="USD",1,INDEX({S_FX},MONTH(B{r}))))')
            d.cell(r, 5, _market(r))
            d.cell(r, 6, typ(r))
            d.cell(r, 7, "Day")
    for j in range(1, OTHER_CAP + 1):
        r = D_OTH0 + j - 1
        d.cell(r, 1, f'=INDEX({OCR},{j},2)&""')
        d.cell(r, 2, f'=IF(AND(ISNUMBER(INDEX({OCR},{j},1)),A{r}<>""),INDEX({OCR},{j},1),"")')
        d.cell(r, 3, f'=IF(B{r}="","",INDEX({OCR},{j},3)&"")')
        d.cell(r, 4, f'=IF(B{r}="",0,IFERROR(N(INDEX({OCR},{j},4))*IF(VLOOKUP(A{r},{S_CHAN},2,0)="USD",1,INDEX({S_FX},MONTH(B{r}))),0))')
        d.cell(r, 5, _market(r))
        d.cell(r, 6, f'=IF(D{r}=0,"",A{r})')
        d.cell(r, 7, f'=IF(INDEX({OCR},{j},8)="Yes","Total","Day")')
    widths(d, {"A": 12, "B": 11, "C": 50, "D": 12, "E": 26, "F": 32, "G": 10})


# ---------------------------------------------------------------------------------------------
def agency_tab(a, weeks, totals):
    title(a, "A1", "Agency weekly reports (Notion) – as written, checked against the platforms", None)
    note(a, "A2", "Source: the agency's weekly reports in Notion, read on 13 Oct 2026 (nothing edited). Spend, leads and CPL are copied as the agency wrote them; "
                  "lead definitions change over the year, so leads and CPL are not comparable week to week. The official spend numbers are the platform exports.")
    section(a, "A4", "WEEK BY WEEK", "ABCDEFGHIJKLMNOPQR")
    hdr = ["Week starts", "Week ends", "Meta spend (agency, $)", "Meta leads (agency)", "Meta lead definition", "Meta CPL (agency)",
           "Google spend (agency, as written)", "Google currency (as written)", "Google leads (agency)", "Google CPL (agency)",
           "Issues found", "What the agency did or recommended", "Meta – platform (USD)", "Meta – platform excl. FR_Alibaba (USD)",
           "Meta: agency − platform excl. FR_Alibaba", "Google – platform (EUR)", "Google: agency ÷ platform", "What the Google difference looks like", "Chart label"]
    header(a, 5, 1, hdr, height=54)
    first = 6
    fr = (DCAMP, '"FR_Alibaba Campaign"')
    for i, w in enumerate(weeks):
        r = first + i
        cell(a, f"A{r}", w["start"], DATE_F)
        cell(a, f"B{r}", w["end"], DATE_F)
        cell(a, f"C{r}", w.get("meta_spend"), AMT2, color=BLUE_T)
        cell(a, f"D{r}", w.get("meta_leads"), "#,##0.##")
        cell(a, f"E{r}", w.get("meta_def"), size=8, wrap=True)
        cell(a, f"F{r}", w.get("meta_cpl"), size=9, align="right")
        cell(a, f"G{r}", w.get("google_spend"), AMT2, color=BLUE_T)
        cell(a, f"H{r}", w.get("google_cur"), align="center", size=9)
        cell(a, f"I{r}", w.get("google_leads"), "#,##0.##")
        cell(a, f"J{r}", w.get("google_cpl"), size=9, align="right")
        cell(a, f"K{r}", w.get("flags"), size=8, wrap=True, color=RED if w.get("flags") else INK)
        cell(a, f"L{r}", w.get("notes"), size=8, wrap=True)
        cell(a, f"M{r}", "=" + dsum(f"$A{r}", f"$B{r}", ch("Meta"), day=True), AMT2)
        cell(a, f"N{r}", f"=M{r}-" + dsum(f"$A{r}", f"$B{r}", ch("Meta"), fr, day=True), AMT2)
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
    note(a, f"A{last + 1}", "Platform columns come from the platform exports (daily rows). From W/C 7 Sep the agency left FR_Alibaba out of its Meta figures, "
                            "so compare the agency's Meta figure with the 'excl. FR_Alibaba' column.")
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
        cell(a, f"F{r}", "=" + dsum(dlo, dhi, ch("Meta")) if has_m else None, AMT2)
        cell(a, f"G{r}", "=" + xsum(GX, CG_COST, CG_DAY, dlo, dhi) if has_g else None, AMT2)
        parts = ([dsum(dlo, dhi, ch("Meta"))] if has_m else []) + ([dsum(dlo, dhi, ch("Google Ads"))] if has_g else [])
        cell(a, f"H{r}", "=" + "+".join(parts), AMT2, bold=True)
        cell(a, f"I{r}", f"=E{r}-H{r}", AMT2, bold=True)
        cell(a, f"J{r}", f'=IF(H{r}=0,"",E{r}/H{r}-1)', '+0%;-0%;0%', align="center", size=9)
        cell(a, f"K{r}", t["note"], size=8, wrap=True)
        for col in "LMNO":
            cell(a, f"{col}{r}", None)
        a.row_dimensions[r].height = 42
    a.conditional_formatting.add(f"I{top + 2}:J{top + 1 + len(totals)}",
                                 FormulaRule(formula=[f"AND(ISNUMBER($I{top + 2}),ABS($I{top + 2})>100)"], font=font(bold=True, color=RED)))
    nr = top + 2 + len(totals)
    note(a, f"A{nr}", "Platform totals: Meta in USD as billed; Google in EUR as billed and converted with the Settings rate. "
                      "The agency's July report converted Google with \"£1 = $1.28\" although the Google Ads account is in euros.")
    a.freeze_panes = "C6"
    widths(a, {"A": 12, "B": 12, "C": 12, "D": 10, "E": 16, "F": 12, "G": 13, "H": 12, "I": 12, "J": 10, "K": 34, "L": 52,
               "M": 13, "N": 13, "O": 12, "P": 13, "Q": 10, "R": 26, "S": 8})
    ctop = nr + 3
    section(a, f"A{ctop}", "GOOGLE ADS: WHAT THE AGENCY REPORTED vs. THE PLATFORM, WEEK BY WEEK", "ABCDEFGHIJ")
    c = BarChart(); c.type = "col"; c.grouping = "clustered"; c.gapWidth = 40
    c.add_data(Reference(a, min_col=7, min_row=5, max_row=last), titles_from_data=True)
    c.add_data(Reference(a, min_col=16, min_row=5, max_row=last), titles_from_data=True)
    c.set_categories(Reference(a, min_col=19, min_row=first, max_row=last))
    style_bar(c, [CH_COLORS["Google Ads"], SLATE])
    c.width, c.height = 30, 9
    a.add_chart(c, f"A{ctop + 1}")
    note(a, f"A{ctop + 19}", "Bars that match = the agency's figure was the platform's euros (often labelled $). "
                             "×2 = doubled week; ≈ ×1.15 = converted to dollars; shorter orange bars = lower than the platform.")


# ---------------------------------------------------------------------------------------------
def calc(k):
    title(k, "A1", "Calculations behind the Dashboard and the checks – hidden, don't edit", "Every Dashboard number can be traced here.", "A2")
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
        (15, "Last 3 full weeks start", "=C13-20", DATE_F),
        (16, "Weeks left", "=C8/7", "0.00"),
        (17, "Days in last full month", "=C10-C11+1", "0"),
    ]
    for r, lab, f, fmt in items:
        cell(k, f"B{r}", lab)
        cell(k, f"C{r}", f, fmt, align="center")
    header(k, 19, 2, ["Channel", "Counts toward budget?", "Spent to date", "Spent last full month", "Spent last 3 full months",
                      "Spent last full week", "Spent last 3 full weeks", "Share of spend"])
    for i, (name, srow, *_) in enumerate(CHANNELS):
        r = 20 + i
        cell(k, f"B{r}", name, bold=True)
        cell(k, f"C{r}", f"=Settings!C{srow}", align="center")
        cell(k, f"D{r}", "=" + dsum("$C$4", "MIN($C$3,$C$5)", ch(name)), AMT)
        cell(k, f"E{r}", "=" + dsum("$C$11", "$C$10", ch(name)), AMT)
        cell(k, f"F{r}", "=" + dsum("$C$12", "$C$10", ch(name)), AMT)
        cell(k, f"G{r}", "=" + dsum("$C$14", "$C$13", ch(name), day=True), AMT)
        cell(k, f"H{r}", "=" + dsum("$C$15", "$C$13", ch(name), day=True), AMT)
        cell(k, f"I{r}", f'=IF($D$25=0,"",D{r}/$D$25)', "0.0%")
    cell(k, "B24", "Total – counts toward budget", bold=True, fill=TOTAL)
    cell(k, "B25", "Total – all channels", bold=True, fill=TOTAL)
    cell(k, "C24", "", fill=TOTAL); cell(k, "C25", "", fill=TOTAL)
    for col in "DEFGH":
        cell(k, f"{col}24", f'=SUMIFS({col}20:{col}23,$C$20:$C$23,"Yes")', AMT, bold=True, fill=TOTAL)
        cell(k, f"{col}25", f"=SUM({col}20:{col}23)", AMT, bold=True, fill=TOTAL)
    cell(k, "I24", '=IF($D$25=0,"",D24/$D$25)', "0.0%", fill=TOTAL); cell(k, "I25", "", fill=TOTAL)
    rows = [
        (27, "Budget", f"={S_BUDGET}", AMT),
        (28, "Maximum (ideally not more)", f"={S_MAX}", AMT),
        (29, "Original budget", f"={S_ORIG}", AMT),
        (30, "Spent to date (budget channels)", "=D24", AMT),
        (31, "Left in the budget", "=C27-C30", AMT),
        (32, "Left up to the maximum", "=C28-C30", AMT),
        (33, "% of budget used", '=IF(C27=0,"",C30/C27)', "0.0%"),
        (34, "% of maximum used", '=IF(C28=0,"",C30/C28)', "0.0%"),
        (35, "Should have spent by now (budget spread evenly by day)", "=C27*C9", AMT),
        (36, "Ahead (+) / behind (−) that even pace", "=C30-C35", AMT),
        (37, "Weekly pace – last 3 full weeks, budget channels, without ended campaigns", "=(H24-C49)/3", AMT),
        (38, "Spent in the last 3 full weeks, budget channels, all campaigns", "=H24", AMT),
        (39, "Current weekly pace used", "=C37", AMT),
        (40, "Source of the current pace", '="the platform exports: last 3 full weeks ("&TEXT(C15,"d mmm")&" – "&TEXT(C13,"d mmm")&"), campaigns still running"', None),
        (41, "Ended campaigns on the Settings list", f'=COUNTIF(Settings!$A${ENDED_FIRST}:$A${ENDED_FIRST + ENDED_N - 1},"?*")', "0"),
        (42, "Forecast year-end at the current pace", "=C30+C39*C16", AMT),
        (43, "Allowed per week to land on the budget", "=IF(C16<=0,0,C31/C16)", AMT),
        (44, "Allowed per week to land on the maximum", "=IF(C16<=0,0,C32/C16)", AMT),
        (45, "Last full month (budget channels)", "=E24", AMT),
        (46, "All spend in the exports (any date)", f"=SUM({DUSD})", AMT),
        (47, "Forecast year-end at last month's pace", "=C30+E24/C17*C8", AMT),
        (48, "Last full week, budget channels", "=G24", AMT),
        (49, "Left out of the pace: ended campaigns' last 3 full weeks (budget channels)", f"=SUM(G{EN_FIRST}:G{EN_FIRST + ENDED_N - 1})", AMT),
    ]
    for r, lab, f, fmt in rows:
        cell(k, f"B{r}", lab)
        cell(k, f"C{r}", f, fmt)

    section(k, "B51", "EXPORTS", "BCDE")
    mb, gb = f"Data!$B${D_META0}:$B${D_GOOG0 - 1}", f"Data!$B${D_GOOG0}:$B${D_OTH0 - 1}"
    for r, lab, f, fmt in [
        (52, "Data up to – automatic (last day in both exports)", "=IF(AND(C53>0,C54>0),MIN(C53,C54),MAX(C53,C54))", DATE_F),
        (53, "Meta – last day in the export", f"=MAX({mb})", DATE_F),
        (54, "Google Ads – last day in the export", f"=MAX({gb})", DATE_F),
        (55, "Meta – first day", f"=MIN({mb})", DATE_F),
        (56, "Google Ads – first day", f"=MIN({gb})", DATE_F),
        (57, "Meta – rows read", f"=COUNT({mb})", "#,##0"),
        (58, "Google Ads – rows read", f"=COUNT({gb})", "#,##0"),
        (59, f"Meta – filled cells below row {META_CAP} (not read)", f"=COUNTA('Meta export'!$A${META_CAP + 1}:$AD${META_CAP + 4000})", "0"),
        (60, f"Google Ads – filled cells below row {GOOGLE_CAP} (not read)", f"=COUNTA('Google export'!$A${GOOGLE_CAP + 1}:$AD${GOOGLE_CAP + 4000})", "0"),
        (61, "Last Sunday (from today's date)", "=TODAY()-WEEKDAY(TODAY(),2)", DATE_F),
    ]:
        cell(k, f"B{r}", lab)
        cell(k, f"C{r}", f, fmt, align="center")

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

    section(k, "B63", "META EXPORT – COLUMNS FOUND (column number; 30 = not found)", "BCDE")
    for r, lab, f in [
        (64, "Header row", first_row_with("Meta export", "Campaign name")),
        (65, "Reporting starts (date)", find("Meta export", "$C$64", "Reporting starts")),
        (66, "Reporting ends", find("Meta export", "$C$64", "Reporting ends")),
        (67, "Campaign name", find("Meta export", "$C$64", "Campaign name")),
        (68, "Amount spent", find("Meta export", "$C$64", "Amount spent (USD)", "Amount spent (EUR)", "Amount spent")),
        (69, "Clicks (unique link clicks, else link clicks)", find("Meta export", "$C$64", "Unique link clicks", "Link clicks")),
        (70, "Conversions (website registrations completed)", find("Meta export", "$C$64", "Website registrations completed")),
        (71, "Spend column header", f"=IF(OR(C64=0,C68={NF}),\"\",INDEX('Meta export'!$A$1:$AD$5,C64,C68)&\"\")"),
        (72, "Currency in the spend header", '=IFERROR(MID(C71,FIND("(",C71)+1,3),"")'),
        (73, "Split by day? (first row starts and ends on the same day)",
         f"=IF(OR(C66={NF},C57=0),TRUE,INDEX({MX},C64+1,C65)=INDEX({MX},C64+1,C66))"),
    ]:
        cell(k, f"B{r}", lab)
        cell(k, f"C{r}", f, align="center")
    section(k, "B75", "GOOGLE ADS EXPORT – COLUMNS FOUND (column number; 30 = not found)", "BCDE")
    for r, lab, f in [
        (76, "Header row", first_row_with("Google export", "Cost")),
        (77, "Campaign", find("Google export", "$C$76", "Campaign")),
        (78, "Day (date)", find("Google export", "$C$76", "Day")),
        (79, "Cost", find("Google export", "$C$76", "Cost")),
        (80, "Clicks", find("Google export", "$C$76", "Clicks")),
        (81, "Conversions", find("Google export", "$C$76", "Conversions")),
        (82, "Currency code", find("Google export", "$C$76", "Currency code")),
        (83, "Currency (first data row)", f'=IF(OR(C76=0,C82={NF},C58=0),"",INDEX({GX},C76+1,C82)&"")'),
    ]:
        cell(k, f"B{r}", lab)
        cell(k, f"C{r}", f, align="center")

    section(k, "B85", "CHECKS (shown on the Update tab)", "BCDEF")
    nolocation = f'SUMIFS({DUSD},{DMKT},"No location found")'
    year_total, mk_total = "SUM(Monthly!$G$5:$G$16)", f"SUM($P${MK0}:$P${MK0 + MKT_N - 1})"
    oc = lambda col: f"'Other channels'!${col}${OC_FIRST}:${col}${OC_FIRST + OTHER_CAP - 1}"
    checks = [
        ("Meta export read correctly",
         f'=IF(OR(C65={NF},C67={NF},C68={NF}),"⚠ Columns not found: "&IF(C65={NF},"Reporting starts · ","")&IF(C67={NF},"Campaign name · ","")&IF(C68={NF},"Amount spent",""),'
         f'IF(C57=0,"⚠ No rows with a date",IF(NOT(C73),"⚠ Not split by day",IF(C72<>Settings!$B$20,"⚠ Spend is in "&C72&", Settings says "&Settings!$B$20,'
         f'IF(COUNT(INDEX({MX},0,C65))=0,"⚠ Dates came in as text","✓ "&TEXT(C57,"#,##0")&" rows · "&TEXT(C55,"d mmm")&" – "&TEXT(C53,"d mmm"))))))'),
        ("Google Ads export read correctly",
         f'=IF(OR(C77={NF},C78={NF},C79={NF}),"⚠ Columns not found: "&IF(C77={NF},"Campaign · ","")&IF(C78={NF},"Day · ","")&IF(C79={NF},"Cost",""),'
         f'IF(C58=0,"⚠ No rows with a date",IF(AND(C82<>{NF},C83<>Settings!$B$21),"⚠ Cost is in "&C83&", Settings says "&Settings!$B$21,'
         f'IF(COUNT(INDEX({GX},0,C78))=0,"⚠ Dates came in as text","✓ "&TEXT(C58,"#,##0")&" rows · "&TEXT(C56,"d mmm")&" – "&TEXT(C54,"d mmm")))))'),
        ("Both exports end on the same day",
         '=IF(OR(C53=0,C54=0),"⚠ One export is empty",IF(C53=C54,"✓ Both end on "&TEXT(C53,"ddd d mmm"),"⚠ Meta ends "&TEXT(C53,"d mmm")&", Google Ads "&TEXT(C54,"d mmm")))'),
        ("The data includes last week",
         '=IF(C3>=C61,"✓ Data runs to "&TEXT(C3,"ddd d mmm"),"⚠ Data ends "&TEXT(C3,"d mmm")&" – last Sunday was "&TEXT(C61,"d mmm"))'),
        ("Every campaign has a market",
         f'=IF({nolocation}=0,"✓ All campaigns found on Settings → Locations","⚠ "&{USD(nolocation)}&" with no market. First: "&E90&" (code: "&F90&")")'),
        ("Every market has a region",
         f'=IF(ABS({year_total}-{mk_total})<1,"✓ All markets listed on Settings","⚠ "&{USD(year_total + "-" + mk_total)}&" is in a market missing from Settings → Markets")'),
        ("The exports fit in the tracker",
         f'=IF(C59+C60=0,"✓ Meta "&TEXT(C57,"#,##0")&" of {META_CAP:,} rows · Google "&TEXT(C58,"#,##0")&" of {GOOGLE_CAP:,}","⚠ An export is longer than the tracker reads")'),
        ("Spend looks right",
         '=IF(C30>2*C28,"⚠ Spend looks too high – numbers may have imported wrongly",IF(C30<=0,"⚠ No spend found","✓ "&' + USD("C30") + '&" spent this year"))'),
        ("Ended campaigns found in the data",
         f'=IF(COUNTIF(D{EN_FIRST}:D{EN_FIRST + ENDED_N - 1},"No")=0,"✓ "&C41&" on the list, all found","⚠ "&COUNTIF(D{EN_FIRST}:D{EN_FIRST + ENDED_N - 1},"No")&" name(s) not found – check the spelling on Settings")'),
        ("Other channels rows complete",
         f'=IF(COUNTIFS({oc("D")},"<>",{oc("B")},"")+COUNTIFS({oc("D")},"<>",{oc("A")},"")=0,"✓ Complete","⚠ A row has spend but no date or channel")'),
    ]
    for i, (lab, f) in enumerate(checks):
        r = CK_FIRST + i
        cell(k, f"B{r}", lab)
        cell(k, f"C{r}", f)
    cell(k, "D90", "First campaign with no market →")
    cell(k, "E90", f'=IFERROR(INDEX({DCAMP},MATCH("No location found",{DMKT},0)),"")')
    cell(k, "F90", f'=IF(E90="","",{_code("E90")})')
    cell(k, "B97", "Number of checks with ⚠", bold=True)
    cell(k, "C97", f'=COUNTIF(C{CK_FIRST}:C{CK_LAST},"⚠*")', "0", bold=True)

    section(k, "B99", "ENDED CAMPAIGNS (Settings list)", "BCDEFG")
    for i in range(ENDED_N):
        r, sr = EN_FIRST + i, ENDED_FIRST + i
        cell(k, f"B{r}", f'=IF(Settings!$A${sr}="","",Settings!$A${sr}&"")')
        cell(k, f"C{r}", f'=IF(B{r}="","",IFERROR(INDEX({DCH},MATCH(B{r},{DCAMP},0)),"–"))', align="center")
        cell(k, f"D{r}", f'=IF(B{r}="","",IF(C{r}="–","No","Yes"))', align="center")
        cell(k, f"E{r}", f'=IF(B{r}="","",' + dsum("$C$15", "$C$13", (DCAMP, f"B{r}"), day=True) + ")", AMT)
        cell(k, f"F{r}", f'=IF(OR(B{r}="",C{r}="–"),FALSE,IFERROR(VLOOKUP(C{r},{S_CHAN},3,0)="Yes",FALSE))', align="center")
        cell(k, f"G{r}", f"=IF(F{r},E{r},0)", AMT)

    def matrix(top, n, name_f, region_f, crit_rng, lab):
        section(k, f"B{top - 2}", lab, "BCDEFGHIJKLMNOPQR")
        header(k, top - 1, 2, ["Name", "Region"] + [f'=TEXT(DATE({S_YEAR},{m},1),"mmm")' for m in range(1, 13)] +
               ["Year total", "Sort key", "Sorted by spend"])
        for i in range(n):
            r = top + i
            cell(k, f"B{r}", name_f(i))
            cell(k, f"C{r}", region_f(i, r))
            for m in range(1, 13):
                cell(k, f"{L(3 + m)}{r}", f'=IF($B{r}="",0,SUMIFS({DUSD},{crit_rng},$B{r},{DDATE},">="&DATE({S_YEAR},{m},1),{DDATE},"<="&EOMONTH(DATE({S_YEAR},{m},1),0)))', AMT)
            cell(k, f"P{r}", f"=SUM(D{r}:O{r})", AMT)
            cell(k, f"Q{r}", f"=IF(P{r}>0,P{r}+(1000-ROW())/1000000,0)", "0.000000")
            big = f"LARGE($Q${top}:$Q${top + n - 1},{i + 1})"
            cell(k, f"R{r}", f'=IF({big}<=0,"",INDEX($B${top}:$B${top + n - 1},MATCH({big},$Q${top}:$Q${top + n - 1},0)))')

    matrix(MK0, MKT_N, lambda i: f"=Settings!$D${MKT_FIRST + i}&\"\"",
           lambda i, r: f'=IF(B{r}="","",Settings!$E${MKT_FIRST + i}&"")', DMKT, "MARKETS – USD BY MONTH (all channels)")
    matrix(TY0, TY_N, lambda i: TYPES[i] if i < len(TYPES) else None, lambda i, r: None, DTYPE, "CAMPAIGN TYPES – USD BY MONTH (all channels)")
    widths(k, {"A": 2, "B": 52, "C": 16, **{L(4 + i): 11 for i in range(12)}, "P": 12, "Q": 14, "R": 34})


# ---------------------------------------------------------------------------------------------
def monthly(m):
    title(m, "A1", "Monthly spend", None)
    cell(m, "A2", f'="Amounts in USD · Google Ads and ChatGPT Ads converted from EUR with the Settings rates · data up to "&TEXT({S_UPTO},"d mmm yyyy")',
         size=9, color=INK2, border=False, italic=True)
    cell(m, "T2", "Data up to", size=8, color=MUTED, border=False, align="right")
    cell(m, "U2", f"={S_UPTO}", DATE_F, size=8, color=MUTED, border=False)
    hdr = ["Month", "Quarter", "Meta", "Google Ads", "ChatGPT Ads", "LinkedIn Ads", "Total – all channels",
           "Counts toward budget", "Plan (budget spread evenly by day)", "Over (+) / under (−) plan",
           "Cumulative spend (budget channels)", "Cumulative plan", "Maximum", "% of budget used", "Status",
           "Meta as billed (USD)", "Google as billed (EUR)", "EUR → USD rate used", "Chart label"]
    header(m, 4, 1, hdr, height=42)
    for i in range(12):
        r = 5 + i
        cell(m, f"A{r}", f"=DATE({S_YEAR},{i + 1},1)", MON_F, bold=True)
        cell(m, f"B{r}", f'="Q"&ROUNDUP(MONTH(A{r})/3,0)', align="center")
        for j, (name, srow, *_) in enumerate(CHANNELS):
            cell(m, f"{L(3 + j)}{r}", "=" + dsum(f"$A{r}", f"EOMONTH($A{r},0)", ch(name)), AMT)
        cell(m, f"G{r}", f"=SUM(C{r}:F{r})", AMT, bold=True)
        cell(m, f"H{r}", "=" + "+".join(f"{L(3 + j)}{r}*{counts(srow)}" for j, (n, srow, *_) in enumerate(CHANNELS)), AMT)
        cell(m, f"I{r}", f"={S_BUDGET}*MAX(0,MIN(EOMONTH($A{r},0),{S_PEND})-MAX($A{r},{S_PSTART})+1)/({S_PEND}-{S_PSTART}+1)", AMT)
        cell(m, f"J{r}", f'=IF(EOMONTH($A{r},0)>{S_UPTO},"",H{r}-I{r})', AMT)
        cell(m, f"K{r}", f'=IF($A{r}>{S_UPTO},"",SUM($H$5:H{r}))', AMT)
        cell(m, f"L{r}", f"=SUM($I$5:I{r})", AMT)
        cell(m, f"M{r}", f"={S_MAX}", AMT, color=INK2)
        cell(m, f"N{r}", f'=IF(OR(K{r}="",{S_BUDGET}=0),"",K{r}/{S_BUDGET})', PCT, align="center")
        cell(m, f"O{r}", f'=IF(EOMONTH($A{r},0)<={S_UPTO},"Complete",IF($A{r}<={S_UPTO},"In progress","Not started"))', align="center", size=9)
        cell(m, f"P{r}", "=" + xsum(MX, CM_SPEND, CM_DATE, f"$A{r}", f"EOMONTH($A{r},0)"), AMT)
        cell(m, f"Q{r}", "=" + xsum(GX, CG_COST, CG_DAY, f"$A{r}", f"EOMONTH($A{r},0)"), AMT)
        cell(m, f"R{r}", f"=INDEX({S_FX},MONTH(A{r}))", "0.0000", align="center", size=9)
        cell(m, f"S{r}", f'=TEXT(A{r},"mmm")', size=8, color=MUTED, align="center")
    cell(m, "A17", "Total", bold=True, fill=TOTAL)
    cell(m, "B17", "", fill=TOTAL)
    for col in "CDEFGHIJPQ":
        cell(m, f"{col}17", f"=SUM({col}5:{col}16)", AMT, bold=True, fill=TOTAL)
    for col in "KLMNORS":
        cell(m, f"{col}17", "", fill=TOTAL)
    note(m, "A18", "Over/under plan is shown for complete months only. The plan spreads the annual budget evenly over the days of the year.")
    m.conditional_formatting.add("J5:J17", FormulaRule(formula=['AND(ISNUMBER(J5),J5>0)'], font=font(bold=True, color=RED)))
    m.conditional_formatting.add("A5:R16", FormulaRule(formula=['$A5>$U$2'], font=font(color=MUTED)))

    section(m, "A21", "CLICKS, CONVERSIONS AND COSTS – as reported by each platform", "ABCDEFGHIJKLMNO")
    groups = [("Meta", "C", lambda lo, hi: xsum(MX, CM_CLK, CM_DATE, lo, hi), lambda lo, hi: xsum(MX, CM_CONV, CM_DATE, lo, hi)),
              ("Google Ads", "D", lambda lo, hi: xsum(GX, CG_CLK, CG_DAY, lo, hi), lambda lo, hi: xsum(GX, CG_CONV, CG_DAY, lo, hi)),
              ("ChatGPT Ads", "E",
               lambda lo, hi: f"SUMIFS('Other channels'!$F$5:$F$304,'Other channels'!$B$5:$B$304,\"ChatGPT Ads\",'Other channels'!$A$5:$A$304,\">=\"&{lo},'Other channels'!$A$5:$A$304,\"<=\"&{hi})",
               lambda lo, hi: f"SUMIFS('Other channels'!$G$5:$G$304,'Other channels'!$B$5:$B$304,\"ChatGPT Ads\",'Other channels'!$A$5:$A$304,\">=\"&{lo},'Other channels'!$A$5:$A$304,\"<=\"&{hi})")]
    cell(m, "A22", "", fill=NAVY); cell(m, "A23", "Month", bold=True, color=WHITE, fill=NAVY, align="center")
    for g, (name, scol, fclk, fconv) in enumerate(groups):
        c0 = 2 + g * 4
        m.merge_cells(start_row=22, start_column=c0, end_row=22, end_column=c0 + 3)
        cell(m, f"{L(c0)}22", name, bold=True, color=WHITE, fill=NAVY, align="center")
        header(m, 23, c0, ["Clicks", "Conversions", "Cost per click", "Cost per conversion"])
    for i in range(12):
        r = 24 + i
        cell(m, f"A{r}", f"=A{5 + i}", MON_F, bold=True)
        lo, hi = f"$A{r}", f"EOMONTH($A{r},0)"
        for g, (name, scol, fclk, fconv) in enumerate(groups):
            c0 = 2 + g * 4
            cl, cv, cpc, cpl = L(c0), L(c0 + 1), L(c0 + 2), L(c0 + 3)
            cell(m, f"{cl}{r}", "=" + fclk(lo, hi), "#,##0")
            cell(m, f"{cv}{r}", "=" + fconv(lo, hi), "#,##0")
            cell(m, f"{cpc}{r}", f'=IF({cl}{r}=0,"",{scol}{5 + i}/{cl}{r})', AMT2)
            cell(m, f"{cpl}{r}", f'=IF({cv}{r}=0,"",{scol}{5 + i}/{cv}{r})', AMT2)
    cell(m, "A36", "Total", bold=True, fill=TOTAL)
    for g, (name, scol, *_) in enumerate(groups):
        c0 = 2 + g * 4
        cl, cv, cpc, cpl = L(c0), L(c0 + 1), L(c0 + 2), L(c0 + 3)
        cell(m, f"{cl}36", f"=SUM({cl}24:{cl}35)", "#,##0", bold=True, fill=TOTAL)
        cell(m, f"{cv}36", f"=SUM({cv}24:{cv}35)", "#,##0", bold=True, fill=TOTAL)
        cell(m, f"{cpc}36", f'=IF({cl}36=0,"",{scol}17/{cl}36)', AMT2, bold=True, fill=TOTAL)
        cell(m, f"{cpl}36", f'=IF({cv}36=0,"",{scol}17/{cv}36)', AMT2, bold=True, fill=TOTAL)
    note(m, "A37", "Conversions use each platform's own definition: Meta = 'Website registrations completed' (clicks = unique link clicks); "
                   "Google Ads = 'Conversions' (its primary conversion actions, which the agency changed during the year). "
                   "Compare each channel with itself, not with each other.")
    m.freeze_panes = "B5"
    widths(m, {"A": 11, "B": 8, **{c: 12 for c in "CDEFGHIJKLMNOPQ"}, "R": 10, "S": 8, "T": 10, "U": 12})


# ---------------------------------------------------------------------------------------------
def weekly(w, notes):
    title(w, "A1", "Weekly spend", None)
    cell(w, "A2", '="Weeks run Monday to Sunday · amounts in USD · from the platform exports. Yellow columns are typed by you."',
         size=9, color=INK2, border=False, italic=True)
    cell(w, "A3", "Data up to:", size=8, color=MUTED, border=False)
    cell(w, "C3", f"={S_UPTO}", DATE_F, size=8, color=MUTED, border=False)
    cell(w, "D3", "Last full week ends:", size=8, color=MUTED, border=False)
    cell(w, "F3", "=Calc!C13", DATE_F, size=8, color=MUTED, border=False)
    cell(w, "H3", "Notes marked 'Agency:' summarise the agency's weekly reports (until W/C 5 Oct). Add your own from W/C 12 Oct.",
         size=9, color=INK2, border=False, italic=True)
    hdr = ["Week", "Starts (Mon)", "Ends (Sun)", "Meta", "Google Ads", "ChatGPT Ads", "LinkedIn Ads", "Total – all channels",
           "Counts toward budget", "Plan (budget spread evenly by day)", "Over (+) / under (−) plan",
           "Meta conversions", "Meta cost per conversion", "Google conversions", "Google cost per conversion",
           "MQLs – paid social (HubSpot, optional)", "MQLs – paid search (HubSpot, optional)", "Notes – what happened this week", "Chart label"]
    header(w, 4, 1, hdr, height=54)
    for col in "PQR":
        w[f"{col}4"].fill = PatternFill("solid", fgColor=INPUT)
        w[f"{col}4"].font = font(9, True, INK)
    for i in range(53):
        r = 5 + i
        cell(w, f"A{r}", i + 1, "0", bold=True, align="center")
        cell(w, f"B{r}", f"={S_W1}+7*(A{r}-1)", DAY_F)
        cell(w, f"C{r}", f"=B{r}+6", DAY_F)
        for j, (name, *_) in enumerate(CHANNELS):
            cell(w, f"{L(4 + j)}{r}", "=" + dsum(f"$B{r}", f"$C{r}", ch(name), day=True), AMT)
        cell(w, f"H{r}", f"=SUM(D{r}:G{r})", AMT, bold=True)
        cell(w, f"I{r}", "=" + "+".join(f"{L(4 + j)}{r}*{counts(srow)}" for j, (n, srow, *_) in enumerate(CHANNELS)), AMT)
        cell(w, f"J{r}", f"={S_BUDGET}*MAX(0,MIN(C{r},{S_PEND})-MAX(B{r},{S_PSTART})+1)/({S_PEND}-{S_PSTART}+1)", AMT)
        cell(w, f"K{r}", f'=IF(OR(C{r}>$C$3,I{r}=0),"",I{r}-J{r})', AMT)
        cell(w, f"L{r}", "=" + xsum(MX, CM_CONV, CM_DATE, f"$B{r}", f"$C{r}"), "#,##0")
        cell(w, f"M{r}", f'=IF(L{r}=0,"",D{r}/L{r})', AMT2)
        cell(w, f"N{r}", "=" + xsum(GX, CG_CONV, CG_DAY, f"$B{r}", f"$C{r}"), "#,##0")
        cell(w, f"O{r}", f'=IF(N{r}=0,"",E{r}/N{r})', AMT2)
        cell(w, f"P{r}", None, "#,##0", fill=INPUT, color=BLUE_T)
        cell(w, f"Q{r}", None, "#,##0", fill=INPUT, color=BLUE_T)
        start = datetime.date(2025, 12, 29) + datetime.timedelta(days=7 * i)
        txt = notes.get(start)
        cell(w, f"R{r}", ("Agency: " + txt) if txt else None, fill=INPUT, color=BLUE_T, wrap=True, size=8)
        cell(w, f"S{r}", f'=TEXT(B{r},"d mmm")', size=8, color=MUTED, align="center")
        w.row_dimensions[r].height = 36 if txt else 15
    note(w, "A59", "Week 1 includes the last days of the previous year. Over/under plan is shown for complete weeks with data. "
                   "Rows typed as a total on 'Other channels' (like the ChatGPT test) count in their month, not here.")
    w.conditional_formatting.add("A5:Q57", FormulaRule(formula=["$B5>$C$3"], font=font(color=MUTED)))
    w.conditional_formatting.add("A5:Q57", FormulaRule(formula=["$C5=$F$3"], fill=PatternFill("solid", fgColor=GREENFILL), font=font(bold=True)))
    w.conditional_formatting.add("K5:K57", FormulaRule(formula=["AND(ISNUMBER(K5),K5>0)"], font=font(bold=True, color=RED)))
    w.freeze_panes = "D5"
    widths(w, {"A": 6, "B": 11, "C": 11, **{c: 11 for c in "DEFGHIJKLMNO"}, "P": 12, "Q": 12, "R": 70, "S": 8})
    c = BarChart(); c.type = "col"; c.grouping = "stacked"; c.overlap = 100; c.gapWidth = 40
    for j in range(4):
        c.add_data(Reference(w, min_col=4 + j, min_row=4, max_row=57), titles_from_data=True)
    c.set_categories(Reference(w, min_col=19, min_row=5, max_row=57))
    style_bar(c, [CH_COLORS[n] for n, *_ in CHANNELS])
    c.width, c.height = 30, 9
    section(w, "A61", "WEEKLY SPEND BY CHANNEL (platform data)", "ABCDEFGHIJ")
    w.add_chart(c, "A62")


# ---------------------------------------------------------------------------------------------
def style_axes(c, yfmt="#,##0"):
    c.y_axis.numFmt = yfmt
    c.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="E1E0D9", w=6350))
    c.y_axis.spPr = GraphicalProperties(ln=LineProperties(noFill=True))
    c.x_axis.spPr = GraphicalProperties(ln=LineProperties(solidFill="C3C2B7", w=9525))
    c.x_axis.delete = False
    c.y_axis.delete = False
    c.legend.position = "b"


def style_bar(c, colors):
    for s, col in zip(c.series, colors):
        s.graphicalProperties.solidFill = col
        s.graphicalProperties.line.solidFill = "FFFFFF"
        s.graphicalProperties.line.width = 12700
    style_axes(c)


def value_labels(c):
    c.dataLabels = DataLabelList()
    c.dataLabels.showVal = True
    c.dataLabels.showSerName = c.dataLabels.showCatName = c.dataLabels.showLegendKey = False
    c.dataLabels.numFmt = "#,##0"
    c.dataLabels.position = "outEnd"


def ref_line(s, color=INK2, dash="dash", width=22225):
    s.graphicalProperties.line.solidFill = color
    s.graphicalProperties.line.width = width
    s.graphicalProperties.line.dashStyle = dash
    s.marker.symbol = "none"
    s.smooth = False


# ---------------------------------------------------------------------------------------------
MK_ROWS, TY_ROWS = 24, 14


def by_location(b):
    title(b, "A1", "Spend by region, market and campaign type", None)
    cell(b, "A2", f'="Amounts in USD · market and type come from the campaign names (Settings → Locations) · sorted by spend · data up to "&TEXT({S_UPTO},"d mmm yyyy")',
         size=9, color=INK2, border=False, italic=True)
    months = [f'=TEXT(DATE({S_YEAR},{m},1),"mmm")' for m in range(1, 13)]

    def block(top, label, n, first, name_f, val_f, region_f=None):
        section(b, f"A{top}", label, "ABCDEFGHIJKLMNOPQ")
        first_m = 3 if region_f else 2
        header(b, top + 1, 1, [first] + (["Region"] if region_f else []) + months + ["Total", "Share", "Share of spend"])
        r0 = top + 2
        for i in range(n):
            r = r0 + i
            cell(b, f"A{r}", name_f(i), bold=True)
            if region_f:
                cell(b, f"B{r}", region_f(r), align="center", size=9)
            for m in range(12):
                cell(b, f"{L(first_m + m)}{r}", val_f(r, m), AMT)
        rl, rt = r0 + n, r0 + n + 1
        cell(b, f"A{rl}", "Other / not listed above", italic=True)
        if region_f:
            cell(b, f"B{rl}", "")
            cell(b, f"B{rt}", "", fill=TOTAL)
        cell(b, f"A{rt}", "Total", bold=True, fill=TOTAL)
        for m in range(12):
            col = L(first_m + m)
            cell(b, f"{col}{rl}", f"=Monthly!$G${5 + m}-SUM({col}{r0}:{col}{rl - 1})", AMT)
            cell(b, f"{col}{rt}", f"=SUM({col}{r0}:{col}{rl})", AMT, bold=True, fill=TOTAL)
        tc, sc, bc = L(first_m + 12), L(first_m + 13), L(first_m + 14)
        for r in range(r0, rt + 1):
            t = r == rt
            fill = TOTAL if t else None
            cell(b, f"{tc}{r}", f'=IF($A{r}="","",SUM({L(first_m)}{r}:{L(first_m + 11)}{r}))', AMT, bold=True, fill=fill)
            cell(b, f"{sc}{r}", f'=IF(OR($A{r}="",${tc}${rt}=0),"",{tc}{r}/${tc}${rt})', PCT, fill=fill, align="center")
            cell(b, f"{bc}{r}", "" if t else f'=IF({sc}{r}="","",REPT("█",ROUND({sc}{r}*40,0)))', fill=fill, color=INK2, size=8)
        return r0, rl, rt

    mcol = lambda m: L(4 + m)  # Calc month columns D..O
    reg = block(4, "BY REGION", len(REGIONS), "Region", lambda i: REGIONS[i],
                lambda r, m: f"=SUMIFS(Calc!${mcol(m)}${MK0}:${mcol(m)}${MK0 + MKT_N - 1},Calc!$C${MK0}:$C${MK0 + MKT_N - 1},$A{r})")
    mkt = block(reg[2] + 3, "BY MARKET (sorted by spend this year)", MK_ROWS, "Market", lambda i: f"=Calc!$R${MK0 + i}",
                lambda r, m: f'=IF($A{r}="","",SUMIFS(Calc!${mcol(m)}${MK0}:${mcol(m)}${MK0 + MKT_N - 1},Calc!$B${MK0}:$B${MK0 + MKT_N - 1},$A{r}))',
                region_f=lambda r: f'=IF($A{r}="","",IFERROR(VLOOKUP($A{r},Calc!$B${MK0}:$C${MK0 + MKT_N - 1},2,0),""))')
    typ = block(mkt[2] + 3, "BY CAMPAIGN TYPE (sorted by spend this year)", TY_ROWS, "Campaign type", lambda i: f"=Calc!$R${TY0 + i}",
                lambda r, m: f'=IF($A{r}="","",SUMIFS(Calc!${mcol(m)}${TY0}:${mcol(m)}${TY0 + TY_N - 1},Calc!$B${TY0}:$B${TY0 + TY_N - 1},$A{r}))')
    b.conditional_formatting.add(f"A{mkt[0]}:Q{mkt[1] - 1}", FormulaRule(formula=[f'$A{mkt[0]}="No location found"'], font=font(bold=True, color=RED)))
    note(b, f"A{typ[2] + 2}", "Market comes from the location code in each campaign name (Settings → Locations): Geo:SA = Middle East (Saudi Arabia), "
                              "as in the 2026/09 location file; Geo:NA = US & Canada; 'Geo:US-UK-FR-IT', 'WW' and 'All' = Worldwide. "
                              "'Test 1' (ChatGPT) has no location in its name. 'No location found' = a code that isn't on Settings yet.")
    b.freeze_panes = "B4"
    widths(b, {"A": 32, "B": 12, **{L(3 + i): 9.5 for i in range(12)}, "O": 11, "P": 11, "Q": 9, "R": 30})
    b.parent._loc = dict(region=reg, market=mkt)


# ---------------------------------------------------------------------------------------------
def dashboard(d):
    d.sheet_view.showGridLines = False
    widths(d, {"A": 2, **{L(2 + i): 12.5 for i in range(12)}, "N": 2})
    d.merge_cells("B1:M1")
    cell(d, "B1", '="Paid Media Spend "&' + S_YEAR + '&" – Year Overview"', size=18, bold=True, color=NAVY, border=False)
    d.row_dimensions[1].height = 30
    d.merge_cells("B2:M2")
    cell(d, "B2", f'="Platform data up to "&TEXT({S_UPTO},"d mmm yyyy")&" · amounts in USD · Google Ads converted from EUR at "&TEXT({S_FXAVG},"0.0000")&" · Meta, Google Ads and ChatGPT Ads"',
         size=9, color=INK2, border=False, italic=True)
    d.merge_cells("B3:M3")
    cell(d, "B3", f'="Budget: "&{S_STATUS}', size=9, bold=True, color=NAVY, fill="E8EEF7", border=False)
    d.row_dimensions[3].height = 20
    tiles = [
        (f'="BUDGET "&{S_YEAR}', f"={USD('Calc!C27')}", f'="Maximum "&{USD("Calc!C28")}&" · originally "&{USD("Calc!C29")}'),
        ('="SPENT SO FAR"', f"={USD('Calc!C30')}", '=TEXT(Calc!C33,"0%")&" of budget · "&TEXT(Calc!C9,"0%")&" of the year gone"'),
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
        cell(d, f"{c1}5", lab, size=8, bold=True, color=INK2, fill=SUBTLE, border=False, align="left")
        cell(d, f"{c1}6", val, size=18, bold=True, color=INK, fill=SUBTLE, border=False, align="left")
        cell(d, f"{c1}7", sub, size=8, color=INK2, fill=SUBTLE, border=False, align="left", wrap=True)
        for r in (5, 6, 7):
            d[f"{c2}{r}"].fill = PatternFill("solid", fgColor=SUBTLE)
    d.row_dimensions[5].height = 18; d.row_dimensions[6].height = 30; d.row_dimensions[7].height = 30
    cell(d, "P1", "Helper cells for formatting – don't edit", size=8, color=MUTED, border=False)
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
        cell(d, f"D{r}", f"={amt}", AMT)
        cell(d, f"E{r}", "=Calc!C30", AMT, bold=True)
        cell(d, f"F{r}", f"={left}", AMT)
        cell(d, f"G{r}", f"={pct}", PCT, align="center", bold=True)
        cell(d, f"H{r}", f'=REPT("█",ROUND(MIN(G{r},1)*26,0))&REPT("░",26-ROUND(MIN(G{r},1)*26,0))', color=INK2, size=8)
        for col in "IJ":
            cell(d, f"{col}{r}", None)
        cell(d, f"K{r}", status, bold=True, size=9)
        for col in "LM":
            cell(d, f"{col}{r}", None)
    d.merge_cells("B13:M13")
    cell(d, "B13", f'="By "&TEXT(Calc!C3,"d mmm")&", "&{USD("Calc!C30")}&" was spent: "&{USD("ABS(Calc!C36)")}&IF(Calc!C36>=0," more"," less")&" than an even pace through the year ("&{USD("Calc!C35")}&"). Current pace from "&Calc!C40&"."',
         size=9, color=INK2, border=False, italic=True, wrap=True)
    d.row_dimensions[13].height = 26
    d.conditional_formatting.add("K11:K12", FormulaRule(formula=['LEFT(K11,1)="▲"'], font=font(9, True, RED)))
    d.conditional_formatting.add("K11:K12", FormulaRule(formula=['LEFT(K11,1)="●"'], font=font(9, True, GREEN)))
    d.conditional_formatting.add("H11:H12", FormulaRule(formula=["G11>=1"], font=font(8, False, RED)))
    d.conditional_formatting.add("H11:H12", FormulaRule(formula=["AND(G11<1,G11>$P$2+0.05)"], font=font(8, False, AMBER)))

    section(d, "B15", "SPEND BY CHANNEL", [L(2 + i) for i in range(12)])
    d.merge_cells("B16:C16"); d.merge_cells("K16:M16")
    hdr = {"B": "Channel", "D": "Spent (USD)", "E": "Share", "F": "Last full month", "G": "Last 3 full months",
           "H": "Last full week", "I": "Counts toward budget?", "J": "Billing currency", "K": "Note"}
    for col in "BCDEFGHIJKLM":
        cell(d, f"{col}16", hdr.get(col), bold=True, color=WHITE, fill=NAVY, align="center", wrap=True, size=9)
    d.row_dimensions[16].height = 26
    for i, (name, srow, bill, cnt, nt) in enumerate(CHANNELS):
        r, cr = 17 + i, 20 + i
        d.merge_cells(f"B{r}:C{r}"); d.merge_cells(f"K{r}:M{r}")
        cell(d, f"B{r}", name, bold=True); cell(d, f"C{r}", None)
        cell(d, f"D{r}", f"=Calc!D{cr}", AMT)
        cell(d, f"E{r}", f"=Calc!I{cr}", PCT, align="center")
        cell(d, f"F{r}", f"=Calc!E{cr}", AMT)
        cell(d, f"G{r}", f"=Calc!F{cr}", AMT)
        cell(d, f"H{r}", f'=IF(Calc!G{cr}=0,"–",Calc!G{cr})', AMT, align="right")
        cell(d, f"I{r}", f"=Settings!C{srow}", align="center")
        cell(d, f"J{r}", f"=Settings!B{srow}", align="center")
        cell(d, f"K{r}", f'=IF(Settings!D{srow}="","",Settings!D{srow})', size=8, wrap=True)
        for col in "LM":
            cell(d, f"{col}{r}", None)
        d.row_dimensions[r].height = 24 if nt else 16
    r = 21
    d.merge_cells(f"B{r}:C{r}"); d.merge_cells(f"K{r}:M{r}")
    cell(d, f"B{r}", "Total – all channels", bold=True, fill=TOTAL); cell(d, f"C{r}", None, fill=TOTAL)
    for col, f in zip("DEFGH", ["=Calc!D25", '=IF(Calc!D25=0,"",1)', "=Calc!E25", "=Calc!F25", '=IF(Calc!G25=0,"–",Calc!G25)']):
        cell(d, f"{col}{r}", f, PCT if col == "E" else AMT, bold=True, fill=TOTAL, align="center" if col == "E" else "right")
    for col in "IJKLM":
        cell(d, f"{col}{r}", None, fill=TOTAL)
    d.merge_cells("B22:M22")
    cell(d, "B22", f'="Last full week = "&TEXT(Calc!C14,"d mmm")&" – "&TEXT(Calc!C13,"d mmm")&". Left out of the current pace: "&{USD("Calc!C49")}&" spent in the last 3 full weeks by campaigns on the Ended campaigns list (Settings)."',
         size=9, color=INK2, border=False, italic=True)

    m = d.parent["Monthly"]
    section(d, "B24", "SPEND BY MONTH AND CHANNEL vs. PLAN", ["B", "C", "D", "E", "F", "G"])
    section(d, "H24", "SPEND SO FAR vs. PLAN AND MAXIMUM (CUMULATIVE)", ["H", "I", "J", "K", "L", "M"])
    bar = BarChart(); bar.type = "col"; bar.grouping = "stacked"; bar.overlap = 100; bar.gapWidth = 60
    for j in range(4):
        bar.add_data(Reference(m, min_col=3 + j, min_row=4, max_row=16), titles_from_data=True)
    bar.set_categories(Reference(m, min_col=19, min_row=5, max_row=16))
    style_bar(bar, [CH_COLORS[n] for n, *_ in CHANNELS])
    ln = LineChart(); ln.add_data(Reference(m, min_col=9, min_row=4, max_row=16), titles_from_data=True)
    ref_line(ln.series[0])
    bar += ln
    bar.x_axis.tickLblSkip = 1
    bar.width, bar.height = 16.2, 8.2
    d.add_chart(bar, "B25")
    cum = BarChart(); cum.type = "col"; cum.gapWidth = 60
    cum.add_data(Reference(m, min_col=11, min_row=4, max_row=16), titles_from_data=True)
    cum.set_categories(Reference(m, min_col=19, min_row=5, max_row=16))
    style_bar(cum, [NAVY])
    ln2 = LineChart()
    ln2.add_data(Reference(m, min_col=12, min_row=4, max_row=16), titles_from_data=True)
    ln2.add_data(Reference(m, min_col=13, min_row=4, max_row=16), titles_from_data=True)
    ref_line(ln2.series[0]); ref_line(ln2.series[1], color=RED, dash="sysDot", width=19050)
    cum += ln2
    cum.x_axis.tickLblSkip = 1
    cum.width, cum.height = 16.2, 8.2
    d.add_chart(cum, "H25")

    top = 42
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
        cell(d, f"K{r}", f'=IF({S_UPTO}>=EOMONTH(Monthly!A{z},0),{nxt},IF({S_UPTO}>=Monthly!A{a},"In progress","Not started"))', align="center", size=9)
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
                                                                       fill=PatternFill("solid", fgColor=GREENFILL)))

    top = 50
    section(d, f"B{top}", "YEAR-END OUTLOOK (budget channels)", [L(2 + i) for i in range(12)])
    for rr in range(top + 1, top + 6):
        d.merge_cells(f"B{rr}:E{rr}"); d.merge_cells(f"J{rr}:M{rr}")
    oh = {"B": "If we spend from now on at…", "F": "Per week (USD)", "G": "Year-end total", "H": "vs. budget",
          "I": "vs. maximum", "J": "What it means"}
    for col in "BCDEFGHIJKLM":
        cell(d, f"{col}{top + 1}", oh.get(col), bold=True, color=WHITE, fill=NAVY, align="center", wrap=True, size=9)
    d.row_dimensions[top + 1].height = 24
    rows = [
        ('="…the current pace"', "=Calc!C39", "=Calc!C42", '="Source: "&Calc!C40'),
        ('="…a pace that lands exactly on the budget"', "=MAX(0,Calc!C43)", "=Calc!C27",
         '=IF(Calc!C31<=0,"The budget is already used up",IF(Calc!C39=0,"",IF(Calc!C43<Calc!C39,TEXT(1-Calc!C43/Calc!C39,"0%")&" less per week than the current pace",TEXT(Calc!C43/Calc!C39-1,"0%")&" more per week than the current pace")))'),
        ('="…a pace that uses the maximum"', "=MAX(0,Calc!C44)", "=Calc!C28",
         '=IF(Calc!C32<=0,"The maximum is already passed",IF(Calc!C39=0,"",IF(Calc!C44<Calc!C39,TEXT(1-Calc!C44/Calc!C39,"0%")&" less per week than the current pace",TEXT(Calc!C44/Calc!C39-1,"0%")&" more per week than the current pace")))'),
        ('="…last month\'s pace ("&TEXT(Calc!C11,"mmmm")&", before the cuts)"', "=Calc!C45/Calc!C17*7", "=Calc!C47", '="For reference"'),
    ]
    for i, (lab, pw, ye, what) in enumerate(rows):
        r = top + 2 + i
        cell(d, f"B{r}", lab, bold=True)
        for col in "CDE":
            cell(d, f"{col}{r}", None)
        cell(d, f"F{r}", pw, AMT)
        cell(d, f"G{r}", ye, AMT, bold=True)
        cell(d, f"H{r}", f"=G{r}-Calc!$C$27", AMT)
        cell(d, f"I{r}", f"=G{r}-Calc!$C$28", AMT)
        cell(d, f"J{r}", what, size=8, wrap=True)
        for col in "KLM":
            cell(d, f"{col}{r}", None)
        d.row_dimensions[r].height = 26 if i == 0 else 16
    d.conditional_formatting.add(f"H{top + 2}:I{top + 5}", FormulaRule(formula=[f"H{top + 2}>0.5"], font=font(10, True, RED)))

    top = 57
    b = d.parent["By location & type"]
    loc = d.parent._loc
    section(d, f"B{top}", "WHERE THE MONEY WENT – BY REGION", ["B", "C", "D", "E", "F", "G"])
    section(d, f"H{top}", "TOP MARKETS (year to date)", ["H", "I", "J", "K", "L", "M"])
    r0, rl, rt = loc["region"]
    reg = BarChart(); reg.type = "bar"; reg.gapWidth = 50
    reg.add_data(Reference(b, min_col=14, min_row=r0, max_row=rl - 1), titles_from_data=False)
    reg.set_categories(Reference(b, min_col=1, min_row=r0, max_row=rl - 1))
    style_bar(reg, [SLATE]); reg.legend = None; value_labels(reg)
    reg.x_axis.scaling.orientation = "maxMin"
    reg.width, reg.height = 16.2, 7
    d.add_chart(reg, f"B{top + 1}")
    m0, ml, mt = loc["market"]
    mk = BarChart(); mk.type = "bar"; mk.gapWidth = 40
    mk.add_data(Reference(b, min_col=15, min_row=m0, max_row=m0 + 9), titles_from_data=False)
    mk.set_categories(Reference(b, min_col=1, min_row=m0, max_row=m0 + 9))
    style_bar(mk, [SLATE]); mk.legend = None; value_labels(mk)
    mk.x_axis.scaling.orientation = "maxMin"
    mk.width, mk.height = 16.2, 7
    d.add_chart(mk, f"H{top + 1}")
    note(d, f"B{top + 16}", "Region and market come from the location code in each campaign name – see 'By location & type'. "
                            "How to update: the 'Update' tab.")
    d.column_dimensions["P"].hidden = True
    d.print_area = "A1:N74"
    d.print_options.horizontalCentered = True
    d.page_setup.orientation = "landscape"
    d.page_setup.fitToWidth = 1
    d.sheet_properties.pageSetUpPr.fitToPage = True
    d.page_setup.fitToHeight = 0


# ---------------------------------------------------------------------------------------------
def update_tab(u, sources):
    u.sheet_view.showGridLines = False
    widths(u, {"A": 2, **{L(2 + i): 12.5 for i in range(12)}, "N": 2, "P": 12, "Q": 12})
    u.merge_cells("B1:M1")
    cell(u, "B1", "Weekly update", size=18, bold=True, color=NAVY, border=False)
    u.row_dimensions[1].height = 30
    u.merge_cells("B2:M2")
    cell(u, "B2", "Every Monday, about 10 minutes: replace the two exports, check the ticks, write one note. "
                  "Every other tab, chart and the Dashboard update by themselves.", size=9, color=INK2, border=False, italic=True)
    # helper cells (column P, hidden): row of the last full week on the Weekly tab, weekly allowance
    cell(u, "P1", "=IFERROR(MATCH(Calc!C14,Weekly!$B$5:$B$57,0),0)", "0", size=8, color=MUTED, border=False)
    cell(u, "P2", "=Calc!C43", AMT, size=8, color=MUTED, border=False)
    cell(u, "P3", f"={CK_COUNT}", "0", size=8, color=MUTED, border=False)

    tiles = [
        ("DATA UP TO", '=TEXT(Calc!C3,"ddd d mmm yyyy")',
         '=IF(Calc!C3>=Calc!C61,"✓ Includes last week","⚠ Last Sunday was "&TEXT(Calc!C61,"d mmm")&": import new exports")'),
        ("META EXPORT", '=TEXT(Calc!C57,"#,##0")&" rows"', f"=Calc!C{CK_FIRST}"),
        ("GOOGLE ADS EXPORT", '=TEXT(Calc!C58,"#,##0")&" rows"', f"=Calc!C{CK_FIRST + 1}"),
        ("CHECKS", f'=IF({CK_COUNT}=0,"✓ All good","⚠ "&{CK_COUNT}&" to fix")', f'=IF({CK_COUNT}=0,"All {CK_LAST - CK_FIRST + 1} checks passed","See the list below")'),
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
    u.row_dimensions[4].height = 18; u.row_dimensions[5].height = 28; u.row_dimensions[6].height = 28
    u.conditional_formatting.add("B6:M6", FormulaRule(formula=['LEFT(B6,1)="⚠"'], font=font(8, True, RED)))
    u.conditional_formatting.add("B6:M6", FormulaRule(formula=['LEFT(B6,1)="✓"'], font=font(8, True, GREEN)))
    u.conditional_formatting.add("K5", FormulaRule(formula=['LEFT(K5,1)="⚠"'], font=font(16, True, RED)))
    u.conditional_formatting.add("K5", FormulaRule(formula=['LEFT(K5,1)="✓"'], font=font(16, True, GREEN)))

    section(u, "B8", "EVERY MONDAY – 3 STEPS", [L(2 + i) for i in range(12)])
    steps = [
        ("Meta → 'Meta export' tab",
         "Ads Manager: Campaigns → dates 1 Jan – yesterday → Breakdown: By time → Day → Reports → Export table data → .csv (same columns every week).\n"
         "Here: open 'Meta export' → Ctrl/Cmd+A → Delete → click A1 → File → Import → Upload → pick the file → "
         "Import location 'Replace data at selected cell' → Import data.",
         f"=Calc!C{CK_FIRST}"),
        ("Google Ads → 'Google export' tab",
         "Google Ads: Reports → your spend report (Campaign, Day, Currency code, Cost, Impr., Clicks, Conversions; save it once) → dates 1 Jan – yesterday → "
         "Download → .csv (not 'Excel .csv').\nHere: open 'Google export' → Ctrl/Cmd+A → Delete → click A1 → File → Import → Upload → "
         "'Replace data at selected cell' → Import data.",
         f"=Calc!C{CK_FIRST + 1}"),
        ("Check the ticks, write last week's note",
         '="All checks below should show ✓. Then Weekly tab → Notes for W/C "&TEXT(Calc!C14,"d mmm")&": launches, pauses, budget changes, anything unusual. '
         'Then look at the Dashboard and share it."',
         '=IF($P$1=0,"",IF(INDEX(Weekly!$R$5:$R$57,$P$1)<>"","✓ Note written for W/C "&TEXT(Calc!C14,"d mmm"),"○ No note yet for W/C "&TEXT(Calc!C14,"d mmm")))'),
    ]
    r = 9
    for n, (head, how, status) in enumerate(steps, 1):
        u.merge_cells(f"B{r}:B{r + 2}")
        cell(u, f"B{r}", n, size=20, bold=True, color=WHITE, fill="2A78D6", border=False, align="center")
        u.merge_cells(f"C{r}:J{r}")
        cell(u, f"C{r}", head, size=11, bold=True, color=NAVY, fill="F3F7FD", border=False)
        u.merge_cells(f"C{r + 1}:J{r + 2}")
        cell(u, f"C{r + 1}", how, size=9, color=INK, fill="F3F7FD", border=False, wrap=True, valign="top")
        u.merge_cells(f"K{r}:M{r + 2}")
        cell(u, f"K{r}", status, size=9, bold=True, color=INK2, fill="F3F7FD", border=False, wrap=True, align="center")
        for rr in range(r, r + 3):
            for col in "BCDEFGHIJKLM":
                if u[f"{col}{rr}"].fill.fgColor.rgb in (None, "00000000"):
                    u[f"{col}{rr}"].fill = PatternFill("solid", fgColor="F3F7FD")
        u.row_dimensions[r].height = 20
        u.row_dimensions[r + 1].height = 27
        u.row_dimensions[r + 2].height = 27
        r += 4
    u.conditional_formatting.add("K9:M19", FormulaRule(formula=['LEFT(K9,1)="⚠"'], font=font(9, True, RED)))
    u.conditional_formatting.add("K9:M19", FormulaRule(formula=['LEFT(K9,1)="✓"'], font=font(9, True, GREEN)))
    u.conditional_formatting.add("K9:M19", FormulaRule(formula=['LEFT(K9,1)="○"'], font=font(9, True, AMBER)))

    top = r  # 21
    section(u, f"B{top}", "ONLY WHEN NEEDED", [L(2 + i) for i in range(12)])
    extra = [
        ("ChatGPT Ads or LinkedIn Ads ran", "'Other channels' tab → one row per campaign per day or week, spend as billed.",
         f'=IF(MAX(\'Other channels\'!$A${OC_FIRST}:$A${OC_FIRST + OTHER_CAP - 1})=0,"No rows yet","Last row: "&TEXT(MAX(\'Other channels\'!$A${OC_FIRST}:$A${OC_FIRST + OTHER_CAP - 1}),"d mmm yyyy"))'),
        ("A campaign stopped for good", "Settings → Ended campaigns → add its name, so the forecast stops counting it.",
         '=Calc!C41&" on the list now"'),
        ("A check says a campaign has no market", "Settings → Locations → add its code (or the full campaign name) with its market.",
         f"=Calc!C{CK_FIRST + 4}"),
        ("Finance gives monthly EUR → USD rates", "Settings → Exchange rate → type each month's rate.",
         '="Now: 1 EUR = "&TEXT(' + S_FXAVG + ',"0.0000")&" USD (average)"'),
        ("First Monday of the month", "Monthly tab → compare last month's 'as billed' columns with Meta and Google Ads billing.", '=""'),
    ]
    header(u, top + 1, 2, ["When", "", "", "What to do", "", "", "", "", "", "Now", "", ""], height=20)
    for a_, z_ in (("B", "D"), ("E", "J"), ("K", "M")):
        u.merge_cells(f"{a_}{top + 1}:{z_}{top + 1}")
    for i, (when, what, now) in enumerate(extra):
        rr = top + 2 + i
        for a_, z_ in (("B", "D"), ("E", "J"), ("K", "M")):
            u.merge_cells(f"{a_}{rr}:{z_}{rr}")
        cell(u, f"B{rr}", when, bold=True, size=9)
        cell(u, f"E{rr}", what, size=9, wrap=True)
        cell(u, f"K{rr}", now, size=9, color=INK2)
        for col in "CDFGHIJLM":
            cell(u, f"{col}{rr}", None)
        u.row_dimensions[rr].height = 18
    u.conditional_formatting.add(f"K{top + 2}:M{top + 6}", FormulaRule(formula=[f'LEFT(K{top + 2},1)="⚠"'], font=font(9, True, RED)))

    top = top + 2 + len(extra) + 1  # 29
    section(u, f"B{top}", "CHECKS", [L(2 + i) for i in range(12)])
    header(u, top + 1, 2, ["Check", "", "", "Result", "", "", "", "", "", "If it shows ⚠", "", ""], height=20)
    for a_, z_ in (("B", "D"), ("E", "J"), ("K", "M")):
        u.merge_cells(f"{a_}{top + 1}:{z_}{top + 1}")
    todo = [
        "Export by day, same columns as before, and import again.",
        "Use the spend report (Campaign, Day, Cost …) and import again.",
        "Export both for the same dates: 1 Jan – yesterday.",
        "Import this week's exports (steps 1 and 2).",
        "Settings → Locations: add the code shown, with its market.",
        "Settings → Markets: add the market with its region.",
        "Ask Claude to make the tracker read more rows.",
        "File → Settings → Locale 'United States', then import again.",
        "Settings → Ended campaigns: copy the name from the export.",
        "Other channels: give each row a date and a channel.",
    ]
    for i in range(CK_LAST - CK_FIRST + 1):
        rr = top + 2 + i
        for a_, z_ in (("B", "D"), ("E", "J"), ("K", "M")):
            u.merge_cells(f"{a_}{rr}:{z_}{rr}")
        cell(u, f"B{rr}", f"=Calc!B{CK_FIRST + i}", bold=True, size=9)
        cell(u, f"E{rr}", f"=Calc!C{CK_FIRST + i}", size=9)
        cell(u, f"K{rr}", todo[i], size=8, color=INK2, wrap=True)
        for col in "CDFGHIJLM":
            cell(u, f"{col}{rr}", None)
        u.row_dimensions[rr].height = 24
    ck0, ck1 = top + 2, top + 1 + (CK_LAST - CK_FIRST + 1)
    u.conditional_formatting.add(f"E{ck0}:J{ck1}", FormulaRule(formula=[f'LEFT($E{ck0},1)="⚠"'], font=font(9, True, RED), fill=PatternFill("solid", fgColor="FBE5E5")))
    u.conditional_formatting.add(f"E{ck0}:J{ck1}", FormulaRule(formula=[f'LEFT($E{ck0},1)="✓"'], font=font(9, False, GREEN)))

    top = ck1 + 2  # 43
    section(u, f"B{top}", '="LAST FULL WEEK – "&UPPER(TEXT(Calc!C14,"d mmm"))&" TO "&UPPER(TEXT(Calc!C13,"d mmm"))', [L(2 + i) for i in range(12)])
    header(u, top + 1, 2, ["Channel", "", "Spend (USD)", "Week before", "Change", "Conversions (platform)", "Cost per conversion",
                           "Share of the week", "", "", "", ""], height=30)
    u.merge_cells(f"B{top + 1}:C{top + 1}"); u.merge_cells(f"I{top + 1}:M{top + 1}")
    lw = [("Meta", "D", "L"), ("Google Ads", "E", "N"), ("ChatGPT Ads", "F", None), ("LinkedIn Ads", "G", None), ("Total – all channels", "H", None)]
    tot_row = top + 2 + len(lw) - 1
    for i, (name, col, convcol) in enumerate(lw):
        rr = top + 2 + i
        t = name.startswith("Total")
        fill = TOTAL if t else None
        u.merge_cells(f"B{rr}:C{rr}"); u.merge_cells(f"I{rr}:M{rr}")
        cell(u, f"B{rr}", name, bold=True, size=9, fill=fill); cell(u, f"C{rr}", None, fill=fill)
        cell(u, f"D{rr}", f"=IF($P$1=0,0,INDEX(Weekly!${col}$5:${col}$57,$P$1))", AMT, bold=True, fill=fill)
        cell(u, f"E{rr}", f"=IF($P$1<2,0,INDEX(Weekly!${col}$5:${col}$57,$P$1-1))", AMT, fill=fill)
        cell(u, f"F{rr}", f'=IF(E{rr}=0,"",D{rr}/E{rr}-1)', '+0%;-0%;0%', align="center", fill=fill)
        if convcol:
            cell(u, f"G{rr}", f"=IF($P$1=0,0,INDEX(Weekly!${convcol}$5:${convcol}$57,$P$1))", "#,##0", align="center", fill=fill)
            cell(u, f"H{rr}", f'=IF(G{rr}=0,"",D{rr}/G{rr})', AMT2, fill=fill)
        else:
            cell(u, f"G{rr}", "–", align="center", fill=fill, color=MUTED)
            cell(u, f"H{rr}", "–", align="center", fill=fill, color=MUTED)
        if t:
            cell(u, f"I{rr}", '="Needed to land on the budget: "&' + USD("$P$2") + '&" a week"', size=9, bold=True, fill=fill)
        else:
            cell(u, f"I{rr}", f'=IF(OR($D${tot_row}=0,D{rr}=0),"",REPT("█",ROUND(D{rr}/$D${tot_row}*40,0))&"  "&TEXT(D{rr}/$D${tot_row},"0%"))',
                 size=8, color=CH_COLORS[name])
        for col in "JKLM":
            cell(u, f"{col}{rr}", None, fill=fill)
    u.conditional_formatting.add(f"F{top + 2}:F{tot_row}", FormulaRule(formula=[f"AND(ISNUMBER(F{top + 2}),F{top + 2}>0.1)"], font=font(10, True, RED)))
    note(u, f"B{tot_row + 1}", "Conversions are each platform's own count (Meta: website registrations completed; Google Ads: conversions) – compare each channel with itself.")

    top = tot_row + 3
    section(u, f"B{top}", "LAST 8 WEEKS – budget channels", [L(2 + i) for i in range(12)])
    header(u, top + 1, 2, ["Week", "", "Spend (USD)", "", "", "", "", "", "", '="vs. "&' + USD("$P$2") + '&" a week (needed to land on the budget)"', "", ""], height=30)
    u.merge_cells(f"B{top + 1}:C{top + 1}"); u.merge_cells(f"E{top + 1}:J{top + 1}"); u.merge_cells(f"K{top + 1}:M{top + 1}")
    w0, w1 = top + 2, top + 9
    for k in range(8):
        rr = top + 2 + k
        idx = f"($P$1-{7 - k})"
        u.merge_cells(f"B{rr}:C{rr}"); u.merge_cells(f"E{rr}:J{rr}"); u.merge_cells(f"K{rr}:M{rr}")
        cell(u, f"B{rr}", f'=IF({idx}<1,"","W/C "&TEXT(INDEX(Weekly!$B$5:$B$57,{idx}),"d mmm"))', size=9, bold=True)
        cell(u, f"C{rr}", None)
        cell(u, f"D{rr}", f'=IF({idx}<1,"",INDEX(Weekly!$I$5:$I$57,{idx}))', AMT, bold=True)
        cell(u, f"E{rr}", f'=IF(OR(D{rr}="",MAX($D${w0}:$D${w1})=0),"",REPT("█",ROUND(D{rr}/MAX($D${w0}:$D${w1})*48,0)))', size=8, color=NAVY)
        cell(u, f"K{rr}", f'=IF(D{rr}="","",IF(D{rr}>$P$2,"▲ "&' + USD(f"D{rr}-$P$2") + f'&" more",IF(D{rr}<$P$2,"▼ "&' + USD(f"$P$2-D{rr}") + '&" less","= on target")))', size=9)
        for col in "FGHIJLM":
            cell(u, f"{col}{rr}", None)
    u.conditional_formatting.add(f"E{w0}:J{w1}", FormulaRule(formula=[f"AND(ISNUMBER($D{w0}),$D{w0}>$P$2)"], font=font(8, False, "D03B3B")))
    u.conditional_formatting.add(f"K{w0}:M{w1}", FormulaRule(formula=[f'LEFT($K{w0},1)="▲"'], font=font(9, True, RED)))
    u.conditional_formatting.add(f"K{w0}:M{w1}", FormulaRule(formula=[f'LEFT($K{w0},1)="▼"'], font=font(9, True, GREEN)))
    note(u, f"B{w1 + 1}", "Red bars = weeks above what we can spend per week from now on and still land on the budget.")

    top = w1 + 3
    section(u, f"B{top}", "SOURCES", [L(2 + i) for i in range(12)])
    for i, t in enumerate(sources):
        rr = top + 1 + i
        u.merge_cells(f"B{rr}:M{rr}")
        cell(u, f"B{rr}", t, size=8, color=INK2, border=False, wrap=True)
        u.row_dimensions[rr].height = 24 if len(t) > 170 else 13
    u.column_dimensions["P"].hidden = True
    u.column_dimensions["Q"].hidden = True


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
    "1 Jan – 12 Oct 2026, exported 13 Oct 2026. For Jan–Sep they match the earlier monthly exports (Meta to the cent; Google within €0.43 of rounding).",
    "ChatGPT Ads: 'Test 1', 23 Sep – 2 Oct 2026, €229.56 in total, typed on 'Other channels' as one total row.",
    "Current pace: last 3 full weeks of the budget channels, without the campaigns on the Ended list (FR_Alibaba, run by PnP's internal team, "
    "last spend 5 Oct; ChatGPT 'Test 1', ended 2 Oct).",
    "Agency figures: the agency's weekly reports in Notion (W/C 29 Dec 2025 – 5 Oct 2026), read on 13 Oct 2026 and copied as written ('Agency reports' tab).",
    "Budget: Tereza, 13 Oct 2026 – $300k for 2026 (originally $350k), up to $320k at most. Exchange rate: 1 EUR = 1.1177 USD (live rate on 13 Oct 2026).",
]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "agency") if os.path.isdir(os.path.join(here, "agency")) else os.path.join(here, "..", "agency"))
    import agency_weeks as AW
    out, meta_csv, google_csv = sys.argv[1], sys.argv[2], sys.argv[3]
    build(out, LX.read(meta_csv), LX.read(google_csv), AW.weeks(), AGENCY_TOTALS, SOURCES)
    print("saved", out)
