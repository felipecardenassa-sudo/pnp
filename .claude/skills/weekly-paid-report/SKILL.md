---
name: weekly-paid-report
description: Build Plug and Play's weekly paid media report (2-page branded PDF plus a Slack/email summary) from the Meta and Google campaign × day exports and the week's HubSpot MQL numbers. Use when Felipe asks for the weekly report, uploads the weekly exports, or says "weekly report".
---

# Weekly paid media report

Generator: `tools/weekly_report/build_weekly_report.py` · settings: `tools/weekly_report/config.toml` · one folder per week: `reports/weekly/<Monday>/` · example: `reports/weekly/2026-10-05/`.

## What Felipe sends (about 10 minutes on Monday)
1. **Meta export**: the same file as the spend tracker's weekly update (Ads Manager, campaign × day, 1 Jan to yesterday, CSV).
2. **Google Ads export**: the same saved report as the tracker (Campaign, Day, Currency code, Cost, Impr., Clicks, Conversions).
3. **HubSpot MQLs** (read-only report): MQLs by original source for the report week and the week before, the week's disqualified MQLs by source, SQLs if available. Aggregates only.
4. **What happened to last week's actions** (done / in progress / not done) and anything that changed (budgets, new ads, campaigns paused).
5. Optional, for the ads section: Meta ad-level export for the week (Campaign, Ad set, Ad name, Amount spent, Results, Result indicator, Link clicks, Impressions) and Google ad-group and search-term reports for the week.

ChatGPT or LinkedIn spend: add a row to `reports/weekly/other_channels.csv` (same columns as the tracker's Other channels tab).

## Steps
1. Brand font: run `tools/brand/install_fonts.sh` (installs Trebuchet MS; skips if present).
2. Create `reports/weekly/<Monday>/inputs.toml`, copying the structure of the last week's file. Fill `[crm]` with the HubSpot numbers. Put last week's actions under `[[last_actions]]` with Felipe's status. If he gave no status, leave them out: the generator shows them as "No update".
3. First run without `--pdf` and read the printed flags and `facts.json`:
   `python3 -I tools/weekly_report/build_weekly_report.py --week <Monday> --meta <meta.csv> --google <google.csv> --inputs reports/weekly/<Monday>/inputs.toml --out reports/weekly/<Monday>`
4. Write the text in `inputs.toml`: headline (one sentence: the main change and the MQL picture), subhead, max 3 `worked`, max 3 `fix`, max 5 `actions` with owner and due day, `decisions` only when Raúl or Tereza must decide. Use `{{key}}` placeholders (keys in `facts.json` → `fmt`) for every number that comes from the exports. Type a number only when it comes from another source, and say which in `data_notes`. From the optional exports, add `[[items]]` (best and worst ads, ad groups) and `[[negatives]]` (off-topic search terms).
5. Run again with `--pdf`. It must print "2 pages" and no WARNING lines. On "non-brand fonts", replace the symbol named; on "3 pages", shorten the text.
6. Check every typed number against its source. Render the pages to PNG and look at them.
7. Commit `inputs.toml`, the PDF, `facts.json` and `summary.md` (the HTML stays out of git), push, send Felipe the PDF and paste `summary.md` in the reply.

## Writing rules
- Plain language for managers: positives first, then what to fix, then actions. One idea per bullet, each with a number and what to do about it.
- Compare with last week **and** the 4-week average; call small numbers small (under 10 leads = low volume).
- USD only. Write "Plug and Play" in full, never "PNP" (brand rule).
- YouTube appears only as a spend line (brand views, not lead generation). LinkedIn is off. Organic search and Semrush are not part of this report.
- HubSpot: counts of 1–4 show as "<5". Read-only: never change anything in HubSpot.
- Leads = platform counts (Meta Results of lead campaigns, Google conversions); MQLs come from HubSpot. Never mix the two.
