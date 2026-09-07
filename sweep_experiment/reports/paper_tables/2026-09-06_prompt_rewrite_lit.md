# How video teams rewrite prompts (2026-09-06)

Literature + what it means for a **new motion shortlist**
and for turning motion *words* into a leftover slide.
No GPU. Do not remake cite-128. Do not start 8-GPU DMD.

Canvas: `canvases/prompt-rewrite-lit.canvas.tsx`.

0006 eyes (user): leftover camera looked still, then the
clip keeps moving **straight into the scene** (pixels expand).
Our slide is a 2-D pan (`dy`/`dx` = ±1). That operator
cannot be a zoom. Leftover mean on 0006 was
\(v_y{=}0.47\), \(v_x{=}0.21\) — a small leftover residual,
then we crawled **+y**. A forward dolly / zoom is mostly
**divergence** (outward flow). Mean flow cancels. The
1-cell floor then invents a pan the opening did not have.

---

## Three jobs the field calls “regenerate the prompt”

They are not the same paper move.

### 1. Train-time recaption (VLM watches the video)

ShareGPT4Video (GPT-4V), CogVLM2-Caption (CogVideoX),
MiraData, InstanceCap: a vision model writes a **long**
caption of the real clip — objects, actions, camera —
so the DiT trains on dense text, not a one-line web tag.

**Motivation:** the training distribution is long prompts.
Short tags under-specify motion.

**Setting:** offline, on the **training videos**. Not a
test-time controller.

### 2. Inference-time rewrite / extend (LLM, no new video)

| Team | Tool | What they ask the LLM to do | Setting |
|---|---|---|---|
| **Movie Gen** (Meta, 2024) | Llama-3 70B teacher → 8B student | Longer, more detailed user prompt. HITL pairs. | T2V inference. **Warn: too much motion detail causes artifacts.** |
| **HunyuanVideo** | Hunyuan-Large PromptRewrite | Normal = keep intent. Master = add composition, lighting, **camera**. Master can drop semantics. | T2V inference, two modes. |
| **CogVideoX** | GLM-4 / GPT (official `convert_demo`) | Expand to 50–100 words to match **train** long-text. | T2V inference. Train captions from CogVLM2-Caption. |
| **Wan 2.1 / 2.2** (our family) | Qwen2.5 or DashScope `qwen-plus` / `qwen-vl-max` | Official `prompt_extend`: 80–100 words; emphasize motion **already in the input**; add “natural actions” with simple verbs; I2V also uses the image. First-last-frame: “camera left/right/up/down.” | Official generate flag. We do **not** turn this on for V2V caption jobs. |
| **SF++ / Relax / Freq / TetherCache** | Qwen2.5-7B-Instruct | “Clarity and diversity” on MovieGen-128. | T2V 30 s / 60 s, VBench-Long. Same rewrite for every method so the table is comparable. |

**Motivation (all of them):** user text is shorter than
the captions the student saw in training. Rewrite is a
**distribution match**, not a motion controller.

Wan’s English system prompt (verbatim intent): keep
original meaning; add style / shot scale; “emphasize
motion information and different camera movements
**present in the input**”; “add natural actions of the
target using simple and direct verbs”; ~80–100 words.

That last line **will invent** “the bookshelves settle /
someone walks” on a still-room caption. That is 0002
with extra T5.

### 3. Eval-suite rewrite (not a method)

VBench’s own prompt lists are **hand-written per
dimension** (dynamic degree uses the subject-consistency
list). Nobody LLM-rewrites those for the official
leaderboard. The MovieGen-128 Qwen pass is a **field
convention** so 30–60 s T2V has enough story to keep
going. It is not “parse verbs into a flow field.”

---

## What they do **not** do

Nobody in that list turns motion words into an optical
flow and slides a mid-step guess. That job is a
**different family**:

- CameraCtrl / MotionCtrl: camera parameters or pose.
- Go-with-the-Flow: warp **starting noise** along a
  driving flow; video needs a student (we already
  refused their LoRA).
- DragNUWA / motion brushes: user draws the field.

Words → T5 is their lever. Words → leftover `(dy,dx)`
is ours, and 0006 says `(dy,dx)` is the wrong model
for in/out of the screen.

---

## Ours, so we do not mix papers

**Hypothesis 3** (already on the atlas): after the lock,
**recaption what is on screen** (VLM of generated
frames) and re-encode T5. That is “the sentence went
stale,” not “add sailing to a bookshelf.”

**This ask:** (a) shortlist clips whose text *and*
leftover already want motion; (b) maybe LLM-add motion
words; (c) maybe parse those words into the initial
slide field.

| Move | Field cousin | Risk on our protocol |
|---|---|---|
| Filter panda clips whose caption already has walk / sail / drive **and** leftover has a **lateral** pan | Eval shortlist, not a rewrite | Honest. 0006 sailing + forward camera would **fail** this filter if we require a pan. |
| Wan-style extend: add “natural verbs” to Panda first-segment | Wan official T2V/I2V extend | T5 can fight the leftover (stem-prompt lesson). Movie Gen: extra motion words → artifacts. 0002 becomes a text lie. |
| Parse “zoom in / dolly” into our current 1-cell pan | None. GwF would want a **radial** field | No-op or a false pan (0006 +y crawl). Need expand/contract, not `dx`. |
| Recaption the generated lock (H3) | LongLive user prompt-switch is occupied; on-screen recaption is not | Different question. Do not mix into the shortlist wave. |

---

## 0006 and straight-on cameras

User: leftover looked still; then the generate keeps
moving **forward** (expansion). Official leftover mean
was not zero (`v_y{=}0.47`, `v_x{=}0.21`); live fired;
we slid **+y**. Eyes: quality held, not more dynamic.

That is expected if the energy is **zoom / dolly-in**:

1. Outward flow on the left cancels inward-looking
   mean on the right. Divergence is large; mean is
   small.
2. A 1-cell **translate** cannot expand the grid.
3. The floor still shoves one axis. On 0006 that was
   vertical — a hitch, not “into the water.”

A flow check (if we want it, login CPU): leftover
Farneback **divergence** vs mean. High divergence +
low mean = this hole. Do not GPU for that.

---

## If we make a new shortlist

**Keep (one wave):** pick ~8 caption-32 / panda clips
where (1) first-segment text already names a **lateral**
action or camera pan, and (2) leftover mean
\(|v_x|\) or \(|v_y|\) is a real pan, not dust and not
mostly divergence. Run `sf_pwarp` + live. Same hold
bar. Do not rewrite the sentence on that wave.

**Do not** on the same wave: Wan-extend the still
rooms; invent zoom words; parse verbs into `(dy,dx)`.

**Later, if the pan shortlist still dies:** either
stop, or spec a **zoom** operator (radial slide of
`pred`) as its own hole — not a prompt rewrite.

No GPU until the user picks the filter-only shortlist
or A / B / C.
