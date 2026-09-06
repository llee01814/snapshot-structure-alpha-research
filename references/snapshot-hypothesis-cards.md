# Snapshot hypothesis cards

These cards turn published LOB research **patterns** into bounded starting points for five-level quote snapshots. They are not a strategy library, not a claim that the owner's Taiwan data has an edge, and not permission to revive S21–S25 or P33.

## Use order

1. Complete the schema audit.
2. Select **at most one** card per mechanism family for the development ledger.
3. Run the card's descriptive event/control table before defining TP or SL.
4. Only a stable excess outcome converts into one frozen strategy card.

Each card intentionally excludes trade messages, participant classification, order identifiers and passive-fill modelling. A change across snapshots is only a quote-dynamics proxy.

---

## HC-01 — Liquidity-drought duration conditional on a price-path shock

**Research motif.** Liquidity-resilience studies treat the duration for a spread/depth stress condition to return below a threshold as an object of study, rather than assuming every shock has the same aftermath.[1][2]

### Observable inputs

- Valid `bid1`, `ask1`, top-5 displayed quantities, prior-only symbol × date spread/depth baselines.
- A past-only local mid-price range and displacement from it.
- `drought(t)`: spread above a prior percentile **or** top-5 total displayed depth below a prior percentile. The exact percentile is fixed before development evaluation.

### Event definition

At the first valid snapshot where both (a) an abnormal local-range displacement and (b) `drought(t)` hold, open one event. De-duplicate until both conditions have cleared. Measure the time / valid-bar count until drought clears, then describe touch-side price resolution after the clearance.

### Null / matched control

For the same symbol/date/time-of-day and same displacement direction/size bucket, match a price displacement whose visible quote state never entered `drought(t)`. The control has the same observation horizon; the only removal is the drought-state condition.

### Falsifier

Reject this card if drought duration has no stable relation to subsequent **executable** resolution versus its control, if sign reverses across development day blocks, or if events are concentrated in two dates.

### Strategy conversion gate

Only convert if the event table shows stable, control-excess touch-side move **after** a pre-defined clearing state. Then freeze direction, next-touch entry, one absolute TP, one absolute SL and the same bracket for the control. Do not infer why displayed liquidity changed.

### Source boundary

Danielsson et al. define threshold exceedance duration for liquidity droughts and model its duration using LOB state; their data has richer event information than this dataset, so this card uses only observable quote-state duration.[1] Lo & Hall study resilience with order-event data; this card retains only spread/depth state and never attributes a shock to a specific event type.[2]

---

## HC-02 — Near-touch versus deeper-book shape transition after displacement

**Research motif.** Empirical LOB work distinguishes depth at the best quote from depth behind it; the recovery profile may differ by level.[2]

### Observable inputs

- `L1_bid`, `L1_ask`, `L2_5_bid`, `L2_5_ask`; each quantity is normalized by a strictly prior symbol × date baseline.
- Prior-only local-range displacement and spread in ticks.
- Derived shape state: `near_touch_share = (L1_bid + L1_ask) / total_top5_depth`, plus bid/ask symmetry. These describe displayed shape only.

### Event definition

After a qualifying displacement, flag the first snapshot where near-touch share moves from an extreme prior-normalized state toward its ordinary range while L2–5 share remains extreme, or the symmetric inverse. The card asks whether this state transition alters the next touch-side path relative to the same displacement alone.

### Null / matched control

Same symbol/date/time bucket, direction and prior range/displacement bucket, but without the L1-versus-L2–5 transition. Match entry timestamp convention and forward measurement window.

### Falsifier

Reject if the shape transition does not improve effect size over control, only works on one side, or loses sign under one-tick-worse execution stress.

### Strategy conversion gate

A trade card is allowed only when the transition adds stable directional information beyond price displacement. Entry is the next valid touch price; TP/SL must be frozen before OOS. The transition itself is not a claim about refill, absorption or intent.

### Source boundary

Lo & Hall explicitly separate best-level and L2–5 depth dynamics.[2] Their identification uses a reconstructed event book, which this dataset lacks. The adaptation is therefore a state-shape comparison, not an order-event explanation.

---

## HC-03 — Range re-entry versus acceptance, conditioned on quote quality

