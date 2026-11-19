# Day 10 — Checkpoint Retention
**Phase:** Python fundamentals through a JS lens · **Time:** ~25 min

Your fraud-model training job saves a checkpoint every epoch to a shared volume, and last night the volume hit 100% and killed three other teams' jobs. You want a cleanup step that keeps only the checkpoints worth having (the best few by validation loss, plus the most recent one to resume from) and lists everything else for deletion. Other files on the volume must never be touched.

## Task
Checkpoint files are named `ckpt-e<epoch>-l<loss>.pt`, e.g. `ckpt-e012-l0.4312.pt` is epoch 12 with validation loss 0.4312.

**`parse_checkpoint(name)`** → `tuple[int, float]` as `(epoch, loss)`
- Strip surrounding whitespace first.
- The name must start with `ckpt-e` and end with `.pt`; the part in between must be `<epoch>-l<loss>`.
- Return the epoch as an `int` and the loss as a `float`.
- Anything that doesn't match (wrong prefix/suffix, missing `-l`, non-numeric parts, empty string) → raise `ValueError`.

**`plan_cleanup(names, keep_best=2, keep_last=1)`** → `tuple[list[str], list[str]]` as `(keep, delete)`
- Names that `parse_checkpoint` rejects aren't checkpoints: leave them out of **both** lists.
- Keep the `keep_best` checkpoints with the **lowest** loss. On equal loss, the earlier epoch wins.
- Also keep the `keep_last` checkpoints with the **highest** epochs. A checkpoint chosen by both rules is kept once.
- Everything else goes in `delete`.
- Both lists hold the original names (stripped), sorted by epoch ascending. Input order doesn't matter.
- `keep_best` or `keep_last` negative → raise `ValueError`. `0` is allowed and means "keep none by that rule".
- No checkpoints → `([], [])`.

### Sample
```python
parse_checkpoint("ckpt-e012-l0.4312.pt")   # -> (12, 0.4312)

names = [
    "ckpt-e003-l0.5100.pt",
    "ckpt-e001-l0.9100.pt",
    "notes.txt",
    "ckpt-e005-l0.5800.pt",
    "ckpt-e002-l0.6200.pt",
    "ckpt-e004-l0.5300.pt",
]
plan_cleanup(names, keep_best=2, keep_last=1)
# keep   -> ["ckpt-e003-l0.5100.pt", "ckpt-e004-l0.5300.pt", "ckpt-e005-l0.5800.pt"]
# delete -> ["ckpt-e001-l0.9100.pt", "ckpt-e002-l0.6200.pt"]
```

## Check your work
```bash
pytest -q
```

## JS → Python
`sorted(items)` returns a new list like `[...items].sort()`, and slicing (`items[:2]`, `items[-1:]`) replaces `.slice()`. Watch one trap: `items[-0:]` is the **whole** list, because `-0` is just `0`.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
