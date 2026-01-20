# HR Chatbot Analytics Module
# Tracking queries, categories, trends, and feedback

import json
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import List, Dict, Optional, Any
import threading

class HRAnalytics:
    """
    Analytics engine untuk HR Chatbot.
    Features:
    - Query logging
    - Category tracking
    - Time-based trends
    - Feedback collection
    - Session management
    """
    
    def __init__(self, data_file: str = "analytics_data.json"):
        self.data_file = data_file
        self.lock = threading.Lock()
        self._load_data()
    
    def _load_data(self):
        """Load existing data from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.queries = data.get('queries', [])
                    self.feedback = data.get('feedback', [])
                    self.sessions = data.get('sessions', {})
            except (json.JSONDecodeError, IOError):
                self._init_empty_data()
        else:
            self._init_empty_data()
    
    def _init_empty_data(self):
        """Initialize empty data structures."""
        self.queries = []
        self.feedback = []
        self.sessions = {}
    
    def _save_data(self):
        """Save data to file."""
        with self.lock:
            try:
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'queries': self.queries[-10000:],  # Keep last 10k queries
                        'feedback': self.feedback[-5000:],  # Keep last 5k feedback
                        'sessions': dict(list(self.sessions.items())[-1000:])  # Keep last 1k sessions
                    }, f, ensure_ascii=False, indent=2)
            except IOError as e:
                print(f"Error saving analytics data: {e}")
    
    def log_query(self, session_id: str, user_input: str, response: dict):
        """
        Log a query for analytics.
        
        Args:
            session_id: Unique session identifier
            user_input: User's question
            response: Chatbot response dict
        """
        query_record = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'user_input': user_input,
            'category': response.get('category'),
            'confidence': response.get('confidence', 0),
            'is_fallback': response.get('is_fallback', False),
        }
        
        self.queries.append(query_record)
        
        # Update session
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'start_time': datetime.now().isoformat(),
                'query_count': 0,
                'last_activity': datetime.now().isoformat(),
                'rated': False,
            }
        
        self.sessions[session_id]['query_count'] += 1
        self.sessions[session_id]['last_activity'] = datetime.now().isoformat()
        
        self._save_data()
    
    def log_feedback(self, session_id: str, rating: int, comment: Optional[str] = None):
        """
        Log user feedback.
        
        Args:
            session_id: Session identifier
            rating: Rating 1-5
            comment: Optional comment
        """
        feedback_record = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'rating': rating,
            'comment': comment,
        }
        
        self.feedback.append(feedback_record)
        
        if session_id in self.sessions:
            self.sessions[session_id]['rated'] = True
            self.sessions[session_id]['rating'] = rating
        
        self._save_data()
    
    def get_top_queries(self, n: int = 10, days: int = 30) -> List[Dict]:
        """Get top N most common queries in the last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        
        recent_queries = [
            q['user_input'].lower() 
            for q in self.queries 
            if datetime.fromisoformat(q['timestamp']) > cutoff
        ]
        
        counter = Counter(recent_queries)
        return [
            {'query': query, 'count': count}
            for query, count in counter.most_common(n)
        ]
    
    def get_category_distribution(self, days: int = 30) -> Dict[str, int]:
        """Get distribution of queries by category."""
        cutoff = datetime.now() - timedelta(days=days)
        
        categories = [
            q['category'] or 'unknown'
            for q in self.queries
            if datetime.fromisoformat(q['timestamp']) > cutoff
        ]
        
        return dict(Counter(categories))
    
    def get_daily_trends(self, days: int = 7) -> List[Dict]:
        """Get daily query counts for the last N days."""
        trends = defaultdict(lambda: {'total': 0, 'categories': defaultdict(int)})
        cutoff = datetime.now() - timedelta(days=days)
        
        for q in self.queries:
            ts = datetime.fromisoformat(q['timestamp'])
            if ts > cutoff:
                date_key = ts.strftime('%Y-%m-%d')
                trends[date_key]['total'] += 1
                category = q['category'] or 'unknown'
                trends[date_key]['categories'][category] += 1
        
        # Fill in missing dates
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
    
    def get_hourly_distribution(self, days: int = 7) -> Dict[int, int]:
        """Get distribution of queries by hour of day."""
        cutoff = datetime.now() - timedelta(days=days)
        
        hours = [
            datetime.fromisoformat(q['timestamp']).hour
            for q in self.queries
            if datetime.fromisoformat(q['timestamp']) > cutoff
        ]
        
        return dict(Counter(hours))
    
    def get_feedback_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get feedback statistics."""
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
            }
        
        ratings = [f['rating'] for f in recent_feedback]
        
        return {
            'average_rating': sum(ratings) / len(ratings),
            'total_feedback': len(recent_feedback),
            'rating_distribution': dict(Counter(ratings)),
            'recent_comments': [
                f['comment'] for f in recent_feedback[-10:] 
                if f.get('comment')
            ]
        }
    
    def get_fallback_rate(self, days: int = 7) -> float:
        """Get percentage of queries that resulted in fallback responses."""
        cutoff = datetime.now() - timedelta(days=days)
        
        recent = [
            q for q in self.queries
            if datetime.fromisoformat(q['timestamp']) > cutoff
        ]
        
        if not recent:
            return 0.0
        
        fallbacks = sum(1 for q in recent if q.get('is_fallback', False))
        return (fallbacks / len(recent)) * 100
    
    def get_confidence_stats(self, days: int = 7) -> Dict[str, float]:
        """Get confidence score statistics."""
        cutoff = datetime.now() - timedelta(days=days)
        
        confidences = [
            q['confidence'] for q in self.queries
            if datetime.fromisoformat(q['timestamp']) > cutoff
            and q.get('confidence') is not None
        ]
        
        if not confidences:
            return {'average': 0, 'min': 0, 'max': 0}
        
        return {
            'average': sum(confidences) / len(confidences),
            'min': min(confidences),
            'max': max(confidences),
        }
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get info about a specific session."""
        return self.sessions.get(session_id)
    
    def check_session_inactive(self, session_id: str, timeout_minutes: int = 3) -> bool:
        """Check if a session has been inactive for more than timeout_minutes."""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        last_activity = datetime.fromisoformat(session['last_activity'])
        inactive_duration = datetime.now() - last_activity
        
        return inactive_duration > timedelta(minutes=timeout_minutes)
    
    def get_summary_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get summary statistics for dashboard."""
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


# Singleton instance
_analytics_instance = None

def get_analytics(data_file: str = "analytics_data.json") -> HRAnalytics:
    """Get or create analytics singleton."""
    global _analytics_instance
    if _analytics_instance is None:
        _analytics_instance = HRAnalytics(data_file)
    return _analytics_instance


if __name__ == "__main__":
    # Test analytics
    analytics = get_analytics("test_analytics.json")
    
    # Simulate some queries
    import uuid
    session_id = str(uuid.uuid4())
    
    test_responses = [
        {'category': 'cuti', 'confidence': 85, 'is_fallback': False},
        {'category': 'gaji', 'confidence': 92, 'is_fallback': False},
        {'category': 'cuti', 'confidence': 78, 'is_fallback': False},
        {'category': None, 'confidence': 45, 'is_fallback': True},
        {'category': 'benefit', 'confidence': 88, 'is_fallback': False},
    ]
    
    for i, resp in enumerate(test_responses):
        analytics.log_query(session_id, f"Test query {i}", resp)
    
    analytics.log_feedback(session_id, 4, "Cukup membantu!")
    
    print("Summary Stats:")
    print(json.dumps(analytics.get_summary_stats(), indent=2, default=str))
