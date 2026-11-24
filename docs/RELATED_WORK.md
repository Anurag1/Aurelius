# Related work and novelty assessment

**Review date:** 24 November 2026. This is a targeted landscape review, not a systematic review or freedom-to-operate analysis.

## Summary

The broad concept of personalized hearing-related audio processing is established. The original Aurelius idea—estimate a frequency-dependent profile, then apply frequency-selective gain—is not novel by itself. Several products and research platforms provide closely related capabilities, and recent research moves substantially beyond static gain curves.

| Work | What it establishes | Implication for Aurelius |
|---|---|---|
| Apple Hearing Aid Feature (FDA authorization, 12 Sep 2024) | Consumer hearable software can use a self-fitting strategy and customize amplification using hearing information; FDA reported a 118-subject study for the authorized feature. | Self-fitting/personalized hearable amplification is already commercialized; do not claim this category as new. |
| openMHA (SoftwareX, 2022; actively maintained) | Open-source, hardware-independent hearing-aid research framework with calibration, multiband compression, noise reduction, beamforming, feedback cancellation, and plugins. | A serious open baseline and potential integration target exists. |
| Differentiable Auditory Loop (arXiv, 2 Jun 2026) | An open framework using differentiable CARFAC cochlear modelling and neural audio processing, evaluated against master-hearing-aid baselines. | Biological auditory-model-in-the-loop personalization is already an active and directly overlapping research direction. |
| Verhulst et al. (JARO, 6 Nov 2026) | Review of personalized hearing-loss compensation, diagnostic markers, computational auditory models, and model-based ML processing. | The current state of the art includes precisely the closed-loop and auditory-model direction previously proposed for Aurelius. |

## What this repository can credibly claim today

The v0.2.0 implementation contributes a **reproducible engineering harness**, not a new hearing algorithm:

1. Explicit and validated synthetic channel profiles, kept separate from clinical audiograms.
2. Controlled comparisons among identity processing, fixed profile equalization, and a Wiener-style oracle-reference experiment.
3. Deterministic seeded trial generation and machine-readable outputs.
4. Tests for parameter validation, reconstruction behaviour, improvement under a known noiseless synthetic channel, and repeatability.
5. An explicit record of the oracle noise-reference assumption and the distinction between signal-fidelity metrics and intelligibility outcomes.

This may be useful as a small teaching/reproducibility artifact. Whether it is publishable as a standalone contribution depends on venue expectations and comparison with existing toolkits; it is not yet a strong scientific novelty claim.

## Gaps before a stronger paper

- Reproduce at least one openMHA baseline using a matched signal path and documented parameters.
- Determine whether the DAL implementation is publicly available and reproducible under its license and dependencies; do not assume the arXiv manuscript alone is sufficient to reproduce it.
- Use real, licensed speech and noise datasets with speaker-disjoint evaluation.
- Include established speech-intelligibility metrics such as STOI only where their assumptions and validity are appropriate; consider subjective listening tests only under an approved expert-led protocol.
- Include ablations, uncertainty intervals, runtime/latency and compute measurements, and failure cases.
- Obtain independent audiology/acoustics review.

## References

1. U.S. Food and Drug Administration. (2024, September 12). *FDA Authorizes First Over-the-Counter Hearing Aid Software*. https://www.fda.gov/news-events/press-announcements/fda-authorizes-first-over-counter-hearing-aid-software
2. Kayser, H., Herzke, T., Maanen, P., Zimmermann, M., Grimm, G., & Hohmann, V. (2022). Open community platform for hearing aid algorithm research: open Master Hearing Aid (openMHA). *SoftwareX, 17*, 100953. https://doi.org/10.1016/j.softx.2021.100953
3. Ballesta Rosen, A., Mikiel-Hunter, J., Maclaren, J., Collins, J., Lyon, R. F., & Carlile, S. (2026). *The Differentiable Auditory Loop (DAL): An ML Framework for Hyper-Personalized Hearing Aids*. arXiv:2606.04103. https://arxiv.org/abs/2606.04103
4. Verhulst, S., Wen, C., Thienpont, M., Nissens, B., Devolder, P., Van Der Biest, H., Inghels, M., Fráter, A., et al. (2026). *Personalized Hearing Loss Compensation for the Next Generation Hearables and Hearing Aids*. Journal of the Association for Research in Otolaryngology. Published 6 November 2026. https://doi.org/10.1007/s10162-026-01077-5
5. American Speech-Language-Hearing Association. *Hearing Aids For Adults*. https://www.asha.org/practice-portal/professional-issues/hearing-aids-for-adults/
