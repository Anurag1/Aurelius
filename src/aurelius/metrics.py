"""Signal-fidelity metrics; none of these alone establishes speech intelligibility."""

from __future__ import annotations

import numpy as np


def _pair(reference: np.ndarray, estimate: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ref = np.asarray(reference, dtype=float)
    est = np.asarray(estimate, dtype=float)
    if ref.ndim != 1 or est.ndim != 1 or ref.size != est.size or ref.size == 0:
        raise ValueError("reference and estimate must be non-empty 1-D arrays of equal length")
    if not np.all(np.isfinite(ref)) or not np.all(np.isfinite(est)):
        raise ValueError("signals must be finite")
    return ref, est


def snr_db(reference: np.ndarray, estimate: np.ndarray) -> float:
    ref, est = _pair(reference, estimate)
    noise = ref - est
    ratio = np.sum(ref**2) / max(float(np.sum(noise**2)), 1e-15)
    return float(10.0 * np.log10(max(ratio, 1e-15)))


def si_sdr_db(reference: np.ndarray, estimate: np.ndarray) -> float:
    ref, est = _pair(reference, estimate)
    ref = ref - np.mean(ref)
    est = est - np.mean(est)
    scale = float(np.dot(est, ref)) / max(float(np.dot(ref, ref)), 1e-15)
    target = scale * ref
    residual = est - target
    ratio = np.sum(target**2) / max(float(np.sum(residual**2)), 1e-15)
    return float(10.0 * np.log10(max(ratio, 1e-15)))
