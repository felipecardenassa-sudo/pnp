# Paid Media Audit — Plug and Play Tech Center

Prepared for Felipe (Performance Marketing & CRM) · audit run on 14 Oct 2026 · read-only.

Goal used to judge everything below: leads from corporations with 10,000+ employees and $100M+ revenue (Head of Innovation, R&D, CDO, C-level) and from governments; startup founders are secondary.

Currencies are as shown in each platform: **Meta in USD**, **Google Ads in EUR**, **ChatGPT Ads in EUR**. "Not visible" means I could not see it.

---

## 0. Access and dates

### 0.1 What I could and could not open

| Area | Opened | Notes |
|---|---|---|
| Meta Ads Manager — account "Plug and Play Tech Center (Dollars)" 471277291299593 | Yes | Campaigns, ad sets, ads, read-only ad set panels |
| Meta Events Manager | Yes (late in the audit) | First attempts were blocked by the browser-extension site permission; it opened on 14 Oct via business.facebook.com |
| Meta Ad Library (page ID 6038767267) | Yes | Counts, matched IDs, one EU transparency panel |
| Meta Graph API | No | Blocked by the tool's safety filter, so everything comes from the UI |
| Meta Leads Center / lead downloads | Not opened on purpose | Contains personal data |
| Google Ads "Plug and Play" 133-450-4766 | Yes | Campaigns, ad groups, keywords, search terms, negatives, ads, assets, settings panels, change history, auction insights, recommendations, auto-apply, conversion actions |
| Google Ads Goals > "Leads (BETA)" | Not opened on purpose | May contain personal data |
| ChatGPT Ads (ads.openai.com, "Ads Manager Beta", account "Plug and Play") | Yes | Already logged in; campaigns, ad groups, ads, Conversions page, Diagnostics |
| ChatGPT Ads "Event Stream" tab | Not opened on purpose | May show user-level events |
| Landing pages (21 URLs) | Yes | Desktop window 1054 px wide; phone check = 390 px-wide copy of the page loaded inside the page; no form submitted |
| YouTube, Video, Demand Gen, Display, LinkedIn, HubSpot, Salesforce | Skipped as instructed | |

### 0.2 Dates used

| Label | Exact dates | Where |
|---|---|---|
| This year | 1 Jan 2026 – 13 Oct 2026 | Meta (URL `date=2026-01-01_2026-10-14`, UI shows "1 Jan 2026 - 13 Oct 2026"), Google Ads ("Jan 1 – Oct 13, 2026") |
| Last 30 days (L30D) | 14 Sep 2026 – 13 Oct 2026 | Meta and Google |
| Auction insights | Jan 1 – Oct 13, 2026 | NA and EMEA 20260813 only have data from 10 Aug 2026, so this equals "last 90 days" (16 Jul – 13 Oct) for them |
| Change history | Latest 50 entries per campaign (10 Aug – 10 Oct 2026) | Google NA and EMEA 20260813 |
| ChatGPT Ads | 1 Sep 2026 – 13 Oct 2026 | Covers the whole "Test 1" flight (23 Sep – 2 Oct) |
| Meta Events Manager | 16 Sep 2026 – 13 Oct 2026 | Platform default (28 days) |
| Landing pages | Checked 14 Oct 2026 | |

### 0.3 What I touched (full disclosure)

| Platform | What happened | Result |
|---|---|---|
| Meta | Opening the "Deep Tech" ad set panel (US-East-Coast/20260617) auto-created a draft ("Unpublished edits"). No field changed. | Reported to you at the time; you chose "Leave it, I'll handle it". On 14 Oct the "Review and publish" button was greyed out again. |
| Meta | Panels for "EMEA Politics/SpainGridReport" and "WW retargeting" also auto-created drafts while scrolling. | Discarded each one ("Discard Draft" → "Discard"), as you approved. |
| Meta | Panels for Brand (EMEA cbo), UK (EMEA abo) and EMEA Quantum. | Closed with "Close"; no draft appeared. |
| Meta | Ads Manager columns, date range, filters and a name search changed; Events Manager rows expanded. | View changes only, not saved as a view. |
| Google | I clicked **Dismiss** on the "Complete UK financial services verification" notice by mistake. | It is an informational banner; it cannot be undone from my side. Nothing in campaigns changed. |
| Google | An inline match-type dropdown opened by accident in the keyword table. | Closed with Escape; no change. |
| Google | A "Get to know conversion goals" guide popup appeared; I closed it ("Exit guide → Leave"). | UI guide only. |
| Google | Added Quality Score columns to the Keywords view, sorted tables, used filters and a 0.6 page zoom; opened Campaign settings side panels for NA and EMEA. | Panels closed with X, no prompt; nothing saved. The NA panel showed an AI Max block with Cancel/Save buttons; I did not touch it. |
| ChatGPT Ads | Changed the date range; ticked the Test 1 row checkbox (selection only); opened "Edit Campaign" to read settings. | Clicked **Cancel**; "Save" was greyed out (no change). |
| Websites | On /ultimate-innovation-platform I chose profiles in the form's first dropdown to see which fields appear, then reset it. | Nothing typed, nothing submitted. |
| Websites | Cookie banners: CookieYes banner did not appear because a consent choice was already stored in this browser before the audit. | I read the banner text from the page code; I could not click "Reject All". |
| Personal data | Google change history shows user e-mails. | Left out of this report; I only say "agency user" or "pnptc.com user". |

### 0.4 Background claims — confirmed or corrected

| Claim | What I saw | Verdict |
|---|---|---|
| Tracking off ~15 Jul – 11 Aug 2026 | Old Google campaigns stop delivering around mid-July and NA/EMEA start on 10 Aug 2026. I did not open a daily conversion breakdown. | Not verified |
| Google rebuilt on 13 Aug into NA/EMEA non-brand Search | Both campaigns are named "...Date:20260813" but their settings show **Start date: August 10, 2026**. Each contains a **Branding** ad group bidding on "plug and play". | Partly correct: start date 10 Aug; not purely non-brand |
| ~14 Sep goal switched to HubSpot qualified leads only; tCPA removed on NA | NA change history, **15 Sep 2026**: 3:48 PM "Standard goals changed — Contacts (Website) removed, Submit lead forms (Website) removed"; 3:59 PM "Target CPA was €30.00". **28 Sep 2026** 11:10 AM (Google Ads API / "Ads Perch (Unverified)"): "Qualified leads (Website) removed, Submit lead forms (Website) added" on both NA and EMEA. Today both campaigns show "Campaign-specific: Submit lead forms". | Correct for 15–28 Sep, then reversed. Today they do **not** optimise to HubSpot qualified leads |
| 10 Oct: EMEA Search got a tCPA of €45 | EMEA change history 10 Oct 2026, 10:21 PM: "Target CPA is €45.00"; settings: "Target CPA - €45.00"; all 4 ad groups show tCPA €45.00 | Confirmed |
| Meta budgets cut from $310 to $160/day on 18 Sep | Active Meta daily budgets today add up to **$154.68** (8 lead campaigns) + **$5.16** (traffic ad set) = **$159.84/day**. I did not open Meta's change history, so $310 and 18 Sep are not visible. Google budgets were cut on 19 Sep (NA €135 → €50, EMEA €104 → €43) and 21 Sep (NA €50 → €33, EMEA €43 → €30). | Current level confirmed; date and old level not visible |
| Case-study statics launched 8 Oct | The Mitsubishi × Kamet case-study ads I found (PP-366/368/369, names dated 202607) are **Off** with $0.58–$2.46 spend each. No case-study ad with spend could be tied to 8 Oct. | Not confirmed |
| Quantum = top ad in Jan | PP-50b "Quantum Computing – Green Screen Notes" is the top creative by spend this year (12+ copies, $6,767.35 in the UK ad set alone). I did not open a month-by-month view. | Top this year: yes. "January" not verified |
| Spanish "Grid" = top in Feb | The Grid ads are about **Spain's energy grid**, written in **English** (Ad Library: 0 Spanish-language ads). PP-67 "Spain Grid Report – Carousel" (name dated 202601) is among the cheapest ads (best $7.67/result). | Ad is English, not Spanish. "February" not verified |
| AICOI = May | TCb368 "AICOI" (name dated 08-2025): $2,067.97, 86 results, $24.05 in USCA 20251010. Its name says LP "AiCOE" but it links to the **quantum report**. | Ad exists; "May" not verified |
| PP-257 = Sept driver | PP-257 "Green screen AI & Robotics V1" is the top-spending ad this year in 3 of the 7 active geo campaigns and second in 2 more (all in Deep Tech ad sets). Deep Tech ad sets had the lowest cost per result in L30D ($4.36–$13.10). | Confirmed |
| PP-266 = to pause | PP-266 "Animated Voice Memo Osama 3 – AI in Healthcare" (→ /health-innovation-platform): 6 copies, $173.57 this year, 3 results. **5 of 6 copies are still Active or Learning limited.** | Exists; not paused yet |

### 0.5 Headline findings (one line each)

1. **Neither Meta nor Google optimises to qualified leads today.** Meta optimises to "welcome_conversions" (rule: URL contains "welcome"); Google NA/EMEA went back to "Submit lead forms" on 28 Sep.
2. **The biggest Google landing page is the homepage.** welcome.plugandplaytechcenter.com/ redirects to www.plugandplaytechcenter.com/ (no lead form): €2,969.63 (NA) + €2,841.09 (EMEA) this year.
3. **"Non-brand" Google spend is largely brand.** 44% of NA's visible search-term cost is "plug and play" variants; old campaigns spent 52–70% in brand ad groups.
4. **Ads and assets attract startups.** Top Google headline "Venture Capitalist"; sitelinks "Services For Startups", "For Mentors"; coworking structured snippets added on 10 Oct; founder-funding queries.
5. **41% of Meta's L30D spend ($3,845.18 of $9,305.68) went to "FR_Alibaba"**, a Traffic campaign buying $0.03 clicks in Turkey and Eastern Europe.
6. **Meta's best signals are Deep Tech report downloads** (PP-257, quantum) and EMEA/Middle-East CPMs. Several US Brand and Health ad sets cost $35–$140 per result in L30D (Brand US-California: $139.57 for 1 result).
7. **ChatGPT "Test 1" spent €229.56 for 0 conversions.** All ads went to the homepage with no tracking parameters, and only US was targeted.

---

## 1. Meta

Account "Plug and Play Tech Center (Dollars)" 471277291299593 · USD · time zone Europe/Madrid · 83 campaigns, 272 ad sets, 1,785 ads (243 ads currently active).

### 1.1 Campaign list

**This year (1 Jan – 13 Oct 2026), campaigns with spend, sorted by spend**

| Campaign | Status | Objective | Budget | Spend | Results (type) | Cost / result | Freq. | CPM | CTR (link) |
|---|---|---|---|---|---|---|---|---|---|
| EMEA/lead/prospecting/abo/20260210 | Off | Leads | Ad set budgets | $71,634.18 | 2,166 welcome_conversions | $33.07 | 4.69 | $20.22 | 1.51% |
| EMEA/lead/prospecting-test/cbo/20251010 | Off | Leads | $50.00/day | $18,000.68 | 1,437 welcome_conversions | $12.53 | 4.84 | $9.40 | 1.21% |
| US-EastCoast/lead/prospecting/cbo/20260409 | Off | Leads | $100.00/day | $15,706.69 | 335 welcome_conversion | $46.89 | 3.78 | $41.23 | 1.34% |
| WW/lead/retargeting/cbo/20260612 | Active (High performing) | Leads | $41.29/day | $12,038.71 | 513 Website completed registration | $23.47 | 5.75 | $17.04 | 1.17% |
| USCA/lead/prospecting/cbo/20251010 | Off | Leads | $70.00/day | $11,688.57 | 691 welcome_conversions | $16.92 | 3.58 | $30.14 | 1.36% |
| California/lead/prospecting-test/cbo/20260115 | Off | Leads | $90.00/day | $11,570.02 | — (multiple conversions) | — | 4.20 | $30.92 | 1.04% |
| US-California/lead/prospecting/cbo/20260602 | Active | Leads | $20.65/day | $6,592.56 | 207 welcome_conversions | $31.85 | 3.46 | $39.85 | 1.17% |
| US-East-Coast/lead/prospecting/cbo/20260617 | Active | Leads | $25.65/day | $5,501.14 | 236 welcome_conversions | $23.31 | 2.89 | $37.97 | 1.43% |
| FR_Alibaba Campaign | Completed | Traffic | Ad set $180/day | $4,491.00 | 130,358 link clicks | $0.03 | 6.62 | $0.54 | 1.55% |
| USCA/lead/prospecting/cbo/20260617 | Active | Leads | $10.32/day | $4,161.50 | 132 welcome_conversions | $31.53 | 2.68 | $33.01 | 1.21% |
| EMEA/lead/prospecting/cbo/20260712 | Active | Leads | $20.65/day | $3,324.30 | 289 welcome_conversions | $11.50 | 3.81 | $8.45 | 3.32% |
| US-Middle-South/lead/prospecting/cbo/20260617 | Active | Leads | $15.48/day | $3,252.86 | 123 welcome_conversions | $26.45 | 2.25 | $43.83 | 1.36% |
| EMEA/lead/retargeting/cbo/20260109 | Off | Leads | $20.00/day | $3,210.56 | 200 Website completed registration | $16.05 | 4.18 | $11.93 | 1.20% |
| Middle-East/lead/prospecting/cbo/20260709 | Active | Leads | $10.32/day | $2,593.31 | 89 welcome_conversions | $29.14 | 2.43 | $8.87 | 2.97% |
| Western-Europe/lead/prospecting/cbo/20260709 | Active | Leads | $10.32/day | $2,583.16 | 108 welcome_conversions | $23.92 | 2.88 | $13.19 | 2.02% |
| CFA \| Amazon US batch 1 | Off | Traffic | Ad set $200/day | $2,286.95 | 2,883 landing page views | $0.79 | 2.46 | $6.11 | 0.97% |
| All/welcome/ABO/20251010 | Off | Leads | Ad sets $20/day | $1,563.17 | 154 welcome_conversions | $10.15 | 3.15 | $5.73 | 0.90% |
| USCA/traffic/cold/abo/20260716 | Active | Traffic | Ad set $5.16/day | $740.70 | 3,045 link clicks | $0.24 | 1.11 | $8.54 | 3.51% |

