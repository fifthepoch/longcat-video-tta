# What coinc-8 tested vs what the field tests (2026-09-22)

**Not a submit. No GPU.** After the user asked
to scrutinize the approach and whether we
should gate the **KV cache** instead.

---

## How the other teams get intuition

They change **the object they claim**, on a
cheap clip, and look.

| Team | Claim | Cheap test |
|---|---|---|
| LongLive | Recache at a new sentence | 10 s, one switch: keep KV vs drop KV vs rebuild KV. CLIP + consistency. |
| Rolling / RF | First-chunk or EMA **sink** | Same student, sink on vs off. Dyn vs identity. |
| ARL² | Replace cross-frame attention | Swap **one** layer, VBench recovery. IQ is the fragile dim. |
| TTT-Video | New TTT layer | Prior: ungated add wrecks a pretrained residual. They gate \(\alpha\approx 0\) **before** 256 H100s. |
| Video-T1 / CachedSearch | Search | Search vs not; no new store. |

None of them invented a second matrix the
student had never seen, wrote into it, and
called that a test of a timing rule. If the
paper is about the KV cache, the 10 s
ablation is on the KV cache.

---

## What we did

We wanted a coincidence rule for “when
motion is real.” We attached it to a
**zero-init DeltaNet** on a **frozen**
Self Forcing student and added
\(0.15\,W\phi(q)\) into attention. The
eight then answered: “does an untrained
write destroy the picture?” Yes (IQ 56,
Dyn 8/8 twitch). It did **not** answer:
“does coincidence select?” \(C\approx 0.91\),
48/48 writes, 40/40 fork. Isolation vs
mean-energy and vs Titans was already
dead on the log.

The clean KV arm was already in the
table: `sf_window` (last 21, sink=0, no
\(W\)). That held IQ (−0.49). We
under-weighted it.

---

## What was logically wrong

1. **Wrong object.** Forcing students
   emit from KV + text. TTT/ARL² only
   read \(W\) after an outer train. We
   used their *read* without their
   *install*. That is not a cheap version
   of their method. It is a different,
   illegal store.

2. **We already had the law.** 2026-09-04:
   selection is safe; editing the host
   sampler / KV write / weights is not.
   AdaSteer, nwarp, leftover \(\rho\)
   already painted. Coinc-8 was that
   class again.

3. **The gate was never on.** Two gates
   (tape + cloud) and both said yes /
   fork. We tested “write every strip
   into \(W\).”

4. **Titans was not Titans.** Residual
   \(\eta\) saturated at 0.3. We did not
   isolate an integrator.

5. **“Update” was not AdaSteer.** The
   write was an outer product, not a
   video loss. That was not said clearly
   enough before launch.

6. **We paid four dying arms** for a
   question `sf_window` vs `notta` had
   already framed: eviction is fine;
   injecting a new store is not.

---

## KV admission is the object that matches
the field’s cheap test

Gating **which tokens enter or stay in the
KV cache** is what LongLive / Rolling / RF
actually ablate. Coincidence can be that
admission rule: many cells changing
together in a short window → those tokens
may stay; a still or a one-cell twitch
does not get to occupy the window.

Occupied: recency window, first-chunk
sink, EMA sink, recache-on-new-text.
Unused (thin): coincidence as the
*which-tokens* mask on a Forcing window,
no second matrix, no 32 GPU-day tune.

Cheap test, their style: first-8,
`notta` / `sf_window` (already have) /
coinc-gated eviction. No \(W\). IQ must
hold. Extra Dyn must not be flicker.
Do not letter n=8. Do not launch 128.
Do not retune coinc-8’s \(\beta\).
