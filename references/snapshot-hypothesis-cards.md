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

## HC-05 — Serial-dependence regime via variance ratio

**Research motif.** A variance ratio measures whether multi-bar return variance is consistent with uncorrelated increments. Intraday work links serial dependence and volatility, but also warns that high-frequency inference is fragile and regime-dependent.[5][6]

### Observable inputs

- Mid-price only for state measurement, resampled by a pre-registered regular clock or valid-bar count.
- Log or arithmetic returns at one fixed base interval; overlapping variance ratios at a fixed small set such as 2 and 4 bars.
- A prior-only volatility baseline for classifying the current variance-ratio state.

### Event definition

After a pre-defined local price displacement, classify the prior return path as `VR_persistent`, `VR_reverting`, or `VR_indeterminate` using development-frozen bands around the null. Test whether the **next executable path** differs by class. The card does not assume which sign wins.

### Null / matched control

Same symbol/date/time bucket, displacement direction and size, with the same entry convention but a different variance-ratio class; where possible, pair `VR_persistent` against `VR_indeterminate` rather than a raw no-signal sample.

### Falsifier

Reject if the class is unstable under one adjacent resampling interval, lacks enough independent dates, or loses effect after conservative touch-side execution. A result that exists only at one selected ratio / interval is also rejected.

### Strategy conversion gate

Convert only the surviving directional resolution into one frozen rule: next valid touch entry, absolute TP, absolute SL and no normal time exit. Variance ratio is a regime gate, not a standalone long/short command.

### Source boundary

Bianco & Renò use intraday variance-ratio/serial-correlation measures with transaction data over thousands of dates.[5] Andersen et al. explicitly caution that conventional variance-ratio inference can be misleading at high frequency.[6] This card therefore uses the statistic as a coarse, robustness-tested classifier—not a significance claim from ~40 dates.

---

## HC-06 — Volatility surprise or compression/expansion as a path regime

**Research motif.** Volatility is persistent and its unexpected component can relate differently to intraday serial dependence than its predictable component.[5] With a short sample, use a transparent prior-window proxy rather than a high-parameter volatility model.

### Observable inputs

- Fixed-interval returns derived from mid-price for state description.
- `RV_short`: sum of squared past returns over one fixed short window.
- `RV_base`: strictly prior expanding/rolling baseline at the same symbol/date/time bucket.
- `vol_state`: compression, ordinary, or expansion from a development-frozen ratio band.

### Event definition

At a pre-defined price-path event—such as first range exit or standardized displacement—record `vol_state` without observing any later bar. Test whether the forward touch-side outcome differs between compression and expansion states.

### Null / matched control

Same symbol/date/time and same event geometry, but replace the tested `vol_state` with ordinary volatility. Do not compare a high-volatility morning move with an unrelated quiet midday move.

### Falsifier

Reject if the result is solely an intraday time-of-day effect, vanishes after a modest alternative prior-window length, or has no executable excess over the ordinary-volatility control.

### Strategy conversion gate

Only a stable state/event interaction can freeze into a strategy. Volatility may set a no-trade condition or scale a pre-declared absolute bracket only if bracket scaling is selected during development and held identical for control/OOS. No volatility-targeted leverage is implied.

### Source boundary

The observed price path supplies only realized, past-window variation; it does not establish news, volume, participant behaviour or a volatility forecast. The literature motivates testing regime interactions, not assuming a directional edge.[5]

---

## HC-07 — Trend slope persistence versus slope decay

**Research motif.** Slope summarizes the first-order geometry of a local price path. Intraday momentum and reversal effects are documented in some instruments and time segments, but are not universal and depend on the formation/holding setting.[7][8]

### Observable inputs

- A fixed number of past valid mid-price bars, detrended only by the window start or expressed in ticks.
- Ordinary least-squares slope, slope t-statistic or fit quality; all windows and thresholds fixed before selection.
- A scale normalizer from strictly prior realized variation, so one symbol's price level does not dominate another's.

### Event definition

At the first crossing of a pre-registered standardized slope magnitude, classify the path as `persistent_candidate` only when slope has held the same sign across two non-overlapping past subwindows; otherwise classify it as `slope_decay_candidate`. Test the next touch-side move, not the in-window move used to create the class.

### Null / matched control

Same symbol/date/time, current displacement and realized-volatility bucket, but remove the two-subwindow persistence condition. The control makes clear whether slope persistence adds beyond “price already moved.”

### Falsifier

Reject if slope direction merely restates the current displacement, if the effect disappears after excluding the highest-volatility date, or if long/short symmetry is absent without a pre-stated market-structure reason.

### Strategy conversion gate

The agent may promote either persistence **or** decay, never both post hoc. It must select entry at the next valid touch and freeze an absolute TP/SL before frozen OOS; no trailing-stop or time-exit rescue is allowed.

### Source boundary

The card does not treat a regression slope as a factor. It tests whether a carefully defined local geometry has incremental executable outcome over a matched current-displacement control. Intraday time-series momentum evidence motivates the question, not the answer.[7][8]

---

## HC-08 — Local-regression residual and curvature transition

**Research motif.** A local linear fit separates a smooth recent path from its latest residual; comparing the current slope with an earlier slope describes deceleration or acceleration. Curvature can flag geometric transitions, but reported evidence is asset- and model-specific.[9]

### Observable inputs

- Two strictly past, non-overlapping fixed windows of mid-price bars.
- Each window's fitted slope, fit quality and residual of the latest price from the older-window projection.
- A prior-only tick/volatility scale to express residual and slope change comparably.

### Event definition

After a qualifying price displacement, define one of three mutually exclusive states at the decision time: `linear_continuation` (same-sign slopes, small residual), `deceleration` (same-sign but smaller recent slope), or `inflection_candidate` (slope sign change with a material residual). The thresholds and hierarchy are written once in the ledger. Measure only the future touch-side resolution.

### Null / matched control

Same symbol/date/time, direction, displacement and volatility bucket, but use a different geometric state. Do not compare delayed entries with immediate controls: signal timestamp, entry timestamp and absolute bracket must match once a strategy is tested.

### Falsifier

Reject if a different adjacent window length reverses the conclusion, if residual/curvature only identify an already-completed move, or if the candidate needs a moving target, a wider stop or a new delay after OOS results.

### Strategy conversion gate

This card is especially vulnerable to recreating P33. It can proceed only if it is a genuinely distinct price-only geometry and wins the same-entry/same-bracket control. Any delayed entry must pass the existing residual R/R gate. Session boundary remains `SESSION_FORCED`; normal exits are fixed TP/SL only.

### Source boundary

Curvature is a descriptive second-order price statistic—not proof of a peak, a bubble, or participant intent. Published curvature studies often use different assets, horizons and model classes; use them only to motivate a falsifiable local-geometry test.[9]

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

[5] Bianco & Renò, *Unexpected volatility and intraday serial correlation* (2009), https://doi.org/10.1080/14697680802452050

[6] Andersen, Bollerslev & Diebold, *Variance-ratio Statistics and High-frequency Data* (2001), https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00326

[7] Liu, Lu, Li & Wang, *Time series momentum and reversal: Intraday information from realized semivariance* (2023), https://doi.org/10.1016/j.jempfin.2023.03.001

[8] Gao et al. intraday time-series momentum evidence is summarized with its formation/holding boundary in https://pmc.ncbi.nlm.nih.gov/articles/PMC10490999/

[9] Zhang et al., *Generalized visible curvature: An indicator for bubble identification and price trend prediction in cryptocurrencies* (2024), https://doi.org/10.1016/j.dss.2024.114309
