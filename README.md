# Aurelius

**A reproducible research sandbox for profile-aware audio compensation experiments.**

[![Tests](https://github.com/Anurag1/Aurelius/actions/workflows/tests.yml/badge.svg)](https://github.com/Anurag1/Aurelius/actions/workflows/tests.yml)

> **Research-only notice.** Aurelius is not a hearing test, hearing aid, medical device, diagnostic tool, or treatment. It must not be used to assess a person's hearing or to select audio levels for listening. The included profiles and signals are synthetic software fixtures. No human-subject, clinical, or real-world hearing-benefit claim is made.

## What changed in v0.2.0

The original single-file demo combined an uncalibrated tone-threshold interaction, a simple frequency-gain curve, and a live microphone loop. That design could not support defensible hearing or intelligibility claims. The research release retires that workflow and replaces it with an **offline, deterministic, testable benchmark**:

- explicit synthetic spectral-loss profiles (not audiograms);
- an STFT-based reference processing path;
- identity and fixed profile-EQ baselines;
- an adaptive Wiener-style processor using an *oracle* noise-only reference;
- deterministic synthetic trial generation;
- SNR and SI-SDR signal-fidelity metrics;
- CSV/JSON result artifacts, unit tests, and continuous integration;
- a research protocol, related-work review, and manuscript draft.

No live microphone, headphones, Bluetooth, calibration, or Ollama dependency is required.

## Research question

Under a **known synthetic frequency-dependent channel**, how do a fixed profile-compensation baseline and a profile-compensation-plus-noise-mask reference algorithm compare with an identity (unprocessed) baseline on signal-fidelity metrics?

This narrow question is deliberately an engineering benchmark. It is not a model of cochlear physiology, a validated hearing-loss simulator, or a test of speech understanding.

## Architecture

~~~text
Synthetic probe + seeded noise
             |
             v
Synthetic spectral-loss channel
             |
             +-------------------------------+
             |               |               |
             v               v               v
          Identity       Fixed profile    Adaptive profile
          baseline       equalization     + oracle Wiener mask
             |               |               |
             +---------------+---------------+
                             |
                             v
                  SNR / SI-SDR evaluation
                             |
                             v
                  CSV + JSON + environment
~~~

The adaptive method is explicitly labelled **oracle** because the synthetic experiment provides an independent noise-only reference. It is an upper-bound experiment, not a deployable noise estimator. The profile equalizer uses a capped gain for numerical control; that cap is not a guarantee of safe acoustic output.

## Quick start

Python 3.10 or newer is required.

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
~~~

Run the benchmark:

~~~bash
python -m aurelius.cli benchmark \
  --output results/synthetic-v0.2 \
  --seed 20261124 \
  --trials-per-condition 3
~~~

Or after installation:

~~~bash
aurelius benchmark --output results/synthetic-v0.2
~~~

The benchmark writes trial_results.csv (one row per trial and algorithm) and summary.json (condition-level means, standard deviations, trial counts, software versions, seed, and scope warning).

## Algorithms

| Name | Role | Key caveat |
|---|---|---|
| identity | No-processing baseline | Retains channel attenuation and added noise |
| fixed_profile_eq | Capped inverse synthetic attenuation curve | Also boosts noise; not a clinical fitting rule |
| adaptive_oracle_wiener | Profile compensation plus Wiener-style mask | Uses an independent noise-only reference unavailable in ordinary deployment |

Profiles are stored as frequency/attenuation pairs and interpolated on a log-frequency axis. All numerical processing is offline and mono. The current implementation is a reference implementation, not a real-time audio engine.

## Interpreting results

SNR and SI-SDR quantify signal fidelity relative to the known synthetic target. They do **not** measure speech intelligibility, listening effort, perceived benefit, comfort, hearing safety, or clinical efficacy. A better score on this synthetic probe does not imply a person will hear better.

Do not compare Aurelius' synthetic results directly with published clinical studies or with other systems unless the stimuli, sampling, profiles, algorithms, and metric implementations are matched in a documented protocol.

## Related work and positioning

Aurelius is not the first project to personalize hearing-related audio processing:

- **openMHA** is an established open-source master-hearing-aid research platform with calibration, multiband compression, noise reduction, beamforming, feedback cancellation, and other signal-processing components. Aurelius should treat it as an important external baseline/integration target, not claim to replace it.
- **Differentiable Auditory Loop (DAL)** describes an open-source machine-learning framework using differentiable cochlear modelling (CARFAC), neural representations, and a neural audio processor for hyper-personalized hearing-aid research.
- **Verhulst et al. (2026)** review personalized hearing-loss compensation and auditory-model-in-the-loop approaches. This work substantially overlaps with the high-level direction proposed for an advanced Aurelius.
- **Apple's Hearing Aid Feature** received FDA marketing authorization in 2024 for compatible AirPods Pro software intended for adults with perceived mild-to-moderate hearing impairment. It demonstrates that personalized self-fitting and consumer hearables are already a real product category.

The defensible contribution of this release is narrower: a small, inspectable, deterministic baseline harness with explicit simulation assumptions, an oracle/no-oracle distinction, tests, machine-readable outputs, and a publication protocol. **No algorithmic novelty or clinical advantage is claimed.**

See docs/RELATED_WORK.md and docs/RESEARCH_PROTOCOL.md.

## Publication status

paper/manuscript.md is a manuscript draft for a software/methods note. It must not be submitted as completed empirical hearing research. Before submission:

1. Freeze a tagged release and archive it with a DOI.
2. Run the full benchmark in a clean environment and attach output artifacts.
3. Independently reproduce the results.
4. Add a fair openMHA baseline and a literature-aligned DAL comparison where code, licenses, and dependencies permit.
5. Add recorded-speech evaluation using properly licensed datasets and established intelligibility metrics; document domain limitations.
6. Obtain domain-expert review from an audiologist/acoustician and a signal-processing researcher.
7. Revise the manuscript based on the actual evidence and the target venue's requirements.

A public preprint or software-artifact release is possible after these checks. Acceptance by a journal or conference cannot be guaranteed.

## Safety and scope

- No human hearing calibration or self-test is implemented.
- No live microphone or headphone output is implemented.
- No individual hearing profile is stored or inferred.
- No real audiogram is accepted as a fitting prescription.
- Synthetic attenuation parameters are not physiological or clinical models.
- No claim is made for diagnosis, prevention, mitigation, treatment, or cure.
- Any future human-subject or clinical research requires qualified professional oversight, ethics review where applicable, appropriate equipment, and relevant regulatory review.

See docs/SAFETY_AND_SCOPE.md.

## Citation

A citation file is provided in CITATION.cff. Until a version is formally archived and assigned a DOI, cite the GitHub repository and exact commit or release tag.

## License

MIT. Third-party datasets, models, and external software retain their own licenses and terms. See the cited projects before integrating them.
