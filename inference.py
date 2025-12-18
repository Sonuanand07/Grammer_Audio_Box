"""
Main inference script for Grammar Scoring Engine
Demonstrates how to use the engine on new audio files
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from audio_processor import AudioProcessor
from text_processor import TextProcessor
from grammar_scorer import GrammarScorer
from utils import print_results_summary, save_results, setup_logging


def score_audio_file(audio_path: str, output_dir: str = './results') -> dict:
    """
    Score a single audio file
    
    Args:
        audio_path: Path to audio file
        output_dir: Directory to save results
        
    Returns:
        Dictionary with scoring results
    """
    logger = setup_logging()
    logger.info(f"Processing: {audio_path}")
    
    # Initialize components
    audio_processor = AudioProcessor()
    text_processor = TextProcessor()
    grammar_scorer = GrammarScorer()
    
    # Step 1: Load and preprocess audio
    logger.info("Step 1: Loading and preprocessing audio...")
    audio, sr = audio_processor.preprocess_audio(audio_path)
    if audio is None:
        logger.error(f"Failed to load audio: {audio_path}")
        return None
    
    # Get audio metrics
    duration = audio_processor.get_duration(audio, sr)
    pause_count = audio_processor.get_pause_count(audio, sr)
    logger.info(f"Audio duration: {duration:.2f}s, Pauses detected: {pause_count}")
    
    # Step 2: Speech to text
    logger.info("Step 2: Converting speech to text...")
    transcript = text_processor.speech_to_text(audio_path)
    if not transcript:
        logger.error("Failed to transcribe audio")
        return None
    logger.info(f"Transcript: {transcript}")
    
    # Step 3: Text preprocessing
    logger.info("Step 3: Preprocessing text...")
    text_data = text_processor.preprocess_text(transcript)
    pos_tags = text_data['pos_tags']
    
    # Step 4: Grammar scoring
    logger.info("Step 4: Scoring grammar...")
    scoring_result = grammar_scorer.score_grammar(
        transcript, 
        duration, 
        pause_count, 
        pos_tags
    )
    
    # Prepare final result
    result = {
        'audio_file': os.path.basename(audio_path),
        'transcript': transcript,
        'audio_duration': round(duration, 2),
        'pauses_detected': pause_count,
        'final_score': scoring_result['final_score'],
        'components': scoring_result['components'],
        'errors': scoring_result['errors'],
        'statistics': scoring_result['statistics'],
    }
    
    # Save results
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 
                               Path(audio_path).stem + '_results.json')
    save_results(result, output_path, format='json')
    
    # Print summary
    print_results_summary(result)
    
    return result


def score_multiple_files(audio_dir: str, output_dir: str = './results') -> list:
    """
    Score all audio files in a directory
    
    Args:
        audio_dir: Directory containing audio files
        output_dir: Directory to save results
        
    Returns:
        List of result dictionaries
    """
    logger = setup_logging()
    logger.info(f"Processing directory: {audio_dir}")
    
    results = []
    audio_files = list(Path(audio_dir).glob('*.wav'))
    audio_files += list(Path(audio_dir).glob('*.mp3'))
    
    logger.info(f"Found {len(audio_files)} audio files")
    
    for i, audio_file in enumerate(audio_files, 1):
        logger.info(f"Processing file {i}/{len(audio_files)}")
        result = score_audio_file(str(audio_file), output_dir)
        if result:
            results.append(result)
    
    return results


if __name__ == "__main__":
    # Example usage
    
    # Single file scoring
    # result = score_audio_file('./data/sample_audio.wav')
    
    # Multiple files scoring
    # results = score_multiple_files('./data')
    
    print("Grammar Scoring Engine - Inference Script")
    print("=" * 60)
    print("\nUsage Examples:")
    print("\n1. Score a single audio file:")
    print("   from inference import score_audio_file")
    print("   result = score_audio_file('path/to/audio.wav')")
    print("\n2. Score all files in a directory:")
    print("   from inference import score_multiple_files")
    print("   results = score_multiple_files('path/to/audio/directory')")
    print("\nFor more details, see README.md")
    print("=" * 60)
