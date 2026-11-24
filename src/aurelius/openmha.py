"""Optional adapter for the official openMHA single-channel noise-reduction reference.

The adapter writes a mono signal as a duplicated, two-channel float WAV and runs
openMHA's documented Breithaupt-2008 single-channel noise-reduction chain through
MHAIOFile. It does not emulate openMHA. A real `mha` executable is required.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from shutil import copy2
from typing import Any

import numpy as np
from scipy.io import wavfile


OPENMHA_REFERENCE = "Breithaupt2008_SCNR"
OPENMHA_RELEASE = "v4.18.1"
OPENMHA_REFERENCE_CONFIG = "reference_algorithms/Breithaupt2008_SCNR/Breithaupt2008_SCNR.cfg"
REQUIRED_SAMPLE_RATE = 16_000


def render_openmha_scnr_config(
    input_name: str = "input_stereo.wav",
    output_name: str = "output_stereo.wav",
) -> str:
    """Render the file-I/O form of openMHA's official Breithaupt-2008 example.

    The algorithm configuration mirrors the official v4.18.1 reference example;
    only the input/output file names are supplied by Aurelius.
    """
    for name in (input_name, output_name):
        p = Path(name)
        if p.is_absolute() or len(p.parts) != 1 or p.name in {"", ".", ".."}:
            raise ValueError("openMHA input/output names must be simple relative file names")
    return "\n".join(
        [
            "# Aurelius generated adapter configuration.",
            "# Settings adapted from openMHA v4.18.1 Breithaupt2008_SCNR.cfg.",
            "# Upstream: https://github.com/HoerTech-gGmbH/openMHA/blob/v4.18.1/reference_algorithms/Breithaupt2008_SCNR/Breithaupt2008_SCNR.cfg",
            "# Original reference configuration copyright 2020 HoerTech gGmbH; see upstream repository for license terms.",
            "# Input/output are static files; no live audio devices are opened.",
            f"srate = {REQUIRED_SAMPLE_RATE}",
            "fragsize = 256",
            "nchannels_in = 2",
            "mhalib = overlapadd",
            "mha.fftlen = 512",
            "mha.wnd.len = 512",
            "mha.wnd.exp = 0.5",
            "mha.plugin_name = mhachain",
            "mha.mhachain.algos = [noise_psd_estimator smooth_cepstrum]",
            "mha.mhachain.smooth_cepstrum.noisePow_name = noise_psd_estimator",
            "iolib = MHAIOFile",
            f"io.in = {input_name}",
            f"io.out = {output_name}",
            "",
        ]
    )


def run_openmha_scnr(
    audio: np.ndarray,
    sample_rate: int,
    *,
    mha_executable: str = "mha",
    timeout_seconds: int = 120,
    archive_dir: str | Path | None = None,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Run real openMHA SCNR on mono audio and return its first output channel.

    A duplicated stereo input is used because the official reference configuration
    declares two input channels. Both channels contain exactly the same waveform.
    The returned signal must preserve length and sample rate; otherwise the run is
    rejected rather than silently trimmed or time-shifted.
    """
    x = np.asarray(audio, dtype=np.float64)
    if x.ndim != 1 or x.size < 16 or not np.all(np.isfinite(x)):
        raise ValueError("audio must be a finite, one-dimensional signal with at least 16 samples")
    if sample_rate != REQUIRED_SAMPLE_RATE:
        raise ValueError(f"the pinned openMHA SCNR config requires {REQUIRED_SAMPLE_RATE} Hz")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")

    executable = shutil.which(mha_executable)
    if executable is None and Path(mha_executable).is_file():
        executable = str(Path(mha_executable).resolve())
    if executable is None:
        raise FileNotFoundError(
            "openMHA executable 'mha' was not found. Install openMHA v4.18.1 and ensure its bin directory is on PATH."
        )

    with tempfile.TemporaryDirectory(prefix="aurelius-openmha-") as temp:
        workdir = Path(temp)
        input_path = workdir / "input_stereo.wav"
        output_path = workdir / "output_stereo.wav"
        config_path = workdir / "aurelius_scnr.cfg"

        stereo = np.column_stack((x, x)).astype(np.float32)
        wavfile.write(input_path, sample_rate, stereo)
        config_text = render_openmha_scnr_config(input_path.name, output_path.name)
        config_path.write_text(config_text, encoding="utf-8")
        command = [executable, f"?read:{config_path.name}", "cmd=start", "cmd=quit"]
        try:
            completed = subprocess.run(
                command,
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
                env=os.environ.copy(),
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"openMHA SCNR timed out after {timeout_seconds} seconds") from exc

        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or "(openMHA returned no diagnostic text)")[-6000:]
            raise RuntimeError(
                f"openMHA SCNR failed with exit code {completed.returncode}.\n{detail}"
            )
        if not output_path.is_file():
            detail = (completed.stderr or completed.stdout or "")[-3000:]
            raise RuntimeError(f"openMHA exited successfully but produced no output WAV.\n{detail}")

        output_rate, output = wavfile.read(output_path)
        output = np.asarray(output)
        if output_rate != sample_rate:
            raise RuntimeError(f"openMHA changed the sample rate: {output_rate} != {sample_rate}")
        if output.ndim != 2 or output.shape[1] != 2:
            raise RuntimeError(f"expected two output channels, received shape {output.shape}")
        if output.shape[0] != x.size:
            raise RuntimeError(f"openMHA changed signal length: {output.shape[0]} != {x.size}")
        result = output[:, 0].astype(np.float64)
        if not np.all(np.isfinite(result)):
            raise RuntimeError("openMHA output contains NaN or infinite values")

        def sha256_file(path: Path) -> str:
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            return digest.hexdigest()

        metadata = {
            "engine": "openMHA",
            "engine_release_expected": OPENMHA_RELEASE,
            "engine_version_operator_asserted": os.environ.get("MHA_VERSION", "not-recorded"),
            "reference_algorithm": OPENMHA_REFERENCE,
            "reference_config": OPENMHA_REFERENCE_CONFIG,
            "executable": executable,
            "sample_rate_hz": sample_rate,
            "input_channels": 2,
            "output_channels_evaluated": 1,
            "input_dtype": "float32 WAV",
            "output_dtype": str(output.dtype),
            "n_samples": int(x.size),
            "command": command,
            "returncode": completed.returncode,
            "config_sha256": hashlib.sha256(config_text.encode("utf-8")).hexdigest(),
            "input_wav_sha256": sha256_file(input_path),
            "output_wav_sha256": sha256_file(output_path),
            "stdout": completed.stdout[-4000:],
            "stderr": completed.stderr[-4000:],
        }
        if archive_dir is not None:
            archive = Path(archive_dir)
            archive.mkdir(parents=True, exist_ok=True)
            copy2(input_path, archive / "input_stereo.wav")
            copy2(output_path, archive / "output_stereo.wav")
            copy2(config_path, archive / "aurelius_scnr.cfg")
            (archive / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
            (archive / "stdout.txt").write_text(completed.stdout, encoding="utf-8")
            (archive / "stderr.txt").write_text(completed.stderr, encoding="utf-8")
        return result, metadata
