import numpy as np
from scipy.io import wavfile
from scipy.signal import hilbert

class AudioEngine:

    @staticmethod
    def load_audio(filepath):
        try:
            sr, data = wavfile.read(filepath)

            if data.ndim > 1:
                data = np.mean(data, axis=1)

            data = data.astype(np.float32)

            if np.max(np.abs(data)) > 0:
                data /= np.max(np.abs(data))

            return sr, data

        except Exception:
            return None, None

    @staticmethod
    def preprocess(data, sr):
        data = data - np.mean(data)
        if np.max(np.abs(data)) > 0:
            data = data / np.max(np.abs(data))
        return data

    @staticmethod
    def extract_features(filepath):
        if filepath is None:
            return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}

        sr, data = AudioEngine.load_audio(filepath)
        if data is None:
            return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}

        audio = AudioEngine.preprocess(data, sr)
        envelope = np.abs(hilbert(audio))

        # --- DURATION (same as before) ---
        duration = len(audio) / sr

        # --- ONSET DETECTION (The Tuned Fix) ---
        # Set a low threshold to detect when the blow actually starts
        threshold = 0.02  # 2% of maximum amplitude
        onset_candidates = np.where(envelope > threshold)[0]

        if len(onset_candidates) > 0:
            onset = onset_candidates[0]
            # Move onset back 0.05s to ensure we catch the very start
            onset = max(0, onset - int(0.05 * sr))
        else:
            onset = 0

        # --- EXPLOSIVE START (Measured from ONSET, not from file start) ---
        # Look at the first 0.4 seconds after the onset (gives a tiny reaction buffer)
        window_samples = int(0.4 * sr)
        explosion_window = envelope[onset:onset + window_samples]

        if len(explosion_window) > 0:
            explosion = np.clip(np.max(explosion_window), 0, 1)
        else:
            explosion = 0

        # --- STABILITY (Measured from ONSET, over a full 6-second window) ---
        # Stability is measured from 0.5s after onset to 6.0s after onset
        stab_start = onset + int(0.5 * sr)
        stab_end = onset + int(6.0 * sr)
        stab_end = min(stab_end, len(envelope))

        sustain = envelope[stab_start:stab_end]

        if len(sustain) > 20:
            mean = np.mean(sustain)
            std = np.std(sustain)
            cv = std / (mean + 1e-6)
            stability = np.clip(1 - cv, 0, 1)
        else:
            stability = 0

        # --- DEBUG OUTPUT (so you can see the tuned values) ---
        print("--------------------------------")
        print(f"Onset Time       : {onset / sr:.2f}s")
        print(f"Explosion (tuned): {explosion:.3f}")
        print(f"Duration         : {duration:.2f}s")
        print(f"Stability (tuned): {stability:.3f}")
        print("--------------------------------")

        return {
            "explosion": round(float(explosion), 3),
            "duration": round(float(duration), 2),
            "stability": round(float(stability), 3)
        }