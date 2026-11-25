# Day 14 — GPU Picker
**Phase:** Python fundamentals through a JS lens · **Time:** ~25 min

Your team shares one 4×A100 training box, and people keep launching jobs on GPU 0 out of habit while someone else's run is already maxing it out, so both crash with CUDA out-of-memory errors. You want the launch script to read `nvidia-smi`'s CSV output, pick the GPUs that are actually free, and hand back a `CUDA_VISIBLE_DEVICES` value.

## Task
The script runs `nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader`, which prints one line per GPU like:

```
0, NVIDIA A100-SXM4-40GB, 38912 MiB, 40960 MiB, 97 %
```

Implement two functions in `solution.py`:

**`parse_gpu_line(line)`** → `dict`
- Strip surrounding whitespace, split on `,`, and strip each field. There must be **exactly 5** fields.
- Return `{"index": int, "name": str, "mem_used": int, "mem_total": int, "util": int}`.
- The two memory fields must end in `MiB` and the utilization field in `%`; the number before the unit is an `int` (space before the unit is optional).
- Raise `ValueError` for anything else: wrong field count, empty name, missing/wrong unit, non-numeric numbers, empty line.

**`pick_gpus(smi_output, count, *, min_free_mib=0, max_util=10)`** → `str`
- `smi_output` is the whole multi-line output. Skip blank lines; parse every other line with `parse_gpu_line` (a bad line raises `ValueError`, don't skip it).
- Free memory is `mem_total - mem_used`. A GPU qualifies if free memory `>= min_free_mib` **and** `util <= max_util`.
- Choose the `count` qualifying GPUs with the **most free memory**. On a tie, the lower index wins.
- Return the chosen indices sorted **ascending** and joined with commas, e.g. `"1,3"`.
- `count < 1` → raise `ValueError`. Fewer than `count` GPUs qualify → raise `RuntimeError`.

### Sample
```python
smi = """
0, NVIDIA A100-SXM4-40GB, 38912 MiB, 40960 MiB, 97 %
1, NVIDIA A100-SXM4-40GB, 512 MiB, 40960 MiB, 0 %
2, NVIDIA A100-SXM4-40GB, 10240 MiB, 40960 MiB, 4 %
3, NVIDIA A100-SXM4-40GB, 0 MiB, 40960 MiB, 0 %
"""

parse_gpu_line("2, NVIDIA A100-SXM4-40GB, 10240 MiB, 40960 MiB, 4 %")
# -> {'index': 2, 'name': 'NVIDIA A100-SXM4-40GB',
#     'mem_used': 10240, 'mem_total': 40960, 'util': 4}

pick_gpus(smi, 2)                       # -> '1,3'   (most free memory)
pick_gpus(smi, 3, min_free_mib=20000)   # -> '1,2,3'
pick_gpus(smi, 4)                       # RuntimeError: GPU 0 is busy
```

## Check your work
```bash
pytest -q
```

## JS → Python
`index, name, used, total, util = fields` unpacks a list straight into names like JS's `const [index, name, used, total, util] = fields`, but Python raises `ValueError` if the count doesn't match, which you can lean on here. And `text.removesuffix("MiB")` is the tidy cousin of JS's `text.endsWith("MiB") ? text.slice(0, -3) : text`.

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
