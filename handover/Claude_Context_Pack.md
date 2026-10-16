# Claude context pack: Felipe Cárdenas · Performance Marketing & CRM · Plug and Play

**As of 16 Oct 2026.** This pack holds everything a new Claude chat needs to continue Felipe's work: how he works, who's who, the numbers, the decisions, the deliverables, the paid media strategy and what's still open.

It comes from the cloud session of 8–16 Oct 2026. The files are in the GitHub repo `felipecardenassa-sudo/pnp`, on the branch `claude/paid-ads-spend-audit-w9vbm5` (no pull request, not merged).

---

## 0. How to use this pack (for Felipe)
1. **Best option: a Claude Project.** Create one, for example "Plug and Play – Performance Marketing & CRM".
   - Paste `Claude_Project_Instructions.md` into the project instructions.
   - Upload this file and the files in section 20 as project knowledge.

   Every chat in the project then starts with all of it.
2. **Quick option: a single chat.** Upload this file plus the files the task needs, and start with: *"Read the context pack first. You're continuing my work at Plug and Play."*
3. **Keep it current.** When a decision or a number changes, ask Claude for the updated section and replace it here.

The new chat isn't connected to GitHub, so it can't run the repo's build scripts (`tools/…`). If file creation is turned on in Claude's settings, it can make files itself (PDF, DOCX, XLSX, PPTX) from data you upload, following the rules below.

---

## 1. How to work with Felipe (most important)
- **Fact-only, no fluff, no assumptions.** Fact-check every number before the final version. Felipe rejected commentary like "where the numbers come from, and how to check them yourself in HubSpot. Nothing needs to be saved." as fluff.
- **Simple, clear and visual, but not shallow.** Quote (13 Oct): "With lighter I also don't mean worse, or oversimplified, or not as detailed, I just need the UX better, easy for me to input info, not messy, clearer."
- **Managers.** Raúl and Tereza have both run paid media.
  - Never explain basics ("I don't want to explain what an ad is, they are not that dumb").
  - Show strategy and structure graphically.
  - No source notes on slides ("I don't like when you put those little letters saying, oh, this came from here").
- **Toddler mode.** When he says "explain it to me as a toddler", give a plain analogy plus the exact clicks or settings.
- **Ask first when asked to.** On 14 Oct he said "just tell me before adding anything to the slide because it makes it unclear for me still". Answer in chat, then change files only after he agrees.
- **Spreadsheets:**
  - Google Sheets only.
  - Plain formulas (SUM, IF, SUMIFS); no XLOOKUP and no macros.
  - Freeze header rows only (Sheets pushes charts below a frozen area).
  - Charts under the tables; plain column or line charts.
  - Conditional formatting can't reference another tab, so use a helper cell on the same tab.
  - Keep formulas in the low thousands.
  - Make them easy to update.
- **PDFs:** short and visual, structured as flagged · working · can be improved · next steps.
- **Presentations:**
  - Each channel's structure as a diagram with counts.
  - What's going well and what's going wrong.
  - Proposed structure as mock-up blocks (campaign → ad sets → creatives → landing page, no copy).
  - Before → after numbers.
  - Landing pages as annotated page images.
  - A 7/30/60/90-day test plan.
  - No charts unless asked.
  - Never mention the research playbook.
  - No HubSpot data in paid media decks.
  - Use CPL: ROAS can't be measured until deal values are tied to campaigns.
- **Scope:**
  - Meta, Google Search and ChatGPT Ads.
  - YouTube is a CEO vanity play for cheap views: leave it out of audits, decks and plans, but keep it in the weekly report.
  - LinkedIn is off for now (Raúl: too expensive; a test sits in the 90-day plan).
  - The audit deck covers Meta and Google Search only (no ChatGPT).
- **Brand.** Follow the Plug and Play Global Brand Guidelines (the 2021 "EXTERNAL" PDF).
  - Colours:
    - primary: Dark Blue #253B49 (titles, key numbers, chart marks);
    - body text: #313C51, never black;
    - secondary text: grey #676E7A;
    - backgrounds: #F5F5F7 and #FBFAFA (dark: #253B49);
    - yellow #F0E545 and purple #6C6CD0, sparingly;
    - charts: Dark Blue, then #4F81F3, #91AFF3 and the tints #E3E9F6 and #D3DEF4;
    - better/worse: green #1E862F and wine #9B3A59, always with an arrow or a label.
  - Fonts:
    - Protipo is primary but licensed, so internal and electronic documents use Trebuchet MS;
    - Bebas Neue is for the logo only;
    - no Inter or Arial;
    - PDFs embed only the brand font, so arrows and ticks are drawn as shapes.
  - Elements: white cards with 1/8-inch rounded corners and a soft shadow (14% opacity, no offset, 14pt blur) on light grey, plus a short yellow underline for emphasis.
  - Logo:
    - only the official wordmark, unaltered (Dark Blue on light backgrounds, white on Dark Blue);
    - at least 130 px wide, with clear space equal to the height of "and";
    - no location or vertical lockups.
  - Felipe chose no logo on the ICP report and the audit decks.
  - Write "Plug and Play" in full; never "PNP" as a name, and leave "PNP" out of new file names.
  - Files made before 14 Oct (spend PDF, newsletter audit, deck v1) aren't on brand yet. Restyle them when they're next rebuilt.
- **HubSpot is a read-only audit.** "We need to be careful… you cannot touch or mess up anything, this is purely an audit." Never create, edit, delete or send anything there.
- **GDPR** ("Let's stay under GDPR when delivering the report"):
  - Aggregates only, with counts of 1–4 shown as "<5".
  - Raw contact exports are deleted after use and never saved in deliverables.
  - Exception: the weekly paid performance report shows exact HubSpot counts. Felipe's rule (14 Oct): "just do as Tereza did i dont care, take that as a rule".
- **Language:** English. Felipe sometimes sends voice-note transcripts, so read for intent.

---

## 2. Role, company and people
- **Felipe Cárdenas**, Performance Marketing & CRM Associate at Plug and Play. He started on 5 Oct 2026; 8 Oct was his 4th day.
- **Plug and Play** is a global innovation platform connecting startups with large corporations and governments: accelerators, startup scouting, pilots and innovation programs. HQ is in Silicon Valley, and it has local offices worldwide.
- **Platforms:**
  - Meta Ads (ad account "Plug and Play Tech Center (Dollars)" 471277291299593, USD, Europe/Madrid);
  - Google Ads (customer 133-450-4766, EUR), mostly Search;
  - ChatGPT (OpenAI) Ads, billed in EUR;
  - LinkedIn Ads (no spend since Oct 2025);
  - HubSpot (portal 3340630, marketing CRM);
  - Salesforce (sales);
  - Playbook and Looker Studio (reporting);
  - Matomo; Google Tag Manager; Semrush (access pending).
- **Agency:** Toco Marketing (Thiago "Toco") runs paid media until **30 Oct 2026**, with a handover document due near the end of October. The agency kept a Notion "PNP" page (see section 14).