Total of the rows above: $180,940.06. All other campaigns: $0.00 this year. Several active campaigns show "modelled" results (Meta uses statistical modelling).

**Last 30 days (14 Sep – 13 Oct 2026)**

| Campaign | Spend | Results | Cost / result |
|---|---|---|---|
| FR_Alibaba Campaign (Traffic, ad set 10 Sep – 5 Oct 2026) | $3,845.18 | 112,039 link clicks | $0.03 |
| WW/lead/retargeting/cbo/20260612 | $1,405.09 | 108 Website completed registration | $13.01 |
| US-East-Coast/.../20260617 | $883.68 | 70 welcome_conversions | $12.62 |
| US-California/.../20260602 | $707.00 | 50 | $14.14 |
| EMEA/.../cbo/20260712 | $694.00 | 105 | $6.61 |
| US-Middle-South/.../20260617 | $532.35 | 44 | $12.10 |
| USCA/.../cbo/20260617 | $356.62 | 23 | $15.51 |
| Western-Europe/.../20260709 | $352.35 | 44 | $8.01 |
| Middle-East/.../20260709 | $348.08 | 39 | $8.93 |
| USCA/traffic/cold/abo/20260716 | $181.33 | 863 link clicks | $0.21 |
| **Total** | **$9,305.68** | | |

### 1.2 Structure (campaign → ad sets → ads → landing page)

**Active campaigns today**

| Campaign | Budget/day | Locations | Ad sets | Top ad this year → landing page |
|---|---|---|---|---|
| WW/lead/retargeting/cbo/20260612 (Advantage+ leads On) | $41.29 | UAE, Canada, Georgia, Qatar, US, Europe | WW_EN_Lead-JTP-Complete-Registration_RT-DC_Topic:Broad (Active, $11,820.45, 509 WCR, $23.22, freq 5.74); USCA …Volvo (Off) | PP-328 "Fast-Track Corporate Innovation" $2,584.23 / 165 / $15.66 → /ultimate-innovation-platform |
| US-California/…/20260602 | $20.65 | California | AI, Brand, Deep Tech, Health, Innovation Leader (Off) | PP-257 $1,391.80 / 30 / $46.39 → /embedded-ai-robotics |
| US-East-Coast/…/20260617 | $25.65 | Washington DC, New Jersey, New York | same 5 topics | PP-257 $2,030.89 / 69 / $29.43 → /embedded-ai-robotics |
| USCA/…/20260617 | $10.32 | US and Canada | same 5 topics | PP-257 $1,563.55 / 36 / $43.43 → /embedded-ai-robotics |
| EMEA/…/cbo/20260712 | $20.65 | 19–20 EMEA countries (IE, NL, NO, ES, SE, CH, TR, AE, FI, DK, BE, AT, KW, PL, PT, LU, CZ, LT, (QA), DE) | same 5 topics | PP-240 CPR 2025 V3 $542.89 / 36 / $15.08 → /company-performance-report-2025 |
| US-Middle-South/…/20260617 | $15.48 | Arizona, Florida, Indiana, Texas | same 5 topics | PP-323 AI & Enterprise Trend Report $748.19 / 26 / $28.78 → /ultimate-enterprise-ai-trend-report (ad now Off) |
| Middle-East/…/20260709 | $10.32 | SA, AE, KW, QA | same 5 topics | PP-236 NJ Press release $775.69 / 8 / $96.96, CTR 5.05% → /ultimate-innovation-platform (Off) |
| Western-Europe/…/20260709 | $10.32 | IT, GB, FR | same 5 topics | PP-345 French AI Startups $886.45 / 46 / $19.27 → /french-ai-startups-to-watch-in-2026 (Off) |
| USCA/traffic/cold/abo/20260716 | $5.16 (ad set) | US | Traffic 20260723 (Active, LPV); Traffic 20260716 (Off, Messaging) | PP-346 "Support the Future of AI" $294.32 / 1,313 LPV → www…/ai-center-of-excellence |

All lead ad sets: optimisation goal OFFSITE_CONVERSIONS, conversion location Website. The geo campaigns since June/July all repeat the same five topic ad sets (AI, Brand, Deep Tech, Health, Innovation Leader); Innovation Leader is Off everywhere.

**Ad set settings read in panels (read-only)**

| Ad set | Key settings |
|---|---|
| Deep Tech (US-East-Coast/20260617) | Goal "Maximise number of leads"; Pixel "Plug and Play Tech Center's Pixel"; event "welcome_conversions (ID 1759876678043283)"; attribution Standard; cost per result goal None; value rules No; "Your audience is broad", 86.1M–101.2M; Meta suggestion "You could get 14–24% lower cost per lead by choosing website and instant forms" (not applied); "Connect your CRM" not connected; 22 ads incl. PP-366/368/369 Mitsubishi × Kamet |
| Brand (EMEA cbo 20260712) | CBO $20.65/day, ad set minimum $4.13; start 13 Jul 2026; Advantage+ audience On; 19 countries; minimum age 18; excludes "welcome-l180days"; all languages; no suggestions; 237.3M–279.1M; EU advertiser "Cassini Bussines Accelerator", payer "Plug and Play Tech Center"; placements not visible (did not load) |
| UK (EMEA abo 20260210, Off) | Saved audience "TC_UK-JobTitles-Generic_June2026"; Advantage+ On; UK; minimum age 25; excludes "HubSpot - Government and corps leads FB Ads", "Leads L180days", "welcome_conversions l90days"; English (US/UK); suggestions: age 30–60, job titles CSO, CIO, CTO, Co-Founder and COO, Founder, Director, CEO, Managing Director, Head of IT, CPO, CDO… |
| EMEA Quantum (prospecting-test 20251010, Off) | Saved audience "TC_EMEA_Job:Tech_Interest:AI-Quantum"; 19 EMEA countries incl. SA, QA, UK, FR, IT; minimum age 25; excludes "Customer and Opportunities Hubspot"; suggestions: CIO, CTO, CISO, Head of IT AND interest Artificial intelligence, field of study Quantum Physics |
| EMEA Politics / SpainGridReport (Off) | 48,300–56,800 people; same 19 countries; age 25+; suggestions CSO, President, VP, CFO, CEO & Founder, MD AND interests International relations, Political science, Politics. **Editor error shown: "Custom audience terms not accepted … accept the custom audience terms at business.facebook.com/ads/manage/customaudiences/tos/?act=471277291299593"** |
| WW retargeting ad set | Event "Complete registration"; Advantage+ leads campaign On; Opportunity score 18; Meta recommends "49 more Advantage+ creative enhancements for 53 ads" (not applied); Advantage+ audience with "Welcome_Conversions \| 180 Days" only as a **suggestion**; exclusions None; estimated audience "Below 1,000" |

Exclusions: newer ad sets exclude "welcome-l180days"; **Brand (USCA/20260617) has no exclusion**. Older ad sets exclude HubSpot lists ("HubSpot - Government and corps leads FB Ads", "Customer and Opportunities Hubspot").

Naming problems seen:
- The campaign "**EMEA**/lead/prospecting/abo/20260210" ($71,634.18) contains **US-state ad sets** (NJ $5,097.37, NY $4,626.52, TX $4,539.13, FL $4,275.98, DC $3,580.62, IN $3,523.38, AZ $3,236.02) besides UK/FR/IT/SA.
- TCb368 is named "LP:AiCOE" but links to /quantum-tech-report-2025; TCb826 is named "LP:Spain Grid Report" but links to /monitoring-decarbonization-in-buildings.
- Ad set "SAUAUE" targets Saudi Arabia only.

**Ad sets with spend, last 30 days**

| Ad set | Campaign | Spend | Results | Cost / result |
|---|---|---|---|---|
| WW_EN_Lead-JTP-Complete-Registration_RT-DC_Topic:Broad | WW retargeting | $1,405.09 | 108 WCR | $13.01 |
| Deep Tech | US-East-Coast | $344.93 | 34 | $10.15 |
| Deep Tech | US-California | $279.35 | 33 | $8.47 |
| Deep Tech | EMEA cbo | $276.99 | 60 | $4.62 |
| Deep Tech | US-Middle-South | $228.37 | 36 | $6.34 |
| AI | US-East-Coast | $194.21 | 19 | $10.22 |
| Health | US-East-Coast | $178.07 | 5 | $35.61 |
| Brand | US-East-Coast | $166.47 | 12 | $13.87 |
| Health | US-California | $144.39 | 4 | $36.10 |
| AI | US-California | $143.69 | 12 | $11.97 |
| Health | EMEA cbo | $140.16 | 14 | $10.01 |
| **Brand** | **US-California** | **$139.57** | **1** | **$139.57** |
| AI | EMEA cbo | $139.18 | 15 | $9.28 |
| Brand | EMEA cbo | $137.67 | 16 | $8.60 |
| Deep Tech | USCA | $131.03 | 10 | $13.10 |
| Deep Tech | Middle-East | $123.38 | 23 | $5.36 |
| AI | US-Middle-South | $112.64 | 2 | $56.32 |
| AI | Western-Europe | $107.38 | 13 | $8.26 |
| Health | US-Middle-South | $101.57 | 2 | $50.79 |
| Deep Tech | Western-Europe | $100.18 | 23 | $4.36 |
| Brand / AI / Health (USCA, ME, WE, US-Middle-South) | various | $71.36–$89.77 each | 2–9 each | $8.38–$38.08 |

**Older / off campaigns (this year, biggest ad sets)**

| Ad set | Campaign | Spend | Results | Cost / result |
|---|---|---|---|---|
| AI | US-EastCoast/20260409 | $15,653.22 | 335 | $46.73 |
| UK JobTitles | EMEA abo 20260210 | $12,583.08 | 547 | $23.00 |
| FR JobTitles | EMEA abo | $12,154.89 | 333 | $36.50 |
| IT JobTitles | EMEA abo | $10,712.39 | 306 | $35.01 |
| SAUAUE (Saudi Arabia) | EMEA abo | $6,190.08 | 193 | $32.07 |
| Quantum | EMEA prospecting-test 20251010 | $4,836.60 | 462 | $10.47 |
| US-California Tech-InterestQuantum | California 20260115 | $4,739.66 | 248 | $19.11 |
| TC_Global-Quantum | USCA 20251010 | $4,564.63 | 329 | $13.87 |
| JobTitlesGeneric InnovationLeader | EMEA prospecting-test | $2,955.49 | 59 | $50.09 |
| EMEA_Politics SpainGridReport | EMEA prospecting-test | $2,751.72 | 314 | $8.76 |
| AI-Robotics | EMEA prospecting-test | $2,666.68 | 241 | $11.07 |
| DecarbonizationReport (Purchase) | EMEA prospecting-test | $1,628.83 | 200 | $8.14 |

### 1.3 Best and worst ads (spend ≥ $300, this year) and named ads

Results are mostly "welcome_conversions" (a website custom conversion, see 1.4), not qualified leads.

**Best 5 by cost per result**

