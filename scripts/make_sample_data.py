"""Create synthetic sample data so every script can be tried straight away.
All data is randomly generated (seeded) and not real. Usage: python3 make_sample_data.py
"""
import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "sample-data"
random.seed(42)


def prices(days=900):
    price, start = 100.0, date(2023, 1, 2)
    with open(OUT / "prices.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "close"])
        for i in range(days):
            price *= math.exp(random.gauss(0.0004, 0.012))
            w.writerow([(start + timedelta(days=i)).isoformat(), round(price, 2)])


def search_terms():
    terms = [("padel racket", 90, 60, 9), ("buy padel racket manila", 70, 40, 7),
             ("free padel lessons", 55, 38, 0), ("padel court near me", 48, 30, 0),
             ("tennis racket cheap", 40, 25, 0), ("padel racket review", 35, 22, 1),
             ("padel shoes", 60, 33, 5), ("free padel racket giveaway", 28, 20, 0),
             ("pickleball paddle", 31, 19, 0), ("padel bag", 22, 14, 2)]
    with open(OUT / "search_terms.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["search_term", "cost", "clicks", "conversions"])
        w.writerows(terms)


def creative_daily():
    with open(OUT / "creative_daily.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ad", "date", "impressions", "clicks", "frequency"])
        for ad, decay in [("Video A", 0.045), ("Static B", 0.005), ("Carousel C", 0.03)]:
            for d in range(14):
                imps = random.randint(9000, 11000)
                ctr = 0.02 * math.exp(-decay * d) * random.uniform(0.95, 1.05)
                w.writerow([ad, (date(2026, 10, 1) + timedelta(days=d)).isoformat(),
                            imps, int(imps * ctr), round(1.2 + d * 0.22, 2)])


def channels():
    rows = [("Meta", 5000, 160), ("Google Search", 3000, 150), ("TikTok", 2000, 40),
            ("LinkedIn", 1500, 12), ("EDM", 500, 55)]
    with open(OUT / "channels.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["channel", "spend", "conversions"])
        w.writerows(rows)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    prices(); search_terms(); creative_daily(); channels()
    print("Sample data written to", OUT)
