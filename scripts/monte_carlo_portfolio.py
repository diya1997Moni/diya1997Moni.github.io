"""Monte Carlo simulation of a portfolio's possible outcomes. Educational only.

Shows the range of outcomes, not a forecast. Real returns have fatter tails than this model.

Usage: python3 monte_carlo_portfolio.py [start=10000] [annual_return=0.07] [annual_vol=0.16] [years=10] [sims=5000]
"""
import math
import random
import sys


def simulate(start, mu, vol, years, sims, seed=7):
    random.seed(seed)
    months = years * 12
    drift, sd = (mu - vol ** 2 / 2) / 12, vol / math.sqrt(12)
    finals, deep_dd = [], 0
    for _ in range(sims):
        v, peak, worst = start, start, 0.0
        for _ in range(months):
            v *= math.exp(random.gauss(drift, sd))
            peak = max(peak, v)
            worst = min(worst, v / peak - 1)
        finals.append(v)
        deep_dd += worst <= -0.30
    finals.sort()
    return finals, deep_dd / sims


if __name__ == "__main__":
    a = [float(x) for x in sys.argv[1:]] + [None] * 5
    start, mu, vol = a[0] or 10000, a[1] if a[1] is not None else 0.07, a[2] or 0.16
    years, sims = int(a[3] or 10), int(a[4] or 5000)
    finals, dd = simulate(start, mu, vol, years, sims)
    pct = lambda p: finals[int(p * (len(finals) - 1))]
    print(f"{sims:,} simulations, {years} years, {mu:.0%} return, {vol:.0%} volatility, start {start:,.0f}\n")
    for p in (0.05, 0.25, 0.5, 0.75, 0.95):
        print(f"  {int(p * 100):>2}th percentile: {pct(p):>12,.0f}")
    print(f"\n  Chance of ending below start: {sum(f < start for f in finals) / len(finals):.0%}")
    print(f"  Chance of a 30%+ drawdown along the way: {dd:.0%}")
