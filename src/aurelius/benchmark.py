"""Reproducible synthetic benchmark runner and result serialization."""

from __future__ import annotations

import csv
import json
import platform
from collections import defaultdict
from pathlib import Path

import numpy as np
import scipy

from . import __version__
from .dsp import adaptive_noise_aware_compensation, fixed_profile_compensation
from .metrics import si_sdr_db, snr_db
from .openmha import OPENMHA_REFERENCE, OPENMHA_RELEASE, run_openmha_scnr
from .profiles import DEFAULT_PROFILES
from .simulation import make_trial


ALGORITHMS = ("identity", "fixed_profile_eq", "adaptive_oracle_wiener")


def run_benchmark(
    output_dir: str | Path,
    seed: int = 20261124,
    trials_per_condition: int = 3,
    include_openmha: bool = False,
) -> dict:
    if trials_per_condition < 1:
        raise ValueError("trials_per_condition must be at least 1")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    profiles = DEFAULT_PROFILES
    snr_conditions = (0.0, 10.0, 20.0)

    trial_index = 0
    openmha_runs: list[dict] = []
    algorithm_names = list(ALGORITHMS)
    if include_openmha:
        algorithm_names.append("openmha_breithaupt2008_scnr")
    for profile_index, profile in enumerate(profiles):
        for snr_index, input_snr in enumerate(snr_conditions):
            for repeat in range(trials_per_condition):
                trial_seed = seed + trial_index * 9973 + profile_index * 101 + snr_index * 17 + repeat
                trial_index += 1
                trial = make_trial(profile, input_snr, trial_seed)
                active = slice(trial.active_start, None)
                reference = trial.clean_target[active]
                mixture = trial.mixture_after_channel
                estimates = {
                    "identity": mixture,
                    "fixed_profile_eq": fixed_profile_compensation(mixture, trial.sample_rate, profile),
                    "adaptive_oracle_wiener": adaptive_noise_aware_compensation(
                        mixture,
                        trial.noise_reference_after_channel,
                        trial.sample_rate,
                        profile,
                    ),
                }
                if include_openmha:
                    run_id = f"{profile.profile_id}__snr{int(input_snr)}__rep{repeat:02d}"
                    openmha_output, run_metadata = run_openmha_scnr(
                        mixture,
                        trial.sample_rate,
                        archive_dir=out / "openmha_runs" / run_id,
                    )
                    openmha_runs.append(
                        {
                            "profile_id": profile.profile_id,
                            "input_snr_db": input_snr,
                            "repeat": repeat,
                            "seed": trial_seed,
                            "archive_dir": f"openmha_runs/{run_id}",
                            **run_metadata,
                        }
                    )
                    estimates["openmha_breithaupt2008_scnr"] = openmha_output
                for algorithm, estimate in estimates.items():
                    output = estimate[active]
                    rows.append(
                        {
                            "profile_id": profile.profile_id,
                            "input_snr_db": input_snr,
                            "repeat": repeat,
                            "seed": trial_seed,
                            "algorithm": algorithm,
                            "snr_db": snr_db(reference, output),
                            "si_sdr_db": si_sdr_db(reference, output),
                        }
                    )

    csv_path = out / "trial_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    grouped: dict[tuple[str, float, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["profile_id"], row["input_snr_db"], row["algorithm"])].append(row)
    summaries = []
    for (profile_id, input_snr, algorithm), group in sorted(grouped.items()):
        summaries.append(
            {
                "profile_id": profile_id,
                "input_snr_db": input_snr,
                "algorithm": algorithm,
                "n": len(group),
                "snr_db_mean": float(np.mean([r["snr_db"] for r in group])),
                "snr_db_std": float(np.std([r["snr_db"] for r in group], ddof=0)),
                "si_sdr_db_mean": float(np.mean([r["si_sdr_db"] for r in group])),
                "si_sdr_db_std": float(np.std([r["si_sdr_db"] for r in group], ddof=0)),
            }
        )

    summary = {
        "benchmark": "Aurelius Synthetic Auditory-Channel Benchmark",
        "benchmark_version": __version__,
        "seed": seed,
        "trials_per_condition": trials_per_condition,
        "profiles": [p.profile_id for p in profiles],
        "input_snr_conditions_db": list(snr_conditions),
        "algorithms": algorithm_names,
        "n_trials": trial_index,
        "n_rows": len(rows),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "external_baselines": {
            "openmha": {
                "included_in_this_run": include_openmha,
                "release_expected": OPENMHA_RELEASE,
                "reference_algorithm": OPENMHA_REFERENCE,
                "reference_role": "single-channel noise-reduction baseline; not a personalized fitting algorithm",
                "run_count": len(openmha_runs),
                "runs": openmha_runs,
                "caveat": (
                    "This baseline performs noise reduction only. It is not a matched reproduction of "
                    "Aurelius profile compensation or a clinical hearing-aid fitting. All runs must "
                    "record the actual openMHA version and compare outputs on the identical input WAV."
                ),
            }
        },
        "scope_warning": (
            "Synthetic signal-fidelity benchmark only. The probe is not recorded speech; "
            "metrics do not establish intelligibility, hearing benefit, safety, or clinical efficacy. "
            "adaptive_oracle_wiener uses an ideal noise reference and is an upper-bound experiment."
        ),
        "grouped_results": summaries,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
