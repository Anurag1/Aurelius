# Research protocol: Aurelius v0.2.1

## Objective and scope

Evaluate reference signal-processing code under a known synthetic frequency-dependent channel and seeded additive noise. This protocol validates software behaviour only. It is not a hearing experiment, a model of cochlear physiology, or a speech-intelligibility evaluation.

## Design

- Sample rate: 16 kHz, mono internal pipeline.
- Probe: deterministic, amplitude-modulated harmonic synthetic signal; not recorded speech.
- Profiles: three deterministic spectral attenuation curves, explicitly not audiograms.
- Noise: seeded white Gaussian noise at nominal pre-channel SNRs of 0, 10 and 20 dB.
- Conditions: identity, fixed inverse-profile EQ capped at 12 dB, and a Wiener-style mask using an independent noise-only reference (oracle).
- Repeats: ten per profile/SNR condition in the archived reference run.
- Full internal run: 3 profiles × 3 conditions × 10 repeats = 90 trials and 270 algorithm rows.
- Root seed: 20261124.

## Metrics

SNR and SI-SDR are computed against the known synthetic target in the active probe interval. They are waveform signal-fidelity metrics. They do not measure speech understanding, perceived hearing benefit, safety, comfort, or clinical effectiveness. The nominal SNR is set before the synthetic attenuation channel and can differ from post-channel SNR.

## External comparators

An optional adapter invokes the official openMHA v4.18.1 Breithaupt2008_SCNR noise-reduction reference using static-file MHAIOFile input/output. The adapter receives a synthetic mono mixture duplicated into two channels to satisfy the upstream example. This is a noise-reduction comparison, not a matched profile-fitting comparison. The real engine was unavailable in the development workspace, so no external metric is reported.

DAL is discussed at the published-method level only. Its CARFAC/SEANet setup and auditory-domain evaluation are not numerically comparable with this synthetic waveform benchmark. The source repository was not retrievable at review time, and no DAL reproduction is claimed.

## Reproducibility

The benchmark records root/trial seeds, package versions, conditions, raw CSV rows and grouped JSON. Five internal tests and eight adapter/contract tests are included; the local suite completed with 13 passed and one real-engine integration test skipped.

## Limitations

No recorded speech, speaker variation, room impulse responses, competing talkers, biological auditory model, calibrated acoustic hardware, human subjects, audiograms, subjective listening tests, or real-time deployment are included. The oracle mask receives an ideal noise-only reference. No conclusions about diagnosis, treatment, intelligibility, hearing benefit or safety can be drawn.

## Future external study

Use licensed recorded-speech/noise datasets, speaker-disjoint splits, a matched openMHA configuration, and an independently reproduced DAL implementation if available. Report appropriate speech metrics, ablations, failure cases, runtime, uncertainty and exact environment. Any human-subject study requires appropriate expert oversight and ethics approval.
