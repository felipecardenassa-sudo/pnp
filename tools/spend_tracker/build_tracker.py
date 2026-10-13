"""Build the PnP Paid Media Spend Tracker (Google Sheets friendly .xlsx).

Usage (from this folder): python build_tracker.py OUT.xlsx PLATFORM_DATA_UP_TO(YYYY-MM-DD) [--draft]

Data rows: dict(date, channel, campaign, spend, impr, clicks, conv, rowtype) with spend in the billing currency.
rowtype "" = a daily row (what gets pasted every week); "Month total" = a whole month on one row (history).
Weekly figures only use daily rows; monthly figures use both.
"""
import sys, datetime, collections
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as L
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.label import DataLabelList
from xlstyle import *
import campaign_map as CM

CHANNELS = [  # name, data tab, settings row, billing currency, counts toward budget, note
    ("Meta", "Meta data", 22, "USD", "Yes", "Includes FR_Alibaba (run by PnP's internal team) – confirm it belongs in this budget."),
    ("Google Ads", "Google data", 23, "EUR", "Yes", ""),
    ("ChatGPT Ads", "ChatGPT data", 24, "EUR", "Yes", "To confirm with Tereza."),
    ("LinkedIn Ads", "LinkedIn data", 25, "USD", "Yes", "No spend in 2026. Billing currency to check."),
]
FX_RATE = 1.1177
FX_SOURCE = "Live rate on 13 Oct 2026 (from Felipe). Replace with Finance's monthly rates if they use them."
DMAX = 20000
HELPER_ROWS = 8000
CAMP_FIRST, CAMP_LAST = 7, 300
REGIONS = ["EMEA", "Americas", "Global", "Not specified"]
SLATE = "6B7A8F"
DRAFT = False
DRAFT_DASH = "DRAFT – not for sharing yet."

# Settings cells
S_UPTO, S_CUR, S_STATUS = "Settings!$C$5", "Settings!$C$6", "Settings!$C$9"
S_PSTART, S_PEND, S_YEAR, S_W1 = "Settings!$C$10", "Settings!$C$11", "Settings!$C$12", "Settings!$C$13"
S_BUDGET, S_MAX, S_ORIG = "Settings!$D$16", "Settings!$D$17", "Settings!$D$18"
S_FX = "Settings!$B$29:$B$40"
S_FXAVG = "Settings!$B$41"


def counts(row):
    return f'(Settings!$C${row}="Yes")'


def sumifs(tab, col, lo, hi, extra="", daily=False):
    rng = lambda c: f"'{tab}'!${c}$3:${c}${DMAX}"
    d = f',{rng("G")},"<>Month total"' if daily else ""
    return f'SUMIFS({rng(col)},{rng("A")},">="&{lo},{rng("A")},"<="&{hi}{extra}{d})'


def CUR(x):
    return f'IF({S_CUR}="USD","$","€")&TEXT({x},"#,##0")'


def to_usd(r):
    return r["spend"] if r["channel"] in ("Meta", "LinkedIn Ads") else r["spend"] * FX_RATE


# ---------------------------------------------------------------------------------------------
def build(out, upto, rows, agency_weeks=(), agency_totals=(), source_note=""):
    wb = Workbook()
    names = ["Dashboard", "Weekly", "Monthly", "By location & type", "Campaigns", "Agency reports",
             "Settings", "How to update", "Meta data", "Google data", "ChatGPT data", "LinkedIn data", "Calc"]
    ws = {n: (wb.active if i == 0 else wb.create_sheet(n)) for i, n in enumerate(names)}
    ws["Dashboard"].title = "Dashboard"
    tabcol = {"Dashboard": NAVY, "Weekly": "2A78D6", "Monthly": "2A78D6", "By location & type": "2A78D6",
              "Campaigns": "BF9000", "Agency reports": "7F7F7F", "Settings": "BF9000", "How to update": "7F7F7F",
              "Meta data": "BF9000", "Google data": "BF9000", "ChatGPT data": "BF9000", "LinkedIn data": "BF9000", "Calc": "7F7F7F"}
    for n, w in ws.items():
        w.sheet_properties.tabColor = tabcol[n]
    notes = {w["start"]: w.get("notes") for w in agency_weeks}
    settings(ws["Settings"], upto)
    data_tabs(ws, rows)
    campaigns(ws["Campaigns"], rows)
    arow = agency_tab(ws["Agency reports"], agency_weeks, agency_totals)
    calc(ws["Calc"], arow)
    monthly(ws["Monthly"])
    weekly(ws["Weekly"], notes)
    by_location(ws["By location & type"], rows)
    how_to(ws["How to update"], source_note)
    dashboard(ws["Dashboard"])
    wb.save(out)


