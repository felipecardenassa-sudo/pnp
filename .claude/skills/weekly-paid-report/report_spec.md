# Weekly paid performance report – content spec

**Rule (Felipe, 14 Oct 2026):** the report keeps everything Tereza's report shows – every section, table and metric
(reference: `reports/weekly/reference/2026-10-05_Tereza_Paid_Performance_Report.md`). The improvement is clarity,
visibility and ease of reading. Never cut sections or metrics to make it shorter.

Felipe owns the report from the week of **12–18 Oct 2026** (tracker task "Weekly paid performance report", from 19 Oct).

## Layout (A4, brand, about 5 pages; page 1 stands alone)

| Page | Content (Tereza's section in brackets) | Visual |
| --- | --- | --- |
| 1 · Summary | Header: logo, week, comparison week, sources line. Headline + subhead. Tiles: paid spend in USD (all channels incl. YouTube), leads (Meta + Google), cost per lead, MQLs with the paid share, organic clicks (Search Console), budget 2026. Cards: **What improved · What declined · Changed significantly**, data flags included (§1). **Top 5 focus list** (§6). | Tiles with arrows and 8-week lines; three short-bullet cards; numbered list |
| 2 · KPI breakdown (§2) | **Google Search**: spend, impressions, clicks, CTR, CPC, conversions (primary), CPA, conversion rate. **Meta account total**: spend, impressions, reach, link clicks, landing page views, CPM, frequency. **Meta lead campaigns** ("lead engine"): spend, leads, CPL, impressions, CPM, link clicks, link CTR. **YouTube** (all campaigns): spend, impressions, clicks, CTR, views, view rate, cost per view, CPV by region, conversions. **Biggest movers** strip. Budget block: spent to date, weekly pace, forecast, what fits the budget. | One table per channel: this week · last week · change (arrow) · 4-week average · note |
| 3 · Paid, channel by channel (§3) | **Meta**: lead campaigns (spend, leads, prior leads, CPL, prior CPL, 4-week CPL, result); best ad; retargeting ads; weak spots; red flags (traffic campaigns, campaign status, traffic share of spend). **Google Ads**: campaigns and ad groups (spend, clicks, conversions, CPA, prior conversions, prior CPA); brand ad groups and the "plug and play" term; NA vs EMEA ad groups; off-topic search terms with spend; Performance Max status. **YouTube**: each campaign's spend, impressions, views, CPV, view rate, completion, conversions; weeks in a row with zero conversions. | Campaign tables with arrows; short "so what" bullets under each |
| 4 · Organic (§3) | **Search Console**: clicks, impressions, CTR, average position desktop and mobile; devices; top countries; top pages (clicks, CTR, position); queries (brand "plug and play", brand total, watch list). **Semrush**: tracked keywords ranking (of total), median position, top 3, top 10, organic results, AI Overview citations, improved / declined / flat; page-level estimated traffic; gainers; losers. | Tiles + tables with arrows; gainers and losers side by side |
| 5 · Leads, actions, sources (§3 CRM, §4, §5, data sources) | **Lead quality**: MQLs by original source (this week, last week restated, change, disqualified, share), Watchleads, paid contribution, cost per paid MQL by source, disqualified share, net MQLs, SQLs when supplied. **Recommendations by channel** (Meta, Google Ads, YouTube, Organic): quick wins and strategic. **Accountability**: prioritise next week (owner, day), experiments to launch, monitor list, and last week's actions with their status (new). **Data sources & reconciliation**: source and window per platform, restatements, gaps, what wasn't pulled. | Tables; two-column quick wins / strategic; status chips |

## Rules
- Same content as Tereza's report, clearer: the point first, tables instead of numbers in sentences, one idea per bullet, plain words.
- USD totals everywhere. Google Ads and YouTube tables also show EUR, the platform's currency, so they match the Google Ads screen and Tereza's earlier reports.
- Compare every metric with last week and the 4-week average; mark low volume.
- HubSpot counts of 1–4 show as "<5" (CLAUDE.md GDPR rule), unless Felipe confirms the internal weekly report may show exact counts.
- Brand rules from CLAUDE.md; PDF embeds the brand font only.
- YouTube, Search Console and Semrush stay in this report (they were in Tereza's). The "leave YouTube out" rule is for audits, decks and plans.

## Data needed each week
1. **Meta**, campaign × day, 1 Jan – yesterday (the tracker's export).
2. **Meta**, report week and the week before: ad level (campaign, ad set, ad name, spend, results, result indicator, link clicks, impressions); account totals from the Ads Manager summary row (reach, frequency, impressions, CPM, link clicks, landing page views).
3. **Google Ads**, campaign × day (the tracker's export).
4. **Google Ads**, report week and the week before: ad groups (campaign, ad group, cost, impressions, clicks, conversions); search terms (term, campaign, ad group, match type, cost, clicks, conversions); keywords (for the brand terms); video campaigns (impressions, views, view rate, average CPV, video played to 100%, clicks, cost, conversions).
5. **Search Console**: Performance, custom range = the report week, compared with the week before; all tabs (queries, pages, countries, devices).
6. **Semrush**: Position Tracking for the report week (keywords, positions, changes, AI Overview) and the page-level estimated traffic. Felipe's access is pending; until then Tereza exports it.
7. **HubSpot** (read-only): MQLs by original source for the week and the week before (restated), disqualified by source, Watchleads; SQLs when Salesforce access allows.
8. **Felipe's notes**: what happened to last week's actions; changes during the week (budgets, launches, pauses).

## Generator status (14 Oct 2026)
- **Built** (`tools/weekly_report/build_weekly_report.py`): tiles (spend, leads, cost per lead, paid MQLs, budget), channel table, Meta and Google campaign tables, ads / ad groups / search terms from typed rows, CRM table and ratios, actions, last week's actions, decision box, data notes, brand checks. Sample: `reports/weekly/sample-2026-10-05/`. It was built from Tereza's week as a format sample and was not sent.
- **To add before the 12–18 Oct report** (build them with that week's real exports, then check every number): the Google Search KPI table (CTR, conversion rate); Meta account totals and the lead-engine table; the YouTube section; parsing of the Google ad-group, search-term and video exports and the Meta ad-level export; the Search Console section and organic tile; the Semrush section; the What improved / What declined / Changed significantly cards; biggest movers; recommendations by channel; experiments; monitor list; Top 5 focus list; data sources and reconciliation. The page check changes from "2 pages" to the new layout.

## First report: week of 12–18 Oct
- Last week's actions = Tereza's 5–11 Oct report: its "Prioritise next week" items, "Experiments to launch" and "Top 5 Focus List" (reference file, sections 5 and 6). Put them in `[[last_actions]]` and ask Felipe for each status. Don't use the sample folder's actions.
- Compare with 5–11 Oct. If HubSpot no longer gives the restated 5–11 Oct MQLs, use the table in Tereza's report and say so in the data notes.
