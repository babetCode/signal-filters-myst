# To Do

This file contains ideas of things to do with this project. This includes edits, revisions, formatting changes, etc.... Not all ideas here are well formulated yet, some are more of a brainstorm of thing that may improve the quality of the project (or may not).

## Chapter Notes

Notes I've taken while reading through the chapter and finding places that potentially could be improved. I'm still working through them and have not proof-read all the chapters yet.

### Introduction

// LINK - notebooks/introduction.py:544
This would be better displayed as either a markdown code block, because editor=true is supposed to be reserved for interactive code where the user is invited to edit it and it will create new/ different output.

// LINK - notebooks/introduction.py:1348
Markdown table should have a line break before the latex equation to prevent mid-equation line wrap.


### Chapter 1

// LINK - notebooks/ch1_language_of_logic.py:671
It would be preferable if the link to chapter 2 pointed to exactly the section of chapter 2 being discussed here.

// LINK - notebooks/ch1_language_of_logic.py:705
Doesn't if specifically have to be a sentence (a statement where all variables are bound by quantifiers?).


### Chapter 2
// LINK - notebooks/ch2_axioms_of_set_theory.py:85
The phrase "Every filter in this book is a *recursion*: it computes the {term}`estimate` $\hat x_k$ from the previous estimate $\hat x_{k-1}$ and the newest measurement $z_k$, for $k = 1, 2, 3, \ldots$" could be misinterpereted as implying that "recursion" is defined as "something that computes the estimate from the previous estimate".


### Chapter 3

// LINK - notebooks/ch3_sets_for_probability.py:296
Possibly confusing wording "a set of sets A is pairwise disjoint if any two distinct members of A are disjoint" could be mistakenly interpereted as "A is disjoint if at least one pair of members are disjoint"

// LINK - notebooks/ch3_sets_for_probability.py:463
The sentence structure 'A question about its value, "is $X$ in $B$?", is the set of outcomes $X^{-1}[B]$.' does not make sense to me; how could a question be a set of outcomes? Is this supposet to mean 'The answer to a question about its value, "is $X$ in $B$?", is the set of outcomes $X^{-1}[B]$.' or 'A question about its value, "is $X$ in $B$?", is answered with the set of outcomes $X^{-1}[B]$.'? Or am I misinterpereting/missing something?

Which lemma is being reference by 'The lemma says that "$X \in B$ or $X \in B'$" is the set $X^{-1}[B] \cup X^{-1}[B']$, that "not $X \in B$" is the complement $X^{-1}[B]^c$, and likewise for infinitely many conditions.'? Images? Preimages preserve set operations? Whenever a lemma is referenced, it should be clear which lemma is being specified.

// LINK - notebooks/ch3_sets_for_probability.py:1294
This interactive doesn't make sense. What is it intended to visualize? Why are the chosen intervals being chosen? Are they being chosen at random? How come sometimes the next "listed rational to aviod" is even further away from the interval than the previous, yet the interaval still gets smaller?

### Chapter 4

// LINK - notebooks/ch4_probability_spaces.py:197
Internal links should specifically go to the section being referenced, so link to De Morgan's laws for families rather than all of chapter 3

// LINK - notebooks/ch4_probability_spaces.py:367
"; we meet one below" should be replaced with. "([the example] is given as an example below)". The reader should always be given clear expectations for what to expect and should never be left in suspense.

// LINK - notebooks/ch4_probability_spaces.py:396
If all the $A_i$ are pairwise disjoint then shouldn't the right side (and therefore both sides of the equality) be in $[0, 1]$? I'm confused why this is $[0, \infty]$.

// LINK - notebooks/ch4_probability_spaces.py:398
Chapter 6 proves the connection between what and what? between probabilities combining and what they mean? or between long term frequency and degree of belief? This could be worded more clearly

// LINK - notebooks/ch4_probability_spaces.py:432
Conversely to what? What is it being contrasted with? Or am I missinterpereting what the word "conversely" is supposed to mean here?

