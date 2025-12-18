"""
Audio Processing Module
Handles audio loading, preprocessing, and feature extraction
"""

import numpy as np
import librosa
import librosa.display
import warnings
from typing import Tuple, Optional

try:
    from src.config import AUDIO_CONFIG
except ImportError:
    from config import AUDIO_CONFIG

warnings.filterwarnings('ignore')


class AudioProcessor:
    """Process audio files for grammar scoring engine"""
    
    def __init__(self, sample_rate: int = None):
        """
        Initialize AudioProcessor
        
        Args:
            sample_rate: Target sample rate in Hz
        """
        self.sample_rate = sample_rate or AUDIO_CONFIG['sample_rate']
        self.chunk_size = AUDIO_CONFIG['chunk_size']
        
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load audio file
        
        Args:
            file_path: Path to audio file (.wav, .mp3, etc.)
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            audio, sr = librosa.load(file_path, sr=self.sample_rate)
            return audio, sr
        except Exception as e:
            print(f"Error loading audio file {file_path}: {e}")
            return None, None
    
    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Normalize audio to [-1, 1] range
        
        Args:
            audio: Audio signal
            
        Returns:
            Normalized audio signal
        """
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val
        return audio
    
    def remove_silence(self, audio: np.ndarray, sr: int, 
                       top_db: float = 40) -> np.ndarray:
        """
        Remove silence from audio
        
        Args:
            audio: Audio signal
            sr: Sample rate
            top_db: Threshold in dB
            
        Returns:
            Audio without silence
        """
        try:
            # Trim leading and trailing silence
            audio_trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
            return audio_trimmed
        except Exception as e:
            print(f"Error removing silence: {e}")
            return audio
    
    def preprocess_audio(self, file_path: str) -> Optional[Tuple[np.ndarray, int]]:
        """
        Complete preprocessing pipeline
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (preprocessed_audio, sample_rate)
        """
        # Load audio
        audio, sr = self.load_audio(file_path)
        if audio is None:
            return None
        
        # Normalize
        if AUDIO_CONFIG['normalize']:
            audio = self.normalize_audio(audio)
        
        # Remove silence
        if AUDIO_CONFIG['remove_silence']:
            audio = self.remove_silence(audio, sr, 
                                       top_db=AUDIO_CONFIG['silence_threshold'])
        
        return audio, sr
    
    def extract_mfcc(self, audio: np.ndarray, sr: int, 
                     n_mfcc: int = 13) -> np.ndarray:
        """
        Extract MFCC features
        
        Args:
            audio: Audio signal
            sr: Sample rate
            n_mfcc: Number of MFCC coefficients
            
        Returns:
            MFCC feature matrix
        """
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
        return mfcc
    
    def extract_spectral_features(self, audio: np.ndarray, sr: int) -> dict:
        """
        Extract spectral features
        
        Args:
            audio: Audio signal
            sr: Sample rate
            
        Returns:
            Dictionary with spectral features
        """
        # Spectral centroid
        spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
        
        # Spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)[0]
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio)[0]
        
        return {
            'spectral_centroid_mean': np.mean(spectral_centroid),
            'spectral_centroid_std': np.std(spectral_centroid),
            'spectral_rolloff_mean': np.mean(spectral_rolloff),
            'spectral_rolloff_std': np.std(spectral_rolloff),
            'zcr_mean': np.mean(zcr),
            'zcr_std': np.std(zcr),
        }
    
    def get_duration(self, audio: np.ndarray, sr: int) -> float:
        """
        Get audio duration in seconds
        
        Args:
            audio: Audio signal
            sr: Sample rate
            
        Returns:
            Duration in seconds
        """
        return librosa.get_duration(y=audio, sr=sr)
    
    def get_pause_count(self, audio: np.ndarray, sr: int, 
                       silence_threshold: float = -40) -> int:
        """
        Estimate number of pauses in audio
        
        Args:
            audio: Audio signal
            sr: Sample rate
            silence_threshold: Threshold in dB
            
        Returns:
            Number of pauses detected
        """
        S = librosa.feature.melspectrogram(y=audio, sr=sr)
        S_db = librosa.power_to_db(S, ref=np.max)
        
        # Find frames below threshold
        silence_frames = np.mean(S_db, axis=0) < silence_threshold
        
        # Count transitions from sound to silence
        transitions = np.diff(silence_frames.astype(int))
        pause_count = np.sum(transitions == 1)
        
        return max(0, pause_count)
