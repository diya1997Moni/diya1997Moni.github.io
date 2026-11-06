"""Backtest a moving-average crossover against buy-and-hold. Educational only.

Trades the NEXT day's return after a signal (no look-ahead) and charges costs per trade.
Past results do not predict future returns, and this is not financial advice.

Input CSV: date, close
Usage: python3 sma_crossover_backtest.py sample-data/prices.csv [fast=20] [slow=50] [cost_bps=5]
"""
import csv
import math
import statistics
import sys


def sma(xs, n, i):
    return sum(xs[i - n + 1:i + 1]) / n


def metrics(returns, label):
    equity, peak, max_dd = 1.0, 1.0, 0.0
    for r in returns:
        equity *= 1 + r
        peak = max(peak, equity)
        max_dd = min(max_dd, equity / peak - 1)
    sd = statistics.pstdev(returns)
    sharpe = statistics.mean(returns) / sd * math.sqrt(252) if sd else 0
    print(f"{label:<14} return {equity - 1:>+8.1%}   max drawdown {max_dd:>7.1%}   Sharpe {sharpe:>5.2f}")


def main(path, fast, slow, cost_bps):
    with open(path, newline="") as f:
        closes = [float(r["close"]) for r in csv.DictReader(f)]
    strat, hold, pos, trades = [], [], 0, 0
    for i in range(slow, len(closes) - 1):
        want = 1 if sma(closes, fast, i) > sma(closes, slow, i) else 0
        cost = cost_bps / 10000 if want != pos else 0
        trades += want != pos
        pos = want
        day = closes[i + 1] / closes[i] - 1
        strat.append(pos * day - cost)
        hold.append(day)
    print(f"SMA {fast}/{slow}, {cost_bps} bps per trade, {trades} trades over {len(strat)} days\n")
    metrics(strat, "Crossover")
    metrics(hold, "Buy and hold")
    print("\nNote: results on synthetic or past data prove nothing about the future.")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    main(a[0], int(a[1]) if len(a) > 1 else 20, int(a[2]) if len(a) > 2 else 50,
         float(a[3]) if len(a) > 3 else 5)