# ---------------------------------------------------------------------------------------------
def settings(s, upto):
    title(s, "A1", "Settings", "Yellow cells are the only ones to change. The rest of the workbook updates from them.", "A2")
    section(s, "A4", "REPORT", "ABCDE")
    for r, lab, val, fmt, nt in [
        (5, "Platform data up to (last day included)", upto, DATE_F, "The last day you pasted platform data for (usually last Sunday)."),
        (6, "Show amounts in", "USD", None, "USD (how PnP talks about budget) or EUR. Every tab switches."),
    ]:
        cell(s, f"A{r}", lab, bold=True); s.merge_cells(f"A{r}:B{r}")
        cell(s, f"C{r}", val, fmt, fill=INPUT, color="0000FF", align="center")
        note(s, f"D{r}", nt)
    section(s, "A8", "BUDGET 2026", "ABCDE")
    cell(s, "A9", "Budget status", bold=True); s.merge_cells("A9:B9")
    cell(s, "C9", "Confirmed by Tereza on 13 Oct 2026: $300k for 2026 (originally $350k). We can go up to $320k, ideally not more.",
         fill=INPUT, color="0000FF", wrap=True)
    s.merge_cells("C9:E9"); s.row_dimensions[9].height = 30
    for r, lab, val in [(10, "Budget period starts", datetime.date(2026, 1, 1)), (11, "Budget period ends", datetime.date(2026, 12, 31))]:
        cell(s, f"A{r}", lab, bold=True); s.merge_cells(f"A{r}:B{r}")
        cell(s, f"C{r}", val, DATE_F, fill=INPUT, color="0000FF", align="center")
    cell(s, "A12", "Year (calculated)", bold=True); s.merge_cells("A12:B12")
    cell(s, "C12", "=YEAR(C10)", "0", align="center")
    cell(s, "A13", "Week 1 starts on (calculated)", bold=True); s.merge_cells("A13:B13")
    cell(s, "C13", "=DATE(C12,1,1)-WEEKDAY(DATE(C12,1,1),2)+1", DATE_F, align="center")
    note(s, "D13", "Weeks run Monday to Sunday.")
    header(s, 15, 1, ["Budget line", "Amount", "Currency", "In report currency", "Note"])
    for r, lab, amt, nt in [(16, "Annual budget", 300000, "Confirmed by Tereza, 13 Oct 2026."),
                            (17, "Maximum (ideally not more)", 320000, "\"We can spend up to 320k this year, ideally not more.\""),
                            (18, "Original budget", 350000, "Reduced because performance wasn't good enough (Tereza).")]:
        cell(s, f"A{r}", lab, bold=True)
        cell(s, f"B{r}", amt, AMT, fill=INPUT, color="0000FF")
        cell(s, f"C{r}", "USD", fill=INPUT, color="0000FF", align="center")
        cell(s, f"D{r}", f'=IF(B{r}="","",B{r}*IF(C{r}=$C$6,1,IF(C{r}="USD",1/$B$41,$B$41)))', AMT, bold=r == 16)
        cell(s, f"E{r}", nt, size=9, color=INK2, wrap=True)
    section(s, "A20", "CHANNELS", "ABCDE")
    header(s, 21, 1, ["Channel", "Billing currency", "Counts toward the budget?", "", "Note"])
    for name, tab, r, bill, cnt, nt in CHANNELS:
        cell(s, f"A{r}", name, bold=True)
        cell(s, f"B{r}", bill, fill=INPUT, color="0000FF", align="center")
        cell(s, f"C{r}", cnt, fill=INPUT, color="0000FF", align="center")
        cell(s, f"D{r}", None)
        cell(s, f"E{r}", nt, size=9, color=INK2, wrap=True)
    section(s, "A27", "EXCHANGE RATE – EUR TO USD", "ABCDE")
    header(s, 28, 1, ["Month", "1 EUR = ? USD", "Source", "", ""])
    s.merge_cells("C28:E28")
    for i in range(12):
        r = 29 + i
        cell(s, f"A{r}", f"=DATE($C$12,{i + 1},1)", MON_F, bold=True)
        cell(s, f"B{r}", FX_RATE, "0.0000", fill=INPUT, color="0000FF", align="center")
        cell(s, f"C{r}", FX_SOURCE if i == 0 else "Same as above", size=8, color=INK2, fill=INPUT)
        s.merge_cells(f"C{r}:E{r}")
    cell(s, "A41", "Average", bold=True, fill=TOTAL)
    cell(s, "B41", "=AVERAGE(B29:B40)", "0.0000", bold=True, fill=TOTAL, align="center")
    note(s, "A43", "The 90k (Google) and 180k (Meta) figures Raúl mentioned were what had been spent so far this year, "
                   "not budgets (Tereza, 13 Oct 2026). Google was €89.7k and Meta $178.1k at 30 Sep.")
    note(s, "A44", "Each spend row is converted with the rate of its month. Budget lines in another currency use the average rate.")
    dv = DataValidation(type="list", formula1='"EUR,USD"', allow_blank=False); s.add_data_validation(dv)
    for ref in ["C6", "C16", "C17", "C18", "B22", "B23", "B24", "B25"]:
        dv.add(ref)
    dv2 = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False); s.add_data_validation(dv2)
    dv2.add("C22:C25")
    widths(s, {"A": 28, "B": 16, "C": 18, "D": 18, "E": 58})


# ---------------------------------------------------------------------------------------------
def data_tabs(ws, rows):
    spec = {
        "Meta": ("Meta Ads – daily spend by campaign, as billed (USD)",
                 "Columns A–F, in this order: Day · Campaign name · Amount spent · Impressions · Link clicks · Website registrations completed"),
        "Google Ads": ("Google Ads – daily spend by campaign, as billed (EUR)",
                       "Columns A–F, in this order: Day · Campaign · Cost · Impr. · Clicks · Conversions"),
        "ChatGPT Ads": ("ChatGPT Ads – daily spend by campaign, as billed (EUR)",
                        "Columns A–F, in this order: date · campaign_name · spend · impressions · clicks · conversions"),
        "LinkedIn Ads": ("LinkedIn Ads – daily spend by campaign, as billed",
                         "Columns A–F, in this order: Start date · Campaign name · Total spent · Impressions · Clicks · Conversions"),
    }
    by_ch = collections.defaultdict(list)
    for r in rows:
        by_ch[r["channel"]].append(r)
    for name, tab, srow, bill, *_ in CHANNELS:
        w = ws[tab]
        t, how = spec[name]
        cell(w, "A1", t + " — paste each week's export under the last row (columns A–F only).", bold=True, color=NAVY, border=False)
        w.merge_cells("A1:I1")
        header(w, 2, 1, ["Date", "Campaign", f"Spend ({bill})", "Impressions", "Clicks", "Conversions", "Row type",
                         "In campaign list?", '="Spend ("&Settings!$C$6&")"'], fill=INPUT, color=INK)
        data = sorted(by_ch.get(name, []), key=lambda r: (r["date"], r["campaign"]))
        for i, r in enumerate(data):
            n = 3 + i
            w.cell(n, 1, r["date"]).number_format = "yyyy-mm-dd"
            w.cell(n, 2, r["campaign"])
            w.cell(n, 3, round(r["spend"], 2)).number_format = "#,##0.00"
            w.cell(n, 4, int(r["impr"])).number_format = "#,##0"
            w.cell(n, 5, int(r["clicks"])).number_format = "#,##0"
            w.cell(n, 6, round(r["conv"], 2)).number_format = "#,##0.##"
            if r.get("rowtype"):
                w.cell(n, 7, r["rowtype"])
        last = HELPER_ROWS if name in ("Meta", "Google Ads") else 2000
        for n in range(3, last + 1):
            w.cell(n, 8, f'=IF(B{n}="","",IF(COUNTIF(Campaigns!$A${CAMP_FIRST}:$A${CAMP_LAST},B{n})>0,"✓","⚠ add to Campaigns tab"))')
            f = f"INDEX({S_FX},MONTH(A{n}))"
            c = w.cell(n, 9, f'=IF(C{n}="","",C{n}*IF(Settings!$B${srow}=Settings!$C$6,1,IF(Settings!$B${srow}="USD",1/{f},{f})))')
            c.number_format = "#,##0.00"
        w.conditional_formatting.add(f"H3:H{last}", FormulaRule(formula=['LEFT(H3,1)="⚠"'], font=font(bold=True, color=RED)))
        w.freeze_panes = "A3"
        widths(w, {"A": 12, "B": 62, "C": 14, "D": 13, "E": 11, "F": 12, "G": 12, "H": 22, "I": 14})
        note(w, "K2", how)
        note(w, "K3", "Row type: leave empty for daily rows. 'Month total' marks the Jan–Sep history (one row per campaign per month); "
                      "if you ever paste daily rows for those months, delete their 'Month total' rows first.")


