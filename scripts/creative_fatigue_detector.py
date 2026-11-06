"""Flag ads whose click-through rate is decaying while frequency climbs.

Input CSV: ad, date, impressions, clicks, frequency  (one row per ad per day)
Usage: python3 creative_fatigue_detector.py sample-data/creative_daily.csv
"""
import csv
import sys
from collections import defaultdict


def ctr(rows):
    imps = sum(r["imps"] for r in rows)
    return sum(r["clicks"] for r in rows) / imps if imps else 0.0


def main(path, window=4, drop_threshold=0.25):
    ads = defaultdict(list)
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            ads[r["ad"]].append({"date": r["date"], "imps": int(r["impressions"]),
                                 "clicks": int(r["clicks"]), "freq": float(r["frequency"])})
    print(f"{'Ad':<14}{'Early CTR':>10}{'Recent CTR':>12}{'Change':>9}{'Freq':>6}  Status")
    for ad, rows in ads.items():
        rows.sort(key=lambda r: r["date"])
        if len(rows) < window * 2:
            continue
        early, recent = ctr(rows[:window]), ctr(rows[-window:])
        change = recent / early - 1 if early else 0
        freq = rows[-1]["freq"]
        status = "FATIGUED: refresh" if change <= -drop_threshold and freq >= 2 else \
                 "watch" if change <= -drop_threshold / 2 else "healthy"
        print(f"{ad:<14}{early:>10.2%}{recent:>12.2%}{change:>+9.0%}{freq:>6.1f}  {status}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
