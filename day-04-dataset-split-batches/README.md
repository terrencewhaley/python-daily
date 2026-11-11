# Day 4 — Dataset Split & Batches
**Phase:** Python fundamentals through a JS lens · **Time:** ~20 min

You're training a defect detector on a folder of product-line scans. The file list arrives already shuffled (with a fixed seed upstream), and you need to carve it into train/val/test sets, then log how the training set will be fed to the GPU in batches so you can sanity-check the run before it starts.

## Task
Implement two functions in `solution.py`:

**`split_dataset(items, train=0.8, val=0.1)`** → `tuple[list, list, list]`
- Return `(train_items, val_items, test_items)`, keeping the original order (no shuffling).
- `n_train = int(len(items) * train)` and `n_val = int(len(items) * val)`; whatever is left over goes to test.
- Raise `ValueError` if `train` or `val` is negative, or if `train + val > 1`.
- Don't modify `items`.

**`batch_labels(items, batch_size)`** → `list[str]`
- Split `items` into consecutive batches of `batch_size` (the last one may be smaller) and return one label per batch:
  - `"batch {i}/{total}: {first}..{last} ({count})"` (batches numbered from 1)
  - a batch with a single item shows just that item: `"batch {i}/{total}: {first} (1)"`
- Empty `items` → `[]`.
- Raise `ValueError` if `batch_size` is less than 1.

### Sample
```python
files = [f"scan_{i:02d}.png" for i in range(10)]   # scan_00.png … scan_09.png

train, val, test = split_dataset(files)
# train → scan_00.png … scan_07.png (8 items)
# val   → ['scan_08.png']
# test  → ['scan_09.png']

batch_labels(train, 3)
# ['batch 1/3: scan_00.png..scan_02.png (3)',
#  'batch 2/3: scan_03.png..scan_05.png (3)',
#  'batch 3/3: scan_06.png..scan_07.png (2)']

batch_labels(files[:4], 3)
# ['batch 1/2: scan_00.png..scan_02.png (3)',
#  'batch 2/2: scan_03.png (1)']
```

## Check your work
```bash
pytest -q
```

## JS → Python
Slicing `items[a:b]` is JS's `items.slice(a, b)`, and like `slice` it never throws when `b` runs past the end. `a, b, c = some_tuple` is array destructuring (`const [a, b, c] = arr`), and `enumerate(xs, start=1)` gives you the index without a manual counter, like `xs.forEach((x, i) => ...)` but 1-based.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
