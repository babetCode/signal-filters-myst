---
title: Glossary Terms
abbreviations:
  iff: if and only if
  diff: null
numbering:
  equations: false
---

:::{glossary}
Continuous time
: *Adjective* — A signal defined at every instant along a continuous time axis (often denoted $x(t)$), where $t$ can take any real value.

Deterministic
: *Adjective* — A signal or system whose future values can be exactly predicted from a known mathematical rule or past behavior, whith no randomness involved.

Discrete time
: *Adjective* — A signal defined only at specific, separate instants (denoted $x[n]$), typically obtained by sampling a continuous signal at regular intervals.

Distributed
: *Adjective* — A system whose parameters are distributed consistently over space, so behavior depends on both time and position. Described by partial differential equations (eg. a transmission line or a vibrating string).

Domain
: The set of allowed inputs for a {term}`function`.

Function
: A mathematical process that gives a unique output for each distinct input in its {term}`domain`.

Integral
: If we partition a {term}`function` $f(x)$ at several places between $x=a$ and $x=b$ (with $a<b$), with maximum partition width $k$, then let $p_i$ be the $x$ value at the start of the $i$-th partition, then the indefinite integral of $f(x)$ from $a$ to $b$ is defined as the {term}`limit`: $$\int_a^b f(x)dx = \lim_{k\rightarrow0}\left(\sum f(p_i)p_i*\right).$$

Left-hand limit
: The limit of a {term}`function` $f(x)$ as $x$ goes to $a$ from the left is defined as $$\lim_{x \rightarrow a^-} f(x) = b$$ iff for every $\epsilon > 0$, there exists some $\delta > 0$ such that for all $x \in (a-\delta, a)$, we have $$|f(x) - b| < \epsilon.$$

Limit
: The (two-sided) limit of a {term}`function` $f(x)$ as $x$ goes to $a$" is defined as $$\lim_{x \rightarrow a} f(x) = b$$ iff $b$ is equal to both the {term}`right-hand limit` and the {term}`left-hand limit`: $$\lim_{x \rightarrow a^-} f(x) = \lim_{x \rightarrow a^+} f(x) = b.$$

Linear
: *Adjective* — A system that satisfies superposition: the response to a weighted sum of inputs equals the same weighted sum of the individual responses (additivity + homogeneity/scaling).

Lumped
: *Adjective* — A system whose parameters are treated as concentrated at discrete points, ignoring spatial variation. Described by ordinary differential equations. Assumes signals act instantaneously throughout the system.

Measurement function
: *Noun* — A function that transforms the system model's state variables into the expected sensor observations.

Non-linear
: *Adjective* — A system that does not satisfy superposition; output is not simply proportional to input, and combined inputs don't produce a simply combined output.

Range
: The set of all possible outputs for a {term}`function`

Right-hand limit
: The limit of a {term}`function` $f(x)$ as $x$ goes to $a$ from the left is defined as $$\lim_{x \rightarrow a^+} f(x) = b$$ iff for every $\epsilon > 0$, there exists some $\delta > 0$ such that for all $x \in (a, a+\delta)$, we have $$|f(x) - b| < \epsilon.$$

Stochastic
: *Adjective* — A {term}`signal` or {term}`system` that involves randomness or uncertainty; its future values can only be described in terms of probabilities, not exact predictions.

System
: *Noun* — Any physical entity or group of entities, delineated by some boundary.

System input
: *Noun* — Something outside a system which causes that system to change. Also known as control inputs.

System model
: *Noun* — A mathematical representation of a system that specifies how its internal state and inputs (if any) determine its outputs, and how it evolves over time. Also known as process model.

System output
: *Noun* — A signal produced by a system model according to some set of rules or operations.

System state
: *Noun* — The minimum set of variables such that, given only their values at the present time, together with the values of the input at the present and all future times, can be used to fully determine the system's defined outputs into the future (or their probability distribution if the system includes randomness).

Time invariant
: *Adjective* — A system whose behavior/characteristics don't change over time: a time-shifted input produces an identically time-shifted output.

Time variant
: *Adjective* — A system whose behavior changes over time, so the same input applied at different times can produce different (non-shifted-equivalent) outputs.
:::