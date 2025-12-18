# __init__.py - Package initialization
"""
Grammar Scoring Engine
A complete AI-based system for analyzing grammatical quality of spoken English
"""

__version__ = '1.0.0'
__author__ = 'Your Name'
__description__ = 'Grammar Scoring Engine from Voice Samples'

from src.audio_processor import AudioProcessor
from src.text_processor import TextProcessor
from src.grammar_scorer import GrammarScorer
from src.utils import (
    setup_logging,
    save_results,
    load_results,
    create_report,
    print_results_summary
)

__all__ = [
    'AudioProcessor',
    'TextProcessor',
    'GrammarScorer',
    'setup_logging',
    'save_results',
    'load_results',
    'create_report',
    'print_results_summary',
]
