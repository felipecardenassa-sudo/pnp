# Context for Claude – Performance Marketing & CRM at Plug and Play

## Who and what
- Felipe Cárdenas, Performance Marketing & CRM Associate (started early October 2026).
- **Manager: Raul (Raúl).** Tereza Pigova (Growth Marketing Director) is Raul's manager.
- Thiago "Toco" runs paid media until 30 Oct 2026 (leaving; handover doc due end of October).
- Platforms: Meta Ads, Google Ads (mostly Search), LinkedIn Ads (no spend since October 2025), ChatGPT (OpenAI) Ads, HubSpot (marketing CRM), Salesforce (sales), Playbook / Looker Studio (reporting).
- Living to-do tracker (Claude Docs, includes the 30/60/90 plan and who's who): https://claude.ai/code/artifact/c6deff91-4a61-4e7b-88ab-bcde7c269a1c
- Paid media best-practice research (Meta, Google, measurement): `research/Paid_Media_Playbook_2026.md`. Use it as the yardstick for audits and new campaign angles.

## 30/60/90-day plan (set by Raul) – key points
- **30 days:** learn PnP, its audience and the paid channel. Onboarding by area: brand (Amanda), ICP, content (Natalia, Anto), email (Raul, Rosa, vertical newsletter owners), paid (syncs with Raul and Toco, audit of 2026 paid accounts, budget per location, keyword positioning), landing pages (Aly, Rosa), HubSpot (lifecycle stages map), 10-day ChatGPT BOFU test for Startup Scouting, first talking head video, EMEA priority market calls, meet Andrew and Alex.
- **60 days:** own the channels. Take over the weekly paid performance report by week 3 (CPL, CPC, ROAS, MQLs by channel, based on Toco's report); vertical newsletters; audit location newsletters/LNS and nurture workflows; newsletter subscription project; launch talking head ads; AI Max / PMax test; keyword optimisation; competitor benchmark (paid + email); 2027 paid plan for YouTube and LinkedIn; GEO; first monthly leadership summary (what worked, what didn't, what's next).
- **90 days:** event emails audit (Sara), LinkedIn test, subscription types cleanup and compliance, LNS revamp, Paid Plan 2027 (Google, Meta, ChatGPT, YouTube, LinkedIn), 2026 funnel attribution report, Email marketing plan 2027.
- **KPIs by end of 2026:** Meta CPL −20%; MQLs from paid search +15%; MQLs converted with last source Email Marketing +25%.
- **Tools:** Google Ads, GTM, HubSpot, Matomo and OpenAI Ads OK. Meta Ads via Tereza. LinkedIn waiting for account restore. Salesforce and Semrush pending.

## Rules for every deliverable
- Keep it simple and fact-only, with no fluff and no assumptions. Fact-check every number before the final version.
- Spreadsheets must work in Google Sheets (the team uses Google Workspace only). Use plain SUM, IF and SUMIFS, and no XLOOKUP or macros.
- PDFs should be short and visual. Each one covers what's flagged, what's working, what can be improved and next steps.
- HubSpot access is **read-only audit**. Never create, edit, delete, send or change anything there.
- Follow GDPR:
  - Deliverables contain aggregates only, with counts of 1–4 shown as "<5".
  - Raw contact exports stay in the scratchpad and are deleted afterwards. Never commit them.

## Budget 2026 (USD) – confirmed by Tereza, 13 Oct 2026
- **Budget: $300k for 2026, in USD** (PnP talks budget in USD). Originally $350k; cut because performance wasn't good enough. **Maximum $320k, "ideally not more".**
- The "90k Google / 180k Meta" figures were **spend so far**, not budgets (Google €89.7k, Meta $178.1k at 30 Sep). The old EUR-based €270k assumption is wrong and its spreadsheet was removed.
- Report everything in USD. Meta bills in USD; Google Ads and ChatGPT Ads bill in EUR. Exchange rate used: 1 EUR = 1.1177 USD (live rate on 13 Oct 2026, from Felipe); monthly rates can be set on the tracker's Settings tab if Finance provides them.
- Counted toward the budget (to confirm): ChatGPT Ads and FR_Alibaba (a Meta campaign run by PnP's internal team, $3.7k in Sep).
- Status at 12 Oct (daily platform exports): $282,524 spent (94% of $300k). Current pace ≈ $1,861/week (last 3 full weeks 21 Sep – 11 Oct, campaigns still running; FR_Alibaba ended 5 Oct and is left out) → forecast ≈ $303.8k at year end (≈ $3.8k over budget, ≈ $16.2k under the maximum). Landing on $300k needs ≈ $1,529/week; the $320k maximum allows ≈ $3,279/week. FR_Alibaba (PnP's internal team) spent $4,491 from 10 Sep to 5 Oct.
- The agency's Notion reports, checked week by week against the platforms: Meta matches within $5 in 31 of 33 weeks (agency left FR_Alibaba out from 7 Sep); Google matched in only 11 of 32 weeks (10 converted to dollars at ≈1.15, 3 exactly doubled, 8 lower). H1: agency $182.5k vs $205.4k on the platforms. Platform exports are the source of truth.

## ICP (Buyer Persona 2024)
- Primary: corporates with 10,000+ employees and $100M+ revenue (Head of Innovation, R&D, CDO, or C-level), plus governments. A $500M threshold is under discussion.
- Secondary: startup founders.
- Measure conversion with Lead Status (SFDC), deals and customers. Don't use lifecycle stage, because 95% of contacts are SQL.

## Key numbers (from Tereza's deck, EMEA H1 2026)
- MQLs 954, SQLs 43, closed won 1, cost per SQL $2.1k (industry $2.5k).
- MQLs split 48% JTP Contact us and 52% content downloads.
- MQL → SQL takes 66 days (benchmark 15). Auto-disqualification breach rate is 15% (target 0).
- Key markets: France, UK, Germany, Spain, Italy. Local content beats generic content 3:1 on cost per lead.

## Files in this repo
- `PNP_Paid_Media_Spend_Tracker_2026.xlsx`: the spend tracker (USD, $300k budget / $320k maximum), v4. Weekly update (Update tab): replace the 'Meta export' and 'Google export' tabs with this year's campaign × day exports (File → Import → 'Replace data at selected cell'), check the 10 automatic ticks, write last week's note on the Weekly tab. The data date, market (location code in the campaign name → Settings → Locations), type (naming rules) and EUR→USD are automatic. Campaigns that stopped for good go on Settings → Ended campaigns (left out of the pace). ChatGPT/LinkedIn rows are typed on 'Other channels'. Hidden tabs: Data (reads the exports by column name, so moved columns don't matter) and Calc. `PNP_Paid_Media_Spend_2026.pdf`: 3-page summary for Tereza and Raúl (data to 12 Oct 2026).
- `PNP_HubSpot_Newsletter_Audit.pdf` / `.xlsx`: newsletter audit covering locations, newsletter map, metrics, workflows and industry newsletters (Oct 2025 – Sep 2026).
- `PNP_ICP_vs_Conversions.pdf` / `.xlsx`: JTP Contact us and content-download converters compared with the ICP (aggregates only).
- `tools/spend_tracker/`: generator for the tracker and the PDF. Run `python build_tracker.py OUT.xlsx META_EXPORT.csv GOOGLE_EXPORT.csv` (exports written as-is into the export tabs; data date automatic), recalc, then `python build_spend_pdf.py TRACKER.xlsx OUT.html` and print to PDF with Chromium. Exports: Meta Ads Manager CSV (campaign × day; needs Reporting starts, Campaign name, Amount spent (USD)), Google Ads report (Campaign, Day, Currency code, Cost, Impr., Clicks, Conversions; .csv or UTF-16 'Excel .csv'). The tracker reads up to 15,000 Meta rows and 7,000 Google rows (Meta was 30 rows a day in Oct 2026). `agency/` holds the parsed agency weekly reports. Last update: data to 12 Oct 2026.
