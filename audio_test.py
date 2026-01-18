import sounddevice as sd
import numpy as np

SAMPLE_RATE = 48000
DURATION = 0.1  # seconds

audio = sd.rec(
    int(SAMPLE_RATE * DURATION),
    samplerate=SAMPLE_RATE,
    channels=2,   # stereo I2S
    dtype='int32'
)
sd.wait()

left = audio[:, 0]
right = audio[:, 1]

print("Left peak:", np.max(np.abs(left)))
print("Right peak:", np.max(np.abs(right)))
