# Read-only audit of Plug and Play's paid media: campaign structure, ads and landing pages

## Context
You're helping Felipe Cárdenas (Performance Marketing & CRM, Plug and Play Tech Center). Plug and Play connects large corporations and governments with startups. Paid media has one goal: as many leads as possible from our target customers – corporations with 10,000+ employees and $100M+ revenue (Head of Innovation, R&D, Chief Digital Officer, C-level) and government bodies. Startup founders are a secondary audience.

Your findings will become a presentation for managers who don't know advertising. I need:
- the real structure of each campaign: campaign → ad sets or ad groups → ads → landing page
- what performed well and why
- what can be improved

In scope: Meta Ads (ad account "Plug and Play Tech Center – Dollars", USD), Google Ads Search and Performance Max (EUR), ChatGPT Ads (EUR), and the landing pages these ads send people to.
Out of scope, skip completely: YouTube, Video, Demand Gen and Display campaigns, LinkedIn, HubSpot, Salesforce.

Background from the agency's weekly reports. Confirm what you can see and correct anything that's wrong:
- Conversion tracking stopped on Meta and Google from about 15 Jul to 11 Aug 2026, so results in that window are undercounted.
- On 13 Aug 2026 Google was rebuilt into two non-brand Search campaigns (NA and EMEA).
- Around 14 Sep 2026 Google's conversion goal was switched to "HubSpot qualified leads" only, and the target CPA was removed on NA Search. On 10 Oct 2026 EMEA Search got a target CPA of €45.
- Meta budgets were cut from $310/day to $160/day on 18 Sep 2026.
- Case-study static ads were launched on 8 Oct 2026 (the report doesn't say on which channel).
- Ads the agency named: "Quantum" (top Meta ad in January), Spanish "Grid" ads (lowered the cost per lead in February), "AICOI" (took a large share of Meta spend at a high cost per lead in May). The agency also refers to "PP-257" (main lead driver in September) and "PP-266" (to pause).

## Rules – read-only, no exceptions
1. Look, don't touch. Never click Publish, Save, Apply, Confirm, Create, Duplicate, Delete, on/off switches, budget fields, "Apply recommendation", "Dismiss" or "Fix". Changing the date range, columns, filters and breakdowns of a report is fine.
2. If you have to open an edit panel to read a setting, change nothing and close it without saving (choose "Discard" or "Close" if asked). If Ads Manager shows a "Review and publish" bar or a draft, or anything else looks changed, stop and tell Felipe straight away.
3. Never submit a form on any website: every submission creates a real lead. Don't open Meta Leads Center, lead downloads or anything showing people's names or emails. No personal data in the report.
4. If you hit a login, a 2-step code, a permission request, a payment page or a "Save file" dialog, stop and ask Felipe.
5. On websites, close cookie banners with the most restrictive option ("Reject" or "Only necessary"), after noting what the banner says.
6. Facts only. Copy numbers exactly as shown, with the currency. If you can't see something, write "not visible". Don't guess.

## Dates
Use two ranges and write the exact dates you used: "This year" = 1 Jan 2026 to yesterday, and "Last 30 days".

## How to work
- Do the parts in order: 1 Meta → 2 Google → 3 ChatGPT → 4 Landing pages. If Felipe asks for one part, do only that part. If he says "continue from 1.3", start there.
- End each part with "Working" and "To improve" points in plain language, each tied to something you saw.
- If the work gets long, stop after a numbered step, give the report so far and say exactly where to continue.

---

## Part 1 – Meta Ads Manager
Campaign names as they appear in Ads Manager (from Felipe's 1 Jan – 12 Oct 2026 export). Paste part of a name into the search box to find it.

Active on 12 Oct:
- Geo:WW_Objective:lead_Type:retargeting_Budget:cbo_Date:20260612
- Geo:US-California_Objective:lead_Type:prospecting_Budget:cbo_Date:20260602
- Geo:US-East-Coast_Objective:lead_Type:prospecting_Budget:cbo_Date:20260617
- Geo:USCA_Objective:lead_Type:prospecting_Budget:cbo_Date:20260617
- Geo:EMEA_Objective:lead_Type:prospecting_Budget:cbo_Date:20260712
- Geo:US-Middle-South_Objective:lead_Type:prospecting_Budget:cbo_Date:20260617
- Geo:Middle-East_Objective:lead_Type:prospecting_Budget:cbo_Date:20260709
- Geo:Western-Europe_Objective:lead_Type:prospecting_Budget:cbo_Date:20260709
- Geo:USCA_Objective:traffic_Type:cold_Budget:abo_Date:20260716

Ended, with the lowest cost per registration (what worked):
- Geo:All_Objective:welcome_Type:ABO_Date:20251010
- Geo:EMEA_Objective:lead_Type:prospecting-test_Budget:cbo_Date:20251010
- Geo:EMEA_Objective:lead_Type:retargeting_Budget:cbo_Date:20260109
- Geo:USCA_Objective:lead_Type:prospecting_Budget:cbo_Date:20251010

Ended, high spend at a higher cost per registration (to compare):
- Geo:EMEA_Objective:lead_Type:prospecting_Budget:abo_Date:20260210
- Geo:US-EastCoast_Objective:lead_Type:prospecting_Budget:cbo_Date:20260409

In the export, most lead campaigns count custom conversion 1759876678043283 as their result, the two retargeting campaigns count "Complete registration", and Geo:US-EastCoast…20260409 counted a custom event called "welcome_conversion".

1.1 Campaign list (This year): every campaign that spent – name, status, objective, budget (campaign or ad set level, per day), spend, results, result type, cost per result, link CTR, CPM, frequency. Add spend, results and cost per result for the Last 30 days.

1.2 Structure – for each campaign named above:
a) Campaign: objective, where the budget sits (campaign or ad sets) and how much per day, bid strategy or cost target.
b) Each ad set: name, status and delivery note (e.g. "Learning limited"), locations, age, languages, audience (Advantage+ audience on or off; the actual interests, job titles, custom audiences or lookalikes), exclusions, placements, conversion location (website / instant form / both), optimisation event, attribution setting, spend, results, cost per result, frequency – This year and Last 30 days.
c) Each ad (for ended campaigns: the top 5 by spend): name, format (image / video / carousel), what the visual shows in one line, the words on the image or video, the first two lines of the primary text, headline, CTA button, destination URL with its UTM parameters, which Advantage+ creative enhancements are on, spend, results, cost per result, CTR. Add the "Creative diversity" label if Ads Manager shows one.

