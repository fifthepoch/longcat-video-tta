# KV cache vs fast weights (2026-09-20)

**Not a submit.** How the two stores are used
in the current T2V method. Slow 1.3B stays
frozen.

---

## What each one is

**KV cache.** The transformer’s usual
attention memory: keys and values of
**recent frames**. Every generated frame
is written here. Attention is
\(\mathrm{softmax}(qK^\top)V\). Entries
are **token- and position-specific**
(RoPE). The window is bounded; old tokens
leave. Self Forcing / Rolling / Reward
Forcing already do this. We did not invent
it.

**Fast weights.** A small matrix
\(W_{\text{fast}}\) (linear / delta-rule)
updated online. The next hidden state
**also** reads \(y = W_{\text{fast}}\,\phi(q)\)
(or a gated residual). That is a
**compressed association**, not a list of
frames. Only chunks that pass the opening
cloud gate are written. Session-local;
thrown away when the video ends.

---

## How they are used differently

| | KV cache | Fast weights |
|---|---|---|
| What goes in | **Every** recent frame | Only chunks whose center and spread match the first chunks |
| What is stored | Exact K,V for those tokens | A low-rank / delta map (many frames → one matrix) |
| How generate uses it | Attention over the window | Read \(W_{\text{fast}}\) as extra state (TTT / ARL²) |
| When a frame leaves | That token is gone (unless another paper’s EMA-sink) | The write can **remain** in the matrix after the tokens have left the window |
| Bound | Time window (last \(N\) tokens) | Capacity of the matrix (rank / slots) |
| Gate | None (FIFO / window) | Opening center + spread; Titans residual only **sizes** a legal write |

The KV cache answers: “what were the last
few frames, exactly, for attention?”
Fast weights answer: “what legal living
structure from this video should still
bias the next frame after those tokens
no longer fit in the window?”

They are not substitutes. Emit uses
**both**: attend to the KV cache, and
read \(W_{\text{fast}}\). EMA-sink in
Reward Forcing / MemRoPE is the
activation-space cousin of a fast-weight
write (compress evicted K,V). Ours is
**gated** and is a weight matrix, not an
EMA of every evicted token.

---

## What we do not do

Put every KV token into \(W_{\text{fast}}\)
(then the matrix is an uncompressed second
cache). Step the 1.3B from \(W_{\text{fast}}\).
Treat the KV cache as “slow weights.”
