# PumpRun — Market & Competition Analysis
*Solo-founder SaaS for septic haulers (1–10 trucks). CSV import → nearest-neighbor route → tap-complete → PDF pump-out report → due-date CRM. Anchor $499/mo flat, $299 drop-test. Profit > everything.*
*Compiled Aug 2026 from live web sources; all pricing verified against vendor pages or flagged as third-party-reported.*

---

## 1. Category Sizing

**The service market is real, growing, and brutally fragmented:**

| Metric | Figure | Source |
|---|---|---|
| US septic, drain & sewer cleaning revenue | **$8.1B (2025) → $8.7B (2026)**, +4.3% YoY, 6.7% CAGR 2020–25 | IBISWorld |
| Businesses in that category | **~7,300–7,717** | IBISWorld |
| Narrower NAICS 562991 (septic tanks + portables) | $6.7B (2025), **3,609 companies**, top-4 share only **11.4%**, avg $1.8M revenue/location | Kentley Insights |
| US households on septic | **>1 in 5 (~20–21%)**, 22–25M systems, 60M+ people served | EPA |
| Pump cadence | Every 3–5 years (EPA); "typically necessary at least once every three years" | EPA / 310 CMR 15.351 |
| Avg residential pump-out ticket | $300–600, median ~$400–450 | Angi/industry surveys |

**Read-through for a software seller:** ~$8B service revenue across ~4–7k operators means the *software* TAM is small by VC standards but fine for a solo founder. If ~65% of the ~7,300 firms run 1–10 trucks (assumption — no public fleet-size breakdown exists), that's **~4,500 target shops**. At $499/mo the theoretical ceiling is **~$27M ARR**; a realistic solo capture of 1–2% over 3 years is **45–100 customers = $270k–600k ARR**. This is a lifestyle-business-sized prize, not a fundable one — which is consistent with why incumbents ignore it.

**Regulatory tailwind (the actual wedge):** Massachusetts 310 CMR 15.351 requires the *pumper* to note system condition on a DEP-approved pumping form and **submit it to the local Approving Authority (Board of Health) within 14 days of every pump-out**, and states pumping is "typically necessary at least once every three years." Towns layer stricter rules on top (e.g., Leominster validates Title 5 inspections for 3 years only with documented annual pumping). Florida counties mandate 3–5 year pump-outs with health-department records. This makes recurring-due-date tracking + board-ready PDFs a *compliance* function, not a convenience.

---

## 2. Direct Competitors

### Generic field-service platforms (all market to septic; none are septic-native)

| | Pricing model | Entry price (verified) | Realistic cost, 3-truck shop (owner + 2 drivers + office ≈ 4–5 users) | Contract |
|---|---|---|---|---|
| **ServiceTitan** | Per technician/mo | **Quote-only.** Third-party reports: $245–$398/tech/mo + $5k–$50k implementation | ~$980–$1,990/mo yr 1 (+impl fee) | 12-mo min, painful exit (documented ETFs $24k–$46k in BBB complaints) |
| **Housecall Pro** | Tiered per-seat | Basic **$59/mo** annual ($79 monthly, 1 user); Essentials **$149** ($189, 5 users, +$100/extra user); Max **$299** ($329, 8 users, +$75/user). Route optimization only on Max | $149–189/mo | Month-to-month |
| **Jobber** | Tiered seat bundles | Core ~$29–49 (1 user), Connect ~$129–169 (5 users), Grow ~$249–349 (10 users), Plus ~$449–599 (15 users); +$29/extra user. *(jobber.com blocked direct fetch; ranges from 6 third-party trackers that disagree)* | $129–169/mo | Month-to-month |
| **Workiz** | Tiered, partially opaque | Lite free (20 jobs/mo cap); paid tiers **not consistently published** — reports range $65 Starter (1–2 users) to ~$229–270 Standard/Pro (5 users); extra users ~$40–65 | ~$229+/mo est. | Month-to-month |
| **Service Fusion** | **Flat, unlimited users** | Starter **$208/mo** annual ($245 monthly); Plus $325/$382; Pro $533/$627 | $208–245/mo | Month-to-month |

