"""Find wasted search spend in an exported search terms report and suggest negatives.
Reads a CSV export only, so it never touches a live ad account.

Input CSV: search_term, cost, clicks, conversions
Usage: python3 search_term_waste_finder.py sample-data/search_terms.csv [min_cost=20]
"""
import csv
import sys
from collections import defaultdict

STOP = {"a", "the", "in", "for", "to", "of", "and", "near", "me"}


def main(path, min_cost):
    with open(path, newline="") as f:
        rows = [{"term": r["search_term"], "cost": float(r["cost"]), "conv": float(r["conversions"])}
                for r in csv.DictReader(f)]
    waste = [r for r in rows if r["conv"] == 0 and r["cost"] >= min_cost]
    total, wasted = sum(r["cost"] for r in rows), sum(r["cost"] for r in waste)
    print(f"Zero-conversion terms over {min_cost:.0f} spend:\n")
    for r in sorted(waste, key=lambda r: -r["cost"]):
        print(f"  {r['term']:<34}{r['cost']:>8.2f}")
    print(f"\nWasted: {wasted:.2f} of {total:.2f} ({wasted / total:.0%})")

    good_words = {w for r in rows if r["conv"] > 0 for w in r["term"].split()}
    by_word = defaultdict(float)
    for r in waste:
        for w in set(r["term"].split()) - STOP - good_words:
            by_word[w] += r["cost"]
    print("\nNegative keyword candidates (words that never appear in a converting term):")
    for w, c in sorted(by_word.items(), key=lambda x: -x[1])[:8]:
        print(f"  {w:<20}{c:>8.2f}")
    print("\nReview before adding. A word can be harmless in one context and costly in another.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 20)
