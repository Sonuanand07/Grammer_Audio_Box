# Configuration file for Grammar Scoring Engine
# This file contains all configurable parameters

# Audio processing parameters
AUDIO_CONFIG = {
    'sample_rate': 16000,  # Hz
    'chunk_size': 1024,
    'audio_format': 'wav',
    'normalize': True,
    'remove_silence': True,
    'silence_threshold': -40,  # dB
}

# Speech Recognition parameters
ASR_CONFIG = {
    'engine': 'whisper',  # 'whisper' or 'google'
    'model_size': 'base',  # 'tiny', 'base', 'small', 'medium', 'large'
    'language': 'en',
    'confidence_threshold': 0.5,
}

# NLP parameters
NLP_CONFIG = {
    'tokenizer': 'nltk',  # 'nltk' or 'spacy'
    'pos_tagger': 'nltk',
    'remove_stopwords': False,
    'lowercase': True,
}

# Grammar scoring parameters
SCORING_CONFIG = {
    'model_type': 'rule_based',  # 'rule_based' or 'ml_based'
    'max_score': 100,
    'min_score': 0,
    'weights': {
        'grammar_errors': 0.4,
        'sentence_complexity': 0.3,
        'fluency': 0.2,
        'clarity': 0.1,
    }
}

# File paths
FILE_PATHS = {
    'data_dir': './data',
    'results_dir': './results',
    'models_dir': './models',
    'logs_dir': './logs',
}

# Logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
}
