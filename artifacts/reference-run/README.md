# Reference synthetic run

Generated from Aurelius v0.2.0 with:

~~~bash
python -m aurelius.cli benchmark --output artifacts/reference-run --seed 20261124 --trials-per-condition 10
~~~

- 3 synthetic profiles × 3 input-SNR cells × 10 seeded repeats = 90 trials.
- 3 algorithms per trial = 270 rows.
- Runtime environment recorded in summary.json.
- trial_results.csv preserves every algorithm-level output score.

This is a software-validation artifact only. The probe is synthetic and not recorded speech. SNR/SI-SDR results do not establish intelligibility, hearing benefit, comfort, safety, or clinical efficacy. The adaptive algorithm uses an oracle noise-only reference.