1.3 Best and worst ads: the 5 best and 5 worst ads This year by cost per result (at least $300 spend each), with one or two plain sentences on what's different about each (offer, visual, message, audience, page). Then find the ads the agency named (Quantum, Grid, AICOI, PP-257, PP-266, the 8 Oct case-study ads): which campaign and ad set each sits in, what it shows, and how it did.

1.4 Events Manager (read-only): every conversion event and custom conversion, what each one counts (its URL or event rule), whether it is receiving events now, and which one each campaign optimises for. Say what custom conversion 1759876678043283 and "welcome_conversion" are.

1.5 Meta Ad Library (facebook.com/ads/library – search the Plug and Play Tech Center page, all countries, active and inactive ads): number of active ads, formats, languages, and the Ad Library link of every ad listed in 1.2c so Felipe can save the images. If the EU transparency section shows audience data (age, gender, countries), note it.

1.6 Working / To improve (Meta).

## Part 2 – Google Ads (Search and Performance Max)
Campaign names as they appear in Google Ads (from the 1 Jan – 12 Oct 2026 report).

Active on 12 Oct:
- Geo:NA_Channel:GoogleAds_Network:search_Type:non-brand_Goal:leads_Date:20260813
- Geo:EMEA_Channel:GoogleAds_Network:search_Type:non-brand_Goal:leads_Date:20260813
- Geo:US-SV_Network:search_Type:coworking-startup_Objective:lead_Channel:Google_Date:20230530

Ended non-brand Search, with the lowest cost per conversion (what worked):
- Geo:IT_Network:search_Type:non-brand_Objective:conversion_Channel:Google_Date:20260114
- Geo:SA_Network:search_Type:non-brand_Objective:conversion_Channel:Google_Date:20260114
- Geo:FR_Network:search_Type:non-brand_Objective:conversion_Channel:Google_Date:20260114
- Geo:EMEA_Network:search_Type:non-brand_Objective:conversion_Channel:Google_Date:20251125

