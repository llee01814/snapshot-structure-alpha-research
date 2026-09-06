#!/usr/bin/env python3
"""Read-only audit for five-level market-by-price quote snapshots (stdlib only)."""
from __future__ import annotations
import argparse, csv, gzip, json, math
from datetime import datetime
from pathlib import Path

CANONICAL = ["timestamp"] + [f"{side}_{field}_{i}" for side in ("bid", "ask") for field in ("px", "qty") for i in range(1, 6)]
ALIASES = {
    "timestamp": ["timestamp", "time", "datetime", "date_time", "ts"],
    **{f"{side}_px_{i}": [f"{side}_px_{i}", f"{side}price{i}", f"{side}_price_{i}", f"{side}Price{i}"] for side in ("bid", "ask") for i in range(1, 6)},
    **{f"{side}_qty_{i}": [f"{side}_qty_{i}", f"{side}size{i}", f"{side}_size_{i}", f"{side}vol{i}", f"{side}_volume_{i}"] for side in ("bid", "ask") for i in range(1, 6)},
}

def as_float(value):
    try:
        x = float(value)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None

def parse_time(value):
    text = str(value).strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text).timestamp()
    except ValueError:
        for fmt in ("%Y/%m/%d %H:%M:%S", "%Y%m%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
            try: return datetime.strptime(text, fmt).timestamp()
            except ValueError: pass
    return None

def resolve(headers):
    lower = {h.strip().lower(): h for h in headers}
    mapped = {}
    for canonical, choices in ALIASES.items():
        for choice in choices:
            if choice.lower() in lower:
                mapped[canonical] = lower[choice.lower()]
                break
    return mapped

def read_rows(path):
    opener = gzip.open if path.suffix.lower() == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as f:
        if path.name.lower().endswith((".jsonl", ".jsonl.gz")):
            rows = [json.loads(line) for line in f if line.strip()]
            return rows, list(rows[0]) if rows else []
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames or []

def audit(path):
    rows, headers = read_rows(path)
    mapping = resolve(headers)
    missing = [x for x in CANONICAL if x not in mapping]
    report = {
        "data_contract": "five_level_quote_snapshot_only", "source": str(path), "rows": len(rows),
        "schema": {"headers": headers, "mapping": mapping, "missing_required": missing},
        "prohibited_inferences": ["queue_position", "true_cancellation", "order_replacement", "iceberg_order", "aggressor_side", "participant_intent"],
        "research_readiness": {"can_claim_order_flow": False, "status": "DATA_NOT_READY" if missing or not rows else "AUDITED_NOT_VALIDATED"},
        "quality": {"timestamp_parse_failures": 0, "non_monotonic_timestamps": 0, "max_timestamp_gap_seconds": None, "crossed_or_locked_rows": 0, "negative_or_missing_quote_fields": 0, "non_monotone_ladder_rows": 0, "stale_best_quote_pairs": 0}
    }
    if missing or not rows: return report
    prior_t = prior_touch = None; gaps = []
    for row in rows:
        t = parse_time(row.get(mapping["timestamp"]))
        if t is None: report["quality"]["timestamp_parse_failures"] += 1
        elif prior_t is not None:
            if t < prior_t: report["quality"]["non_monotonic_timestamps"] += 1
            else: gaps.append(t-prior_t)
        if t is not None: prior_t = t
        bids = [as_float(row.get(mapping[f"bid_px_{i}"])) for i in range(1,6)]
        asks = [as_float(row.get(mapping[f"ask_px_{i}"])) for i in range(1,6)]
        qtys = [as_float(row.get(mapping[f"{s}_qty_{i}"])) for s in ("bid","ask") for i in range(1,6)]
        if any(x is None or x <= 0 for x in bids+asks+qtys): report["quality"]["negative_or_missing_quote_fields"] += 1; continue
        if any(bids[i] < bids[i+1] for i in range(4)) or any(asks[i] > asks[i+1] for i in range(4)): report["quality"]["non_monotone_ladder_rows"] += 1
        if bids[0] >= asks[0]: report["quality"]["crossed_or_locked_rows"] += 1
        touch = (bids[0], asks[0])
        if touch == prior_touch: report["quality"]["stale_best_quote_pairs"] += 1
        prior_touch = touch
    report["quality"]["max_timestamp_gap_seconds"] = max(gaps) if gaps else 0.0
    return report

def main():
    p = argparse.ArgumentParser(); p.add_argument("input", type=Path); p.add_argument("--output", type=Path, required=True)
    a = p.parse_args(); result = audit(a.input); a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": result["research_readiness"]["status"], "rows": result["rows"], "missing": result["schema"]["missing_required"]}, ensure_ascii=False))
if __name__ == "__main__": main()
