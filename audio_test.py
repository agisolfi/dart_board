import sounddevice as sd
import numpy as np

sd.default.device = 1  # Google VoiceHAT / I2S card
sd.default.samplerate = 48000
sd.default.channels = 1

audio = sd.rec(int(0.5 * 48000), dtype='int32')
sd.wait()

print("Peak:", np.max(np.abs(audio)))
