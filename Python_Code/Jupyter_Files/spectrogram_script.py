import librosa
import numpy as np
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 4))

y, sr = librosa.load(librosa.util.example_audio_file())
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
                                         fmax=8000)

S_dB = librosa.power_to_db(S, ref=np.max)
librosa.display.specshow(S_dB, x_axis='time',
                             y_axis='mel', sr=sr,
                              fmax=8000)
plt.colorbar(format='%+2.0f dB')
plt.title('Mel-frequency spectrogram')
plt.tight_layout()
plt.show()