**Research motif.** Rather than search raw depth ratios, first identify a price-path state and ask whether a contemporaneous visible liquidity condition changes its resolution. This follows the general distinction between static LOB state and the harder-to-observe dynamic flows.[3]

### Observable inputs

- A strictly prior local range, crossing direction, crossing magnitude in ticks, current spread, displayed top-5 total depth and quote age.
- No external price, trades, volume, order metadata or cross-asset data.

### Event definition

First valid exit from the prior range. At a pre-registered confirmation snapshot, classify only two point-in-time outcomes: still outside the range or back inside. Test whether a valid/narrow-spread/ordinary-depth state changes the **subsequent** touch-side probability of acceptance versus re-entry.

### Null / matched control

Same symbol/date/time bucket, exit direction and crossing magnitude, but remove the tested quote-quality condition while retaining identical entry time, absolute TP and absolute SL once a strategy is frozen.

### Falsifier

Reject if quote-quality does not add to the price-path-only control, if the result disappears after exclusion of ambiguous bracket paths, or if it requires retuning the confirmation delay.

### Strategy conversion gate

Only one of acceptance or re-entry may be selected after development. The selected rule must have an observable range, a single next-touch entry, fixed absolute bracket and a residual R/R gate if entry is delayed. There is no normal time exit; unfinished session positions are `SESSION_FORCED`.

### Source boundary

Bechler & Ludkovski show that static LOB metrics can modulate price dynamics but emphasize that their strongest findings use flows and executed-volume buckets unavailable here.[3] This card deliberately asks the weaker, testable incremental-state question.

---

## HC-04 — Spread-state-conditioned displacement resolution

**Research motif.** Spread is both an observable liquidity state and an execution burden. Forecasting research shows that predictive LOB performance must be separated from transaction practicality, and spread distributions create materially different book regimes.[4]

### Observable inputs

- Prior-normalized spread in ticks, local displacement/range state, quote validity and touch-side prices.
- Spread regime is set from development-only prior baselines and never recomputed using future dates.

### Event definition

At the first qualifying price displacement, compare the subsequent touch-side path conditional on a narrow/ordinary spread regime against an elevated-spread regime. This is a conditional event study, not a claim that wide spreads reveal informed trading.

### Null / matched control

Within the same symbol/date/time bucket and same displacement size/direction, control for the alternative spread regime. If a strategy is promoted, the control uses the identical signal timestamp, entry timestamp, absolute TP/SL and cost schedule.

### Falsifier

Reject if gross touch-side advantage is smaller than the entry/exit spread burden, if it vanishes with conservative quote-side execution, or if it is simply a time-of-day proxy after same-bucket matching.

### Strategy conversion gate

Only turn this into a rule if one spread regime has stable, control-excess gross touch-side P&L and enough dates/events. Spread is a no-trade gate or state condition; it must not be optimized jointly with TP/SL on the frozen OOS dates.

### Source boundary

Briola, Bartolucci & Aste document that microstructural conditions such as spread regimes matter for forecasting and separately evaluate the practicality of forecasts; their data spans years and includes message data, unlike the owner's ~40-day snapshot dataset.[4] This card uses spread only as a directly observable gate and demands executable validation.

---

## Explicit exclusions

- S21–S25 continuation/acceptance/void routes are rejected and cannot be renamed through these cards.
- P33 is rejected and cannot be re-opened through a different recovery threshold.
- No card may add a time stop, averaging down, position reversal, or an unequal control bracket.
- A positive discovery table is not a strategy; it earns only a pre-registered strategy test.

## Sources

[1] Danielsson, Panayi, Peters & Zigrand, *Market Resilience* (2018), https://researchonline.lse.ac.uk/id/eprint/118932/1/dp_78.pdf

[2] Lo & Hall, *Resiliency of the Limit Order Book* (2015), https://opus.lib.uts.edu.au/bitstream/10453/98964/1/Lo_Hall_Resiliency_of_the_limit_order_book_Accepted_Manuscript.pdf

[3] Bechler & Ludkovski, *Order Flows and Limit Order Book Resiliency on the Meso-Scale* (2017), https://arxiv.org/pdf/1708.02715

[4] Briola, Bartolucci & Aste, *Deep limit order book forecasting: a microstructural guide* (2025), https://pmc.ncbi.nlm.nih.gov/articles/PMC12315853/
