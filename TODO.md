# To Do

This file contains ideas of things to do with this project. This includes edits, revisions, formatting changes, etc.... Not all ideas here are well formulated yet, some are more of a brainstorm of thing that may improve the quality of the project (or may not).

## Chapter Notes

Notes I've taken while reading through the chapter and finding places that potentially could be improved. I'm still working through them and have not proof-read all the chapters yet.

### Introduction

// LINK - notebooks/introduction.py:549
This would be better displayed as either a markdown code block or an interactive feature with editor=true (rather than code with echo=true, because the raw code does not receive syntax highlighting or line wrap in the rendered website). The style_guide.md should be updated to reflect the fact that echo=true is not recommended for use.

// LINK - notebooks/introduction.py:1202
Again, it would be better to use a markdown code cell for this, or to make it interactive with editor=true. Additionally, it should be considered whether non-ascii characters "Δx̂" are a good idea to put in the code snippet.

// LINK - notebooks/introduction.py:1337
Markdown table should always use colons so that alignmnet is intentional, rather than default. Usually columns should be either center aligned or left aligned. In this case, there should probably also be a line break before the latex equation to prevent mid-equation line wrap.


### Chapter 1

// LINK - notebooks/ch1_language_of_logic.py:681
It would be preferable if the link to chapter 2 pointed to exactly the section of chapter 2 being discussed here. I need to learn more about how internal references and links work in MySTmd [references](https://mystmd.org/spec/references), [cross-references](https://mystmd.org/guide/cross-references) so that I can make a more organized strucutre of references with rabbit-hole links. Ideally, should determine if it's possible to include my interactive outputs in the hover text as is done in the mystmd docs, and figure out how to use `kind` reference diagrams, figures, etc, and use the proof/lemma/theorem/corellary directive system to manage cross-references for the math [proofs and theorems in mystmd](https://mystmd.org/guide/proofs-and-theorems).

// LINK - notebooks/ch1_language_of_logic.py:697
Doesn't if specifically have to be a sentence (a statement where all variables are bound by quantifiers?).

// LINK - notebooks/ch1_language_of_logic.py:760
This should be using [proofs and theorems in mystmd](https://mystmd.org/guide/proofs-and-theorems). Although I'm guessing the best way to implement this will be to leave it as is in the mariom notebook and just add a function to sync_notebooks.py that uses regex to detect theorems and proofs in marimo admonition format and export to the appropriate mystmd syntax.


### Chapter 2
// LINK - notebooks/ch2_axioms_of_set_theory.py:299
The phrase "Every filter in this book is a *recursion*: it computes the {term}`estimate` $\hat x_k$ from the previous estimate $\hat x_{k-1}$ and the newest measurement $z_k$, for $k = 1, 2, 3, \ldots$" could be misinterpereted as implying that "recursion" is defined as "something that computes the estimate from the previous estimate".

// LINK - notebooks/ch2_axioms_of_set_theory.py:181
Again, these should use the lemma directive


### Chapter 3

// LINK - notebooks/ch3_sets_for_probability.py:299
Possibly confusing wording "a set of sets A is pairwise disjoint if any two distinct members of A are disjoint" could be mistakenly interpereted as "A is disjoint if at least one pair of members are disjoint"

// LINK - notebooks/ch3_sets_for_probability.py:467
The sentence structure 'A question about its value, "is $X$ in $B$?", is the set of outcomes $X^{-1}[B]$.' does not make sense to me; how could a question be a set of outcomes? Is this supposet to mean 'The answer to a question about its value, "is $X$ in $B$?", is the set of outcomes $X^{-1}[B]$.' or 'A question about its value, "is $X$ in $B$?", is answered with the set of outcomes $X^{-1}[B]$.'? Or am I misinterpereting/missing something?

Which lemma is being reference by 'The lemma says that "$X \in B$ or $X \in B'$" is the set $X^{-1}[B] \cup X^{-1}[B']$, that "not $X \in B$" is the complement $X^{-1}[B]^c$, and likewise for infinitely many conditions.'? Images? Preimages preserve set operations? Whenever a lemma is referenced, it should be clear which lemma is being specified.

// LINK - notebooks/ch3_sets_for_probability.py:1294
This interactive doesn't make sense. What is it intended to visualize? Why are the chosen intervals being chosen? Are they being chosen at random? How come sometimes the next "listed rational to aviod" is even further away fromt the interval than the previous, yet the interaval still gets smaller? do the listed rationals and the intervals have anything to do with eachother?


### Chapter 4

// LINK - notebooks/ch4_probability_spaces.py:179
$\sigma$ latex fails to render when inside of {term} directive. This is an issue in a couple other places as well. One solution to this may be to use the unicode character for sigma, but this sometimes causes errors with publishing to github and it would be better for consistency to use latex everywhere if possible.

// LINK - notebooks/ch4_probability_spaces.py:197
Internal links should specifically go to the section being referenced, rather than just going to the whole chapter (or appendix) generally (unless the whole chapter/appendix is being referenced generally). This should be the standard accross the whole book. Since this seems to be a recurring issue I will just abbreviate with "link to section" for future notes when I notice an instance of this. 

// LINK - notebooks/ch4_probability_spaces.py:370
"; we meet one below" should be replaced with. "([the example] is given as an example below)". The reader should always be given clear expectations for what to expect and should never be left in suspense.

// LINK - notebooks/ch4_probability_spaces.py:386
Another instance of latex in the {term}

// LINK - notebooks/ch4_probability_spaces.py:400
If all the $A_i$ are pairwise disjoint then shouldn't the right side (and therefore both sides of the equality) be in $[0, 1]$? I'm confused why this is $[0, \infty]$.

Another instance place that should link to section, rather than just going to the chapter (and appendix) generally.

// LINK - notebooks/ch4_probability_spaces.py:402
Chapter 6 proves the connection between what and what? This could be worded more clearly

// LINK - notebooks/ch4_probability_spaces.py:414
If you mean "the discrete probability measures theorem", then just say that rather than "the next theorem" (this eliminates all confusion of "does that mean this theorem here or the next one?")

// LINK - notebooks/ch4_probability_spaces.py:430
Sentences should only be phrased as commands when describing the math being carried out or the setup for a thought experiment (e.g. "Chose a number $p \in [0, 1]$", or "Imagine that you step on the scale"). When describing a conceptual tool that the reader may use, it is preferable to phrase it as such: "We may conceptualize $p_n$ as if it were a mass placed at the outcome..." or "$p_n$ can be thought of as a mass placed at the outcome..."

// LINK - notebooks/ch4_probability_spaces.py:435
Conversely to what? What is it being contrasted with? Or am I missinterpereting what the word "conversely" is supposed to mean here?

// LINK - notebooks/ch4_probability_spaces.py:445
link to section

// LINK - notebooks/ch4_probability_spaces.py:456


## Other Potential Revisions

As pointed out in the chapter notes, chapters should be updated to use [cross-references](https://mystmd.org/guide/cross-references) and [proof and theorems](https://mystmd.org/guide/proofs-and-theorems), using kinds and/or labels to be able to reference them.

Pureley for development purposes, it's nice to have things render properly in the marimo notebook (although this doesn't matter at all for deployment, it just makes development nicer). As such, it would be nice to establish book conventions for which marimo admonition styes ['note', 'attention', 'caution', 'danger', 'error', 'tip', 'hint', 'warning', 'important', 'info', 'success'] should get translated to which mystmd admonitions styles [note, important, hint, seealso, tip, attention, caution, warning, danger, error], that way the notebooks can be written in a way that renders during development, and then sync_notebooks can export them properly to .md. currently, seealso is being used directly in marimo and not rending properly. it would also be nice to have a dedicated marimo syntax that renders nicely which is reserved to be exported to proof/lemma/theorem directives in mystmd.