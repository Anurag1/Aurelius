from __future__ import annotations

import os
import shutil
import textwrap

import numpy as np
import pytest
from scipy.io import wavfile

from aurelius.openmha import render_openmha_scnr_config, run_openmha_scnr


def test_config_tracks_official_reference_chain_and_static_file_io():
    config = render_openmha_scnr_config("in.wav", "out.wav")
    assert "srate = 16000" in config
    assert "mha.mhachain.algos = [noise_psd_estimator smooth_cepstrum]" in config
    assert "mha.mhachain.smooth_cepstrum.noisePow_name = noise_psd_estimator" in config
    assert "iolib = MHAIOFile" in config
    assert "io.in = in.wav" in config
    assert "io.out = out.wav" in config


@pytest.mark.parametrize("name", ["../bad.wav", "/tmp/absolute.wav", "a/b.wav", ""])
def test_config_rejects_nonlocal_file_names(name):
    with pytest.raises(ValueError):
        render_openmha_scnr_config(name, "out.wav")


def test_adapter_fails_closed_when_real_engine_is_unavailable():
    signal = np.zeros(512, dtype=float)
    with pytest.raises(FileNotFoundError):
        run_openmha_scnr(signal, 16_000, mha_executable="/definitely/not/an/mha/binary")


def test_adapter_file_io_and_channel_contract_with_stub_executable(tmp_path):
    """Tests adapter mechanics only; this stub is not the openMHA engine."""
    stub = tmp_path / "mha-stub"
    stub.write_text(
        textwrap.dedent(
            """\
            #!/usr/bin/env python3
            import re
            import sys
            from pathlib import Path
            from scipy.io import wavfile
            cfgarg = next(arg for arg in sys.argv[1:] if arg.startswith('?read:'))
            cfg = Path(cfgarg.split(':', 1)[1]).read_text(encoding='utf-8')
            inp = re.search(r'^io\\.in\\s*=\\s*(.+)$', cfg, re.M).group(1).strip()
            out = re.search(r'^io\\.out\\s*=\\s*(.+)$', cfg, re.M).group(1).strip()
            rate, data = wavfile.read(inp)
            wavfile.write(out, rate, data)
            """
        ),
        encoding="utf-8",
    )
    stub.chmod(0o755)
    signal = 0.1 * np.sin(2 * np.pi * 440 * np.arange(1600) / 16_000)
    output, metadata = run_openmha_scnr(signal, 16_000, mha_executable=str(stub))
    assert output.shape == signal.shape
    assert np.allclose(output, signal, atol=1e-7)
    assert metadata["reference_algorithm"] == "Breithaupt2008_SCNR"
    assert metadata["input_channels"] == 2
    assert metadata["returncode"] == 0


def test_adapter_rejects_unsupported_sample_rate():
    with pytest.raises(ValueError, match="requires 16000 Hz"):
        run_openmha_scnr(np.zeros(512), 44_100, mha_executable="mha")


@pytest.mark.skipif(
    not (os.environ.get("AURELIUS_RUN_OPENMHA_INTEGRATION") == "1" and shutil.which("mha")),
    reason="requires an installed openMHA binary and explicit AURELIUS_RUN_OPENMHA_INTEGRATION=1",
)
def test_real_openmha_reference_chain_smoke():
    signal = 0.1 * np.sin(2 * np.pi * 440 * np.arange(16_000) / 16_000)
    output, metadata = run_openmha_scnr(signal, 16_000)
    assert output.shape == signal.shape
    assert np.all(np.isfinite(output))
    assert metadata["returncode"] == 0
