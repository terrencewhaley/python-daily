# Hints (smallest nudge first)

1. Write a tiny helper like `_number(text, unit)` that checks `text.endswith(unit)`, raises `ValueError` if not, then returns `int(text.removesuffix(unit).strip())`. `int("abc")` already raises `ValueError` for you, so you don't need to check digits yourself. For `pick_gpus`, `smi_output.splitlines()` plus `if not line.strip(): continue` handles the blank lines.

2. Build a list of the GPUs that qualify, then sort it with a key that puts most-free first and breaks ties by index: `key=lambda g: (-(g["mem_total"] - g["mem_used"]), g["index"])`. Slice off `[:count]`, check you actually got `count`, then `",".join(str(i) for i in sorted(...))`.
