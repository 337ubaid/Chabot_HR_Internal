"""
HR Chatbot Fuzzy Matcher
=========================
Cara kerja:
1. Preprocessing: lowercase, remove punctuation
2. Hitung 4 jenis fuzzy scores
3. Weighted average dari scores
4. Return jawaban jika score >= threshold
"""

from fuzzywuzzy import fuzz
from typing import Tuple, List, Optional
import re

from config import config


class HRFuzzyMatcher:
    """
    Matcher berbasis FuzzyWuzzy dengan multiple strategies.
    
    Menggunakan 4 algoritma:
    1. Token Set Ratio - untuk pertanyaan dengan kata berbeda urutan
    2. Token Sort Ratio - untuk pertanyaan dengan kata sama tapi urutan berbeda
    3. Partial Ratio - untuk pertanyaan yang merupakan subset
    4. Simple Ratio - untuk pertanyaan yang mirip persis
    """
    
    def __init__(self, qa_pairs: List[Tuple[str, str, str]], threshold: int = None):
        """
        Initialize matcher dengan QA pairs.
        
        Args:
            qa_pairs: List of (pertanyaan, jawaban, kategori)
            threshold: Minimum score untuk match (0-100). None = ambil dari config
        """
        self.qa_pairs = qa_pairs
        self.threshold = threshold or config.FUZZY_THRESHOLD
        
        # Preprocess semua pertanyaan untuk efisiensi
        self.questions = [self._preprocess(q) for q, _, _ in qa_pairs]
        self.answers = [a for _, a, _ in qa_pairs]
        self.categories = [c for _, _, c in qa_pairs]
        
    def _preprocess(self, text: str) -> str:
        """
        Preprocess text: lowercase, remove punctuation, normalize whitespace.
        
        Args:
            text: Text mentah
        
        Returns:
            Text yang sudah dibersihkan
        """
        # Validasi input
        if not text or not isinstance(text, str):
            return ""
        
        try:
            # Lowercase
            text = text.lower()
            
            # Remove punctuation (keep alphanumeric dan spaces)
            text = re.sub(r'[^\w\s]', ' ', text)
            
            # Normalize multiple spaces ke single space
            text = re.sub(r'\s+', ' ', text)
            
            return text.strip()
        except Exception as e:
            print(f"⚠️ Error preprocessing text: {e}")
            return ""
    
    def _calculate_scores(self, query: str, target: str) -> dict:
        """
        Hitung multiple fuzzy scores antara query dan target.
        
        Args:
            query: Pertanyaan user (sudah di-preprocess)
            target: Pertanyaan dari knowledge base (sudah di-preprocess)
        
        Returns:
            Dict dengan 4 jenis scores
        """
        return {
            'simple': fuzz.ratio(query, target),
            'partial': fuzz.partial_ratio(query, target),
            'token_sort': fuzz.token_sort_ratio(query, target),
            'token_set': fuzz.token_set_ratio(query, target),
        }
    
    def _weighted_score(self, scores: dict) -> float:
        """
        Hitung weighted average score.
        Weights prioritize token_set dan partial untuk flexibility.
        
        Args:
            scores: Dict dari _calculate_scores
        
        Returns:
            Single weighted score (0-100)
        """
        weights = config.FUZZY_WEIGHTS
        return sum(scores[k] * weights[k] for k in weights)
    
    def find_best_match(self, query: str) -> Tuple[Optional[str], float, Optional[str]]:
        """
        Cari jawaban terbaik untuk query user.
        
        Args:
            query: Pertanyaan user
        
        Returns:
            Tuple of (answer, confidence_score, category)
            Jika tidak ada match: (None, best_score, None)
        """
        # Validasi input
        if not query or not isinstance(query, str):
            return None, 0, None
        
        processed_query = self._preprocess(query)
        
        # Jika query kosong setelah preprocessing
        if not processed_query:
            return None, 0, None
        
        best_score = 0
        best_idx = -1
        
        # Loop semua pertanyaan di knowledge base
        for idx, question in enumerate(self.questions):
            scores = self._calculate_scores(processed_query, question)
            weighted = self._weighted_score(scores)
            
            if weighted > best_score:
                best_score = weighted
                best_idx = idx
        
        # Return jawaban jika score cukup tinggi
        if best_score >= self.threshold and best_idx >= 0:
            return self.answers[best_idx], best_score, self.categories[best_idx]
        
        return None, best_score, None
    
    def find_top_matches(self, query: str, top_n: int = None) -> List[Tuple[str, str, float, str]]:
        """
        Cari top N matching answers untuk suggestion.
        
        Args:
            query: Pertanyaan user
            top_n: Berapa banyak top matches (None = ambil dari config)
        
        Returns:
            List of (original_question, answer, score, category)
            Sorted by score descending
        """
        top_n = top_n or config.MAX_SUGGESTIONS
        
        # Validasi input
        if not query or not isinstance(query, str):
            return []
        
        processed_query = self._preprocess(query)
        
        if not processed_query:
            return []
        
        results = []
        
        # Hitung score untuk semua pertanyaan
        for idx, question in enumerate(self.questions):
            scores = self._calculate_scores(processed_query, question)
            weighted = self._weighted_score(scores)
            results.append((
                self.qa_pairs[idx][0],  # original question
                self.answers[idx],
                weighted,
                self.categories[idx]
            ))
        
        # Sort by score descending dan ambil top N
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:top_n]
    
    def get_fallback_response(self) -> str:
        """
        Return fallback response saat tidak ada match.
        
        Returns:
            String pesan fallback
        """
        return (
            f"Maaf, saya belum bisa memahami pertanyaan Anda. 🤔\n\n"
            f"Silakan coba tanyakan dengan cara lain atau hubungi HR Hotline di **{config.HR_HOTLINE}**.\n\n"
            f"Anda juga bisa bertanya tentang: cuti, gaji, benefit, lembur, atau kebijakan kantor."
        )


