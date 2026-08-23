# PumpRun — Moat Analysis: Generic FSM Platforms
*Companion to MARKET_ANALYSIS.md (sizing/pricing baseline lives there; not repeated here). Focus: why each incumbent's moat does and doesn't reach septic, and where the $499 flat wedge fits. Live-verified Aug 2026.*

---

## 1. ServiceTitan (TTAN — public since Dec 2024)

**Pricing model (live-verified):** Quote-only. servicetitan.com/pricing shows three per-technician packages (Starter / Essentials / The Works), each ending in a "Request Pricing" button — no dollar figures anywhere on the page. Third-party reported: **$245–$500/tech/mo**, implementation **$5k–$50k+**, contracts **12–36 months** ([fieldservicecompare.com](https://fieldservicecompare.com/articles/servicetitan-review-2026/), [thetechyside.com.au](https://www.thetechyside.com.au/software/servicetitan), [toarn.com](https://toarn.com/insights/servicetitan-ai)). Flagged: third-party reported.

**Stated moat:** "Operating system of the trades." Pricing page claims 100,000+ contractors and "+15% average yearly revenue increase." Investor narrative: gross dollar retention **>95%** and net dollar retention **>110%** for 10+ consecutive quarters; **$82.1B gross transaction volume** processed in FY2026; ~$961M FY2026 revenue, +33% YoY ([omahaline.com/essays/ttan](https://omahaline.com/essays/ttan)). Distribution moat via ABC trade-association partnership (23k members, free-trial funnel) and ABC Supply supplier integrations with nightly price syncs ([ainvest.com](https://www.ainvest.com/news/servicetitan-abc-playbook-building-500b-moat-trades-software-sector-2507/)).

**Real moat (analysis):**
- **Switching costs — the strongest in category.** ETF = **100% of remaining contract value**; BBB filings document shops pursued for $18,000–$67,230 ([runacall.com](https://www.runacall.com/learn/articles/servicetitan-etf-what-hvac-shops-pay-to-leave), [bbb.org complaints](https://www.bbb.org/us/ca/glendale/profile/project-management-software/servicetitan-inc-1216-1290182/complaints)). Data egress is adversarial: 60-day post-cancellation export window, full job-history/photo extraction requires custom API work, multiple reports of contractors needing legal help to leave ([thetechyside](https://www.thetechyside.com.au/software/servicetitan)).
- **Payments take-rate:** processing markup of ~30–60bps over standard processor rates on high transaction volume ([fieldservicesoftware.io comparison](https://fieldservicesoftware.io/comparisons/service-fusion-vs-servicetitan/)); $82B GTV means even thin bps is real revenue.
- **Integration gravity:** they *shut off Podium's integration for ~1,000 shared customers* mid-season when Podium launched a competing FSM — proof they treat system-of-record status as a defended asset ([saastr.com](https://www.saastr.com/servicetitan-just-shut-off-podiums-integration-for-1000-shared-customers-agents-turned-a-9-year-partner-into-a-direct-competitor/)).
- **Data moat:** hundreds of millions of recorded trades calls feed booking AI ([toarn](https://toarn.com/inservicetitan-ai) → https://toarn.com/insights/servicetitan-ai).
- **Sales-led distribution:** enterprise AE motion + association channels; deliberately excludes small shops.

**Will they chase $499 flat septic? No — structurally cannot.**
- Their own public position: platform "not optimized for businesses with 3 or fewer technicians"; Year-1 cost for a 10-tech shop exceeds $60K ([toarn](https://toarn.com/insights/servicetitan-ai)). A sales-led model needs ACVs north of ~$25K to cover AE + implementation cost; a $6K ACV septic shop is negative-margin.
- Public-company growth targets point upmarket (Max program reportedly doubles subscription revenue per customer when ramped — [omahaline](https://omahaline.com/essays/ttan)). The entire US septic software spend at $499/mo × ~7,300 firms ≈ $44M/yr ceiling — immaterial against ~$1B revenue.
- They maintain an SEO landing page for septic ([servicetitan.com/industries/septic-business-software](https://www.servicetitan.com/industries/septic-business-software)) — keyword harvesting, not product investment. No statutory filing workflow exists or is coming.

**PumpRun wedge:** (1) Their contract hostility is a marketing gift — "no contracts, no ETF, export your data anytime" writes itself against documented BBB horror stories. (2) 3–12 month implementations vs day-one CSV import. (3) The Podium episode proves integration access is revocable at their whim — a septic-native tool that owns its own compliance data has no such exposure. (4) Shops graduating past PumpRun's ceiling are ST's only relevant overlap; make that graduation path expensive for them by owning the tank-history ledger.

---

## 2. Housecall Pro

**Pricing model (live-verified):** Published tiers — Basic **$59/mo** annual ($79 monthly, 1 user); Essentials **$149** ($189, 5 users, **+$100/user** after); Max **$299** ($329, 8 users, **+$75/user** after). Card processing "as low as 2.59%", bank payments 1%. Explicitly **no contracts, cancel anytime**. Route optimization gated to Max tier; field capability is "**Offline viewing**" only — their own pricing page admits it ([housecallpro.com/pricing](https://www.housecallpro.com/pricing/)).

**Stated moat:** "System of record" for 200K+ pros; community of 30K+ members; "AI built from 100M+ jobs." The sharpest stated strategy comes from their President/former Chief Fintech Officer: treat payments as a business, not a feature — cards, ACH, consumer financing, payroll, bill pay — "make financial services disappear into the workflow… customers for life" ([pipe.com interview](https://pipe.com/resources/articles/vertical-saas-at-work-making-finance-disappear-for-home-service-pros)). Investor framing: default platform for the trades' broad middle ([deltavcapital.com](https://deltavcapital.com/insights/why-we-invested-in-housecall-pro)).

**Real moat (analysis):**
- **Payments/fintech attach is the moat engine**, not the subscription: card take-rate from 2.59%, consumer financing on big tickets, payroll and accounting services. Revenue reached **$201.2M in 2024** (up from $37.2M in 2021) across ~180K paying pros → blended ARPU ≈ **$93/mo** ([geo.sig.ai](https://geo.sig.ai/brands/housecall-pro)).
- **Brand/SEO dominance** in SMB home services; review volume compounds.
- **Community network effects are soft** — real but shallow; the consumer marketplace (hauling/junk removal) is niche.
- **Churn is structurally higher**: owner-operated base "changes tools when they change phones"; Jobber/Workiz/Fusion all run displacement plays into their base ([withorbital.com](https://www.withorbital.com/data/software/housecall-pro/)). BBB pattern: worst offender of the big three for cancellation friction and post-cancellation charges ([crewroute.app BBB report](https://crewroute.app/resources/best/bbb-complaints-field-service-software/)).

**Will they chase $499 flat septic? No.**
- Horizontal across 30+ trades; **no septic industry page exists** in their nav (checked live). MA Title 5 filing logic serves maybe ~400 MA shops = 0.2% of their base; engineering hours go to AI CSR serving every trade instead.
- Seat-based tiering means a flat product would cannibalize Essentials→Max upgrade math for zero strategic gain.
- Their fintech moat barely maps onto septic: pump-outs are frequently invoiced to municipalities, property managers, and realtors on net terms — low card volume, low financing attach. The niche monetizes badly inside their model.

**PumpRun wedge:** (1) Offline **completion** vs their offline *viewing* — rural dead-zone routes are daily pain. (2) Board-formatted compliance PDFs vs generic invoices. (3) +$100/user seat taxes punish exactly the office-staffed 3–8 truck shop PumpRun prices flat. (4) Their churn-and-displacement base is PumpRun's lead list: every HCP septic customer is one renewal-price hike from switching.

---

## 3. Jobber

**Pricing model (fetch blocked — flagged):** getjobber.com/pricing returned **403 twice** (bot-blocked). Search-index snippet of the official page advertises "Core starting at $21/mo*, Connect $70/mo*, Grow $105/mo*" (annual teaser rates). Converged third-party trackers: Core **$29–49** (1 user), Connect **$99–139** (1 user) / **$149–199** (5 users), Grow **$149–199** (1 user) / **$229–299** (5 users), Plus **$399–499** (5 users); **+$29/user**; payments 1–2.9% + 30¢; **annual prepaid plans non-refundable** ([getjobber.com via search](https://www.getjobber.com/pricing/), [fieldservicepro.io](https://fieldservicepro.io/blog/jobber-pricing/), [fsmadvisor.com](https://www.fsmadvisor.com/pricing/jobber), [frontdeskreview.com](https://frontdeskreview.com/software/field-service-management/jobber/)). All figures third-party reported.

**Stated moat:** CEO Sam Pillar: "We're a SaaS-plus company. The first thing we are is **workflow system of record**, and that's really the entry point for all customers to adopt payments after that" ([Axios](https://www.axios.com/pro/fintech-deals/2023/02/07/jobber-raises-100m-fintech)). Brand: "blue collar first," proprietary Home Service Economic Report drawn from 100K businesses ([prnewswire Q2 2026](https://www.prnewswire.com/news-releases/home-service-delivers-steady-revenue-growth-in-q2-2026-proving-its-resilience-through-a-volatile-quarter-302856785.html)).

**Real moat (analysis):**
- **Payments take-rate rising:** online payments crossed **>50% of Jobber-processed transactions** in Q3 2025 (+7% YoY); est. $150M revenue (~2023) over 100K customers → blended ARPU ≈ **$125/mo**; $13B billed/collected annually through platform ([sacra.com](https://sacra.com/c/jobber/), [Contrary Research](https://research.contrary.com/report/jobber), [TechCrunch](https://techcrunch.com/2023/02/07/jobber-fixes-on-100m-as-its-platform-for-home-services-pros-hits-200k-users/)).
- **Brand among sole proprietors** (lawn, cleaning, handyman) is arguably the strongest in category; capital-efficient growth story.
- **Churn acknowledged by their own investors:** SMB segment brings "higher churn than enterprise, less potential for MRR expansion, low ARPU" ([Version One](https://versionone.vc/announcing-jobbers-100m-series-d-building-a-company-for-the-long-term-in-an-era-of-start-up-hyper-growth/)). Month-to-month defaults mean retention rests on habit breadth (quote→invoice→payment→payroll), not contracts.
- **No true network effects** — Pillar explicitly refuses lead-gen/discoverability ("race to the bottom"), so there's no marketplace flywheel.

**Will they chase $499 flat septic? No.**
- Sweet spot is <20 employees, many 1–2 person shops, across 50+ segments served generically ([TechCrunch](https://techcrunch.com/2023/02/07/jobber-fixes-on-100m-as-its-platform-for-home-services-pros-hits-200k-users/)). State-level septic filing logic contradicts the horizontal-leverage thesis that got them to $150M.
- At ~$125 blended ARPU, a $499 vertical SKU would be their top-tier outlier requiring dedicated support content for a segment that is one line item in fifty.
- Routing is basic; dispatch-dense verticals are explicitly not their strength.

**PumpRun wedge:** Jobber is the "good enough cheaper" threat itself — don't fight it head-on. Wedge points: (1) basic routing vs NN route sequencing tuned to dump-station geography; (2) no compliance documents; (3) $29/user escalation + non-refundable annual prepay = price-framing contrast for flat $499; (4) zero septic presence means zero brand defense when a hauler asks peers "what do you use?"

---

## 4. Workiz

**Pricing model (partially opaque — flagged):** workiz.com/pricing returns **404 live**; no consistently published paid-tier pricing. Third-party reported: Lite free (20 jobs/mo cap), Starter ~**$65** (1–2 users), Standard/Pro ~**$229–299**, extra users ~$40–65; realistic all-in for a 3-truck shop **$450–900/mo before processing** ([pipelineon.com, Jun 2026](https://pipelineon.com/blog/workiz-pricing/)). Payments: Workiz Pay card rates **not published**; contractor-reported **2.6–3.0%/card, 1% ACH** (ACH confirmed on [help.workiz.com](https://help.workiz.com/hc/en-us/articles/18053122621329-Understanding-bank-transfers-ACH-Workiz); instant payout +1% fee confirmed [here](https://help.workiz.com/hc/en-us/articles/18053114324753-Enabling-instant-payouts-for-card-payments-Workiz)). All figures third-party reported except ACH/instant-payout fees.

**Stated moat:** Dispatch-first positioning for route-dense, phone-heavy trades (locksmith, garage door, appliance repair); Genius AI answering/marketing add-ons; self-description as "the leading field service payments software" ([workiz.com/features/online-payments](https://www.workiz.com/features/online-payments/)).

**Real moat (analysis): thinnest of the five.**
- **The business model IS the payments spread**: unpublished 2.6–3.0% card rates above market benchmarks are the margin engine; subscriptions are the entry point. This is a take-rate business wearing an SaaS costume.
- Niche concentration in locksmith/garage gives word-of-mouth density in those trades only.
- No meaningful network effects, smallest brand and installed base of the five, VC growth pressure pushes toward AI add-on upsell rather than depth.

**Will they chase $499 flat septic? Unlikely — wrong economics both ways.**
- Septic is not a phone-volume/card-volume vertical: haulers invoice municipalities and commercial accounts on net terms, so Workiz's spread-capture model earns little from them. A flat $499 subscription with no payments upside is the worst possible customer in their P&L.
- Smallest product org of the five; zero compliance capability; building state-by-state board-filing logic is far outside their AI-answering roadmap.

**PumpRun wedge:** (1) **Pricing opacity is their biggest reported gotcha** — transparent flat $499 with published everything is a direct trust contrast. (2) Their unpublished payment rates let PumpRun own "no hidden spread" positioning. (3) If a septic shop ever evaluates Workiz, nothing in it speaks their language — no tanks, no due dates, no manifests.

---

## 5. Service Fusion (EverCommerce)

**Pricing model (live-verified):** Fully published — Starter **$208/mo** billed annual ($245 monthly), Plus **$325** ($382), Pro **$533** ($627); **unlimited users on every plan**; **no contracts**, month-to-month available; zero setup fees claimed; free personalized onboarding; ~7,000 service companies claimed ([servicefusion.com/pricing](https://www.servicefusion.com/pricing)). Note: one reviewer claims the page went quote-only ([contractorsoftwarehub.com](https://www.contractorsoftwarehub.com/service-fusion-review/)) — contradicted by today's live fetch showing dollar figures; live fetch wins. Older third-party figures ($149/$249/$389 — [fieldservicesoftware.io](https://fieldservicesoftware.io/software/servicefusion/)) reflect pre-increase pricing.

**Stated moat:** Unlimited-user flat billing ("Whether you have one technician and one dispatcher or 20 technicians and a full office, your pricing will be the same"); built-in VoIP (ServiceCall.ai); FusionPay payments powered by PaySimple; anti-lock-in marketing vs ServiceTitan ("Most companies charge an average of $2,000 for onboarding… we don't") ([servicefusion.com FAQ](https://www.servicefusion.com/service-fusion-vs-the-competitors-faq)).

**Real moat (analysis):**
- **The flat-unlimited-user price position IS the moat** — it defends the 10–20 user shop against per-seat rivals and is genuinely hard for per-seat competitors to answer without breaking their models ([withorbital.com](https://www.withorbital.com/data/software/service-fusion/): "The flat bill is the moat").
- **Parent EverCommerce portfolio** (FieldEdge, Kickserv, Joist) provides distribution, capital, and a sideways-not-upward upgrade path — retention without product excellence.
- QuickBooks Desktop sync depth and included VoIP are sticky accounting/workflow anchors.
- Weaknesses: aging UI, Android app reliability complaints, inconsistent support ([contractorsoftwarehub](https://www.contractorsoftwarehub.com/service-fusion-review/), [fieldservicesoftware.io](https://fieldservicesoftware.io/software/servicefusion/)).

**Will they chase $499 flat septic? They're already below it — and that's the trap.**
- Starter at $208–245 undercuts PumpRun outright for any shop comparing on price alone. They also maintain a septic landing page ([servicefusion.com/septic-service-software](https://www.servicefusion.com/septic-service-software)) — again SEO, not product.
- But flat unlimited-user pricing caps ARPU: ~7,000 customers × ~$250 avg ≈ low-tens-of-millions revenue funding no deep vertical R&D. EverCommerce runs a rollup playbook optimizing cross-sell across portfolio products, not state-level regulatory engineering for a 7,300-firm niche. Their competitive response to PumpRun will be marketing pages, never Title 5 form logic.

**PumpRun wedge:** (1) Never compete with Fusion on price — compete on septic depth: statutory due dates, board-formatted PDFs, offline tap-complete (their app is connectivity-dependent). (2) Their flat-price buyers are exactly PumpRun's profile (multi-user shops tired of seat math) — sell the upgrade as "same flat bill, plus the compliance layer Fusion will never build." (3) Aging mobile UX is a demo-day gift.

---

## Cross-Cutting Synthesis

### Moat strength ranking (re: septic relevance)
| Rank | Vendor | Dominant moat | Does it reach septic? |
|---|---|---|---|
| 1 | ServiceTitan | Contract + data-egress switching costs, payments bps on $82B GTV | No — sub-20-tech exclusion is deliberate and structural |
| 2 | Housecall Pro | Fintech attach (cards/financing/payroll) + SMB brand | Barely — septic's net-terms B2G billing defeats card-spread economics |
| 3 | Jobber | Payments adoption on system-of-record habit + sole-prop brand | No — horizontal thesis forbids single-state vertical depth |
| 4 | Service Fusion | Flat-price position + EverCommerce portfolio shelter | Price yes, product no — ARPU cap funds no vertical R&D |
| 5 | Workiz | Payments spread on unpublished rates | Worst fit — septic generates neither phone volume nor card volume |

### Why $499 flat is uneconomic for all five (ARPU pressure quantified)
- **ServiceTitan:** sales-led CAC (AE comp + $5k–50k implementation teams) requires ~$25k+ ACV; $6k ACV septic accounts are negative-margin before support. Public targets push ARPU *up* (Max doubling program).
- **Housecall Pro:** blended ARPU ≈ $93/mo across ~180K pros. Maintaining MA Title 5 logic serves ~400 shops = 0.2% of base; same engineers could ship AI CSR features serving 100% of base. Flat $499 also breaks their seat-upgrade ladder ($59→$149→$299).
- **Jobber:** blended ARPU ≈ $125/mo across 100K customers in 50 segments; investors already flag low ARPU/high churn as the model's tax. A one-state compliance SKU fails every internal prioritization test a horizontal platform runs.
- **Workiz:** monetization = subscription + unpublished payment spread. Septic's municipal/commercial invoicing produces minimal card volume → near-zero marginal profit → deprioritized regardless of TAM.
- **Service Fusion:** flat pricing already below $499, so "chasing" is meaningless — matching PumpRun's *depth* would require vertical R&D their ~$250-ARPU flat model and rollup parent won't fund.

**Common structural blind spot:** none of the five treats a government filing deadline as data. Their CRMs track *customer* recurrences (memberships, service plans); PumpRun tracks *statutory* recurrences enforced by a Board of Health with a 14-day clock. That inversion — regulator as the stakeholder, not just the homeowner — is outside every one of their product grammars.

### Consolidated wedge checklist (from evidence above)
1. **Anti-contract positioning** vs ServiceTitan's documented $18k–$67k ETF pursuits (BBB) — say "cancel anytime, export anytime" in every pitch.
2. **Offline completion** vs HCP's admitted offline-viewing-only.
3. **Flat-vs-seat math** for 4+ user shops vs HCP's +$100/user and Jobber's +$29/user.
4. **Transparent pricing** vs Workiz's 404 pricing page and unpublished payment rates.
5. **Depth-over-price** vs Service Fusion: never discount, always out-comply.
6. **Graduation asset:** own the tank ledger so the day a shop outgrows PumpRun, their history moves with friction toward whoever paid for it — and ST's data-egress hostility makes "your data is yours" a durable promise.

---

## Source Log (new fetches/searches, Aug 2026)
- servicetitan.com/pricing (fetched live: quote-only, per-tech packages, "Request Pricing")
- servicefusion.com/pricing (fetched live: $208/$325/$533 annual, $245/$382/$627 monthly, unlimited users, no contract)
- housecallpro.com/pricing (fetched live: $59/$149/$299 annual tiers, seat add-ons, 2.59% processing floor, offline viewing)
- workiz.com/pricing (404 live — flagged); pipelineon.com/blog/workiz-pricing (third-party ranges + unpublished payment-rate analysis)
- getjobber.com/pricing (403 twice — flagged); fieldservicepro.io/blog/jobber-pricing, fsmadvisor.com/pricing/jobber, frontdeskreview.com (converged third-party tables)
- omahaline.com/essays/ttan (GDR/NDR/GTV investor-data synthesis)
- ainvest.com ServiceTitan ABC playbook (distribution + supplier-integration moat)
- saastr.com Podium integration shutoff (system-of-record defense behavior)
- runacall.com ServiceTitan ETF explainer + bbb.org ServiceTitan complaint pages (ETF = 100% remaining value; $18k–$67,230 documented)
- crewroute.app BBB cross-platform report (113+ complaints across ST/HCP/Jobber; cancellation-friction patterns)
- pipe.com Housecall Pro embedded-finance interview (stated fintech strategy)
- geo.sig.ai Housecall Pro revenue ($201.2M 2024); deltavcapital.com investment thesis
- axios.com Jobber "SaaS-plus" CEO quote; techcrunch.com Series D (<20 employee sweet spot); sacra.com ($150M est., >50% digital payments Q3 2025); research.contrary.com/report/jobber; versionone.vc (SMB churn admission); prnewswire Q2 2026 report
- help.workiz.com ACH (1%) and instant-payout (+1%) fee confirmations
- withorbital.com Housecall Pro + Service Fusion install-base analyses ("flat bill is the moat"; displacement patterns)
- fieldservicesoftware.io Service Fusion review + ST comparison (payments markup 30–60bps; pre-increase pricing history)
- contractorsoftwarehub.com Service Fusion review (Android/UI weaknesses; quote-only claim contradicted by live fetch)
- servicetitan.com/industries/septic-business-software + servicefusion.com/septic-service-software (septic SEO pages exist; nav check confirms housecallpro.com has none)

---
---

# Part II — Septic-Vertical Specialists
*Live-verified Aug 22, 2026 unless flagged. Covers the vendors whose entire product IS septic/liquid-waste — the ones a pumper actually hears about from peers. PumpRun reference point throughout: $499/mo flat (1–10 trucks), CSV import → NN routing → tap-complete → board-formatted PDF, offline field app.*

---

## V1. ServiceCore (Denver/Lakewood, CO — PE-backed)

**Pricing model (live-verified):** Quote-only. servicecore.com/pricing shows two plans ("Start" and "Pro" — with identical feature bullet lists on the page) and zero dollar figures: "To see pricing for your business, schedule a personalized demo today." Third-party converged estimate: **~$200–400+/mo per truck, enterprise-shaped** ([septibase.com/compare](https://septibase.com/compare), [cleansavannah.com Aug 2026](https://www.cleansavannah.com/post/best-septic-service-software-2026)). Flagged: third-party reported.

**Contract:** **Annual contract required**, billed monthly — their own FAQ: "ServiceCore is billed monthly with an annual contract. We believe that you're making an investment in your business…" ([servicecore.com/pricing FAQ](https://servicecore.com/pricing/)).

**Onboarding:** **6–12 weeks** — their own FAQ: "Depending on the size of your business, that typically takes 6-12 weeks" (same page). No free trial; demo call required.

**Customers/geo:** No customer count published anywhere (MakerStack explicitly declines to invent one — [makerstack.co/reviews/servicecore-review](https://makerstack.co/reviews/servicecore-review/)). Platform stats claimed live: 556K tracked units, 3.5M completed jobs, $400M revenue processed. Capterra availability lists **US + Canada only**. $54M investment from Mainsail Partners, Feb 2022 ([pumpdocket.com comparison citing Mainsail press release](https://www.pumpdocket.com/resources/septic-software-comparison)).

**Reviews:** Capterra **4.0/5 across 51 reviews** ([capterra.com](https://www.capterra.com/p/158918/ServiceCore/reviews/)) — mediocre for a vertical category leader; no G2 presence of note.

**Stated moat:** "Built specifically for portable rental, septic, and dumpster rental businesses… best for operators that have multiple trucks." Support staff hired *from* the portable sanitation and dumpster industries ("more than any other software company in our space"). Ambassador program ("Operators Helping Operators"), ToiletTalk content brand, 2025 Portable Sanitation Industry Benchmark Report, Grease Trap Permit Lead Finder tool ([servicecore.com/pricing](https://servicecore.com/pricing/), [/become-an-ambassador](https://servicecore.com/become-an-ambassador/)).

**Real moat (analysis):**
- **Industry insidedness is genuine**: ex-operator support staff + ambassador operators = credibility no horizontal vendor can fake quickly.
- **Data gravity attempt**: the PSI Benchmark Report aggregates operator financials — the only real industry-data flywheel in the vertical. Small today, compounding if operators keep feeding it.
- **Lead-gen distribution**: Grease Permit Lead Finder makes ServiceCore a *source of revenue*, not just a cost — stickiest feature class in SMB SaaS.
- **PE capital ($54M)** funds sales coverage across four verticals (portable/septic/dumpster/grease).
- **Weaknesses:** 28-day billing cycles and unit tracking are portable-rental DNA; septic is their second language. Annual contract + 6–12 week onboarding is the exact friction profile small pumpers flee. 4.0 Capterra with 51 reviews after ~10 years signals satisfaction, not love.

**Vulnerability / where PumpRun beats them:**
1. **Speed**: 6–12 weeks vs day-one CSV→route→PDF. A 3-truck shop cannot justify a quarter of setup for scheduling software.
2. **Contract**: annual lock vs cancel-anytime — same anti-contract wedge documented against ServiceTitan in Part I.
3. **Compliance depth**: no advertised septage manifest/trip-ticket workflow; PumpDocket's neutral-ish comparison tells buyers to "ask ServiceCore about their septage compliance capabilities during your demo" — i.e., nobody knows ([pumpdocket.com/resources/septic-software-comparison](https://www.pumpdocket.com/resources/septic-software-comparison)).
4. **Price opacity** vs published flat $499.

**Defensibility: HIGH but shallow-reaching.** Their moat (industry staff, benchmark data, lead tools, PE-funded sales) is real and hard to replicate — but it's optimized for multi-truck portable-sanitation fleets, not 1–10 truck septic shops. They won't follow PumpRun down-market: quote-only sales motion structurally can't serve a $6K ACV account profitably.

---

## V2. Tank Track (Concord, NH — family-owned, founded 2013)

**Pricing model (live-verified):** **$180/mo first truck + $150/mo each additional truck**, unlimited users/tanks/storage, 10% off annual ([tank-track.com/#pricing](https://tank-track.com/)). ⚠️ **Price hike caught mid-flight**: site schema.org markup still advertises "$149 first / $125 additional"; Guideflow's July 21, 2026 snapshot shows $149/$125 ([guideflow.com/blog/septic-pumping-software](https://www.guideflow.com/blog/septic-pumping-software)); DynoRoute's Aug 19, 2026 fetch confirms $180/$150 ([dynoroute.com](https://dynoroute.com/septic-software/blog/best-septic-pumping-software)). That's a **+20% increase within weeks of this writing** — third parties are already flagging "the vendor's own signup calculator gave inconsistent numbers this week" ([cleansavannah](https://www.cleansavannah.com/post/best-septic-service-software-2026)).

**Contract:** Month-to-month, no contract, free white-glove onboarding (they import/clean your data), 1–4 live training sessions. **No free trial — 60-day money-back guarantee instead** ([tank-track.com](https://tank-track.com/), [PumpDocket comparison](https://www.pumpdocket.com/resources/septic-software-comparison)).

**Onboarding:** Minutes to register, days-to-weeks to full customization; they do the migration.

**Customers/geo:** **300+ operators claimed, 45 US states + 3 Canadian provinces**; claims users generate "27% more revenue per truck after 1 year" and aggregate recurring-revenue-captured stats for 2025 ([tank-track.com](https://tank-track.com/), [/request-demo](https://tank-track.com/request-demo)). In market since 2013 (Pumper magazine product listing Oct 2015 — [pumper.com](https://www.pumper.com/g/product-focus-office-technology-and-software/2015/10/fleet_business_management_tank_track_software)).

**Reviews:** ⚠️ **Zero reviews on Capterra as of Aug 2026** per two independent sources ([dynoroute.com](https://dynoroute.com/septic-software/blog/best-septic-pumping-software): "Tank Track shows zero reviews on Capterra… every claim above stays a vendor claim"). Their homepage schema self-reports "aggregateRating 5/5, reviewCount 300" from on-site testimonials — not third-party. Real sentiment lives in Facebook's Pumper Nation group and Reddit, where it's mixed (below).

**Stated moat:** "**#1 Most Recommended Software in Pumper Nation**" — testimonials attributed to Pumper Nation "Top contributor"/"All-star contributor" badges; "Trusted by over 300+ operators"; family-owned; "We handle onboarding for you… no strings attached."

**Real moat (analysis):**
- **Community goodwill is their actual castle.** Pumper Nation (the industry's Facebook watering hole) recommendation flow is Tank Track's acquisition engine — 13 years of founder-visible presence, CEO personally replying to Reddit threads ([r/septictanks thread](https://www.reddit.com/r/septictanks/comments/1o0bwm4/septic_service_business_looking_for_a/)). This is the one moat in the vertical that marketing dollars can't buy quickly.
- **White-glove free migration** lowers switching costs INTO them — and creates the reciprocal fear when leaving.
- Audit-ready waste manifests auto-generated as work completes; WI DNR audit-pass testimonial on homepage.
- **Weaknesses:** browser-only, **no native mobile app** (offline field capability unproven); QuickBooks connection described by competitors as "journal entries," not true sync ([PumpDocket comparison](https://www.pumpdocket.com/resources/septic-software-comparison)); compliance coverage is state-by-state patchwork — **TX and OH manifests only** per multiple sources.

**Documented failure mode (Reddit, r/septictanks):** a hauler reports: "They promised us they would integrate Florida's new manifest… (Texas and Ohio is what they have now). They promised us they wouldn't charge their monthly fee until we were up and running. **7 months later and system is not working properly, manifest has not been integrated and we have spent over $1,000. I do NOT recommend Tank Track.**" The CEO replied publicly defending onboarding timing ([reddit.com/r/septictanks/comments/1o0bwm4](https://www.reddit.com/r/septictanks/comments/1o0bwm4/septic_service_business_looking_for_a/)). Two lessons: (a) state-manifest coverage gaps are their known soft spot; (b) they fight for reputation personally — expect a scrappy defender.

**Vulnerability / where PumpRun beats them:**
1. **Flat price at 3+ trucks**: Tank Track costs $480/mo at 3 trucks, **$630 at 4, $780 at 5** — PumpRun's flat $499 wins from truck #4 onward, and the fresh +20% hike gives an immediate "lock your rate" pitch against every existing Tank Track quote.
2. **Offline completion**: browser-only tool vs PumpRun's offline tap-complete in dead zones.
3. **Compliance breadth**: TX/OH manifests vs statutory due-date engine + board-formatted PDFs; the FL manifest promise-break is citable evidence.
4. **True QuickBooks sync** vs journal-entry export.

**Defensibility: MEDIUM — community yes, product no.** The Pumper Nation position took 13 years and is genuinely hard to attack head-on; the product (browser-only, per-truck pricing, patchwork compliance) is straightforwardly out-engineerable. Expect them to defend via service and relationships, not features. Do NOT fight them inside Pumper Nation early — route around via SEO/comparison content until there's a testimonial bench.

---

## V3. PumpDocket (Steady Grove LLC — launched 2026, bootstrapped)

**Pricing model (live-verified):** Fully published, three tiers, currently **30% intro discount "locked for life"**: Starter **$99/mo** (intro; $139 std) — 1–3 trucks, **75-active-customer cap**; Team **$230/mo** (intro; $329 std) — 4–10 trucks, adds recurring scheduling, regulatory-profile trip tickets, FOG manifests, QuickBooks sync; Fleet **$454/mo** (intro; $649 std) — 11+ trucks, bulk audit exports, dedicated onboarding. Unlimited users on every plan; first month free; no contracts; no setup fee ([pumpdocket.com/pricing](https://www.pumpdocket.com/pricing)).

**Contract:** None. Month-to-month, cancel anytime; card collected at signup, charged day 31.

**Onboarding:** "Go live in one day" — self-serve CSV import on Starter, white-glove import on Team+.

**Customers/geo:** None disclosed — launched 2026, bootstrapped, single-entity LLC (support@steadygrove.com). **Zero reviews on GetApp/G2 network** ([getapp listing: "(0)"](https://www.getapp.za.com/software/2084416/pumpdocket)); no Capterra footprint found.

**Stated moat:** "Software for pumpers, not plumbers." **50-state regulatory profiles with cited source links** powering trip tickets; "no per-user fees, ever"; tap-start → gallons/disposal → tap-complete field flow "on any phone — no app to download"; same-day bookkeeper handoff; TCEQ-fine fear marketing ("a single TCEQ violation can cost up to $25,000 per day — Texas Water Code 7.102").

**Real moat (analysis): effectively none yet — but the positioning is a mirror of PumpRun's.**
- This is the closest copy of PumpRun's thesis in the market: CSV import, tap-complete closeout, same-day invoice, compliance paperwork, unlimited users, transparent pricing, no contracts. Launched months ago.
- Their claimed differentiator — cited jurisdiction profiles — is **marketing-depth, not engineering-depth**: their own compliance disclaimer reads "We don't guarantee compliance — that's your responsibility — but we make the source trail and workflow easier to defend" ([pumpdocket.com/pricing](https://www.pumpdocket.com/pricing)). Citations ≠ maintained town-by-town filing logic.
- Compliance features sit behind the Team tier; Starter caps at 75 active customers — a real operational ceiling for even tiny routes.
- Bootstrapped solo-shop economics: no observed customer count, review base, or support org. Key-person risk.

**Vulnerability / where PumpRun beats them:**
1. **They validate the category — and give PumpRun a differentiation checklist.** Every PumpDocket claim PumpRun can't match (50-state profile citations, lifetime rate-lock, first month free) should be either matched or out-flanked publicly.
2. **Depth race PumpRun can win now**: statutory due-date engine with filing-clock enforcement (14-day MA Title 5-style deadlines) vs static citation pages; offline-native completion parity needs verification — their "offline field app" claim exists ([product-preview#step-drivers](https://pumpdocket.com/product-preview)) but is unproven at zero-review scale.
3. **Price honesty cuts both ways**: intro pricing expiring to $139/$329/$649 gives PumpRun a standing "what it really costs" comparison once their launch window closes.
4. **Trust surface**: anonymous LLC vs verifiable operator references — in a word-of-mouth trade, the vendor pumpers can call wins.

**Defensibility: LOW today, but highest watch-list priority.** Nothing replicates slowly here — they're fast, cheap, and saying the right things to the exact buyer. If they land even 100 shops and publish state-profile maintenance cadence, they become the price floor under the whole category. Counter-strategy: out-publish them on compliance (real form logic, named towns, filing receipts) and out-reference them (customer stories with phone numbers).

---

## Fringe Map — the crowded edge (brief)

| Vendor | Pricing (live/flagged) | Septic posture | Why it matters |
|---|---|---|---|
| **Business Genie** (Business Genie LLC) | **$50/$100/$200/$350 by user tier** (1/3/8/9–15 users), month-to-month, 1-mo free trial ([businessgenieapp.com/pricing](https://www.businessgenieapp.com/pricing)) | Dedicated septic page; claims **180+ septic companies**, tank records, disposal tracking; QB one-way sync; Calendly-demo sales ([septic page](https://www.businessgenieapp.com/industries/septic-service)) | Multi-industry FSM larping vertical; user-tier ladder recreates seat math PumpRun kills |
| **Smart Service** | Quote-only; third-party ~$49 base + per-user, annual ([itqlick.com](https://www.itqlick.com/smart-service/pricing), [saasworthy: quotation-based](https://www.saasworthy.com/product/smart-service/pricing)) | **QuickBooks add-on** (not standalone); surprisingly deep septic language — lid access, sludge measurements, real-estate inspection workflows ([smartservice.com/industry/septic-tank-service-software](https://www.smartservice.com/industry/septic-tank-service-software)) | The QB Desktop incumbent's answer; requires QB license; no compliance filing story; legacy UX |
| **FieldPulse** (Dallas, TX) | Quote-only, per-seat incl. limited field seats ([dynoroute Aug 2026](https://dynoroute.com/septic-software/blog/best-septic-pumping-software)); GetApp **4.6/468 reviews** ([getapp](https://www.getapp.za.com/software/2084416/pumpdocket)) | Generic FSM with a septic solutions page — scheduling/estimates/inventory; zero manifest/trip-ticket language ([fieldpulse.com/solutions/septic](https://www.fieldpulse.com/solutions/septic)) | Strongest review base of any fringe player; "78% YoY revenue growth" marketing; septic is 1 of 16 industries in nav |
| **SeptiBase** | **$79 solo / $149 crew (≤4 techs) / $249 company**, 14-day trial ([septibase.com/compare](https://septibase.com/compare)) | Septic-native startup; growth tools (win-back campaigns, review automation); CSV import | Another 2026-vintage PumpRun-shaped entrant; competes on price from below |
| **LooNexus** | **$30–50/user/mo** published ([loonexus.com/compare](https://loonexus.com/compare)) | AI-first porta/septic; DOT + septage paperwork angle; "manifests file themselves" | Portables-first; AI positioning overlaps nothing PumpRun sells |
| **QuoteIQ** | **$29.99/mo** Essentials ([myquoteiq.com](https://myquoteiq.com/pricing/essentials/)) | Generalist ranked "#1 for septic" by its own co-founder's blog ([cleansavannah disclosure](https://www.cleansavannah.com/post/best-septic-service-software-2026)) | Price floor noise; no septic semantics; biased rankings pollute buyer research |
| **GetRouteHouse** | Not published (found via Reddit) | Septic-native startup; truck-size-aware routing, GPS lid-location marking ([r/septictanks mention](https://www.reddit.com/r/septictanks/comments/1o0bwm4/septic_service_business_looking_for_a/)) | Evidence the long tail keeps spawning; lid-GPS is a feature worth stealing |
| **Others** | — | SanMan (portables), Orderry ($39–199+, 0 septic evidence — [dynoroute](https://dynoroute.com/septic-software/blog/best-septic-pumping-software)), Successware (quote-only), PumperSoftware.com | Edge is crowded enough that generic "septic software" SEO no longer converts without specificity |

---

## Cross-Cutting Synthesis — Vertical Moat Thickness

### Ranking (re: defense against PumpRun at $499 flat, 1–10 trucks)
| Rank | Vendor | Dominant moat | Thickness | Does it stop PumpRun? |
|---|---|---|---|---|
| 1 | Tank Track | Pumper Nation community goodwill + 13yr brand + free white-glove migration | **MEDIUM** | Slows adoption via peer recommendation; loses on product (browser-only, per-truck price at 4+) and just hiked prices 20% |
| 2 | ServiceCore | Industry-insider staff, benchmark data gravity, lead-gen tools, PE capital | **HIGH but aimed up-market** | Irrelevant below ~8 trucks; annual contract + 6–12wk onboarding repels exactly PumpRun's buyer |
| 3 | PumpDocket | Positioning parity + claimed 50-state profiles | **LOW (today)** | Doesn't block PumpRun — but defines the feature table buyers will compare against |
| 4 | Smart Service | QuickBooks Desktop install-base gravity | **MEDIUM-NARROW** | Owns the QB-Desktop shop; irrelevant to everyone else |
| 5 | Fringe (BG/SeptiBase/LooNexus/QuoteIQ et al.) | Price floors + SEO noise | **THIN** | Compresses perceived category value; none can serve compliance depth |

### Where the real moats actually live (brand / data gravity / compliance database)
1. **Brand = community, not ads.** The only durable brand asset in this vertical is peer recommendation inside Pumper Nation and r/septictanks. Tank Track holds it; ServiceCore rents an adjacent version (ambassadors, ToiletTalk); PumpDocket is buying it with content velocity. PumpRun's cheapest path is comparison-content SEO + verifiable customer references, NOT paid presence in the FB group before there's a testimonial bench.
2. **Data gravity barely exists yet.** ServiceCore's benchmark report is the sole aggregate-data flywheel; Tank Track publishes vanity gallons-pumped counters; nobody owns the tank-history ledger across shops. First mover to make **tank history portable and valuable** (transfer on sale of a route, drop-test history attached to parcels) builds the moat Part I said ServiceTitan fears — at vertical scale.
3. **The compliance database is still open ground — town-by-town.** Verified reality as of Aug 2026: Tank Track ships **TX/OH manifests** (FL promised and missed — Reddit); PumpDocket ships **cited jurisdiction profiles** with an explicit "we don't guarantee compliance" disclaimer; ServiceCore has **no advertised septage filing workflow**; fringe players have none. Nobody maintains named-town filing rules, deadline clocks, or board-formatted PDF outputs as a maintained dataset. That is PumpRun's defensible layer — provided it's maintained like a dataset (change-log per jurisdiction, effective dates), not written like marketing copy the way PumpDocket's citations are.

### Honest price-position warning (profit > everything)
PumpRun's $499 flat is **not the low-price option in this vertical**:
- vs **Tank Track**: cheaper from truck #4 ($630) — but Tank Track wins at 1–3 trucks ($180–480).
- vs **PumpDocket**: PumpDocket Team is **cheaper at every count** ($230 intro / $329 standard for 4–10 trucks).
- vs **ServiceCore/fringe**: PumpRun wins on predictability alone.
Therefore the $499 pitch against verticals must lead with **compliance depth + offline completion + flat predictability**, never with price — except against Tank Track at 4+ trucks and post-hike quotes, where "lock $499 flat while they just raised yours 20%" is a clean, evidenced kill shot.

### Consolidated vertical wedge checklist
1. **Anti-contract, anti-onboarding** vs ServiceCore: "live tomorrow, cancel anytime" against their own published 6–12 weeks + annual contract.
2. **Rate-lock counterattack** vs Tank Track: their $149→$180 hike is weeks old and third-party-documented; target their 4+-truck accounts first (where per-truck math already exceeds $499).
3. **Out-comply PumpDocket, don't out-cheap them**: maintain jurisdiction profiles as living data (effective dates, filing clocks, receipt PDFs) vs their cited-links-with-disclaimer approach; match unlimited users and month-to-month so those aren't differentiators.
4. **Own the ledger**: tank-history portability + drop-test records as the graduation-proof asset no incumbent treats as data.
5. **Community patience**: earn Pumper Nation presence through customer advocates; never advertise there first.
6. **Reference density beats review counts**: the entire vertical's third-party review base is ~520 reviews combined (ServiceCore 51, FieldPulse 468, Tank Track 0, PumpDocket 0) — a dozen named, callable septic customers outranks everyone.

---

## Source Log — Part II (fetches/searches, Aug 22, 2026)
- pumpdocket.com/ + /pricing (fetched live: $99/$230/$454 intro, $139/$329/$649 standard, 75-customer Starter cap, unlimited users, TCEQ disclaimer, Steady Grove LLC)
- tank-track.com/ + /request-demo (fetched live: $180/$150 per truck, 300+ operators, 45 states + 3 CA provinces, Pumper Nation #1 claim, no-trial/60-day-MBG, schema stale at $149/$125)
- servicecore.com/pricing/ (fetched live: quote-only, Start/Pro plans, annual contract FAQ, 6–12 week onboarding FAQ, 556K units/3.5M jobs/$400M stats, US+Canada)
- reddit.com/r/septictanks/comments/1o0bwm4 (Tank Track FL-manifest failure thread + CEO reply; ServiceCore and GetRouteHouse mentions)
- pumpdocket.com/resources/septic-software-comparison (competitor-published but source-linked: founded dates, contract terms, TX/OH manifest scope, QB journal-entries detail, Mainsail $54M)
- dynoroute.com/septic-software/blog/best-septic-pumping-software (Aug 19, 2026 independent verification: Tank Track $180/$150 + zero Capterra reviews; FieldPulse/Successware quote-only; Orderry 36 reviews/no septic evidence)
- guideflow.com/blog/septic-pumping-software (Jul 21, 2026 snapshot: Tank Track still $149/$125 — dates the price hike)
- cleansavannah.com/post/best-septic-service-software-2026 (Aug 2026 roundup; author discloses QuoteIQ co-founder bias; Tank Track signup-calculator inconsistency note)
- capterra.com/p/158918/ServiceCore/reviews/ (+ regional mirrors: 4.0/51 reviews)
- getapp.za.com/software/2084416/pumpdocket (0 reviews; FieldPulse 4.6/468 cross-reference)
- makerstack.co/reviews/servicecore-review (declines to invent customer count; per-truck model analysis)
- businessgenieapp.com/pricing + /industries/septic-service (fetched live: $50–$350 user tiers, 180+ septic companies claim, one-way QBO)
- smartservice.com/industry/septic-tank-service-software (QuickBooks add-on architecture, sludge/lid-access feature depth); itqlick.com + saasworthy.com (quote-based/third-party ~$49 base + per-user)
- fieldpulse.com/solutions/septic (generic FSM septic page; no manifest language; 78% YoY claim)
- septibase.com/compare + /blog/best-septic-business-software ($79/$149/$249 tiers; independent confirmation of ServiceCore enterprise pricing shape)
- loonexus.com/compare ($30–50/user AI-first fringe positioning; SanMan reference)
- pumper.com Oct 2015 product listing (Tank Track longevity since ≥2013)
