# Handoff: sponsor summer report (writing project)

**To the agent taking this over.** This is a
**writing / disclosure** project, not a GPU
job. The science line (search vs KV, no
launch until the user picks) stays in
`AGENTS.md` and
`2026-09-22_search_kv_open_challenges.md`.
Do not mix unpublished recipes into the
partner note.

**Report (the deliverable):**
`sweep_experiment/reports/paper_tables/2026-09-20_sponsor_summer_report.md`

**Figures:**
`sweep_experiment/reports/paper_tables/sponsor_summer_2026_figures/`

**Plot / strip scripts:**
`scripts/plot_sponsor_summer_figures.py`,
`scripts/export_sponsor_frame_strips.py`

Updated 28 September 2026: late-September
experimental class is now in the report
without method names. Continue from the
checklist at the bottom.

---

## What this writing project is

A short confidential progress note for an
**external company that funds the work**.
It covers long-horizon video generation,
May–September 2026.

It is **not** the academic paper, not
`paper/main.tex`, and not a method spec.
The user asked for lab-style disclosure:
problem, class of approach, measured
outcomes. Mirror what OpenAI / Anthropic
technical reports **withhold** (recipes,
hyperparameters, unpublished
interventions), not their marketing tone.

Length: relatively short, long enough to
walk through major findings and show
figures. Prose first. Bullets are allowed;
the whole note must not be a bullet dump.

---

## Criteria the user set (initial)

From the 20 September request:

1. Short enough for a sponsor; long enough
   for major findings and interesting work.
2. Keep technical methods **ambiguous**.
3. Explain why we moved from **parameter
   space** to **sampling space** and
   **distillation** without naming the
   exact method under investigation.
4. State the **research direction** in
   general terms; do not give away the
   unpublished recipe.
5. Bullet points are fine; do not write
   the entire report as bullets.
6. Mirror commercial-lab technical reports
   on **what they do not disclose**.
7. Need **data visualizations** and
   **frame-by-frame** video showcases.

Official quality in any number we show:
full-clip VBench. Dynamic Degree = **share
of clips** that are living, not a median.
Do not treat n=2 / n=8 protocol smokes as
headline results (except as a clearly
labeled quality veto, as of 28 September).

---

## Criteria added along the way

8. **Do not reveal too many implementation
   details to the external funder.** This
   is the last standing writing rule. If a
   sentence would let a competent reader
   rebuild the unpublished controller,
   cut it.

9. It is okay to present **always-on seed
   search** (Best-of-N) as a measured
   lever. **Do not present seed search as
   if we invented it.** The only thing we
   must not mention is **our own
   unpublished method**.

10. Do not name Pseudo-future Search,
    leftover ρ, nwarp / pwarp, coincidence
    writes, DeltaNet, Azouz / König,
    prefix-protected fast weights, whole-
    latent KV admission, or any other
    internal code name.

11. Field language if you must speak
    internally: **context frames**, **KV
    cache**, **fast weights**. In the
    sponsor note, prefer ordinary
    English: opening frames, attention
    window, session-local store.

12. Frame strips: matched cite-128 clips;
    top = published few-step baseline,
    bottom = always-on seed search. User
    picked living-vs-still examples
    (panda 0003 / 0001 on cluster). Local
    iCloud dehydrates; regenerate on the
    cluster if a PNG is missing.

13. Laptop SSH/SCP host is `wc3013@torch`
    only. Never invent `torch-login-*`
    FQDNs.

---

## What is already in the report

| Section | Status |
|---|---|
| Disclosure header (OpenAI / Anthropic withhold) | Done |
| Problem (30–60 s freeze / twitch / rewrite) | Done |
| Why parameter-space TTA was left (N=1000 null, router flip, 60 s δ null, TTC cite) | Done + fig1–2 |
| Why sampling / distillation (drift fig3; classes not recipes) | Done |
| Cite-128 table: few-step / streaming / always-on seed search | Done + fig4–6 |
| Other sampling classes as **classes** (reward-to-opening, pin opening, noise-path edits) | Done |
| Frame strips fig7 (became living) / fig8 (stayed static) | Done |
| Late September: untrained session-local store **NO**; cache-admission idea dropped; no scale | **Added 2026-09-28** |
| Direction: remaining published holes are search vs KV; no recipe | **Rewritten 2026-09-28** (old text leaked “remember the opening / refuse a freeze”) |
| Limitations, including n=8 veto | Updated 2026-09-28 |

Internal numbers the report is allowed to
use (already public-facing in the note):
few-step 0.666 / 72.07 / 32.8% (42/128) /
108 s; streaming 0.685 / 71.52 / 28.9% /
47 s; always-on search 0.661 / 72.19 /
50.8% (65/128) / 354 s; ~3× cost; 25
clips became living, 2 lost, 40 already
living, 61 stayed still.

Late September (disclosed only as a
class): IQ about −17, subject about
−0.34, Dyn marked 8/8 but flicker; window
without the extra store held IQ. **Do not
add** MovieGen, job IDs, arm names, or
write-tape statistics to the partner
note.

---

## What you must not put in the report

These exist in this repo and must stay
**out** of the sponsor file:

- Coincidence first-8, Titans / writeevery
  / meandelta arms, \(C\), cloud
  \(\tau\), \(\eta_{\max}\)
- Prefix-protect first-8 spec (never
  launched)
- Whole-latent KV admission
- nwarp / pwarp / leftover ρ / mix /
  FIFO / schedule8 harvests
- “Pseudo-future Search” as a title
- Artificial Individuality (different
  project; not this briefing)

If you need the science record, read
`2026-09-22_t2v_coinc8_quality.md` and
`2026-09-22_search_kv_open_challenges.md`.
Translate into the sponsor note only at
the **class + outcome** level.

---

## Where the previous agent left off

The partner note is substantively
complete for May–September plus the
late-September veto. Remaining writing
work (this is where you continue):

1. **Leak pass.** Read the report as a
   funder with a video-generation staff.
   Cut any sentence that names or
   reconstructs an unpublished
   controller. The 28 September rewrite
   already removed the “remember the
   opening / refuse a freeze” next-step
   paragraph.

2. **Figure completeness.** Confirm all
   eight PNGs exist and render. If
   dehydrated locally, regenerate; do
   not invent new clips. Scripts above.
   User already approved fig7 = search
   woke a still; fig8 = both stay still.

3. **Sponsor packaging** if the user
   asks: a clean PDF or a copy with
   figures inlined. Do not start a PDF
   unless they ask. Do not `git add`
   from the iCloud tree; push via the
   `/tmp` clone pattern in `AGENTS.md`
   §5.

4. **Do not** add new experiments to
   this note unless the user asks, and
   then only as a class + official
   full-clip outcome. Do not letter n=2.
   Do not launch 128. Do not reopen
   coincidence or KV-admission in the
   briefing.

5. If the user wants the note shorter
   still, cut from “Why sampling space”
   repetition and keep the 128-clip
   table + two strips + the late-
   September veto.

---

## Continue

Please take over `2026-09-20_sponsor_summer_report.md`.
Run the leak pass first. Then ask the
user whether they want a PDF or any
length cut before you change tone or
add figures. Keep the disclosure rules
above even if they ask for “more
technical detail” — push back and offer
a class-level sentence instead.
