# simple_path_case_normalizer

Normalizes path casing for case-insensitive filesystems so that paths differing only in letter case can be detected as duplicates.

```python
from simple_path_case_normalizer import normalize_path, find_duplicates

normalize_path('/Home/User/File.TXT')
# '/home/user/file.txt'

find_duplicates(['/Home/User', '/home/user', '/other'])
# [('/Home/User', '/home/user')]
```

## Why this exists

A path list assembled from a case-insensitive host (macOS, Windows) can contain two entries that name the same file but differ in case. That is harmless on the host where the list was built and a broken build on a case-sensitive one. Detecting the collision before it ships is the whole point of this library.

The trade-off is that normalisation is a plain `str.lower` and nothing else. We do not fold Unicode case in a locale-aware way, we do not resolve `..`, and we do not collapse repeated separators. Those operations change path meaning, and a duplicate detector that reports false positives is worse than one that occasionally misses a collision. Lowercasing is order-independent and stable, which is what `find_duplicates` needs.

## The awkward edge

Three paths that collide are reported as two pairs against the first-seen path, not as an all-pairs set. `find_duplicates(['/A/b', '/a/B', '/a/b'])` returns `[('/A/b', '/a/B'), ('/A/b', '/a/b')]`. If you need every colliding pair, group the input by `normalize_path` yourself; this library deliberately keeps the output linear in the number of collisions.