# ---------------------------------------------------------------------------------------------
def campaigns(c, rows):
    title(c, "A1", "Campaigns – market, region, type and spend by month",
          "Every campaign in the data tabs needs a row here. Yellow = type it in when a new campaign starts. "
          "Market and region come from the location code in the campaign name.", "A2")
    for i in range(12):
        col = L(6 + i)
        cell(c, f"{col}3", f"=DATE({S_YEAR},{i + 1},1)", "d mmm", size=8, color=MUTED, border=False, align="center")
        cell(c, f"{col}4", f"=EOMONTH({col}3,0)", "d mmm", size=8, color=MUTED, border=False, align="center")
    cell(c, "A3", "Check – spend in the data tabs that is missing from this list:", bold=True, border=False, size=9)
    cell(c, "D3", "=Calc!C46-R6", AMT, bold=True, border=False)
    cell(c, "E3", '=IF(ABS(D3)<0.5,"✓ all listed","⚠ add the campaigns flagged in the data tabs")', bold=True, border=False, size=9)
    c.conditional_formatting.add("E3", FormulaRule(formula=['LEFT(E3,1)="⚠"'], font=font(bold=True, color=RED)))
    hdr = ["Campaign", "Channel", "Market", "Region", "Type"] + [f'=TEXT({L(6 + i)}3,"mmm")' for i in range(12)] + \
          [f'="Total ("&{S_CUR}&")"', "Clicks", "Conversions", "Cost per conversion"]
    header(c, 5, 1, hdr)
    cell(c, "A6", "Total – all campaigns listed", bold=True, fill=TOTAL)
    for col in "BCDE":
        cell(c, f"{col}6", "", fill=TOTAL)
    for j in range(6, 21):
        col = L(j)
        cell(c, f"{col}6", f"=SUM({col}{CAMP_FIRST}:{col}{CAMP_LAST})", AMT if j < 19 else "#,##0", bold=True, fill=TOTAL)
    cell(c, "U6", '=IF(T6=0,"",R6/T6)', AMT2, bold=True, fill=TOTAL)
    tot = collections.OrderedDict()
    for r in rows:
        k = (r["channel"], r["campaign"])
        tot[k] = tot.get(k, 0) + to_usd(r)
    order = {n: i for i, (n, *_) in enumerate(CHANNELS)}
    camps = sorted(tot, key=lambda k: (order[k[0]], -tot[k]))
    for i in range(len(camps) + 40):
        r = CAMP_FIRST + i
        if i < len(camps):
            ch, name = camps[i]
            mk, rg = CM.location(name)
            vals = [name, ch, mk, rg, CM.ctype(ch, name)]
        else:
            vals = [None] * 5
        for j, v in enumerate(vals):
            cell(c, f"{L(1 + j)}{r}", v, fill=INPUT, color="0000FF" if v else INK)
        for m in range(12):
            col = L(6 + m)
            f = "0"
            for name_, tab, *_ in reversed(CHANNELS):
                expr = sumifs(tab, "I", f"{col}$3", f"{col}$4", f",'{tab}'!$B$3:$B${DMAX},$A{r}")
                f = f'IF($B{r}="{name_}",{expr},{f})'
            cell(c, f"{col}{r}", f'=IF($A{r}="","",{f})', AMT)
        cell(c, f"R{r}", f'=IF($A{r}="","",SUM(F{r}:Q{r}))', AMT, bold=True)
        for colx, src in (("S", "E"), ("T", "F")):
            f = "0"
            for name_, tab, *_ in reversed(CHANNELS):
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
         "How market and region were set: from the location code in the campaign name (e.g. 'Geo:EMEA', 'Geo:FR', 'Texas_EN_…'). "
         "Geo:SA = Middle East (Saudi Arabia), as in the 2026/09 location file; Geo:NA = US & Canada; "
         "'Geo:US-UK-FR-IT', 'WW' and 'All' = Worldwide. 'Test 1' (ChatGPT) has no location in its name.")


