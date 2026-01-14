"""
HR Internal Chatbot - Streamlit Application
Features:
1. Interactive chat interface dengan FuzzyWuzzy matching
2. Session management dengan timeout detection
3. Rating system untuk feedback
4. HR Analytics Dashboard
"""

import streamlit as st
import sys
import os
import uuid
from datetime import datetime, timedelta
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.hr_knowledge_base import get_flat_qa_pairs, get_categories, HR_KNOWLEDGE_BASE
from core.fuzzy_matcher import HRChatbotEngine
from core.analytics import get_analytics

# Page configuration
st.set_page_config(
    page_title="HR Chatbot Internal",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .chat-message.bot {
        background-color: #f5f5f5;
        border-left: 4px solid #4CAF50;
    }
    .confidence-badge {
        font-size: 0.75rem;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
        background-color: #e8f5e9;
        color: #2e7d32;
    }
    .category-badge {
        font-size: 0.75rem;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
        background-color: #fff3e0;
        color: #e65100;
        margin-left: 0.5rem;
    }
    .stButton>button {
        width: 100%;
    }
    .rating-section {
        background-color: #fff8e1;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    div[data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'chatbot_engine' not in st.session_state:
        qa_pairs = get_flat_qa_pairs()
        st.session_state.chatbot_engine = HRChatbotEngine(qa_pairs, threshold=65)
    if 'analytics' not in st.session_state:
        st.session_state.analytics = get_analytics("hr_analytics_data.json")
    if 'last_activity' not in st.session_state:
        st.session_state.last_activity = datetime.now()
    if 'session_ended' not in st.session_state:
        st.session_state.session_ended = False
    if 'rating_submitted' not in st.session_state:
        st.session_state.rating_submitted = False
    if 'show_rating_prompt' not in st.session_state:
        st.session_state.show_rating_prompt = False

init_session_state()

# Sidebar Navigation
st.sidebar.title("🏢 HR Chatbot")
page = st.sidebar.radio(
    "Menu",
    ["💬 Chat", "📊 Dashboard Analytics", "📚 FAQ Lengkap", "ℹ️ Tentang"],
    index=0
)

# Check for inactivity (3 minutes)
def check_inactivity():
    if st.session_state.messages and not st.session_state.session_ended:
        time_since_last = datetime.now() - st.session_state.last_activity
        if time_since_last > timedelta(minutes=3):
            st.session_state.show_rating_prompt = True

# ==================== CHAT PAGE ====================
def render_chat_page():
    st.title("💬 HR Assistant Chatbot")
    st.markdown("---")
    
    # Check inactivity
    check_inactivity()
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user">
                    <strong>👤 Anda:</strong>
                    <p>{message["content"]}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                confidence = message.get("confidence", 0)
                category = message.get("category", "")
                
                confidence_color = "#4CAF50" if confidence >= 75 else "#FF9800" if confidence >= 50 else "#f44336"
                
                badge_html = ""
                if confidence > 0:
                    badge_html += f'<span class="confidence-badge" style="background-color: {confidence_color}20; color: {confidence_color};">Confidence: {confidence:.0f}%</span>'
                if category:
                    badge_html += f'<span class="category-badge">{category.upper()}</span>'
                
                st.markdown(f"""
                <div class="chat-message bot">
                    <strong>🤖 HR Bot:</strong>
                    <p>{message["content"]}</p>
                    <div style="margin-top: 0.5rem;">{badge_html}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show suggestions if available
                if message.get("suggestions"):
                    with st.expander("💡 Mungkin yang Anda maksud:"):
                        for sug in message["suggestions"]:
                            if st.button(f"❓ {sug['question']}", key=f"sug_{i}_{sug['question'][:20]}"):
                                # Process suggested question
                                process_user_input(sug['question'])
                                st.rerun()
    
    # Rating prompt after inactivity
    if st.session_state.show_rating_prompt and not st.session_state.rating_submitted:
        st.markdown("---")
        st.markdown("""
        <div class="rating-section">
            <h4>⏰ Sepertinya percakapan sudah selesai...</h4>
            <p>Apakah Anda sudah selesai bertanya? Mohon berikan rating untuk membantu kami meningkatkan layanan.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            rating = st.slider("Rating pengalaman Anda:", 1, 5, 4, key="inactivity_rating")
        with col2:
            if st.button("🔄 Lanjut Chat", key="continue_chat"):
                st.session_state.show_rating_prompt = False
                st.session_state.last_activity = datetime.now()
                st.rerun()
        
        comment = st.text_area("Komentar (opsional):", key="inactivity_comment", height=80)
        
        if st.button("✅ Kirim Rating & Selesai", key="submit_inactivity_rating"):
            st.session_state.analytics.log_feedback(
                st.session_state.session_id,
                rating,
                comment if comment else None
            )
            st.session_state.rating_submitted = True
            st.session_state.session_ended = True
            st.success("Terima kasih atas feedback Anda! 🙏")
            st.rerun()
    
    # Chat input
    st.markdown("---")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Ketik pertanyaan Anda:",
            key="user_input",
            placeholder="Contoh: Berapa jatah cuti tahunan saya?",
            disabled=st.session_state.session_ended
        )
    
    with col2:
        send_clicked = st.button("Kirim 📤", disabled=st.session_state.session_ended)
    
    if (send_clicked or user_input) and user_input.strip():
        process_user_input(user_input.strip())
        st.rerun()
    
    # End chat button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.session_ended:
            if st.button("🏁 Selesai & Beri Rating", use_container_width=True):
                st.session_state.show_rating_prompt = True
                st.rerun()
        else:
            if st.button("🔄 Mulai Percakapan Baru", use_container_width=True):
                # Reset session
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.messages = []
                st.session_state.last_activity = datetime.now()
                st.session_state.session_ended = False
                st.session_state.rating_submitted = False
                st.session_state.show_rating_prompt = False
                st.rerun()
    
    # Quick action buttons
    st.markdown("---")
    st.markdown("**🚀 Pertanyaan Populer:**")
    quick_questions = [
        "Berapa jatah cuti tahunan?",
        "Kapan gaji cair?",
        "Cara ajukan cuti?",
        "Aturan WFH?",
        "THR kapan diberikan?",
    ]
    
    cols = st.columns(len(quick_questions))
    for i, q in enumerate(quick_questions):
        with cols[i]:
            if st.button(q, key=f"quick_{i}", disabled=st.session_state.session_ended):
                process_user_input(q)
                st.rerun()

def process_user_input(user_input: str):
    """Process user input and generate response."""
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Get response
    response = st.session_state.chatbot_engine.get_response(user_input)
    
    # Log to analytics
    st.session_state.analytics.log_query(
        st.session_state.session_id,
        user_input,
        response
    )
    
    # Add bot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response['answer'],
        "confidence": response['confidence'],
        "category": response['category'],
        "suggestions": response.get('suggestions', [])
    })
    
    # Update last activity
    st.session_state.last_activity = datetime.now()
    st.session_state.show_rating_prompt = False

