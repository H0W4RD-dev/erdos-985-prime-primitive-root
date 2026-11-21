# A prime primitive root below every odd prime

**Will Howe, Grant Huffman, Jensen Kohlmeyer, and Liam Kruer**

November 20, 2026 · Erdős problem 985 · JSP-000818

For every odd prime $p$ there is a prime integer $q<p$ of multiplicative order $p-1$ modulo $p$. Erdős asked the strict-bound question on printed page 233. At $p=2$ there is no smaller prime. Theorem 1.1 gives the deduction for all odd primes. [Manuscript (PDF, 2 pages)](Erdos_985_Prime_Primitive_Root.pdf) · [TeX source](Erdos_985_Prime_Primitive_Root.tex) · [Erdős’s 1965 paper, p. 233](https://www.renyi.hu/~p_erdos/1965-17.pdf#page=39)

## Proof and attribution

McGown, Treviño and Trudgian proved under GRH that the least **prime** primitive root is below $\sqrt{p}-2$ for every prime $p>2791$. Levent Alpöge, working with Claude, supplied the zeta and Dirichlet GRH theorems. Andrew V. Sutherland independently verified the theorem statements and reports kernel checks of the proof. These results give the required strict bound above 2791. Lemma 2.1 verifies the remaining 405 prime moduli by exact integer arithmetic. [McGown, Treviño and Trudgian, Theorem 1](https://doi.org/10.7169/facm/2016.55.2.5) · [Alpöge’s announcement](https://alpo.ge/remark.pdf) · [Sutherland’s verification report](https://math.mit.edu/~drew/grh/)

The authors acknowledge assistance from OpenAI Codex in preparing the manuscript and verifying the finite calculations. A January 2026 note in Neel Somani’s GPT-Erdos project recorded the conditional deduction and finite check. On November 20, @lixiang90 submitted the deduction using Alpöge’s announced proof in prize PR #5615. Computations of least prime primitive roots also predate these notes. [January note](https://github.com/neelsomani/gpt-erdos/blob/9fead6532ee692f2a14d872175c52ddd19656698/data/solutions/985/candidate_solution.md) · [Earlier prize submission](https://github.com/TheJustinSunPrize/awards/pull/5615) · [Tomás Oliveira e Silva’s computations](https://sweet.ua.pt/tos/p_roots.html)

The companion argument takes $x=p$ in the character-sum lemma. It proves the required bound above explicit thresholds, then certifies every one of 74,187 remaining candidates, including 18,802 prime moduli. [Derivation and certificate format](endpoint.md) · [Per-range results](x-equals-p.json)

## Reproduce the finite calculations

With Python 3.10 or later, run the following from this directory. The verifier uses the standard library and the files included here.

~~~sh
python verify.py
~~~

The first check reads each prime factorization and exclusion residue, then follows the complete multiplicative orbit for each of the 405 small witnesses. The second enumerates the candidate moduli from their factorizations, verifies the rational estimates and replays every word in the companion certificate. [Small witness table](small-prime-witnesses.tsv) · [Companion certificate](x-equals-p-witnesses.zip) · [Verifier source](verify.py)

~~~text
Small table: 405 primes, 524,044 orbit multiplications, maximum q = 53.
x=p: 74,187 candidates, 18,802 prime moduli, 46,493 proper divisors, 8,892 Euler witnesses, maximum q = 173.
~~~

To typeset the manuscript, run the following command with Tectonic.

~~~sh
tectonic Erdos_985_Prime_Primitive_Root.tex
~~~