# ---------------------------------------------------------------------------------------------
def agency_tab(a, weeks, totals):
    title(a, "A1", "Agency weekly reports (Notion) – as written, with the issues found", None)
    note(a, "A2", "Source: the agency's weekly reports in Notion, read on 13 Oct 2026 (nothing edited). Spend, leads and CPL are copied as the agency wrote them; "
                  "lead definitions change over the year, so leads and CPL are not comparable week to week. The official spend numbers are the platform exports.")
    section(a, "A4", "WEEK BY WEEK", "ABCDEFGHIJKLMNO")
    hdr = ["Week starts", "Week ends", "Meta spend (agency, $)", "Meta leads (agency)", "Meta lead definition", "Meta CPL (agency)",
           "Google spend (agency, as written)", "Google currency (as written)", "Google leads (agency)", "Google CPL (agency)",
           "Issues found", "What the agency did or recommended", "Meta – platform, same week (USD)", "Google – platform, same week (EUR)",
           "Meta: agency − platform"]
    header(a, 5, 1, hdr, height=44)
    first = 6
    for i, w in enumerate(weeks):
        r = first + i
        cell(a, f"A{r}", w["start"], DATE_F)
        cell(a, f"B{r}", w["end"], DATE_F)
        cell(a, f"C{r}", w.get("meta_spend"), AMT2, color="0000FF")
        cell(a, f"D{r}", w.get("meta_leads"), "#,##0.##")
        cell(a, f"E{r}", w.get("meta_def"), size=8, wrap=True)
        cell(a, f"F{r}", w.get("meta_cpl"), size=9, align="right")
        cell(a, f"G{r}", w.get("google_spend"), AMT2, color="0000FF")
        cell(a, f"H{r}", w.get("google_cur"), align="center", size=9)
        cell(a, f"I{r}", w.get("google_leads"), "#,##0.##")
        cell(a, f"J{r}", w.get("google_cpl"), size=9, align="right")
        cell(a, f"K{r}", w.get("flags"), size=8, wrap=True, color=RED if w.get("flags") else INK)
        cell(a, f"L{r}", w.get("notes"), size=8, wrap=True)
        cell(a, f"M{r}", f"={sumifs('Meta data', 'C', f'$A{r}', f'$B{r}', daily=True)}", AMT2)
        cell(a, f"N{r}", f"={sumifs('Google data', 'C', f'$A{r}', f'$B{r}', daily=True)}", AMT2)
        cell(a, f"O{r}", f'=IF(OR(C{r}="",M{r}=0),"",C{r}-M{r})', AMT2)
        a.row_dimensions[r].height = 54
    last = first + len(weeks) - 1
    note(a, f"A{last + 1}", "Platform columns fill in once daily platform exports are pasted in the data tabs (they only use daily rows).")
    top = last + 3
    section(a, f"A{top}", "WHAT THE AGENCY SAID IN TOTAL vs. THE PLATFORM EXPORTS", "ABCDEFGHIJKLMNO")
    header(a, top + 1, 1, ["Period", "", "What the agency wrote", "", "Agency figure ($)", "Platform – Meta (USD)", "Platform – Google (EUR)",
                           '="Platform – total ("&' + S_CUR + '&")"', "Agency − platform", "Difference", "Note", "", "", "", ""], height=36)
    for i, t in enumerate(totals):
        r = top + 2 + i
        a.merge_cells(f"A{r}:B{r}"); a.merge_cells(f"C{r}:D{r}"); a.merge_cells(f"K{r}:O{r}")
        cell(a, f"A{r}", t["period"], bold=True); cell(a, f"B{r}", None)
        cell(a, f"C{r}", t["quote"], size=8, wrap=True); cell(a, f"D{r}", None)
        cell(a, f"E{r}", t["agency"], AMT2, color="0000FF")
        lo, hi = t["lo"], t["hi"]
        dlo, dhi = f"DATE({lo.year},{lo.month},{lo.day})", f"DATE({hi.year},{hi.month},{hi.day})"
        meta_u = sumifs("Meta data", "I", dlo, dhi)
        goog_u = sumifs("Google data", "I", dlo, dhi)
        cell(a, f"F{r}", f"={sumifs('Meta data', 'C', dlo, dhi)}" if t["chan"] in ("both", "meta") else None, AMT2)
        cell(a, f"G{r}", f"={sumifs('Google data', 'C', dlo, dhi)}" if t["chan"] in ("both", "google") else None, AMT2)
        parts = ([meta_u] if t["chan"] in ("both", "meta") else []) + ([goog_u] if t["chan"] in ("both", "google") else [])
        cell(a, f"H{r}", "=" + "+".join(parts), AMT2, bold=True)
        cell(a, f"I{r}", f'=IF({S_CUR}="USD",E{r}-H{r},"")', AMT2, bold=True)
        cell(a, f"J{r}", f'=IF(OR({S_CUR}<>"USD",H{r}=0),"",E{r}/H{r}-1)', '+0%;-0%;0%', align="center", size=9)
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
               "M": 13, "N": 13, "O": 12})
    ctop = nr + 3
    section(a, f"A{ctop}", "WEEKLY SPEND AS THE AGENCY REPORTED IT", "ABCDEFGHIJ")
    ch = BarChart(); ch.type = "col"; ch.grouping = "clustered"; ch.gapWidth = 40
    ch.add_data(Reference(a, min_col=3, min_row=5, max_row=last), titles_from_data=True)
    ch.add_data(Reference(a, min_col=7, min_row=5, max_row=last), titles_from_data=True)
    ch.set_categories(Reference(a, min_col=16, min_row=first, max_row=last))
    style_bar(ch, [CH_COLORS["Meta"], CH_COLORS["Google Ads"]])
    ch.width, ch.height = 30, 9
    a.add_chart(ch, f"A{ctop + 1}")
    note(a, f"A{ctop + 19}", "Meta in $ as reported (excludes FR_Alibaba from 7 Sep). Google as written: labelled $ before 21 Sep, but later "
                             "reports show the same numbers in €, so treat them as euros. Weeks without a bar had no spend in the report.")
    for i in range(len(weeks)):
        cell(a, f"P{first + i}", f'=TEXT(A{first + i},"d mmm")', size=8, color=MUTED, align="center")
    cell(a, "P5", "Chart label", bold=True, color=WHITE, fill=NAVY, align="center", size=9)
    idx = [first + i for i, w in enumerate(weeks) if w.get("meta_spend") and w.get("google_cur") == "€"][-3:]
    return dict(first=first, last=last, pace_rows=idx)