# ==================== DASHBOARD PAGE ====================
def render_dashboard_page():
    st.title("📊 HR Analytics Dashboard")
    st.markdown("---")
    
    analytics = st.session_state.analytics
    
    # Time range selector
    days = st.selectbox("Periode:", [7, 14, 30], index=0, format_func=lambda x: f"{x} hari terakhir")
    
    # Summary metrics
    summary = analytics.get_summary_stats(days)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Pertanyaan",
            summary['total_queries'],
            help="Jumlah pertanyaan dalam periode ini"
        )
    
    with col2:
        st.metric(
            "Total Sesi",
            summary['total_sessions'],
            help="Jumlah sesi unik"
        )
    
    with col3:
        st.metric(
            "Fallback Rate",
            f"{summary['fallback_rate']:.1f}%",
            help="Persentase pertanyaan yang tidak terjawab"
        )
    
    with col4:
        avg_rating = summary['feedback_stats'].get('average_rating', 0)
        st.metric(
            "Rating Rata-rata",
            f"⭐ {avg_rating:.1f}/5" if avg_rating > 0 else "N/A",
            help="Rating kepuasan pengguna"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Tren Pertanyaan Harian")
        daily_trends = analytics.get_daily_trends(days)
        
        if daily_trends:
            import pandas as pd
            df_trends = pd.DataFrame(daily_trends)
            st.line_chart(df_trends.set_index('date')['total'])
        else:
            st.info("Belum ada data untuk ditampilkan")
    
    with col2:
        st.subheader("📊 Distribusi Kategori")
        categories = analytics.get_category_distribution(days)
        
        if categories:
            import pandas as pd
            df_cat = pd.DataFrame(list(categories.items()), columns=['Kategori', 'Jumlah'])
            df_cat = df_cat.sort_values('Jumlah', ascending=False)
            st.bar_chart(df_cat.set_index('Kategori'))
        else:
            st.info("Belum ada data untuk ditampilkan")
    
    st.markdown("---")
    
    # Top queries
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔝 Top 10 Pertanyaan")
        top_queries = analytics.get_top_queries(10, days)
        
        if top_queries:
            for i, item in enumerate(top_queries, 1):
                st.markdown(f"**{i}.** {item['query']} ({item['count']}x)")
        else:
            st.info("Belum ada data untuk ditampilkan")
    
    with col2:
        st.subheader("⏰ Distribusi Jam Aktif")
        hourly = analytics.get_hourly_distribution(days)
        
        if hourly:
            import pandas as pd
            # Create full 24-hour distribution
            full_hourly = {h: hourly.get(h, 0) for h in range(24)}
            df_hourly = pd.DataFrame(list(full_hourly.items()), columns=['Jam', 'Jumlah'])
            df_hourly = df_hourly.sort_values('Jam')
            st.bar_chart(df_hourly.set_index('Jam'))
        else:
            st.info("Belum ada data untuk ditampilkan")
    
    st.markdown("---")
    
    # Feedback section
    st.subheader("💬 Feedback & Rating")
    
    feedback_stats = analytics.get_feedback_stats(days)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Feedback", feedback_stats['total_feedback'])
    
    with col2:
        rating_dist = feedback_stats.get('rating_distribution', {})
        if rating_dist:
            st.markdown("**Distribusi Rating:**")
            for rating in range(5, 0, -1):
                count = rating_dist.get(rating, 0)
                st.progress(count / max(rating_dist.values()) if rating_dist.values() else 0)
                st.caption(f"{'⭐' * rating}: {count}")
    
    with col3:
        comments = feedback_stats.get('recent_comments', [])
        if comments:
            st.markdown("**Komentar Terbaru:**")
            for comment in comments[-5:]:
                st.markdown(f"- _{comment}_")
        else:
            st.info("Belum ada komentar")
    
    st.markdown("---")
    
    # Confidence stats
    st.subheader("🎯 Statistik Akurasi")
    conf_stats = analytics.get_confidence_stats(days)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Confidence Rata-rata", f"{conf_stats['average']:.1f}%")
    with col2:
        st.metric("Confidence Minimum", f"{conf_stats['min']:.1f}%")
    with col3:
        st.metric("Confidence Maximum", f"{conf_stats['max']:.1f}%")

# ==================== FAQ PAGE ====================
def render_faq_page():
    st.title("📚 FAQ Lengkap HR")
    st.markdown("---")
    
    # Category filter
    all_categories = get_categories()
    selected_category = st.selectbox(
        "Filter Kategori:",
        ["Semua"] + sorted(all_categories)
    )
    
    # Search
    search_term = st.text_input("🔍 Cari pertanyaan:", "")
    
    st.markdown("---")
    
    # Display FAQs
    for item in HR_KNOWLEDGE_BASE:
        # Filter by category
        if selected_category != "Semua" and item['kategori'] != selected_category:
            continue
        
        # Filter by search term
        if search_term:
            if search_term.lower() not in item['pertanyaan_utama'].lower() and \
               search_term.lower() not in item['jawaban'].lower():
                continue
        
        with st.expander(f"❓ {item['pertanyaan_utama']}"):
            st.markdown(f"**Jawaban:**\n\n{item['jawaban']}")
            st.markdown(f"**Kategori:** `{item['kategori'].upper()}`")
            
            # Show variations
            if item['variasi']:
                st.markdown("**Variasi pertanyaan yang dipahami:**")
                st.caption(", ".join(item['variasi'][:5]) + ("..." if len(item['variasi']) > 5 else ""))

# ==================== ABOUT PAGE ====================
def render_about_page():
    st.title("ℹ️ Tentang HR Chatbot")
    st.markdown("---")
    
    st.markdown("""
    ### 🤖 HR Internal Chatbot
    
    Chatbot ini dirancang untuk membantu karyawan mendapatkan informasi seputar kebijakan HR dengan cepat dan mudah.
    
    #### ✨ Fitur Utama:
    
    1. **Chat Interaktif**
       - Tanya jawab dengan bahasa natural
       - Matching berbasis FuzzyWuzzy untuk akurasi tinggi
       - Suggestion untuk pertanyaan yang mirip
    
    2. **Session Management**
       - Deteksi inaktivitas (3 menit)
       - Prompt untuk feedback setelah selesai
       - History percakapan per sesi
    
    3. **Rating System**
       - Rating 1-5 bintang
       - Komentar opsional
       - Tracking kepuasan pengguna
    
    4. **Analytics Dashboard**
       - Top pertanyaan
       - Distribusi kategori
       - Tren waktu
       - Statistik feedback
    
    #### 📂 Kategori yang Tersedia:
    """)
    
    categories = get_categories()
    cols = st.columns(3)
    category_icons = {
        'cuti': '🏖️',
        'gaji': '💰',
        'benefit': '🎁',
        'lembur': '⏰',
        'administrasi': '📋',
        'karir': '📈',
        'fasilitas': '🏢',
        'kebijakan': '📜',
        'reimbursement': '💳',
        'kontak': '📞',
        'greeting': '👋',
    }
    
    for i, cat in enumerate(sorted(categories)):
        with cols[i % 3]:
            icon = category_icons.get(cat, '📌')
            st.markdown(f"{icon} **{cat.upper()}**")
    
    st.markdown("---")
    
    st.markdown("""
    #### 🔧 Teknologi yang Digunakan:
    - **FuzzyWuzzy** - String matching
    - **Streamlit** - Web interface
    - **Python** - Backend logic
    
    #### 📧 Kontak:
    Untuk pertanyaan yang tidak terjawab, silakan hubungi HR Hotline di **0812-XXXX-XXXX**
    """)

# ==================== MAIN ====================
if page == "💬 Chat":
    render_chat_page()
elif page == "📊 Dashboard Analytics":
    render_dashboard_page()
elif page == "📚 FAQ Lengkap":
    render_faq_page()
elif page == "ℹ️ Tentang":
    render_about_page()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    HR Chatbot v1.0<br>
    © 2024 Internal Use Only
</div>
""", unsafe_allow_html=True)
