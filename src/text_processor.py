"""
Text Processing Module
Handles speech-to-text conversion and text preprocessing
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet, stopwords
import re
from typing import List, Dict, Tuple
import numpy as np

try:
    from src.config import NLP_CONFIG, ASR_CONFIG
except ImportError:
    from config import NLP_CONFIG, ASR_CONFIG

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


class TextProcessor:
    """Process text for grammar analysis"""
    
    def __init__(self):
        """Initialize TextProcessor"""
        self.stop_words = set(stopwords.words('english'))
    
    def speech_to_text_whisper(self, audio_path: str) -> str:
        """
        Convert speech to text using OpenAI Whisper
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            import whisper
            model = whisper.load_model(ASR_CONFIG['model_size'])
            result = model.transcribe(audio_path, language=ASR_CONFIG['language'])
            return result['text']
        except Exception as e:
            print(f"Error in Whisper transcription: {e}")
            return ""
    
    def speech_to_text_google(self, audio_path: str) -> str:
        """
        Convert speech to text using Google Speech Recognition
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            from speech_recognition import Recognizer, AudioFile
            recognizer = Recognizer()
            
            with AudioFile(audio_path) as source:
                audio = recognizer.record(source)
            
            text = recognizer.recognize_google(audio)
            return text
        except Exception as e:
            print(f"Error in Google Speech Recognition: {e}")
            return ""
    
    def speech_to_text(self, audio_path: str, engine: str = None) -> str:
        """
        Convert speech to text using specified engine
        
        Args:
            audio_path: Path to audio file
            engine: 'whisper' or 'google'
            
        Returns:
            Transcribed text
        """
        engine = engine or ASR_CONFIG['engine']
        
        if engine == 'whisper':
            return self.speech_to_text_whisper(audio_path)
        elif engine == 'google':
            return self.speech_to_text_google(audio_path)
        else:
            raise ValueError(f"Unknown engine: {engine}")
    
    def clean_text(self, text: str) -> str:
        """
        Basic text cleaning
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:-]', '', text)
        
        return text
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Tokenize text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        sentences = sent_tokenize(text)
        return sentences
    
    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Input text
            
        Returns:
            List of words
        """
        words = word_tokenize(text)
        return words
    
    def get_pos_tags(self, text: str) -> List[Tuple[str, str]]:
        """
        Get Part-of-Speech tags for text
        
        Args:
            text: Input text
            
        Returns:
            List of (word, pos_tag) tuples
        """
        words = self.tokenize_words(text)
        pos_tags = pos_tag(words)
        return pos_tags
    
    def remove_stopwords(self, words: List[str]) -> List[str]:
        """
        Remove stopwords from word list
        
        Args:
            words: List of words
            
        Returns:
            Filtered word list
        """
        return [w for w in words if w.lower() not in self.stop_words]
    
    def preprocess_text(self, text: str) -> Dict:
        """
        Complete text preprocessing pipeline
        
        Args:
            text: Raw text from ASR
            
        Returns:
            Dictionary with processed text components
        """
        # Clean
        text = self.clean_text(text)
        
        # Lowercase if configured
        if NLP_CONFIG['lowercase']:
            text = text.lower()
        
        # Tokenize
        sentences = self.tokenize_sentences(text)
        words = self.tokenize_words(text)
        
        # POS tagging
        pos_tags = self.get_pos_tags(text)
        
        # Remove stopwords if configured
        if NLP_CONFIG['remove_stopwords']:
            words_filtered = self.remove_stopwords(words)
        else:
            words_filtered = words
        
        return {
            'raw_text': text,
            'sentences': sentences,
            'words': words,
            'words_filtered': words_filtered,
            'pos_tags': pos_tags,
            'num_sentences': len(sentences),
            'num_words': len(words),
        }
    
    def calculate_text_stats(self, text_data: Dict) -> Dict:
        """
        Calculate statistics about the text
        
        Args:
            text_data: Preprocessed text data
            
        Returns:
            Dictionary with text statistics
        """
        sentences = text_data['sentences']
        words = text_data['words']
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Average word length
        avg_word_length = np.mean([len(w) for w in words]) if words else 0
        
        # Sentence length std
        sentence_lengths = [len(self.tokenize_words(s)) for s in sentences]
        sentence_length_std = np.std(sentence_lengths) if sentence_lengths else 0
        
        return {
            'avg_sentence_length': avg_sentence_length,
            'avg_word_length': avg_word_length,
            'sentence_length_std': sentence_length_std,
            'total_sentences': len(sentences),
            'total_words': len(words),
        }


import numpy as np