# ---------------------------------------------------------------------------------------------
def calc(k, arow):
    title(k, "A1", "Calculations used by the Dashboard – don't edit", "Shown so every Dashboard number can be checked.", "A2")
    items = [
        (3, "Platform data up to", f"={S_UPTO}", DATE_F),
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
    hdr = ["Channel", "Counts toward budget?", "Spent to date", "Spent last full month", "Spent last 3 full months",
           "Spent last full week (daily rows)", "Spent last 3 full weeks (daily rows)", "Share of spend"]
    header(k, 19, 2, hdr)
    for i, (name, tab, srow, *_) in enumerate(CHANNELS):
        r = 20 + i
        cell(k, f"B{r}", name, bold=True)
        cell(k, f"C{r}", f"=Settings!C{srow}", align="center")
        cell(k, f"D{r}", f"={sumifs(tab, 'I', '$C$4', 'MIN($C$3,$C$5)')}", AMT)
        cell(k, f"E{r}", f"={sumifs(tab, 'I', '$C$11', '$C$10')}", AMT)
        cell(k, f"F{r}", f"={sumifs(tab, 'I', '$C$12', '$C$10')}", AMT)
        cell(k, f"G{r}", f"={sumifs(tab, 'I', '$C$14', '$C$13', daily=True)}", AMT)
        cell(k, f"H{r}", f"={sumifs(tab, 'I', '$C$15', '$C$13', daily=True)}", AMT)
        cell(k, f"I{r}", f'=IF($D$25=0,"",D{r}/$D$25)', "0.0%")
    cell(k, "B24", "Total – counts toward budget", bold=True, fill=TOTAL)
    cell(k, "B25", "Total – all channels", bold=True, fill=TOTAL)
    cell(k, "C24", "", fill=TOTAL); cell(k, "C25", "", fill=TOTAL)
    for col in "DEFGH":
        cell(k, f"{col}24", f'=SUMIFS({col}20:{col}23,$C$20:$C$23,"Yes")', AMT, bold=True, fill=TOTAL)
        cell(k, f"{col}25", f"=SUM({col}20:{col}23)", AMT, bold=True, fill=TOTAL)
    cell(k, "I24", '=IF($D$25=0,"",D24/$D$25)', "0.0%", fill=TOTAL); cell(k, "I25", "", fill=TOTAL)

    a = "'Agency reports'!"
    pr = arow["pace_rows"]
    if len(pr) == 3:
        meta = "+".join(f"{a}C{r}" for r in pr)
        goog = "+".join(f"{a}G{r}" for r in pr)
        fx = f"INDEX({S_FX},MONTH({a}A{pr[-1]}))"
        agency_pace = f'=(({meta})*IF({S_CUR}="USD",1,1/{fx})+({goog})*IF({S_CUR}="USD",{fx},1))/3'
        agency_label = f'="the agency reports for W/C "&TEXT({a}A{pr[0]},"d mmm")&" – "&TEXT({a}A{pr[-1]},"d mmm")&" (after the September cuts)"'
    else:
        agency_pace, agency_label = "=0", '=""'
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
        (37, "Weekly pace – platform, last 3 full weeks (budget channels)", "=H24/3", AMT),
        (38, "Weekly pace – agency reports, last 3 clean weeks", agency_pace, AMT),
        (39, "Current weekly pace used", "=IF(C37>0,C37,C38)", AMT),
        (40, "Source of the current pace", '=IF(C37>0,"the platform exports, last 3 full weeks",C41)', None),
        (41, "Agency weeks used", agency_label, None),
        (42, "Forecast year-end at the current pace", "=C30+C39*C16", AMT),
        (43, "Allowed per week to land on the budget", "=IF(C16<=0,0,C31/C16)", AMT),
        (44, "Allowed per week to land on the maximum", "=IF(C16<=0,0,C32/C16)", AMT),
        (45, "Last full month (budget channels)", "=E24", AMT),
        (46, "All spend in the data tabs (any date)", "=" + "+".join(f"SUM('{t}'!$I$3:$I${DMAX})" for n, t, *_ in CHANNELS), AMT),
        (47, "Forecast year-end at last month's pace", "=C30+E24/C17*C8", AMT),
        (48, "Last full week, budget channels (daily rows)", "=G24", AMT),
    ]
    for r, lab, f, fmt in rows:
        cell(k, f"B{r}", lab)
        cell(k, f"C{r}", f, fmt)
    widths(k, {"A": 2, "B": 52, "C": 16, **{c: 14 for c in "DEFGHI"}})


