"""
Configuration File untuk HR Chatbot
====================================
File ini berisi semua konfigurasi yang digunakan di seluruh aplikasi.
Jika ingin mengubah threshold, timeout, atau nilai lainnya,  edit di sini.
"""

class Config:
    """
    Kelas konfigurasi untuk HR Chatbot.
    Semua nilai yang sering diubah dikumpulkan di sini.
    """
    
    # ==================================================
    # FUZZY MATCHING SETTINGS
    # ==================================================
    # Threshold minimum untuk menganggap pertanyaan cocok (0-100)
    # Semakin tinggi = semakin ketat matching
    FUZZY_THRESHOLD = 65
    
    # Bobot untuk masing-masing algoritma fuzzy matching
    # Total harus = 1.0
    FUZZY_WEIGHTS = {
        'simple': 0.15,      # Kesamaan exact string
        'partial': 0.25,     # Deteksi substring
        'token_sort': 0.25,  # Abaikan urutan kata
        'token_set': 0.35,   # Abaikan kata duplikat
    }
    
    # ==================================================
    # SESSION MANAGEMENT
    # ==================================================
    # Berapa menit user tidak aktif sebelum muncul rating prompt
    INACTIVITY_TIMEOUT_MINUTES = 3
    
    # Maksimal jumlah pesan yang disimpan di memory
    # Mencegah memory penuh jika chat terlalu panjang
    MAX_CHAT_HISTORY = 100
    
    # ==================================================
    # ANALYTICS & DATA STORAGE
    # ==================================================
    # Nama file untuk menyimpan data analytics
    ANALYTICS_FILE = "hr_analytics_data.json"
    
    # Batasan data yang disimpan (untuk mencegah file terlalu besar)
    MAX_QUERIES_RETAINED = 10000   # Simpan max 10k queries terakhir
    MAX_FEEDBACK_RETAINED = 5000   # Simpan max 5k feedback terakhir
    MAX_SESSIONS_RETAINED = 1000   # Simpan max 1k sessions terakhir
    
    # Pengaturan batch saving (untuk efisiensi)
    SAVE_BATCH_SIZE = 10          # Save setiap 10 queries
    SAVE_INTERVAL_SECONDS = 60    # Atau save setiap 60 detik
    
    # Default periode untuk analytics
    DEFAULT_ANALYTICS_DAYS = 7
    DEFAULT_TREND_DAYS = 7
    DEFAULT_FEEDBACK_DAYS = 30
    
    # ==================================================
    # UI SETTINGS
    # ==================================================
    # Judul dan icon aplikasi
    PAGE_TITLE = "HR Chatbot Internal"
    PAGE_ICON = "🏢"
    
    # Pertanyaan cepat yang muncul di bottom chat
    QUICK_QUESTIONS = [
        "cuti tahunan berapa?",
        "gimana cara ngajuin cuti ya",
        "gaji turun tanggal brp",
        "ada shuttle bus ga",
        "halo",
    ]
    
    # ==================================================
    # DATA VALIDATION
    # ==================================================
    # Batasan panjang input untuk mencegah spam/abuse
    MAX_USER_INPUT_LENGTH = 500   # Maksimal 500 karakter untuk pertanyaan
    MAX_COMMENT_LENGTH = 1000     # Maksimal 1000 karakter untuk komentar
    
    # Range rating yang valid
    MIN_RATING = 1
    MAX_RATING = 5
    
    # ==================================================
    # CONTACT INFORMATION
    # ==================================================
    # Nomor hotline HR yang ditampilkan di fallback response
    HR_HOTLINE = "0812-XXXX-XXXX"
    
    # ==================================================
    # SUGGESTION SETTINGS
    # ==================================================
    # Berapa banyak suggestion yang ditampilkan saat fallback
    MAX_SUGGESTIONS = 3
    
    # Minimum score untuk menampilkan suggestion (0-100)
    SUGGESTION_MIN_SCORE = 40


# Singleton instance yang bisa diimport di file lain
config = Config()