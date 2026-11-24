# Differentiable Auditory Loop (DAL): reproducibility note

Primary source: Ballesta Rosen et al. (2026), The Differentiable Auditory Loop (DAL): An ML Framework for Hyper-Personalized Hearing Aids, arXiv:2606.04103, submitted 2 June 2026. https://arxiv.org/abs/2606.04103

## Method summary

DAL describes a differentiable CARFAC cochlear model coupled to a causal SEANet waveform processor. Its objective compares neural activity pattern (NAP) and stabilized auditory image (SAI) outputs from impaired and normal-hearing auditory models. Its dataset section reports 10,265 four-second chunks from LibriSpeech train-clean-100, a speaker-ID holdout, white-noise mixtures with target SNR sampled between -5 and +10 dB, and a 1,000-utterance evaluation set.

These results are not numerically comparable with Aurelius synthetic waveform SNR/SI-SDR: the corpus, auditory model, impaired-hearing simulation, algorithms, output domain and metrics differ. DAL also reports its own MHA implementation in JAX; that is not the same as running the openMHA software distribution.

## Source access status

The paper points to:
https://github.com/Australian-Future-Hearing-Initiative/hp-acoustic/tree/main/Frameworks/DAL_framework

On 24 November 2026, this URL returned HTTP 404 through the connected GitHub integration, and the public organization page inspected did not list hp-acoustic. This is an access/retrieval status, not proof of deletion. No DAL source, training run, or checkpoint was independently executed.

## Reproduction requirements

If the source becomes accessible, pin the repository commit, submodules, license and dependencies; obtain exact model weights or retrain from documented seeds; verify data licensing and speaker split; recreate CARFAC impairment parameters and NAP/SAI losses; reproduce the paper's original MHA baselines; and compare only under the identical dataset, split, model and metric protocol.

Until then, DAL belongs in related work and methods discussion only, not in a quantitative Aurelius result table.
