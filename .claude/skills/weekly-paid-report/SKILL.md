---
name: weekly-paid-report
description: Build Plug and Play's weekly paid performance report (branded PDF plus a Slack/email summary) with the full content of Tereza's report – paid channels, YouTube, Search Console, Semrush, HubSpot leads, recommendations and actions – from Felipe's weekly exports. Use when Felipe asks for the weekly report, uploads the weekly exports, or says "weekly report".
---

# Weekly paid performance report

Felipe's weekly task from the week of 12–18 Oct 2026 (tracker: "Weekly paid performance report", from 19 Oct).

- **Content:** everything in Tereza's report, made clearer, never shorter. Read `report_spec.md` (in this folder) first: layout page by page, rules, the data needed and what the generator still lacks. Reference: `reports/weekly/reference/2026-10-05_Tereza_Paid_Performance_Report.md`.
- **Code:** `tools/weekly_report/build_weekly_report.py`, with settings in `tools/weekly_report/config.toml`. One folder per week: `reports/weekly/<Monday>/`. Format sample, not sent: `reports/weekly/sample-2026-10-05/`.

## What Felipe sends
The list in `report_spec.md` → "Data needed each week": Meta and Google exports (tracker files plus the week's ad, ad-group, search-term and video detail), Search Console, Semrush, HubSpot MQLs, and the status of last week's actions. ChatGPT or LinkedIn spend: add a row to `reports/weekly/other_channels.csv`, the same columns as the tracker's Other channels tab.

## Steps
1. Install the brand font: `tools/brand/install_fonts.sh` (skips if present).
2. **First run only (12–18 Oct):** extend the generator with the sections listed under "To add" in `report_spec.md`, using that week's real exports. Check every new number against its source before writing any text.
3. Create `reports/weekly/<Monday>/inputs.toml` from the previous week's file. Fill `[crm]` with the HubSpot numbers and `[[last_actions]]` with each status. For 12–18 Oct, last week's actions come from Tereza's report, not from the sample.
4. Run without `--pdf` and read the printed flags and `facts.json`:
   `python3 -I tools/weekly_report/build_weekly_report.py --week <Monday> --meta <meta.csv> --google <google.csv> --inputs reports/weekly/<Monday>/inputs.toml --out reports/weekly/<Monday>`
5. Write the text in `inputs.toml`, section by section as in the spec. Use `{{key}}` placeholders (`facts.json` → `fmt`) for every number from the exports. Type a number only when it comes from another source, and name that source in the data notes.
6. Run with `--pdf`. Fix every WARNING: replace symbols missing from the brand font, and check the page count against the spec. Render the pages to PNG and look at them.
7. Commit `inputs.toml`, the PDF, `facts.json` and `summary.md` (the HTML stays out of git), push, send Felipe the PDF and paste `summary.md` in the reply.

## Writing rules
- Plain language: the point first, positives before problems, one idea per bullet with its number and what to do about it.
- Compare with last week **and** the 4-week average; call small numbers small (under 10 leads = low volume).
- USD totals; Google and YouTube tables also in EUR. Write "Plug and Play" in full, never "PNP".
- HubSpot is read-only and aggregates only. Counts are shown exactly, as Tereza did. When in doubt, do what Tereza's report did.
- Leads = platform counts (Meta Results of lead campaigns, Google conversions); MQLs come from HubSpot. Never mix them.
