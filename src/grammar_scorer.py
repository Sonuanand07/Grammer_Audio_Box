"""
Grammar Scoring Module
Analyzes and scores grammatical correctness
"""

import re
import numpy as np
from typing import Dict, List, Tuple
from nltk import pos_tag, word_tokenize
from nltk.tokenize import sent_tokenize

try:
    from src.config import SCORING_CONFIG
except ImportError:
    from config import SCORING_CONFIG

# Common grammar error patterns
GRAMMAR_RULES = {
    'subject_verb_agreement': {
        'pattern': r'\b(is|are|was|were|be|been|being)\b',
        'description': 'Subject-verb agreement issues'
    },
    'article_usage': {
        'pattern': r'\b(a|an|the)\s+\w+',
        'description': 'Article usage issues'
    },
    'tense_consistency': {
        'pattern': r'\b(is|am|are|was|were|will|would|should|could|have|has|had)\b',
        'description': 'Tense consistency issues'
    },
    'pronoun_agreement': {
        'pattern': r'\b(he|she|it|they|we|you|I)\s+\w+',
        'description': 'Pronoun agreement issues'
    },
}


class GrammarScorer:
    """Analyze and score grammatical correctness of text"""
    
    def __init__(self):
        """Initialize GrammarScorer"""
        self.max_score = SCORING_CONFIG['max_score']
        self.min_score = SCORING_CONFIG['min_score']
        self.weights = SCORING_CONFIG['weights']
    
    def detect_grammar_errors(self, text: str, pos_tags: List[Tuple]) -> Dict:
        """
        Detect potential grammar errors using pattern matching
        
        Args:
            text: Input text
            pos_tags: POS tags for the text
            
        Returns:
            Dictionary with error counts and details
        """
        errors = {
            'total_errors': 0,
            'error_types': {},
            'error_positions': []
        }
        
        # Check each grammar rule
        for rule_name, rule_info in GRAMMAR_RULES.items():
            matches = list(re.finditer(rule_info['pattern'], text, re.IGNORECASE))
            if matches:
                errors['error_types'][rule_name] = len(matches)
                errors['total_errors'] += len(matches)
                
                for match in matches:
                    errors['error_positions'].append({
                        'rule': rule_name,
                        'position': match.start(),
                        'text': match.group()
                    })
        
        return errors
    
    def calculate_sentence_complexity(self, sentences: List[str]) -> float:
        """
        Calculate average sentence complexity based on length and structure
        
        Args:
            sentences: List of sentences
            
        Returns:
            Complexity score (0-1)
        """
        if not sentences:
            return 0.0
        
        complexities = []
        
        for sentence in sentences:
            words = word_tokenize(sentence)
            word_count = len(words)
            
            # Basic complexity: longer sentences are considered more complex
            # Normalize to 0-1 scale (assuming max 30 words per sentence)
            complexity = min(word_count / 30.0, 1.0)
            complexities.append(complexity)
        
        return np.mean(complexities)
    
    def calculate_fluency_score(self, text: str, duration: float, 
                                pause_count: int) -> float:
        """
        Calculate fluency based on speech patterns
        
        Args:
            text: Transcribed text
            duration: Audio duration in seconds
            pause_count: Number of pauses detected
            
        Returns:
            Fluency score (0-1)
        """
        if duration == 0:
            return 0.0
        
        words = len(text.split())
        
        # Words per minute
        wpm = (words / duration) * 60
        
        # Ideal WPM for English is 130-150
        # Score based on deviation from ideal
        ideal_wpm = 140
        wpm_score = 1.0 - (abs(wpm - ideal_wpm) / ideal_wpm)
        wpm_score = max(0, min(wpm_score, 1.0))
        
        # Pause penalty (too many pauses indicate disfluency)
        pause_penalty = min(pause_count / 10.0, 0.5)  # Max 50% penalty
        
        fluency = wpm_score * (1.0 - pause_penalty)
        return max(0, min(fluency, 1.0))
    
    def calculate_clarity_score(self, text: str, pos_tags: List[Tuple]) -> float:
        """
        Calculate clarity based on vocabulary and structure
        
        Args:
            text: Input text
            pos_tags: POS tags
            
        Returns:
            Clarity score (0-1)
        """
        if not text or not pos_tags:
            return 0.0
        
        # Count different POS tags (higher variety = more clear structure)
        pos_types = len(set([tag for word, tag in pos_tags]))
        
        # Normalize (assume max 15 different POS tags)
        pos_diversity = min(pos_types / 15.0, 1.0)
        
        # Check for common clear language patterns
        clear_patterns = len(re.findall(
            r'\b(the|a|is|are|and|but|or|if|when|because)\b', 
            text, 
            re.IGNORECASE
        ))
        
        pattern_score = min(clear_patterns / 20.0, 1.0)
        
        clarity = (pos_diversity * 0.5) + (pattern_score * 0.5)
        return max(0, min(clarity, 1.0))
    
    def calculate_grammar_score_component(self, grammar_errors: Dict, 
                                         total_words: int) -> float:
        """
        Calculate grammar score component (0-1)
        
        Args:
            grammar_errors: Dictionary with error counts
            total_words: Total number of words
            
        Returns:
            Grammar score component (0-1)
        """
        if total_words == 0:
            return 0.0
        
        # Normalize error count by text length
        error_rate = grammar_errors['total_errors'] / total_words
        
        # Convert to score (fewer errors = higher score)
        # Assume 0.1 errors per word = 0 score, 0 errors = 1.0 score
        grammar_score = max(0, 1.0 - (error_rate / 0.1))
        
        return min(grammar_score, 1.0)
    
    def score_grammar(self, text: str, audio_duration: float, 
                      pause_count: int, pos_tags: List[Tuple]) -> Dict:
        """
        Calculate comprehensive grammar score
        
        Args:
            text: Transcribed text
            audio_duration: Duration of audio in seconds
            pause_count: Number of pauses in audio
            pos_tags: POS tags for the text
            
        Returns:
            Dictionary with detailed scoring breakdown
        """
        # Get text components
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        total_words = len(words)
        
        # Calculate component scores (0-1)
        grammar_errors = self.detect_grammar_errors(text, pos_tags)
        
        grammar_component = self.calculate_grammar_score_component(
            grammar_errors, total_words
        )
        
        complexity_component = self.calculate_sentence_complexity(sentences)
        
        fluency_component = self.calculate_fluency_score(
            text, audio_duration, pause_count
        )
        
        clarity_component = self.calculate_clarity_score(text, pos_tags)
        
        # Weighted average
        final_score = (
            grammar_component * self.weights['grammar_errors'] +
            complexity_component * self.weights['sentence_complexity'] +
            fluency_component * self.weights['fluency'] +
            clarity_component * self.weights['clarity']
        )
        
        # Scale to max_score (0-100)
        final_score = final_score * self.max_score
        
        return {
            'final_score': round(final_score, 2),
            'components': {
                'grammar': round(grammar_component * 100, 2),
                'complexity': round(complexity_component * 100, 2),
                'fluency': round(fluency_component * 100, 2),
                'clarity': round(clarity_component * 100, 2),
            },
            'errors': grammar_errors,
            'statistics': {
                'total_words': total_words,
                'total_sentences': len(sentences),
                'avg_sentence_length': total_words / len(sentences) if sentences else 0,
            }
        }
