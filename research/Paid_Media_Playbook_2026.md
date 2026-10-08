# Paid Media Playbook 2026: B2B lead gen on Meta and Google (for PnP)

As of 8 Oct 2026. Three research passes covered Meta, Google, and measurement / new angles.

**Read this first:**
- The research proxy blocked direct page opens, so every point comes from search-result summaries of the cited pages. YouTube videos were not watched; practitioner views come from written summaries of their content.
- Check any figure on the source page before quoting it outside the team.

**Labels:**
- [OFFICIAL] Meta, Google or HubSpot documentation or announcement.
- [DATA] Benchmark or study.
- [PRAC] Practitioner opinion.
- [VENDOR] Agency or vendor claim.

---

## 1. The 10 things that matter most for PnP

1. **Optimise on a qualified signal, not on form fills.** Both platforms train toward whoever fills forms. At PnP that is mostly startups: 79% of JTP Contact us contacts are startups (ICP report).
   - Send a same-day "ICP-qualified lead" event back to Meta and Google: corporate or government, 10,000+ employees, target role.
   - Count startup leads at value 0, or not at all.
   - [OFFICIAL] Meta Conversion Leads docs; [PRAC] Verto Digital, Zapier/Meta guide.
2. **SQL is too slow to be the bidding signal.** PnP's MQL→SQL takes 66 days.
   - Meta needs the optimised stage within 28 days.
   - Google imports must arrive within 90 days of the click, and won deals (about 245 days) never fit.
   - Use a fast proxy event for bidding, and import SQL and opportunity for reporting and value.
   - [OFFICIAL] Meta Conversion Leads integration; Google Ads Help 14274408.
3. **HubSpot lifecycle stage is not a usable signal today.** About 95% of JTP contacts are already "SQL" in HubSpot (ICP report).
   - Syncing "lifecycle = SQL" to the ad platforms would teach them nothing.
   - The signal has to come from Salesforce lead status or from a fit property instead.
   - This is PnP-specific, from our own data.
