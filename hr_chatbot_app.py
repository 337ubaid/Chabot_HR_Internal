"""
HR INTERNAL CHATBOT - SINGLE FILE VERSION
==========================================
Chatbot HR dengan FuzzyWuzzy + Streamlit + Analytics Dashboard

Cara jalankan:
1. pip install streamlit fuzzywuzzy python-Levenshtein pandas
2. streamlit run hr_chatbot_app.py
"""

import streamlit as st
import json
import os
import uuid
import re
import threading
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import List, Dict, Optional, Any, Tuple
from fuzzywuzzy import fuzz

# ============================================================================
# KNOWLEDGE BASE - DATA PERTANYAAN & JAWABAN HR
# ============================================================================

HR_KNOWLEDGE_BASE = [
    # ==================== KATEGORI: CUTI ====================
    {
        "kategori": "cuti",
        "pertanyaan_utama": "Berapa jatah cuti tahunan saya?",
        "variasi": [
            "berapa cuti tahunan", "jatah cuti setahun", "total cuti pertahun",
            "cuti tahunan berapa hari", "berapa hari cuti dalam setahun",
            "hak cuti karyawan", "jumlah cuti tahunan", "saya dapat cuti berapa hari",
            "cuti annual berapa", "annual leave berapa hari",
        ],
        "jawaban": "Karyawan berhak mendapatkan 12 hari cuti tahunan setelah bekerja selama 12 bulan berturut-turut."
    },
    {
        "kategori": "cuti",
        "pertanyaan_utama": "Bagaimana cara mengajukan cuti?",
        "variasi": [
            "cara ajukan cuti", "prosedur pengajuan cuti", "mau ambil cuti gimana",
            "apply cuti dimana", "submit cuti bagaimana", "cara request cuti",
            "pengajuan cuti lewat mana", "mau cuti harus ngapain", "langkah ambil cuti",
            "cara minta cuti",
        ],
        "jawaban": "Pengajuan cuti dilakukan melalui portal HRIS maksimal 3 hari sebelum tanggal pengambilan cuti."
    },
    {
        "kategori": "cuti",
        "pertanyaan_utama": "Berapa lama cuti melahirkan?",
        "variasi": [
            "cuti melahirkan berapa bulan", "maternity leave berapa lama",
            "cuti hamil berapa hari", "hak cuti lahiran", "cuti persalinan",
            "cuti ibu melahirkan", "lama cuti hamil", "durasi cuti melahirkan",
            "jatah cuti lahiran", "berapa hari cuti melahirkan",
        ],
        "jawaban": "Cuti melahirkan diberikan selama 3 bulan (90 hari kalender) dengan gaji penuh."
    },
    {
        "kategori": "cuti",
        "pertanyaan_utama": "Apakah sisa cuti bisa diuangkan?",
        "variasi": [
            "cuti bisa dicairkan tidak", "sisa cuti jadi uang", "tukar cuti dengan uang",
            "cuti hangus atau diuangkan", "kompensasi sisa cuti", "cuti tidak terpakai gimana",
            "cuti bisa dituker duit", "cuti yang tidak diambil", "cairkan sisa cuti",
            "konversi cuti ke uang",
        ],
        "jawaban": "Sesuai kebijakan perusahaan, sisa cuti tahunan tidak dapat diuangkan dan akan hangus di akhir tahun jika tidak digunakan."
    },
    {
        "kategori": "cuti",
        "pertanyaan_utama": "Berapa jatah cuti menikah?",
        "variasi": [
            "cuti nikah berapa hari", "hak cuti pernikahan", "cuti kawin",
            "jatah cuti wedding", "cuti untuk menikah", "berapa lama cuti nikah",
            "cuti khusus menikah", "marriage leave", "izin nikah berapa hari",
            "cuti hari pernikahan",
        ],
        "jawaban": "Karyawan diberikan cuti khusus menikah selama 3 hari kerja."
    },
    
    # ==================== KATEGORI: GAJI ====================
    {
        "kategori": "gaji",
        "pertanyaan_utama": "Kapan gaji bulanan cair?",
        "variasi": [
            "tanggal gajian", "gaji turun kapan", "payroll kapan", "salary kapan masuk",
            "gaji dibayar tanggal berapa", "jadwal gajian", "kapan terima gaji",
            "gaji masuk tanggal", "pembayaran gaji kapan", "payday kapan",
        ],
        "jawaban": "Gaji dibayarkan setiap tanggal 25. Jika tanggal 25 jatuh pada hari libur, maka akan dibayarkan pada hari kerja sebelumnya."
    },
    {
        "kategori": "gaji",
        "pertanyaan_utama": "Di mana saya bisa ambil slip gaji?",
        "variasi": [
            "download slip gaji", "lihat slip gaji dimana", "payslip dimana",
            "cara dapat slip gaji", "akses slip gaji", "cetak slip gaji",
            "slip gaji online", "bukti gaji dimana", "struk gaji", "print payslip",
        ],
        "jawaban": "Slip gaji dapat diunduh dalam format PDF melalui portal HRIS menu 'My Payroll'."
    },
    {
        "kategori": "gaji",
        "pertanyaan_utama": "Apakah ada potongan gaji jika izin?",
        "variasi": [
            "izin dipotong gaji", "gaji dipotong kalau izin", "unpaid leave potong gaji",
            "izin tanpa cuti kena potong", "kalau izin gaji berkurang",
            "potongan untuk izin pribadi", "izin tidak pakai cuti",
            "gaji dikurangi kalau absen", "absen dipotong gaji tidak", "potong gaji karena izin",
        ],
        "jawaban": "Izin pribadi yang tidak menggunakan jatah cuti akan dikenakan potong gaji proporsional (Unpaid Leave)."
    },
    
    # ==================== KATEGORI: BENEFIT ====================
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apa syarat klaim kacamata?",
        "variasi": [
            "klaim kacamata gimana", "reimburse kacamata", "benefit kacamata",
            "ganti kacamata kantor", "tunjangan kacamata", "claim glasses",
            "kacamata ditanggung kantor", "plafon kacamata berapa", "fasilitas kacamata",
            "beli kacamata dibayar kantor",
        ],
        "jawaban": "Anda bisa klaim kacamata 1x dalam 2 tahun dengan plafon Rp1.500.000. Lampirkan resep dokter dan kuitansi asli."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apakah ada tunjangan makan?",
        "variasi": [
            "uang makan", "tunjangan lunch", "meal allowance", "makan ditanggung kantor",
            "fasilitas makan", "uang makan karyawan", "tunjangan konsumsi",
            "allowance makan", "benefit makan", "subsidi makan",
        ],
        "jawaban": "Tunjangan makan diberikan dalam bentuk uang tunai yang sudah termasuk di dalam komponen gaji bulanan."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apa itu asuransi tambahan kantor?",
        "variasi": [
            "asuransi kantor apa", "asuransi kesehatan karyawan", "health insurance kantor",
            "asuransi selain bpjs", "asuransi swasta perusahaan", "coverage asuransi",
            "fasilitas asuransi", "benefit asuransi", "asuransi rawat inap", "asuransi rawat jalan",
        ],
        "jawaban": "Selain BPJS, kantor menyediakan asuransi swasta (Manulife/Prudential) untuk rawat inap dan rawat jalan."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apa itu tunjangan hari raya (THR)?",
        "variasi": [
            "THR kapan", "tunjangan lebaran", "bonus lebaran", "THR berapa", "uang THR",
            "tunjangan hari raya berapa", "THR diberikan kapan", "dapat THR kapan",
            "THR 1 bulan gaji", "syarat dapat THR",
        ],
        "jawaban": "THR diberikan sebesar 1 bulan gaji bagi yang sudah bekerja >1 tahun, diberikan maksimal H-7 Lebaran."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apakah ada bonus tahunan?",
        "variasi": [
            "bonus akhir tahun", "annual bonus", "bonus kinerja", "bonus performance",
            "dapat bonus kapan", "bonus tahunan berapa", "bonus perusahaan",
            "insentif tahunan", "year end bonus", "bonus berdasarkan KPI",
        ],
        "jawaban": "Bonus tahunan diberikan berdasarkan performa perusahaan dan nilai KPI individu di akhir tahun fiskal."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apakah ada bantuan duka cita?",
        "variasi": [
            "uang duka", "santunan kematian", "bantuan meninggal", "duka cita keluarga",
            "uang turut berduka", "kompensasi duka", "benefit kematian",
            "santunan duka", "bantuan keluarga meninggal", "tunjangan duka",
        ],
        "jawaban": "Ya, perusahaan memberikan uang duka untuk anggota keluarga inti yang meninggal dunia sesuai ketentuan PP."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apakah ada dana pinjaman karyawan?",
        "variasi": [
            "pinjaman karyawan", "kasbon", "pinjaman darurat", "loan karyawan",
            "minjem uang ke kantor", "fasilitas pinjaman", "koperasi karyawan",
            "pinjaman lunak", "emergency loan", "hutang ke perusahaan",
        ],
        "jawaban": "Perusahaan bekerja sama dengan koperasi karyawan untuk fasilitas pinjaman darurat."
    },
    
    # ==================== KATEGORI: LEMBUR ====================
    {
        "kategori": "lembur",
        "pertanyaan_utama": "Bagaimana cara lapor lembur?",
        "variasi": [
            "klaim lembur", "input lembur dimana", "overtime claim", "laporan lembur",
            "ajukan lembur", "cara dapat uang lembur", "lembur harus lapor kemana",
            "form lembur", "approval lembur", "prosedur lembur",
        ],
        "jawaban": "Lembur harus disetujui atasan di portal HRIS paling lambat H+1 setelah pengerjaan lembur selesai."
    },
    
    # ==================== KATEGORI: ADMINISTRASI ====================
    {
        "kategori": "administrasi",
        "pertanyaan_utama": "Bagaimana cara ganti password portal HR?",
        "variasi": [
            "lupa password HRIS", "reset password portal", "ganti password HR",
            "forgot password HRIS", "password HRIS lupa", "cara reset password",
            "ubah password portal", "login HRIS gagal", "tidak bisa masuk HRIS",
            "password portal expired",
        ],
        "jawaban": "Klik 'Forgot Password' pada halaman login portal HRIS atau hubungi tim IT Helpdesk."
    },
    {
        "kategori": "administrasi",
        "pertanyaan_utama": "Bagaimana cara daftar BPJS Kesehatan?",
        "variasi": [
            "daftar bpjs", "registrasi bpjs kesehatan", "bpjs keluarga",
            "tambah anggota bpjs", "cara ikut bpjs", "pendaftaran bpjs",
            "bpjs untuk keluarga", "dokumen bpjs", "syarat daftar bpjs", "bpjs kesehatan kantor",
        ],
        "jawaban": "Serahkan fotokopi KK dan KTP anggota keluarga ke bagian HR Admin di lantai 2."
    },
    {
        "kategori": "administrasi",
        "pertanyaan_utama": "Bagaimana jika kartu akses hilang?",
        "variasi": [
            "id card hilang", "kartu karyawan hilang", "access card hilang",
            "kehilangan kartu akses", "ganti kartu akses", "buat kartu baru",
            "kartu kantor hilang", "badge hilang", "kartu security hilang", "lapor kartu hilang",
        ],
        "jawaban": "Segera lapor ke bagian Security/General Affair untuk penonaktifan kartu lama dan pembuatan kartu baru (biaya Rp50rb)."
    },
    {
        "kategori": "administrasi",
        "pertanyaan_utama": "Bagaimana cara pesan ruang rapat?",
        "variasi": [
            "booking meeting room", "reservasi ruang meeting", "pesan ruangan",
            "book ruang rapat", "jadwal ruang meeting", "pakai ruang rapat",
            "cara booking room", "meeting room availability", "ruangan untuk meeting", "schedule room",
        ],
        "jawaban": "Pemesanan ruang rapat dilakukan melalui kalender Microsoft Outlook atau Google Calendar kantor."
    },
    
    # ==================== KATEGORI: KARIR ====================
    {
        "kategori": "karir",
        "pertanyaan_utama": "Apa syarat promosi jabatan?",
        "variasi": [
            "cara naik jabatan", "syarat kenaikan pangkat", "promosi karyawan",
            "naik level gimana", "kriteria promosi", "kapan bisa dipromosikan",
            "promotion criteria", "kenaikan jabatan", "syarat naik grade", "career advancement",
        ],
        "jawaban": "Promosi didasarkan pada penilaian kinerja (KPI) minimal 'A' selama 2 periode berturut-turut dan ketersediaan posisi."
    },
    {
        "kategori": "karir",
        "pertanyaan_utama": "Bagaimana prosedur resign?",
        "variasi": [
            "cara resign", "mau keluar kerja", "prosedur pengunduran diri",
            "resign notice period", "one month notice", "surat resign",
            "berhenti kerja gimana", "keluar dari perusahaan", "undur diri", "resignation process",
        ],
        "jawaban": "Karyawan wajib menyerahkan surat pengunduran diri minimal 30 hari sebelum tanggal terakhir bekerja (One Month Notice)."
    },
    {
        "kategori": "karir",
        "pertanyaan_utama": "Apa itu sistem KPI?",
        "variasi": [
            "KPI itu apa", "key performance indicator", "penilaian kinerja",
            "performance review", "evaluasi karyawan", "KPI gimana caranya",
            "target KPI", "nilai KPI", "sistem penilaian kerja", "assessment karyawan",
        ],
        "jawaban": "KPI adalah indikator performa utama yang dinilai setiap semester untuk menentukan kenaikan gaji dan bonus."
    },
    {
        "kategori": "karir",
        "pertanyaan_utama": "Kapan evaluasi karyawan kontrak?",
        "variasi": [
            "kontrak diperpanjang kapan", "evaluasi PKWT", "kontrak habis gimana",
            "perpanjangan kontrak", "diangkat tetap kapan", "status kontrak",
            "review karyawan kontrak", "masa kontrak selesai", "kontrak mau habis", "kontrak ke tetap",
        ],
        "jawaban": "Evaluasi dilakukan 1 bulan sebelum masa kontrak berakhir untuk menentukan perpanjangan atau pengangkatan tetap."
    },
    {
        "kategori": "karir",
        "pertanyaan_utama": "Apakah perusahaan membiayai sertifikasi?",
        "variasi": [
            "biaya sertifikasi", "training sertifikasi", "sertifikat ditanggung",
            "certification program", "biaya ujian sertifikasi", "professional certification",
            "kantor bayar sertifikasi", "L&D sertifikasi", "program sertifikasi", "biaya exam ditanggung",
        ],
        "jawaban": "Ya, melalui program Learning & Development, perusahaan menanggung biaya sertifikasi yang relevan dengan job desc."
    },
    {
        "kategori": "karir",
        "pertanyaan_utama": "Bagaimana cara ikut training internal?",
        "variasi": [
            "daftar training", "ikut pelatihan", "training karyawan", "jadwal training",
            "internal training", "program pelatihan", "learning program",
            "cara join training", "training gratis kantor", "workshop internal",
        ],
        "jawaban": "Daftar melalui kalender pelatihan di portal HR Learning atau hubungi atasan Anda."
    },
    
    # ==================== KATEGORI: FASILITAS ====================
    {
        "kategori": "fasilitas",
        "pertanyaan_utama": "Apakah ada jemputan karyawan?",
        "variasi": [
            "shuttle bus kantor", "antar jemput karyawan", "bus karyawan",
            "transportasi kantor", "jemputan dari mana", "shuttle kantor",
            "fasilitas antar jemput", "bus jemputan", "kendaraan kantor", "commute ke kantor",
        ],
        "jawaban": "Saat ini perusahaan menyediakan shuttle bus di 3 titik: Bekasi, Depok, dan Tangerang menuju kantor pusat."
    },
    {
        "kategori": "fasilitas",
        "pertanyaan_utama": "Di mana lokasi ruang laktasi?",
        "variasi": [
            "ruang menyusui", "nursing room", "tempat pompa asi", "lactation room",
            "ruang asi", "fasilitas laktasi", "tempat ibu menyusui",
            "breastfeeding room", "pumping room", "ruangan untuk menyusui",
        ],
        "jawaban": "Ruang laktasi tersedia di lantai 3, tepat di sebelah klinik kesehatan kantor."
    },
    {
        "kategori": "fasilitas",
        "pertanyaan_utama": "Bagaimana cara pinjam laptop kantor?",
        "variasi": [
            "pinjam laptop", "request laptop", "butuh laptop", "laptop untuk kerja",
            "borrow laptop", "peminjaman laptop", "laptop kantor",
            "minta laptop", "loan laptop", "laptop sementara",
        ],
        "jawaban": "Silakan ajukan request peminjaman melalui aplikasi IT Asset Management."
    },
    {
        "kategori": "fasilitas",
        "pertanyaan_utama": "Apa syarat mendapatkan laptop baru?",
        "variasi": [
            "laptop baru kapan", "ganti laptop", "refresh laptop", "laptop replacement",
            "dapat laptop baru", "laptop rusak ganti", "upgrade laptop",
            "laptop sudah tua", "peremajaan laptop", "laptop baru karyawan",
        ],
        "jawaban": "Laptop baru diberikan setiap 4 tahun sekali sebagai bagian dari program peremajaan perangkat kerja."
    },
    
    # ==================== KATEGORI: KEBIJAKAN ====================
    {
        "kategori": "kebijakan",
        "pertanyaan_utama": "Apa aturan pakaian hari Jumat?",
        "variasi": [
            "dresscode jumat", "pakaian casual friday", "baju jumat", "friday dress code",
            "batik friday", "pakaian kerja jumat", "aturan baju jumat",
            "jumat pakai apa", "casual friday", "dress code friday",
        ],
        "jawaban": "Setiap hari Jumat, karyawan diwajibkan menggunakan pakaian Batik atau Smart Casual yang rapi."
    },
    {
        "kategori": "kebijakan",
        "pertanyaan_utama": "Jam berapa jam kerja dimulai?",
        "variasi": [
            "jam masuk kantor", "jam kerja", "working hours", "office hours",
            "jam operasional", "masuk jam berapa", "pulang jam berapa",
            "jadwal kerja", "jam kantor", "shift kerja",
        ],
        "jawaban": "Jam kerja operasional dimulai pukul 08.30 WIB hingga 17.30 WIB dengan waktu istirahat 1 jam."
    },
    {
        "kategori": "kebijakan",
        "pertanyaan_utama": "Apakah boleh kerja remote (WFH)?",
        "variasi": [
            "WFH policy", "kerja dari rumah", "work from home", "remote working",
            "hybrid working", "boleh WFH tidak", "aturan WFH",
            "WFA", "kerja remote", "WFH berapa hari",
        ],
        "jawaban": "Kebijakan WFH saat ini adalah Hybrid (3 hari di kantor, 2 hari di rumah) sesuai jadwal tim masing-masing."
    },
    {
        "kategori": "kebijakan",
        "pertanyaan_utama": "Apa sanksi jika sering telat?",
        "variasi": [
            "hukuman telat", "sanksi terlambat", "telat kena SP", "datang telat",
            "keterlambatan karyawan", "punishment telat", "telat berapa kali kena",
            "terlambat masuk", "late penalty", "konsekuensi telat",
        ],
        "jawaban": "Keterlambatan lebih dari 3x dalam sebulan tanpa alasan jelas akan dikenakan Surat Peringatan (SP) Lisan."
    },
    {
        "kategori": "kebijakan",
        "pertanyaan_utama": "Apa prosedur jika sakit?",
        "variasi": [
            "izin sakit", "sick leave", "sakit tidak masuk", "lapor sakit",
            "surat dokter", "sakit harus ngapain", "tidak masuk karena sakit",
            "prosedur sakit", "medical leave", "cuti sakit",
        ],
        "jawaban": "Informasikan atasan langsung dan serahkan surat keterangan dokter ke HR jika sakit lebih dari 1 hari."
    },
    
    # ==================== KATEGORI: REIMBURSEMENT ====================
    {
        "kategori": "reimbursement",
        "pertanyaan_utama": "Bagaimana cara klaim parkir?",
        "variasi": [
            "reimburse parkir", "klaim biaya parkir", "parkir diganti", "biaya parkir",
            "claim parking", "parkir meeting client", "parkir business trip",
            "ganti uang parkir", "reimbursement parkir", "parkir visit client",
        ],
        "jawaban": "Klaim parkir hanya berlaku untuk kunjungan klien (business trip) dengan melampirkan karcis asli di form reimbursement."
    },
    {
        "kategori": "reimbursement",
        "pertanyaan_utama": "Bagaimana cara klaim reimbursement medis?",
        "variasi": [
            "klaim medical", "reimburse obat", "klaim biaya dokter", "medical reimbursement",
            "ganti biaya berobat", "claim kesehatan", "reimburse rumah sakit",
            "klaim rawat jalan", "medical claim", "ganti biaya medis",
        ],
        "jawaban": "Unggah foto kuitansi asli dan resume medis ke modul 'Reimbursement' di portal HRIS."
    },
    
    # ==================== KATEGORI: KONTAK ====================
    {
        "kategori": "kontak",
        "pertanyaan_utama": "Siapa kontak darurat HR?",
        "variasi": [
            "nomor HR", "hotline HR", "telepon HR", "contact HR", "hubungi HR",
            "nomor darurat HR", "HR hotline", "emergency contact HR", "call HR", "WA HR",
        ],
        "jawaban": "Anda bisa menghubungi HR Hotline di nomor 0812-1234-5678 untuk keadaan darurat."
    },
    
    # ==================== KATEGORI: GREETING ====================
    {
        "kategori": "greeting",
        "pertanyaan_utama": "Halo, apa yang bisa kamu lakukan?",
        "variasi": [
            "halo", "hi", "hello", "hai", "hey", "selamat pagi", "selamat siang",
            "selamat sore", "kamu bisa apa", "fungsi kamu apa", "bot ini untuk apa",
            "apa ini", "kamu siapa", "perkenalkan diri",
        ],
        "jawaban": "Halo! 👋 Saya adalah asisten HR digital. Saya bisa menjawab pertanyaan seputar kebijakan kantor, cuti, gaji, benefit, dan administrasi HR lainnya. Silakan tanyakan apa saja!"
    },
    {
        "kategori": "greeting",
        "pertanyaan_utama": "Terima kasih bantuannya.",
        "variasi": [
            "terima kasih", "makasih", "thanks", "thank you", "thx", "tq",
            "trims", "terimakasih ya", "makasih banyak", "thanks a lot",
        ],
        "jawaban": "Sama-sama! 😊 Senang bisa membantu Anda. Ada lagi yang ingin ditanyakan?"
    },
    {
        "kategori": "greeting",
        "pertanyaan_utama": "Sampai jumpa",
        "variasi": [
            "bye", "goodbye", "dadah", "sampai nanti", "see you", "bye bye",
            "selamat tinggal", "sudah cukup", "tidak ada lagi", "cukup sekian",
        ],
        "jawaban": "Terima kasih sudah menggunakan layanan HR Chatbot! Sampai jumpa lagi. 👋"
    },
]