| Person | Role | Go to them for |
| --- | --- | --- |
| Raúl (Raul) | **Felipe's manager** | 30/60/90 plan, paid sync, email marketing structure, HubSpot onboarding, ICP, Salesforce access |
| Tereza Pigova | Growth Marketing Director (Raúl's manager) | Performance, lead generation, revenue projects; Meta Ads access goes through her; made the weekly paid report until 5–11 Oct |
| Allison Romero | Marketing Director | Content, design, organic channels; newsletter ownership (with Raúl) |
| Thiago (Toco) | Agency, runs paid media until 30 Oct | Handover doc, Google and Meta tests, year-end pacing, Notion, naming conventions |
| Amanda | Brand | Brand guidelines, review of running ads, talking-head video |
| Natalia | Content (to confirm) | Content onboarding |
| Anto (Anto Guarin in HubSpot) | Content (to confirm) | Paid content with the external vendor, asset management, newsletter workflows, creative pipeline; co-creates the Global Newsletter |
| Rosa | Email and landing pages (to confirm) | New email modules, landing page optimisations, page designs and edits |
| Aly | Landing pages (to confirm) | Landing page onboarding |
| Andrew | Key player (to confirm) | Newsletter subscription project |
| Juki | Newsletters (to confirm) | Newsletter requirements |
| Sara | Event emails (to confirm) | Event emails audit, newsletter training for new hires |
| Alex | Sales enablement (joined Aug 2026) | Marketing–sales processes, SLAs, disqualification reasons |
| Andrea & Ale | Leadhub team (inbound lead triage in Salesforce) | Top-of-funnel experiments, inbound queues |
| Saku | Analytics | Playbook / Looker training, custom dashboards |
| Leticia | External MarTech contractor | Looker dashboards |
| Sanam | Leadership | Wants the full funnel report: visitors → MQL → SQL → opportunity → closed won |
| Sina | Head of EMEA (Barcelona); all MDs report to Sina | EMEA vs Americas parity in spend and ROI |
| Cami | Works with Amanda on the talking-head video | Talking-head video review (meeting planned w/c 19 Oct) |

The name spellings come from automatic transcripts and Felipe's notes.

---

## 3. 30/60/90-day plan (set by Raúl), KPIs and tools
- **KPIs by end of 2026:**
  - Meta CPL −20%;
  - MQLs from paid search +15%;
  - MQLs converted with last source Email Marketing +25%.
- **First 30 days: learn Plug and Play, its audience and the paid channel.**
  - Brand: meet Amanda; brand guidelines; flag issues in the ads now running.
  - ICP: meeting with Raúl; ICP vs conversions breakdown (done).
  - Content: meet Natalia; review paid content; meet Anto.
  - Email marketing: meet Raúl about structure; meet Rosa about new modules; audit the vertical newsletters.
  - Paid: sync with Raúl; sync with Toco (done 8 Oct); audit the 2026 paid accounts (done, deck v3); real spend breakdown per location; keyword positioning (product based).
  - Landing pages: meet Aly; meet Rosa.
  - HubSpot: meet Raúl; map lifecycle stages and qualifying milestones.
  - ChatGPT Ads: 10-day BOFU test for Startup Scouting (a first campaign already ran).
  - First talking-head video (sync with Amanda).
  - Join the monthly EMEA priority-market calls.
  - Meet Andrew and Alex.
- **60 days: total ownership of the channels.**
  - Take over the weekly paid performance report by week 3.
  - Take over the vertical newsletters.
  - Audit the location newsletters and the LNS (lead nurture system).
  - Audit the nurture and reactivation workflows.
  - Take over the newsletter subscription project (Andrew).
  - Manage all paid platforms.
  - Launch talking-head ads.
  - Run an AI Max / PMax test.
  - Optimise Google keywords.
  - Benchmark competitors (paid and email).
  - Paid plan 2027 for YouTube and LinkedIn.
  - GEO training.
  - First monthly leadership summary: what worked, what didn't, what's next.
- **90 days: 2027 planning, cleanup and compliance.**
  - Audit event emails (Sara).
  - Test LinkedIn.
  - Clean up subscription types and database compliance.
  - Launch the LNS revamp.
  - Paid Plan 2027 (Google, Meta, ChatGPT, YouTube, LinkedIn).
  - 2026 funnel attribution report.
  - Email marketing plan 2027.
- **Tools access:**
  - OK: Google Ads, GTM, HubSpot, Matomo, OpenAI Ads.
  - Meta Ads: through Tereza.
  - Pending: LinkedIn (account restore), Salesforce, Semrush.

---

## 4. ICP and funnel numbers
- **ICP (Buyer Persona 2024):**
  - Primary: corporates with 10,000+ employees and $100M+ revenue (Head of Innovation, R&D, CDO or C-level), plus governments. A $500M threshold is under discussion.
  - Secondary: startup founders.
- **Measuring conversion:** use Lead Status (Salesforce), deals and customers. Not lifecycle stage: 95% of JTP contacts are "SQL" in HubSpot.
- **Agency avatars:**
  - Innovation Leader (Head of Innovation / R&D / CDO);
  - C-level (CEO / COO / CFO / President);
  - Government Innovation Leader.
- **Key numbers from Tereza's deck (EMEA H1 2026):**

  | Metric | EMEA | Global | Note (as in Tereza's deck) |
  | --- | --- | --- | --- |
  | MQLs | 954 | 2k | −28% |
  | SQLs | 43 | 118 | +150% |
  | Closed won | 1 | 3 | −50% |
  | Cost per SQL | $2.1k | industry $2.5k | 20% better than industry |

  - MQLs split 48% JTP Contact us and 52% content downloads ("WLs").
  - MQL → SQL takes 66 days (benchmark 15); the full cycle is 245 days.
  - Auto-disqualification breach rate is 15% (target 0).
  - 28 open opportunities are worth $5.5M; 35% have no deal amount.
  - Spain Grid Report: 991 leads at $8.86 each.
  - **Local content beats generic content 3:1 on cost per lead.**
  - Key markets: France, UK, Germany, Spain, Italy.
  - Leadership responds best to logos and $1M deals.

---

## 5. Budget 2026 and spend status
- **Budget (Tereza, 13 Oct):** $300k for 2026, in USD ("we usually talk in USD").
  - It was originally $350k and was cut because performance wasn't good enough ("we just didn't want Thiago to blow the budget").
  - Maximum $320k, "ideally not more".
  - The "90k Google / 180k Meta" figures were spend so far, not budgets. The first EUR-based €270k assumption (8 Oct) was wrong.
- **FX:** 1 EUR = 1.1177 USD (live rate on 13 Oct, from Felipe). Finance's monthly rates can replace it.
- **Status, platform exports to 12 Oct 2026** (from the spend tracker):
  - **Spent:** $282,523.69, which is 94% of $300k while 78% of the year has gone.
    - Meta $180,767 (64%), Google Ads $101,500 (36%), ChatGPT Ads $257.
    - By region: EMEA $141,049 (50%), Americas $127,616 (45%), Global $13,602 (5%).
    - Meta prospecting lead ads plus Google Search non-brand are 84% of all spend.
  - **Plan:** $300k spread evenly is $5,753 a week, so an even pace would be $234,247 by 12 Oct. We are $48,277 ahead of it.
    - Q1 ran +$33,496 over plan and Q2 +$23,169.
    - Every month since August has been under plan (September: $18,174, which is $6,484 under).
  - **Current pace:** $1,860.75 a week (last 3 full weeks, 21 Sep – 11 Oct, leaving out ended campaigns).
  - **Forecast at 31 Dec:** $303,789.43, about $3.8k over budget and $16.2k under the maximum (11.4 weeks left).
  - **To land on $300k:** about $1,529 a week (18% less). The $320k maximum allows about $3,279 a week.
  - **Last full week, 5–11 Oct:** $1,887 (Meta $1,174, Google Ads $713).
- **Budget cuts:** Meta went from $310 to $160 a day from 18 Sep. Google was cut on 19 and 21 Sep: NA €135 → €50 → €33 and EMEA €104 → €43 → €30.
- **FR_Alibaba:** a Meta traffic campaign run by Plug and Play's internal team. It spent $4,491 from 10 Sep to 5 Oct, and the agency left it out of its reports from 7 Sep.
  - It counts in "spent so far" but is left out of the pace because it ended.
  - Whether it counts toward the $300k is an **open question for Tereza**.
- **ChatGPT Ads:** the test (23 Sep – 2 Oct) cost €229.56 ($256.58). Whether it counts toward the $300k is open too.
- **Agency reports vs platforms**, checked week by week:
  - Meta matched within $5 in 31 of 33 weeks.
  - Google matched in only 11 of 32: 10 weeks converted to dollars at about 1.15, 3 exactly doubled (6 Apr, 11 May, 25 May) and 8 lower. The July report used £1 = $1.28 on a euro account.
  - H1: agency $182,516 vs platforms $205,432.
  - **The platform exports are the source of truth.**
- About 45% of 2026 spend went to Americas campaigns. Open question: does the $300k cover all territories?

---

## 6. Paid media today: audit findings (1 Jan – 13 Oct 2026)
These come from a read-only Claude-in-Chrome audit on 14 Oct (`reports/audit/paid_media_audit_2026-10-14.md`). Its figures match the platform exports. "Last 30 days" means 14 Sep – 13 Oct.

**Tracking outage:** Meta and Google recorded almost no results from 15 Jul to 10 Aug. Judge campaigns started in June or July on the last 30 days.

### 6.1 Meta
- **Account:**
  - 83 campaigns, 272 ad sets and 1,785 ads in total.
  - **Live: 9 campaigns, 30 ad sets and 243 ads on about $160 a day** ($154.68 on 8 lead campaigns plus $5.16 on a traffic ad set).
  - 7 location campaigns (US-California, US East Coast, US & Canada, US Middle-South, EMEA, Middle East, Western Europe) each repeat the same 5 topic ad sets: AI, Brand, Deep Tech, Health, and Innovation Leader (off everywhere).
  - That gives $10–$26 a day per campaign and **about $4 a day per ad set**.
- **Optimisation event:** "welcome_conversions", a custom conversion on the welcome_conversion event where the URL contains "welcome". It's used by 29 ad sets.
  - Student and job-seeker answers count as leads.
  - Meta's "Connect your CRM" isn't connected.
  - Results are form fills, not qualified leads.
- **Audience setup:** Advantage+ audience is on, so the job titles and interests were **only suggestions**.
  - Value rules are off.
  - "Custom audience terms not accepted", so the HubSpot list exclusions may not apply.
  - The Brand USCA ad set has no exclusion.
  - Newer ad sets exclude "welcome-l180days".
- **UTMs:** every ad uses `utm_source=facebook&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}`.
- **Last 30 days by region:**

  | Region | Spend | Leads | CPL |
  | --- | --- | --- | --- |
  | Europe & Middle East (EMEA, Middle East, Western Europe) | $1,394 | 188 | **$7.42** |
  | US (East Coast, California, Middle-South, US & Canada) | $2,480 | 187 | $13.26 |
  | Worldwide retargeting | $1,405 | 108 registrations | $13.01 |

  - That works out to about 4 leads per ad set a week; Meta needs about 50 to learn.
  - FR_Alibaba took 41% of the last 30 days' spend ($3,845 of $9,306) buying $0.03 clicks in Turkey and Eastern Europe.
- **Split vs grouped (same region, Feb–Jul):**
  - **Split:** "EMEA/lead/prospecting/abo/20260210", one job-title ad set per country.
    - $71,634 spent, 2,166 leads, **$33.07 per lead**.
    - Country ad sets: UK $23.00, France $36.50, Italy $35.01, Saudi Arabia $32.07.
    - 7 US-state ad sets inside this "EMEA" campaign took $28,879 (40%): New Jersey $5,097, New York $4,627, Texas $4,539, Florida $4,276, Washington DC $3,581, Indiana $3,523, Arizona $3,236.
    - Without the US states, the UK/France/Italy/Saudi ad sets still cost **$30.20** per lead.
  - **Grouped:** "EMEA/lead/prospecting-test/cbo/20251010" (Jan–Jul), 19 countries together, one ad set per report topic.
    - $18,001 spent, 1,437 leads, **$12.53 per lead**.
    - Ad sets: Decarbonisation $8.14, Spain energy grid $8.76, Quantum $10.47, AI & robotics $11.07, "Job titles only" (Innovation Leader) $50.09.
  - Grouped was **2.6× cheaper** (2.4× like for like).
- **Local creatives (Felipe, 14 Oct):** the split was meant to make the ads local, since Plug and Play has offices worldwide and Raúl wants well-targeted, local-language ads. In practice the **country ad sets ran the same English ads to the same English pages**:
  - Quantum video (PP-50b): grouped $7.47, UK $20.38, France $36.22 per lead.
  - Spain grid ad (English; 0 Spanish-language ads exist): grouped $7.67, UK $18.02, Italy $29.08.
  - So the same English ad cost **2.4–4.8× more per lead** in a country ad set.
  - Ad Library: about 280 live ads, about 240 of them in English. French, Italian, German, Arabic and Portuguese together: about 3. Spanish: 0.
  - Report landing pages are English.
- **Best ads this year (cost per lead):**
  - Quantum report static $6.86 (126 leads);
  - Quantum short video $7.47 (188);
  - AI trend report $7.48 (56);
  - Spain grid carousel PP-67 $7.67 (207);
  - AI & robotics product video PP-257 in EMEA $4.10 (73);
  - press quote "Fast-Track Corporate Innovation" PP-328 in retargeting $15.66 (165).
- **By format, Q1 2026 (agency review):** static $12.91, carousel $13.77, short video $20.54. A video showing the product cost $9.23 vs $20.79 for a person talking.
- **Losing ads:**
  - Event and case-study videos and ebooks in narrow ad sets cost $129–$190 per lead.
  - Brand in California: $139.57 for 1 lead.
  - Health ad sets in the US: $36–$51 per lead.
  - Innovation Leader job titles: $50.09 per lead.
  - The healthcare voice-memo video PP-266 runs as 6 copies: $173.57 for 3 leads, with 5 copies still active.
  - The 2025 report ad PP-102b got 0 leads after $373 and is still on.
  - The quantum video PP-50b runs as 12+ separate copies, which splits the learning.
- **Retargeting:**
  - The audience is under 1,000 people, with frequency 5.75.
  - The past-converter audience is only a suggestion.
  - It runs 53 ads to the innovation platform page.
- **Pixel hygiene:**
  - A staging domain (pnptc-master.herokuapp.com) sends pixel data.
  - Event match quality is 6.1–6.6.
- **Location fees from 1 Jul 2026:** UK 2%; France, Italy and Spain 3%. This works against the "Meta CPL −20%" KPI.

### 6.2 Google Search
- **Account:** "Plug and Play" 133-450-4766, EUR. Search + PMax spend this year was about €80k ($89.5k); all Google Ads, including video, was about €90.9k.
- **Live: 3 campaigns, 9 ad groups, 9 ads:**
  - **NA 20260813:** €30 a day, Maximise conversions, AI Max on, all broad match.
  - **EMEA 20260813:** €33 a day, tCPA €45 from 10 Oct, AI Max search-term matching.
  - **US-SV coworking:** €5 a day.
  - Each regional campaign has the same 4 ad groups: Branding, Startup Collaboration, Innovation, AI & Innovation Strategy.
  - Total: €68 a day, about $76.
- **Since 10 Aug, NA + EMEA (€9,623 together):**
  - Brand ad groups took **37%** and startup-side ad groups **42%**; Innovation took 14% and AI strategy 7%.
  - Landing pages: **homepage 60%** (the welcome root redirects to the homepage, which has no lead form; €5,811), innovation platform page 28%, supply-chain page 3%.
- **Per US state or area (Jan–May) vs per region (Aug–Oct), cost per conversion:**
  - New York €550 ($614), US East Coast €327 ($366), Florida €288 ($322), Texas €280 ($313), Arizona €254 ($284), New Jersey €249 ($279).
  - vs NA €44.23 ($49) and EMEA €41.36 ($46).
- **What works:**
  - Corporate searches with a matching page: the NA Innovation ad group sends supply-chain searches to the supply-chain page, converting **24% of clicks at €11.51** ($12.86).
  - Corporate ad copy: "Top Corporate Accelerator | Corporate Innovation Lab" converted 9–10% of clicks at €29.84–€35.87, half the cost of the generic ad.
  - Best markets: Saudi Arabia €32.26, Qatar €44.35, France €52.75, UK €54.02 per conversion.
- **What doesn't:**
  - The homepage gets the traffic.
  - Brand sits inside non-brand campaigns that are limited by budget (lost impression share to budget, last 30 days: NA 27.8%, EMEA 53.8%).
  - The startup side: a "Venture Capitalist" headline, coworking structured snippets added on 10 Oct, and "startup india certificate".
  - Broad match plus AI Max pick the searches.
  - Budgets were cut 71–76% in three days.
  - The business name, logo and 14 of 18 images are disapproved.
  - PMax was paused in the week of 7 Sep.
  - AI Max was paused for URL expansion issues; Toco is building a landing-page whitelist. The research shows **AI Max has no strict whitelist mode**: use URL exclusions or turn URL expansion off.
- **Last 30 days:** NA €1,768, 28 conversions, €63.14. EMEA €1,440, 28 conversions, €51.42. US-SV €144, 10 conversions, €14.36.
- **Cost per HubSpot lead** (Google's attribution): NA €262.83, EMEA €396.97, NA PMax €122.32, IT €181.27, EMEA PMax quiz €62.76.

### 6.3 ChatGPT Ads (in strategy scope, not in the audit deck)
- **Test 1, 23 Sep – 2 Oct:**
  - US only, €25 a day, conversions objective.
  - 4,021 impressions, 43 clicks, **0 conversions**, €229.56; CTR 1.07%, CPC €5.34.
  - All ads went to the homepage (no form), with no UTMs.
  - Text customisation was on, so copy is auto-rewritten.
  - Pixel email coverage is 1.8%, with no Conversions API.
  - A second campaign is a draft.
- **Proposed Test 2 (deck v2):**
  - Startup Scouting, US + Europe.
  - Send clicks to a form page.
  - Add tracking parameters and server events; turn text customisation off.
- This matches the 30-day plan item: a 10-day BOFU test for Startup Scouting.
- ChatGPT Ads has been live in 31 European markets since 24 Aug 2026 (the UK since June). HubSpot can sync conversion events to it (beta).

### 6.4 Landing pages (desktop 1,054 px, phone 390 px)
- **Report template** (most Meta report pages):
  - The form sits next to the headline (191–199 px down).
  - 10 required fields plus reCAPTCHA. It asks company size (10,001+ is an option) and job level.
  - **The profile dropdown includes "student" and "looking for job opportunities", and those downloads count as Meta conversions.**
  - On phone the form is 493–675 px down.
  - Several pages have no H1.
  - Case studies (Mitsubishi × Kamet, Aeroporti di Roma) are gated.
- **/ultimate-innovation-platform** (Google and retargeting):
  - One message for corporates, startups, governments and VCs.
  - Stats: 550+ partners, 60+ locations, 100K+ startups, 35+ unicorns.
  - The form is at 777 px, just below the first screen; **on phone it's at 1,542 px (about 2 screens down)**.
  - The form opens with a profile dropdown. The corporate path has 12 fields (11 required), **no company size**, and "location" is a 187-country list.
- **Homepage:** no lead form, only a newsletter sign-up at the bottom of an 8,769 px page; 156 links; on phone two chat widgets cover the headline.
- **Proof numbers disagree:** 30+, 35+ or 40+ unicorns; 50,000+ or 100,000+ startups.
- **Proposed corporate landing page:**
  - No main menu (startups get their own page).
  - A short form at the top with 6 fields: name, work email, company, company size, role, country. No student or job-seeker option.
  - Proof next to the form (logos plus one result in numbers).
  - Three offers: startup scouting, pilots, innovation programs.
  - An open case study, and the form again at the end.
  - On phone, the form sits within the first screen.
  - Vs the innovation platform page: fields 12 → 6; company size asked no → yes; student option yes → no; phone form "2 screens down" → "first screen".

---

## 7. The audit deck: `Paid_Media_Audit_2026.pdf` (v3, 15 slides, 16:9, on brand, no logo)
It's for Raúl and Tereza and covers Meta and Google Search only.

1. **Cover:** Meta $180,940, "Google Search" $89,478, 1 Jan – 13 Oct 2026.
   - **Fix at the next rebuild:** the Google figure (€80,055.62) includes PMax (€4,878.59). Search alone is €75,177.03 ($84,025). Either relabel it "Google Search + PMax" or use the Search-only figure. Ask Felipe first.
2. **Short version:** what's working, what's not working and what we change, with a before → after strip:
   - Meta campaigns 9 → 3;
   - ad sets 30 → 5;
   - leads per ad set a week ≈4 → ≈29–52;
   - Google clicks to the homepage 60% → 0%;
   - own-name spend mixed into non-brand 37% → 0%.
3. **Andromeda:** "Meta changed how it picks who sees our ads. Our set-up didn't."
   - Andromeda is Meta's ad retrieval system since Dec 2024. It reads the creative itself to decide who sees it; audience settings are only suggestions.
   - Many small ad sets on small budgets never leave the learning phase.
4. **Our own data:** grouping beats splitting, 2.6× cheaper per lead (numbers in 6.1).
5. **Local creatives:** "Going local is right. The country split didn't make our ads local."
   - Local the Andromeda way:
     - one broad ad set per region;
     - each ad carries French, German, Italian and Spanish versions, and Meta shows each person their language (English for everyone else);
     - local topic and proof;
     - a page in the ad's language.
   - A market gets its own ad set only when its budget buys about 50 leads a week (about $53 a day at Europe's cost per lead).
6. **What's working on Meta:** three campaign cards, each with structure, spend, who we targeted, why it works and how to improve it.
   - Broad Europe & Middle East: $7.42 per lead.
   - Report-topic ad sets: $12.53.
   - Retargeting: $13.01. Improve with $20 a day and 4–6 ads refreshed every 2–4 weeks.
7. **Not working → replacement:**
   - US split into 4 campaigns and 16 ad sets → one US & Canada ad set.
   - Brand and Health ad sets → proof and health as creatives.
   - Job-title ad sets → the ad names the buyer.
   - Traffic campaigns → lead campaigns only.
   - Ads that don't deliver → a weekly rule: after $50 spent, pause any ad 20% above the average cost per lead.
8. **Creatives:**
   - Best ads, and format results from Q1.
   - Stop: $129–$190 per-lead content, and the 12+ copies of one video.
   - What we make next, with 8–15 concepts per ad set:
     - data-hook static ×3;
     - report carousel ×2;
     - product explainer ×2;
     - case result or logos ×2;
     - talking head (test);
     - a French, German, Italian and Spanish version of each.
   - Each concept speaks to one persona: innovation & R&D leaders, C-level, digital leaders (CDO), governments.
   - New ideas start in the test campaign (2–5 ads, 7 days). New concepts every 2–3 weeks.
9. **New Meta structure** (mock-up blocks):
   - **Prospecting CBO, $110 a day:** two broad ad sets, Europe & Middle East (≈$55) and US & Canada (≈$55).
   - **Retargeting, $20 a day:** visitors and past leads, last 180 days.
   - **Creative test ABO, $30 a day (20%):** 2 test ad sets at $15 each; winners move to Prospecting after 7 days.
   - Same $160 a day in total.
   - Goal: a lead form sent, with student and job-seeker answers left out (corporate and government only once there's volume).
   - Every ad set: location, language, age 25+, exclusions, ICP job titles as suggestions.
10. **How broad still gets us our ICP:** five controls, today → new:
    1. Who can see the ad: hard limits and exclusions that work.
    2. Where Meta looks first: ICP job titles plus a lookalike of corporate leads as suggestions.
    3. What the ad says: every ad names the buyer.
    4. What counts as a result: students and job seekers stop counting now; later corporate and government only, then CRM-qualified leads.
    5. How we judge each ad: the share of each ad's leads that fit the ICP, weekly.

    Bottom line: "Meta can't target company size or a list of companies. It finds more people like the ones who trigger the result, so what we count as a result is our sharpest targeting."
11. **Google Search findings:** per state vs per region; today's structure with spend shares; working vs not working (numbers in 6.2).
12. **New Google structure:**
    - **Step 1: Semrush keyword research** for the US, UK, France, Germany, Spain and Italy, plus competitor terms and negatives.
    - **Brand** campaign (all markets, capped, exact and phrase) → corporate page.
    - **Corporate · US & Canada** and **Corporate · Europe & Middle East** (phrase and exact). Ad groups: Corporate innovation, Startup scouting, Open innovation & pilots, Industry (supply chain, health, energy). 2 ads each, landing on a matching page with a form.
    - Rules:
      - standing negatives: jobs, careers, apply, funding for my startup, pitch, grants, education, free;
      - location set to "presence";
      - goal: the corporate form (downloads count as secondary);
      - AI Max later, as a test.
    - Before → after: brand inside non-brand 37% → 0%; startup-side ad groups 42% → 0%; homepage clicks 60% → 0%; broad-match keywords all → none.
    - Same total, about $76 a day.
13. **Landing pages today:** 3 annotated wireframes (report page, innovation platform page, homepage).
14. **Proposed corporate landing page:** wireframe, phone view, and the before → after table.
15. **90-day plan:**
    - **Days 1–7, build:**
      - new Meta structure; pause old campaigns, traffic and losing ads;
      - students and job seekers stop counting as results;
      - Google brand campaign apart, negatives, no startup or coworking extras, no homepage traffic;
      - Semrush research;
      - paid forms: drop the student and job-seeker options and add company size.
    - **Days 8–30, learn:**
      - no Meta changes for 7 days, then budget moves of 20% at most;
      - French, German, Italian and Spanish versions of the best 3–4 ads;
      - Test 1: the same report as static, carousel and video;
      - corporate ad groups plus a weekly search-term review;
      - build the corporate page;
      - weekly ICP share of each ad's leads.
    - **Days 31–60, test:**
      - Test 2: talking head vs proof;
      - Test 3: local topic and proof vs global;
      - local-language report page;
      - an AI Max test once there are 30+ qualified conversions a month;
      - send qualified leads from the CRM to Meta and Google.
    - **Days 61–90, scale:**
      - scale winners in 20% steps;
      - bid on qualified leads;
      - an interactive assessment instead of a PDF;
      - the 2027 plan.
    - **To start, we need:**
      1. a yes to the structures (same budget);
      2. a US budget decision: the US ad set needs about **$95 a day** to learn (Europe about $53), but the plan gives it $55;
      3. web team time in weeks 2–4;
      4. local teams to write or check the French, German, Italian and Spanish versions.
- **Earlier versions:**
  - v2 (9 slides, with ChatGPT) and v1 (`PNP_Paid_Media_Audit_Strategy_2026.pdf`, 17 slides, style rejected) are superseded.
  - The landing pages are wireframes, because the site was blocked in the cloud. They can be swapped for real screenshots.

---

## 8. Getting the ICP with broad targeting: what we agreed with landing pages first
Felipe's concern, and Raúl's: with broad ad sets and the creative doing the targeting, how do we still reach the ICP and make Meta optimise for the right lead?

**The idea:** Meta finds more people like the ones who trigger the result it optimises for. Today that result is any form sent, so Meta finds form-fillers. The fix is to read the landing-page form answers at submit and only reward Meta for good leads. That's the top recommendation in the research.

Felipe decided (14 Oct): **landing pages stay the main route.** Instant forms are only a performance test.

**The setup, in plain terms:**
1. **Build the new results once, in Google Tag Manager** (Felipe has GTM access). Add a rule on the landing pages: when the HubSpot form is sent, read the answers and send Meta an event (browser pixel plus a server-side copy through the Conversions API).
   - **"Qualified lead"** = any form **except** student, job-seeker and startup answers. That's about 7 in 10 forms, going by the content-download mix, so there's enough volume to learn.
   - **"ICP lead"** = a corporate with 10,000+ employees, **or** government. That's about 1 in 10 forms.
   - Then create a custom conversion for each in Events Manager, the same way "welcome_conversions" exists today.
   - Correction to a chat simplification on 14 Oct: "Qualified lead" is **not** "corporate or government only". That definition is too narrow for Meta to learn at today's budget.
2. **Ads Manager, at the ad set level of Prospecting:**
   - **Conversion event:** "Qualified lead" instead of "welcome_conversions". Leads objective, website, same performance goal.
   - **Audience:** Advantage+ audience with hard controls:
     - countries, languages, minimum age 25;
     - exclusions: customers, current leads, students and job seekers.
   - **Suggestions:** Raúl's ICP job titles, plus a lookalike of corporate leads.
   - **Value rules:** bid more for France, the UK, Germany, Spain and Italy, and less for Audience Network (or remove it from placements).
   - **Ads:** each says who it's for, for example "For innovation leaders at companies with 10,000+ employees".
3. **Every Monday:** in Customise columns, add "ICP lead" and "cost per ICP lead". Keep the ads that bring ICP leads and turn off those that don't.
4. **Tests,** judged on one number, cost per ICP lead:
   - **Test A:** the test campaign optimises for "ICP lead".
   - **Test B:** instant forms with Meta's **conversion-leads** goal.
     - Higher Intent form with qualifying questions: work email, company, company size, role, profile.
     - HubSpot marks "ICP fit" the same day from the answers (not lifecycle stage) and sends it back through the Conversions API for CRM.
     - Meta's requirements: instant-form leads, at least 200 leads a month (Meta gets about 480 a month today on website forms), the stage reached within 28 days (ours is same day), 1–40% of leads reaching it (corporates with 10,000+ are about 5.5% of paid social leads), events for at least 60% of leads, and daily uploads.
     - Meta estimates the setup takes 3–4 weeks and pays off after about a month.
     - Meta's own suggestion in the account reads: "You could get 14–24% lower cost per lead by choosing website and instant forms" (both destinations together).
5. **Why not optimise for "ICP lead" straight away:** Meta needs about 50 results per ad set a week, and ICP leads come in at under 10 a week at today's budget.
6. **Structural catch:** at $110 a day, "Qualified lead" gives about 60 results a week across prospecting, so about 30 per ad set with two ad sets. The fix is either **one prospecting ad set** (the language versions cover the regions, and value rules can protect the US) or more budget. Decide this together with the US budget question.

**To confirm:**
- In Ads Manager: is the ad-level "Languages" option available on our lead ads with a website form, and can each language have its own URL and video?
- Does HubSpot save the ad name from the UTM (utm_content) on each contact?
- Someone with admin rights accepts Meta's custom-audience terms.
- Who builds the GTM rule and the server-side copy?

**Not yet in the deck:** slide 10, the structure slide and the plan don't yet show the two events, the one-ad-set option or the two tests. Felipe asked to be told before slides change, so **ask before updating**.

**Context (chat only; HubSpot data stays out of paid decks):** paid social brought 8,214 content contacts in 12 months. Only 449 (5.5%) were corporates with 10,000+ employees (about 9 a week), and fewer than 5 got a deal. The "precise" setup did not deliver the ICP.

---

## 9. Weekly paid performance report (Felipe's weekly task)
- **From the week of 12–18 Oct 2026**, every week from Monday 19 Oct. Tereza made it until 5–11 Oct (Word, 7 pages).
- **Felipe's rule:** keep ALL of Tereza's content. Make it clearer, more visual and easier to read, never shorter. When in doubt, do what Tereza's report did. It shows exact HubSpot counts.
- **Layout** (A4, on brand, about 5 pages; page 1 stands alone):
  1. **Summary:**
     - tiles: paid spend in USD (all channels incl. YouTube), leads (Meta + Google), cost per lead, MQLs with the paid share, organic clicks (Search Console), budget 2026, each with arrows and 8-week lines;
     - cards: What improved · What declined · Changed significantly;
     - the Top 5 focus list.
  2. **KPI breakdown,** one table per channel (this week · last week · change · 4-week average · note):
     - Google Search: spend, impressions, clicks, CTR, CPC, conversions, CPA, conversion rate;
     - Meta account totals: spend, impressions, reach, link clicks, landing page views, CPM, frequency;
     - Meta lead campaigns, the "lead engine": spend, leads, CPL, impressions, CPM, link clicks, link CTR;
     - YouTube: spend, impressions, clicks, CTR, views, view rate, cost per view, CPV by region, conversions;
     - a biggest-movers strip, and a budget block (spent, pace, forecast).
  3. **Paid, channel by channel:**
     - Meta lead campaigns, best ad, retargeting, weak spots, red flags;
     - Google campaigns and ad groups, brand terms, NA vs EMEA, off-topic search terms, PMax status;
     - YouTube campaigns, including weeks in a row with zero conversions.
  4. **Organic:**
     - Search Console: clicks, impressions, CTR, position on desktop and mobile, devices, countries, top pages, brand queries;
     - Semrush: tracked keywords ranking, median position, top 3 and top 10, AI Overview citations, gainers and losers, page-level traffic.
  5. **Leads, actions, sources:**
     - lead quality: MQLs by original source (this week, last week restated, change, disqualified, share), Watchleads, paid contribution, cost per paid MQL, SQLs when available;
     - recommendations by channel (quick wins and strategic);
     - accountability: next week's priorities with owner and day, experiments, monitor list, last week's actions with status;
     - data sources and reconciliation.
- **Rules:**
  - Totals in USD; Google and YouTube tables also in EUR.
  - Compare with last week **and** the 4-week average.
  - Call small numbers small (under 10 leads is low volume).
  - Leads are platform counts; MQLs come from HubSpot. Never mix them.
  - The point first, positives before problems, one idea per bullet with its number and the action.
- **Data Felipe sends each week:**
  1. Meta campaign × day export, 1 Jan – yesterday (the same as for the tracker).
  2. Meta ad-level data for the week and the week before, plus the account totals (reach, frequency, CPM, link clicks, landing page views).
  3. Google Ads campaign × day export (the same as for the tracker).
  4. Google ad groups, search terms, keywords and the video (YouTube) report for the week and the week before.
  5. Search Console for the week vs the week before (queries, pages, countries, devices).
  6. Semrush position tracking (until Felipe has access, Tereza exports it).
  7. HubSpot: MQLs by original source for both weeks (restated), disqualified, Watchleads, SQLs when available.
  8. What happened to last week's actions, and any changes during the week.
- **Definitions:**
  - Leads = Meta "Results" of lead campaigns, as Ads Manager shows (97 for 5–11 Oct), plus Google conversions.
  - The tracker uses Meta "Website registrations completed" (101 for 5–11 Oct), so the two differ slightly.
- **5–11 Oct baseline** (Tereza's report and the generator check):
  - Meta $1,174.12 and 97 leads.
  - Google Search €501.48 and 27 conversions.
  - Paid social gave **3 MQLs from 97 leads**.
  - MQL disqualification 33% vs 18%.
  - Google CPA under €25 is the watch line.
  - Search Console CTR 2.27%; Semrush ranking count 72 vs 74.
- **First report (12–18 Oct):** "last week's actions" are Tereza's 5–11 Oct items. Ask Felipe the status of each.
  - **Prioritise next week:**
    - Meta: reallocate to PP-196 (Quantum short video, $7.78 CPL) and PP-324 ($8.83), away from PP-328 ($18.23); confirm FR_Alibaba is off.
    - Google: negatives ("web summit 2027", "dubai chamber of digital economy", "startup graveyard", "startup rip", "how to start business without money"); shift budget from NA Startup Collaboration (€45.90 per conversion) to EMEA Startup Collaboration (€10.42) and EMEA Innovation (€18.86); set up the brand-negative test.
    - CRM: get the SQL export and a stable MQL sync, and agree the restated MQL baseline.
  - **Experiments:**
    - a brand-negative test on Google non-brand, read after 7 days;
    - the PP-196 angle in USCA and Western Europe prospecting;
    - a Japan-language Search test (Japan is 18.6% of organic clicks with no paid support).
  - **Monitor:** paid MQLs and the SQL lag; MQL disqualification rate; Google CPA under €25 as budget rises; Search Console CTR; Semrush ranking count.
  - **Top 5 focus list:**
    1. Scale PP-196 and move retargeting budget from PP-328 to PP-324.
    2. Fix the MQL gap (SQL export, restated baseline, why paid social gave 3 MQLs from 97 leads).
    3. Google: negatives, budget shift to EMEA Startup Collaboration and Innovation, brand-negative test.
    4. Confirm FR_Alibaba is off and the new YouTube US-UK-FR-IT campaign was paused on purpose; set a YouTube decision date (8 weeks, zero conversions, about €550 a month).
    5. Protect organic: "plug and play summit" (position 1.90 → 8.16) and "plugnplay" (−44), and internal links to the November Summit page.
- **Generator status:** in the cloud repo, `tools/weekly_report/build_weekly_report.py` built the paid and CRM parts.
  - Verified on 5–11 Oct: it matches the tracker to the cent and matches Tereza's platform figures.
  - Still to add: Google KPI table, Meta account totals and lead engine, YouTube, the ad-group / search-term / video / ad-level parsing, Search Console, Semrush, the improved/declined/changed cards, biggest movers, recommendations, experiments, monitor list, Top 5, data sources.
  - In a normal chat, build the report directly (DOCX or PDF) from the uploaded exports, following this spec.

---

## 10. Spend tracker: `PNP_Paid_Media_Spend_Tracker_2026.xlsx` (Google Sheets, v5)
- Uploaded to Google Drive and opened as a Google Sheet. It's in USD, with the $300k budget and $320k maximum.
- **Tabs:** Dashboard · Update · Weekly · Monthly · By location · Meta export · Google export · Other channels · Settings · Agency check, plus a hidden Calc tab.
  - About 4,800 plain formulas; stacked-column and column charts only.
  - Weekly runs Monday to Sunday.
- **Every Monday (about 10 minutes), on the Update tab:**
  1. Replace the 'Meta export' tab with this year's Meta campaign × day export: select all → delete → A1 → File → Import → "Replace data at selected cell". The columns needed are Reporting starts, Campaign name, Amount spent (USD).
  2. Do the same for 'Google export' (Campaign, Day, Currency code, Cost, Impr., Clicks, Conversions; .csv or UTF-16 "Excel .csv").
  3. Check the 6 ticks: columns found, dates read, both exports end on the same day, every campaign has a market, the exports fit, ended campaigns found. Then write last week's note on Weekly.
- **What's automatic:** data date, EUR→USD, market and campaign type. Market comes from the location code at the start of the campaign name (Settings → Locations).
- **Typed by hand:** ChatGPT and LinkedIn rows go on 'Other channels'. Campaigns that stopped for good go on Settings → Ended campaigns, which leaves them out of the pace.
- **First Monday of the month:** check last month's "as billed" totals against the Meta and Google invoices.
- **Capacity:** reads up to 15,000 Meta and 7,000 Google rows (Meta is about 30 rows a day).
- **Presenter notes:** `Spend_Tracker_Notes_2026.pdf` (2 pages, for Felipe). It ends with the decisions to ask for:
  1. Does FR_Alibaba count?
  2. Does ChatGPT count?
  3. Land on $300k or keep the current pace?
  4. Which exchange rate?
  5. What is the 2027 budget?
- **Summary PDF:** `PNP_Paid_Media_Spend_2026.pdf`, 3 pages for Tereza and Raúl, data to 12 Oct.

---

## 11. HubSpot newsletter audit: `PNP_HubSpot_Newsletter_Audit.pdf` / `.xlsx`
Read-only, pulled 8 Oct 2026. The period is 1 Oct 2025 – 30 Sep 2026.
- **Volume and engagement:**
  - 1,028,641 emails sent (−22% vs the previous 365 days) across 1,032 unique emails.
  - Open rate 26.9%, click rate 3.3%.
  - Hard bounce 1.29% (+97%); unsubscribe 0.81% (+72%).
- **Email health (HubSpot, last 30 days):** score 3/10. Hard bounces 2.54% vs a 0.25% benchmark; unsubscribes 1.04% vs 0.35%.
- **Bounces:** three emails caused 83% of hard bounces in Aug–Sep: "JAP_Sansan List_Consent Mail" (3,421), the Corporate Partnership Survey third batch (748) and "FR_ALIBABA COCREATE STARUP EMAIL" (743).
- **Database cost:**
  - **590,458 marketing contacts in a 630,000 tier (93.7%)**; the next tier update is 31 Oct.
  - **508,812 (86%) had no open or click in 12 months.**
  - **433,657 never opened** a marketing email.
- **Subscription types:**
  - **Location newsletters share one subscription type,** "Plug and Play Marketing Communications" (UK, Texas, Italy, Seattle, Indiana, Türkiye, Cyprus, Central Asia). Unsubscribing from one removes the person from all Plug and Play marketing.
  - There are 95 subscription types (14 active, 81 archived).
- **Tracking gaps:**
  - The **unsubscribe survey is OFF.**
  - **No email has a team assigned,** although 62 HubSpot teams exist, so HubSpot can't report by location.
  - 309 workflows send email; 251 are ON, **65 are ON but not updated since before 2024**, and **5 still send COVID-era ebooks**.
  - 232 emails are HR birthday or anniversary emails.
- **The newsletter map lists 40 recurring newsletters:** 1 global (GNL, sender "Jacky from Plug and Play", created by Jacky Tsang and Anto Guarin), 15 location, 9 industry, 6 program, 8 mentor/alumni and 1 internal (Sanam Amidi).
  - Industry newsletters: Enterprise & AI, Sustainable Future, Fintech & AI Fund Insights, Smart Cities, Global Travel & Hospitality, Health, Financial Services, Brand & Retail (BRAM), Supply Chain SLAM.
  - It covers the location audit, who sends recurring newsletters, metrics, CRM and workflows, and industry newsletter performance.

---

## 12. ICP vs Conversions: `ICP_vs_Conversions_2026.pdf` / `.xlsx` (Raúl's exercise)
- **The exercise:** break down the marketing email database and conversions against the ICP. For JTP Contact us: "Type of profile form" + original source + job title. For content downloaders: "RFI type of profile form" + original source.
- **Data:** a read-only HubSpot pull on 8 Oct 2026, covering form submissions 1 Oct 2025 – 30 Sep 2026. Aggregates only, with "<5" for counts of 1–4.
- **Totals:**
  - JTP: 11,881 contacts (13,395 submissions, 8 forms).
  - Content: 13,385 contacts (17,052 submissions, 66 forms).
- **Corporates with 10,000+ employees:**
  - **2.0% of JTP (243)** and **6.4% of content (853).**
  - They get a deal **about 10× (JTP, 5.3% vs 0.5%)** and **about 5× (content, 4.7% vs 1.0%)** more often than average.
  - Strict ICP (role + 10,000+, plus $100M revenue where known): JTP 24, content 76.
- **Other profiles:** government 384 (JTP) and 544 (content); startups 9,410 (**79% of JTP**) and 2,255 (content).
- **Deals:** 63 (JTP) and 135 (content). Customers: 17 and 72.
- **Job title empty:** 67% of JTP and 83% of content contacts.
- **Content profile mix:** Other 3,783 · Startup 2,255 · Corporate smaller or unknown size 1,891 · Investor/VC 1,523 · Job seeker 992 · Corporate 10,000+ 853 · Student 803 · University 732 · Government 544.
- **Paid social:** 61% of content contacts (8,214), of which 449 were corporates with 10,000+ employees, and **fewer than 5 deals**. JTP from paid social: 665 contacts, 40% disqualified.

---

## 13. Research yardstick (internal only, never cite in presentations)
The source is `research/Paid_Media_Playbook_2026.md` (as of 8 Oct 2026). Felipe also has a Word version, "B2B_Lead_Gen_Paid_Media_Playbook_2026 (Meta, Google Search, ChatGPT Ads).docx".

**The 10 things that matter most:**
1. **Optimise on a qualified signal, not form fills.** Send a same-day "ICP-qualified lead" event to Meta and Google; count startup leads at value 0 or not at all.
2. **SQL is too slow to bid on** (66 days). Meta needs the optimised stage within 28 days; Google imports must arrive within 90 days. Use a fast proxy event.
3. **HubSpot lifecycle stage is unusable** (95% SQL). Use Salesforce lead status or a fit property.
4. **On Meta, creative is the targeting.**
   - Broad audiences with hard controls: location, language, minimum age, custom-audience exclusions.
   - 8 or more genuinely different concepts per ad set, one persona each, with the qualification in the ad.
5. **Instant forms:** Higher Intent, qualifying questions, lead filtering. Conversion Leads works only with instant forms; website forms need CAPI events.
6. **Google:**
   - Brand, non-brand and competitor terms in separate campaigns; exact and phrase match as the core.
   - At about €7.5k a month, the account is below the $10–50k a month band where Smart Bidding works best.
7. **AI Max has no strict whitelist mode.** Use campaign URL exclusions or turn URL expansion off. Messaging restrictions (up to 40) can keep "for startups" wording out.
8. **Report cost per SQL and pipeline next to CPL.**
9. **Local-language creative and landing pages** for France, the UK, Germany, Spain and Italy. Plug and Play's own 3:1 result is the strongest evidence.
10. **Add a "How did you hear about us?" field.**

**Meta:**
- Structure:
  - CBO with 1–3 broad ad sets; ABO for tests at about 20% of budget (2–5 ads each).
  - About 50 optimisation events per ad set a week.
  - Raise budgets about 20% at a time.
  - Prospecting and retargeting in separate campaigns; no interest splits.
- Narrow stacks of about 8k people drive CPMs up. One agency widened to about 300k, put the qualifying into the creative and reports CPL down 40–60% (single case).
- Creative: 8–20 concepts per ad set, refreshed every 2–3 weeks.
  - B2B formats: founder or expert talking head; proof (logos, case results); "problem" statics that name the buyer; carousels.
- Value rules raise or lower bids by country, placement or age.
- The Creative Testing tool runs 2–5 test ads at even spend.
- Changes and constraints since 2025:
  - Detailed-targeting exclusions were removed in 2025; use custom-audience exclusions.
  - The 7-day-view and 28-day-view windows were removed from the Insights API on 12 Jan 2026, and since Jan 2026 EU users have had a "less personalised ads" option.
  - **No political or social-issue ads in the EU since 6 Oct 2025 (TTPA),** a risk for government-themed creative.
  - Location fees from 1 Jul 2026.
- HubSpot's native Meta CAPI integration syncs lifecycle changes and HubSpot form submissions. Only events after setup count, and the pixel should be installed only through HubSpot to avoid duplicates.
- Make's CAPI-for-CRM app is free from Feb 2026 to Feb 2028.
- Vendor case: a separate "qualified" event (disqualifying by revenue and headcount) cut cost per qualified lead by 46%.

**Google:**
- AI Max for Search (GA reportedly 15 Apr 2026): search-term matching, text customisation, final URL expansion. The search terms report has a "Source" column.
- Auto-upgrade to AI Max in Sept 2026 for campaigns with automatic assets or broad match. **Check whether our campaigns were upgraded.**
- PMax: 10,000 negatives, search terms report, channel reporting.
- Offline conversion uploads go through the Data Manager API from 15 Jun 2026.
- Consent Mode v2 is mandatory in the EEA.
- "Qualified Future Conversions" (predicts up to 180 days) is in limited test.

**KPI risks to raise with Raúl:**
- Meta CPL −20% conflicts with lead-quality filtering and the location fees. Agree on CPL per qualified lead instead.
- Paid search MQLs +15% depends on AI Max and on MQL meaning corporate MQLs.

**New angles to test:**
- talking-head and opinion-leader video (AI CoE experts, local MDs);
- localised lead magnets per market;
- an interactive "innovation maturity assessment" instead of a PDF;
- separate corporate and startup journeys;
- instant forms with Higher Intent;
- an AI Max experiment;
- 1–2 competitor campaigns;
- webinars and events as SQL accelerators (webinar MQLs convert to SQL at 39% vs 26% for PPC);
- a ChatGPT BOFU test;
- a LinkedIn company-list test.

---

## 14. The agency's account notes (Toco Marketing, Notion "PNP" page; Felipe has `PNP_Account_Report.docx`)
- **Meta:**
  - Optimises for welcome_conversion at a **$10 target CPA**.
  - The written strategy (Oct 2025: two scale CBOs plus a 20% ABO testing campaign) no longer matches the account. The **2026 location strategy (from 15 Jan)** set one CBO per location with no separate creative testing.
  - Week of 5 Oct: 93 Meta leads at $11.91. Weekly spend fell from about $2,150 to about $1,100 after the cut to $160 a day; leads fell from 178 to 93.
- **Google:**
  - Search CPL fell from €97.30 to €27.75 over 5 weeks after the August restructure.
  - NA loses 74% and EMEA 84% of eligible impressions to budget.
  - On 13 Aug it was restructured into NA and EMEA non-brand Search (originally €147.40 a day each), with brand inside them.
- **Creatives:** 59 of 279 tested creatives (21%) won.
- **Naming:**
  - Campaign: `{Location}_{Language}_{Type}_{Objective}`.
  - Ad set: `{Location}_{Language}_{Type}_{Objective}-{Event}_{Audience}_{Topic}`.
  - The August Google campaigns use `Geo:NA_Channel:GoogleAds_Network:search_Type:non-brand_Goal:leads_Date:20260813`, so naming isn't consistent.
- **Audiences:** rebuilt on 16 Apr 2026 (website actions, content pages, Instagram and Facebook engagement, video 25%). There's **no CRM customer audience.**
- **Gaps:**
  - an empty Experimentation Roadmap;
  - the 4-week welcome-tracking outage in Jul–Aug;
  - an open HubSpot discrepancy.
- **Toco, 8 Oct:**
  - The co-working campaign performs well. Toco said it was paused for budget; the 14 Oct audit shows US-SV coworking live at €5 a day.
  - Ads featuring Naomi can keep running as long as the creatives aren't edited.
  - An AI survey launch was planned.

---

## 15. Deliverables so far (all on the GitHub branch above)
| File | What it is | Status |
| --- | --- | --- |
| `Paid_Media_Audit_2026.pdf` | Audit deck v3, 15 slides (section 7) | Ready to present; ask before changing slides |
| `PNP_Paid_Media_Spend_Tracker_2026.xlsx` | Spend tracker, Google Sheets (section 10) | Live in Felipe's Drive; data to 12 Oct |
| `PNP_Paid_Media_Spend_2026.pdf` | 3-page spend summary for Tereza and Raúl | Data to 12 Oct; to present |
| `Spend_Tracker_Notes_2026.pdf` | Felipe's 2-page presenter notes for the tracker | Done |
| `ICP_vs_Conversions_2026.pdf` / `.xlsx` | Raúl's ICP exercise (section 12), on brand, no logo | Done |
| `PNP_HubSpot_Newsletter_Audit.pdf` / `.xlsx` | Newsletter audit (section 11) | Done (not yet on brand) |
| `PNP_Paid_Media_Audit_Strategy_2026.pdf` | Deck v1 | Superseded |
| `reports/audit/paid_media_audit_2026-10-14.md` | Full read-only browser audit (Meta, Google, ChatGPT, 21 landing pages) | Source data |
| `research/Paid_Media_Playbook_2026.md` | Research yardstick (section 13) | Internal |
| `prompts/browser_audit_paid_media.md` | Read-only Claude-in-Chrome audit prompt (run one part per session) | Reusable |
| `reports/weekly/reference/2026-10-05_Tereza_Paid_Performance_Report.md` | Tereza's 5–11 Oct report as text | Reference for the weekly report |
| `reports/weekly/sample-2026-10-05/` | Format sample (not sent) | Reference |
| `.claude/skills/weekly-paid-report/report_spec.md` | Weekly report spec (section 9) | Reference |
| `tools/…` | Python builders (deck, tracker, ICP report, weekly report, brand module) | Need Claude Code with the repo |

Earlier, on 8 Oct, Felipe sent Tereza and Raúl a first spend spreadsheet (Q3 and full year, in EUR) with an email. It's superseded by the USD tracker.

---

## 16. To-do tracker (Claude Doc)
https://claude.ai/code/artifact/c6deff91-4a61-4e7b-88ab-bcde7c269a1c

The doc is titled "To-Do Tracker – Performance Marketing & CRM". Its sections are:
- Inbox
- Before Thiago leaves (30 Oct)
- This week: access and setup
- Next 2–4 weeks
- My 30/60/90-day plan (with KPIs, Tools access)
- Other tasks from my list
- Later (once settled)
- Weekly routine
- Questions to clarify with Tereza
- Done so far
- Reporting: what leadership wants and current numbers
- Who's who
- Meeting notes

Felipe adds new items to the Inbox, and Claude sorts them into the right section.

**Open items, as of 16 Oct:**
- **Before Thiago leaves:**
  - review the handover document;
  - ask how paid spend splits between content downloads and Contact us forms;
  - get access to Thiago's paid media dashboard;
  - ask whether the agency fees came out of the paid budget, and which Meta metric the agency used for leads and CPL;
  - ask about the agency report issues (Google's currency before 21 Sep, the doubled weeks, which H1 total is right, the approved monthly caps).
- **This week:**
  - Salesforce access (follow up with Raúl);
  - Playbook / Looker Studio training link from Saku;
  - get Tereza's meeting deck;
  - Leticia's Looker report;
  - present the spend PDF and agree the Q4 pace;
  - find the AI CoE opinion-leader videos and the local video assets (Italy, France, UK);
  - schedule the talking-head review with Cami and Amanda (w/c 19 Oct, align with Raúl);
  - check whether HubSpot campaigns are connected to the ad accounts;
  - track the AI survey launch;
  - check which landing page each live campaign uses, then meet Rosa on designs and edits (bring the audit fixes and the corporate page brief; ask which redesigns are already running);
  - book the intro with Anto (newsletter workflows, past practices, creative pipeline; covers the 30-day "meet Anto" item);
  - subscribe to the newsletters (global, internal, the 9 industry and 15 location newsletters);
  - agree newsletter ownership with Raúl and Allison.
- **Next 2–4 weeks:**
  - weekly MQL/SQL routine;
  - campaigns with local assets for the 5 key markets;
  - newsletter fix plan;
  - **HubSpot cost:** size the saving from setting the 508,812 inactive marketing contacts to non-marketing;
  - subscriber growth: history and peaks, and the metrics leadership receives;
  - nurture strategy for content downloaders (52% of MQLs);
  - an EMEA vs Americas spend and ROI view for Sina;
  - relationships with the local teams;
  - check HubSpot vertical names against the 27 official verticals.
- **Weekly routine:**
  - MQL and SQL CSVs from Playbook, split by JTP Contact us vs content downloaders;
  - source mix week on week;
  - MQLs by country vs spend by country;
  - disqualification reasons and the auto-disqualification rate;
  - the Monday tracker update;
  - the monthly invoice check;
  - the weekly paid performance report from 19 Oct.
- **Other tasks from the list:**
  - confirm the AI Max campaigns are back on once the landing-page whitelist is ready;
  - talk to Juki about newsletter requirements;
  - plan new-hire newsletter training with Sara;
  - organise CRM contact data (inactive contacts);
  - documentation: an onboarding process, and Confluence templates as the source of truth;
  - dashboards: new contacts, form submissions, page views, channel performance.
- **Later (once settled):**
  - interview salespeople on inbound lead quality;
  - test the ICP revenue threshold ($100M vs $500M);
  - help with sales collateral;
  - help raise marketing's profile internally (share wins: logos, big deals).

---

## 17. Meeting notes
- **Tereza, 8 Oct (voice-note transcript):** Felipe got the funnel numbers in section 4, the weekly routine, the who's who, and these open questions (section 18). Key asks from that meeting:
  - weekly MQL/SQL analysis split by JTP Contact us vs content downloaders;
  - MQLs by country vs spend by country;
  - EMEA vs Americas parity for Sina;
  - Sanam's full funnel report;
  - a nurture strategy for content downloaders.
- **Thiago (Toco), 8 Oct:**
  - He leaves on 30 Oct, with a handover doc (Google and Meta tests, insights, caveats) near month end.
  - Felipe gets Notion and the naming conventions.
  - Performance is stable, with Google improving and budgets reduced.
  - The co-working campaign is paused but performs well.
  - AI Max is paused (URL expansion issues; landing-page whitelist in progress).
  - Naomi ads can run as long as the creatives aren't edited.
  - The AI survey launch is planned.
  - Felipe gets to know the brand, then holds a dedicated sync (done).
- **Marketing handover meeting (notes added 16 Oct):**
  - Goal: align on handover priorities for landing pages, newsletters and the CRM database.
  - Discussed:
    - the audit of marketing materials and the CRM, to find what performs and cut HubSpot subscription costs;
    - landing page assets, redesigns in progress and who edits pages (Rosa for designs and edits);
    - vertical and location newsletters, sender approvals, brand guidelines and the handover of responsibilities;
    - historical subscriber peaks, the inactive-contact clean-up and the metrics shared with leadership.
  - Next steps: the four "This week" items in section 16.
  - The counterpart wasn't named. If it was Aly, tick "Landing pages: meet Aly".

---

## 18. Open questions and decisions pending
**With Tereza:**
- Does FR_Alibaba ($4,491) count toward the $300k?
- Does ChatGPT Ads ($257) count?
- Land on $300k (about $1,529 a week) or keep the current pace (about $303.8k)?
- Which FX rate: 1.1177, or Finance's monthly rates?
- What is the 2027 budget?
- Does the $300k cover all territories?
- SQL definition: Salesforce or HubSpot?
- AI CoE startup share: over 60% (said in the meeting) or over 50% (in the deck)?
- Should the ICP revenue threshold be $500M instead of $100M?
- Which agency did she mean?

**With Raúl and Tereza (from the audit deck):**
- A yes to the new Meta and Google structures (same budget).
- The US budget: about $95 a day to learn vs $55 in the plan.
- One prospecting ad set or two (section 8).
- Web team time; local teams for the translations.
- The two tests: "ICP lead" optimisation and instant forms.

**Checks:**
- Is the Meta "Languages" option available on lead ads with a website form, and can each language have its own URL and video?
- Does HubSpot store utm_content?
- Accept Meta's custom-audience terms.
- Who builds the GTM rule and the Conversions API copy?
- Were the Google campaigns auto-upgraded to AI Max?
- The deck cover's Google figure includes PMax (section 7, slide 1). Fix it at the next rebuild, after asking Felipe.
- Semrush access.

**Felipe's pending call:** update slide 10, the structure slide and the plan with section 8. He said to tell him before changing slides.

---

## 19. Timeline (8–16 Oct 2026)
- **8 Oct:**
  - First spend spreadsheet (EUR, later corrected) and an email to Tereza and Raúl.
  - HubSpot newsletter audit (PDF and spreadsheet; read-only, via Claude in Chrome).
  - ICP vs Conversions v1.
  - Tereza meeting brief and the to-do tracker (Claude Doc).
  - Paid media research playbook.
  - Felipe's 30/60/90 plan saved.
- **13 Oct:**
  - Budget confirmed: $300k USD, max $320k.
  - Agency Notion reports extracted (Claude in Chrome) and checked against the platforms.
  - Spend tracker rebuilt in USD for Google Sheets (v4, then v5 after UX feedback and a chart fix).
  - Spend PDF.
- **14 Oct:**
  - Audit deck v1 (rejected style).
  - Browser audit prompt; Felipe ran the read-only audit (Meta, Google, ChatGPT, landing pages).
  - Weekly report generator, brand guidelines adopted, and the weekly report spec ("keep all of Tereza's content").
  - ICP report rebuilt on brand.
  - Tracker presenter notes.
  - Audit deck v2, then v3 (visual, Andromeda, mock-ups, wireframes, 90-day plan).
  - Local-creatives slide added.
  - ICP-controls slide added.
  - Chat answers on getting the ICP with broad targeting (section 8).
- **16 Oct:** handover meeting notes added to the tracker; this context pack.

---

## 20. Files to upload to the new chat or project
**From GitHub** (`felipecardenassa-sudo/pnp`, branch `claude/paid-ads-spend-audit-w9vbm5`: Code → Download ZIP, or open each file and click "Download raw file"):
- `handover/Claude_Context_Pack.md` (this file) and `handover/Claude_Project_Instructions.md`
- `Paid_Media_Audit_2026.pdf`
- `PNP_Paid_Media_Spend_Tracker_2026.xlsx` (or use the Google Sheet in Drive) and `Spend_Tracker_Notes_2026.pdf`
- `ICP_vs_Conversions_2026.pdf` and `.xlsx`
- `PNP_HubSpot_Newsletter_Audit.pdf` and `.xlsx`
- `reports/audit/paid_media_audit_2026-10-14.md`
- `research/Paid_Media_Playbook_2026.md`
- `reports/weekly/reference/2026-10-05_Tereza_Paid_Performance_Report.md`
- `.claude/skills/weekly-paid-report/report_spec.md`
- `prompts/browser_audit_paid_media.md`

**From Felipe's own files:**
- Plug and Play Brand Guidelines 2021 EXTERNAL (PDF)
- Buyer Persona 2024 (PDF) and the Key Messages spreadsheet
- Felipe's 30 days plan (PDF)
- Tereza's EMEA MD Joint Session deck (July 2026)
- Tereza's "Paid_Performance_Report_Oct5-11_2026.docx"
- The agency's "PNP_Account_Report.docx"
- The playbook .docx

**Each week, for the weekly report:** the exports listed in section 9.
