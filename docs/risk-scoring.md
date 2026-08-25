# Risk scoring

Each finding contributes its configured score multiplied by confidence. From v0.2, the same `(category, rule ID)` contributes only once; if duplicate instances differ, the strongest confidence-adjusted contribution wins. This prevents repeated equivalent detector output from inflating risk while preserving distinct rules in one category.

Contributions are summed per category and capped at 35. Category values are combined as:

```text
100 × (1 − product(1 − category_score / 100))
```

Two bounded correlations are then applied: `PI-001` plus `HID-001` adds 10, and `HID-001` plus `SEC-001` adds 7. The rounded result is clamped to 0–100. Bands remain 0–19 informational, 20–39 low, 40–59 medium, 60–79 high, and 80–100 critical.

Tests verify empty input, confidence adjustment, category caps, duplicate resistance, strongest-duplicate selection, ordering invariance, multi-category combination, both synergies, score bounds, and band boundaries. A risk score prioritizes review; it is neither a probability nor a maliciousness verdict.
