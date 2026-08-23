# Why PumpRun Is Not Good Enough (Kill Research)
*Self-run live research, Aug 22 2026. Every claim sourced. This is the case for the prosecution — what actually kills the sale or churns the customer.*

**Verdict up front:** PumpRun today is a **compliance records tool wearing an FSM costume**. Buyers do not buy compliance records tools. They buy **"close-your-day loop" machines**: dispatch → field closeout → invoice same-day → money in bank. Every competitor's marketing converges on that exact loop because that is where the buyer's pain is. PumpRun has no invoicing, no payments, no QuickBooks, no customer communication, and its "offline tap-complete" claim is currently false. The moats we built are real but they defend a product the market hasn't asked to buy yet.

---

## 1. Deal-killers (buyer walks in the demo)

### 1.1 No invoicing, no payments — the loop never closes
PumpDocket's entire pitch is the "close-your-day loop": dispatch → closeout → **invoice same day → Stripe payment → QuickBooks export** (pumpdocket.com/resources/why-pumpdocket). SepticCycle: "Generate invoices in one click... Stripe Connect routes funds directly to your bank account." SepTechPro: techs collect card payments from their phone. Smart Service: closes into QuickBooks with disposal docs attached.

The industry data says this is THE lever: field payment at completion = 2–4 day collection vs 28 days paper mail (septicmind.com benchmarks). Payment cycle compression is the #1 measurable win owners cite (Elite Sanitation ServiceCore case study: auto-pay + batch billing was the headline outcome).

**PumpRun: captures gallons and disposal site… and stops.** No invoice, no price book, no payment capture, nothing to hand the bookkeeper. An owner testing PumpRun against any rival will feel this within one simulated workday.
**Severity: DEAL-KILLER.** $499/mo for half a loop cannot survive a side-by-side against $99–$230 full-loop rivals.

