from pathlib import Path

import numpy as np
import pytest

from aurelius.benchmark import run_benchmark
from aurelius.dsp import (
    adaptive_noise_aware_compensation,
    fixed_profile_compensation,
    simulate_channel,
)
from aurelius.metrics import si_sdr_db
from aurelius.profiles import DEFAULT_PROFILES, SpectralLossProfile
from aurelius.simulation import make_trial


def test_profile_validation_and_interpolation():
    with pytest.raises(ValueError):
        SpectralLossProfile((1000.0, 500.0), (2.0, 3.0))
    profile = DEFAULT_PROFILES[0]
    got = profile.attenuation_at(np.array([125.0, 1000.0, 8000.0]))
    assert np.allclose(got, [0.0, 3.0, 12.0])


def test_fixed_profile_compensation_reduces_synthetic_channel_error():
    sr = 16_000
    t = np.arange(sr) / sr
    clean = 0.5 * np.sin(2 * np.pi * 1000 * t) + 0.2 * np.sin(2 * np.pi * 4000 * t)
    profile = DEFAULT_PROFILES[0]
    degraded = simulate_channel(clean, sr, profile)
    restored = fixed_profile_compensation(degraded, sr, profile)
    region = slice(1024, -1024)
    assert si_sdr_db(clean[region], restored[region]) > si_sdr_db(clean[region], degraded[region]) + 5.0


def test_adaptive_processor_is_finite_and_length_preserving():
    trial = make_trial(DEFAULT_PROFILES[0], input_snr_db=5.0, seed=13)
    output = adaptive_noise_aware_compensation(
        trial.mixture_after_channel,
        trial.noise_reference_after_channel,
        trial.sample_rate,
        DEFAULT_PROFILES[0],
    )
    assert output.shape == trial.mixture_after_channel.shape
    assert np.all(np.isfinite(output))


def test_benchmark_is_reproducible_and_writes_artifacts(tmp_path: Path):
    one = run_benchmark(tmp_path / "one", seed=123, trials_per_condition=1)
    two = run_benchmark(tmp_path / "two", seed=123, trials_per_condition=1)
    assert one["n_trials"] == 9
    assert one["n_rows"] == 27
    assert one["grouped_results"] == two["grouped_results"]
    assert (tmp_path / "one" / "trial_results.csv").exists()
    assert (tmp_path / "one" / "summary.json").exists()


def test_input_validation():
    trial = make_trial(DEFAULT_PROFILES[0], input_snr_db=10.0, seed=1)
    with pytest.raises(ValueError):
        fixed_profile_compensation(trial.mixture_after_channel, trial.sample_rate, DEFAULT_PROFILES[0], max_boost_db=30)
