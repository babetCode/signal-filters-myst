---
title: Glossary
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

Filter
: *Noun* — Any algorithm that selectively modifies or removes noise from a signal.

Left-hand limit
: *Noun* — The left-hand limit $$\lim_{x \rightarrow a^-} f(x)$$ (read "limit of $f(x)$ as $x$ goes to $a$ from the left") equals $b$ iff for every $\epsilon > 0$, there exists some $\delta > 0$ such that for all $x \in (a-\delta, a)$, we have $$|f(x) - b| < \epsilon.$$

Limit
: *Noun* — The (two-sided) limit $$\lim_{x \rightarrow a} f(x)$$ (read "limit of $f(x)$ as $x$ goes to $a$") equals $b$ iff $$\lim_{x \rightarrow a^-} f(x) = \lim_{x \rightarrow a^+} f(x) = b.$$

Linear
: *Adjective* — A system that satisfies superposition: the response to a weighted sum of inputs equals the same weighted sum of the individual responses (additivity + homogeneity/scaling).

Lumped
: *Adjective* — A system whose parameters are treated as concentrated at discrete points, ignoring spatial variation. Described by ordinary differential equations. Assumes signals act instantaneously throughout the system.

Measurement function
: *Noun* — A function that transforms the system model's state variables into the expected sensor observations.

Noise
: *Noun* — Any unwanted, unpredictable, or random component added to a signal that degrades or obscures the information it carries.

Non-linear
: *Adjective* — A system that does not satisfy superposition; output is not simply proportional to input, and combined inputs don't produce a simply combined output.

Right-hand limit
: *Noun* — The right-hand limit $$\lim_{x \rightarrow a^+} f(x)$$ (read "limit of $f(x)$ as $x$ goes to $a$ from the right") equals $b$ iff for every $\epsilon > 0$, there exists some $\delta > 0$ such that for all $x \in (a, a+\delta)$, we have $$|f(x) - b| < \epsilon.$$

Signal
: *Noun* — Any function that represents how a quantity varies over time or space.

Stochastic
: *Adjective* — A signal or system that involves randomness or uncertainty; its future values can only be described in terms of probabilities, not exact predictions.

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


## Index

```{show-index}

```