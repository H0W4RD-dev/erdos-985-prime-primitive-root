"""Replay the small prime table and the x=p certificate using Python 3.10+."""

import csv
import json
import struct
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import gcd, isqrt, prod
from pathlib import Path
from zipfile import ZipFile


HERE = Path(__file__).resolve().parent
# (number of distinct factors of p-1, square-root cutoff, logarithm bound)
BOUNDS = [(3, 143, 10), (4, 363, 12), (5, 871, 14), (6, 2019, 16),
          (7, 4321, 17), (8, 9693, 19), (9, 20443, 20)]


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def check_small_table():
    with (HERE / "small-prime-witnesses.tsv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source, delimiter="\t"))
    primes = [p for p in range(3, 2792) if prime(p)]
    require([int(row["p"]) for row in rows] == primes, "small table coverage and order")
    roots = []
    multiplications = 0
    for p, row in zip(primes, rows, strict=True):
        q = int(row["q"])
        require(prime(q) and q < p, (p, q))
        factors = [tuple(map(int, pair.split("^"))) for pair in row["p_minus_one_factorization"].split("*")]
        divisors = [r for r, _ in factors]
        require(divisors == sorted(set(divisors)) and all(prime(r) and e > 0 for r, e in factors), p)
        require(prod(r**e for r, e in factors) == p - 1 and pow(q, p - 1, p) == 1, p)
        residues = [(r, pow(q, (p - 1) // r, p)) for r in divisors]
        printed = [tuple(map(int, pair.split(":"))) for pair in row["order_exclusion_residues"].split(";")]
        require(residues == printed and all(a != 1 for _, a in residues), p)
        value = 1
        for exponent in range(1, p):
            value = value * q % p
            if value == 1:
                break
        require(value == 1 and exponent == p - 1, (p, q, "first return"))
        multiplications += exponent
        roots.append((p, q))
    require(len(roots) == 405 and max(q for p, q in roots) == 53, "finite theorem")
    require([p for p, q in roots if q == 53] == [2791] and multiplications == 524044, "finite extrema")
    print(f"Small table: {len(roots):,} primes, {multiplications:,} orbit multiplications, maximum q = 53.")


def exp_lower(x):
    term = total = Fraction(1)
    for j in range(1, 101):
        term *= Fraction(x, j)
        total += term
    return total


def check_scalar_bounds(metadata):
    c = (Fraction(2, 3) * (1 + Fraction(2, 52) + Fraction(3, 52**3))
         * (1 + Fraction(5, 21)) + Fraction(9, 52 * 7))
    require(str(c) == metadata["c_p_p_strict_upper"] and c < 1, "character sum constant")
    require(3**7 < 2792 and 52**2 < 2792 < exp_lower(8) and 2 * (1 + 3 * 8) < 52, "ranks 1 and 2")
    floors = [(f["rank"], f["sqrt_floor"], f["log_upper"]) for f in metadata["rank_floors"]]
    require(floors == BOUNDS, "rank cutoffs")
    for k, u, log_upper in BOUNDS:
        require(u**2 < exp_lower(log_upper) and 2 * (1 + (2**k - 1) * log_upper) < u, k)
    first_ten = [p for p in range(2, 31) if prime(p)]
    require(len(first_ten) == 10 and prod(first_ten) == metadata["prime_product_first_ten"] > 80000**2,
            "primorial")
    require(80000**2 < exp_lower(23) and 16 < exp_lower(3) and 2 * (1 + 1024 * 23) < 80000,
            "ranks 10 and above")


def candidates(rank, upper):
    """All even n=p-1 in the strip, with their distinct prime factors."""
    high = upper - 2
    first = [p for p in range(2, 31) if prime(p)]
    # Every possible largest factor leaves at least the product of the first k-1 primes.
    odd_primes = [q for q in range(3, high // prod(first[:rank - 1]) + 1, 2) if prime(q)]

    def extend(n, factors, start):
        remaining = rank - len(factors)
        if remaining == 0:
            if n >= 2791:
                yield n, factors
            return
        for i in range(start, len(odd_primes)):
            q = odd_primes[i]
            if n * q**remaining > high:
                break
            multiple = n * q
            while multiple <= high:
                yield from extend(multiple, (*factors, q), i + 1)
                multiple *= q

    values = []
    two_power = 2
    while two_power <= high:
        values.extend(extend(two_power, (2,), 0))
        two_power *= 2
    return sorted(values)


def check_strip(raw, row, rank, upper):
    values = candidates(rank, upper)
    require(len(values) == row["positions"] and len(raw) == 2 * len(values), ("strip size", rank))
    require(sha256(raw).hexdigest() == row["raw_sha256"], ("certificate digest", rank))
    counts = Counter()
    largest_q = largest_p = previous = 0
    for (n, factors), (word,) in zip(values, struct.iter_unpack("<H", raw), strict=True):
        tag, b = divmod(word, 16384)
        p = n + 1
        require(previous < n and 2792 <= p < upper and 1 < b < p, ("scope", p))
        previous = n
        if tag == 0:
            require(p % b == 0, ("divisor", p, b))
            counts["proper_divisor"] += 1
        elif tag == 1:
            require(pow(b, n, p) != 1 or 1 < gcd(pow(b, n // 2, p) - 1, p) < p, ("Euler", p, b))
            counts["Euler_composite"] += 1
        elif tag == 2:
            require(prime(b) and pow(b, n, p) == 1 and all(pow(b, n // r, p) != 1 for r in factors),
                    ("prime primitive root", p, b))
            counts["prime_primitive_root"] += 1
            largest_q = max(largest_q, b)
            largest_p = max(largest_p, p)
        else:
            raise ValueError(("unrecognized certificate", p, word))
    require(dict(counts) == row["counts"] and (largest_q, largest_p) == (row["largest_root"], row["largest_prime"]),
            ("strip totals", rank))
    return counts, largest_q


def check_endpoint():
    metadata = json.loads((HERE / "x-equals-p.json").read_bytes())
    check_scalar_bounds(metadata)
    path = HERE / "x-equals-p-witnesses.zip"
    require(sha256(path.read_bytes()).hexdigest() == metadata["archive_sha256"], "archive digest")
    totals, roots = Counter(), []
    with ZipFile(path) as archive:
        names = [f"strip-{i:02d}.u16" for i in range(len(BOUNDS))]
        require(sorted(archive.namelist()) == names, "strip inventory")
        for i, ((k, u, _), row) in enumerate(zip(BOUNDS, metadata["groups"], strict=True)):
            require((row["strip"], row["rank"], row["lower"], row["upper"]) == (i, k, 2792, u*u), k)
            counts, largest = check_strip(archive.read(names[i]), row, k, u*u)
            totals.update(counts)
            roots.append(largest)
    require(dict(totals) == metadata["counts"] and totals["prime_primitive_root"] == metadata["prime_moduli"] == 18802,
            "prime total")
    require(sum(totals.values()) == metadata["independently_replayed_positions"] == 74187
            and max(roots) == metadata["largest_prime_witness"] == 173, "endpoint total")
    print(f"x=p: {sum(totals.values()):,} candidates, {totals['prime_primitive_root']:,} prime moduli, "
          f"{totals['proper_divisor']:,} proper divisors, {totals['Euler_composite']:,} Euler witnesses, "
          f"maximum q = {max(roots)}.")


if __name__ == "__main__":
    check_small_table()
    check_endpoint()
