# Research contract

## Minimum audit decisions

- `DATA_NOT_READY`: missing required field, unparseable timestamps, or unexplained session/gap/quote-quality defects.
- `AUDITED_NOT_VALIDATED`: schema is usable; no alpha conclusion yet.

Do not silently drop bad observations. Report their count, rules, and impact. Derive a date/session key only from trustworthy timestamp or source metadata.

## Discovery event table

One row per deduplicated event:

```text
event_id,date,symbol,side,event_timestamp,entry_timestamp,
state_family,variant_id,prior_only_inputs,matched_control_id,
valid_quote_gate,entry_bid1,entry_ask1,forward_touch_outcomes,
exclude_reason
```

Discovery tests state-conditioned **touch-side** forward outcomes first. Use a fixed small horizon set determined before reading results, e.g. 1/3/5 valid bars—not a sweep. Use matched controls in the same symbol/date/time-of-day and comparable prior range/spread bucket where feasible.

## Trade ledger

```text
trade_id,event_id,date,symbol,side,signal_timestamp,entry_timestamp,
entry_price,entry_touch,stop_price,target_price,residual_rr,
exit_timestamp,exit_price,exit_touch,exit_reason,gross_pnl,
commission_slippage_scenario,net_pnl_scenario,control_id,quality_flags
```

Execution convention:

```text
long entry  = first valid ask1 after signal
long exit   = first valid bid1 at TP/SL/forced-session evaluation
short entry = first valid bid1 after signal
short exit  = first valid ask1 at TP/SL/forced-session evaluation
```

If a bar/snapshot spans both bracket boundaries and exact sequence is unknowable, mark `AMBIGUOUS_BRACKET_PATH`; use a conservative adverse ordering for the primary result and report the alternative separately. Never assume a passive displayed quote filled.

## Small-sample validation

For about 40 dates:

1. Lock the last 40% complete dates before candidate selection.
2. Use earlier dates only to choose from the finite ledger.
3. Freeze the exact selected card and run it once on OOS.
4. Aggregate P&L/events by date. Bootstrap/resample dates or contiguous date blocks—not individual snapshots/trades.
5. A candidate concentrated in two or fewer dates is rejected even if total P&L is positive.

A simple optional search-stability diagnostic: repeat several chronological or balanced date-block splits **inside development only**, select the top card in each, and tabulate selection frequency plus holdout rank. It is diagnostic, not proof; with too few dates, say `INSUFFICIENT_BLOCKS_FOR_STABILITY`.

## Validation report template

```text
Data facts: source paths, dates, rows, sampling/gaps, quote defects.
Candidate mechanism: observable state only; no claim about unseen order flow.
Search ledger: families/variants tried, all results.
Frozen rule: exact entry, TP, SL, R/R, no-trade, forced-session conventions.
Execution: touch-side convention and ambiguous-path treatment.
Development: event/trade counts, controls, daily concentration.
Frozen OOS: same metrics, by side/symbol/date, gross then cost stress.
Uncertainty: date/block bootstrap setup and interval.
Decision: REJECT | PROVISIONAL / SHADOW ONLY | REPLICATION_REQUIRED.
What would falsify / next untouched-data requirement:
```

## Evidence anchors

- Briola, Bartolucci & Aste (2025), *Deep limit order book forecasting*: high forecasting metrics need not translate to actionable trading signals; evaluate transaction practicality.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC12315853/
- Bailey et al. (2017), *The Probability of Backtest Overfitting*: model-free, non-parametric PBO/CSCV framework for selection bias in investment backtests.
  https://scholarworks.wmich.edu/math_pubs/42
- Sullivan, Timmermann & White (1998/1999): bootstrap evaluation of a full rule universe to account for data snooping.
  https://researchonline.lse.ac.uk/id/eprint/119144/