Ended non-brand Search, high spend at a high cost per conversion (to compare):
- Geo:US-CA_Network:search_Type:non-brand_Objective:conversion_Channel:Google_Date:20260114
- Geo:US-South-Central_Network:search_Type:non-brand_Objective:unknown_Channel:Google_Date:20260115

Performance Max:
- Geo:NA_Network:pmax_Objective:conversion_Channel:Google_Date:20260608
- Geo:EMEA_Network:pmax_Objective:lead_Date:20260819
- EMEA_EN_DC_PMax_Quiz
- US_EN_DC_PMax_Quiz

2.1 Campaign list (This year): every Search and Performance Max campaign that spent – name, type, status, daily budget, bid strategy and target, spend, clicks, CTR, avg. CPC, conversions, cost per conversion, conversion rate, search impression share, impression share lost to budget, lost to rank. Add spend, conversions and cost per conversion for the Last 30 days. Then, for the campaigns named above, split conversions by conversion action (Segment → Conversions → Conversion action).

2.2 Structure – for each Search campaign named above:
a) Settings: networks (Search partners / Display on or off), locations and the location option ("Presence" vs "Presence or interest"), languages, conversion goals used, AI Max (on or off, and which features), broad match setting.
b) Ad groups: name, theme, spend, conversions, cost per conversion.
c) Keywords: top 15 by cost – keyword, match type, Quality Score and its three parts (expected CTR, ad relevance, landing page experience), cost, conversions.
d) Search terms: top 20 by cost This year with their conversions; then the search terms that don't fit corporate innovation (jobs, students, startups looking for funding or an accelerator, other companies' brands…) with their cost.
e) Negative keywords: how many, which lists, obvious gaps.
f) Ads (active campaigns: all; ended campaigns: the top 3 by spend): every headline and description, any pinned ones, ad strength, final URL, stats.
g) Assets: sitelinks (text + URL), callouts, structured snippets, images, lead form.

2.3 Conversions (Goals → Conversions, read-only): each conversion action – name, source, primary or secondary, what it counts, conversion window. Then open Change history (view only) and check the background points about the 14 Sep goal switch, the NA target CPA and the €45 EMEA target. Write the dates you see.

2.4 Auction insights for the two non-brand campaigns (last 90 days): the competing domains and their impression share.

2.5 Recommendations page: optimisation score and the recommendations as listed; the auto-apply settings (read only). Apply or dismiss nothing.

2.6 Working / To improve (Google).

## Part 3 – ChatGPT Ads
Campaigns: "Test 1" (ran 23 Sep – 2 Oct 2026) and "Plug and Play Tech Center campaign" (paused, no spend).
For each campaign: objective, dates, budget, locations, languages, bid. Every ad group: the context hints in full, bid. Every ad: title, description, image (one line), landing page URL. Stats: impressions, clicks, CTR, CPC, spend, conversions. Whether a pixel or conversion event is set up and receiving events. Then Working / To improve.

## Part 4 – Landing pages
List every unique destination URL used by the ads in Parts 1–3 (without UTM parameters) and which ads use it. For each page, on desktop and, if you can resize the window, at phone width (about 390 px):
- Page title, main headline, language
- Who it speaks to (corporates, governments, startups, investors, everyone) and the main promise
- Does it match the ads that send traffic to it (same offer, same words)? Yes / partly / no, and the difference
- The form: visible without scrolling? Every field and whether it's required; the options in any role, company size or profile dropdown; the button text. Do not submit.
- Proof on the page (client logos, numbers, testimonials, case studies)
- Links or menus that lead away from the form
- The cookie banner: what it says and which options it offers
- Anything broken, slow or awkward on a phone
- Optional: in view-source, whether the Meta Pixel (fbevents.js) and the Google tag (gtag.js / googletagmanager.com) load

Then Working / To improve for the pages.

## Output
One Markdown report with these headings: 0. Access and dates · 1. Meta · 2. Google Search · 3. ChatGPT Ads · 4. Landing pages. Use tables for every list. Under "0", say what you could and couldn't open.
