---
name: snapshot-structure-alpha-research
description: Use when researching five-level quote snapshot alpha.
---

# Snapshot Structure Alpha Research

Use this for the owner's `timestamp + bid/ask price_1..5 + displayed qty_1..5` data. The goal is **not** a factor model or a guaranteed alpha. The goal is a disciplined answer: does a repeatable, executable price/quote-state phenomenon survive a small-sample test?

**Hard boundary:** five-level snapshots show displayed quotes at sampling times. They do **not** reveal trades, aggressor side, queue position, cancellations, order replacement, iceberg orders, or participant intent. Call changes `quote-dynamics proxies`, never order flow.

## Start: audit before a hypothesis

Run the included helper on a copy or source path; it is read-only:

```bash
python3 ~/.hermes/skills/research/snapshot-structure-alpha-research/scripts/audit_snapshot_quotes.py \
  /path/to/raw.csv --output /path/to/run/audit.json
```

If schema, timestamps, tick behavior, sessions, crossed/locked quotes, stale periods, or gaps cannot be explained, stop at `DATA_NOT_READY`. Never invent columns or silently fill missing prices.

Required minimum: timestamp, five bid prices/quantities, five ask prices/quantities, plus a trustworthy symbol/date source. Keep futures contract month distinct; do not merge or roll it invisibly.

## Operating loop

```text
Audit → form observable state table → find one structure → preregister one rule/control pair
→ day-blocked test → execution/cost stress → reject, provisional, or replication-required
```

### 1. Normalize only with past data

- Retain raw snapshots and create derived, timestamped bars/events with no future row access.
- Use `mid=(bid1+ask1)/2` only for **state description**. Executable prices remain touch-side.
- Compute price-path state: prior range, displacement, return-to-range, realized spread, top-5 displayed depth, depth symmetry, quote age/staleness, and quote validity.
- Normalize thresholds per **symbol × date**, using an expanding or strictly prior rolling baseline. Do not normalize against full-sample future volatility.
- Treat a date as the independent unit. Thousands of same-day snapshots are correlated observations, not thousands of independent experiments.

### 2. Discover structures, not parameter soup

Create a finite `hypothesis_ledger.csv` *before* selecting a winner. Limit the development search to at most **three mechanism-distinct families**, each with at most **three fixed variants**. Record all variants including failures.

Allowed observable families:

1. **State-conditioned excursion resolution:** abnormal displacement from a prior local range, then test whether the next valid state resolves by continuation or re-entry.
2. **Range rejection/acceptance:** price exits a recent range and then either persists outside or re-enters; condition only on quote validity/spread/depth state already observable at entry.
3. **Quote-quality transition:** spread/depth/staleness state changes coincident with an already-defined price-path state; test whether it adds incremental information versus the same price-path event alone.

For each candidate, first make a descriptive event table: count by date/symbol/side, touch-side forward outcome at a few preregistered horizons, and matched controls. A structure is worth trading research only if its direction, effect size, and cross-date coverage are coherent **before** bracket tuning.

Do not recycle the same continuation/reversal hypothesis under renamed thresholds. Do not reopen rejected S21–S25/P33-style lines through parameter changes.

### 3. Convert only one surviving phenomenon into a trade rule

Write a feature card before the first trade simulation:

```text
mechanism (observable, not claimed participant intent):
point-in-time state and event de-duplication:
entry: long=next valid ask1; short=next valid bid1
absolute stop / absolute target:
residual reward:risk gate at entry:
forced session close definition (separate from normal exits):
no-trade and data-quality gates:
matched control (same event, same entry, same absolute bracket):
falsifier:
```

Normal exits are **TP or SL only**. Session boundary becomes `SESSION_FORCED`, reported separately. No averaging down, no add-to-loser, no in-position reversal, and no OOS parameter rescue.

For every delayed confirmation rule, calculate remaining reward/risk at the actual touch-side entry. Skip events with `reward <= 0`, `risk <= 0`, or preregistered residual R/R not met. A control may differ in **one causal gate only**; it must retain the same event, entry timestamp, absolute stop, absolute target, R/R gate, sizing and execution convention.

### 4. Validate at the correct sample scale

Choose by complete trading days, not snapshots:

- `<20 days`: audit/descriptive only; no alpha claim.
- `20–59 days` (this owner's likely case): chronological development / frozen OOS split by complete dates, target roughly 60/40; reserve at least 8 complete OOS dates. Keep only one final candidate per mechanism family.
- `≥60 days`: still use day-blocked OOS; add expanding walk-forward folds only if no OOS date has influenced selection.

For every candidate and control report:

- event/trade count; number of dates, symbols and sides; concentration by date;
- gross touch-side P&L, then conservative spread/slippage/cost stress separately;
- TP, SL, `SESSION_FORCED`, rejected-by-gate counts;
- profit factor, median trade, max drawdown, payoff ratio, and daily P&L distribution;
- date-cluster or moving-block bootstrap confidence interval for **mean daily** P&L / event excess, with a sensitivity range of block lengths;
- matched-control incremental result and frozen OOS result.

Do not use IID bootstrap on snapshots. Do not select the best result after testing a broad menu and then report it as a single hypothesis. If the development search is materially broad, retain every trial and run a lightweight search penalty diagnostic (rank stability across day blocks / CSCV when enough blocks exist); a “winner” that often falls below median OOS is `REJECT`.

### 5. Decision gate

`REJECT` if gross touch-side result is negative, direction flips across OOS, result is concentrated in ≤2 dates, control is equal/better, residual R/R gates remove nearly all events, or costs plausibly erase the edge.

`PROVISIONAL / SHADOW ONLY` requires positive frozen OOS, coherent sign across a meaningful share of OOS dates, no single-date dependence, and better result than matched control. It is not deployment approval.

`REPLICATION_REQUIRED` means a provisional candidate needs new, untouched dates. No live order or autonomous trading authorization arises from this skill.

## Outputs required in every run

```text
run_manifest.json       paths, hashes, date split, config, code version
schema_audit.json       direct audit output
hypothesis_ledger.csv   every candidate/variant and outcome
feature_cards.md        only preregistered candidates
trade_ledger.csv        one row per signal/trade with all touch-side prices/reasons
validation_report.md    facts, inference, costs, controls, decision
```

Use `references/research-contract.md` for exact columns, edge cases, and report template.

## Red flags

- Treating a predictive mid-price label as executable P&L.
- Using an observed quote as a guaranteed passive fill.
- Calling displayed-quantity changes cancellations or absorption.
- Tuning TP/SL after seeing OOS, or using a different bracket/control geometry.
- Counting one day with thousands of snapshots as thousands of samples.
- Promoting a positive backtest without untouched-date replication.
