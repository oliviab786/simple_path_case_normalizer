"""Public API for simple_path_case_normalizer.

Re-exports the small surface defined in :mod:`core` so that callers can use
``from simple_path_case_normalizer import normalize_path`` without knowing the
internal module layout.
"""

from .core import normalize_path, find_duplicates

__all__ = ["normalize_path", "find_duplicates"]
