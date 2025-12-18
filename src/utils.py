"""
Utility functions for Grammar Scoring Engine
"""

import os
import json
import logging
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime
import numpy as np
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level
        log_file: Optional log file path
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, log_level))
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def ensure_directory(directory: str) -> None:
    """
    Ensure directory exists, create if not
    
    Args:
        directory: Directory path
    """
    os.makedirs(directory, exist_ok=True)


def save_results(results: Dict[str, Any], output_path: str, format: str = 'json') -> None:
    """
    Save results to file
    
    Args:
        results: Results dictionary
        output_path: Output file path
        format: 'json' or 'csv'
    """
    ensure_directory(os.path.dirname(output_path))
    
    if format == 'json':
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
    
    elif format == 'csv':
        # Flatten results for CSV
        if isinstance(results, list):
            df = pd.DataFrame(results)
        else:
            df = pd.DataFrame([results])
        
        df.to_csv(output_path, index=False)
    
    print(f"Results saved to {output_path}")


def load_results(input_path: str) -> Dict[str, Any]:
    """
    Load results from file
    
    Args:
        input_path: Input file path
        
    Returns:
        Results dictionary
    """
    if input_path.endswith('.json'):
        with open(input_path, 'r') as f:
            return json.load(f)
    
    elif input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
        return df.to_dict('records')
    
    else:
        raise ValueError("Unsupported file format")


def create_report(results: List[Dict], output_path: str = None) -> pd.DataFrame:
    """
    Create a report from multiple results
    
    Args:
        results: List of result dictionaries
        output_path: Optional output file path
        
    Returns:
        Pandas DataFrame with results
    """
    report_data = []
    
    for result in results:
        row = {
            'audio_file': result.get('audio_file', ''),
            'grammar_score': result.get('final_score', 0),
            'grammar_component': result.get('components', {}).get('grammar', 0),
            'fluency_component': result.get('components', {}).get('fluency', 0),
            'clarity_component': result.get('components', {}).get('clarity', 0),
            'complexity_component': result.get('components', {}).get('complexity', 0),
            'total_errors': result.get('errors', {}).get('total_errors', 0),
            'total_words': result.get('statistics', {}).get('total_words', 0),
        }
        report_data.append(row)
    
    df = pd.DataFrame(report_data)
    
    if output_path:
        ensure_directory(os.path.dirname(output_path))
        df.to_csv(output_path, index=False)
        print(f"Report saved to {output_path}")
    
    return df


def get_timestamp() -> str:
    """
    Get current timestamp
    
    Returns:
        Timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class ResultsProcessor:
    """Process and analyze results"""
    
    @staticmethod
    def aggregate_scores(results: List[Dict]) -> Dict[str, Any]:
        """
        Aggregate scores across multiple results
        
        Args:
            results: List of result dictionaries
            
        Returns:
            Aggregated statistics
        """
        scores = [r.get('final_score', 0) for r in results]
        
        return {
            'mean_score': np.mean(scores),
            'std_score': np.std(scores),
            'min_score': np.min(scores),
            'max_score': np.max(scores),
            'median_score': np.median(scores),
            'total_samples': len(scores),
        }
    
    @staticmethod
    def score_distribution(results: List[Dict], bins: int = 5) -> Dict:
        """
        Get distribution of scores
        
        Args:
            results: List of result dictionaries
            bins: Number of bins for histogram
            
        Returns:
            Distribution dictionary
        """
        scores = [r.get('final_score', 0) for r in results]
        hist, bin_edges = np.histogram(scores, bins=bins)
        
        return {
            'histogram': hist.tolist(),
            'bin_edges': bin_edges.tolist(),
            'distribution': dict(zip(range(len(hist)), hist.tolist()))
        }
    
    @staticmethod
    def export_detailed_report(results: List[Dict], output_path: str) -> None:
        """
        Export detailed results with all components
        
        Args:
            results: List of result dictionaries
            output_path: Output file path
        """
        ensure_directory(os.path.dirname(output_path))
        
        detailed_data = []
        for result in results:
            detailed_data.append({
                'audio_file': result.get('audio_file', ''),
                'final_score': result.get('final_score', 0),
                'grammar_score': result.get('components', {}).get('grammar', 0),
                'fluency_score': result.get('components', {}).get('fluency', 0),
                'clarity_score': result.get('components', {}).get('clarity', 0),
                'complexity_score': result.get('components', {}).get('complexity', 0),
                'total_errors': result.get('errors', {}).get('total_errors', 0),
                'total_words': result.get('statistics', {}).get('total_words', 0),
                'total_sentences': result.get('statistics', {}).get('total_sentences', 0),
                'transcript': result.get('transcript', ''),
            })
        
        df = pd.DataFrame(detailed_data)
        df.to_csv(output_path, index=False)
        print(f"Detailed report saved to {output_path}")


def print_results_summary(result: Dict) -> None:
    """
    Print formatted results summary
    
    Args:
        result: Result dictionary
    """
    print("\n" + "="*60)
    print("GRAMMAR SCORING RESULTS")
    print("="*60)
    print(f"Audio File: {result.get('audio_file', 'N/A')}")
    print(f"Transcript: {result.get('transcript', 'N/A')}")
    print(f"\nFinal Grammar Score: {result.get('final_score', 0)}/100")
    print("\nComponent Scores:")
    components = result.get('components', {})
    for component, score in components.items():
        print(f"  - {component.capitalize()}: {score}/100")
    
    print(f"\nError Analysis:")
    errors = result.get('errors', {})
    print(f"  - Total Errors Found: {errors.get('total_errors', 0)}")
    
    print(f"\nText Statistics:")
    stats = result.get('statistics', {})
    print(f"  - Total Words: {stats.get('total_words', 0)}")
    print(f"  - Total Sentences: {stats.get('total_sentences', 0)}")
    print(f"  - Avg Sentence Length: {stats.get('avg_sentence_length', 0):.2f}")
    print("="*60 + "\n")
