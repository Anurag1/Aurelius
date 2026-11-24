# External baseline protocol and execution status

Review date: 24 November 2026
Pinned upstream target: openMHA v4.18.1
Selected reference: Breithaupt2008_SCNR

## Comparator selection

openMHA is an established open-source master-hearing-aid research platform. Aurelius targets the official single-channel noise-reduction reference because its config and static-file interface are inspectable. This is a noise-reduction comparator, not a full, matched hearing-aid fitting or profile-compensation comparison.

Upstream:
- https://github.com/HoerTech-gGmbH/openMHA/releases/tag/v4.18.1
- https://github.com/HoerTech-gGmbH/openMHA/blob/v4.18.1/reference_algorithms/Breithaupt2008_SCNR/Breithaupt2008_SCNR.cfg
- https://github.com/HoerTech-gGmbH/openMHA/blob/v4.18.1/examples/07-single-channel-noise-reduction/single_channel_noise_reduction.cfg

## Configuration and adapter

The generated config follows the upstream chain: 16 kHz, 2 input channels, 256-sample fragments, overlap-add, 512-point FFT/window, noise_psd_estimator followed by smooth_cepstrum, and MHAIOFile static-file IO.

The adapter accepts mono 16 kHz synthetic audio, duplicates the signal into two identical channels to match the upstream input layout, writes float32 WAV, runs the mha command with a generated config, and validates exit status, output file, sample rate, channel count, sample count, and finite output. It records config/input/output hashes, command, logs and optional archived files.

The adapter does not query the installed openMHA version. MHA_VERSION is operator-supplied metadata only; preserve the actual release asset, package checksum, platform and executable provenance separately.

## Smoke command

~~~bash
MHA_VERSION=v4.18.1 python -m aurelius.cli benchmark --output results/openmha-smoke --seed 20261124 --trials-per-condition 1 --include-openmha
~~~

Start with one repeat. A ten-repeat run invokes the external engine 90 times.

## Execution status

Real openMHA engine: NOT RUN. The development workspace is Debian 13, no mha executable is installed, and outbound DNS/network access was unavailable for obtaining the official distribution. Local adapter tests use a stub executable and establish file/command contract behaviour only; they are not an openMHA engine run. The status is recorded in artifacts/external-baselines/status.json.

No openMHA metrics appear in the paper. A real-engine run and independent reproduction remain publication gates.

## Comparison caveats

The SCNR chain performs noise reduction; it is not the same method as Aurelius fixed profile EQ or an individualized fitting algorithm. Synthetic profiles are not audiograms, and SNR/SI-SDR are waveform fidelity metrics, not clinical or intelligibility measures.
