# Safety, intended use, and scope

Aurelius is an offline software-engineering and signal-processing research sandbox. It is not intended for diagnosis, screening, hearing assessment, hearing-aid fitting, rehabilitation, or treatment.

## Prohibited interpretations

- SpectralLossProfile is a synthetic channel attenuation curve, not an audiogram or hearing-loss estimate.
- The benchmark does not infer a person's hearing thresholds.
- The 12 dB algorithmic gain cap is only a numerical parameter in a simulation. It does not establish a safe sound-pressure level.
- SNR and SI-SDR are not validated measures of human speech understanding or hearing benefit.
- A synthetic benchmark improvement does not imply that a real listener would benefit.

## Current technical boundaries

The package has no microphone capture, playback, Bluetooth routing, personal profile storage, user-facing calibration, or model-based clinical recommendation. These omissions are deliberate.

## Future work boundary

Any move toward human use must begin with qualified audiology/acoustics expertise, calibrated measurement equipment, safety engineering, a defined intended-use statement, ethics review where applicable, and regulatory assessment in each target jurisdiction. This repository alone does not provide those capabilities.
