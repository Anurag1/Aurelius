# Related work and novelty assessment

Review date: 24 November 2026. This is a targeted review, not a systematic review, patent search, or freedom-to-operate analysis.

| Work | Main overlap | Aurelius implication |
|---|---|---|
| Apple Hearing Aid Feature (FDA authorization, 12 Sep 2024) | Consumer hearable software offers personalized hearing assistance for eligible adults. | Personalized consumer amplification is already commercialized. |
| openMHA (SoftwareX 2022; release v4.18.1, 6 Jun 2026) | Open-source hearing-aid research platform with calibration, compression, noise reduction, beamforming and reference algorithms. | A substantial external engine exists; Aurelius should integrate with or compare against it, not claim to replace it. |
| Differentiable Auditory Loop (arXiv, 2 Jun 2026) | Differentiable CARFAC auditory models, NAP/SAI objectives and a causal SEANet audio processor. | Auditory-model-in-the-loop personalization is already an active research direction. |
| Verhulst et al. (JARO, 6 Nov 2026) | Review of precision diagnostics, auditory models, machine learning and personalized compensation. | The broad future direction overlaps with ongoing research. |

## Current defensible contribution

Aurelius v0.2.1 provides a small synthetic benchmark with deterministic trials, explicit synthetic profiles, identity/fixed-EQ/oracle-mask reference paths, machine-readable outputs, automated tests, and an optional adapter contract for the official openMHA Breithaupt2008_SCNR reference.

This is a reproducibility/engineering artifact, not a new hearing algorithm. The real openMHA engine was not run in this environment. DAL was reviewed at paper/method level, but source code and weights were not independently run. No external head-to-head performance claim is made.

## What must happen before stronger claims

- Run and independently reproduce the real openMHA reference adapter.
- Build a justified openMHA profile-compensation or multiband-compression baseline; do not treat a generic noise reducer as a matched fitting baseline.
- Reproduce DAL only if the exact source, license, environment, data split, model weights/training configuration and original NAP/SAI protocol can be obtained.
- Add licensed recorded-speech/noise datasets, speaker-disjoint evaluation, appropriate intelligibility/quality metrics, ablations, uncertainty, runtime and failure analysis.
- Obtain independent review from auditory signal-processing and audiology/acoustics specialists.

## References

1. FDA (2024). FDA Authorizes First Over-the-Counter Hearing Aid Software. https://www.fda.gov/news-events/press-announcements/fda-authorizes-first-over-counter-hearing-aid-software
2. Kayser et al. (2022). Open community platform for hearing aid algorithm research: openMHA. SoftwareX, 17, 100953. https://doi.org/10.1016/j.softx.2021.100953
3. Ballesta Rosen et al. (2026). The Differentiable Auditory Loop. arXiv:2606.04103. https://arxiv.org/abs/2606.04103
4. Verhulst et al. (2026). Personalized Hearing Loss Compensation for the Next Generation Hearables and Hearing Aids. JARO. https://doi.org/10.1007/s10162-026-01077-5
