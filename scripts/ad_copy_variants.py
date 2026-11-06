"""Generate ad copy variants with the Claude API, enforcing platform character limits.

Setup:  pip install anthropic   and   export ANTHROPIC_API_KEY=your_key
Usage:  python3 ad_copy_variants.py "Padel racket store in the Philippines" "Free shipping over PHP 3000"
Always review output before it goes live.
"""
import json
import sys

import anthropic

LIMITS = {"headline": 30, "description": 90}  # Google responsive search ad limits
MODEL = "claude-sonnet-5-5"


def generate(product: str, offer: str, n: int = 5) -> dict:
    client = anthropic.Anthropic()
    prompt = (
        f"Write {n} ad headlines (max {LIMITS['headline']} characters) and {n} descriptions "
        f"(max {LIMITS['description']} characters) for: {product}. Offer: {offer}. "
        "Vary the angle: benefit, urgency, proof, price. Return JSON only: "
        '{"headlines": [...], "descriptions": [...]}'
    )
    msg = client.messages.create(model=MODEL, max_tokens=800, messages=[{"role": "user", "content": prompt}])
    return json.loads(msg.content[0].text)


def within_limits(copy: dict) -> dict:
    return {
        "headlines": [h for h in copy["headlines"] if len(h) <= LIMITS["headline"]],
        "descriptions": [d for d in copy["descriptions"] if len(d) <= LIMITS["description"]],
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    print(json.dumps(within_limits(generate(sys.argv[1], sys.argv[2])), indent=2))
