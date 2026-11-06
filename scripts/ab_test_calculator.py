"""A/B test significance and sample-size calculator (standard library only).

Usage:
  python3 ab_test_calculator.py test 120 4000 156 4000     # conv_A n_A conv_B n_B
  python3 ab_test_calculator.py size 0.03 0.20             # baseline rate, relative lift to detect
"""
import math
import sys
from statistics import NormalDist

N = NormalDist()


def z_test(conv_a, n_a, conv_b, n_b):
    p_a, p_b = conv_a / n_a, conv_b / n_b
    pooled = (conv_a + conv_b) / (n_a + n_b)
    se = math.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    z = (p_b - p_a) / se
    return p_a, p_b, z, 2 * (1 - N.cdf(abs(z)))


def sample_size(base, rel_lift, alpha=0.05, power=0.8):
    p1, p2 = base, base * (1 + rel_lift)
    pbar = (p1 + p2) / 2
    za, zb = N.inv_cdf(1 - alpha / 2), N.inv_cdf(power)
    top = za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil(top ** 2 / (p2 - p1) ** 2)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 5 and a[0] == "test":
        p_a, p_b, z, p = z_test(int(a[1]), int(a[2]), int(a[3]), int(a[4]))
        print(f"A: {p_a:.2%}   B: {p_b:.2%}   lift: {(p_b / p_a - 1):+.1%}")
        print(f"z = {z:.2f}   p-value = {p:.4f}")
        print("Significant at 95%." if p < 0.05 else "Not significant. Keep running or call it a tie.")
    elif len(a) == 3 and a[0] == "size":
        print(f"Needed per variant: {sample_size(float(a[1]), float(a[2])):,} visitors (95% confidence, 80% power)")
    else:
        sys.exit(__doc__)
