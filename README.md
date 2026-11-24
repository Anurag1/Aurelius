# Aurelius

**Reproducible synthetic audio-processing research benchmark.**

> Research-only software. Aurelius is not a hearing test, hearing aid, diagnostic tool, medical device, or treatment. Its profiles and probes are synthetic, not audiograms or validated hearing-loss models. It has no live microphone or headphone path.

## v0.2.1 research update

The original single-file demo has been refactored into a deterministic, offline Python package with synthetic spectral-loss profiles, a seeded probe/noise generator, identity/fixed-EQ/oracle-Wiener baselines, SNR and SI-SDR metrics, CSV/JSON outputs, tests, and continuous integration configuration.

An optional adapter invokes the official openMHA v4.18.1 Breithaupt2008_SCNR reference through its MHAIOFile static-file interface. The adapter contract has local stub-based tests; the real engine was not installed in the development environment, so no openMHA metric or head-to-head result is claimed.

## Install and run

Python 3.10 or newer:

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
python -m aurelius.cli benchmark --output results/synthetic-v0.2.1 --seed 20261124 --trials-per-condition 10
~~~

The archived internal reference experiment contains 3 synthetic profiles × 3 nominal pre-channel SNR conditions × 10 repeats: 90 trials and 270 algorithm-level rows.

## Optional openMHA run

Install the upstream openMHA v4.18.1 distribution and ensure the mha executable and its plugins are available:

~~~bash
MHA_VERSION=v4.18.1 python -m aurelius.cli benchmark --output results/openmha-smoke --seed 20261124 --trials-per-condition 1 --include-openmha
~~~

MHA_VERSION is operator-supplied metadata, not a value automatically queried or verified. Preserve the actual release asset, checksum, platform, and executable provenance. The selected SCNR chain is a noise-reduction comparator, not a matched hearing-aid fitting algorithm.

## Research and publication documents

- docs/EXTERNAL_BASELINES.md: openMHA adapter, configuration, execution status and comparison limitations.
- docs/DAL_REPRODUCIBILITY.md: DAL paper summary and source-access status.
- docs/PUBLICATION_CHECKLIST.md: completed checks and remaining publication gates.
- paper/manuscript-v0.2.1.md: software/methods manuscript draft.

## Results interpretation

SNR and SI-SDR do not measure speech intelligibility, listening effort, perceived benefit, comfort, safety, or clinical efficacy. The oracle processor receives an independent noise-only reference unavailable to an ordinary deployed system. No clinical, human-subject, or real-world hearing-benefit claim is made.

## License and citation

MIT. Third-party software, models, and datasets retain their own licenses and terms. See CITATION.cff and cite the exact tag or commit used.
