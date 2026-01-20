"""
HR Chatbot Analytics
============================
1. Logging queries dari user
2. Logging feedback (rating & komentar)
3. Tracking sessions
4. Menyediakan fungsi analytics untuk dashboard
"""

import json
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import List, Dict, Optional, Any
import threading
import time

from config import config


class HRAnalytics:
    """
    Analytics engine untuk HR Chatbot.
    Menyimpan dan menganalisis data percakapan untuk improvement.
    """
    
    def __init__(self, data_file: str = None):
        """
        Inisialisasi analytics engine.
        
        Args:
            data_file: Path file JSON untuk menyimpan data. 
                      Jika None, akan pakai default dari config.
        """
        self.data_file = data_file or config.ANALYTICS_FILE
        self.lock = threading.Lock()
        
        # Load data yang sudah ada
        self._load_data()
        
        # Counter untuk batch saving
        self.unsaved_changes = 0
        self.last_save_time = time.time()
    
    def _load_data(self):
        """
        Load data dari file JSON.
        Jika file tidak ada atau corrupt, mulai dengan data kosong.
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Load data dengan default empty jika tidak ada
                    self.queries = data.get('queries', [])
                    self.feedback = data.get('feedback', [])
                    self.sessions = data.get('sessions', {})
                    
                    # Validasi tipe data
                    if not isinstance(self.queries, list):
                        self.queries = []
                    if not isinstance(self.feedback, list):
                        self.feedback = []
                    if not isinstance(self.sessions, dict):
                        self.sessions = {}
                        
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ Error loading data: {e}. Starting with fresh data.")
                self._init_empty_data()
        else:
            self._init_empty_data()
    
    def _init_empty_data(self):
        """Initialize struktur data kosong."""
        self.queries = []
        self.feedback = []
        self.sessions = {}
    
    def _save_data(self, force: bool = False):
        """
        Save data ke file dengan batch optimization.
        Tidak akan save setiap kali, tapi:
        - Setiap N queries (batch size)
        - Setiap N detik
        - Atau jika dipaksa (force=True)
        
        Args:
            force: Paksa save sekarang, abaikan threshold
        """
        current_time = time.time()
        time_elapsed = current_time - self.last_save_time
        
        # Cek apakah perlu save
        should_save = (
            force or 
            self.unsaved_changes >= config.SAVE_BATCH_SIZE or
            time_elapsed >= config.SAVE_INTERVAL_SECONDS
        )
        
        if not should_save:
            return
        
        with self.lock:
            try:
                # Save ke temporary file dulu (atomic write)
                temp_file = f"{self.data_file}.tmp"
                
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'queries': self.queries[-config.MAX_QUERIES_RETAINED:],
                        'feedback': self.feedback[-config.MAX_FEEDBACK_RETAINED:],
                        'sessions': dict(list(self.sessions.items())[-config.MAX_SESSIONS_RETAINED:])
                    }, f, ensure_ascii=False, indent=2)
                
                # Replace file asli dengan temp file (atomic)
                os.replace(temp_file, self.data_file)
                
                # Reset counter
                self.unsaved_changes = 0
                self.last_save_time = current_time
                
            except IOError as e:
                print(f"❌ Error saving analytics data: {e}")
                # Hapus temp file jika ada
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
    
    def log_query(self, session_id: str, user_input: str, response: dict):
        """
        Log pertanyaan user untuk analytics.
        
        Args:
            session_id: ID unik session
            user_input: Pertanyaan user
            response: Dictionary response dari chatbot
        """
        # Validasi input
        if not session_id or not user_input:
            return
        
        # Sanitize input (potong jika terlalu panjang)
        user_input = user_input.strip()[:config.MAX_USER_INPUT_LENGTH]
        
        # Buat record query
        query_record = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'user_input': user_input,
            'category': response.get('category'),
            'confidence': round(response.get('confidence', 0), 2),
            'is_fallback': response.get('is_fallback', False),
        }
        
        self.queries.append(query_record)
        
        # Update atau create session
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'start_time': datetime.now().isoformat(),
                'query_count': 0,
                'last_activity': datetime.now().isoformat(),
                'rated': False,
            }
        
        self.sessions[session_id]['query_count'] += 1
        self.sessions[session_id]['last_activity'] = datetime.now().isoformat()
        
        # Increment unsaved counter dan coba save
        self.unsaved_changes += 1
        self._save_data()
    
    def log_feedback(self, session_id: str, rating: int, comment: Optional[str] = None):
        """
        Log feedback dari user.
        
        Args:
            session_id: ID session
            rating: Rating 1-5
            comment: Komentar opsional
        """
        # Validasi rating
        if not config.MIN_RATING <= rating <= config.MAX_RATING:
            print(f"⚠️ Invalid rating: {rating}. Must be {config.MIN_RATING}-{config.MAX_RATING}.")
            return
        
        # Sanitize comment
        if comment:
            comment = comment.strip()[:config.MAX_COMMENT_LENGTH]
            if not comment:
                comment = None
        
        # Buat record feedback
        feedback_record = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'rating': rating,
            'comment': comment,
        }
        
        self.feedback.append(feedback_record)
        
        # Update session
        if session_id in self.sessions:
            self.sessions[session_id]['rated'] = True
            self.sessions[session_id]['rating'] = rating
        
        # Force save untuk feedback (data penting)
        self.unsaved_changes += 1
        self._save_data(force=True)
    
    def get_top_queries(self, n: int = 10, days: int = None) -> List[Dict]:
        """
        Dapatkan top N pertanyaan paling sering.
        
        Args:
            n: Berapa banyak top queries yang diambil
            days: Periode dalam hari (None = default dari config)
        
        Returns:
            List of dict dengan format: [{'query': str, 'count': int}, ...]
        """
        days = days or config.DEFAULT_ANALYTICS_DAYS
        
        try:
            cutoff = datetime.now() - timedelta(days=days)
            
            # Filter queries dalam periode
            recent_queries = [
                q['user_input'].lower() 
                for q in self.queries 
                if datetime.fromisoformat(q['timestamp']) > cutoff
            ]
            
            # Count dan ambil top N
            counter = Counter(recent_queries)
            return [
                {'query': query, 'count': count}
                for query, count in counter.most_common(n)
            ]
        except Exception as e:
            print(f"❌ Error in get_top_queries: {e}")
            return []
    
    def get_category_distribution(self, days: int = None) -> Dict[str, int]:
        """
        Dapatkan distribusi pertanyaan per kategori.
        
        Args:
            days: Periode dalam hari
        
        Returns:
            Dict dengan format: {'kategori': count, ...}
        """
        days = days or config.DEFAULT_ANALYTICS_DAYS
        
        try:
            cutoff = datetime.now() - timedelta(days=days)
            
            categories = [
                q['category'] or 'unknown'
                for q in self.queries
                if datetime.fromisoformat(q['timestamp']) > cutoff
            ]
            
            return dict(Counter(categories))
        except Exception as e:
            print(f"❌ Error in get_category_distribution: {e}")
            return {}
    
    def get_daily_trends(self, days: int = None) -> List[Dict]:
        """
        Dapatkan tren harian jumlah queries.
        
        Args:
            days: Berapa hari ke belakang
        
        Returns:
            List of dict dengan format:
            [{'date': 'YYYY-MM-DD', 'total': int, 'categories': {...}}, ...]
        """
        days = days or config.DEFAULT_TREND_DAYS
        
        try:
            trends = defaultdict(lambda: {'total': 0, 'categories': defaultdict(int)})
            cutoff = datetime.now() - timedelta(days=days)
            
            for q in self.queries:
                ts = datetime.fromisoformat(q['timestamp'])
                if ts > cutoff:
                    date_key = ts.strftime('%Y-%m-%d')
                    trends[date_key]['total'] += 1
                    category = q['category'] or 'unknown'
                    trends[date_key]['categories'][category] += 1
            
            # Isi tanggal yang kosong dengan 0
            result = []
            for i in range(days):
                date = (datetime.now() - timedelta(days=days-1-i)).strftime('%Y-%m-%d')
                if date in trends:
                    result.append({
                        'date': date,
                        'total': trends[date]['total'],
                        'categories': dict(trends[date]['categories'])
                    })
                else:
                    result.append({
                        'date': date,
                        'total': 0,
                        'categories': {}
                    })
            
            return result
        except Exception as e:
            print(f"❌ Error in get_daily_trends: {e}")
            return []
    
    def get_hourly_distribution(self, days: int = None) -> Dict[int, int]:
        """
        Dapatkan distribusi queries per jam.
        
        Args:
            days: Periode dalam hari
        
        Returns:
            Dict dengan format: {hour: count, ...} (hour = 0-23)
        """
        days = days or config.DEFAULT_ANALYTICS_DAYS
        
        try:
            cutoff = datetime.now() - timedelta(days=days)
            
            hours = [
                datetime.fromisoformat(q['timestamp']).hour
                for q in self.queries
                if datetime.fromisoformat(q['timestamp']) > cutoff
            ]
            
            return dict(Counter(hours))
        except Exception as e:
            print(f"❌ Error in get_hourly_distribution: {e}")
            return {}
    
    def get_feedback_stats(self, days: int = None) -> Dict[str, Any]:
        """
        Dapatkan statistik feedback.
        
        Args:
            days: Periode dalam hari
        
        Returns:
            Dict dengan keys: average_rating, total_feedback, 
            rating_distribution, recent_comments
        """
        days = days or config.DEFAULT_FEEDBACK_DAYS
        
        try:
            cutoff = datetime.now() - timedelta(days=days)
            
            recent_feedback = [
                f for f in self.feedback
                if datetime.fromisoformat(f['timestamp']) > cutoff
            ]
            
            if not recent_feedback:
                return {
                    'average_rating': 0,
                    'total_feedback': 0,
                    'rating_distribution': {},
                    'recent_comments': []
                }
            
            ratings = [f['rating'] for f in recent_feedback]
            
            return {
                'average_rating': round(sum(ratings) / len(ratings), 2),
                'total_feedback': len(recent_feedback),
                'rating_distribution': dict(Counter(ratings)),
                'recent_comments': [
                    f['comment'] for f in recent_feedback[-10:] 
                    if f.get('comment')
                ]
            }
        except Exception as e:
            print(f"❌ Error in get_feedback_stats: {e}")
            return {
                'average_rating': 0,
                'total_feedback': 0,
                'rating_distribution': {},
                'recent_comments': []
            }
    
    def get_fallback_rate(self, days: int = None) -> float:
        """
        Dapatkan persentase pertanyaan yang tidak terjawab (fallback).
        
        Args:
            days: Periode dalam hari
        
        Returns:
            Float persentase (0-100)
        """
        days = days or config.DEFAULT_ANALYTICS_DAYS
        
        try:
            cutoff = datetime.now() - timedelta(days=days)
            
            recent = [
                q for q in self.queries
                if datetime.fromisoformat(q['timestamp']) > cutoff
            ]
            
            if not recent:
                return 0.0
            
            fallbacks = sum(1 for q in recent if q.get('is_fallback', False))
            return round((fallbacks / len(recent)) * 100, 2)
        except Exception as e:
            print(f"❌ Error in get_fallback_rate: {e}")
            return 0.0
    
    def get_confidence_stats(self, days: int = None) -> Dict[str, float]:
        """
        Dapatkan statistik confidence score.
        
        Args:
            days: Periode dalam hari
        
        Returns:
            Dict dengan keys: average, min, max
        """
        days = days or config.DEFAULT_ANALYTICS_DAYS
        
        try:
            cutoff = datetime.now() - timedelta(days=days)
            
            confidences = [
                q['confidence'] for q in self.queries
                if datetime.fromisoformat(q['timestamp']) > cutoff
                and q.get('confidence') is not None
            ]
            
            if not confidences:
                return {'average': 0, 'min': 0, 'max': 0}
            
            return {
                'average': round(sum(confidences) / len(confidences), 2),
                'min': round(min(confidences), 2),
                'max': round(max(confidences), 2),
            }
        except Exception as e:
            print(f"❌ Error in get_confidence_stats: {e}")
            return {'average': 0, 'min': 0, 'max': 0}
    
    def get_summary_stats(self, days: int = None) -> Dict[str, Any]:
        """
        Dapatkan summary statistik untuk dashboard.
        Menggabungkan semua stats dalam satu call.
        
        Args:
            days: Periode dalam hari
        
        Returns:
            Dict dengan semua statistik penting
        """
        days = days or config.DEFAULT_ANALYTICS_DAYS
        
        try:
            cutoff = datetime.now() - timedelta(days=days)
            
            recent_queries = [
                q for q in self.queries
                if datetime.fromisoformat(q['timestamp']) > cutoff
            ]
            
            recent_sessions = {
                k: v for k, v in self.sessions.items()
                if datetime.fromisoformat(v['start_time']) > cutoff
            }
            
            return {
                'total_queries': len(recent_queries),
                'total_sessions': len(recent_sessions),
                'fallback_rate': self.get_fallback_rate(days),
                'avg_confidence': self.get_confidence_stats(days)['average'],
                'feedback_stats': self.get_feedback_stats(days),
                'top_categories': self.get_category_distribution(days),
            }
        except Exception as e:
            print(f"❌ Error in get_summary_stats: {e}")
            return {
                'total_queries': 0,
                'total_sessions': 0,
                'fallback_rate': 0,
                'avg_confidence': 0,
                'feedback_stats': {},
                'top_categories': {}
            }
    
    def __del__(self):
        """Destructor: save data saat object dihapus."""
        self._save_data(force=True)


# Singleton instance
_analytics_instance = None

def get_analytics(data_file: str = None) -> HRAnalytics:
    """
    Factory function untuk mendapatkan analytics instance.
    Menggunakan singleton pattern agar hanya ada 1 instance.
    
    Args:
        data_file: Path file JSON
    
    Returns:
        HRAnalytics instance
    """
    global _analytics_instance
    if _analytics_instance is None:
        _analytics_instance = HRAnalytics(data_file)
    return _analytics_instance