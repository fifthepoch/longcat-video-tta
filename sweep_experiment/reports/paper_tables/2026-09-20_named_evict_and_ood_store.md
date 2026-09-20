# Named evict vs an OOD store-cap (2026-09-20)

**Not a submit. No GPU.** The user asked whether
named evict has real benefits, and whether we
should only store sequences below an OOD score
so the slow object never sees broken frames.

---

## Short answers

**Named evict helps only if the slow object is
not an average.** The name is bookkeeping. The
benefit is (a) a scene cut does not smear into
the old sink, and (b) a slice cannot vanish
before the well has seen it. If sleep is “mean
of leftover tokens,” naming ≈ leftover-EMA and
our own kill test already calls that **NO**.

**An OOD cap is the right filter for generated
frames and the wrong one for leftover.** High
leftover OOD is a cut or a camera surprise, not
a broken picture. Refusing to store it makes a
conservative easy-reservoir and never opens the
new well Gap 3 needs. High *generated* OOD is
the twitch / paint the atlas already forbids
writing into anything slow.

---

## Does named evict do real work?

What EMA-sink / MemRoPE / Titans already do:
blend or decay. AdaState’s complaint is exactly
that an average cannot follow a scene change
and a static copy cannot leave frame 0.

What a **name** adds, by itself: we can point
at the leaving slice. That is not a quality
term.

What **blocked delete** adds: the well is
guaranteed to see every leftover slice that
leaves the KV window. That is the CL sentence
(fine-grained consolidation at a shift).
Without the block, we can drop a cut before
any well exists. With the block and a slow
sleep, we hitch — that is a cost, not a
quality win.

What **named + not-an-average** adds (the
only quality claim):

- Extreme leftover error → **new well**, not
  a 0.9·old + 0.1·cut blend.
- A bad *generated* write, if we ever made
  one, can be subtracted. EMA cannot unmix
  paint.

So: named evict is real against **EMA-blur at
cuts** and against **silent loss before
consolidation**. It is ceremony if the well
is a mean, and it is overhead if leftover
never cuts. That is why the kill test is
“well ≈ leftover-EMA on subject / IQ.”

We should not sell the name. We should sell
**leftover source + no blend across a cut**.
The name is how we implement “no blend.”

---

## Only store below an OOD score?

Split the stream. The same number means
opposite things.

### Generated / self-rollout (broken is possible)

**Yes: cap what the slow object is allowed
to see.** Extreme generated OOD is twitch,
paint, identity rewrite. Writing that into
a well, a sink, or a teacher-match is the
loser-matching we already closed. Low /
in-support generated may be stored if we
ever store self at all. Mid generated is
untrusted — default skip, do not let slow
weights see it.

This is Titans run **backwards** on self:
they write more of a surprising token. We
refuse to let a surprising *dream* become
cortex. That matches the atlas, not SuRe
on human text.

### Leftover / arrived camera (not a broken
generation)

**No: a one-sided cap throws away the
method.** Leftover is GT of the past. High
forecast error vs the current well is
AdaState’s “scene changed,” which is when
we **open a new well** and store that
slice there. It is not “do not store.”

A one-sided “only store leftover with OOD
< τ” does three bad things:

1. The well only sees easy leftover →
   static-sink behaviour, identity freeze.
2. Scene B never gets a well → Gap 3 is
   empty.
3. Consolidation at the shift (the CL
   open question) never happens.

Our leftover FM-OOD already failed as
“high = bad generation” (\(|\rho|\approx 0.16\),
Q3 cancel). Do not reuse that score as a
store-cap on leftover.

### The rule that is not a second method

| Slice | Low error | Mid error | Extreme error |
|---|---|---|---|
| **Leftover** | Do not write (nothing new) | Update current well | **Store as a new well.** Do not mix into the old one. Not “broken.” |
| **Generated** | Optional store if we store self at all | Do not let slow see | **Do not store.** Skip. Not a well, not a teacher target. |

That is the mid / extreme band we already
have. It is not a new knob called “max OOD
to store.” One threshold on a mixed stream
will either starve leftover cuts or admit
paint.

If we keep the method as **leftover-only
wells**, the generated row is almost idle:
slow weights never see self-rollout, so
they never see broken generated frames.
The OOD cap is then only a guard if a later
fork writes successful generated chunks
into the bank. Do not add it as a second
title.

---

## What this does to named evict

If wells are leftover-only **and** leftover
writes are banded (no blend across a cut),
named evict’s remaining job is small: name
the leaving leftover slice so it goes to
the right well, then delete. The OOD cap
on generated does not replace that — it
answers a different leak (paint in cortex).

If someone dropped named evict and only
kept “leftover-EMA of mid-band leftover,”
they would still blend through a slow
pan and they would still smear a cut if
the extreme band is off. The name is how
the extreme band *targets* a new well
instead of the old average.

---

## Do not do

- One OOD threshold on leftover+self mixed.
- Leftover FM-OOD as “broken.”
- Official Dyn as the store-cap.
- Argmax-surprise teacher-match of generated
  extremes (Alice).
- Sell “named evict” without a non-average
  slow object.
