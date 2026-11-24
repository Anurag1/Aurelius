"""Validated synthetic spectral-loss profiles used by controlled experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class SpectralLossProfile:
    """A simulated frequency-dependent attenuation curve.

    The profile is intentionally not represented as an audiogram. Values are
    attenuation magnitudes in dB for a synthetic channel simulation, not
    measured hearing thresholds and not fitting prescriptions.
    """

    frequencies_hz: tuple[float, ...]
    attenuation_db: tuple[float, ...]
    profile_id: str = "synthetic-profile"

    def __post_init__(self) -> None:
        f = np.asarray(self.frequencies_hz, dtype=float)
        a = np.asarray(self.attenuation_db, dtype=float)
        if f.ndim != 1 or a.ndim != 1 or len(f) != len(a) or len(f) < 2:
            raise ValueError("frequencies_hz and attenuation_db must be 1-D, equal-length arrays (>=2)")
        if not np.all(np.isfinite(f)) or not np.all(np.isfinite(a)):
            raise ValueError("profile values must be finite")
        if np.any(f <= 0) or np.any(np.diff(f) <= 0):
            raise ValueError("frequencies_hz must be positive and strictly increasing")
        if np.any(a < 0) or np.any(a > 60):
            raise ValueError("synthetic attenuation must be within [0, 60] dB")
        if not self.profile_id.strip():
            raise ValueError("profile_id must be non-empty")

    @classmethod
    def from_arrays(
        cls, frequencies_hz: Iterable[float], attenuation_db: Iterable[float], profile_id: str
    ) -> "SpectralLossProfile":
        return cls(tuple(float(x) for x in frequencies_hz), tuple(float(x) for x in attenuation_db), profile_id)

    def attenuation_at(self, frequencies_hz: np.ndarray) -> np.ndarray:
        """Interpolate attenuation on a log-frequency axis, holding endpoints."""
        query = np.asarray(frequencies_hz, dtype=float)
        if np.any(query < 0):
            raise ValueError("query frequencies cannot be negative")
        anchors = np.asarray(self.frequencies_hz, dtype=float)
        values = np.asarray(self.attenuation_db, dtype=float)
        safe_query = np.maximum(query, anchors[0])
        return np.interp(np.log2(safe_query), np.log2(anchors), values)


DEFAULT_PROFILES = (
    SpectralLossProfile.from_arrays((125, 250, 500, 1000, 2000, 4000, 8000), (0, 1, 2, 3, 6, 10, 12), "high-frequency-rolloff"),
    SpectralLossProfile.from_arrays((125, 250, 500, 1000, 2000, 4000, 8000), (8, 8, 7, 5, 3, 2, 1), "low-frequency-rolloff"),
    SpectralLossProfile.from_arrays((125, 250, 500, 1000, 2000, 4000, 8000), (2, 4, 6, 8, 10, 12, 14), "broadband-slope"),
)