def get_flat_qa_pairs():
    """Menghasilkan list of tuples (pertanyaan, jawaban, kategori)"""
    pairs = []
    for item in HR_KNOWLEDGE_BASE:
        pairs.append((item["pertanyaan_utama"], item["jawaban"], item["kategori"]))
        for variasi in item["variasi"]:
            pairs.append((variasi, item["jawaban"], item["kategori"]))
    return pairs


def get_categories():
    return list(set(item["kategori"] for item in HR_KNOWLEDGE_BASE))


# ============================================================================
# FUZZY MATCHER ENGINE
# ============================================================================

class HRFuzzyMatcher:
    """Matcher berbasis FuzzyWuzzy dengan multiple strategies."""
    
    def __init__(self, qa_pairs: List[Tuple[str, str, str]], threshold: int = 65):
        self.qa_pairs = qa_pairs
        self.threshold = threshold
        self.questions = [self._preprocess(q) for q, _, _ in qa_pairs]
        self.answers = [a for _, a, _ in qa_pairs]
        self.categories = [c for _, _, c in qa_pairs]
        
    def _preprocess(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _calculate_scores(self, query: str, target: str) -> dict:
        return {
            'simple': fuzz.ratio(query, target),
            'partial': fuzz.partial_ratio(query, target),
            'token_sort': fuzz.token_sort_ratio(query, target),
            'token_set': fuzz.token_set_ratio(query, target),
        }
    
    def _weighted_score(self, scores: dict) -> float:
        weights = {'simple': 0.15, 'partial': 0.25, 'token_sort': 0.25, 'token_set': 0.35}
        return sum(scores[k] * weights[k] for k in weights)
    
    def find_best_match(self, query: str) -> Tuple[Optional[str], float, Optional[str]]:
        processed_query = self._preprocess(query)
        best_score, best_idx = 0, -1
        
        for idx, question in enumerate(self.questions):
            scores = self._calculate_scores(processed_query, question)
            weighted = self._weighted_score(scores)
            if weighted > best_score:
                best_score, best_idx = weighted, idx
        
        if best_score >= self.threshold and best_idx >= 0:
            return self.answers[best_idx], best_score, self.categories[best_idx]
        return None, best_score, None
    
    def find_top_matches(self, query: str, top_n: int = 3) -> List[Tuple[str, str, float, str]]:
        processed_query = self._preprocess(query)
        results = []
        
        for idx, question in enumerate(self.questions):
            scores = self._calculate_scores(processed_query, question)
            weighted = self._weighted_score(scores)
            results.append((self.qa_pairs[idx][0], self.answers[idx], weighted, self.categories[idx]))
        
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:top_n]
    
    def get_fallback_response(self) -> str:
        return (
            "Maaf, saya belum bisa memahami pertanyaan Anda. 🤔\n\n"
            "Silakan coba tanyakan dengan cara lain atau hubungi HR Hotline di **0812-1234-5678**.\n\n"
            "Anda juga bisa bertanya tentang: cuti, gaji, benefit, lembur, atau kebijakan kantor."
        )


