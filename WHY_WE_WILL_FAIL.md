# Why PumpRun Will Fail
*Kill-research, Aug 23 2026. Self-run, live-sourced. This is the case for the prosecution with numbers attached. Companion to WHY_NOT_ENOUGH.md (product gaps) — this file is about the venture dying, not the product being incomplete.*

---

## TL;DR — the four numbers that kill us

| Number | Reality | Our plan assumed |
|---|---|---|
| **Dials → meeting** | Tech/software cold-call conversion ≈ **0.95–1%**; Belkins 175k-dial study: **~370 dials per booked meeting** | 800 dials/mo → **24 demos** |
| **Solo-founder ceiling** | Only **11%** of solo micro-SaaS ever cross $10K MRR; **<1%** cross $50K MRR; median outcome is **$500 MRR** | $299×60 shops = $18K MRR base case |
| **Time-to-first-customer** | Winners: **median 34 days** from start to first dollar. Stalled: **141 days**. We are deep into build-mode with **0 prospects contacted** | "50 calls then pilots" — still unscheduled |
| **Churn floor** | SMB SaaS churn avg **4.5%/mo**; #1 cause (**32%**) = *customer business closed* — a floor no product fixes | 3%/mo churn in the model |

Every one of these is documented below. The product was never going to be the problem. The go-to-market arithmetic was.

---

## Failure mode #1 — The distribution math was fantasy (probability of killing us: HIGH)

Our acquisition model: *"40 dials/day × 20 days = 800 dials/mo → ~15% decision-maker connect = 120 conversations → 20% book demos = 24 demos → 25% close = ~6 customers/mo."*

What the actual 2025–2026 datasets say:

- **Tech/software cold-call conversion runs 0.95%** end-to-end (SalesHive, Prospeo/Focus Digital). At that rate, 800 dials/mo produces **~8 meetings**, not 24.
- Belkins' analysis of **175,000+ dials**: 9.9% connect → 58% conversations → **4.6% conversation→meeting** ⇒ **one meeting per ~370 dials**. That's **~2 meetings/month** on 800 dials.
- The best independent dataset (3.57M dials): **411 dials → 1 meeting**.
- Top-quartile teams hit 1 meeting per 15–20 *dials-to-connect* — but that's with verified mobile data, parallel dialers, and coaching. A solo founder with a purchased list is average, not top-quartile.

At 2 meetings/month × even a generous 25% close = **0.5 customers/month**, not 6. Equilibrium customer count collapses accordingly: at 3%/mo churn you need +3 closes/mo just to hold ~100; we'd be adding half a customer a month while SMB churn (4.5%) removes 4+. **The bucket leaks faster than we can fill it by dialing alone.** The entire bottoms-up model in MARKET_ANALYSIS.md §5 was off by roughly an order of magnitude on the binding constraint.

**Early warning:** fewer than 2 booked demos after the first 300 dials ⇒ model dead.
**What would have to be true:** warm-channel acquisition (Pumper community presence, referrals, comparison SEO) replacing ≥80% of cold volume before the cash/founder-time clock runs out.

## Failure mode #2 — We are executing the exact "stalled founder" pattern (probability: HIGH)

Micro-SaaS dataset (n=312): winners' median time-to-first-paying-customer = **34 days**; stalled products = **141 days**. The single strongest predictor in the dataset.

PumpRun status: multiple weeks of full-time building, 146 tests, nine feature cycles completed this session alone — and **zero customer conversations, zero dials, zero demo bookings, zero dollars**. We keep shipping because shipping is comfortable and measurable; selling is neither. This is not a hypothetical risk. It's the observed behavior of this very project, logged in plain sight:

- Session history: adversarial planning → market analysis → moat analysis → moat builds → gap research → fix validation → 8 fixes → Stripe → offline PWA → SMS. Every cycle ended with "next profit lever: dials." No cycle started them.
- The 312-product dataset calls this out directly: founders who spend months building before anyone pays "overwhelmingly stall out or quit."

**Early warning (already tripped):** any further feature cycle begun before the first prospect conversation.
**What would have to be true:** first 10 dials within 48 hours; first third-party human seeing the product inside a week.

## Failure mode #3 — The price war we re-anchored into is unwinnable (probability: MEDIUM-HIGH)

The competitive floor moved under us mid-build, and the newest intel makes it worse:

