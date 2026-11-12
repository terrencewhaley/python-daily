# Day 5 — Image Tag Audit
**Phase:** Python fundamentals through a JS lens · **Time:** ~25 min

Your team's Kubernetes manifests reference container images for the model-serving stack. Twice this month a pod quietly pulled a new `:latest` image and changed model behaviour, and once someone deployed from a public registry by mistake. You want a pre-deploy check that parses every image reference and flags the risky ones.

## Task
Implement two functions in `solution.py`:

**`parse_image(ref)`** → `tuple[str, str, str]` as `(registry, repo, tag)`
- Strip surrounding whitespace first. Raise `ValueError` if the ref is empty.
- Split on `/`. The **first** segment is the registry only if there is more than one segment **and** that first segment contains a `.` or a `:`, or is exactly `localhost`. Otherwise the registry is `"docker.io"` and every segment belongs to the repo.
- The tag comes after a `:` in the **last** segment only (a `:` in the registry is a port, not a tag). No tag → `"latest"`.
- Raise `ValueError` if there's a `:` but the tag after it is empty (e.g. `acme/x:`).
- `repo` is the remaining segments joined with `/` (no tag). Don't add Docker Hub's `library/` prefix.

**`audit_images(refs, allowed_registries=("ghcr.io",))`** → `list[str]`
- Walk `refs` with positions counting from **1** (blank/whitespace-only entries are skipped but still count as a position, so numbers match the manifest).
- For each ref (shown stripped), emit lines in this order:
  - unparseable → `"#{n} {ref}: invalid reference"` (and nothing else for it)
  - registry not in `allowed_registries` → `"#{n} {ref}: registry '{registry}' not allowed"`
  - tag is `latest` → `"#{n} {ref}: unpinned tag 'latest'"`
- Return `[]` when nothing is wrong.

### Sample
```python
parse_image("ghcr.io/acme/fraud-detector:v7")    # ('ghcr.io', 'acme/fraud-detector', 'v7')
parse_image("redis:7.2")                         # ('docker.io', 'redis', '7.2')
parse_image("localhost:5000/models/churn:dev")   # ('localhost:5000', 'models/churn', 'dev')
parse_image("acme/feature-store")                # ('docker.io', 'acme/feature-store', 'latest')

refs = [
    "ghcr.io/acme/fraud-detector:v7",
    "redis:7.2",
    "   ",
    "ghcr.io/acme/feature-store",
    "localhost:5000/models/churn:dev",
]
audit_images(refs)
# [
#   "#2 redis:7.2: registry 'docker.io' not allowed",
#   "#4 ghcr.io/acme/feature-store: unpinned tag 'latest'",
#   "#5 localhost:5000/models/churn:dev: registry 'localhost:5000' not allowed",
# ]
```

## Check your work
```bash
pytest -q
```

## JS → Python
`for n, ref in enumerate(refs, start=1)` is Python's version of `refs.forEach((ref, i) => …)` with the index already shifted, and `name, tag = last.rsplit(":", 1)` unpacks like `const [name, tag] = …` (but raises if the count doesn't match).

Stuck? Ask Claude Code for a hint (see `HINTS.md`, but try not to peek).