class HRChatbotEngine:
    """
    Main chatbot engine yang menggabungkan matcher dengan conversation management.
    Ini adalah interface utama yang digunakan oleh aplikasi.
    """
    
    def __init__(self, qa_pairs: List[Tuple[str, str, str]], threshold: int = None):
        """
        Initialize chatbot engine.
        
        Args:
            qa_pairs: List of (pertanyaan, jawaban, kategori)
            threshold: Minimum confidence score (None = dari config)
        """
        self.matcher = HRFuzzyMatcher(qa_pairs, threshold)
        
    def get_response(self, user_input: str) -> dict:
        """
        Dapatkan response untuk user input.
        Ini adalah method utama yang dipanggil app.
        
        Args:
            user_input: Pertanyaan dari user
        
        Returns:
            Dict dengan keys:
            - answer: Jawaban chatbot
            - confidence: Score 0-100
            - category: Kategori pertanyaan
            - is_fallback: Boolean, True jika tidak ada match
            - suggestions: List suggestion jika fallback
        """
        answer, confidence, category = self.matcher.find_best_match(user_input)
        
        if answer:
            # Ada match yang bagus
            response = {
                'answer': answer,
                'confidence': confidence,
                'category': category,
                'is_fallback': False,
                'suggestions': []
            }
        else:
            # Tidak ada match, berikan fallback + suggestions
            top_matches = self.matcher.find_top_matches(user_input)
            
            # Filter suggestions dengan minimum score
            suggestions = [
                {'question': q, 'score': s} 
                for q, _, s, _ in top_matches 
                if s >= config.SUGGESTION_MIN_SCORE
            ]
            
            response = {
                'answer': self.matcher.get_fallback_response(),
                'confidence': confidence,
                'category': None,
                'is_fallback': True,
                'suggestions': suggestions[:config.MAX_SUGGESTIONS]
            }
        
        return response


# Quick test jika file dijalankan langsung
if __name__ == "__main__":
    from hr_knowledge_base import get_flat_qa_pairs
    
    # Setup engine
    pairs = get_flat_qa_pairs()
    engine = HRChatbotEngine(pairs)
    
    # Test queries

    print("=" * 60)
    print("HR CHATBOT - FUZZY MATCHER TEST")
    print("=" * 60)
    
    for query in config.QUICK_QUESTIONS:
        print(f"\n📌 Q: {query}")
        result = engine.get_response(query)
        print(f"   A: {result['answer'][:100]}...")
        print(f"   Confidence: {result['confidence']:.1f}% | Category: {result['category']}")
        print(f"   Fallback: {result['is_fallback']}")
        
        if result['suggestions']:
            print(f"   Suggestions: {len(result['suggestions'])} items")