# Language lock — context frames, KV cache, representation (2026-09-20)

**Not a submit.** The user rejected leftover / well / memory
as our slang. New speech uses field terms. Old notes still
contain the slang; this file is the translation.

---

## The three objects (field names)

**Context frames.** Real visual prefix already observed.
In our V2V jobs this is the start of the Panda file (the
runner still names it leftover). It is GT of the past, not
a generated frame. If more of the file is later admitted
as history, the context grows. T2V-from-text has no context
frames in this sense.

**KV cache.** The model’s bounded attention keys and
values for recent frames. When the window is full, tokens
evict. Forcing papers put evicted tokens into a **sink**
(copy frame 0, or EMA). Always say KV cache, not “memory.”

**Context-frame representation.** What earlier notes called
a “well”: a compact embedding or a few tokens that summarize
the current context-frame scene. Same scene → update it. A
cut → freeze it and start another. Generated frames do not
enter it.

---

## The well is not fast weights

**Fast weights** (\(W_{\text{fast}}\), TTT, Titans,
delta-rule) are rapidly updated **parameters**. We discussed
that and **dropped it** from this method.

The context-frame representation is **not** \(W_{\text{fast}}\).
It is not LoRA. It is not the KV cache. It is a small
summary of context frames sitting beside the frozen 1.3B.

If that summary is only the mean of context-frame tokens,
it is an EMA of the context frames and the method is empty.

---

## Translation table (old note → say this)

| Old note | Say to the user |
|---|---|
| leftover | context frames |
| leftover grows | more context frames are revealed |
| leftover → 30 s tail | context frames → 30 s generated continuation |
| memory | KV cache (or name the other store) |
| named evict | name the oldest KV tokens; do not drop them until the context-frame representation has used the matching context frames |
| well / scene well | context-frame representation (scene embedding / prototype) |
| leftover-only well | representation fitted on context frames only |
| leftover-EMA | EMA of context-frame tokens |
