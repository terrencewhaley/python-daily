# Hints (smallest nudge first)

1. For `loss_spikes`, you need "this epoch and the previous one" side by side. Slicing gives you a list shifted by one (`losses[1:]`); what built-in walks two lists in lockstep? For `early_stop`, you only need three variables as you walk: the best loss so far, its epoch, and how many epochs since it improved. And remember `0.0` is falsy, so check `is None`.

2. Spikes: `for epoch, (prev, cur) in enumerate(zip(losses, losses[1:]), start=2):` then skip if either is `None`, and collect `epoch` when `cur > prev * ratio` (a list comprehension works too). Early stop: start with `best = best_epoch = None` and `waited = 0`; loop `for epoch, loss in enumerate(losses, start=1)`, `continue` on `None`, update best when `best is None or loss < best - min_delta`, otherwise `waited += 1` and `return epoch, best_epoch` once `waited == patience`. After the loop, `return None, best_epoch`.