class HRChatbotEngine:
    """Main chatbot engine."""
    
    def __init__(self, qa_pairs: List[Tuple[str, str, str]], threshold: int = 65):
        self.matcher = HRFuzzyMatcher(qa_pairs, threshold)
        
    def get_response(self, user_input: str) -> dict:
        answer, confidence, category = self.matcher.find_best_match(user_input)
        
        if answer:
            return {
                'answer': answer, 'confidence': confidence, 'category': category,
                'is_fallback': False, 'suggestions': []
            }
        else:
            top_matches = self.matcher.find_top_matches(user_input, top_n=3)
            suggestions = [{'question': q, 'score': s} for q, _, s, _ in top_matches if s >= 40]
            return {
                'answer': self.matcher.get_fallback_response(), 'confidence': confidence,
                'category': None, 'is_fallback': True, 'suggestions': suggestions[:3]
            }


# ============================================================================
# ANALYTICS MODULE
# ============================================================================

class HRAnalytics:
    """Analytics engine untuk HR Chatbot."""
    
    def __init__(self, data_file: str = "hr_analytics_data.json"):
        self.data_file = data_file
        self.lock = threading.Lock()
        self._load_data()
    
    def _load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.queries = data.get('queries', [])
                    self.feedback = data.get('feedback', [])
                    self.sessions = data.get('sessions', {})
            except:
                self._init_empty_data()
        else:
            self._init_empty_data()
    
    def _init_empty_data(self):
        self.queries, self.feedback, self.sessions = [], [], {}
    
    def _save_data(self):
        with self.lock:
            try:
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'queries': self.queries[-10000:],
                        'feedback': self.feedback[-5000:],
                        'sessions': dict(list(self.sessions.items())[-1000:])
                    }, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Error saving: {e}")
    
    def log_query(self, session_id: str, user_input: str, response: dict):
        self.queries.append({
            'timestamp': datetime.now().isoformat(), 'session_id': session_id,
            'user_input': user_input, 'category': response.get('category'),
            'confidence': response.get('confidence', 0), 'is_fallback': response.get('is_fallback', False),
        })
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'start_time': datetime.now().isoformat(), 'query_count': 0,
                'last_activity': datetime.now().isoformat(), 'rated': False
            }
        self.sessions[session_id]['query_count'] += 1
        self.sessions[session_id]['last_activity'] = datetime.now().isoformat()
        self._save_data()
    
    def log_feedback(self, session_id: str, rating: int, comment: Optional[str] = None):
        self.feedback.append({
            'timestamp': datetime.now().isoformat(), 'session_id': session_id,
            'rating': rating, 'comment': comment
        })
        if session_id in self.sessions:
            self.sessions[session_id]['rated'] = True
            self.sessions[session_id]['rating'] = rating
        self._save_data()
    
    def get_top_queries(self, n: int = 10, days: int = 30) -> List[Dict]:
        cutoff = datetime.now() - timedelta(days=days)
        recent = [q['user_input'].lower() for q in self.queries if datetime.fromisoformat(q['timestamp']) > cutoff]
        return [{'query': q, 'count': c} for q, c in Counter(recent).most_common(n)]
    
    def get_category_distribution(self, days: int = 30) -> Dict[str, int]:
        cutoff = datetime.now() - timedelta(days=days)
        cats = [q['category'] or 'unknown' for q in self.queries if datetime.fromisoformat(q['timestamp']) > cutoff]
        return dict(Counter(cats))
    
    def get_daily_trends(self, days: int = 7) -> List[Dict]:
        trends = defaultdict(lambda: {'total': 0, 'categories': defaultdict(int)})
        cutoff = datetime.now() - timedelta(days=days)
        for q in self.queries:
            ts = datetime.fromisoformat(q['timestamp'])
            if ts > cutoff:
                date_key = ts.strftime('%Y-%m-%d')
                trends[date_key]['total'] += 1
                trends[date_key]['categories'][q['category'] or 'unknown'] += 1
        
        result = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=days-1-i)).strftime('%Y-%m-%d')
            result.append({
                'date': date, 'total': trends[date]['total'] if date in trends else 0,
                'categories': dict(trends[date]['categories']) if date in trends else {}
            })
        return result
    
    def get_hourly_distribution(self, days: int = 7) -> Dict[int, int]:
        cutoff = datetime.now() - timedelta(days=days)
        hours = [datetime.fromisoformat(q['timestamp']).hour for q in self.queries if datetime.fromisoformat(q['timestamp']) > cutoff]
        return dict(Counter(hours))
    
    def get_feedback_stats(self, days: int = 30) -> Dict[str, Any]:
        cutoff = datetime.now() - timedelta(days=days)
        recent = [f for f in self.feedback if datetime.fromisoformat(f['timestamp']) > cutoff]
        if not recent:
            return {'average_rating': 0, 'total_feedback': 0, 'rating_distribution': {}, 'recent_comments': []}
        ratings = [f['rating'] for f in recent]
        return {
            'average_rating': sum(ratings) / len(ratings), 'total_feedback': len(recent),
            'rating_distribution': dict(Counter(ratings)),
            'recent_comments': [f['comment'] for f in recent[-10:] if f.get('comment')]
        }
    
    def get_fallback_rate(self, days: int = 7) -> float:
        cutoff = datetime.now() - timedelta(days=days)
        recent = [q for q in self.queries if datetime.fromisoformat(q['timestamp']) > cutoff]
        if not recent: return 0.0
        return (sum(1 for q in recent if q.get('is_fallback', False)) / len(recent)) * 100
    
    def get_confidence_stats(self, days: int = 7) -> Dict[str, float]:
        cutoff = datetime.now() - timedelta(days=days)
        confs = [q['confidence'] for q in self.queries if datetime.fromisoformat(q['timestamp']) > cutoff and q.get('confidence')]
        if not confs: return {'average': 0, 'min': 0, 'max': 0}
        return {'average': sum(confs)/len(confs), 'min': min(confs), 'max': max(confs)}
    
    def get_summary_stats(self, days: int = 7) -> Dict[str, Any]:
        cutoff = datetime.now() - timedelta(days=days)
        recent_q = [q for q in self.queries if datetime.fromisoformat(q['timestamp']) > cutoff]
        recent_s = {k: v for k, v in self.sessions.items() if datetime.fromisoformat(v['start_time']) > cutoff}
        return {
            'total_queries': len(recent_q), 'total_sessions': len(recent_s),
            'fallback_rate': self.get_fallback_rate(days),
            'avg_confidence': self.get_confidence_stats(days)['average'],
            'feedback_stats': self.get_feedback_stats(days), 'top_categories': self.get_category_distribution(days)
        }


