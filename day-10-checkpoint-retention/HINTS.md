# Hints (smallest nudge first)

1. For `parse_checkpoint`, check `startswith("ckpt-e")` and `endswith(".pt")`, then slice out the middle. Unpacking does a lot of the validation for you: `epoch_text, loss_text = middle.split("-l")` already raises `ValueError` if there isn't exactly one `-l`, and so do `int(...)` and `float(...)` on bad text.

2. For `plan_cleanup`, build a list of `(epoch, loss, name)` tuples, skipping names that raise (`try` / `except ValueError: continue`). Sort it two ways: by `(loss, epoch)` for the best ones and by epoch for the latest ones, then slice each. Collect the kept names in a `set` so overlaps count once. Careful with `keep_last=0`: `lst[-0:]` is the whole list, so slice from `len(lst) - keep_last` instead.