- **Tank Track shipped a native mobile app (April 2026)** — the "browser-only, no offline" weakness we were selling against is closing. Their public schema now advertises **$149 first truck / $125 additional** (down from the $180/$150 we validated), plus text+email reminders, online payments ("Get Paid Faster"), job checklists, and aggregateRating markup claiming 300 reviews at 5.0.
- **PumpDocket maintains a battery of maintained comparison pages** ("updated April 7 2026", "we fix errors within 48 hours") covering every buyer-research keyword we targeted — "Tank Track Alternative," "ServiceCore Alternative," three-way comparison. They are doing the Move-2 distribution play with a 6-month head start, at **$99/$230/$454 with a 30-day trial**.
- Guideflow's July 2026 round-up already crowns Tank Track "#1 septic-native" and PumpDocket "**best value for small pumping fleets**." PumpRun appears nowhere in category coverage.

We re-anchored to $299 against rivals at $99–$149 who now match or beat our differentiators (offline queue ✅ theirs, SMS ✅ theirs, invoicing+payments ✅ theirs, MA compliance layouts ✅ theirs). What remains uniquely ours — town-level filing clocks, route-sale ledger export, no-pumping notices — is real but unproven to buyers and invisible to researchers who never find us.

**Early warning:** any demo lost head-to-head where price was the stated reason; PumpDocket publishing an enhanced-MA filing workflow.
**What would have to be true:** a buyer segment that values the compliance *dataset* enough to pay 2–3× the $99 alternative — untested assumption, currently backed by zero evidence.

## Failure mode #4 — Churn math has a floor we can't engineer away (probability: MEDIUM)

SMB SaaS benchmarks 2026: **4.5%/mo average churn (42%/yr)**. Causes ranked:
1. **32% — the customer's business closed or owner exited.** Septic haulers skew old (majority ≤3-truck family businesses; succession is a known industry event). This churn exists regardless of our quality.
2. **28% — switched to cheaper/free competitor.** In a market where the incumbent set includes $99 flat, this fires every time we're 2× price.
3. 18% — too complex without IT support. Server-rendered Django helps, but "complexity churn" hits exactly when we hand over a multi-feature app.

Involuntary churn (failed payments, business closures) is **30–40% of SMB churn** — and we haven't built billing/dunning at all yet (Stripe Checkout exists; subscription management does not).

Model impact: at the SMB-average 4.5% churn (vs our modeled 3%), steady-state customers drop ~33%, turning the $250–350k base case into ~$170–230k before founder opportunity cost. Below 5K MRR, Stripe-data puts typical churn at **8–12%/mo** — at that rate the venture never leaves the treadmill regardless of sales.

**Early warning:** month-1 cohort retention below 70%; any cancel citing "went back to paper/PumpDocket."
**What would have to be true:** annual-prepay mix >30% at signup (cuts churn ~30% per the datasets) AND the tank-ledger switching cost materializing before month 3 of each cohort.

## Failure mode #5 — Solo ceiling + bus factor (probability: MEDIUM, terminal when hit)

Solo micro-SaaS outcomes: 24% reach $5K MRR, 11% reach $10K, **4%** reach $20K, **<1%** reach $50K. The ceiling isn't skill — it's operational load: support + infrastructure + development + marketing exceeding one human. Our target state (~$15K MRR at 60 shops) sits **inside** the zone where the dataset says one person starts drowning, and our buyers are phone-first, low-tech-tolerance owners whose support expectation is "you answer."