| Ad | Campaign / ad set | Spend | Results | Cost / result | CTR | Landing page |
|---|---|---|---|---|---|---|
| TCb817 Quantum Report – YouTube Thumbnail V2 (static) | EMEA prospecting-test / Quantum | $864.92 | 126 | $6.86 | 0.60% | /quantum-tech-report-2025 |
| PP-50b Quantum Computing – Green Screen Notes (short video) | EMEA prospecting-test / Quantum | $1,404.34 | 188 | $7.47 | 1.91% | /quantum-tech-report-2025 |
| PP-70b AI & Enterprise Trend Report – Test 3 | EMEA prospecting-test / AI-Robotics | $418.89 | 56 | $7.48 | 0.74% | /ultimate-enterprise-ai-trend-report |
| PP-67 Spain Grid Report – Carousel | EMEA prospecting-test / EMEA_Politics | $1,587.28 | 207 | $7.67 | 2.35% | /spain-energy-grid |
| PP-50c Quantum Green Screen Notes | EMEA prospecting-test / Quantum | $411.81 | 50 | $8.24 | 1.40% | /quantum-tech-report-2025 |

Just below the $300 line: PP-257 in EMEA cbo Deep Tech, $299.40 / 73 / **$4.10**.

**Worst 5 by cost per result (plus zero-result ads)**

| Ad | Campaign / ad set | Spend | Results | Cost / result | CTR |
|---|---|---|---|---|---|
| TCb729 Barcelona Health Expo V1 – Osama (video) | California 20260115 / Complete-Registration Health | $380.31 | 2 WCR | $190.16 | 1.92% |
| PP-138 AI Case Study (video) | EMEA abo / SAUAUE | $346.60 | 2 | $173.30 | 5.05% |
| PP-173 French AI Startups Ebook V2 | EMEA abo / FR | $319.15 | 2 | $159.57 | 0.51% |
| TCb368 Quantum report (video) | EMEA abo / SAUAUE | $436.13 | 3 | $145.38 | 1.59% |
| PP-231 AI Use Case ebook V1 v2 | US-EastCoast 20260409 / AI | $1,675.36 | 13 | $128.87 | 1.34% |
| Zero results: PP-231 (EMEA abo / FR) | | $408.47 | 0 | — | 1.14% |
| Zero results: **PP-102b CPR 2025 (Western-Europe / Deep Tech) — still ON** | | $372.88 | 0 | — | 0.65% |
| Zero results: PP-239 CPR 2025 V2 (Western-Europe / Brand) | | $363.75 | 0 | — | 0.43% |

**Named ads**

| Named ad | What it is | Main figures (this year) |
|---|---|---|
| Quantum (PP-50b/50c/196/291, TCb817/368) | Short "green screen notes" video and YouTube-thumbnail statics → /quantum-tech-report-2025 | PP-50b UK $6,767.35 / 332 / $20.38; FR $4,273.87 / 118 / $36.22; EMEA Quantum $1,404.34 / 188 / $7.47. PP-196 (Deep Tech ad sets, this year): $253.08 / 25 / $10.12 (US-East-Coast), $147.44 / 24 / $6.14 (US-Middle-South) |
| "Grid" (PP-67, TCb820, TCb836) | English ads on Spain's energy grid, headline "60% of Spain's Power Gone in Seconds" → /spain-energy-grid | PP-67 EMEA Politics $1,587.28 / 207 / $7.67; IT $2,122.82 / 73 / $29.08; UK $1,513.90 / 84 / $18.02 |
| AICOI (TCb368) | Video, "Download Now"; named LP:AiCOE but links to quantum report | USCA Quantum $2,067.97 / 86 / $24.05; SA $436.13 / 3 / $145.38; IT $583.69 / 5 / $116.74 |
| PP-257 | "Green screen AI & Robotics V1", 30–40 s video, "Access the Full Report" → /embedded-ai-robotics | US-East-Coast DT $2,030.89 / 69 / $29.43; USCA DT $1,563.55 / 36 / $43.43; US-California DT $1,391.80 / 30 / $46.39; US-Middle-South DT $724.84 / 32 / $22.65; EMEA DT $299.40 / 73 / $4.10 |
| PP-266 | "Animated Voice Memo Osama 3 – AI in Healthcare" video → /health-innovation-platform | 6 copies $21.15–$33.86 each, total $173.57, 3 results; 5 copies still Active/Learning limited |

### 1.4 Events Manager

| Item | What it shows |
|---|---|
| Datasets | "Plug and Play Tech Center's Pixel" ID 444584699312563 — 214.1K events in 28 days, Meta pixel + Conversions API. "Plug and Play Tech Center (Dollars…)" ID 847859232929373 — 0 events, "Never received events", no integrations |
| Websites on the pixel | www.plugandplaytechcenter.com + 6 more |
| Diagnostics (1 active, detected 14 Oct 2026) | "Confirm domains that belong to you": it.plugandplaytechcenter.com, en.pnpchina.com, **pnptc-master.herokuapp.com**, welcome.plugandplaytechcenter.com, + 2 more |
| Banner | Offer to "Enable automatic events" (not touched) |

| Event (16 Sep – 13 Oct 2026) | Used by | Event match quality | Events |
|---|---|---|---|
| PageView | — | 6.1/10 | 174.9K |
| **Lead** | — | 6.1/10 "Update recommended" | **18.5K** |
| Complete registration | 1 ad set | 6.6/10 "Update recommended" | 2.6K |
| welcome_conversion | 29 ad sets | 6.6/10 | 1.5K |
| Submit Application | — | 6.3/10 "Update recommended" | 475 |
| Newsletter | — | 6.1/10 | 12 |

| Custom conversion | Rule | Status | Count (16 Sep – 13 Oct) |
|---|---|---|---|
| welcome_conversions (ID 1759876678043283) | Event welcome_conversion **AND URL contains "welcome"**; value 0.00 USD | Active | 555 |
| JTP Lead (ID 8414692411875171) | URL equals "https://www.plugandplaytechcenter…" (rest cut off on screen); value 0.00 USD | No recent activity (last 7 days ago) | 60 |

### 1.5 Ad Library (page ID 6038767267, checked 14 Oct 2026)

| Item | Count / detail |
|---|---|
| Active ads (all countries) | ~280 |
| All ads (active + inactive) | ~710 |
| Active by media | video ~110, image ~3, image+text ~150 |
| Language | English ~240 active / ~650 all; **Spanish 0**; FR/IT/DE/AR/PT ~3 combined |
| Most common active headlines (86 cards) | "Access World-Class Startups" ×16, "Join the Innovation Platform" ×16, "Join the Platform" ×8, quantum video ×7, "Access the report" ×6, "Access the Full Report" ×5, "Fast-Track Corporate Innovation" ×3 |

Matched Library IDs (open as `https://www.facebook.com/ads/library/?id=<ID>`):

| Ad | Library IDs |
|---|---|
| PP-328 "Fast-Track Corporate Innovation" | 1548020570157866; also 1444381547510685, 1599344838528115 |
| PP-257 Embedded AI & Robotics | 827663797036023, 1777541663669737, 1025988960220556, 1684621526996443, 1239065305027622 |
| Quantum "Access the report" | 1748635849745383, 2474749012992156, 1387553270132929, 1843245243707861, 2294998667930172, 1111047671290662, 1604955291241443, 1407397378253602, 1333649505393168, 2273805243443301 |
| PP-103b 20-Year Blueprint | 1715911216211426 |
| PP-231 AI Use Cases | 2022802191649772, 2022638695123628 |
| PP-102b / PP-239-240 CPR 2025 | 1354194756856211, 983529104763707, 1376443407781624 |
| "Support the Future of AI" | 1771104790706742, 1410006404346881 |
| ADR × Ottonomy | 2271277786996345 |

EU transparency for 1548020570157866 (PP-328): location Europe; age 25–65+; EU reach 12,557. Visible breakdown rows (5,250 people): male 4,305, female 842, unknown 103; ages 25–34: 1,788, 35–44: 1,818, 45–54: 1,029, 55–64: 450, 65+: 165; top countries France 889, Germany 827, **Greece 681, Bulgaria 636, Hungary 390**, Finland 330, Croatia 326, Belgium 255.

### 1.6 Meta — Working / To improve

**Working**
- **Deep Tech report downloads are the cheapest offer.** All five Deep Tech ad sets cost $4.36–$13.10 per result in L30D, driven by PP-257 (embedded AI robotics) and the quantum notes (PP-196).
- **EMEA and Middle-East reach is cheap.** CPMs were $8.45 (EMEA cbo), $8.87 (Middle-East) and $13.19 (Western-Europe) against $33–$44 in US campaigns. EMEA cbo cost $6.61 per result in L30D.
- **Retargeting with a third-party quote works.** WW retargeting delivered 108 Complete registrations at $13.01 in L30D. PP-328 (BizJournals quote, "Fast-Track Corporate Innovation") is its best ad at $15.66.
- **Hygiene basics are in place.** Past converters ("welcome-l180days") are excluded on most active ad sets, and every ad carries the same UTM template (`utm_source=facebook&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}`).

**To improve**
- **Optimise to a real lead signal.** The optimisation event "welcome_conversions" uses the rule *URL contains "welcome"*, which is true for every page on the welcome subdomain. The pixel also fired **18.5K "Lead" events** in 28 days against 555 welcome_conversions, so "Lead" is clearly over-firing. Connect HubSpot (CRM / Conversions API) and optimise to qualified leads. The "(Dollars)" dataset has never received events.
- **Check FR_Alibaba.** This Traffic campaign took **41% of L30D spend ($3,845.18)** buying link clicks at $0.03 in Turkey, Greece, Croatia, Poland, Bulgaria, Slovakia, Lithuania, Hungary, Romania, Estonia and Latvia. These are not target audiences and the objective is not leads. The PP-328 EU reach (Greece, Bulgaria, Hungary in the top countries) points the same way.
- **Pause or cut the expensive US ad sets.** In L30D: Brand US-California $139.57 for 1 result, AI US-Middle-South $56.32, Health US-Middle-South $50.79, Health US $35–$36. Move that money to the Deep Tech ad sets.
- **Finish the planned pauses.** PP-266 is still live in 5 of 6 ad sets (3 results for $173.57). PP-102b is still ON in Western-Europe Deep Tech with 0 results after $372.88.
- **Consolidate the structure.** Seven geo campaigns × five topic ad sets on $10–$26/day leave many ad sets "Learning limited". The same creative is duplicated as separate ads (PP-50b has 12+ copies), which splits learning.
- **Fix the naming.** The "EMEA" abo campaign holds US states, and ad names point to the wrong landing pages (TCb368, TCb826). Reporting by name is unreliable.
- **Tighten retargeting.** The retargeting audience is only an Advantage+ *suggestion*, so Meta can go beyond past visitors, and the estimated audience is "Below 1,000".
- **Accept the custom-audience terms.** The editor shows "Custom audience terms not accepted", so HubSpot list exclusions may not apply in new or edited ads.
- **Clean the pixel data.** A staging domain (pnptc-master.herokuapp.com) and other domains send pixel data. Event match quality is 6.1–6.6 with "Update recommended".
- **Clicks without conversions in some markets.** High CTR with few results in Middle-East and Western-Europe (PP-236 5.05% CTR, 8 results; TCb729 21.27% CTR, 2 results) suggests accidental or low-intent clicks.

---

## 2. Google Search (and Performance Max)

Account "Plug and Play" 133-450-4766 · EUR · time zone GMT+02:00 CET. Before I started, the campaign list showed "Drafts in progress: 3" (not mine). Notices: "Complete financial services verification" for France, Germany or Spain (open; "Fix it" not clicked).

### 2.1 Campaign list and conversions by action

**This year (Jan 1 – Oct 13, 2026), Search + PMax with spend**

