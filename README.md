# Snapshot Structure Alpha Research

A conservative AgentSkill for turning **five-level quote snapshots** into a small, falsifiable research process for structural trading hypotheses.

It is designed for data with:

```text
timestamp
bid/ask price levels 1–5
bid/ask displayed quantities 1–5
```

It is not an order-flow, queue-position, or passive-fill simulator. It does not promise an alpha or authorize trading.

## Install for a remote Hermes agent

Clone the repository, then either copy the directory into that agent's skills directory or install the packaged `.skill` file:

```bash
git clone <REPOSITORY_URL>
cp -R snapshot-structure-alpha-research ~/.hermes/skills/research/
```

The agent should load `snapshot-structure-alpha-research` before using local quote data.

## Run the audit

```bash
python3 scripts/audit_snapshot_quotes.py /path/to/raw.csv --output run/schema_audit.json
```

The helper is read-only and uses Python standard library only. It accepts CSV/CSV.GZ and JSONL/JSONL.GZ. It reports schema mapping, missing required fields, timestamp ordering/gaps, quote-ladder violations, crossed/locked quotes and stale touch quotes.

## Workflow

```text
Audit → point-in-time state table → small hypothesis ledger
→ pre-registered strategy/control → day-blocked OOS
→ touch-side/cost stress → REJECT | PROVISIONAL | REPLICATION_REQUIRED
```

For roughly 40 complete trading dates: reserve the final ~40% dates before selection; test a maximum of three mechanism-distinct families and three fixed variants each during development; freeze candidates before the OOS run.

## Critical execution rules

```text
long entry = first valid ask1 after signal
long exit  = first valid bid1 at exit
short entry = first valid bid1 after signal
short exit  = first valid ask1 at exit
normal exit = TP or SL only
session boundary = SESSION_FORCED, separately reported
```

See `SKILL.md` and `references/research-contract.md` for the full contract, matched-control geometry, uncertainty reporting and rejection gates.

## Verify

```bash
python3 tests/test_snapshot_structure_audit.py
python3 -m py_compile scripts/audit_snapshot_quotes.py
```

Expected result: `PASS: snapshot audit contract`.

## Research basis

- Briola, Bartolucci & Aste (2025): LOB forecast accuracy does not necessarily create actionable trading signals.
- Bailey et al. (2017): probability of backtest overfitting / CSCV.
- Sullivan, Timmermann & White (1998/1999): bootstrap evaluation under rule-selection data snooping.

Links are retained in `references/research-contract.md`.