### Septic-vertical specialists (the real competition)

| | Pricing (verified) | Notes |
|---|---|---|
| **ServiceCore** | **Not disclosed — demo-only quote.** Two plans (Start, Pro), billed monthly on an **annual contract**; onboarding takes **6–12 weeks**; FAQ says "best for operators that have multiple trucks" | The vertical's mindshare leader (portables/septic/grease/dumpster). Deliberately ignores tiny shops. |
| **Tank Track** | **$180/mo first truck + $150/truck after** (10% off annual; schema markup shows $149/$125 annual rates). Unlimited users/tanks/storage. No contract. Free data import + 1–4 live training sessions | 300+ operators, 45 states, strong Pumper-community reputation. Auto-generates waste manifest reports. NH-based; multiple MA customer testimonials. |
| **PumpDocket** | **$99/mo flat, everything included**, month-to-month, no contracts, 30-day trial | Small startup explicitly positioned as the cheap ServiceCore alternative; advertises "50-state regulatory profiles" and trip tickets. |
| Others in the fringe | Business Genie, Bella FSM, Smart Service, FieldPulse, Home Service One — all have septic landing pages; pricing mostly demo-gated | Proof the vertical is crowded at the edges, not empty. |

**The uncomfortable headline:** the task premise "incumbents won't chase $499 flat" is **half wrong**. Generic FSM platforms indeed won't build Title 5 form logic or town-by-town Board of Health rules — the category is too small for their ARPU models. But two septic-native startups already sell compliance-aware dispatch at **$99–$480/mo**. PumpRun's true competitive set is Tank Track and PumpDocket, not ServiceTitan.

---

## 3. Feature Matrix vs. Wedge

| Capability | ServiceTitan | HCP | Jobber | Workiz | Service Fusion | ServiceCore | Tank Track | PumpDocket | **PumpRun** |
|---|---|---|---|---|---|---|---|---|---|
| Routing | ✔ (dispatch) | Max tier only | ✔ basic | ✔ | ✔ | ✔ optimized | ✔ capacity-aware | ✔ | ✔ NN (simple, fast) |
| CRM / recurring due dates | ✔ memberships | ✔ plans | ✔ | ✔ | ✔ | ✔ | ✔ auto reminders | ✔ | ✔ statutory-cycle core |
| Compliance PDF / manifests | generic docs | generic invoices | generic | generic | custom docs add-on | ✔ pro reports | ✔ waste manifests | ✔ trip tickets, 50-state | ✔ **health-board-formatted pump-out report** |
| Statutory filing workflow (14-day BOH form, MA) | ✗ | ✗ | ✗ | ✗ | ✗ | partial | partial | partial (state profiles) | ✔ **purpose-built** |
| Offline field completion | mobile app (online-first) | "offline viewing" only | limited | partial | app | app | app | claims offline closeout | ✔ **offline tap-complete** |
| CSV import day-one | migration project ($5k+) | manual | manual | manual | onboarding | **6–12 weeks** | free white-glove import | self-serve | ✔ self-serve, minutes |
| Transparent pricing | ✗ | ✔ | ~ | ✗ | ✔ | ✗ | ✔ | ✔ | ✔ |
| Price for 3-truck shop | ~$1k–2k/mo | $149–189 | $129–169 | ~$229 | $208–245 | quote | **$480** | **$99** | **$499** |

### Where PumpRun genuinely wins
1. **Statutory due dates as the product spine.** Nobody treats the 310 CMR 15.351 14-day filing clock or town-level pumping bylaws as first-class data. A CRM where every tank has a legal next-due date and an auto-generated, board-formatted PDF is a defensible framing — for now.
2. **Offline tap-complete.** Pioneer Valley routes include dead zones; Housecall Pro's own pricing page admits only "offline viewing." Rural completion without signal is a real daily pain.
3. **Flat price predictability at ≥3 trucks.** $499 beats Tank Track at 4+ trucks ($630+), beats every per-tech model at any size, and beats Service Fusion's unlimited-user tiers on septic depth.
4. **Day-one CSV import.** The status quo competitor is a spreadsheet and a route book. Importing it in minutes vs ServiceCore's 6–12 week onboarding is a real sales moment.

