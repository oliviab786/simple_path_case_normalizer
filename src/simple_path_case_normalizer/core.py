"""Path case normalisation for case-insensitive filesystem inspection.

The problem this module solves is narrow: given a list of paths that may have
been produced on different machines (or by different tools on the same machine),
find pairs that differ only in letter case. On a case-insensitive filesystem
those paths refer to the same file, so shipping both is a bug that is invisible
until it reaches a case-sensitive host.

The normalisation choice is deliberate and simple: *lowercase everything*. We do
not attempt to preserve the casing of the first occurrence, because that would
make the result depend on input order and would hide the duplicate rather than
surface it. Lowercasing is stable, order-independent, and easy to reason about.

Only the path string is normalised. No filesystem access is performed, so the
function works with paths that do not exist on the current machine.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

__all__ = ["normalize_path", "find_duplicates"]


def normalize_path(path: str) -> str:
    """Return *path* lowercased for case-insensitive comparison.

    The transformation is intentionally total: every character is passed
    through :meth:`str.lower`. We do not collapse separators, resolve ``..``,
    or strip trailing slashes, because those operations change path meaning and
    would make the duplicate detector report false positives for paths that are
    genuinely different.

    >>> normalize_path('/Home/User/File.TXT')
    '/home/user/file.txt'
    """
    if not isinstance(path, str):
        raise TypeError(f"path must be str, got {type(path).__name__}")
    return path.lower()


def find_duplicates(paths: Iterable[str]) -> List[Tuple[str, str]]:
    """Find pairs of paths that collide after case normalisation.

    Returns a list of ``(first_seen, later_seen)`` tuples. ``first_seen`` is the
    path that appeared earlier in *paths*; ``later_seen`` is the one that
    collided with it. The original (un-normalised) strings are returned, so the
    caller can report the real names.

    Only the first colliding pair for a given normalised key is reported. If
    three paths collide, the second and third are each reported against the
    first, giving two tuples rather than three. This keeps the output linear in
    the number of collisions and avoids an O(n^2) all-pairs explosion.

    >>> find_duplicates(['/A/b', '/a/B', '/a/b'])
    [('/A/b', '/a/B'), ('/A/b', '/a/b')]
    """
    seen: Dict[str, str] = {}
    duplicates: List[Tuple[str, str]] = []
    for path in paths:
        key = normalize_path(path)
        if key in seen:
            duplicates.append((seen[key], path))
        else:
            seen[key] = path
    return duplicates
