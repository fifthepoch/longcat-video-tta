# Winners, losers, and a low-energy region (2026-09-08)

Follow-on to `2026-09-08_bond_dmd_bon_open.md`. User asked:
(1) use losers as negatives (e.g. 30% winners, 30% losers,
different updates); (2) an energy model that constrains
**where** low energy is allowed.

**Not a submit. No GPU.**

---

## Losers as negatives — yes, with the right update

BOND’s useful signal is often “this ranks worse than the
others.” Gui et al. do supervised copy of the best **and**
preference training on best-vs-worst. VideoDPO builds
win/lose pairs. Alice keeps some **failed** teacher videos
at low weight: drop them all and physics gets worse; weight
them equally and the student **imitates** failures.

So: do not throw losers away. Do **not** run the same
teacher-matching on them.

| Clip | Allowed update | Illegal update |
|---|---|---|
| Winner | Teacher-matching (look like Wan) and/or “this continuation is good” | — |
| Loser | Raise energy / lower chance / winner beats loser by a margin | Teacher-matching on the loser (teaches the student to **make** that failure look like Wan) |

A fixed 30% / 30% is a starting split, not a title. Say
what the 30% is **of**: several seeds from **one opening**,
or a whole batch. If we only draw four seeds, 30% is not
even one clip. Better: **best and worst of this opening**
(or best vs worse-than-median), which is BOND’s rank, not
a global percentile.

**Hard vs easy losers.** The worst 30% of a batch may be
broken pictures. Those are easy “don’t make garbage”
signals the teacher already has. The useful loser is a
**near miss**: same opening, still a legal video, worse
on the continuation judge (too still, or a new room).
If the judge is wrong, the “loser” may be the honest
living clip — then negatives **hurt**.

Alice’s 1:5 fail:success is the caution, not our number.

---

## Energy model: constrain the low-energy set

Write a score \(E(\text{video})\). The model prefers low
energy: chance \(\propto \exp(-E)\). Teacher-matching
already pushes toward “Wan-like.” An energy on the
**continuation** is a second question: “is this a good
ending of **this** opening?”

**Constrain the area allowed for low energy** means: only
a small set of videos is allowed to be easy for the
student. Two different constraints:

1. **Volume only** (any small blob). The student collapses
   to one still, one twitch, or one invented pan. That is
   reverse-KL / prefix-match / mixctx. Do not do this.
2. **Where** (a small blob **inside** “same scene and
   living,” **outside** new-room and jitter). Winners must
   sit in the low-energy well. Losers must sit outside it
   (or at least higher by a margin). That is contrastive
   energy / preference, not “make everything sharp.”

What should happen if (2) is right:

- Winner: \(E\) goes down. Teacher-matching can still
  run on that clip.
- Loser: \(E\) goes up. No teacher-matching.
- Barrier: new-scene and twitch cannot be low energy
  even if Wan would accept the picture.

What goes wrong:

- Well too tight → freeze (Rolling’s identity tax).
- Well too wide → losers still cheap, no effect.
- Teacher-matching and energy disagree → paint or
  ignore the judge (picker vs teacher).
- Energy trained on official Dynamic Degree → twitch
  gets the well (DOLLAR / our mix).

This is not a new energy-based *image* paper. It is
“BOND’s rank reward, written as an energy on
continuations, with a support constraint so the well
cannot sit on a new room.” The 30/30 split is how you
estimate that well from a few seeds. The method, if
any, is the **constraint on where the well is allowed**,
plus the vanilla winner-only teacher-matching control.

---

## Do not

Teacher-match the losers. Use official Dynamic Degree
as \(E\). Shrink the well without saying where. Launch
8-GPU before the judge that defines winner/loser is
written (same scene and living).
