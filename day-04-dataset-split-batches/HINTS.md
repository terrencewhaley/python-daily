# Hints (smallest nudge first)

1. Once you know `n_train` and `n_val`, all three sets are slices of `items`: one ends at `n_train`, the next starts there. For batching, `range(start, stop, step)` can give you the starting index of every batch.
2. Build the batches first with a list comprehension, `[items[i:i + batch_size] for i in range(0, len(items), batch_size)]`, then loop over them with `enumerate(batches, start=1)`. `batch[0]` and `batch[-1]` are the first and last items, and `len(batches)` is the total.
