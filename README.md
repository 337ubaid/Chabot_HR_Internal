# HR Internal Chatbot 🤖

Chatbot internal untuk menjawab pertanyaan karyawan seputar kebijakan HR dengan sistem fuzzy matching dan analytics dashboard.

## 📋 Fitur

### 1. Interactive Chat
- ✅ Fuzzy matching dengan FuzzyWuzzy (toleran terhadap typo)
- ✅ Confidence score untuk setiap jawaban
- ✅ Suggestions jika pertanyaan tidak cocok
- ✅ Support 200+ variasi pertanyaan

### 2. Session Management
- ✅ Tracking aktivitas user
- ✅ Auto-prompt rating setelah 3 menit inaktif
- ✅ Session ID unik untuk analytics

### 3. Rating System
- ✅ Rating 1-5 bintang
- ✅ Komentar opsional
- ✅ Tracking kepuasan pengguna

### 4. Analytics Dashboard
- ✅ Top 10 pertanyaan
- ✅ Distribusi kategori
- ✅ Tren harian
- ✅ Distribusi jam aktif
- ✅ Statistik feedback
- ✅ Fallback rate

### 5. FAQ Browser
- ✅ Browse semua FAQ
- ✅ Filter by kategori
- ✅ Search functionality

## 🗂️ Struktur File

```
hr-chatbot/
│
├── config.py                 # Konfigurasi (threshold, timeout, dll)
├── hr_knowledge_base.py      # Database pertanyaan & jawaban
├── fuzzy_matcher.py          # Engine matching FuzzyWuzzy
├── analytics.py              # Module analytics & logging
├── app.py                    # Aplikasi Streamlit utama
├── requirements.txt          # Dependencies Python
├── hr_analytics_data.json    # Data analytics (auto-generated)
└── README.md                 # Dokumentasi
```

## 🚀 Cara Install & Run

### 1. Clone Repository
```bash
git clone <repo-url>
cd hr-chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Aplikasi
```bash
streamlit run app.py
```

Aplikasi akan buka di browser: `http://localhost:8501`

## ⚙️ Konfigurasi

Edit `config.py` untuk mengubah:

```python
# Threshold matching (0-100)
FUZZY_THRESHOLD = 65

# Timeout inactivity (menit)
INACTIVITY_TIMEOUT_MINUTES = 3

# Maximum chat history
MAX_CHAT_HISTORY = 100

# Batch saving
SAVE_BATCH_SIZE = 10
SAVE_INTERVAL_SECONDS = 60

# dsb..
```

## 📂 Kategori FAQ

Chatbot memahami pertanyaan dalam kategori:
- 🏖️ **Cuti** - Cuti tahunan, melahirkan, menikah
- 💰 **Gaji** - Jadwal gaji, slip gaji, potongan
- 🎁 **Benefit** - THR, bonus, asuransi, tunjangan
- ⏰ **Lembur** - Klaim lembur, approval
- 📋 **Administrasi** - BPJS, kartu akses, password
- 📈 **Karir** - Promosi, resign, KPI, training
- 🏢 **Fasilitas** - Shuttle bus, ruang laktasi, laptop
- 📜 **Kebijakan** - Jam kerja, WFH, dress code
- 💳 **Reimbursement** - Klaim parkir, medis
- 📞 **Kontak** - Hotline HR
- 👋 **Greeting** - Sapaan dasar

## 📝 Cara Menambah FAQ Baru

Edit `hr_knowledge_base.py`:

```python
{
    "kategori": "cuti",
    "pertanyaan_utama": "Pertanyaan baru?",
    "variasi": [
        "variasi 1",
        "variasi 2",
        "variasi 3",
    ],
    "jawaban": "Jawaban lengkap di sini."
}
```

Restart aplikasi untuk apply changes.

## 📊 Analytics Data

Data disimpan di `hr_analytics_data.json`:

```json
{
  "queries": [...],      // Log semua pertanyaan
  "feedback": [...],     // Log rating & komentar
  "sessions": {...}      // Info session user
}
```

**Note**: File ini auto-generated, tidak perlu edit manual.

## 🌐 Deploy ke Streamlit Cloud

### Option 1: File JSON (Temporary)
1. Push ke GitHub
2. Connect di [streamlit.io](https://streamlit.io)
3. Deploy!

⚠️ **Caveat**: Data analytics akan hilang setiap redeploy.

### Option 2: Supabase (Production)
Untuk persistent storage, ikuti guide di [DEPLOYMENT.md](DEPLOYMENT.md)

## 🤝 Kontribusi

Untuk menambah fitur atau fix bugs:

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push & create PR

## 📄 License

Internal use only


---

**Version**: 1.3
**Last Updated**: January 2026  
**Maintained by**: IT Team