# ============================================================================
# STREAMLIT APPLICATION
# ============================================================================

st.set_page_config(page_title="HR Chatbot Internal", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .chat-message { padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; }
    .chat-message.user { background-color: #e3f2fd; border-left: 4px solid #2196F3; }
    .chat-message.bot { background-color: #f5f5f5; border-left: 4px solid #4CAF50; }
    .rating-section { background-color: #fff8e1; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if 'session_id' not in st.session_state: st.session_state.session_id = str(uuid.uuid4())
    if 'messages' not in st.session_state: st.session_state.messages = []
    if 'chatbot_engine' not in st.session_state:
        st.session_state.chatbot_engine = HRChatbotEngine(get_flat_qa_pairs(), threshold=65)
    if 'analytics' not in st.session_state: st.session_state.analytics = HRAnalytics()
    if 'last_activity' not in st.session_state: st.session_state.last_activity = datetime.now()
    if 'session_ended' not in st.session_state: st.session_state.session_ended = False
    if 'rating_submitted' not in st.session_state: st.session_state.rating_submitted = False
    if 'show_rating_prompt' not in st.session_state: st.session_state.show_rating_prompt = False

init_session_state()

st.sidebar.title("🏢 HR Chatbot")
page = st.sidebar.radio("Menu", ["💬 Chat", "📊 Dashboard Analytics", "📚 FAQ Lengkap", "ℹ️ Tentang"])


def check_inactivity():
    if st.session_state.messages and not st.session_state.session_ended:
        if datetime.now() - st.session_state.last_activity > timedelta(minutes=3):
            st.session_state.show_rating_prompt = True


def process_user_input(user_input: str):
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = st.session_state.chatbot_engine.get_response(user_input)
    st.session_state.analytics.log_query(st.session_state.session_id, user_input, response)
    st.session_state.messages.append({
        "role": "assistant", "content": response['answer'],
        "confidence": response['confidence'], "category": response['category'],
        "suggestions": response.get('suggestions', [])
    })
    st.session_state.last_activity = datetime.now()
    st.session_state.show_rating_prompt = False


# ===================== PAGE: CHAT =====================
def render_chat_page():
    st.title("💬 HR Assistant Chatbot")
    st.markdown("---")
    check_inactivity()
    
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user"><strong>👤 Anda:</strong><p>{msg["content"]}</p></div>', unsafe_allow_html=True)
        else:
            conf = msg.get("confidence", 0)
            cat = msg.get("category", "")
            conf_color = "#4CAF50" if conf >= 75 else "#FF9800" if conf >= 50 else "#f44336"
            badge = f'<span style="font-size:0.75rem;padding:0.2rem 0.5rem;border-radius:0.25rem;background:{conf_color}20;color:{conf_color};">Confidence: {conf:.0f}%</span>'
            if cat: badge += f'<span style="font-size:0.75rem;padding:0.2rem 0.5rem;border-radius:0.25rem;background:#fff3e0;color:#e65100;margin-left:0.5rem;">{cat.upper()}</span>'
            st.markdown(f'<div class="chat-message bot"><strong>🤖 HR Bot:</strong><p>{msg["content"]}</p><div style="margin-top:0.5rem;">{badge}</div></div>', unsafe_allow_html=True)
            
            if msg.get("suggestions"):
                with st.expander("💡 Mungkin yang Anda maksud:"):
                    for sug in msg["suggestions"]:
                        if st.button(f"❓ {sug['question']}", key=f"sug_{i}_{hash(sug['question'])}"):
                            process_user_input(sug['question'])
                            st.rerun()
    
    # Rating prompt
    if st.session_state.show_rating_prompt and not st.session_state.rating_submitted:
        st.markdown("---")
        st.markdown('<div class="rating-section"><h4>⏰ Sepertinya percakapan sudah selesai...</h4><p>Apakah Anda sudah selesai? Mohon berikan rating.</p></div>', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1: rating = st.slider("Rating:", 1, 5, 4, key="inact_rating")
        with col2:
            if st.button("🔄 Lanjut Chat", key="cont"):
                st.session_state.show_rating_prompt = False
                st.session_state.last_activity = datetime.now()
                st.rerun()
        comment = st.text_area("Komentar (opsional):", key="inact_comment", height=80)
        if st.button("✅ Kirim Rating & Selesai", key="submit_inact"):
            st.session_state.analytics.log_feedback(st.session_state.session_id, rating, comment or None)
            st.session_state.rating_submitted = True
            st.session_state.session_ended = True
            st.success("Terima kasih atas feedback Anda! 🙏")
            st.rerun()
    
    # Chat input
    st.markdown("---")
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Ketik pertanyaan:", key="user_input", placeholder="Contoh: Berapa jatah cuti tahunan?", disabled=st.session_state.session_ended)
    with col2:
        send = st.button("Kirim 📤", disabled=st.session_state.session_ended)
    
    if (send or user_input) and user_input.strip():
        process_user_input(user_input.strip())
        st.rerun()
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.session_ended:
            if st.button("🏁 Selesai & Beri Rating", use_container_width=True):
                st.session_state.show_rating_prompt = True
                st.rerun()
        else:
            if st.button("🔄 Mulai Percakapan Baru", use_container_width=True):
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.messages = []
                st.session_state.last_activity = datetime.now()
                st.session_state.session_ended = False
                st.session_state.rating_submitted = False
                st.session_state.show_rating_prompt = False
                st.rerun()
    
    # Quick buttons
    st.markdown("---")
    st.markdown("**🚀 Pertanyaan Populer:**")
    quick_qs = ["Berapa jatah cuti tahunan?", "Kapan gaji cair?", "Cara ajukan cuti?", "Aturan WFH?", "THR kapan?"]
    cols = st.columns(len(quick_qs))
    for i, q in enumerate(quick_qs):
        with cols[i]:
            if st.button(q, key=f"quick_{i}", disabled=st.session_state.session_ended):
                process_user_input(q)
                st.rerun()


# ===================== PAGE: DASHBOARD =====================
def render_dashboard_page():
    st.title("📊 HR Analytics Dashboard")
    st.markdown("---")
    
    analytics = st.session_state.analytics
    days = st.selectbox("Periode:", [7, 14, 30], format_func=lambda x: f"{x} hari terakhir")
    summary = analytics.get_summary_stats(days)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Pertanyaan", summary['total_queries'])
    col2.metric("Total Sesi", summary['total_sessions'])
    col3.metric("Fallback Rate", f"{summary['fallback_rate']:.1f}%")
    avg_r = summary['feedback_stats'].get('average_rating', 0)
    col4.metric("Rating Rata-rata", f"⭐ {avg_r:.1f}/5" if avg_r > 0 else "N/A")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Tren Pertanyaan Harian")
        import pandas as pd
        daily = analytics.get_daily_trends(days)
        if daily:
            df = pd.DataFrame(daily)
            st.line_chart(df.set_index('date')['total'])
        else:
            st.info("Belum ada data")
    
    with col2:
        st.subheader("📊 Distribusi Kategori")
        cats = analytics.get_category_distribution(days)
        if cats:
            import pandas as pd
            df = pd.DataFrame(list(cats.items()), columns=['Kategori', 'Jumlah']).sort_values('Jumlah', ascending=False)
            st.bar_chart(df.set_index('Kategori'))
        else:
            st.info("Belum ada data")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔝 Top 10 Pertanyaan")
        top_q = analytics.get_top_queries(10, days)
        if top_q:
            for i, item in enumerate(top_q, 1):
                st.markdown(f"**{i}.** {item['query']} ({item['count']}x)")
        else:
            st.info("Belum ada data")
    
    with col2:
        st.subheader("⏰ Distribusi Jam Aktif")
        hourly = analytics.get_hourly_distribution(days)
        if hourly:
            import pandas as pd
            full_h = {h: hourly.get(h, 0) for h in range(24)}
            df = pd.DataFrame(list(full_h.items()), columns=['Jam', 'Jumlah']).sort_values('Jam')
            st.bar_chart(df.set_index('Jam'))
        else:
            st.info("Belum ada data")
    
    st.markdown("---")
    st.subheader("💬 Feedback & Rating")
    fb = analytics.get_feedback_stats(days)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Feedback", fb['total_feedback'])
    
    with col2:
        rd = fb.get('rating_distribution', {})
        if rd:
            st.markdown("**Distribusi Rating:**")
            for r in range(5, 0, -1):
                c = rd.get(r, 0)
                st.progress(c / max(rd.values()) if rd.values() else 0)
                st.caption(f"{'⭐'*r}: {c}")
    
    with col3:
        comments = fb.get('recent_comments', [])
        if comments:
            st.markdown("**Komentar Terbaru:**")
            for c in comments[-5:]: st.markdown(f"- _{c}_")
        else:
            st.info("Belum ada komentar")


# ===================== PAGE: FAQ =====================
def render_faq_page():
    st.title("📚 FAQ Lengkap HR")
    st.markdown("---")
    
    sel_cat = st.selectbox("Filter Kategori:", ["Semua"] + sorted(get_categories()))
    search = st.text_input("🔍 Cari pertanyaan:", "")
    st.markdown("---")
    
    for item in HR_KNOWLEDGE_BASE:
        if sel_cat != "Semua" and item['kategori'] != sel_cat: continue
        if search and search.lower() not in item['pertanyaan_utama'].lower() and search.lower() not in item['jawaban'].lower(): continue
        
        with st.expander(f"❓ {item['pertanyaan_utama']}"):
            st.markdown(f"**Jawaban:**\n\n{item['jawaban']}")
            st.markdown(f"**Kategori:** `{item['kategori'].upper()}`")
            if item['variasi']:
                st.markdown("**Variasi pertanyaan yang dipahami:**")
                st.caption(", ".join(item['variasi'][:5]) + ("..." if len(item['variasi']) > 5 else ""))


# ===================== PAGE: ABOUT =====================
def render_about_page():
    st.title("ℹ️ Tentang HR Chatbot")
    st.markdown("""
    ### 🤖 HR Internal Chatbot
    
    Chatbot untuk membantu karyawan mendapatkan informasi HR dengan cepat.
    
    #### ✨ Fitur:
    - **Chat Interaktif** - FuzzyWuzzy matching dengan akurasi tinggi
    - **Session Management** - Deteksi inaktivitas 3 menit
    - **Rating System** - Feedback 1-5 bintang
    - **Analytics Dashboard** - Top queries, kategori, tren
    
    #### 📂 Kategori:
    - 🏖️ Cuti | 💰 Gaji | 🎁 Benefit | ⏰ Lembur
    - 📋 Administrasi | 📈 Karir | 🏢 Fasilitas
    - 📜 Kebijakan | 💳 Reimbursement | 📞 Kontak
    
    #### 📧 Kontak:
    HR Hotline: **0812-1234-5678**
    """)


# ===================== MAIN =====================
if page == "💬 Chat": render_chat_page()
elif page == "📊 Dashboard Analytics": render_dashboard_page()
elif page == "📚 FAQ Lengkap": render_faq_page()
elif page == "ℹ️ Tentang": render_about_page()

st.sidebar.markdown("---")
st.sidebar.markdown('<div style="text-align:center;color:#666;font-size:0.8rem;">HR Chatbot v1.0<br>© 2026 Internal Use</div>', unsafe_allow_html=True)