### 1.2 No QuickBooks integration or export
"Nearly every septic company already uses QuickBooks" (septictankhub.com). FieldEdge wins deals on two-way live sync; even PumpDocket Team ships one-way QB export; SepticCycle lists it as roadmap priority #1. Smart Service is literally *a QuickBooks add-on* as its positioning.
**PumpRun: zero accounting story.** The owner still re-keys every job at month end — which means PumpRun adds a system instead of replacing one.
**Severity: DEAL-KILLER** for any shop with >~50 jobs/month. (A CSV export of completed jobs would cover ~70% of the need cheaply; even that doesn't exist.)

### 1.3 "Offline tap-complete" is claimed but not true
Our compare pages sell offline completion as differentiator #2 (vs HCP's "offline viewing only"). Reality in code: server-rendered Django forms; no service worker, no local queue, no sync-on-reconnect. First dead-zone test on a Pioneer Valley route fails, and rural MA/VT/NH routes have dead zones daily. Meanwhile PumpDocket explicitly markets "data saves locally and syncs when reception returns."
Selling a feature we don't have is worse than not having it — it's a refund request waiting to happen.
**Severity: DEAL-KILLER if demoed in a dead zone; brand-killer regardless.**

### 1.4 The compliance wedge is real law but weak product-market fit
Verified: 310 CMR 15.351 requires the pumper to file a DEP-approved System Pumping Record with the Board of Health **within 14 days** (law.cornell.edu). Mendon BOH even requires a monthly "no pumping done" notice. BUT: filing is **paper/email to ~350 individual town boards**, each with its own form preference ("Other forms may be used, but information must be substantially the same"; towns like Hopkinton host their own Form 4 copies). MassDEP eDEP covers *permits*, not pumping records — there is no central digital intake.
So our PDF is genuinely useful — but it does not *file* anything. The hauler still prints/mails/emails per town. Our FilingReceipt model records intent, not submission. The wedge is a **worksheet**, not a workflow. And the buyer's willingness-to-pay anchors to workflow, not worksheets.
**Severity: BIG FRICTION** — the pitch must be reframed from "we file for you" (false) to "you never miss a 14-day clock, and here's the town-correct form prefilled" (true and still valuable).

---

## 2. Big frictions (churn drivers post-sale)

### 2.1 Customer reminders & notifications don't exist
The Reddit r/septictanks buyer thread (Oct 2025) describes the exact incumbent stack we're displacing: a basic tracker that generates due reports, then **humans stick labels on reminder postcards**. What they asked for next: scanning file cards, tank sketches, better reminders. Every competitor leads with automated SMS/email reminders (SepTechPro, SepticCycle 5 SMS templates, PumpDocket due-soon queue + SMS, Smart Service text campaigns). Reminder automation is also the retention engine: "the company that reminds them on schedule is the company that gets the job" (Smart Service).
**PumpRun: dashboard buckets exist, outreach does not.** The due-date CRM tells you who's overdue and then leaves the phone dialing to you.
**Severity: HIGH** — this is half the recurring-revenue promise of the category.

### 2.2 Tank-level context beats our customer-level model
PumpDocket's stated reason generic tools lose: "Generic tools track customers and jobs. They do not track **individual tanks**." Multiple tanks per property (septic + grease trap + pump chamber), effluent tee/filter condition, sludge/scum measurements (Form 4 literally asks condition + filter-cleaned), lid/access notes and photos per site.
Our TankEvent ledger groups by tank_key — good bones — but there is **one tank record per customer row**, no multi-tank-per-site, no photos, no access notes surfaced at dispatch, no sludge-depth fields.
**Severity: MEDIUM-HIGH** — commercial accounts (the higher-ticket segment) hit this first.

### 2.3 Dispatch board ≠ route page
Buyers expect a morning dispatch board: all trucks, drag-drop resequence, driver-on-the-way texts, midday insertions. We have a single-day checkbox picker + NN order — fine for 1 truck, no multi-truck concept anywhere (no Driver/Truck model at all). A 3-truck shop — our target — can't assign stops to trucks.
**Severity: MEDIUM** at 1–2 trucks, **deal-killer at 3+** — which is exactly the segment our pricing needs.

### 2.4 Seasonality + solo-founder support risk
New England pumping demand craters in winter (frozen ground); a $499/mo bill hitting in February invites churn conversations. And every support call lands on the founder who is also doing sales and code.
**Severity: MEDIUM** — mitigate via annual-prepay discount (cash now, churn buffer) and honest winter pause option rather than silent churn.

---

## 3. Competitive reality check (what changed since our analysis)

| Threat | New fact | Implication |
|---|---|---|
| **QuoteIQ Elite $299 flat** | Full FSM (route opt, job costing, self-scheduling, AI) at $299 — directly undercuts our $499 anchor while claiming "everything included" (myquoteiq.com ServiceTitan-alternative page) | Our flat-price advantage narrows to compliance depth only |
| **SepticCycle $149 flat unlimited** | Purpose-built septic: TCEQ/county exports, manifests, land-application logs, tank-per-property, Stripe, API/webhooks | At $149 with more septic depth than us, they're below both us AND PumpDocket |
| **PumpDocket Team $230** | Now includes 50-state profiles w/ cited sources, enhanced MA layout, QB export, SMS reminders, offline queue | Their "disclaims compliance" gap we documented is closing fast; our /compare/pumpdocket page ages badly |
| **ServiceCore ~$200/truck reported, Capterra 51 reviews 4.0** | Still annual+demo, but driver-app photo proof-of-service + real-time QBO sync are table stakes they already ship | Our "they can't serve small shops" holds, but our feature deficit vs them at parity price is embarrassing |

**Net:** the $499 anchor now sits ABOVE three credible flat-rate septic-native options ($99/$149/$230) plus a horizontal $299. Our earlier "wedge survives at ≥3 trucks" conclusion assumed Tank Track's $480 as the floor. That floor has collapsed to $99–$299.

---

## 4. What is actually good enough (the bar)

Synthesizing buyer language across sources, a 3-truck shop buys when the product:
1. Closes the day: complete → invoice → paid (Stripe link or card-on-file) → bookkeeper/QB export
2. Reminds: due-soon queue + SMS/email to customers automatically
3. Survives dead zones honestly (real offline queue)
4. Files: prefilled correct-town form + deadline clock + proof-of-filing log
5. Onboards in a day: CSV import (have), free trial, self-serve signup (missing — Django admin login-only)

We currently satisfy #4 partially and #5's import half. That's 1.5 of 5.

---

## 5. Profit-ranked fix list (do in this order)

| # | Move | Why first | Est. effort | Revenue impact |
|---|---|---|---|---|
| 1 | **Invoice + payment link per job** (price × gallons simple math, emailed/stripped-down Stripe link; cash/check marking ok pre-Stripe) | Converts tool from cost to cash-flow machine; the demo moment | 2–3 days | Makes $499 defensible; unblocks same-day-close pitch |
| 2 | **Fix or stop claiming offline** | Integrity + our own compare pages cite it | PWA service worker ≈ 1 wk, or reword pages in 1 hr | Prevents refund/churn trigger |
| 3 | **QB export (CSV) + bookkeeper report** | Table stakes; one-way CSV covers most shops | 1–2 days | Removes deal-killer #2 at low cost |
| 4 | **Due-soon email/SMS reminders** (email first — free via console backend now, SES later) | Retention engine of the whole category | 2–3 days | Directly attacks 3%/mo churn moat thesis |
| 5 | **Re-anchor price: $299 base (≤3 trucks) / $499 fleet (4+)** | Floor moved under us; $299 drop-test was already planned | Pricing page change | Matches PMF probe to market reality |
| 6 | **Multi-tank + photos + access notes** | Commercial accounts; Form 4 fields (condition, filter) | 1 wk | Unlocks higher-ticket segment |
| 7 | **Multi-truck assignment on dispatch board** | Needed for the exact 3–8 truck ICP | 1 wk | Required by our own pricing tier |
| 8 | Reframe compliance copy: "never miss the 14-day clock + prefilled town form," drop any "we file" implication | Truth-in-advertising; Mendon-style monthly notices could even be a generated artifact | Hours | Protects the one true wedge |

**Kill-switch update:** if after moves 1–4 a 10-demo smoke test still can't close ≥3 at $299 against PumpDocket/SepticCycle, the honest answer is that this market's software budget is already spoken for at $99–$230, and PumpRun should pivot to selling the compliance dataset + filing service *to those platforms' customers* (or wind down) rather than fight a four-way price war with no distribution.

---
### Source log (live fetches/searches Aug 22 2026)
- law.cornell.edu 310 CMR 15.351 (14-day filing duty) · mass.gov Title 5 forms (Form 4 PDF/DOC) · mendonma.gov BOH (14-day + monthly no-pumping notice) · inspectapedia Form 4 ("other forms may be used") · portal.laserfiche Hopkinton
- pumpdocket.com /resources/why-pumpdocket + homepage (close-your-day loop, tiers $99/$230/$454, offline queue, 50-state cited profiles, QB one-way export, SMS)
- septiccycle.com ($149 flat, Stripe Connect, TCEQ/county exports, tank-per-property, API/webhooks, QB "coming soon")
- septechpro.com (SMS reminders, mobile invoicing/payments, native QBO sync, size-based quote pricing)
- smartservice.com/septic (QB add-on positioning, reminder automation, sludge history on work orders)
- myquoteiq.com ServiceTitan-alternative + top-10 work-order posts (QuoteIQ $299 Elite; ServiceCore ~$200/truck reported; complaint patterns)
- saasrat.com/servicecore (Capterra 4.0/51, driver-app adoption risk, migration time, contract gotchas)
- rolloffamigo.com ServiceCore-alternative (small-hauler complaints: price, contracts, desktop-first)
- reddit r/septictanks 1o0bwm4 (incumbent stack = basic tracker + label postcards; asks for card scanning + reminders)
- septictankhub.com (QB universal, Jobber/HCP entry pricing, route fuel math)
- septicmind.com benchmarks (28d→4d payment cycle via field pay; avg tickets)
- pulserevops.com fee benchmarks (trip/disposal/after-hours fee structures = invoice line items buyers expect)
- krusersepticservice.com (real rate card incl. per-gallon overage — invoice modeling reference)