4. **On Meta, creative is now the targeting.** Andromeda (Meta's ad retrieval system) picks ads by creative, and detailed targeting is only a suggestion.
   - Use broad audiences with hard controls: location, language, minimum age, custom-audience exclusions.
   - Run 8 or more genuinely different concepts per ad set, each aimed at one persona, with the qualification written into the ad ("For innovation leaders at 10,000+ employee companies").
   - [OFFICIAL] Meta Engineering Dec 2024; [PRAC] Jon Loomer 2025–26.
5. **Instant forms: use Higher Intent, qualifying questions and lead filtering.** Meta's Conversion Leads optimisation works only with Instant Forms, not website forms.
   - The JTP Contact us form is on the website, so it needs CAPI website events instead (HubSpot integration).
   - [OFFICIAL] Meta docs; [PRAC] Loomer.
6. **On Google, keep brand, non-brand and competitor terms in separate campaigns,** with exact and phrase match as the core.
   - Use broad match only where Smart Bidding gets quality signals.
   - At about €7.5k a month, PnP is below the $10–50k a month band where Smart Bidding performs best.
   - [DATA] Optmyzr 14,584 accounts; Optmyzr Feb 2026 match-type study.
7. **AI Max has no strict "whitelist" mode.**
   - URL inclusions (ad-group level) add candidate pages; they do not restrict expansion to them.
   - The hard controls are campaign-level URL exclusions (startup pages, careers, events, blog) or turning URL expansion off.
   - Messaging restrictions (up to 40 per campaign) can keep "for startups" wording out in every language.
   - Relevant to Thiago's whitelist plan before 30 Oct. [OFFICIAL] Google Ads Help 16230205, 16489313.
8. **Report cost per SQL and pipeline next to CPL.**
   - Cheap leads can hide a worse customer acquisition cost. In one dataset, retargeting had a CPL that looked cheap but a CAC of about $26.7k vs about $5.6k for prospecting.
   - [VENDOR/DATA] Metadata 2026 benchmark.
9. **Local-language creative and landing pages for FR, UK, DE, ES and IT.** PnP's own result (local beats generic 3:1 on cost per lead) is stronger evidence than any external benchmark found.
10. **Add a "How did you hear about us?" field.**
    - With 245–272-day journeys, software attribution misses most of the influence. In Refine Labs' data, buyers credited podcasts with 53% of revenue that software attributed 0%.
    - [VENDOR/DATA] Refine Labs; Dreamdata 2026.

---

## 2. What changed in 2025–2026

**Meta**
- **Andromeda retrieval system (from Dec 2024):** the diversity of creative concepts and personas matters more than splitting ad sets. [OFFICIAL]
- **Advantage+ is the default for the Leads objective (Feb 2025).** Most audience inputs are now suggestions; minimum age (up to 25) is the only hard age control. [OFFICIAL/PRAC]
- **Targeting removals:**
  - Detailed-targeting exclusions were removed in 2025. Use custom-audience exclusions instead.
  - Consolidated interests had to be replaced by 15 Jan 2026. [OFFICIAL/press]
- **New in 2025:**
  - Value Rules: raise or lower bids by segment such as country, placement or age.
  - Creative Testing tool: 2–5 test ads with even spend, suggested at no more than 20% of budget.
  - Opportunity Score (9 Jun 2025): Meta claims a 12% median lower cost per result when its recommendations are applied. [OFFICIAL]
- **CRM connections:**
  - Native HubSpot and Salesforce integrations.
  - The separate Offline Conversions API was reportedly retired in May 2025 (vendor claim, not confirmed by Meta).
  - Make's CAPI-for-CRM app is free from Feb 2026 to Feb 2028.
- **Attribution:** the 7-day-view and 28-day-view windows were removed from the Insights API on 12 Jan 2026, so less long-cycle credit is visible. [PPC Land]
- **EU signal:** users have had a "less personalised ads" option since Jan 2026, which weakens signal for those who opt out. [eMarketer]
- **No political or social-issue ads in the EU since 6 Oct 2025 (TTPA).** Government or policy-themed creative risks rejection. Relevant to PnP's government ICP. [PPC Land]
- **Location fees from 1 Jul 2026:** UK 2%; France, Italy and Spain 3%; Germany not listed. This is a direct headwind to the "Meta CPL −20%" KPI. [eMarketer]
- **Generative AI creative tools:** video generation from images, dubbing and translation in one step, brand kits. Audit "Advantage+ creative enhancements", which can rewrite qualifying copy. [OFFICIAL/PRAC]

**Google**
- **AI Max for Search** launched in May 2025 and reportedly went generally available on 15 Apr 2026 [secondary source].
  - It has three parts: search-term matching, text customisation and final URL expansion.
  - Since Oct 2025 the search terms report has a "Source" column that separates keyword matches from AI Max matches. [OFFICIAL]
- **Auto-upgrade:** campaigns using automatically created assets, or the campaign-level broad match setting, were due to auto-upgrade to AI Max in Sept 2026. The Dynamic Search Ads sunset moved to Feb 2027. **Check whether PnP's campaigns were upgraded.** [secondary]
- **Brand lists:** new brand lists on Search require AI Max (May 2025). [OFFICIAL]
- **Performance Max:** up to 10,000 negative keywords, a full search terms report, channel reporting (data from 6 Jun 2025) and brand exclusions. [OFFICIAL]
- **Offline conversion uploads:** new offline conversion imports and enhanced conversions for leads uploads go through the **Data Manager API** from 15 Jun 2026. Enhanced conversions for web and for leads are merged into one setting. [OFFICIAL via PPC Land]
- **Bidding names:** "Maximize conversions with a target CPA" was renamed "Target CPA" (Jun 2026). [OFFICIAL]
- **Google Marketing Live 2026:**
  - AI Brief steers AI Max in plain language.
  - **Qualified Future Conversions** predicts conversions up to 180 days after the click. It fits PnP's cycle but is in limited test. [OFFICIAL via SEJ]
- **Ads in AI Overviews and AI Mode:** eligible only for broad or keywordless targeting. No confirmed ad serving in the UK, Germany or France yet; France got AI Mode in Jul 2026 without ads. [OFFICIAL via SEL]
- **Consent Mode v2** is mandatory in the EEA, and its modelling thresholds are hard for low-volume B2B accounts to reach.

**Cross-channel**
- **ChatGPT Ads** live in 31 European markets, including France, Germany, Spain and Italy, from 24 Aug 2026; the UK launched in June. Ads show only to Free and Go users, and EU ads are reportedly not personalised at launch. [OFFICIAL]
  - A pixel and Conversions API launched 5 May 2026, followed by conversion-optimised CPC.
  - HubSpot can sync conversion events to ChatGPT Ads (beta). [OFFICIAL HubSpot KB]
  - One B2B pilot spent about $1,470 and got 0 conversions. OpenAI publishes no benchmarks. [DATA, thin]

---

## 3. Meta playbook for B2B

**Structure**
- Use Advantage campaign budget (CBO) with 1–3 broad ad sets for scaling, and ad-set budgets (ABO) for controlled tests. [PRAC]
- Aim for about 50 optimisation events per ad set per week; raise budgets about 20% at a time. [PRAC]
- Keep prospecting and retargeting in separate campaigns.
- Do not split ad sets by interest: they overlap and stay in "Learning Limited". [PRAC Loomer]
- Very narrow stacks of job title, interest and company size (about 8k people) drive CPMs up. One agency widened to about 300k and moved the qualifying into the creative; it reports CPL down 40–60% (single case). [PRAC]

**Lead quality**
- **Conversion Leads (CAPI for CRM).** Meta's own claim: 15% lower cost per quality lead and a 44% higher lead-to-quality rate vs the Leads goal. [OFFICIAL figure]
  - Works only with Instant Forms.
  - Needs about 200 leads a month and at least daily uploads.
  - The optimised stage must happen within 28 days and convert at 1–40%.
  - Store the Meta Lead ID in the CRM.
- **HubSpot's native Meta CAPI integration** syncs lifecycle changes and HubSpot form submissions.
  - Only events after setup count, and only HubSpot forms sync.
  - Install the pixel only through HubSpot to avoid duplicates.
  - Deal stages are not covered natively (vendor claim). [OFFICIAL HubSpot KB 2026]
- **Instant form controls:**
  - Higher Intent type.
  - Lead filtering, so only qualifying answers can submit.
  - Conditional logic.
  - Required work email.
  - SMS verification.
  - Autofill off. [PRAC Loomer]
- **Instant form vs website:** Loomer's tests do not show the assumed quality drop. If one destination is cheaper and the other better, he suggests Value Rules rather than dropping one. [PRAC]
- **Value Rules:** bid down placements with junk leads (e.g. Audience Network) and bid up priority countries. [PRAC]
- **Qualified-event case:** sending a separate "qualified" event, with disqualification by revenue and headcount, cut cost per qualified lead by 46% and grew qualified leads by 340% (Gushwork). [VENDOR, Flighted]

**Creative**
- Diversity means different concepts, personas and formats, not small tweaks.
  - Suggested volume: 8–20 concepts per ad set, refreshed every 2–3 weeks. These are vendor ranges; Meta publishes no number.
- **B2B formats:**
  - Founder or expert talking-head video (this fits the 60-day "talking head ads" goal).
  - Proof: logos and case results.
  - "Problem" statics that name the buyer.
  - Carousels. [PRAC]
- **Lead magnets:** interactive assessments and calculators beat gated PDFs (calculators 8.3%, assessments 6.2%, PDFs 3.8% conversion). [VENDOR Brixon] Gate only original research and tools; ungate the rest. [consensus, opinion]
- **Partnership (creator) ads:** Meta claims 19% lower CPA; an independent analysis of $130M of spend found about 5% better. No B2B data. [OFFICIAL/DATA]

**Funnel for long cycles**
- **Cold:** always-on thought-leadership video and opinion-leader content (the AI CoE videos).
- **Warm:** video viewers and site visitors get proof content and lead magnets.
- **Hot:** contact-page visitors and engaged leads get the "Talk to us / Join the Platform" offer. [PRAC Directive]
- **Retargeting:** frequency 1–2 a week, creative refreshed every 2–4 weeks, judged on cost per SQL. Retargeting often reaches people who already know the brand. [PRAC]
- **Lookalikes:** seed them from closed-won and ICP accounts, not from all leads. [PRAC]

---

## 4. Google Ads playbook for B2B

**Structure and keywords**
- Keep brand, non-brand and competitor terms separate. Competitor terms: split by intent (alternative, pricing) and start with one or two competitors. [PRAC]
- Promote search terms that keep converting into exact-match keywords. [PRAC Brad Geddes]
- **Standing negative lists for PnP** (my suggestion, from the ICP data):
  - Job seekers: jobs, careers, internship.
  - Startup-side intent: apply, accelerator application, funding for my startup, pitch.
  - Free / DIY.
  - Education.
- Location set to "Presence", not "Presence or interest". Search Partners and Display expansion off unless they have been proven to work. [PRAC]
- Auto-applied recommendations that add keywords or change bidding: switch them off. [PRAC]

**AI Max: how to use it safely**
- Run it as an experiment, not a switch-on.
- Set URL exclusions and brand controls first.
- Optimise only to qualified-lead or SQL conversions.
- Review search terms by "Source" and the landing pages report every week. [PRAC consensus]
- **Results data:**
  - Google claims +14% conversions at similar CPA. [OFFICIAL claim]
  - Independent tests found lead-gen accounts tended to underperform. [DATA, small]
  - One lead-gen case got a lower CPA but fewer real outcomes. [DATA]
  - Practitioner rule: use AI Max for lead gen only with CRM-qualified feedback and 30+ conversions a month. [PRAC SEL]

**Performance Max and Demand Gen**
- **Performance Max:** optimised to form fills, it finds the cheapest leads, including spam, via Display, Discover and lead forms. Hold it until offline SQL import works. Google advises allowing up to 6 weeks before big changes. [PRAC/OFFICIAL]
- **Demand Gen** is upper-funnel. At this budget, use it only for retargeting with Customer Match.

**Lead quality and measurement**
- **Enhanced conversions for leads** match on hashed email; add the GCLID where you have it.
- **Salesforce:** needs a custom GCLID field plus a Flow that copies it from Lead to Opportunity. [OFFICIAL/PRAC]
- **HubSpot "Google Ads optimization events"** send lifecycle-stage changes. They connect only to individual accounts, not manager accounts. [OFFICIAL]
- **Conversion goals:**
  - Primary: 1–2 actions, e.g. the ICP-qualified lead and an imported SQL.
  - Secondary: all form fills and content downloads.
  - Never put downloads in Primary alongside the contact form. [PRAC]
- **Values per stage:**
  - Separate conversion actions per stage, with values from close rate and margin.
  - Startup lead type at value 0. This is the single biggest lever on the 79% startup problem. [PRAC]
- **Spam controls:** reCAPTCHA, honeypot field, free-email block on the corporate form, conversion fired only after server-side validation.
- **Lead form assets:** use "More qualified" mode; practitioners report very high junk rates. Prefer landing pages for the corporate ICP. [PRAC]
- **Landing pages:**
  - Say who the offer is for. AI Max reads the page to choose queries and write ads.
  - Keep startup routes on separate URL paths so they can be excluded.
  - Add qualifying fields: organisation type, company size, role. [PRAC]

**Bidding at PnP's volume**
- Start with Maximize Conversions on the ICP-qualified proxy, using a portfolio strategy to pool thin campaigns.
- Move to Target CPA after 30+ conversions per 30 days.
- Use value-based bidding only once SQL imports are steady. [OFFICIAL/PRAC]

---

## 5. Measurement setup PnP needs (both channels)

1. **Define one "ICP-qualified lead" event** that can fire the same day: organisation type corporate or government, company size 10,000+, target role. HubSpot already has the `mql_fit_score_threshold` properties, which could be the base.
2. **Send it to the platforms:**
   - Meta via the HubSpot CAPI integration (website forms) and Conversion Leads (instant forms).
   - Google via HubSpot optimisation events or enhanced conversions for leads (Data Manager).
   - ChatGPT Ads via HubSpot (beta).
3. **Import SQL and opportunity from Salesforce for reporting and values.** Accept that won deals (about 245 days) fall outside the windows.
4. **Use one UTM taxonomy:** all lowercase, fixed source and medium values, a unique UTM per ad, campaign IDs stable. [PRAC]
5. **Add a mandatory "How did you hear about us?" field** in HubSpot and sync it to Salesforce.
6. **Incrementality:** at PnP's volume, a geo holdout (pausing one market) is more workable than platform lift studies. [opinion] Google's lift threshold is reportedly about $5k. [PPC Land]

---

## 6. Benchmarks (directional; none are EMEA B2B-specific)

| Metric | Figure | Source |
|---|---|---|
| Meta CPL, all industries (US) | $27.66 (+21% YoY) | LocaliQ/WordStream, Sep 2025 [DATA] |
| Meta CPL, B2B/SaaS lead forms | $30–65 | Prospeo 2026 [VENDOR] |
| Meta CPM, B2B services | about €8–15 | Junto via Abe Agency [VENDOR] |
| Google Search CPL, Business Services (US) | $93.69; CPC $5.87; conversion rate 4.85% | WordStream/LocaliQ 2026 [DATA, secondary] |
| Google Search, enterprise B2B (one agency's clients) | CPC $6.29; CTR 1.30%; conversion rate 0.31% | 42 Agency 2026 [DATA] |
| MQL→SQL median | about 13% | Salesforce State of Sales [DATA] |
| MQL→SQL by source | SEO 51%, email 46%, webinar 39%, LinkedIn 30%, PPC 26% | First Page Sage, Jun 2025 [DATA] |
| Cost per SQL (US SaaS) | Google $250–450, Meta $300–600, LinkedIn $350–800 | SaaS Hero, Jan 2026 [VENDOR] |
| Return on ad spend, closed-won | LinkedIn 121%, Google Search 67%, Meta 51% | Dreamdata, Mar 2026 [VENDOR/DATA] |
| B2B journey length | 272 days | Dreamdata 2026 [VENDOR/DATA] |
| Lead response time | average 42–47 hours; under 1% respond within 5 min | Workato 2022; RevenueHero 2025 [DATA] |

**PnP baselines to compare against:**
- EMEA H1 2026 MQL→SQL: 43 / 954 = **4.5%**, vs about 13% median.
- MQL→SQL time: **66 days**, vs a 15-day benchmark.
- **Cost per SQL: two figures, to reconcile with Tereza.**
  - Deck: $2.1k.
  - Meta + Google spend Jan–Jun 2026 from our spend sheet is €179.3k (Meta €118.5k at 1.16, Google €60.9k). Divided by 43 EMEA SQLs that is about €4.2k. This is a ceiling: not all SQLs came from paid, and part of the spend may target markets outside EMEA.

---

## 7. New angles to test at PnP (to confirm against the account audit)

1. **Talking-head and opinion-leader video on Meta** (AI CoE experts, local MDs) as always-on cold reach. This is already in the 60-day plan.
2. **Localised lead magnets per market:** a research report on corporate innovation per country (FR, UK, DE, ES, IT), gated; everything else ungated.
3. **An interactive tool**, such as an "innovation maturity assessment", instead of a PDF download.
4. **Split corporate and startup journeys:** separate landing pages, forms and events, so platforms can learn from the corporate leads alone.
5. **Instant forms with Higher Intent + lead filtering** for corporates, optimised to a Conversion Leads stage within 28 days.
6. **AI Max experiment** with URL exclusions, messaging restrictions and qualified-lead bidding. This is already in the 60-day plan.
7. **Competitor campaigns** (one or two corporate-innovation competitors), each with its own page.
8. **Webinars and events as SQL accelerators,** given webinar MQLs convert to SQL at 39% vs 26% for PPC.
9. **ChatGPT Ads 10-day BOFU test** in priority markets, tracked through HubSpot, with spend capped.
10. **LinkedIn test for company-list targeting** of the corporate ICP; Meta cannot target company lists. This is already in the 90-day plan.

**KPI risks to raise with Raul**
- **Meta CPL −20%** conflicts with lead-quality filtering, which raises raw CPL, and with the 2–3% location fees. Suggest agreeing on CPL **per qualified lead**.
- **Paid search MQLs +15%** depends on AI Max being back on, and on MQL meaning corporate MQLs rather than startup form fills.

---

## 8. Audit checklists (used for the account audit)

### Meta (28 checks)
1. Pixel and CAPI both active for key events; "Server" connection visible.
2. Browser and server events deduplicated (shared event_id); no manual pixel next to HubSpot's.
3. Event Match Quality at 6 or above as a minimum, aiming for 8 or above.
4. Domain verified; event priority configured.
5. fbclid/fbc captured on website form submissions.
6. Meta Lead ID stored in the CRM; leads synced within about 90 days.
7. CAPI for CRM sending 1–2 predictive stages at least daily.
8. Performance goal is Conversion Leads or a qualified event, not raw Leads.
9. Objective matches the goal; no Traffic or Engagement campaigns counted as lead gen.
10. Optimisation events at about 50 or more per ad set per week; "Learning Limited" status reviewed.
11. 1–3 ad sets per campaign; no overlapping interest splits.
12. Prospecting and retargeting in separate campaigns.
13. Hard controls correct: locations, languages, minimum age.
14. Custom-audience exclusions: customers, current leads, employees, startup and student leads.
15. Interests deprecated in Jan 2026 removed.
16. Instant form type is Higher Intent or Rich Content, not More Volume.
17. Qualifying questions, lead filtering, conditional logic, work-email and SMS verification.
18. Lead quality checked by placement (especially Audience Network).
19. Value Rules tested (countries, placements).
20. At least 8 conceptually distinct ads per ad set (video, static, carousel, proof).
21. Fatigue check: frequency trend, CTR down more than 20% over 14 days.
22. Advantage+ creative enhancements audited, plus the account-level "Test new optimizations" setting.
23. Creative and landing-page language match per market (FR, DE, ES, IT, UK).
24. No social-issue or political themes in the EU (TTPA).
25. Attribution settings updated after the Jan 2026 window removals.
26. Opportunity Score recommendations reviewed, not applied blindly.
27. Cost per SQL and pipeline per campaign reported from Salesforce.
28. Budget and pacing account for the Jul 2026 location fees.

### Google Ads (30 checks)
1. Primary conversions are only 1–2 high-intent actions; downloads and other forms are Secondary.
2. No double counting between GA4-imported goals and the Ads tag.
3. Enhanced conversions on; Diagnostics healthy.
4. CRM import live (HubSpot or Salesforce via Data Manager); recent uploads with no errors.
5. GCLID captured in a hidden field and carried from Lead to Opportunity.
6. Conversion windows match the sales cycle; a same-day proxy conversion exists.
7. Values per stage; startup leads at 0 or excluded.
8. Consent Mode v2 sending all four parameters on EEA traffic.
9. Brand, non-brand and competitor in separate campaigns with separate budgets.
10. Location set to "Presence"; target countries only.
11. Language and copy localised per market.
12. Match-type mix: exact and phrase core; broad only with quality signals.
13. Search terms reviewed weekly (n-grams, AI Max "Source" column).
14. Negative lists: jobs, startup intent, free/DIY, education; no conflicts with active keywords.
15. AI Max: URL exclusions, URL inclusions, landing pages report reviewed.
16. AI Max: brand controls and text guidelines (term exclusions, messaging restrictions) set.
17. AI Max tested via an experiment and judged on SQLs, not CPL.
18. Pinned assets not overridden by URL expansion.
19. Auto-applied recommendations reviewed; keyword, bidding and match-type ones off.
20. Bid strategy matches volume (30+ conversions per 30 days for Target CPA); no frequent target changes.
21. Portfolio strategies pool thin campaigns.
22. Impression share lost to budget and to rank reviewed.
23. Search Partners and Display expansion off unless proven.
24. PMax (if any): brand exclusions, negatives, channel report, placements, value-based goals.
25. RSAs: ad strength, asset labels, qualifying language, sitelinks to corporate pages.
26. Landing pages: separate corporate and government pages, qualifying fields, speed, clear next step.
27. Form spam controls: reCAPTCHA, honeypot, free-email block, server-side validation.
28. Lead form assets: "More qualified" mode, qualifying questions, CRM routing.
29. Reporting links cost to MQL, SQL, Opportunity and won, by campaign and by search term.
30. Change history reviewed for automated changes; check for the Sept 2026 auto-upgrade to AI Max.

---

## 9. Who to follow

- **PPC Land:** fastest coverage of Google, Meta and OpenAI platform changes.
- **Search Engine Land / Search Engine Roundtable:** reliable reporting on AI Mode and ChatGPT ad features.
- **Jon Loomer:** the deepest coverage of Meta targeting and optimisation changes.
- **Dreamdata benchmarks:** European-based, revenue-attributed B2B channel data.
- **Metadata benchmark report:** pipeline and acquisition cost by channel rather than CPL.
- **Refine Labs:** demand-gen thinking and self-reported attribution.
- **Exit Five (podcast):** senior B2B marketers on pipeline-led strategy.
- **The Loop (Cognism, podcast):** B2B demand gen from a European operator's view.
- **PPC Town Hall (Frederick Vallaeys):** practitioner sessions on Google automation.
- **Marketing O'Clock:** weekly PPC and SEO news roundup.

## 10. Key sources

**Meta**
- Andromeda: https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/
- Conversion Leads integration: https://developers.facebook.com/documentation/ads-commerce/conversions-api/conversion-leads-integration
- HubSpot × Meta CAPI: https://knowledge.hubspot.com/ads/create-and-sync-ad-conversion-events-with-your-meta-ads-accounts-using-metas-conversion-api
- Jon Loomer:
  - https://www.jonloomer.com/meta-ads-targeting-2026/
  - https://www.jonloomer.com/meta-andromeda/
  - https://www.jonloomer.com/11-new-meta-lead-ads-features/
- Location fees: https://www.emarketer.com/content/meta-passes-location-fees-onto-businesses-raising-ad-costs-across-europe
- TTPA political ads ban: https://ppc.land/meta-blocks-political-ads-in-eu-as-ttpa-regulation-takes-effect

**Google**
- AI Max overview: https://support.google.com/google-ads/answer/15910366
- AI Max URL controls: https://support.google.com/google-ads/answer/16230205
- AI Max text guidelines: https://support.google.com/google-ads/answer/16489313
- Search terms "Source" column: https://support.google.com/google-ads/answer/16470459
- Enhanced conversions for leads: https://support.google.com/google-ads/answer/14274408
- Data Manager API change: https://ppc.land/google-blocks-new-offline-conversion-imports-via-ads-api-from-june-15/
- Optmyzr match types: https://www.optmyzr.com/blog/google-ads-match-type-performance/
- Optmyzr bidding strategies: https://www.optmyzr.com/blog/impact-of-ppc-bidding-strategies/
- AI Max lead-gen test: https://searchengineland.com/googles-ai-max-for-search-30-days-testing-462568
- Qualified Future Conversions: https://www.searchenginejournal.com/googles-marvin-clarifies-ai-search-and-qualified-future-conversions/582185/

**Cross-channel**
- ChatGPT Ads in Europe: https://openai.com/index/chatgpt-ads-expands-across-europe/
- HubSpot × ChatGPT Ads: https://knowledge.hubspot.com/create-and-sync-ad-conversion-events-with-chatgpt
- Metadata benchmark: https://www.metadata.io/benchmark-report-2026
- Dreamdata: https://dreamdata.io/blog/linkedin-ads-benchmarks
- Refine Labs: https://www.refinelabs.com/blog/attribution-mirage
- Gushwork case: https://www.flighted.co/case-studies/340-qualified-lead-growth-while-cutting-cpql-by-46-for-gushwork