| Campaign | Budget/day | Status | Bidding | Cost | Clicks | CTR | Avg CPC | Conv. | Cost/conv. | Search IS | Lost IS (budget) | Lost IS (rank) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Geo:EMEA …non-brand…Date:20251125 | €46.80 | Paused | Max conversions | €8,946.52 | 4,387 | 10.06% | €2.04 | 165.95 | €53.91 | 10.62% | 17.99% | 71.39% |
| Geo:US …non-brand…Date:20251008 | €46.80 | Paused | Max conversions | €8,868.17 | 3,478 | 11.72% | €2.55 | 133.84 | €66.26 | 11.38% | 13.30% | 75.33% |
| Geo:US-CA …20260114 | €45.00 | Paused | Max conversions | €8,669.74 | 1,899 | 6.78% | €4.57 | 84.20 | €102.96 | 24.38% | 8.38% | 67.24% |
| Geo:US-South-Central …20260115 | €60.30 | Paused | Max clicks | €6,360.89 | 1,537 | 4.85% | €4.14 | 41.39 | €153.69 | 30.58% | 20.75% | 48.67% |
| **Geo:NA_Channel:GoogleAds_Network:search_Type:non-brand_Goal:leads_Date:20260813** | €30.00 | **Eligible (Limited) – Limited by budget** | Max conversions | €5,256.66 | 2,601 | 9.79% | €2.02 | 118.84 | €44.23 | 12.78% | 26.61% | 60.61% |
| Geo:US-East-Coast …20260114 | €46.80 | Paused | Max clicks | €4,905.28 | 260 | 3.98% | €18.87 | 15.00 | €327.02 | 60.98% | 15.17% | 23.86% |
| Geo:FR …20260114 | €18.90 | Paused | Max conversions | €4,415.75 | 1,721 | 11.08% | €2.57 | 83.82 | €52.68 | 15.33% | 22.54% | 62.13% |
| Geo:UK …20260114 | €18.90 | Paused | Max conversions | €4,412.69 | 1,503 | 9.37% | €2.94 | 42.10 | €104.81 | 13.89% | 22.65% | 63.47% |
| **Geo:EMEA_Channel:GoogleAds_…_Date:20260813** | €33.00 | **Eligible** | Target CPA (€45.00) | €4,366.65 | 3,165 | 9.60% | €1.38 | 105.57 | €41.36 | 12.53% | 49.84% | 37.64% |
| New York_EN_Search_Conversions | €26.00 | Paused | Max clicks | €3,478.33 | 371 | 4.40% | €9.38 | 6.33 | €549.70 | 46.20% | 18.05% | 35.75% |
| Florida_EN_Search_Conversions | €24.00 | Paused | Max conversions | €3,204.66 | 210 | 5.36% | €15.26 | 11.13 | €287.94 | 63.50% | 14.82% | 21.68% |
| Geo:NA_Network:pmax_…_20260608 (PMax) | €110.00 | Paused | Max conversions | €3,058.05 | 2,685 | 2.95% | €1.14 | 287.90 | €10.62 | <10% | 20.62% | 70.27% |
| Texas_EN_Search_Conversions | €21.00 | Paused | Max conversions | €2,826.08 | 238 | 7.24% | €11.87 | 10.08 | €280.30 | 52.55% | 28.72% | 18.73% |
| Geo:IT …20260114 | €18.00 | Paused | Target CPA | €2,356.54 | 1,132 | 10.05% | €2.08 | 77.00 | €30.60 | 16.35% | 18.36% | 65.29% |
| New Jersey_EN_Search_Conversions | €16.00 | Paused | Max conversions | €2,161.21 | 181 | 4.67% | €11.94 | 8.67 | €249.37 | 48.69% | 29.46% | 21.85% |
| Geo:SA …20260114 | €7.20 | Paused | Max conversions | €1,522.89 | 1,047 | 7.51% | €1.45 | 44.96 | €33.87 | <10% | 25.23% | 67.75% |
| Arizona_EN_Search_Conversions | €12.00 | Paused | Max clicks | €1,460.19 | 292 | 4.07% | €5.00 | 5.75 | €254.04 | 30.07% | 22.48% | 47.46% |
| **Geo:US-SV …coworking-startup…20230530** | €5.00 | **Eligible (Limited)** | Target CPA (avg €39.07) | €1,112.61 | 561 | 8.11% | €1.98 | 44.81 | €24.83 | <10% | 15.40% | 80.34% |
| EMEA_EN_DC_PMax_Quiz | €10.00 | Paused | Target CPA €10.43 | €878.59 | 1,601 | 3.51% | €0.55 | 91.02 | €9.65 | <10% | 0.13% | >90% |
| US_EN_DC_PMax_Quiz | €10.00 | Paused | Target CPA €14.51 | €786.62 | 1,355 | 2.09% | €0.58 | 77.07 | €10.21 | <10% | 0.50% | >90% |
| USCA_EN_Search_Brand | €40.00 | Paused | Max conversions | €558.80 | 534 | 15.27% | €1.05 | 23.16 | €24.13 | 10.08% | 18.77% | 71.15% |
| EMEA_EN_Search_Brand | €20.00 | Paused | Target CPA €45.00 | €293.37 | 257 | 13.76% | €1.14 | 5.00 | €58.67 | 15.33% | 22.22% | 62.45% |
| Geo:EMEA_Network:pmax_…_20260819 (PMax) | €20.00 | Paused | Max conversions | €155.33 | 1,592 | 3.75% | €0.10 | 4.00 | €38.83 | <10% | 88.49% | 7.55% |

Search + PMax total conversions: 1,487.57. Account cost including video: €90,897.68.

**Last 30 days (Sep 14 – Oct 13, 2026)** — only three campaigns spent:

| Campaign | Bidding | Cost | Conv. | Cost/conv. | Clicks | CTR | CPC | Search IS | Lost IS (budget) | Lost IS (rank) |
|---|---|---|---|---|---|---|---|---|---|---|
| NA 20260813 | Max conversions | €1,767.85 | 28.00 | €63.14 | 831 | 13.99% | €2.13 | 11.62% | 27.80% | 60.58% |
| EMEA 20260813 | Target CPA | €1,439.75 | 28.00 | €51.42 | 652 | 8.25% | €2.21 | 10.40% | 53.76% | 35.83% |
| US-SV coworking | Target CPA (avg €39.55) | €143.63 | 10.00 | €14.36 | 45 | 8.29% | €3.19 | <10% | 1.85% | >90% |

**Conversions by action (this year) and cost per HubSpot qualified lead**

"HubSpot" = "Contacts – Contacts Lifecycle Stage becomes Lead and 1 more condition" (imported from clicks).

| Campaign | Total conv. | GA4 contact_form | Welcome LPs | Contact website | JTP-form | HubSpot | Cost per HubSpot lead* |
|---|---|---|---|---|---|---|---|
| EMEA 20251125 | 165.95 | 8.95 | 51 | – | 79 | 27 | €331.35 |
| US 20251008 | 133.84 | 9.84 | 38 | – | 72 | 14 | €633.44 |
| US-CA 20260114 | 84.20 | 7.20 | 18 | – | 57 | 2 | €4,334.87 |
| US-South-Central | 41.39 | 2.39 | 12 | 14 | 9 | 4 | €1,590.22 |
| **NA 20260813** | 118.84 | 2.84 | 16 | 64 | 16 | 20 | **€262.83** |
| US-East-Coast | 15.00 | – | 6 | 5 | 2 | 2 | €2,452.64 |
| FR | 83.82 | 1.82 | 28 | 30 | 16 | 8 | €551.97 |
| UK | 42.10 | 2.10 | 13 | – | 23 | 4 | €1,103.17 |
| **EMEA 20260813** | 105.57 | 0.57 | 7 | 62 | 25 | 11 | **€396.97** |
| **NA PMax 20260608** | 287.90 | 11.90 | 85 | 91 | 75 | 25 | **€122.32** |
| IT | 77.00 | – | 24 | 25 | 15 | 13 | €181.27 |
| SA | 44.96 | 2.96 | 11 | – | 29 | 2 | €761.45 |
| US-SV coworking | 44.81 | 0.81 | 21 | 22 | – | 1 | €1,112.61 |
| EMEA_EN_DC_PMax_Quiz | 91.02 | 13.02 | 63 | – | 1 | 14 | €62.76 |
| US_EN_DC_PMax_Quiz | 77.07 | 40.07 | 30 | – | 4 | 3 | €262.21 |
| USCA_EN_Search_Brand | 23.16 | 3.16 | 20 | – | – | – | — |
| EMEA_EN_Search_Brand | 5.00 | – | 5 | – | – | – | — |
| New York / Florida / Texas / New Jersey / Arizona | 6.33 / 11.13 / 10.08 / 8.67 / 5.75 | small | 2–5 | 1–2 | 2–5 | – | — |

