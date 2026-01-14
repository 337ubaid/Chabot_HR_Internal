# 🏢 HR Internal Chatbot

Chatbot HR internal berbasis FuzzyWuzzy untuk menjawab pertanyaan karyawan seputar kebijakan perusahaan, dengan fitur analytics dashboard dan rating system.

## ✨ Fitur

### 1. Chat Interface
- **Natural Language Processing** - Menggunakan FuzzyWuzzy dengan multiple matching strategies
- **High Accuracy** - Kombinasi Token Set, Token Sort, Partial, dan Simple Ratio
- **Smart Suggestions** - Memberikan saran pertanyaan jika tidak ditemukan match

### 2. Session Management
- **Timeout Detection** - Mendeteksi inaktivitas setelah 3 menit
- **Auto Rating Prompt** - Meminta feedback setelah sesi selesai
- **Conversation History** - Menyimpan riwayat percakapan per sesi

### 3. Analytics Dashboard
- **Top 10 Queries** - Pertanyaan paling sering ditanyakan
- **Category Distribution** - Distribusi pertanyaan per kategori
- **Daily Trends** - Tren pertanyaan harian/mingguan
- **Hourly Distribution** - Jam-jam aktif penggunaan
- **Feedback Stats** - Statistik rating dan komentar
- **Accuracy Metrics** - Confidence score rata-rata

### 4. Rating System
- Rating 1-5 bintang
- Komentar opsional
- Tracking untuk improvement

## 📁 Struktur Project

```
hr_chatbot/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── data/
│   ├── __init__.py
│   └── hr_knowledge_base.py  # Knowledge base dengan variasi pertanyaan
├── core/
│   ├── __init__.py
│   ├── fuzzy_matcher.py      # FuzzyWuzzy matcher engine
│   └── analytics.py          # Analytics tracking module
└── hr_analytics_data.json    # Analytics data storage (auto-generated)
```

## 🚀 Cara Menjalankan

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone atau copy folder project
cd hr_chatbot

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
```

### Akses Aplikasi
Buka browser dan akses: `http://localhost:8501`

## 📂 Kategori Pertanyaan

| Kategori | Topik |
|----------|-------|
| 🏖️ Cuti | Cuti tahunan, cuti melahirkan, cuti menikah |
| 💰 Gaji | Tanggal gajian, slip gaji, potongan |
| 🎁 Benefit | Asuransi, THR, bonus, pinjaman |
| ⏰ Lembur | Cara lapor lembur |
| 📋 Administrasi | BPJS, password portal, kartu akses |
| 📈 Karir | Promosi, resign, KPI, training |
| 🏢 Fasilitas | Shuttle, ruang laktasi, laptop |
| 📜 Kebijakan | Jam kerja, WFH, dress code |
| 💳 Reimbursement | Klaim parkir, klaim medis |
| 📞 Kontak | HR Hotline |

## 🔧 Konfigurasi

### Threshold Matching
Edit di `app.py`:
```python
st.session_state.chatbot_engine = HRChatbotEngine(qa_pairs, threshold=65)
```
- Nilai lebih tinggi = lebih strict
- Nilai lebih rendah = lebih flexible

### Timeout Inaktivitas
Edit di `app.py` fungsi `check_inactivity()`:
```python
if time_since_last > timedelta(minutes=3):  # Ubah menit sesuai kebutuhan
```

### Menambah Pertanyaan Baru
Edit `data/hr_knowledge_base.py`:
```python
{
    "kategori": "nama_kategori",
    "pertanyaan_utama": "Pertanyaan utama?",
    "variasi": [
        "variasi 1",
        "variasi 2",
        # dst...
    ],
    "jawaban": "Jawaban lengkap untuk pertanyaan ini."
}
```

## 📊 Analytics Data

Data analytics disimpan di `hr_analytics_data.json` dengan format:
- **queries**: Log semua pertanyaan (max 10,000 terakhir)
- **feedback**: Log semua rating/komentar (max 5,000 terakhir)
- **sessions**: Data sesi pengguna (max 1,000 terakhir)

## 🎯 Algoritma Matching

FuzzyWuzzy menggunakan kombinasi weighted scoring:

| Method | Weight | Kegunaan |
|--------|--------|----------|
| Token Set Ratio | 35% | Kata berbeda urutan |
| Partial Ratio | 25% | Substring matching |
| Token Sort Ratio | 25% | Kata sama, urutan beda |
| Simple Ratio | 15% | Mirip persis |

## 📝 Contoh Penggunaan

### Pertanyaan Normal
```
User: "gimana cara ngajuin cuti ya?"
Bot:  "Pengajuan cuti dilakukan melalui portal HRIS maksimal 3 hari sebelum tanggal pengambilan cuti."
      Confidence: 87% | Category: CUTI
```

### Pertanyaan Tidak Dikenali
```
User: "xyz123"
Bot:  "Maaf, saya belum bisa memahami pertanyaan Anda..."
      [Suggestions: pertanyaan yang mungkin dimaksud]
```

## 🛠️ Troubleshooting

### Streamlit Error
```bash
pip install --upgrade streamlit
```

### FuzzyWuzzy Warning
```bash
pip install python-Levenshtein
```

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

## 📧 Support

Untuk pertanyaan teknis atau request fitur baru, hubungi tim IT Development.

---
**Version**: 1.0  
**Last Updated**: 2024  
**Internal Use Only**
