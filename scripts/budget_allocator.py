"""Reallocate a marketing budget using diminishing returns.

Assumes conversions = a * spend^e for each channel (e < 1 means each extra dollar works
a little less). 'a' is fitted from last period's spend and conversions. Each channel keeps
at least (1 - max_shift) of its current spend, and the rest is handed out in small steps to
whichever channel gains most, capped at (1 + max_shift). Treat the output as a hypothesis to
test with a small budget shift, not a guarantee.

Input CSV: channel, spend, conversions
Usage: python3 budget_allocator.py sample-data/channels.csv [elasticity=0.7] [max_shift=0.5]
"""
import csv
import sys


def allocate(rows, elasticity=0.7, max_shift=0.5, steps=400):
    total = sum(r["spend"] for r in rows)
    for r in rows:
        r["a"] = r["conversions"] / r["spend"] ** elasticity
        r["new"] = r["spend"] * (1 - max_shift)
        r["cap"] = r["spend"] * (1 + max_shift)
    step = total * max_shift / steps
    for _ in range(steps):
        open_rows = [r for r in rows if r["new"] + step <= r["cap"] + 1e-9]
        if not open_rows:
            break
        best = max(open_rows, key=lambda r: r["a"] * ((r["new"] + step) ** elasticity - r["new"] ** elasticity))
        best["new"] += step
    return rows


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    e = float(sys.argv[2]) if len(sys.argv) > 2 else 0.7
    shift = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    with open(sys.argv[1], newline="") as f:
        data = [{"channel": r["channel"], "spend": float(r["spend"]), "conversions": float(r["conversions"])}
                for r in csv.DictReader(f)]
    out = allocate(data, e, shift)
    now = sum(r["conversions"] for r in out)
    then = sum(r["a"] * r["new"] ** e for r in out)
    print(f"{'Channel':<16}{'Now':>10}{'Suggested':>12}{'Change':>10}")
    for r in out:
        print(f"{r['channel']:<16}{r['spend']:>10,.0f}{r['new']:>12,.0f}{r['new'] / r['spend'] - 1:>+10.0%}")
    print(f"\nModelled conversions: {now:,.0f} -> {then:,.0f} ({then / now - 1:+.1%}), elasticity {e}, max shift {shift:.0%}")
