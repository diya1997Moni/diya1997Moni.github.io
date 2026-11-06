"""Summarise an ad platform CSV export and flag winners and underperformers.

Input CSV columns: campaign, spend, impressions, clicks, conversions, revenue
Usage: python3 ad_performance_summary.py sample-data/ads_export.csv
Works on exported files only, so it never touches a live ad account.
"""
import csv
import statistics
import sys


def ratio(a: float, b: float) -> float:
    return a / b if b else 0.0


def load(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = []
        for r in csv.DictReader(f):
            spend, imps = float(r["spend"]), float(r["impressions"])
            clicks, conv, rev = float(r["clicks"]), float(r["conversions"]), float(r["revenue"])
            rows.append({
                "campaign": r["campaign"],
                "spend": spend,
                "ctr": ratio(clicks, imps) * 100,
                "cpc": ratio(spend, clicks),
                "cpa": ratio(spend, conv),
                "roas": ratio(rev, spend),
            })
        return rows


def main(path: str) -> None:
    rows = load(path)
    total_spend = sum(r["spend"] for r in rows)
    median_roas = statistics.median(r["roas"] for r in rows)
    print(f"{'Campaign':<24}{'Spend':>10}{'CTR %':>8}{'CPC':>8}{'CPA':>9}{'ROAS':>7}  Flag")
    for r in sorted(rows, key=lambda r: r["roas"], reverse=True):
        flag = "scale" if r["roas"] > median_roas * 1.2 else "review" if r["roas"] < median_roas * 0.8 else ""
        print(f"{r['campaign']:<24}{r['spend']:>10.2f}{r['ctr']:>8.2f}{r['cpc']:>8.2f}{r['cpa']:>9.2f}{r['roas']:>7.2f}  {flag}")
    print(f"\nTotal spend: {total_spend:.2f} | Median ROAS: {median_roas:.2f}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
