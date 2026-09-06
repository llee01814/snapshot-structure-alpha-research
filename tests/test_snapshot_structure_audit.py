#!/usr/bin/env python3
"""Contract test for the reusable snapshot audit helper."""
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_SCRIPT = Path(__file__).resolve().parents[1] / "scripts/audit_snapshot_quotes.py"

HEADER = ["timestamp"] + [f"bid_px_{i}" for i in range(1, 6)] + [f"bid_qty_{i}" for i in range(1, 6)] + [f"ask_px_{i}" for i in range(1, 6)] + [f"ask_qty_{i}" for i in range(1, 6)]
ROWS = [
    ["2026-06-05 09:00:00", "100", "99", "98", "97", "96", "10", "9", "8", "7", "6", "101", "102", "103", "104", "105", "11", "10", "9", "8", "7"],
    ["2026-06-05 09:00:01", "100", "99", "98", "97", "96", "10", "9", "8", "7", "6", "101", "102", "103", "104", "105", "11", "10", "9", "8", "7"],
    ["2026-06-05 09:00:05", "102", "99", "98", "97", "96", "10", "9", "8", "7", "6", "101", "102", "103", "104", "105", "11", "10", "9", "8", "7"],
]

def test_quote_audit_contract() -> None:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "sample.csv"
        p.write_text("\n".join([",".join(HEADER)] + [",".join(r) for r in ROWS]) + "\n", encoding="utf-8")
        out = Path(d) / "audit.json"
        proc = subprocess.run([sys.executable, str(SKILL_SCRIPT), str(p), "--output", str(out)], text=True, capture_output=True)
        assert proc.returncode == 0, proc.stderr
        report = json.loads(out.read_text(encoding="utf-8"))
        assert report["data_contract"] == "five_level_quote_snapshot_only"
        assert report["schema"]["missing_required"] == []
        assert report["quality"]["crossed_or_locked_rows"] == 1
        assert report["quality"]["stale_best_quote_pairs"] == 1
        assert report["quality"]["max_timestamp_gap_seconds"] == 4.0
        assert "queue_position" in report["prohibited_inferences"]
        assert report["research_readiness"]["can_claim_order_flow"] is False

if __name__ == "__main__":
    test_quote_audit_contract()
    print("PASS: snapshot audit contract")
