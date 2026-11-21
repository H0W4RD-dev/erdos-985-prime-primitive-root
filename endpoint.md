# A second proof from the character sums at $x=p$

Will Howe, with computational assistance from OpenAI Codex · November 20, 2026

For every odd prime $p$, some prime integer $q<p$ generates the units modulo $p$. For $p>2791$, the manuscript deduces this directly from McGown, Treviño and Trudgian's Theorem 1. Here we instead derive the weaker bound $q<p$ from their Lemma 1, using the same zeta RH and Dirichlet GRH inputs. The finite part of this argument is larger, and every case has an independently replayable certificate. [Manuscript, Theorem 1.1](Erdos_985_Prime_Primitive_Root.pdf) · [McGown, Treviño and Trudgian, §2](https://arxiv.org/pdf/1508.05182) · [Sutherland’s verification of Alpöge’s GRH theorem](https://math.mit.edu/~drew/grh/)

## From weighted sums to a prime generator

Put $N=p-1$ and let $k$ be the number of distinct primes dividing $N$. For each character $\chi$ modulo $p$ form

$$
S_\chi=\sum_{1\le n<p}\Lambda(n)\chi(n)(1-n/p),
$$

where $\Lambda$ is the von Mangoldt function. In this range the principal character is 1. For $p>2791$, Lemma 1 gives

$$
|S_1-p/2|\le\sqrt{p}/20+3,\qquad
|S_\chi|\le c(p,p)\sqrt{p}\log p\quad(\chi\ne1),
$$

where

$$
c(p,p)=\tfrac23(1+2/\sqrt{p}+3/p^{3/2})(1+5/(3\log p))
             +(\log p+2)/(\sqrt{p}\log p).
$$

Here $\sqrt{p}>52$ and $\log p>7$, so substitution gives $c(p,p)<50077/56784<1$. Also $\sqrt{p}/20+3<\sqrt{p}$. Thus the principal sum exceeds $p/2-\sqrt{p}$ and every nonprincipal sum has absolute value below $\sqrt{p}\log p$. [Lemma 1, equations (3) and (4)](https://arxiv.org/pdf/1508.05182)

For each unit $a$, cyclicity gives the indicator of the generators as

$$
\mathbf{1}_{\mathrm{gen}}(a)=\frac{\varphi(N)}{N}
  \sum_{d\mid N}\frac{\mu(d)}{\varphi(d)}
  \sum_{\operatorname{ord}\chi=d}\chi(a).
$$

To verify it, write $a=g^j$ for a fixed generator $g$. Expand the outer sum as a product over primes $r\mid N$, using the unique decomposition of each squarefree-order character into its prime-order factors. The characters of order $r$ sum to $r-1$ if $r\mid j$ and to $-1$ otherwise. The resulting factor is zero in the first case and $r/(r-1)$ in the second. Multiplication by $\varphi(N)/N$ gives the asserted indicator. After factoring out this positive prefactor, the principal coefficient is 1. The nonprincipal coefficients have total absolute value $2^k-1$, since each squarefree divisor $d>1$ contributes $\varphi(d)$ characters with coefficient of magnitude $1/\varphi(d)$. [Published character expansion, equation (5)](https://arxiv.org/pdf/1508.05182)

Multiply the indicator by $\Lambda(n)(1-n/p)$ and sum over $1\le n<p$. By the triangle inequality the resulting real sum is positive whenever

$$
2\bigl[1+(2^k-1)\log p\bigr]<\sqrt{p}. \tag{1}
$$

A positive summand has $n=q^e<p$ for a prime $q$ and integer $e\ge1$. The order of $q^e$ is $p-1$ and divides the order of $q$. Since $q$ is a unit its order divides $p-1$, proving that $q$ is a prime generator.

## Where inequality (1) holds

For $C=2^k-1$, the derivative of $(1+C\log t)/\sqrt{t}$ is $(2C-1-C\log t)/(2t^{3/2})$, which is negative when $\log t>2$. For $k\le2$ apply (1) at $t=2792$, using $\sqrt{2792}>52$ and $\log 2792<8$. For $3\le k\le9$, each column satisfies $\log(u^2)<L$ and $2[1+(2^k-1)L]<u$. Consequently (1) holds for all $p\ge u^2$ in that column.

| Distinct prime factors $k$ | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|
| $u$ | 143 | 363 | 871 | 2019 | 4321 | 9693 | 20443 |
| $L$ | 10 | 12 | 14 | 16 | 17 | 19 | 20 |

For $k=10+j$, the first ten primes have product $6{,}469{,}693{,}230>80{,}000^2$. Each further distinct prime is at least 31. Thus $p>T=80{,}000^2\,16^j$. Since $\log T<23+3j\le23\cdot2^j$, we have

$$
2[1+(2^{10+j}-1)\log T]<2[1+1024\cdot23\cdot4^j]
<80{,}000\cdot4^j=\sqrt{T}.
$$

Monotonicity gives (1) at $p$. The verifier checks all the numerical lower bounds on exponentials by summing terms of degrees 0 through 100 over the rationals. [Scalar checks](verify.py)

## Certificates for the remaining integers

It remains to check odd $p$ with $2792\le p<u^2$ and exactly $k$ distinct prime factors in $p-1$, for each of the seven columns. Factoring $p-1$ into increasing primes with positive exponents enumerates these candidates without duplication, by unique factorization. The factor 2 is mandatory. For largest factor $r$, the other $k-1$ factors have product at least the product of the first $k-1$ primes, giving the explicit upper bound on $r$ used by the verifier. The original checks also enumerated squarefree radicals and their smooth multiples separately.

Each archive member holds one little-endian 16-bit word per candidate in increasing order of $p$ for its column. If the word is $2^{14}a+b$, then $1<b<p$ and the verifier checks the following.

| $a$ | Certificate | Number verified |
|---:|---|---:|
| 0 | $b$ is a proper divisor of $p$. | 46,493 |
| 1 | The base $b$ fails Fermat's congruence, or $\gcd(b^{(p-1)/2}-1,p)$ gives a proper divisor. | 8,892 |
| 2 | $b$ is prime, $b^{p-1}\equiv1\bmod p$, and $b^{(p-1)/r}\not\equiv1\bmod p$ for every prime $r\mid p-1$. | 18,802 |

In the third case $b$ has order $p-1$, forcing $p$ itself to be prime since $\varphi(p)<p-1$ for composite $p>2$. Across all seven columns there are 74,187 candidates. The largest prime witness is 173. Lemma 2.1 of the manuscript covers the 405 odd primes below 2792, which completes the argument. [Certificate archive](x-equals-p-witnesses.zip) · [Counts and hashes by column](x-equals-p.json) · [Independent replay](verify.py)