# ---------------------------------------------------------------------------------------------
def monthly(m):
    title(m, "A1", "Monthly spend", None)
    cell(m, "A2", f'="Amounts in "&{S_CUR}&" · Google converted from EUR with the Settings rates · platform data up to "&TEXT({S_UPTO},"d mmm yyyy")',
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
        for j, (name, tab, srow, *_) in enumerate(CHANNELS):
            cell(m, f"{L(3 + j)}{r}", f"={sumifs(tab, 'I', f'$A{r}', f'EOMONTH($A{r},0)')}", AMT)
        cell(m, f"G{r}", f"=SUM(C{r}:F{r})", AMT, bold=True)
        cell(m, f"H{r}", "=" + "+".join(f"{L(3 + j)}{r}*{counts(srow)}" for j, (n, t, srow, *_) in enumerate(CHANNELS)), AMT)
        cell(m, f"I{r}", f"={S_BUDGET}*MAX(0,MIN(EOMONTH($A{r},0),{S_PEND})-MAX($A{r},{S_PSTART})+1)/({S_PEND}-{S_PSTART}+1)", AMT)
        cell(m, f"J{r}", f'=IF(EOMONTH($A{r},0)>{S_UPTO},"",H{r}-I{r})', AMT)
        cell(m, f"K{r}", f'=IF($A{r}>{S_UPTO},"",SUM($H$5:H{r}))', AMT)
        cell(m, f"L{r}", f"=SUM($I$5:I{r})", AMT)
        cell(m, f"M{r}", f"={S_MAX}", AMT, color=INK2)
        cell(m, f"N{r}", f'=IF(OR(K{r}="",{S_BUDGET}=0),"",K{r}/{S_BUDGET})', PCT, align="center")
        cell(m, f"O{r}", f'=IF(EOMONTH($A{r},0)<={S_UPTO},"Complete",IF($A{r}<={S_UPTO},"In progress","Not started"))', align="center", size=9)
        cell(m, f"P{r}", f"={sumifs('Meta data', 'C', f'$A{r}', f'EOMONTH($A{r},0)')}", AMT)
        cell(m, f"Q{r}", f"={sumifs('Google data', 'C', f'$A{r}', f'EOMONTH($A{r},0)')}", AMT)
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
    groups = [("Meta", "Meta data", "C"), ("Google Ads", "Google data", "D"), ("ChatGPT Ads", "ChatGPT data", "E")]
    cell(m, "A22", "", fill=NAVY); cell(m, "A23", "Month", bold=True, color=WHITE, fill=NAVY, align="center")
    for g, (name, tab, scol) in enumerate(groups):
        c0 = 2 + g * 4
        m.merge_cells(start_row=22, start_column=c0, end_row=22, end_column=c0 + 3)
        cell(m, f"{L(c0)}22", name, bold=True, color=WHITE, fill=NAVY, align="center")
        header(m, 23, c0, ["Clicks", "Conversions", "Cost per click", "Cost per conversion"])
    for i in range(12):
        r = 24 + i
        cell(m, f"A{r}", f"=A{5 + i}", MON_F, bold=True)
        for g, (name, tab, scol) in enumerate(groups):
            c0 = 2 + g * 4
            cl, cv, cpc, cpl = L(c0), L(c0 + 1), L(c0 + 2), L(c0 + 3)
            cell(m, f"{cl}{r}", f"={sumifs(tab, 'E', f'$A{r}', f'EOMONTH($A{r},0)')}", "#,##0")
            cell(m, f"{cv}{r}", f"={sumifs(tab, 'F', f'$A{r}', f'EOMONTH($A{r},0)')}", "#,##0")
            cell(m, f"{cpc}{r}", f'=IF({cl}{r}=0,"",{scol}{5 + i}/{cl}{r})', AMT2)
            cell(m, f"{cpl}{r}", f'=IF({cv}{r}=0,"",{scol}{5 + i}/{cv}{r})', AMT2)
    cell(m, "A36", "Total", bold=True, fill=TOTAL)
    for g, (name, tab, scol) in enumerate(groups):
        c0 = 2 + g * 4
        cl, cv, cpc, cpl = L(c0), L(c0 + 1), L(c0 + 2), L(c0 + 3)
        cell(m, f"{cl}36", f"=SUM({cl}24:{cl}35)", "#,##0", bold=True, fill=TOTAL)
        cell(m, f"{cv}36", f"=SUM({cv}24:{cv}35)", "#,##0", bold=True, fill=TOTAL)
        cell(m, f"{cpc}36", f'=IF({cl}36=0,"",{scol}17/{cl}36)', AMT2, bold=True, fill=TOTAL)
        cell(m, f"{cpl}36", f'=IF({cv}36=0,"",{scol}17/{cv}36)', AMT2, bold=True, fill=TOTAL)
    note(m, "A37", "Conversions use each platform's own definition: Meta = 'Website registrations completed'; Google Ads = 'Conversions' "
                   "(its primary conversion actions, which the agency changed during the year). Compare each channel with itself, not with each other.")
    m.freeze_panes = "B5"
    widths(m, {"A": 11, "B": 8, **{c: 12 for c in "CDEFGHIJKLMNOPQ"}, "R": 10, "S": 8, "T": 10, "U": 12})


# ---------------------------------------------------------------------------------------------
def weekly(w, notes):
    title(w, "A1", "Weekly spend", None)
    cell(w, "A2", f'="Weeks run Monday to Sunday · amounts in "&{S_CUR}&" · from the daily platform exports. Yellow columns are typed by you."',
         size=9, color=INK2, border=False, italic=True)
    cell(w, "A3", "Data up to:", size=8, color=MUTED, border=False)
    cell(w, "C3", f"={S_UPTO}", DATE_F, size=8, color=MUTED, border=False)
    cell(w, "D3", "Last full week ends:", size=8, color=MUTED, border=False)
    cell(w, "F3", "=Calc!C13", DATE_F, size=8, color=MUTED, border=False)
    cell(w, "H3", "Spend before October fills in once the daily platform exports are pasted. Until then, the agency's weekly figures are on "
                  "the 'Agency reports' tab and their notes are in column R.", size=9, bold=True, color=AMBER, border=False)
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
        for j, (name, tab, srow, *_) in enumerate(CHANNELS):
            cell(w, f"{L(4 + j)}{r}", f"={sumifs(tab, 'I', f'$B{r}', f'$C{r}', daily=True)}", AMT)
        cell(w, f"H{r}", f"=SUM(D{r}:G{r})", AMT, bold=True)
        cell(w, f"I{r}", "=" + "+".join(f"{L(4 + j)}{r}*{counts(srow)}" for j, (n, t, srow, *_) in enumerate(CHANNELS)), AMT)
        cell(w, f"J{r}", f"={S_BUDGET}*MAX(0,MIN(C{r},{S_PEND})-MAX(B{r},{S_PSTART})+1)/({S_PEND}-{S_PSTART}+1)", AMT)
        cell(w, f"K{r}", f'=IF(OR(C{r}>$C$3,I{r}=0),"",I{r}-J{r})', AMT)
        cell(w, f"L{r}", f"={sumifs('Meta data', 'F', f'$B{r}', f'$C{r}', daily=True)}", "#,##0")
        cell(w, f"M{r}", f'=IF(L{r}=0,"",D{r}/L{r})', AMT2)
        cell(w, f"N{r}", f"={sumifs('Google data', 'F', f'$B{r}', f'$C{r}', daily=True)}", "#,##0")
        cell(w, f"O{r}", f'=IF(N{r}=0,"",E{r}/N{r})', AMT2)
        cell(w, f"P{r}", None, "#,##0", fill=INPUT, color="0000FF")
        cell(w, f"Q{r}", None, "#,##0", fill=INPUT, color="0000FF")
        start = datetime.date(2025, 12, 29) + datetime.timedelta(days=7 * i)
        txt = notes.get(start)
        cell(w, f"R{r}", ("Agency: " + txt) if txt else None, fill=INPUT, color="0000FF", wrap=True, size=8)
        cell(w, f"S{r}", f'=TEXT(B{r},"d mmm")', size=8, color=MUTED, align="center")
        w.row_dimensions[r].height = 36 if txt else 15
    note(w, "A59", "Week 1 includes the last days of the previous year. Over/under plan is shown for complete weeks with data. "
                   "Notes marked 'Agency:' are summarised from the agency's weekly reports.")
    w.conditional_formatting.add("A5:Q57", FormulaRule(formula=["$B5>$C$3"], font=font(color=MUTED)))
    w.conditional_formatting.add("A5:Q57", FormulaRule(formula=["$C5=$F$3"], fill=PatternFill("solid", fgColor="E2EFDA"), font=font(bold=True)))
    w.conditional_formatting.add("K5:K57", FormulaRule(formula=["AND(ISNUMBER(K5),K5>0)"], font=font(bold=True, color=RED)))
    w.freeze_panes = "D5"
    widths(w, {"A": 6, "B": 11, "C": 11, **{c: 11 for c in "DEFGHIJKLMNO"}, "P": 12, "Q": 12, "R": 70, "S": 8})
    ch = BarChart(); ch.type = "col"; ch.grouping = "stacked"; ch.overlap = 100; ch.gapWidth = 40
    for j in range(4):
        ch.add_data(Reference(w, min_col=4 + j, min_row=4, max_row=57), titles_from_data=True)
    ch.set_categories(Reference(w, min_col=19, min_row=5, max_row=57))
    style_bar(ch, [CH_COLORS[n] for n, *_ in CHANNELS])
    ch.width, ch.height = 30, 9
    section(w, "A61", "WEEKLY SPEND BY CHANNEL (platform data)", "ABCDEFGHIJ")
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


def value_labels(ch):
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ch.dataLabels.showSerName = ch.dataLabels.showCatName = ch.dataLabels.showLegendKey = False
    ch.dataLabels.numFmt = "#,##0"
    ch.dataLabels.position = "outEnd"


def ref_line(s, color=INK2, dash="dash", width=22225):
    s.graphicalProperties.line.solidFill = color
    s.graphicalProperties.line.width = width
    s.graphicalProperties.line.dashStyle = dash
    s.marker.symbol = "none"
    s.smooth = False


# ---------------------------------------------------------------------------------------------
def by_location(b, rows):
    title(b, "A1", "Spend by region, market and campaign type", None)
    cell(b, "A2", f'="Amounts in "&{S_CUR}&" · location and type come from the Campaigns tab (based on the campaign names) · platform data up to "&TEXT({S_UPTO},"d mmm yyyy")',
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
            cell(b, f"A{r}", k[0] if isinstance(k, tuple) else k, bold=True)
            if region_col:
                cell(b, f"B{r}", k[1], align="center", size=9)
            for mth in range(12):
                cell(b, f"{L(first_m + mth)}{r}", f"=SUMIFS({camp(L(6 + mth))},{camp(key_col)},$A{r})", AMT)
        rl, rt = r0 + len(keys), r0 + len(keys) + 1
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
            t = r == rt
            cell(b, f"{tc}{r}", f"=SUM({L(first_m)}{r}:{L(first_m + 11)}{r})", AMT, bold=True, fill=TOTAL if t else None)
            cell(b, f"{sc}{r}", f'=IF(${tc}${rt}=0,"",{tc}{r}/${tc}${rt})', PCT, fill=TOTAL if t else None, align="center")
            cell(b, f"{bc}{r}", "" if t else f'=IF({sc}{r}="","",REPT("█",ROUND({sc}{r}*40,0)))', fill=TOTAL if t else None, color=INK2, size=8)
        return r0, rl, rt

    tot_m, tot_t, reg_of = collections.Counter(), collections.Counter(), {}
    for r in rows:
        mk, rg = CM.location(r["campaign"])
        tot_m[mk] += to_usd(r); reg_of[mk] = rg
        tot_t[CM.ctype(r["channel"], r["campaign"])] += to_usd(r)
    markets = [(m, reg_of[m]) for m, _ in tot_m.most_common()]
    types = [t for t, _ in tot_t.most_common()]
    reg = block(4, "BY REGION", "D", REGIONS, "Region")
    mkt = block(reg[2] + 3, "BY MARKET", "C", markets, "Market", region_col=True)
    block(mkt[2] + 3, "BY CAMPAIGN TYPE", "E", types, "Campaign type")
    b.freeze_panes = "B4"
    widths(b, {"A": 32, "B": 12, **{L(3 + i): 9.5 for i in range(12)}, "O": 11, "P": 11, "Q": 9, "R": 30})
    b.parent._loc = dict(region=reg, market=mkt, n_markets=len(markets))


# ---------------------------------------------------------------------------------------------
def how_to(h, source_note):
    title(h, "A1", "How to update this tracker", None)
    lines = [
        ("EVERY MONDAY (about 15 minutes)", None),
        ("1", "Google Ads → Reports → open the saved report 'PnP spend tracker' (Campaign × Day: Cost, Impr., Clicks, Conversions). "
              "Date range: last week (Mon–Sun). Download as CSV."),
        ("2", "Copy the rows (without the header) and paste them under the last row of the 'Google data' tab, starting in column A. "
              "Leave column G (Row type) empty."),
        ("3", "Meta Ads Manager → Campaigns → same date range → Breakdown: By time → Day → saved columns 'PnP spend tracker' "
              "(Campaign name, Amount spent, Impressions, Link clicks, Website registrations completed) → Export table data (CSV). "
              "Paste under the last row of 'Meta data'."),
        ("4", "If ChatGPT Ads or LinkedIn Ads ran, do the same for their tabs."),
        ("5", "Settings tab → change 'Platform data up to' to last Sunday."),
        ("6", "In the data tabs, column H must show ✓. If it says '⚠ add to Campaigns tab', add that campaign at the bottom of the "
              "Campaigns tab with its channel, market, region and type."),
        ("7", "Weekly tab → write 1–2 lines in 'Notes' for the week (launches, pauses, budget changes, anything unusual). "
              "Optional: add MQLs by channel from HubSpot."),
        ("8", "Dashboard → check the budget check rows and the forecast. Flag anything red to Raúl."),
        ("ONCE A MONTH (first Monday)", None),
        ("9", "Check last month's totals on the Monthly tab (columns 'Meta as billed' and 'Google as billed') against the billing pages "
              "(Meta: Billing & payments; Google Ads: Billing → Summary)."),
        ("10", "If Finance gives monthly EUR→USD rates, put them in the exchange-rate table on the Settings tab."),
        ("ONE-TIME SETUP", None),
        ("11", "Save the two reports described in steps 1 and 3, with the columns in exactly that order, so every week the export pastes straight in."),
        ("12", "Recommended: export Campaign × Day for 1 Jan – last Sunday once, delete the 'Month total' rows and paste the daily rows, "
               "so the Weekly tab shows the whole year from platform data."),
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
def dashboard(d):
    d.sheet_view.showGridLines = False
    widths(d, {"A": 2, **{L(2 + i): 12.5 for i in range(12)}, "N": 2})
    d.merge_cells("B1:M1")
    cell(d, "B1", '="Paid Media Spend "&' + S_YEAR + '&" – Year Overview"', size=18, bold=True, color=NAVY, border=False)
    d.row_dimensions[1].height = 30
    d.merge_cells("B2:M2")
    cell(d, "B2", f'="Platform data up to "&TEXT({S_UPTO},"d mmm yyyy")&" · amounts in "&{S_CUR}&" · Google converted from EUR at "&TEXT({S_FXAVG},"0.0000")&" · Meta, Google Ads and ChatGPT Ads"',
         size=9, color=INK2, border=False, italic=True)
    d.merge_cells("B3:M3")
    cell(d, "B3", f'="Budget: "&{S_STATUS}', size=9, bold=True, color=NAVY, fill="E8EEF7", border=False)
    d.row_dimensions[3].height = 20
    if DRAFT:
        d.merge_cells("B4:M4")
        cell(d, "B4", DRAFT_DASH, size=9, bold=True, color=RED, border=False)
    tiles = [
        (f'="BUDGET "&{S_YEAR}', f"={CUR('Calc!C27')}", f'="Maximum "&{CUR("Calc!C28")}&" · originally "&{CUR("Calc!C29")}'),
        ('="SPENT SO FAR"', f"={CUR('Calc!C30')}", f'=TEXT(Calc!C33,"0%")&" of budget · "&TEXT(Calc!C9,"0%")&" of the year gone"'),
        ('="LEFT IN THE BUDGET"', f'=IF(Calc!C31<0,"–"&{CUR("-Calc!C31")},{CUR("Calc!C31")})',
         f'=IF(Calc!C31<0,"Budget already used up","≈ "&{CUR("Calc!C43")}&" a week until "&TEXT(Calc!C5,"d mmm"))'),
        ('="LEFT UP TO THE MAXIMUM"', f'=IF(Calc!C32<0,"–"&{CUR("-Calc!C32")},{CUR("Calc!C32")})',
         f'=IF(Calc!C32<0,"Maximum already passed","≈ "&{CUR("Calc!C44")}&" a week until "&TEXT(Calc!C5,"d mmm"))'),
        ('="CURRENT PACE PER WEEK"', f"={CUR('Calc!C39')}", '=IF(Calc!C37>0,"Platforms, last 3 full weeks","Agency reports, last 3 weeks (after the cuts)")'),
        ('="FORECAST YEAR-END"', f"={CUR('Calc!C42')}",
         f'=IF(Calc!C42>Calc!C27,"▲ "&{CUR("Calc!C42-Calc!C27")}&" over budget","▼ "&{CUR("Calc!C27-Calc!C42")}&" under budget")&" · "&IF(Calc!C42>Calc!C28,"over","within")&" the maximum"'),
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
         '=IF(Calc!C30>=Calc!C27,"▲ Budget used up",IF(Calc!C42>Calc!C27,"▲ Ends ≈ "&' + CUR("Calc!C42-Calc!C27") + '&" over budget","● Ends within budget"))'),
        ("Maximum (ideally not more)", "Calc!C28", "Calc!C32", "Calc!C34",
         '=IF(Calc!C30>=Calc!C28,"▲ Maximum passed",IF(Calc!C42>Calc!C28,"▲ Ends ≈ "&' + CUR("Calc!C42-Calc!C28") + '&" over the maximum","● Ends ≈ "&' + CUR("Calc!C28-Calc!C42") + '&" under the maximum"))'),
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
    cell(d, "B13", f'="By "&TEXT(Calc!C3,"d mmm")&", "&{CUR("Calc!C30")}&" was spent: "&{CUR("ABS(Calc!C36)")}&IF(Calc!C36>=0," more"," less")&" than an even pace through the year ("&{CUR("Calc!C35")}&"). Current pace from "&Calc!C40&"."',
         size=9, color=INK2, border=False, italic=True, wrap=True)
    d.row_dimensions[13].height = 26
    d.conditional_formatting.add("K11:K12", FormulaRule(formula=['LEFT(K11,1)="▲"'], font=font(9, True, RED)))
    d.conditional_formatting.add("K11:K12", FormulaRule(formula=['LEFT(K11,1)="●"'], font=font(9, True, GREEN)))
    d.conditional_formatting.add("H11:H12", FormulaRule(formula=["G11>=1"], font=font(8, False, RED)))
    d.conditional_formatting.add("H11:H12", FormulaRule(formula=["AND(G11<1,G11>$P$2+0.05)"], font=font(8, False, AMBER)))

    section(d, "B15", "SPEND BY CHANNEL", [L(2 + i) for i in range(12)])
    d.merge_cells("B16:C16"); d.merge_cells("K16:M16")
    hdr = {"B": "Channel", "D": '="Spent ("&' + S_CUR + '&")"', "E": "Share", "F": "Last full month", "G": "Last 3 full months",
           "H": "Last full week", "I": "Counts toward budget?", "J": "Billing currency", "K": "Note"}
    for col in "BCDEFGHIJKLM":
        cell(d, f"{col}16", hdr.get(col), bold=True, color=WHITE, fill=NAVY, align="center", wrap=True, size=9)
    d.row_dimensions[16].height = 26
    for i, (name, tab, srow, bill, cnt, nt) in enumerate(CHANNELS):
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
        cell(d, f"K{r}", f'=IF(Settings!E{srow}="","",Settings!E{srow})', size=8, wrap=True)
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
    note(d, "B22", "'Last full week' needs daily platform rows: it shows – until the daily exports are pasted.")

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
                                                                       fill=PatternFill("solid", fgColor="E2EFDA")))

    top = 50
    section(d, f"B{top}", "YEAR-END OUTLOOK (budget channels)", [L(2 + i) for i in range(12)])
    for rr in range(top + 1, top + 6):
        d.merge_cells(f"B{rr}:E{rr}"); d.merge_cells(f"J{rr}:M{rr}")
    oh = {"B": "If we spend from now on at…", "F": '="Per week ("&' + S_CUR + '&")"', "G": "Year-end total", "H": "vs. budget",
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
    nshow = min(10, loc["n_markets"])
    mk = BarChart(); mk.type = "bar"; mk.gapWidth = 40
    mk.add_data(Reference(b, min_col=15, min_row=m0, max_row=m0 + nshow - 1), titles_from_data=False)
    mk.set_categories(Reference(b, min_col=1, min_row=m0, max_row=m0 + nshow - 1))
    style_bar(mk, [SLATE]); mk.legend = None; value_labels(mk)
    mk.x_axis.scaling.orientation = "maxMin"
    mk.width, mk.height = 16.2, 7
    d.add_chart(mk, f"H{top + 1}")
    note(d, f"B{top + 16}", "Region and market come from the location code in each campaign name – see the 'By location & type' and 'Campaigns' tabs. "
                            "Sources, exchange rate and how to update: 'How to update' tab.")
    d.column_dimensions["P"].hidden = True
    d.print_area = "A1:N74"
    d.print_options.horizontalCentered = True
    d.page_setup.orientation = "landscape"
    d.page_setup.fitToWidth = 1
    d.sheet_properties.pageSetUpPr.fitToPage = True
    d.page_setup.fitToHeight = 0


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


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "agency") if os.path.isdir(os.path.join(here, "agency")) else os.path.join(here, "..", "agency"))
    import load_monthly as LM, agency_weeks as AW
    out, upto = sys.argv[1], datetime.date.fromisoformat(sys.argv[2])
    DRAFT = "--draft" in sys.argv
    rows = LM.all_rows()
    for r in rows:
        r["rowtype"] = "Month total"
    src = ("Platform data: Meta ('Plug and Play Tech Center – Dollars' ad account, USD) and Google Ads (EUR) exports by campaign and month, "
           "1 Jan – 30 Sep 2026, exported 8 Oct 2026; each month is one 'Month total' row per campaign. ChatGPT Ads: 'Test 1', 23 Sep – 2 Oct 2026, "
           "€229.56 in total, put on its start date.\n"
           "Agency figures: the agency's weekly reports in Notion (W/C 29 Dec 2025 – 5 Oct 2026), read with Claude in Chrome on 13 Oct 2026, copied as written.\n"
           "Budget: Tereza, 13 Oct 2026 – $300k for 2026 (originally $350k), up to $320k at most. Exchange rate: 1 EUR = 1.1177 USD (live rate on 13 Oct 2026).")
    build(out, upto, rows, AW.weeks(), AGENCY_TOTALS, src)
    print("saved", out)
