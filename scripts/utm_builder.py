"""Build consistent UTM-tagged URLs from a CSV of campaigns.

Input CSV columns: url, source, medium, campaign, content (optional), term (optional)
Usage: python3 utm_builder.py sample-data/campaigns.csv > tagged_urls.csv
"""
import csv
import sys
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse


def slug(value: str) -> str:
    return "_".join(value.strip().lower().split())


def tag(row: dict) -> str:
    parts = urlparse(row["url"].strip())
    query = dict(parse_qsl(parts.query))
    query.update({
        "utm_source": slug(row["source"]),
        "utm_medium": slug(row["medium"]),
        "utm_campaign": slug(row["campaign"]),
    })
    for key in ("content", "term"):
        if row.get(key, "").strip():
            query[f"utm_{key}"] = slug(row[key])
    return urlunparse(parts._replace(query=urlencode(query)))


def main(path: str) -> None:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    writer = csv.writer(sys.stdout)
    writer.writerow(["campaign", "tagged_url"])
    for row in rows:
        writer.writerow([row["campaign"], tag(row)])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
