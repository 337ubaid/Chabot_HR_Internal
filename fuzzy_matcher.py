# HR Chatbot Fuzzy Matcher
# Menggunakan FuzzyWuzzy dengan multiple matching strategies untuk akurasi tinggi

from fuzzywuzzy import fuzz, process
from typing import Tuple, List, Optional
import re

class HRFuzzyMatcher:
    """
    Matcher berbasis FuzzyWuzzy dengan multiple strategies:
    1. Token Set Ratio - untuk pertanyaan dengan kata berbeda urutan
    2. Token Sort Ratio - untuk pertanyaan dengan kata sama tapi urutan berbeda
    3. Partial Ratio - untuk pertanyaan yang merupakan subset
    4. Simple Ratio - untuk pertanyaan yang mirip persis
    """
    
    def __init__(self, qa_pairs: List[Tuple[str, str, str]], threshold: int = 65):
        """
        Initialize matcher dengan QA pairs.
        
        Args:
            qa_pairs: List of (pertanyaan, jawaban, kategori)
            threshold: Minimum score untuk dianggap match (0-100)
        """
        self.qa_pairs = qa_pairs
        self.threshold = threshold
        self.questions = [self._preprocess(q) for q, _, _ in qa_pairs]
        self.answers = [a for _, a, _ in qa_pairs]
        self.categories = [c for _, _, c in qa_pairs]
        
    def _preprocess(self, text: str) -> str:
        """Preprocess text: lowercase, remove punctuation, normalize whitespace."""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _calculate_scores(self, query: str, target: str) -> dict:
        """Calculate multiple fuzzy scores."""
        return {
            'simple': fuzz.ratio(query, target),
            'partial': fuzz.partial_ratio(query, target),
            'token_sort': fuzz.token_sort_ratio(query, target),
            'token_set': fuzz.token_set_ratio(query, target),
        }
    
    def _weighted_score(self, scores: dict) -> float:
        """
        Calculate weighted average score.
        Weights prioritize token_set dan partial untuk flexibility.
        """
        weights = {
            'simple': 0.15,
            'partial': 0.25,
            'token_sort': 0.25,
            'token_set': 0.35,
        }
        return sum(scores[k] * weights[k] for k in weights)
    
    def find_best_match(self, query: str) -> Tuple[Optional[str], float, Optional[str]]:
        """
        Find the best matching answer for a query.
        
        Returns:
            Tuple of (answer, confidence_score, category) or (None, 0, None) if no match
        """
        processed_query = self._preprocess(query)
        
        best_score = 0
        best_idx = -1
        
        for idx, question in enumerate(self.questions):
            scores = self._calculate_scores(processed_query, question)
            weighted = self._weighted_score(scores)
            
            if weighted > best_score:
                best_score = weighted
                best_idx = idx
        
        if best_score >= self.threshold and best_idx >= 0:
            return self.answers[best_idx], best_score, self.categories[best_idx]
        
        return None, best_score, None
    
    def find_top_matches(self, query: str, top_n: int = 3) -> List[Tuple[str, str, float, str]]:
        """
        Find top N matching answers.
        
        Returns:
            List of (question, answer, score, category)
        """
        processed_query = self._preprocess(query)
        
        results = []
        for idx, question in enumerate(self.questions):
            scores = self._calculate_scores(processed_query, question)
            weighted = self._weighted_score(scores)
            results.append((
                self.qa_pairs[idx][0],  # original question
                self.answers[idx],
                weighted,
                self.categories[idx]
            ))
        
        # Sort by score descending
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:top_n]
    
    def get_fallback_response(self) -> str:
        """Return fallback response when no match found."""
        return (
            "Maaf, saya belum bisa memahami pertanyaan Anda. "
            "Silakan coba tanyakan dengan cara lain atau hubungi HR Hotline di 0812-XXXX-XXXX. "
            "Anda juga bisa bertanya tentang: cuti, gaji, benefit, lembur, atau kebijakan kantor."
        )


class HRChatbotEngine:
    """
    Main chatbot engine yang menggabungkan matcher dengan conversation management.
    """
    
    def __init__(self, qa_pairs: List[Tuple[str, str, str]], threshold: int = 65):
        self.matcher = HRFuzzyMatcher(qa_pairs, threshold)
        self.conversation_history = []
        
    def get_response(self, user_input: str) -> dict:
        """
        Get response untuk user input.
        
        Returns:
            dict with keys: answer, confidence, category, is_fallback, suggestions
        """
        answer, confidence, category = self.matcher.find_best_match(user_input)
        
        if answer:
            response = {
                'answer': answer,
                'confidence': confidence,
                'category': category,
                'is_fallback': False,
                'suggestions': []
            }
        else:
            # Get suggestions from top matches
            top_matches = self.matcher.find_top_matches(user_input, top_n=3)
            suggestions = [
                {'question': q, 'score': s} 
                for q, _, s, _ in top_matches if s >= 40
            ]
            
            response = {
                'answer': self.matcher.get_fallback_response(),
                'confidence': confidence,
                'category': None,
                'is_fallback': True,
                'suggestions': suggestions[:3]
            }
        
        # Track conversation
        self.conversation_history.append({
            'user_input': user_input,
            'response': response
        })
        
        return response
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []


# Quick test
if __name__ == "__main__":
    from hr_knowledge_base import get_flat_qa_pairs
    
    pairs = get_flat_qa_pairs()
    engine = HRChatbotEngine(pairs, threshold=65)
    
    test_queries = [
        "cuti tahunan berapa?",
        "gimana cara ngajuin cuti ya",
        "gaji turun tanggal brp",
        "mau resign gimana prosedurnya",
        "ada shuttle bus ga",
        "halo",
        "xyz123abc",  # Should not match
    ]
    
    print("=" * 60)
    print("HR CHATBOT - FUZZY MATCHER TEST")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\nQ: {query}")
        result = engine.get_response(query)
        print(f"A: {result['answer'][:100]}...")
        print(f"   Confidence: {result['confidence']:.1f}% | Category: {result['category']}")
        print(f"   Fallback: {result['is_fallback']}")