### Where PumpRun loses (be honest)
1. **Price vs. vertical rivals.** PumpDocket at $99 does dispatch + regulatory trip tickets month-to-month. Tank Track at $180/truck includes free migration, manifests, and has 300+ reference customers and community goodwill PumpRun lacks. At 1–2 trucks (likely the majority of the 4,500-shop base), PumpRun is 2–5x more expensive than both.
2. **No installed base or brand.** Tank Track is recommended in Pumper forums; PumpRun has 8 demo customers.
3. **Thin technical moat.** NN routing, reportlab PDFs, and a Django CRUD app are replicable in weeks by any competitor who notices. The moat is distribution speed + regional compliance content (town-by-town BOH rule database), not code.
4. **Generic FSMs are "good enough" cheaper.** A 2-truck shop can run Jobber Connect at $129 and keep pumping records in a spreadsheet. Beating "good enough" costs selling effort, not just features.

---

## 4. The $499 Flat Wedge — Quantified

Per-tech/per-seat pricing punishes exactly the shops PumpRun targets:

| Shop profile | ServiceTitan (reported) | HCP Essentials | Jobber Connect | Tank Track | **PumpRun flat** |
|---|---|---|---|---|---|
| 1 truck, owner-only | ~$245–398 | $59–79 (Basic) | $29–49 (Core) | **$180** | $499 ← loses |
| 3 trucks, 4 users | ~$980–1,590 | $149–189 | $129–169 | $480 | **$499 ≈ parity** |
| 5 trucks, 6 users | ~$1,225–1,990 | $349+ ($149+$100 user) | $187+ ($129+$29×2) | $780 | **$499 wins** |
| 8 trucks, 9 users | ~$1,960–3,180 | $549+ | $274+ | $1,380 | **$499 wins big** |

- The flat price is a **hiring insurance policy**: adding driver #4 doesn't raise the bill. Per-tech models tax growth precisely when margins are thinnest.
- But the wedge only bites at **≥3 trucks**. Below that, Tank Track/PumpDocket/Jobber win on price and PumpRun's pitch collapses to "compliance PDFs," which a $99 rival also claims. **The drop-test at $299 isn't optional — it's the real PMF probe for the 1–2-truck majority.**
- Why incumbents won't follow down-market: ServiceTitan's model needs ACVs north of $25k (sales-led, 12-mo contracts, $5k+ implementations); HCP/Jobber optimize for 200k+ pros across dozens of trades and won't maintain MA Title 5 form logic for maybe 400 MA shops; ServiceCore explicitly targets multi-truck operators with annual contracts. The vertical-specific compliance layer for one state is beneath all of them — but not beneath Tank Track or PumpDocket, who are already there.

---

## 5. Risks, Moat, Bottoms-Up Math

### Risks (ranked)
1. **Underpriced vertical rivals (existential).** PumpDocket at $99 and Tank Track at $180/truck already occupy the wedge. If either adds MA BOH-formatted PDFs properly, PumpRun's differentiation shrinks to UI taste.
2. **TAM ceiling.** Even perfect execution caps around ~$27M ARR category-wide; solo-realistic is $300–600k. Fine for profit, worthless for fundraising — don't raise.
3. **Churn from both directions.** Customers graduating past 10 trucks leave for ServiceCore/ServiceTitan; 1-truck customers downgrade to paper or PumpDocket. Expect bimodal churn.
4. **Seasonality.** New England pumping demand peaks spring/fall; winter slowdowns stress $499/mo commitments.
5. **Founder bus factor.** Solo support + sales + dev. One bad winter of unanswered support calls = churn spiral.
6. **Regulatory dependence cuts both ways.** If MA ever centralizes e-filing (state portal), the PDF wedge narrows.

### Moat (thin, be realistic)
The only durable asset is **accumulated compliance data gravity**: years of per-town Board of Health form variants, filing deadlines, and each customer's tank history + due-date ledger. Switching costs are moderate (migrating 3,000 customer records with due dates hurts) but not high. Speed of regional distribution is the real moat — own Pioneer Valley, then New England, before anyone notices.