\*My calculation: campaign cost ÷ HubSpot conversions shown in Google Ads (Google's own attribution).

### 2.2 Search campaigns in detail

#### 2.2.1 NA 20260813 (campaign ID 24120365465) — active

**Settings** (side panel, read-only)

| Setting | Value |
|---|---|
| Status / type / networks | Enabled, Eligible (Limited) – Limited by budget; Search; Google Search Network only |
| Optimisation score | 92.1% |
| Conversion goal | "Campaign-specific: Submit lead forms" |
| Bidding | Maximize conversions (no target CPA); Budget €30.00/day; bid equally for new and existing customers; value rules none |
| AI Max | Change history: AI Max turned on (8 Sep 2026); panel shows toggle on; text customization Off; final URL expansion opted out (8 Sep) |
| Brands | Limiting 0 / excluding 0 brand lists |
| Locations / language | Canada and United States; location option changed on 9 Sep to "people in my targeted location"; English |
| Dates | Start **August 10, 2026**, no end |
| Other | Broad match keywords setting "Off" (but every keyword is Broad match type); Ad rotation Optimize; URL tracking options set; no IP exclusions |

**Ad groups (this year)**

| Ad group | Target CPA | Cost | Clicks | Conv. | Cost/conv. | Avg CPC | Conv. rate |
|---|---|---|---|---|---|---|---|
| PlugNPlay-NA-Leads-Search-**Branding** | — | €2,396.68 | 1,297 | 40.17 | €59.66 | €1.85 | 3.10% |
| PlugNPlay-NA-Leads-Search_StartupCollaboration | — | €2,350.98 | 1,135 | 48.00 | €48.98 | €2.07 | 4.23% |
| PlugNPlay-NA-Leads-Search_Innovation | — | €341.47 | 122 | 29.66 | €11.51 | €2.80 | 24.31% |
| PlugNPlay-NA-Leads-Search_AI_&_Innovation_Strategy | — | €167.53 | 47 | 1.00 | €167.53 | €3.56 | 2.13% |

The Branding ad group is 45.6% of NA cost. 300 keywords; all top keywords are **Broad match**.

**Top 15 keywords by cost (this year)** — QS columns: Quality Score | Expected CTR | Landing page exp. | Ad relevance

| # | Keyword | Ad group | Status | Cost | Clicks | Conv. | Cost/conv. | QS | Exp. CTR | LP exp. | Ad rel. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | plug and play | Branding | Eligible | €1,148.55 | 568 | 19.00 | €60.45 | 7/10 | Average | Above avg | Average |
| 2 | startup accelerator | StartupCollab. | Eligible | €504.52 | 259 | 12.00 | €42.04 | **3/10** | Below avg | Average | Below avg |
| 3 | plug and play tech center | Branding | Eligible | €449.84 | 274 | 7.17 | €62.72 | 10/10 | Above | Above | Above |
| 4 | business incubators and accelerators | StartupCollab. | Paused | €209.13 | 103 | 1.00 | €209.13 | — | — | — | — |
| 5 | open innovation companies | Innovation | Eligible | €146.41 | 50 | 7.00 | €20.92 | — | — | — | — |
| 6 | venture capital financing for startups | StartupCollab. | Eligible | €118.45 | 20 | 2.00 | €59.23 | — | — | — | — |
| 7 | startup accelerator program | StartupCollab. | Eligible | €109.81 | 28 | 2.00 | €54.91 | — | — | — | — |
| 8 | plug and play ventures | Branding | Eligible | €108.83 | 76 | 3.00 | €36.28 | 6/10 | Average | Above | Below |
| 9 | entrepreneur accelerator program | StartupCollab. | Eligible | €108.47 | 49 | 1.00 | €108.47 | — | — | — | — |
| 10 | incubators and accelerators | StartupCollab. | Paused | €94.19 | 55 | 3.00 | €31.40 | — | — | — | — |
| 11 | tech incubators | StartupCollab. | Paused | €88.08 | 46 | 3.00 | €29.36 | — | — | — | — |
| 12 | start up accelerator program | StartupCollab. | Eligible | €80.38 | 40 | 0.00 | — | — | — | — | — |
| 13 | plug and play accelerator | Branding | Eligible | €73.62 | 33 | 1.00 | €73.62 | 5/10 | Below | Above | Below |
| 14 | startup sourcing | StartupCollab. | Eligible | €72.80 | 16 | 1.00 | €72.80 | — | — | — | — |
| 15 | venture building | StartupCollab. | Eligible | €68.40 | 28 | 0.00 | — | — | — | — | — |

Also: "innovation challenge" (Innovation) Eligible (Limited) – *Rarely shown (low Quality Score)*, QS 1/10, €59.52 / 15.00 conv. / €3.97; "ai startup funding" Paused €55.68 / 0; "plug & play llc" €57.02 / 0.

**Top 20 search terms by cost (this year)** — visible terms: 1,758 clicks / €3,244.67 / 75.84 conv.; "Other search terms" (hidden by Google): 842 clicks / 43.00 conv.

| # | Search term | Match | Added/Excluded | Ad group | Clicks | Cost | Conv. |
|---|---|---|---|---|---|---|---|
| 1 | plug and play | Exact | Added | Branding | 340 | €636.75 | 13.00 |
| 2 | plug and play tech center | Exact | Added | Branding | 215 | €337.23 | 3.17 |
| 3 | plug and play ventures | Exact | Added | Branding | 66 | €83.65 | 3.00 |
| 4 | plug and play accelerator | Exact | Added + Excluded | Branding | 33 | €73.62 | 1.00 |
| 5 | plug and play sunnyvale | Exact (close var.) | None | Branding | 35 | €63.08 | 1.00 |
| 6 | plug and play vc | Exact | Excluded | Branding | 26 | €58.73 | 0 |
| 7 | how to contact investors for startup | Phrase (close var.) | None | StartupCollab. | 1 | €44.75 | 0 |
| 8 | cofounderslab | Broad | Excluded | Branding | 22 | €32.99 | 0 |
| 9 | rbc ventures | Broad | None | StartupCollab. | 1 | €32.53 | 1.00 |
| 10 | plug n play | Exact | Added | Branding | 22 | €30.18 | 0 |
| 11 | plugandplay | Exact | None | Branding | 19 | €29.72 | 0 |
| 12 | plug and play silicon valley | Exact | Added | Branding | 20 | €29.58 | 3.00 |
| 13 | south park commons | Broad | None | StartupCollab. | 6 | €24.19 | 1.00 |
| 14 | alchemist accelerator | Broad | None | StartupCollab. | 8 | €23.49 | 3.00 |
| 15 | plugnplay | Exact | Added | Branding | 13 | €22.11 | 0 |
| 16 | plug n play accelerator | Phrase (close var.) | None | StartupCollab. | 15 | €20.21 | 1.00 |
| 17 | 70blå | Broad | Excluded | StartupCollab. | 1 | €20.17 | 0 |
| 18 | mindsumo | Broad | None | Innovation | 7 | €20.03 | 2.00 |
| 19 | plug and play incubator | Phrase (close var.) | Excluded | StartupCollab. | 9 | €18.44 | 1.00 |
| 20 | plug and play corporate partners | Exact | Added | Branding | 8 | €17.56 | 0 |

Brand terms are 13 of the top 20 rows, **€1,420.86 = 43.8%** of the visible search-term cost.

Irrelevant or off-target terms (ranks 21–50):
- **Competitors / other programmes:** pnptc €16.44; eit innoenergy €15.74; the yield lab €13.58; boost vc €11.45; zetta venture partners €11.15.
- **Founder funding and grants:** where to find investors €13.42; free grants for women owned businesses €13.00; bizee fresh start business grant €12.35; startup funding €12.26; startup pitch competitions €11.14.
- **Generic or unrelated:** company €12.60; us startup companies €12.51; us startups €12.39; trendspider ai €12.20; telusinternational ai €11.66.

**Negative keywords (23, campaign level)**

- **Incubator terms:** [70blå], [bits pilani incubation centre], [cofounderslab], [france startup incubator], "incubadora", "incubateur", "incubateurs", "incubation", [incubation center near me], [incubation centre], [incubation program], "incubator", [incubator in usa], "incubators", "incubazione", [plug and play incubator], [plug n play incubator], [small business incubator near me], [startup incubation centre in bangalore], [startup incubators in bangalore].
- **Brand variants:** [plug and play accelerator] (also an active keyword), [plug and play vc].
- **List:** "Competitor Accelerators and VCs" (applied 16 Sep). Its contents were not opened; South Park Commons, Alchemist, Boost VC, The Yield Lab, RBC Ventures, Zetta and MindSumo still matched.

**Ads (4 responsive search ads, all Eligible, final domain welcome.plugandplaytechcenter.com)**

| Ad (first headlines) | Ad group | Ad strength | Clicks | Cost | Conv. | Cost/conv. | Conv. rate |
|---|---|---|---|---|---|---|---|
| Find the Right Startups \| Startup Scouting Platform \| Test Ideas with Pilot Programs | Branding | Average | 1,297 | €2,396.68 | 40.17 | €59.66 | 3.10% |
| Plug and Play \| Global Innovation Ecosystem \| Business transformation | StartupCollaboration | **Poor** | 1,135 | €2,350.98 | 48.00 | €48.98 | 4.23% |
| Corporate Matchmaking \| Innovative Solution For You \| Supply Chain Innovation | Innovation | Average | 122 | €341.47 | 29.66 | €11.51 | 24.31% |
| Plug and Play \| Global Innovation Ecosystem \| Business transformation | AI_&_Innovation_Strategy | Average | 47 | €167.53 | 1.00 | €167.53 | 2.13% |

Full assets (no pins on any ad; asset report impressions / cost / conv.):

- **Branding ad** — 15 headlines; top by cost:
  - Startup Scouting Platform €1,153.56 / 16
  - Build Pilot Programs €1,127.54 / 20.17
  - Check our Tech Center €1,009.62 / 15.17
  - Plug and Play Tech Center €936.40 / 11
  - Launch Startup Pilots €751.07 / 16
  - Plug and Play Official Site €719.27 / 9

  Lowest: 550+ Corporate Partners €107.91 / 0; Accelerate Pilot Success €34.95 / 0. Descriptions:
  - "Run startup PoCs efficiently with our proven tools and best practices." (€2,256.52 / 40.17)
  - "Join our startup network & check emerging tech solutions. Partner with **50,000+** startups."
  - "Identify top startups through our global scouting network."
  - "Discover and test emerging technologies faster through startup scouting."
- **StartupCollaboration ad (Poor)** — top headline by cost is **"Venture Capitalist"** (€1,423.74 / 27). Next:
  - Choose From 100,000+ Startups €1,218.14 / 17
  - Plug and Play €985.46 / 21
  - Start Your Innovation Journey €747.41 / 17

  Only 3 descriptions, including "Join our global ecosystem of 550+ partners & **100,000+** vetted startups across 60+ locations".
- **Innovation ad** — corporate ad group but headlines include **"Fund Your Future"** (€169.14 / 22.66), **"Empowering Founders"**, **"Back Exceptional Founders"**, "Venture Capitalist". Description: "From sourcing to last-mile delivery, we are bringing together the most innovative startups".
- **AI ad** — "AI Implementation Support", "AI Governance & Roadmap", "AI Strategy for Enterprises", "We work with large corporations & give them access to a strategically aligned network.", "We bring technological transformation to the largest corporations. Get in touch today". Low volume (569 impressions this year).

**Assets on NA (from the ad asset report)**

| Asset | Status / detail |
|---|---|
| Business name "Plug and Play" | **Not eligible – Disapproved (Business Name Irrelevance)** |
| Business logo 2400×2400 | **Disapproved (Business Logo Irrelevance)**; a Google-AI 32×32 logo serves instead (10,607 impr.) |
| Campaign images (added 19 Sep via recommendation) | **14 disapproved (Text or graphic overlays)**; 4 eligible (799×421: 0 impr., 799×416: 0, 535×533: 85, 533×533: 152) |
| Campaign sitelinks (advertiser, 10 Aug) | Our Verticals 2,961 impr. / €415.70 / 5; Plug And Play Ventures "Learn about our venture fund" 2,242 / €371.07 / 9.50; Institutional Innovation "Innovation programs for public **ector** and government teams" 703 / €184.48 / 3; Get In Touch Today 555 / €123.43; Innovation Handbook 132 / €26.64 |
| Campaign callouts (10 Oct) | Startup Growth 1,102 impr.; Scale with Startups 738; Innovate your corporation 108; Global Network 106; Corporate Partners 40; Boost your startup 25 |
| **Campaign structured snippets (10 Oct, via recommendation)** | **Coworking content**: "Service catalog: Business Address, Mailbox Service, Package Service, Meeting Room Rental, Event Space Rental, Day Passes"; "Types: Open Desk, Dedicated Desk, Private Office, Day Pass, Meeting Room, Virtual Office, Event Space"; "Amenities: 24/7 Member Access, High-Speed Internet, Coffee & Tea…" |
| Ad-group sitelinks "Added by Google AI" (19 Sep, 8 Oct) | Services For Startups 1,545 impr. / €591.12; For Mentors 490 / €228.81; Services For Corporations 453 / €192.85; Startup Scouting 323; For Universities; For Governments 99; Get The AI Playbook; Download Commerce Report |
| Account-level (Google AI, 2025) | Sitelinks For Startups 4,990 impr. / €891.40; For Mentors 3,142 / €512.19; For Corporations 722; For Governments 765; For Universities 712. Callouts Read Our Blog / View Events / Explore Resources |

**Landing pages report (this year)**

| URL | Clicks | Cost |
|---|---|---|
| **welcome.plugandplaytechcenter.com/** (redirects to the corporate homepage) | 1,556 | €2,969.63 |
| welcome.plugandplaytechcenter.com/ultimate-innovation-platform | 721 | €1,553.73 |
| welcome.plugandplaytechcenter.com/supply-chain-innovation-2025 | 107 | €265.89 |
| www…/venture-capital/all-about-venture-capital (sitelink) | 16 | €19.53 |
| www…/how-we-work/our-verticals/ with a 2023 `_ga=` parameter hard-coded | 4 | €4.58 |

**Locations:** United States 2,245 clicks / €4,470.12 / conv. rate 4.11%; Canada 356 / €786.53 / 7.46%.

#### 2.2.2 EMEA 20260813 (campaign ID 24120623279) — active

**Settings:** Enabled, Eligible; Search network; optimisation score 99.9%; "Campaign-specific: Submit lead forms"; **Target CPA €45.00**; budget €33.00/day (warning icon next to budget); locations "France (country) + 5 more"; English; EU political ads: no; start August 10, 2026; Broad match setting Off; AI Max search-term matching active (search terms show match type "AI Max"); automatically created assets and text/URL automation turned off on 15 Sep.

**Ad groups (this year)**

| Ad group | Target CPA | Cost | Clicks | Conv. | Cost/conv. | Avg CPC | Conv. rate |
|---|---|---|---|---|---|---|---|
| Startup_Collaboration | €45.00 | €1,656.44 | 1,210 | 36.75 | €45.07 | €1.37 | 3.04% |
| Branding | €45.00 | €1,208.63 | 717 | 38.82 | €31.14 | €1.69 | 5.41% |
| Innovation | €45.00 | €989.11 | 519 | 22.25 | €44.45 | €1.91 | 4.29% |
| AI_&_Innovation_Strategy | €45.00 | €512.47 | 719 | 7.75 | €66.13 | €0.71 | 1.08% |

**Locations (this year)**

| Country | Bid adj. | Clicks | Cost | Conv. | Cost/conv. |
|---|---|---|---|---|---|
| Saudi Arabia | +15% | 446 | €887.02 | 27.50 | €32.26 |
| United Kingdom | — | 419 | €818.29 | 15.15 | €54.02 |
| United Arab Emirates | −40% | 271 | €650.09 | 7.00 | €92.87 |
| Italy | −40% | 318 | €489.50 | 6.00 | €81.58 |
| France | — | 250 | €421.97 | 8.00 | €52.75 |
| Qatar | −20% | 134 | €266.12 | 6.00 | €44.35 |

The location rows add up to €3,533.00 / 69.65 conv. against a campaign total of €4,366.65 / 105.57 conv. The remaining €833.65 has no targeted-location row (as shown).

**Top 15 keywords (all Broad match)**

| # | Keyword | Ad group | Cost | Clicks | Conv. | Cost/conv. | QS (Exp CTR / LP / Ad rel.) |
|---|---|---|---|---|---|---|---|
| 1 | plug and play | Branding | €714.17 | 429 | 15.25 | €46.83 | 7 (Avg / Avg / Above) |
| 2 | startup accelerator | Startup_Collab. | €330.22 | 167 | 4.50 | €73.38 | 3 (Avg / Below / Below) |
| 3 | innovation hub funding (Paused) | Innovation | €271.54 | 153 | 6.00 | €45.26 | — |
| 4 | artificial intelligence innovation | AI | €185.39 | 382 | 1.00 | €185.39 | — |
| 5 | **startup india certificate** | Startup_Collab. | €166.47 | 192 | 3.00 | €55.49 | 5 (Above / Below / Below) |
| 6 | ai investments | AI | €107.84 | 136 | 1.00 | €107.84 | 5 (Avg / Avg / Below) |
| 7 | innovation consulting | Innovation | €85.99 | 39 | 4.00 | €21.50 | — |
| 8 | open innovation | Innovation | €84.53 | 48 | 1.00 | €84.53 | 3 (Avg / Below / Below) |
| 9 | saudi arabia venture capital fund | Startup_Collab. | €79.10 | 36 | 2.00 | €39.55 | — |
| 10 | innovation hub (rarely shown) | Innovation | €78.14 | 29 | 1.00 | €78.14 | **1** (Below ×3) |
| 11 | startup sourcing | Startup_Collab. | €77.56 | 46 | 2.00 | €38.78 | — |
| 12 | fintech accelerator | Startup_Collab. | €72.94 | 37 | 3.00 | €24.31 | 3 |
| 13 | playbook plug and play | Branding | €67.24 | 33 | 2.00 | €33.62 | 3 |
| 14 | plug and play ventures | Branding | €66.01 | 43 | 5.57 | €11.86 | 6 |
| 15 | accelerator program for startups | Startup_Collab. | €64.92 | 58 | 2.50 | €25.97 | — |

QS 1/10 "Rarely shown": innovation hub, uk accelerators, open innovation platform, ai startup funding, startup incubator, innovation hackathon, accelerator programs.

**Top 20 search terms** (visible: 2,280 clicks / €2,789.95 / 74.90 conv.; other: 883 clicks / 30.67 conv.)

| # | Search term | Match | Ad group | Clicks | Cost | Conv. |
|---|---|---|---|---|---|---|
| 1 | plug and play | Exact (Added) | Branding | 196 | €276.44 | 10.75 |
| 2 | **startup india certificate** | Exact (Added + Excluded) | Startup_Collab. | 134 | €114.85 | 2.00 |
| 3 | **skywork ai** | Phrase cv (Excluded) | AI | 245 | €73.27 | 0 |
| 4 | plug and play ventures | Exact | Branding | 36 | €52.56 | 1.15 |
| 5 | plug and play tech center | Broad (Excluded) | Startup_Collab. | 49 | €37.22 | 2.00 |
| 6 | wron ai | Phrase cv | AI | 13 | €32.56 | 0 |
| 7 | playbook plug and play | Exact | Branding | 7 | €25.56 | 0 |
| 8 | plug and play accelerator | Exact | Branding | 20 | €24.71 | 2.00 |
| 9 | startup qatar | **AI Max** | Innovation | 7 | €21.86 | 0 |
| 10 | start up india certificate | Exact cv | Startup_Collab. | 22 | €21.39 | 1.00 |
| 11 | innocentive | Broad | Innovation | 12 | €21.22 | 1.00 |
| 12 | plug and play vc | Exact (Excluded) | Branding | 12 | €19.86 | 0 |
| 13 | plug and play abu dhabi | Phrase (Excluded) | Branding | 10 | €19.86 | 0 |
| 14 | flat6labs | Broad (Excluded) | Innovation | 4 | €18.97 | 0 |
| 15 | top 100 yc companies | Phrase cv | Startup_Collab. | 1 | €18.48 | 0 |
| 16 | pnptc | Broad | Startup_Collab. | 14 | €18.34 | 0 |
| 17 | plug and play tech center | Exact cv (Excluded) | Branding | 15 | €17.40 | 0 |
| 18 | plug & play ventures | Exact | Branding | 7 | €17.64 | 1.00 |
| 19 | how to sell ideas | Broad | Branding | 1 | €17.19 | 0 |
| 20 | idice startup bridge | Broad | Innovation | 10 | €15.64 | 0 |

Brand rows in the top 20: €491.25 (17.6% of visible cost).

Irrelevant terms in ranks 21–50:
- **Competitors / programmes:** accelerators in dubai; strategic gears; katapult africa accelerator; y combinator (excluded); dealmakers academy; hub71 initiate; khalifa fund for enterprise development; kaust taqadam; startup valley club.
- **Founder / investor:** angel investor; investors near me (AI Max); angel investors in saudi arabia; investors from saudi arabia; pre seed funding; startup qatar investment program; india uae startup.
- **Events / institutions:** founders forum; web summit 2027 (AI Max); dubai chamber of digital economy.
- **Government certificate:** startup india certificate apply online government website.

**Negatives (26, campaign level):** the same incubator set as NA, plus [plug and play abu dhabi], **[plug and play tech center]** (the company's own name, excluded as exact), [skywork ai], [startup india certificate], trading (broad) and wron (broad). The keyword "startup india certificate" started in the SA campaign (exact keyword there) and was carried into EMEA 20260813.

**Ads (4 RSAs)**

| Ad | Ad group | Strength | Clicks | Cost | Conv. | Cost/conv. |
|---|---|---|---|---|---|---|
| Startup Accelerator Program \| Join a Fintech Accelerator \| Venture Capital Accelerator (display path /startups/accelerator) | Startup_Collaboration | Excellent | 1,210 | €1,656.44 | 36.75 | €45.07 |
| Find the Right Startups \| Startup Scouting Platform \| Test Ideas with Pilot Programs | Branding | Good | 717 | €1,208.63 | 38.82 | €31.14 |
| Corporate Matchmaking \| Innovative Solution For You \| Start Your Innovation Journey | Innovation | Average | 519 | €989.11 | 22.25 | €44.45 |
| Plug and Play \| Global Innovation Ecosystem \| Business transformation | AI | Average | 719 | €512.47 | 7.75 | €66.13 |

In the biggest EMEA ad, headlines by cost are Connect With Corporations (€409.74), Global Innovation Ecosystem (€344.74), Plug and Play Tech Center (€308.05) and Startup Accelerator Program (€46.69). Descriptions include "Our startup accelerator programs link startups with corporate partners across industries." and "We run a venture fund and a global startup ecosystem." Google's insight on this ad reads "Search term categories your ad appears for: startup qatar, startup grind riyadh, plug and play ventures, + 94 more".

**Assets:** same campaign assets as NA (business name and logo disapproved; images, callouts and the Institutional Innovation sitelink added 10 Oct). Landing pages: welcome root → homepage €2,841.09 (2,410 clicks); /ultimate-innovation-platform €1,138.70; automatically selected /investment-portfolio €26.86 and /exploring-saudi-arabias-thriving-vc-ecosystem €4.43.

#### 2.2.3 US-SV coworking (campaign ID 20213311596) — active since 2023

| Item | Detail |
|---|---|
| Settings | Eligible (Limited); €5.00/day; Target CPA (avg €39.07); optimisation score 85.1%; 80 km around Silicon Valley, CA |
| Ad group | "Coworking" |
| Top keywords | virtual workspace (Paused) €515.75 / 22.39 conv.; co working space near me (QS 1/10, rarely shown) €259.10 / 8.00; shared office space €129.84 / 5.00; coworking space (Paused) €101.79 / 0.41; office space for rent €66.42 / 6.00 |
| Top search terms (visible €493.09) | plug n play sunnyvale €64.07 / 4.05; plug and play tech center sunnyvale €28.53; plug and play san jose €27.70; silicon valley startups €17.25; plug and play silicon valley €14.36; south park commons €10.30; 440 n wolfe road sunnyvale €6.39; regus / wework / hanahaus terms |
| Ad | "Office space in Silicon Valley \| Plug and Play \| Designed for startups" — "Come And Join Our Co-Working Community Designed Purely For Startups…", Average strength, 541 clicks, €1,064.80, 44.81 conv., €23.77 |
| Conversions | Welcome LPs 21, Contact website 22, HubSpot 1 |

Most of its spend goes on brand and address searches.

#### 2.2.4 Ended campaigns (summary)

| Campaign | Brand ad group share of cost | Top keywords (cost / conv.) | Top 3 ads (cost / conv. / cost per conv.) |
|---|---|---|---|
| EMEA 20251125 (€8,946.52) | 51.7% (Plug and Play AG €4,629.07) | "corporate accelerators" €563.41 / 23.16; "plug and play" €555.28 / 15.30; [plug and play] €545.54 / 15.30; "corporate incubator" €372.35 / 10.70; "corporate startup accelerator" €259.20 / 0.17 | "Global Innovation Ecosystem" (Poor) €4,012.87 / 80.75 / €49.70; **"Top Corporate Accelerator \| Corporate Innovation Lab \| Partner with Startups" (Good) €1,718.30 / 57.58 / €29.84**; same "Global…" ad in Corporate €1,303.94 / 6.75 / €193.15 |
| US 20251008 (€8,868.17) | 65.1% | "corporate accelerators" €757.12 / 19.32; [us startups] (in brand AG) €723.36 / 8.19; [plug and play] €534.86; [startups companies in usa] €467.22 | "Global Innovation Ecosystem" (Poor) €5,049.35 / 69.26 / €72.91; **"Top Corporate Accelerator" €1,723.21 / 48.04 / €35.87 (conv. rate 10.07%)**; "Fund Your Future" €484.93 / 3.21 / €151.08 |
| US-CA 20260114 (€8,669.74) | 27.0% | business incubator €2,108.30 / 32.20; "artificial intelligence innovation" €744.35 / 6.00; "san francisco startup accelerators" €614.94 / 0.19 (QS 1) | "Top Corporate Accelerator" €3,017.40 / 47.77 / €63.16; "Global…" brand €702.61 / 12.92; "Global…" Corporate (Poor) €1,913.80 / 9.39 / €203.76 |
| US-South-Central 20260115 (€6,360.89; ad groups named "Indiana_…") | 4.3% | product innovation strategy €2,129.24 / 7.92 (€268.80); startup scouting €2,044.02 / 15.29 | "Find the Right Startups" (Excellent) €1,588.70 / 13.51 / €117.63; "Global Innovation Ecosystem \| Plug and Play Tech Center" (Poor) €1,468.51 / 6.33; "Global…" €825.96 / 4.00 |
| FR 20260114 (€4,415.75) | 70.5% | [plug and play] €605.18 / 19.00; "plug and play" €350.32; [plug and play vc] €253.54; [plug n play] QS 2 | "Global…" (Poor) €2,525.98 / 56.39 / €44.79; "Fund Your Future" €470.07 / 6.00; "Top Corporate Accelerator" €602.53 / 7.00 / €86.08 |
| IT 20260114 (€2,356.54; tCPA €20 per ad group) | 52.4% | [idice startup bridge] €372.41 / 12.00; "accelerator program for startups" €212.84 / **15.00 (€14.19)**; [plug and play] €207.27 / 7.00 | "Global…" (Average) €712.36 / 27.45 / €25.95; "Fund Your Future" €241.90 / 4.00; "Plug and Play Tech Center \| World's Top Accelerator" €280.37 / 5.00 |
| SA 20260114 (€1,522.89) | 14.0% | business accelerator program €770.62 / 23.51 (€32.78); tech accelerator €157.33 / 9.10 (€17.28); strategy and innovation €199.13 / 2.51 | Not collected |

Search terms in ended campaigns:
- **EMEA 20251125:** 18 of the top 20 terms are brand ("plug and play", "plug and play abu dhabi", "…munich", "…spain").
- **US-CA:** competitor accelerators lead ("alchemist accelerator" €470.41, "south park commons" €175.67, "founders network", "venture smarter", "cofounderslab").
- **US-South-Central:** almost all irrelevant with zero conversions: VC firm names (bronco partners, boldstart ventures, high alpha), "yc request for startups 2026", and **textbook citations** ("barringer b r & ireland r d 2019 entrepreneurship… pearson").

The best-CPA ended ad groups were corporate-intent: IT Corporate €24.46 and SA Corporate €29.00 per conversion.

### 2.3 Conversion actions and change history

**Conversion actions (Goals > All conversions, 18 actions; "all conv." this year)**

| Goal category | Action | Source | Status | Primary / secondary | Count | Window | In account goals | All conv. |
|---|---|---|---|---|---|---|---|---|
| Submit lead forms | JTP-form | Website | Active | Primary | One | 30 d | Yes | 483.00 |
| Submit lead forms | GA4 contact_form_submission | GA4 | Active | Secondary | Every | 90 d | No | 137.09 |
| Submit lead forms | GA4 Form Sent Co-working / form_sent___jtp_corporate / form_sent___jtp_venture | GA4 | No recent conversions | Secondary | Every | 90 d | No | 0 |
| **Contacts** | **Contact website** | Website | Active | Primary | One | 30 d | Yes | **1,121.67** |
| **Contacts** | **Conversion Welcome LPs** | Website | Active | Primary | One | 30 d | Yes | **753.00** |
| Contacts | Smart campaign clicks to call (×2); Clicks to call, Contact (GA4), Coworking (removed) | — | No recent / Removed | — | — | — | — | 0 |
| **Qualified leads** | **Contacts – Contacts Lifecycle Stage becomes Lead and 1 more condition** (HubSpot import) | Import from clicks | Active | Primary | One | 90 d | Yes | 270.00 |
| Page views | GA4 acces_to_join_to_platform | GA4 | No recent conversions | Primary | Every | 90 d | Yes | 0 |
| Phone calls / directions / downloads | Smart-campaign and app actions | — | No recent / Removed | — | — | — | — | 0 |

Total all conv. 2,764.76.

**Change history highlights (NA and EMEA 20260813; latest 50 rows each; users from an external agency domain plus one pnptc.com user; some changes via "Google Ads API / Ads Perch (Unverified)" and Google Ads Editor)**

| Date (2026) | Campaign | Change |
|---|---|---|
| 23 Aug | NA | Budget decreased (amount not expanded) |
| 8 Sep | NA | AI Max on → off → on; automatically created assets off; text asset automation and final URL expansion opted out |
| 9 Sep | NA | Location option: "people in, searching for, or viewing pages about" → "people in my targeted location" |
| 15 Sep 3:48 PM | NA (Editor) | Standard goals: Contacts removed, Submit lead forms removed (→ Qualified leads only) |
| 15 Sep 3:59 PM | NA (Editor) | "Target CPA was €30.00" (tCPA removed) |
| 15 Sep 4:51 PM | NA + EMEA (API) | 26 broad keywords paused (NA), negative phrases added, RSAs changed; EMEA automated assets off |
| 16 Sep | NA + EMEA | Negative list "Competitor Accelerators and VCs" applied |
| 19 Sep | NA / EMEA | Budget €135.00 → €50.00 (NA); €104.00 → €43.00 (EMEA); image extension recommendation applied (NA) |
| 21 Sep | NA / EMEA | Budget €50.00 → €33.00 (NA); €43.00 → €30.00 (EMEA) |
| 20 Sep – 2 Oct | NA + EMEA | Many bid adjustments: Desktop −15% ↔ −30%, Tablet −50%, Mobile high-end +15%, audience segments −10% to +15% |
| **28 Sep 11:10 AM** | NA + EMEA (API) | **Standard goals: Qualified leads removed, Submit lead forms added** |
| 10 Oct | NA + EMEA | Recommendations applied by a user: Redundant keyword (24 broad keywords removed in each), New keyword (+1 NA, +2 EMEA), Callout, **Structured snippets (coworking)**, Image extension (EMEA), Improve RSA (EMEA) |
| 10 Oct 8:49–8:51 PM | NA / EMEA | Budget €33.00 → €30.00 (NA); €30.00 → €33.00 (EMEA) |
| **10 Oct 10:21 PM** | EMEA | **"Target CPA is €45.00"** + 4 bid adjustments |

### 2.4 Auction insights (Search)

| Campaign | Domain | Impression share | Overlap | Position above | Top of page | Abs. top |
|---|---|---|---|---|---|---|
| NA 20260813 | pitchbook.com | 17.02% | 10.37% | 60.46% | 84.18% | 39.89% |
| NA 20260813 | You | 12.68% | — | — | 61.24% | 28.62% |
| NA 20260813 | oneday.org | < 10% | 6.62% | 52.18% | 82.24% | 28.93% |
| EMEA 20260813 | pitchbook.com | 18.65% | 19.35% | 73.63% | 81.00% | 45.88% |
| EMEA 20260813 | You | 12.45% | — | — | 68.06% | 28.23% |
| EMEA 20260813 | amazon.com | < 10% | 8.10% | 79.58% | 84.01% | 47.92% |

Only three rows each; no other accelerator or innovation platform shows up as a competitor.

### 2.5 Recommendations and auto-apply (read only)

| Item | Value |
|---|---|
| Account optimisation score | 95.9% (Bidding & budgets +3%, Keywords & targeting +0.4%) |
| Open recommendations | "Adjust your budgets" +2.8% (projected +5.32 conversions/week at +€3.30 cost/conv.); "Expand your audiences" +0.3% (mentions TrueView views); "Remove redundant keywords" +0.1% (77, e.g. plug and play programs, plug and play apply, plug and play equity); "Add new keywords" +0.1% ("rental space for lease", "space for work") |
| Auto-apply | **Off**: "Maintain your ads 0 of 7 selected", "Grow your business 0 of 14 selected". The recommendation changes in the history were applied manually. |

### 2.6 Google — Working / To improve

**Working**
- **EMEA 20260813 is the more efficient active campaign:** €41.36 per conversion this year and €51.42 in L30D, with tCPA €45 since 10 Oct. **Saudi Arabia** is its best market (€32.26 per conversion with a +15% bid adjustment).
- **Corporate-intent ads and keywords win.** "Top Corporate Accelerator | Corporate Innovation Lab | Partner with Startups" was the best large ad in the old campaigns (€29.84 and €35.87 per conversion; conversion rate 8.93–10.07%). Corporate ad groups in IT (€24.46) and SA (€29.00) had the lowest CPAs; "accelerator program for startups" (IT) cost €14.19 per conversion.
- **PMax drove the cheapest HubSpot leads.** NA PMax (paused) produced HubSpot leads at €122.32 each, against €262.83 for NA Search and €396.97 for EMEA Search.
- **Hygiene is in place.** A competitor negative list exists (applied 16 Sep), NA was switched to "presence" location targeting (9 Sep), and auto-apply is off.

**To improve**
- **Optimise to qualified leads again.** Since 28 Sep both active campaigns optimise "Submit lead forms" (JTP-form plus GA4 secondaries), not the HubSpot qualified-lead import. "Contact website" (1,121.67) and "Welcome LPs" (753) are still primary account-default actions and inflate "conversions" in other campaigns.
- **Separate brand from non-brand.** Brand is 45.6% of NA cost and 43.8% of its visible search-term cost, while NA is "Limited by budget" (lost IS budget 27.80% in L30D). Brand should have its own campaign and budget; today the company name "plug and play tech center" is even excluded in EMEA.
- **Stop paying for startup-side traffic.**
  - Keywords: startup accelerator (QS 3/10), "venture capital financing for startups".
  - Headlines in a corporate ad group: "Venture Capitalist", "Fund Your Future", "Empowering Founders".
  - Sitelinks: the Google-AI "Services For Startups", "For Mentors" and "For Universities" get the most impressions.
  - Snippets: coworking structured snippets were added on 10 Oct.

  All of these pull founders, students and coworking seekers rather than corporate innovation leaders.
- **Add negatives from 2.2.** Competitors (South Park Commons, Alchemist, Boost VC, The Yield Lab, Y Combinator terms, Hub71, Flat6Labs), funding and grants (pre seed funding, angel investors, free grants), "startup india certificate" and textbook citations. Check what the competitor list actually contains.
- **Send traffic to a page with a form.** The biggest final URL is welcome.plugandplaytechcenter.com/, which redirects to the corporate homepage (newsletter form only): €5,810.72 across NA and EMEA this year. Use a corporate landing page with a qualifying form.
- **Fix the assets.** Business name and logo are disapproved; 14 of 18 images are disapproved for text overlays; there is a typo "public ector" in a sitelink. Old ads also contain "strategically-aligned of startups" and "Out platform". The startup counts are inconsistent ("50,000+" vs "100,000+").
- **Stabilise the setup.** Everything is broad match plus AI Max on €30–€33/day, with frequent budget cuts and dozens of bid-adjustment edits in three weeks. On 10 Oct a €45 tCPA was set with a €33 budget (budget below 1× tCPA). Fewer, larger changes would let bidding learn.
- **Govern who changes what.** Changes come from several users, an unverified API tool ("Ads Perch (Unverified)"), Editor and the Recommendations page. Five recommendation types were applied in one evening (10 Oct) without checking their content (the coworking snippets).
- **Review the coworking campaign.** It still runs (since 2023) and mostly buys brand/address searches.

---

## 3. ChatGPT Ads

ads.openai.com ("Ads Manager Beta"), account "Plug and Play", EUR, time zone CET (billing in UTC). Date range 1 Sep – 13 Oct 2026.

### 3.1 Campaigns

| Campaign | Active toggle | Status | Type | Impr. | Clicks | Conv. | Spend | CTR | Avg CPC | Avg CPM | Budget | Dates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Test 1 | On | Not serving (end date passed) | Conversions | 4,021 | 43 | **0** | €229.56 | 1.07% | €5.34 | €57.09 | €25.00/day | 23 Sep – 2 Oct 2026 |
| Plug and Play Tech Center campaign | Off | **Draft** (not "paused"); "Finish draft" | Conversions | – | – | 0 | €0.00 | – | – | – | "Set up" (none) | Start 16 Sep 2026 |

### 3.2 Test 1 settings (Edit Campaign window, closed with Cancel)

| Setting | Value |
|---|---|
| Objective / billing | Conversions / Impressions (CPM) |
| Locations | **United States only**; no exclusions |
| Eligible platforms | All platforms |
| Tracking parameters | **Empty** (no UTMs, no campaign/ad IDs on the click) |
| Included / excluded custom audiences | None ("No custom audiences yet") |
| Budget | Daily €25.00 |
| Schedule | Start 23 Sep 2026 10:55 AM GMT+2; end 2 Oct 2026 10:55 AM |
| Text customization | **On**: "AI automatically generates personalized and translated versions of your ad's headlines and descriptions, which may be shown without your individual review or approval." |
| Conversion event | Lead Created |
| Ad group "Generic" | Context hints: Open innovation programs for corporations; Governments looking to boost their startup ecosystem; University programs for startups and innovation; Investment in startups by companies; Corporate accelerators; Hackathons; Managing startups POCs as corporates. Billing event Impression; bid strategy Maximize results |

### 3.3 Ads (Test 1, 1 Sep – 13 Oct 2026)

| Ad | Text | Impr. | Clicks | Conv. | Spend | CTR | CPC | URL |
|---|---|---|---|---|---|---|---|---|
| Ad 5 | Plug and Play — "Discover seamless startup partnership opportunities." | 2,995 | 37 | 0 | €179.79 | 1.24% | €4.86 | https://www.plugandplaytechcenter.com/ |
| Ad 4 | "Build, buy, or pass? Make smarter innovation decisions with us." | 519 | 2 | 0 | €19.20 | 0.39% | €9.60 | homepage |
| Ad 2 | "Driving innovation for partners in 25+ industries worldwide." | 239 | 2 | 0 | €11.26 | 0.84% | €5.63 | homepage |
| Ad 3 | "Boost ROI with high-impact startup pilots." | 212 | 2 | 0 | €17.57 | 0.94% | €8.78 | homepage |
| Ad 1 | "Trusted innovation partners for 550+ leading global companies." | 56 | 0 | 0 | €1.75 | 0.00% | — | homepage |
| Draft ad | "Plug and Play \| We Drive Innovation" | – | – | – | – | – | – | homepage |

### 3.4 Pixel status (Conversions page)

| Item | Value |
|---|---|
| Data source | "My first pixel" (ID 1wviVmvm8RWCTitGD8C1sk), Web, status shows a warning icon, EQS "—", 19.2K events |
| Conversion event | "Lead Created" (lead_created), used by 1 campaign, identifier coverage 68%, 341 events |
| Warnings (2 medium) | "No recent server-to-server events … in the last 24 complete UTC hours"; "Some events are missing user data — Email coverage 1.8% (21,226 events), External ID coverage 0.0%" |
| Conversion API keys | "No conversion API keys yet." |
| On the website | The OpenAI pixel script (bzrcdn.openai.com/sdk/oaiq.min.js) loads on the homepage and all welcome pages checked |

### 3.5 ChatGPT Ads — Working / To improve

**Working**
- The context hints describe the right buyers (corporate open innovation, governments, corporate accelerators, startup pilots).
- CTR 1.07% and CPC €5.34 are in line with Google Search NA (CPC €2.02–€2.13) at a small test budget.
- The pixel is installed site-wide and the test stopped on schedule at €25/day.

**To improve**
- **Send clicks to a page that can convert.** €229.56 produced 0 conversions; every ad went to the homepage (no lead form) with **no tracking parameters**, so the visits can't be followed in GA4 or HubSpot. Use a dedicated landing page with a form, and add UTMs via "Tracking parameters".
- **Match the targeting to the goal.** Only the United States was targeted, even though the account bills in EUR and the goal includes EMEA corporations and governments.
- **Turn off text customization for this audience.** It was On, so the platform can rewrite copy without review.
- **Spread delivery across ads.** Ad 5 took 74% of impressions and all ads have the same "Plug and Play" title.
- **Fix the measurement before the next test.** Email coverage is 1.8% and there is no server-to-server connection. "Lead Created" fired 341 times — check what triggers it versus real form submissions.
- **Tidy the second campaign.** "Plug and Play Tech Center campaign" is a draft with no budget, not a paused campaign.

---

## 4. Landing pages

Checked 14 Oct 2026. Desktop = browser window 1,054 px wide; phone = the same page loaded at 390 px wide. No form was submitted.

### 4.1 Page by page

| URL | Used by | Title / headline | Audience | Match with ads | Form (desktop top position) | Phone 390 px |
|---|---|---|---|---|---|---|
| **welcome.plugandplaytechcenter.com/** → **redirects to www.plugandplaytechcenter.com/** | Google NA €2,969.63 + EMEA €2,841.09; ChatGPT Test 1 (homepage); Meta traffic ads | "Plug and Play \| We Drive Innovation"; H1 "We Drive Innovation" — "Empowering the future with corporations, governments, startups, investors, and universities." | Everyone | Weak: corporate ad copy lands on a generic homepage | **No lead form**; only a newsletter form (email + consent, "Sign up") at the bottom; CTA "Get In Touch" | No sideways scroll; page 8,769 px; two chat widgets ("Hey! Let's talk, I'm your personal AI agent." and "Accelerate your innovation") **cover the headline** on the first screen |
| /ultimate-innovation-platform | Google NA €1,553.73, EMEA €1,138.70; Meta PP-328, PP-324, PP-236, PP-220 | "PNPTC \| Corporate Innovation"; H1 "Start Your Innovation Journey"; stats 550+ partners / 60+ locations / 100K+ startups / 35+ unicorns | Corporations, startups, governments and VCs on one page | Partial | HubSpot "Get in touch" at 777 px (just below the first screen). Opens with a profile dropdown; corporate path = 12 fields, 11 required (see 4.2) | Form starts at **1,542 px** (≈ 2 screens down) |
| /embedded-ai-robotics | Meta PP-257 (Sept driver) | "How Embedded AI Robotics is Transforming Industries & Daily Life"; **no H1**; "360+ European robotics startups … $38B by 2035" | Corporate / industry readers | Yes (report) | Report form "Download now" at 199 px, 10 required fields + reCAPTCHA | Form at 675 px |
| /quantum-tech-report-2025 | Meta PP-50b/50c/196/291, TCb817, TCb368 "AICOI" | "The Quantum Leap: Transforming Industries With Emerging Tech"; **no H1** | Corporate tech leaders | Yes (TCb368 is named "AiCOE" but lands here) | Report form at 199 px | Form at 608 px |
| /the-success-story-of-mitsubishi-electric-and-kamet-ai | Meta TCb721, PP-366/368/369 | "Predictive AI Robotics: Mitsubishi Electric & Kamet AI Success Story" (H2, **no H1**) | Corporate | Yes, but the **case study is gated** behind the 10-field form | Report form at 199 px | Form at 635 px |
| /supply-chain-innovation-2025 | Google NA Innovation ad group €265.89 | Title "Boost your innovation strategy"; H2 "End-to-end Supply Chain Innovation Starts Here"; Holman × Wilya case study | Corporate supply-chain | Yes for "Supply Chain Innovation" ads; not for generic "open innovation" keywords | Contact form "Get in touch", 14 fields, at 175 px | Form at **948 px** |
| /spain-energy-grid | Meta PP-67, TCb820, TCb836 ("Grid") | "Investing in Spain's Grid Resilience"; H1 "The Grid Is Under Pressure. The Visionaries Will Build What Comes Next."; **English** | Energy / policy leaders | Yes | Report form at 191 px | Form at 547 px |
| /20-year-anniversary-book | Meta PP-103b (retargeting) | H1 "Celebrating 20 years of innovation, collaboration, & growth"; "30+ Unicorns Valued $1B+" | Brand / retargeting | Yes | Short form "Download Now", 8 fields (5 required: names, email, profile, interest; company and size optional), at 191 px | Form at 493 px |
| /company-performance-report-2025 | Meta PP-102b, PP-199, PP-239, PP-240 | H1s "A Year in Review" / "Our 2025 Awards & Recognition" / "Some highlights from 2025" (3 H1s) | Brand / retargeting | Yes | "Access Now", 9 fields, at 227 px | Form at 623 px |
| /ultimate-ai-playbook | Meta PP-231, PP-138; Google sitelink "Get The AI Playbook" | H1 "From Experimentation to Enterprise-Wide Impact"; "10 AI deployments from inside Plug and Play's partner network" | Enterprise AI leaders | Yes | Report form at 191 px | Form at 613 px |
| /health-innovation-platform | Meta Health ad sets (TCb729, TCb176, PP-266) | Title "Boost your innovation strategy" (same as supply chain); H2 "End-to-end Health Innovation Starts Here"; **no H1** | Healthcare leaders | Yes | Contact form, 14 fields, at 175 px | Form at **894 px** |
| /monitoring-decarbonization-in-buildings | Meta TCb826, TCb828, TCb837 | H1 "Buildings Are the Next Frontier for Climate Action" | Real estate / sustainability | Yes | Report form at 191 px | Form at 667 px |
| www…/innovation-services/ai-center-of-excellence | Meta traffic ads (PP-346, PP-285) | "AI Centers of Excellence \| Plug and Play"; "Your strategic hub for AI adoption, innovation, and talent development." | Corporate AI | Partial | **No lead form**; newsletter only at 10,658 px; 78 links, full menu | not measured |
| /the-success-story-of-aeroporti-di-roma-and-ottonomy | Meta PP-299 | "The Success Story of Aeroporti di Roma and Ottonomy"; **no H1** | Corporate travel | Yes | Report form at 199 px (gated case study) | not measured |
| /french-ai-startups-to-watch-in-2026 | Meta PP-163, PP-173, PP-345 | H1 "Emerging Innovators to Market Leaders"; "AI startups personally picked by 16 investors" | Investors / scouting teams | Yes | Report form at 191 px | not measured |
| /2026-enterprise-ai-strategy-pulse-survey-plug-and-play | (in ad names) | H1 "Breaking Down the Enterprise Value of AI Pilots"; "…how top Fortune 500 leaders…" | **Large enterprises** (closest to the goal) | — | Report form at 191 px | not measured |
| /ultimate-enterprise-ai-trend-report | Meta PP-70b, PP-323, TCb726 | "The Ultimate Enterprise AI Trend Report"; **no H1** | Enterprise | Yes | Report form at 199 px | not measured |
| /innovation-assessment-report-plug-and-play | Meta PP-272 | H1 "The State of Innovation Readiness 2026"; "surveyed over 1,000 professionals from corporations, government bodies and universities" | Corporate / government | Yes | Report form at 191 px | not measured |
| /ai-enabled-waste-recovery | Meta PP-307 | H1 "Reclaiming Billions in Recoverable Resources" | Industry / sustainability | Yes | Report form at 191 px | not measured |
| /unicorn-report | (in ad names) | H1 "The next unicorn is already out there. We've been there from day one."; "our **40+ unicorns**" | Investors / startups | — | Report form at 191 px | not measured |
| welcome…/startups/accelerator | Display path of the EMEA "Startup Accelerator Program" ad | **404 "Page not found"** | — | Only a display path (real final URLs are listed in 2.2.2) | — | — |

All pages checked had no sideways scrolling at 390 px. Pages marked "not measured" were not checked on phone.

### 4.2 Forms (fields, required, dropdowns, button)

| Form | Pages | Fields | Dropdown options | Button |
|---|---|---|---|---|
| **Report template** | embedded-ai-robotics, quantum, Mitsubishi, Spain grid, AI playbook, decarbonization, Ottonomy, French AI, pulse survey, trend report, innovation assessment, waste recovery, unicorn | First Name*, Last Name*, Email*, Company Name*, Company Website*, profile*, job title*, **"How many employees work at your company?"***, "What country are you based in?"*, consent checkbox* (10, all required) + reCAPTCHA Enterprise | Profile: major corporation / angel investor or VC / startup / government institution / university / **student** / **looking for job opportunities** / Other. Job title: C-Level, EVP/SVP, VP, Director, Manager, Associate, Other. Size: 1-10 … 1,001-10,000 / **10,001+**. Country: 187 options | "Download now" |
| **Contact template** | supply-chain-innovation-2025, health-innovation-platform | Profile*, First name*, Last name*, Email*, Organization name*, organization website*, "What Plug and Play location interests you?"* (a 187-country list, not Plug and Play locations), industry* (28), phone (optional), job title*, reason* (text), Company Size, "How did you hear about us" (Search Engine / AI Search / LinkedIn / Youtube / Word of Mouth / Email / Event / PR), consent (14) | as above | "Get in touch" |
| **/ultimate-innovation-platform** | 1 page | Starts with a profile dropdown only. **Corporation or government** adds: First name*, Last name*, Email*, Organization name*, website*, location* (country list), industry*, phone (optional), job title*, reason*, consent* (12 fields, 11 required, **no company size**). **Startup** adds ~25 inputs (LinkedIn, 12 interest checkboxes incl. "Office Space", stage, paying customers, raising, capital raised, pitch deck) | Profile: student / angel investor or VC / startup / government or public sector / major corporation / university / Other | "Get in touch" |
| 20-year book / CPR 2025 | 2 pages | 8–9 fields; company name and size optional; "What are you interested in" (3 options) | — | "Download Now" / "Access Now" |
| Homepage / AI CoE | 2 pages | Newsletter: email* + "I agree to receive information about Plug and Play"* | — | "Sign up" |

Privacy text on the forms: "By submitting this form you are agreeing to be contacted by Plug and Play … Plug and Play will not sell or share your information to third parties and you may unsubscribe at any time."

### 4.3 Cookie banner, proof, leak links, tags

| Item | What I saw |
|---|---|
| Cookie banner (CookieYes, all pages) | Pop-up in the centre: "We value your privacy — We use cookies to enhance your browsing experience, serve personalised ads or content, and analyse our traffic. By clicking "Accept All", you consent to our use of cookies. Cookie Policy". Buttons: **Customise / Reject All / Accept All**; preference centre: Reject All / Save My Preferences / Accept All. Hidden in this browser because a choice was already stored; I could not click it |
| Proof | Partner logos (JLR, Bayer, Daimler Truck NA, Volvo Group, Porsche, Samsung, PepsiCo, Mitsubishi Electric, MUFG, NYC EDC…), Roche Diagnostics quote, data partner "appliedAI Institute for Europe", named experts on report pages. **Inconsistent numbers:** "35+ Unicorns" (/ultimate-innovation-platform), "30+ Unicorns" (anniversary book), "40+ unicorns" (unicorn report); "100,000+ startups" vs "50,000+" (Google ad) |
| Leak links | welcome pages: 18–22 links (logo, "Contact", "Join the Platform", "Get in touch today", 4 social, hubspot.com ×2, the web agency credit ×3). Homepage: 156 links incl. "Join a Startup", jobs.pnptc.com, social. AI CoE page: 78 links |
| Tags (view of loaded scripts) | All pages checked: Meta Pixel (fbq), GTM-KB86JKSP, Google Ads AW-11114141677, GA4 G-VKRQ69SPCS (+ G-252977536 on welcome pages), HubSpot, OpenAI pixel (oaiq), CookieYes |

### 4.4 Landing pages — Working / To improve

**Working**
- **The report template is tidy.** On desktop the form sits next to the headline (top 191–199 px); on phone it starts within about one screen (493–675 px). There is no sideways scrolling, and leak links are few (18).
- **The report form can qualify the target.** It asks company size (10,001+ is an option) and seniority (C-Level, EVP/SVP, VP…).
- **Topic offers match the ads well** (quantum, embedded AI robotics, Spain grid, decarbonisation, AI playbook).
- **Tags and consent are complete.** All tags (Meta, Google Ads, GA4, HubSpot, OpenAI) load, and the cookie banner offers "Reject All" on the first layer.

**To improve**
- **Fix Google's biggest landing page.** welcome.plugandplaytechcenter.com/ redirects to the corporate homepage with no lead form (€5,810.72 this year across NA and EMEA). Point Search ads to a corporate page with the qualifying form.
- **Split /ultimate-innovation-platform by audience.** It speaks to corporations, startups, governments and VCs at once. The form opens with only a dropdown, has no company-size question on the corporate path, and asks "What Plug and Play location interests you?" with a 187-country list. On phone the form starts at 1,542 px.
- **Bring contact forms up on phone.** The contact-template pages (supply chain, health) show the form at 894–948 px. Their 14 fields include optional ones that could be dropped.
- **Remove low-intent profile options.** "I am a student" and "I am looking for job opportunities" are on every report form, so these downloads also count as Meta "welcome_conversions".
- **Reconsider gating case studies.** The Mitsubishi × Kamet and Aeroporti di Roma case studies sit behind 10 required fields; "proof" content usually works better ungated or with a shorter form.
- **Fix the page basics.** Several pages have no H1 (embedded AI, quantum, Mitsubishi, health, Ottonomy, trend report) and the CPR page has three. Two pages share the title "Boost your innovation strategy".
- **Align the proof numbers** (30+ / 35+ / 40+ unicorns; 50,000+ vs 100,000+ startups).
- **Clear the phone hero on the homepage.** The two chat widgets cover the headline.

---

## Not done / where to continue

| Item | Status |
|---|---|
| Meta change history (to verify the $310 → $160 budget cut on 18 Sep) | Not opened |
| Month-by-month view to confirm Quantum = Jan, Grid = Feb, AICOI = May | Not opened |
| Daily conversions to confirm the tracking gap 15 Jul – 11 Aug | Not opened |
| PP-36x / PP-266 list: 10 middle rows (spend between $2.46 and $21.15) | Not captured |
| Google: UK, New York, Florida, Texas, New Jersey, Arizona and US-East-Coast campaigns in detail; SA ads and search terms | Only totals and account-level keyword rows |
| Google: change history before 23 Aug (NA) and before 15 Sep (EMEA) | Not loaded |
| Google: contents of the "Competitor Accelerators and VCs" negative list | Not opened |
| Phone check for the last 7 report pages | Not measured (same template as the measured ones) |
| Cookie banner "Reject All" click | Not possible (consent already stored in this browser) |

To continue: start with "Meta change history" and "Google UK / state campaigns". Everything else in sections 0–4 is complete.

