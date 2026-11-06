"""Risk-based position sizing. Educational only, not financial advice.

Usage: python3 position_size_calculator.py ACCOUNT RISK_PCT ENTRY STOP [TARGET]
Example: python3 position_size_calculator.py 10000 1 50 47 59
"""
import math
import sys


def main(account, risk_pct, entry, stop, target=None):
    risk_cash = account * risk_pct / 100
    per_share = abs(entry - stop)
    shares = math.floor(risk_cash / per_share)
    print(f"Risking {risk_pct}% = {risk_cash:,.2f}  |  stop distance {per_share:.2f}")
    print(f"Position: {shares} units, cost {shares * entry:,.2f} ({shares * entry / account:.0%} of account)")
    if target:
        rr = abs(target - entry) / per_share
        print(f"Reward:risk = {rr:.2f}:1  |  break-even win rate = {1 / (1 + rr):.0%}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) not in (4, 5):
        sys.exit(__doc__)
    main(float(a[0]), float(a[1]), float(a[2]), float(a[3]), float(a[4]) if len(a) == 5 else None)
