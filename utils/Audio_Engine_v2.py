"""
=========================================================
PFT AI Companion
Audio_Engine.py (V2 - Clean & Consistent)

Author: Jasmine Yu, ChatGPT, DeepSeek

Purpose:
Handles all audio loading, preprocessing, and feature
extraction for the spirometry practice module.
=========================================================
"""

import numpy as np
import scipy.io.wavfile as wav

class AudioEngine:

    @staticmethod
    def load_audio(filepath):
        """
        Loads a WAV file from the given filepath.
        Returns sampling_rate and audio_data (numpy array).
        """
        if filepath is None:
            return None, None
        try:
            sampling_rate, audio_data = wav.read(filepath)
            return sampling_rate, audio_data
        except Exception as e:
            print(f"Audio load error: {e}")
            return None, None

    @staticmethod
    def preprocess(audio_data, sampling_rate):
        """
        Preprocesses the raw audio signal.
        - Converts stereo to mono if needed.
        - Normalizes int16 to float between -1 and 1.
        """
        if audio_data is None:
            return None

        # Convert stereo to mono (take first channel if 2D)
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]

        # Normalize 16-bit PCM to float range -1.0 to 1.0
        audio_float = audio_data.astype(np.float32) / 32768.0

        return audio_float

    @staticmethod
    def extract_features(filepath):
        """
        Extracts the 3 key metrics from the audio:
        - explosion (peak amplitude, normalized 0-1)
        - duration (seconds)
        - stability (consistency of the blow)
        
        Returns a dictionary matching the expected structure.
        """
        if filepath is None:
            return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}

        # 1. Load
        sampling_rate, data = AudioEngine.load_audio(filepath)
        if sampling_rate is None or data is None:
            return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}

        # 2. Preprocess
        audio = AudioEngine.preprocess(data, sampling_rate)
        # No redundant None check here — load_audio already guarantees valid data.

        # 3. Calculate Metrics
        duration = len(audio) / sampling_rate

        # Peak amplitude (Explosiveness)
        peak = np.max(np.abs(audio))
        explosion = np.clip(peak, 0.0, 1.0)  # Already normalized to 0-1

        # Stability: How consistent is the airflow?
        mean_abs = np.mean(np.abs(audio))
        if peak > 0.01:
            stability = np.clip(mean_abs / peak, 0.0, 1.0)
        else:
            stability = 0.0

        return {
            "explosion": round(explosion, 3),
            "duration": round(duration, 1),
            "stability": round(stability, 3)
        }