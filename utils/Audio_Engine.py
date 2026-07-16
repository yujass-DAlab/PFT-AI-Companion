# Audio Engine.py
"""
=========================================================
PFT AI Companion
Audio Engine.py

Author: Jasmine Yu, ChatGPT, DeepSeek

Purpose:
Handles all audio loading, preprocessing, and feature
extraction for the spirometry practice module.

=========================================================
"""

import numpy as np
import scipy.io.wavfile as wav
from utils.helper import page_header, section, disclaimer, footer, encouragement

class AudioEngine:

    @staticmethod
    def load_audio(filepath):
        """
        Loads a WAV file from the given filepath.
        Returns sample_rate and audio_data (numpy array).
        """
        if filepath is None:
            return None, None
        try:
            sample_rate, audio_data = wav.read(filepath)
            return sample_rate, audio_data
        except Exception as e:
            print(f"Audio load error: {e}")
            return None, None

    @staticmethod
    def preprocess(audio_data, sample_rate):
        """
        Preprocesses the raw audio signal.
        - Converts stereo to mono if needed.
        - Normalizes int16 to float between -1 and 1.
        - (Future: noise reduction / silence trimming)
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
        rate, data = AudioEngine.load_audio(filepath)
        if rate is None or data is None:
            return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}

        # 2. Preprocess
        audio = AudioEngine.preprocess(data, rate)
        if audio is None:
            return {"explosion": 0.0, "duration": 0.0, "stability": 0.0}

        # 3. Calculate Metrics
        duration = len(audio) / rate

        # Peak amplitude (Explosiveness)
        peak = np.max(np.abs(audio))
        explosion = np.clip(peak, 0.0, 1.0)  # Already normalized to 0-1

        # Stability: How consistent is the airflow?
        # We calculate the mean absolute amplitude and divide by the peak.
        # If the mean is close to the peak, it's very stable (flat).
        # If the mean is much lower, it's spiky/unstable.
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