### Bottoms-up unit economics (cold-call acquisition)

**Acquisition engine (founder time is the only real cost):**
- 40 dials/day × 20 days = 800 dials/mo → ~15% decision-maker connect = 120 conversations → ~20% book demos = 24 demos → 25% close = **~6 new customers/mo optimistic, 3 conservative**
- Cash CAC: ~$100–150 (list data, dialer, email tool). Loaded CAC valuing founder at $50/hr × ~20 hrs/close ≈ **$1,000–1,250 opportunity cost**
- Payback: **<1 month** at $499. LTV:CAC >10x if churn holds — the binding constraint is founder hours, never economics.

**Retention assumption:** SMB FSM logo churn 3%/mo (industry norm 2–5%). Average lifetime ≈ 33 months → LTV ≈ $499 × 33 × 90% gross margin ≈ **$14,900**.

**Cost base:** hosting ~$50/mo, SMS/email ~$10/customer/mo, card fees ~$15/customer (push ACH), misc $200/mo. Fixed ≈ **$400/mo** → break-even at **1 customer**.

| Customers | MRR | Monthly net (≈90% GM − fixed) | Annualized pre-tax profit |
|---|---|---|---|
| 8 (today) | $3,992 | ~$3,190 | ~$38k |
| 25 | $12,475 | ~$10,830 | ~$130k |
| 50 | $24,950 | ~$22,055 | ~$265k |
| 100 (near ceiling of solo ops) | $49,900 | ~$44,510 | ~$534k |

At 3 closes/mo with 3%/mo churn, steady state settles near **~100 customers** (equilibrium where monthly adds = monthly losses) — i.e., **~$500k/yr profit is the realistic solo ceiling**; ~$250–350k is the base case within 30–36 months.

### Verdict
- **Kill criteria:** if the $299 drop-test converts <10% of demos, or churn exceeds 5%/mo after 6 months, the $499 thesis is dead — the market has spoken via Tank Track/PumpDocket pricing.
- **Sharpest move:** stop selling "field service software" and sell the **14-day Board of Health filing deadline** — a legally mandated document workflow no generic FSM touches and only one $99 startup half-covers. Anchor $499 for 3+ truck shops (where it beats Tank Track), let $299 prove whether 1–2 truck shops can be profitable to serve at all. They probably can't be at founder-time CAC — and that's fine: 60 three-to-eight-truck shops ≈ **$360k ARR at ~90% margin**, which is the whole game.

---

## Source Log (live fetches/searches, Aug 2026)
- IBISWorld industry page (OD4710): $8.7bn 2026, 7,717 businesses — ibisworld.com/united-states/industry/septic-drain-sewer-cleaning-services/4710
- Kentley Insights NAICS 562991: $6.7B, 3,609 companies, top-4 = 11.4% — kentleyinsights.com
- EPA About Septic Systems (>1 in 5 households) — epa.gov/septic/about-septic-systems
- 310 CMR 15.351 (pumping form filed w/ Approving Authority within 14 days; ~3-year cadence) — law.cornell.edu/regulations/massachusetts/310-CMR-15-351; mass.gov/septic-systems-title-5
- Leominster BOH (inspection validity tied to documented pumping) — leominster-ma.gov
- housecallpro.com/pricing (fetched): $59/$149/$299 annual tiers, seat add-ons, "offline viewing"
- servicefusion.com/pricing (fetched): $208/$325/$533 annual, unlimited users
- servicetitan.com/pricing (fetched): quote-only, per-technician packages; reported $245–$398/tech + $5k–50k impl via TrustRadius/ITQlick/BBB-complaint compilations
- jobber.com/pricing (403 — ranges compiled from 6 third-party trackers, flagged as such)
- workiz.com (pricing page 404/non-public; figures from G2/SaaSworthy/fsmadvisor/serviceagent trackers, flagged as estimates)
- servicecore.com/pricing (fetched): no public pricing, annual contract, 6–12 wk onboarding
- tank-track.com (fetched): $180 first truck + $150/additional, unlimited users, no contract
- pumpdocket.com comparison pages (fetched): $99/mo flat, month-to-month, 50-state regulatory profiles
