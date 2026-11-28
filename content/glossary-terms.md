---
title: Glossary
---

:::{index}
single: index one
single: index parent; index child
pair: index two; index three
pair: index four; index five
triple: index six; index seven; index eight
:::

:::{glossary}

Continuous time
: (Of a {term}`signal`) defined at every instant along a continuous time axis (often denoted $x(t)$), where $t$ can take any real value.

Discrete time
: (Of a {term}`signal`) defined only at specific, separate instants (denoted $x[n]$), typically obtained by sampling a continuous signal at regular intervals.

Distributed
: (Of a {term}`system`) having parameters distributed consistently over space, so behavior depends on both time and position. Described by partial differential equations (eg. a transmission line or a vibrating string).

Integral
: 1. The **definite integral** of a {term}`function` $f(x)$ from $a$ to $b$ is the exact signed area under the curve $y = f(x)$ over $[a,b]$, defined as the {term}`limit` of the {term}`riemann sum` as the partition's maximum subinterval width goes to zero. Applying the definition of the limit, this means that the integral of $f(x)$ over $[a,b]$ is defined as
  $$\int_a^b f(x) \, dx := I$$
  iff for every $\epsilon > 0$, there exists a $\delta > 0$ such that for any partition $P$ with maximum subinterval width less than $\delta$ and any choice of sample points $x_i^* \in [x_{i-1}, x_i]$, we have
  $$\left\vert{} \left( \sum_{i=1}^{n} f(x_i^*) \Delta x_i \right) - I \right\vert{} < \epsilon.$$
  
  2. The **indefinite integral** of a {term}`function` $f(x)$ represents the set of all {term}`antiderivatives <antiderivative>` of $f(x)$:
  $$\int f(x) \, dx := F(x) + C,$$
  where $C$ is the constant of integration that accounts for every vertical shift.

  By the Fundamental Theorem of Calculus, the definite integral of $f(x)$ over $[a,b]$ equals the difference between any antiderivative evaluated at $b$ and $a$:
  $$\int_a^b f(x) \, dx = F(b) - F(a).$$

Left-hand limit
: The limit of a {term}`function` $f(x)$ as $x$ goes to $a$ from the left is defined as $$\lim_{x \rightarrow a^-} f(x) := b$$ iff for every $\epsilon > 0$, there exists some $\delta > 0$ such that for all $x \in (a-\delta, a)$, we have $$|f(x) - b| < \epsilon.$$

Limit
: The (two-sided) limit of a {term}`function` $f(x)$ as $x$ goes to $a$ is defined as $$\lim_{x \rightarrow a} f(x) := b$$ iff $b$ is equal to both the {term}`right-hand limit` and the {term}`left-hand limit`: $$\lim_{x \rightarrow a^-} f(x) = \lim_{x \rightarrow a^+} f(x) = b.$$

Linear
: *Adjective* — A system that satisfies superposition: the response to a weighted sum of inputs equals the same weighted sum of the individual responses (additivity + homogeneity/scaling).

Lumped
: *Adjective* — A system whose parameters are treated as concentrated at discrete points, ignoring spatial variation. Described by ordinary differential equations. Assumes signals act instantaneously throughout the system.

Non-linear
: *Adjective* — A system that does not satisfy superposition; output is not simply proportional to input, and combined inputs don't produce a simply combined output.

Right-hand limit
: The limit of a {term}`function` $f(x)$ as $x$ goes to $a$ from the right is defined as $$\lim_{x \rightarrow a^+} f(x) := b$$ iff for every $\epsilon > 0$, there exists some $\delta > 0$ such that for all $x \in (a, a+\delta)$, we have $$|f(x) - b| < \epsilon.$$

Stochastic
: (Of a {term}`signal` or {term}`system`) involving randomness or uncertainty; its future values can only be described in terms of probabilities, not exact predictions.

System input
: Something outside a {term}`system` which causes that system to change. Also known as control inputs.

System model
: A mathematical representation of a {term}`system` that specifies how its internal {term}`state <system state>` and inputs (if any) determine its outputs, and how it evolves over time. Also known as process model.

System output
: A {term}`signal` produced by a {term}`system model` according to some set of rules or operations.

Time invariant
: (Of a {term}`system`) not changing over time: a time-shifted input produces an identically time-shifted output.

Time variant
: (Of a {term}`system`) changing over time, so the same input applied at different times can produce different (non-shifted-equivalent) outputs.
:::

## Index

```{show-index}

```