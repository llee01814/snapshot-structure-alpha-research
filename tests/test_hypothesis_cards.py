#!/usr/bin/env python3
"""Contract test for research direction cards, not strategy profitability."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "references" / "snapshot-hypothesis-cards.md"
text = CARDS.read_text(encoding="utf-8")

required_cards = [
    "HC-01",  # liquidity drought duration / resolution
    "HC-02",  # L1 vs L2-5 shape transition
    "HC-03",  # range acceptance/re-entry conditional event
    "HC-04",  # spread-state-conditioned displacement
    "HC-05",  # variance-ratio / serial-dependence regime
    "HC-06",  # volatility surprise / compression-expansion regime
    "HC-07",  # slope persistence versus decay
    "HC-08",  # local-regression residual / curvature transition
]
for card in required_cards:
    assert card in text, f"missing required research direction: {card}"

for requirement in [
    "Observable inputs", "Event definition", "Null / matched control",
    "Falsifier", "Strategy conversion gate", "Source boundary",
]:
    assert text.count(requirement) >= 4, f"each card must specify {requirement}"

forbidden = [
    "queue position", "aggressor side", "actual cancellation",
    "executed volume", "guaranteed passive fill", "hidden liquidity",
]
low = text.lower()
for phrase in forbidden:
    assert phrase not in low, f"unavailable-data claim leaked into cards: {phrase}"

assert "S21–S25" in text and "P33" in text
assert "not a strategy library" in low
print("PASS: hypothesis cards provide bounded snapshot-only directions")
