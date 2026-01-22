"""
HR Internal Chatbot - Streamlit Application
============================================
Aplikasi chatbot HR dengan interface web menggunakan Streamlit.

Fitur utama:
1. Interactive chat interface dengan fuzzy matching
2. Session management dengan timeout detection
3. Rating system untuk feedback
4. Analytics dashboard
5. FAQ browser
"""

import streamlit as st
import sys
import os
import uuid
from datetime import datetime, timedelta

# Add parent directory untuk imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hr_knowledge_base import get_flat_qa_pairs, get_categories, HR_KNOWLEDGE_BASE
from fuzzy_matcher import HRChatbotEngine
from analytics import get_analytics
from config import config

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    /* Styling untuk chat messages */
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
    
    /* Badge untuk confidence dan category */
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
    
    /* Rating section */
    .rating-section {
        background-color: #fff8e1;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """
    Initialize semua session state variables.
    Dipanggil saat app pertama kali load.
    """
    # Session ID unik untuk tracking
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    # Chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Chatbot engine
    if 'chatbot_engine' not in st.session_state:
        qa_pairs = get_flat_qa_pairs()
        st.session_state.chatbot_engine = HRChatbotEngine(qa_pairs, threshold=config.FUZZY_THRESHOLD)
    
    # Analytics engine
    if 'analytics' not in st.session_state:
        st.session_state.analytics = get_analytics(config.ANALYTICS_FILE)
    
    # Session tracking
    if 'last_activity' not in st.session_state:
        st.session_state.last_activity = datetime.now()
    
    # Session status
    if 'session_ended' not in st.session_state:
        st.session_state.session_ended = False
    
    # Rating status
    if 'rating_submitted' not in st.session_state:
        st.session_state.rating_submitted = False
    
    # Rating prompt visibility
    if 'show_rating_prompt' not in st.session_state:
        st.session_state.show_rating_prompt = False
    
    # Input counter untuk reset textbox
    if 'input_counter' not in st.session_state:
        st.session_state.input_counter = 0


# Initialize session state
init_session_state()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.title(f"{config.PAGE_ICON} HR Chatbot")
page = st.sidebar.radio(
    "Menu",
    ["💬 Chat", "📊 Dashboard Analytics", "📚 FAQ Lengkap", "ℹ️ Tentang"],
    index=0
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def check_inactivity():
    """
    Check apakah user sudah tidak aktif selama N menit.
    Jika ya, tampilkan rating prompt.
    """
    if st.session_state.messages and not st.session_state.session_ended:
        time_since_last = datetime.now() - st.session_state.last_activity
        if time_since_last > timedelta(minutes=config.INACTIVITY_TIMEOUT_MINUTES):
            st.session_state.show_rating_prompt = True


def process_user_input(user_input: str):
    """
    Process input dari user dan generate response.
    
    Args:
        user_input: Pertanyaan dari user
    """
    # Validasi input
    if not user_input or not user_input.strip():
        return
    
    # Sanitize input
    user_input = user_input.strip()[:config.MAX_USER_INPUT_LENGTH]
    
    # Check duplicate message (mencegah double submit)
    if st.session_state.messages:
        last_message = st.session_state.messages[-1]
        if last_message["role"] == "user" and last_message["content"] == user_input:
            return  # Skip jika duplikat
    
    # Add user message ke history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Get response dari chatbot
    response = st.session_state.chatbot_engine.get_response(user_input)
    
    # Log ke analytics
    st.session_state.analytics.log_query(
        st.session_state.session_id,
        user_input,
        response
    )
    
    # Add bot response ke history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response['answer'],
        "confidence": response['confidence'],
        "category": response['category'],
        "suggestions": response.get('suggestions', [])
    })
    
    # Limit chat history untuk mencegah memory leak
    if len(st.session_state.messages) > config.MAX_CHAT_HISTORY:
        st.session_state.messages = st.session_state.messages[-config.MAX_CHAT_HISTORY:]
    
    # Update last activity
    st.session_state.last_activity = datetime.now()
    st.session_state.show_rating_prompt = False


# ============================================================================
# PAGE: CHAT
# ============================================================================

def render_chat_page():
    """Render halaman chat utama."""
    st.title("💬 HR Assistant Chatbot")
    
    # Check inactivity
    check_inactivity()
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                # User message
                st.markdown(f"""
                <div class="chat-message user">
                    <strong>👤 Anda:</strong>
                    <p>{message["content"]}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Bot message
                confidence = message.get("confidence", 0)
                category = message.get("category", "")
                
                # Determine confidence color
                if confidence >= 75:
                    conf_color = "#4CAF50"  # Green
                elif confidence >= 50:
                    conf_color = "#FF9800"  # Orange
                else:
                    conf_color = "#f44336"  # Red
                
                # Build badges HTML
                badge_html = ""
                if confidence > 0:
                    badge_html += f'<span class="confidence-badge" style="background-color: {conf_color}20; color: {conf_color};">Confidence: {confidence:.0f}%</span>'
                if category:
                    badge_html += f'<span class="category-badge">{category.upper()}</span>'
                
                st.markdown(f"""
                <div class="chat-message bot">
                    <strong>🤖 HR Bot:</strong>
                    <p>{message["content"]}</p>
                    <div style="margin-top: 0.5rem;">{badge_html}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show suggestions jika ada
                if message.get("suggestions"):
                    with st.expander("💡 Mungkin yang Anda maksud:"):
                        for sug in message["suggestions"]:
                            # Button unik per suggestion
                            if st.button(
                                f"✓ {sug['question']}", 
                                key=f"sug_{i}_{hash(sug['question'])}"
                            ):
                                process_user_input(sug['question'])
                                st.session_state.input_counter += 1
                                st.rerun()
    
    # Rating prompt setelah inactivity
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
            rating = st.slider(
                "Rating pengalaman Anda:", 
                config.MIN_RATING, 
                config.MAX_RATING, 
                4, 
                key="inactivity_rating"
            )
        
        with col2:
            if st.button("🔄 Lanjut Chat", key="continue_chat"):
                st.session_state.show_rating_prompt = False
                st.session_state.last_activity = datetime.now()
                st.rerun()
        
        comment = st.text_area(
            "Komentar (opsional):", 
            key="inactivity_comment", 
            height=80,
            max_chars=config.MAX_COMMENT_LENGTH
        )
        
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
    
    # Chat input section
    st.markdown("---")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        # Dynamic key untuk auto-reset input field
        user_input = st.text_input(
            "Ketik pertanyaan Anda:",
            key=f"user_input_{st.session_state.input_counter}",
            placeholder="Contoh: Berapa jatah cuti tahunan saya?",
            disabled=st.session_state.session_ended
        )
    
    with col2:
        send_clicked = st.button(
            "Kirim 📤", 
            disabled=st.session_state.session_ended
        )
    
    # Process input jika ada
    if send_clicked and user_input and user_input.strip():
        process_user_input(user_input.strip())
        st.session_state.input_counter += 1  # Increment untuk reset input
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
                st.session_state.input_counter += 1
                st.rerun()
    
    # Quick action buttons
    st.markdown("---")
    st.markdown("**🚀 Pertanyaan Populer:**")
    
    quick_qs = config.QUICK_QUESTIONS
    cols = st.columns(len(quick_qs))
    
    for i, q in enumerate(quick_qs):
        with cols[i]:
            if st.button(
                q, 
                key=f"quick_{i}", 
                disabled=st.session_state.session_ended
            ):
                process_user_input(q)
                st.session_state.input_counter += 1
                st.rerun()


# ============================================================================
# PAGE: DASHBOARD ANALYTICS
# ============================================================================

def render_dashboard_page():
    """Render halaman analytics dashboard."""
    st.title("📊 HR Analytics Dashboard")
    st.markdown("---")
    
    analytics = st.session_state.analytics
    
    # Time range selector
    days = st.selectbox(
        "Periode:", 
        [7, 14, 30], 
        index=0, 
        format_func=lambda x: f"{x} hari terakhir"
    )
    
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
            help="Jumlah sesi percakapan unik"
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
            df_cat = pd.DataFrame(
                list(categories.items()), 
                columns=['Kategori', 'Jumlah']
            )
            df_cat = df_cat.sort_values('Jumlah', ascending=False)
            st.bar_chart(df_cat.set_index('Kategori'))
        else:
            st.info("Belum ada data untuk ditampilkan")
    
    st.markdown("---")
    
    # Top queries dan hourly distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Top 10 Pertanyaan")
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
            df_hourly = pd.DataFrame(
                list(full_hourly.items()), 
                columns=['Jam', 'Jumlah']
            )
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
                max_count = max(rating_dist.values()) if rating_dist.values() else 1
                st.progress(count / max_count)
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


# ============================================================================
# PAGE: FAQ LENGKAP
# ============================================================================

def render_faq_page():
    """Render halaman FAQ browser."""
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
            if (search_term.lower() not in item['pertanyaan_utama'].lower() and 
                search_term.lower() not in item['jawaban'].lower()):
                continue
        
        with st.expander(f"{item['pertanyaan_utama']}"):
            st.markdown(f"**Jawaban:**\n\n{item['jawaban']}")
            st.markdown(f"**Kategori:** `{item['kategori'].upper()}`")
            
            # Show variations
            if item['variasi']:
                st.markdown("**Variasi pertanyaan yang dipahami:**")
                variasi_text = ", ".join(item['variasi'][:5])
                if len(item['variasi']) > 5:
                    variasi_text += "..."
                st.caption(variasi_text)


# ============================================================================
# PAGE: TENTANG
# ============================================================================

def render_about_page():
    """Render halaman about/info."""
    st.title("ℹ️ Tentang HR Chatbot")
    st.markdown("---")
    
    st.markdown("""
    ### 🤖 HR Internal Chatbot
    
    Chatbot ini dirancang untuk membantu karyawan mendapatkan informasi seputar 
    kebijakan HR dengan cepat dan mudah.
    
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
    
    # Icon mapping untuk kategori
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
    
    st.markdown(f"""
    #### 🔧 Teknologi yang Digunakan:
    - **FuzzyWuzzy** - String matching algorithm
    - **Streamlit** - Web interface framework
    - **Python** - Backend programming language
    
    #### 📧 Kontak:
    Untuk pertanyaan yang tidak terjawab, silakan hubungi HR Hotline di **{config.HR_HOTLINE}**
    """)


# ============================================================================
# MAIN ROUTER
# ============================================================================

# Route ke halaman yang dipilih
if page == "💬 Chat":
    render_chat_page()
elif page == "📊 Dashboard Analytics":
    render_dashboard_page()
elif page == "📚 FAQ Lengkap":
    render_faq_page()
elif page == "ℹ️ Tentang":
    render_about_page()

# ============================================================================
# FOOTER
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    HR Chatbot v1.3<br>
    © 2026 Internal Use Only
</div>
""", unsafe_allow_html=True)