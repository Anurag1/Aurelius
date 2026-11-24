# Publication readiness checklist

Software version: 0.2.1
Assessment date: 24 November 2026
Manuscript status: Draft software/methods note; not submitted or peer reviewed.

## Completed
- [x] Replaced the single-file live demo with an offline synthetic benchmark.
- [x] Kept synthetic channel profiles distinct from audiograms.
- [x] Added deterministic trials, three internal algorithms, SNR/SI-SDR metrics and CSV/JSON outputs.
- [x] Added packaging, CLI, automated tests and CI workflow configuration.
- [x] Implemented an optional adapter for the official openMHA v4.18.1 Breithaupt2008_SCNR static-file reference.
- [x] Added stub-based adapter tests and a separately gated real-engine test.
- [x] Reviewed DAL at paper/method level and documented why its values are not directly comparable.
- [x] Added related work, protocol, safety scope, external-baseline docs and manuscript draft.

## Verified locally
- [x] Editable package install succeeded with local build dependencies.
- [x] Python compile check succeeded.
- [x] Test suite: 13 passed, 1 skipped; the skipped test needs the real openMHA engine.
- [x] Internal synthetic benchmark reproduced with seed 20261124: 90 trials and 270 algorithm rows.
- [x] Raw/compressed result artifacts and SHA-256 manifest generated.

## Remaining publication gates
- [ ] Install openMHA v4.18.1 on a supported platform; preserve release asset, checksum and executable provenance.
- [ ] Run real openMHA smoke test and archive config, WAVs, logs, command, hashes and output.
- [ ] Independently repeat the external-engine run on a clean machine.
- [ ] Reassess DAL source availability; if accessible, pin commit, license, environment and checkpoints and reproduce its original NAP/SAI protocol.
- [ ] Add licensed recorded-speech/noise data, speaker-disjoint splits and appropriate intelligibility/quality metrics.
- [ ] Add ablations, failure analysis, uncertainty estimates and runtime/latency measurements.
- [ ] Obtain independent review from auditory signal-processing and audiology/acoustics specialists.
- [ ] Re-run from a clean checkout and independently reproduce all artifacts.
- [ ] Confirm remote GitHub Actions on supported Python versions; an earlier hosted-runner attempt failed before runner steps were allocated.
- [ ] Select the publication venue and follow its ethics, data, authorship, artifact and formatting policies.
- [ ] Archive a stable release, mint a DOI and update citation metadata before final submission.

## Claims not supported

Do not claim that Aurelius outperforms openMHA or DAL, improves real-world speech intelligibility or hearing, is a hearing aid or diagnostic tool, or has clinical efficacy or proven safety.

Defensible current description: “Aurelius is an open-source, reproducible synthetic audio-processing benchmark with an optional adapter for an external openMHA noise-reduction reference.”
