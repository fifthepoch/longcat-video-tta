# Slide-the-guess: interpretation gaps and failure points (2026-09-06)

Not a harvest. pwarp jobs **17058386–393** may still be
on disk. Pull the command block in chat before changing
code. **No 8-GPU DMD. No remake cite-128.**

---

## Two interpretations (do not mix)

**Yours.** After pass 1, move the guessed *picture* so the
remaining passes cannot stay a still. Direction from the
real 2 s leftover. If a frozen strip would vote “do not
move,” do not listen to it.

**What I ran first (extras).** Drift the *snow*. That died
(Imaging Quality 49 / 54) because we locked one noise
stencil for 30 s. That was not your idea.

**What I ran second (`sf_pwarp`).** Closer, but I added
choices you did not state. Those choices can kill the
photograph even if “slide the guess” is right.

I have **not** harvested pwarp numbers in this note. If
Imaging Quality is ~50, treat it like lastmix-class paint
until the per-clip table says which hole fired.

---

## Where I drifted from your sentence

| # | Your sentence | What I coded | Why I did it | Why it can fail |
|---|---|---|---|---|
| 1 | Move the guessed picture | Rigid translate of the **whole 3-latent strip** by the same \((dy,dx)\) | Simplest integer slide | The three frames stay a still *relative to each other*. You get a hitch every ~0.75 s, not living motion inside the strip. |
| 2 | Leftover mean for direction | Farneback **mean**, then **dominant axis only** (up/down *or* left/right) | Tiny leftover on the truck was 0.004 cells / frame | Throws away diagonal motion. A person walking while the camera sits still averages toward zero. |
| 3 | Force motion if freeze would vote zero | **1 latent cell every strip**, from strip 1 | Faithful leftover speed never crosses 1 cell | ~40 slides × 8 pixels ≈ **320 px crawl** over 30 s. That is a new camera, not “continue the opening.” |
| 4 | Remaining passes finish the shift | Slide only after pass 1; extras stay white | Isolate from the dead stencil | Later passes + leftover in memory can **pull the picture back**. Two steps left cannot hide a seam (lastmix / restep). |
| 5 | Fill the new edge | **Repeat** the last row/column | No wrap, no noise in the photo | Edge smear / stretch. Imaging Quality death that looks like paint. |
| 6 | (unstated) memory | Leftover KV **does not slide** | Sliding prefix tokens paints the real opening | Spatial seam: current tokens are a translated bathroom; cache is the untranslated leftover. |
| 7 | When to start | Every strip from the first generated block | Same-wave always-on | Early strips hitch against a still-healthy leftover. Your later-chunk instinct was not in this wave. |

---

## Failure points (one at a time)

Confirm with the cluster dump, then change **one** row.

### F1 — Later passes undo the slide

**Look for:** live skip tails = Self Forcing, but always-on
tails ≈ host and official dynamic still 0/8. Sidecar
`n_shifts` high, videos look like the host with a faint
hitch.

**Fix (only if F1):** slide after **every** pass, or slide
`noisy` after `add_noise` too, still no extra-nwarp.

### F2 — KV seam / leftover does not move

**Look for:** Imaging Quality 50s **and** subject drop
(face/truck morphs), flicker in the 0.978 band, first
chunk already worse than later (seam at leftover | gen).

**Fix (only if F2):** do **not** slide against the leftover.
Start slides only after chunk 2 (history is already our
pixels). Or mix: `pred ← (1-α) pred + α shift` with
α ≈ 0.25. Do not translate the real leftover in KV
(that paints the opening).

### F3 — 1 cell / strip is a violent pan

**Look for:** subject collapse, background still “a room”
but the camera crawls; tail motion up; official dynamic
maybe up; Imaging Quality maybe holds or dies from smear.

**Fix (only if F3):** 1 cell per **chunk** (~2 s), or ramp
0 → 1 only after 10 s. Keep leftover *sign*.

### F4 — Whole-strip rigid translate (no intra-strip motion)

**Look for:** hitch-hitch-hitch, each 0.75 s still looks
frozen between hitches. Official dynamic stays 0. Tail
may rise from the hitch alone.

**Fix (only if F4):** shear: latent frame \(i\) in the
strip shifts by \(i \cdot v\) (or 0, 1, 2 cells). The
strip itself is no longer a still.

### F5 — Edge replicate paints

**Look for:** Imaging Quality death, aesthetic down,
stretched borders, flicker OK-ish.

**Fix (only if F5):** fill the new edge from the last
leftover / last locked frame (content that should enter),
not a repeated column.

### F6 — Mean flow is the wrong direction

**Look for:** leftover `vy_px` ≈ 0 on clips that clearly
move (0001 kitchen, 0006 boat). Live gate fires on
`prefix_motion` but `dy=dx=0` because mean cancelled.

**Fix (only if F6):** use leftover **median** flow, or
magnitude-weighted mean, or the live `prefix_motion`
axis only as a “something moved” bit and pick the
axis from the largest |mean| among a 3×3 spatial grid
(still not a full field).

### F7 — Student never saw a slid guess (4-step budget)

**Look for:** same letter as lastmix (identity or IQ
collapse) even after F3/F4 soften. Smoke already dead.

**Fix:** stop. That is the frozen-student hole. Do not
stack extras + pred. Do not start 8-GPU DMD tonight.

---

## What I would not change yet

Do not reuse the 30 s extra stencil. Do not wrap. Do not
RAFT on half-clean `pred`. Do not combine holes in one
wave. Same-wave always-on + live stays.

---

## Cluster pull (paste the whole block)

See the command block in the chat that asked for this
note. First sidecar must show `prompt_source=metadata_csv`
and `pwarp.dy` / `dx` / `n_shifts`.
