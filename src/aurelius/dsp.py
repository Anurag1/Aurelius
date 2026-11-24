"""Offline STFT-based reference algorithms for synthetic experiments only."""

from __future__ import annotations

import numpy as np
from scipy.signal import istft, stft

from .profiles import SpectralLossProfile


_EPS = 1e-12


def _as_mono(audio: np.ndarray) -> np.ndarray:
    x = np.asarray(audio, dtype=np.float64)
    if x.ndim != 1:
        raise ValueError("audio must be a one-dimensional mono array")
    if x.size < 16 or not np.all(np.isfinite(x)):
        raise ValueError("audio must contain at least 16 finite samples")
    return x


def _transform(audio: np.ndarray, sample_rate: int, nperseg: int, noverlap: int):
    x = _as_mono(audio)
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if nperseg < 32 or not 0 <= noverlap < nperseg:
        raise ValueError("require nperseg >= 32 and 0 <= noverlap < nperseg")
    return stft(
        x,
        fs=sample_rate,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap,
        boundary="zeros",
        padded=True,
    )


def _inverse(frequencies, times, spectrum, sample_rate: int, nperseg: int, noverlap: int, length: int) -> np.ndarray:
    _, reconstructed = istft(
        spectrum,
        fs=sample_rate,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap,
        input_onesided=True,
        boundary=True,
    )
    if reconstructed.size < length:
        reconstructed = np.pad(reconstructed, (0, length - reconstructed.size))
    return np.asarray(reconstructed[:length], dtype=np.float64)


def _apply_frequency_gain(
    audio: np.ndarray,
    sample_rate: int,
    gain_db: np.ndarray,
    nperseg: int = 512,
    noverlap: int = 384,
) -> np.ndarray:
    x = _as_mono(audio)
    f, t, z = _transform(x, sample_rate, nperseg, noverlap)
    gain = np.asarray(gain_db, dtype=float)
    if gain.shape != f.shape or not np.all(np.isfinite(gain)):
        raise ValueError("gain_db must be a finite vector matching the STFT frequency bins")
    z_out = z * (10.0 ** (gain[:, None] / 20.0))
    return _inverse(f, t, z_out, sample_rate, nperseg, noverlap, x.size)


def simulate_channel(audio: np.ndarray, sample_rate: int, profile: SpectralLossProfile) -> np.ndarray:
    """Apply synthetic frequency-dependent attenuation; not a biological ear model."""
    x = _as_mono(audio)
    f, _, _ = _transform(x, sample_rate, 512, 384)
    attenuation = profile.attenuation_at(f)
    return _apply_frequency_gain(x, sample_rate, -attenuation)


def fixed_profile_compensation(
    audio: np.ndarray,
    sample_rate: int,
    profile: SpectralLossProfile,
    max_boost_db: float = 12.0,
) -> np.ndarray:
    """Apply capped inverse profile gain as a simple fixed-EQ baseline."""
    if not 0.0 <= max_boost_db <= 24.0:
        raise ValueError("max_boost_db must be in [0, 24] for this research baseline")
    x = _as_mono(audio)
    f, _, _ = _transform(x, sample_rate, 512, 384)
    gain = np.minimum(profile.attenuation_at(f), max_boost_db)
    return _apply_frequency_gain(x, sample_rate, gain)


def adaptive_noise_aware_compensation(
    audio: np.ndarray,
    noise_reference: np.ndarray,
    sample_rate: int,
    profile: SpectralLossProfile,
    max_boost_db: float = 12.0,
    mask_floor: float = 0.08,
) -> np.ndarray:
    """Apply profile compensation with an oracle noise-reference Wiener mask.

    noise_reference must be an independent noise-only reference of the same
    duration. In the included synthetic benchmark it is available by design;
    this is an oracle upper-bound experiment, not a deployable noise estimator.
    """
    x = _as_mono(audio)
    noise = _as_mono(noise_reference)
    if noise.size != x.size:
        raise ValueError("noise_reference must have the same number of samples as audio")
    if not 0.0 <= max_boost_db <= 24.0:
        raise ValueError("max_boost_db must be in [0, 24]")
    if not 0.0 < mask_floor <= 1.0:
        raise ValueError("mask_floor must be in (0, 1]")

    f, t, z = _transform(x, sample_rate, 512, 384)
    _, _, noise_z = _transform(noise, sample_rate, 512, 384)
    noise_power = np.mean(np.abs(noise_z) ** 2, axis=1, keepdims=True)
    mixture_power = np.mean(np.abs(z) ** 2, axis=1, keepdims=True)
    estimated_signal_power = np.maximum(mixture_power - noise_power, _EPS)
    wiener_mask = estimated_signal_power / (estimated_signal_power + noise_power + _EPS)
    wiener_mask = np.maximum(wiener_mask, mask_floor)

    profile_gain = np.minimum(profile.attenuation_at(f), max_boost_db)
    total_gain = (10.0 ** (profile_gain[:, None] / 20.0)) * wiener_mask
    return _inverse(f, t, z * total_gain, sample_rate, 512, 384, x.size)