Compounding: New England seasonality means support load peaks in spring/fall rushes while revenue dips in winter — worst-case timing for a solo operator with no slack. One missed-busy-season of slow support = the referral network (Move 2's whole engine) hears about it.

**Early warning:** median support response >24h during any busy month.
**What would have to be true:** ruthless scope freeze + documentation-first support + annual prepay smoothing — all planned, none proven.

## Failure mode #6 — Regulatory pivot risk kills the wedge (probability: LOW-MEDIUM, severity: FATAL if hit)

The wedge is Massachusetts' decentralized 14-day Board-of-Health paper/email filing. If MassDEP ever centralizes septage tracking into eDEP-style e-filing (the way other states run manifest portals), the PDF packet becomes a print button and the dataset moat halves overnight. This is not paranoid: states modernize septage reporting continuously, and our own NH/ME seed rows already carry "operational target, not statute" disclaimers because those rules are softer than MA's. A single regulatory act converts our price-defense layer into table stakes.

**Early warning:** any MassDEP pilot program for electronic pumping-record submission.
**Mitigation:** multi-state dataset spread — but that collides with PumpDocket's existing 50-state cited profiles.

## Failure mode #7 — Liability tail in a word-of-mouth trade (probability: LOW, severity: SEVERE)

We auto-generate compliance paperwork for regulated filings. If a form variant is wrong for a town and a hauler eats a fine — or worse, a Title 5 dispute reaches court — the damage propagates through Pumper Nation and Facebook groups faster than any marketing can counter. PumpDocket defends itself with "we don't guarantee compliance" disclaimers; we inherited that posture but our copy leans harder on compliance value than theirs does. The better we sell the wedge, the bigger the liability when it hiccups.

**Early warning:** any customer-reported rejected form.
**Mitigation:** explicit "verify with your board" language everywhere (present), E&O insurance (absent), never auto-submitting on the customer's behalf (current design).

## Failure mode #8 — Opportunity-cost failure (probability: CERTAIN if modes 1–2 play out)

Even the success case is modest: solo-realistic capture is $270–600k ARR at ~90% margin, taking 30–36 months, unfundable by design (~$27M category ceiling). Against a founder-market salary of $120–180k/yr plus equity elsewhere, the realistic expected value of 3 years here is comparable to employment with none of the downside protection. The 312-product dataset's blunt framing applies: 70% of micro-SaaS never breaks $500/mo, and the ones who write about their numbers are the survivors. We planned against the highlight reel once already (the original 6-closes/month model).

---

## The compounding scenario

These modes interact. The likely death sequence:

1. Weeks N+1..N+2: dials finally start → 2 meetings/month reality vs 24 planned (#1).
2. The two meetings see a good product but meet $299 vs PumpDocket's $99-with-trial → both stall (#3).
3. Founder responds the way this session trained him: ships more features instead of fixing distribution (#2 compounds).
4. Cash/founder-time runway burns; no cohort exists to measure churn (#4 moot).
5. Wind-down at month 4–6 with a well-tested codebase and zero market learning worth anything.

That is the modal outcome on current behavior. Not because the product is bad — it's genuinely decent now — but because **the constraint was never code.**

## What would flip the verdict (falsifiable, dated)

| By | Gate | Pass condition |
|---|---|---|
| Day 14 from first dial | Pipeline | ≥150 dials, ≥8 live conversations, ≥2 demos booked |
| Day 30 | Close signal | ≥1 paid pilot at $299 (or 3 signed LOIs) |
| Day 45 | Drop-test | ≥10% of demos convert at $299; else kill or pivot to compliance-dataset licensing to rival platforms' customers |
| Month 3 | Cohort health | Month-1 retention ≥70%; annual-prepay share ≥25% |
| Month 6 | Treadmill check | Net new logos > 0 two consecutive months at ≥$5K MRR |

If gates 1–2 fail, the honest move is execution of the pre-committed wind-down — selling the compliance-dataset asset or the codebase — rather than another feature cycle. This document exists so that decision is pre-made and cannot be argued away later.

## Source log
- cognism.com/reports/cold-calling-report-2026 (200k calls: 2.7% avg success, 11.3% elite) · saleshive.com B2B benchmarks 2025-26 (tech 0.95%, ~40 dials/meeting avg) · prospeo.io cold-calling stats (tech ~105 calls/sale; Focus Digital table) · belkins.io/blog/cold-calling-benchmarks (175k dials: 9.9% connect, 4.6% convo→meeting ⇒ ~370 dials/meeting) · coldcallbenchmarks.com (3.57M dials: 411→1)
- saasopportunities.com 312-micro-SaaS study (solo ceilings 11%/$10K-MRR, <1%/$50K; TTC 34d vs 141d; churn<5% divides winners; vertical B2B wins 2×) · groundworkblog.com micro-SaaS economics (median $500 MRR; 70% <$500; 18% sustainability zone) · retentioncheck.com SMB churn 4.5% (32% closures, 28% cheaper-switch) · savemrr.co Stripe churn bands (<$5K MRR: 8–12%/mo) · saasranger.com (involuntary 20–40%) · groundworkblog.com churn guide (annual-prepay −38% median churn; SaaS Capital GRR floors)
- fieldservicesoftware.io (small-business FSM adoption 29% and rising — the market is reachable, which cuts both ways)
- pumpdocket.com comparison suite (maintained Apr 2026, 48h-fix policy, $99/$230/$454, 30d trial, offline+SMS parity claims) · tank-track.com homepage+schema ($149/$125, payments-by-tech review, 300-review rating markup) · marlvel.ai Tank Track intel (native app launched Apr 2026; pivoting to offline-first messaging) · guideflow.com July 2026 roundup (category coverage excludes us; PD "best value")
