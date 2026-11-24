"""Deterministic synthetic signal generator for controlled pipeline tests.

The probe is deliberately not recorded speech and must not be interpreted as
an intelligibility or hearing-benefit stimulus.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .dsp import simulate_channel
from .profiles import SpectralLossProfile


@dataclass(frozen=True)
class SyntheticTrial:
    clean_target: np.ndarray
    mixture_after_channel: np.ndarray
    noise_reference_after_channel: np.ndarray
    active_start: int
    sample_rate: int
    profile_id: str
    input_snr_db: float


def _probe_signal(sample_rate: int, duration_s: float, rng: np.random.Generator) -> np.ndarray:
    n = int(sample_rate * duration_s)
    t = np.arange(n, dtype=float) / sample_rate
    envelope = 0.25 + 0.75 * (0.5 + 0.5 * np.sin(2 * np.pi * 2.1 * t))
    phase = 2 * np.pi * (135 * t + 8 * t**2)
    signal = (
        0.55 * np.sin(phase)
        + 0.24 * np.sin(2 * phase + 0.2)
        + 0.13 * np.sin(3 * phase + 0.4)
        + 0.08 * np.sin(5 * phase + 0.7)
    )
    signal *= envelope
    signal += 0.035 * np.sin(2 * np.pi * 730 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.7 * t))
    signal += 0.02 * rng.standard_normal(n)
    peak = max(float(np.max(np.abs(signal))), 1e-12)
    return 0.6 * signal / peak


def make_trial(
    profile: SpectralLossProfile,
    input_snr_db: float,
    seed: int,
    sample_rate: int = 16_000,
    active_duration_s: float = 1.5,
    noise_prelude_s: float = 0.25,
) -> SyntheticTrial:
    """Create a reproducible profile-attenuated noisy probe with a noise reference."""
    if not -5.0 <= input_snr_db <= 30.0:
        raise ValueError("input_snr_db must be in [-5, 30]")
    if sample_rate < 8_000 or active_duration_s <= 0 or noise_prelude_s <= 0:
        raise ValueError("invalid simulation timing or sample rate")
    rng = np.random.default_rng(seed)
    active = _probe_signal(sample_rate, active_duration_s, rng)
    prelude_n = int(sample_rate * noise_prelude_s)
    target = np.concatenate((np.zeros(prelude_n, dtype=float), active))

    noise = rng.standard_normal(target.size)
    signal_rms = np.sqrt(np.mean(active**2))
    noise_rms = signal_rms / (10.0 ** (input_snr_db / 20.0))
    noise *= noise_rms / max(np.sqrt(np.mean(noise**2)), 1e-12)

    channel_input = target + noise
    channel_mixture = simulate_channel(channel_input, sample_rate, profile)
    channel_noise = simulate_channel(noise, sample_rate, profile)
    return SyntheticTrial(
        clean_target=target,
        mixture_after_channel=channel_mixture,
        noise_reference_after_channel=channel_noise,
        active_start=prelude_n,
        sample_rate=sample_rate,
        profile_id=profile.profile_id,
        input_snr_db=float(input_snr_db),
    )
