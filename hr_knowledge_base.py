# HR Knowledge Base dengan variasi pertanyaan untuk training FuzzyWuzzy
# Setiap entry memiliki: kategori, pertanyaan utama, variasi pertanyaan, dan jawaban

HR_KNOWLEDGE_BASE = [
    # ==================== KATEGORI: CUTI ====================
    {
        "kategori": "cuti",
        "pertanyaan_utama": "Berapa jatah cuti tahunan saya?",
        "variasi": [
            "berapa cuti tahunan",
            "jatah cuti setahun",
            "total cuti pertahun",
            "cuti tahunan berapa hari",
            "berapa hari cuti dalam setahun",
            "hak cuti karyawan",
            "jumlah cuti tahunan",
            "saya dapat cuti berapa hari",
            "cuti annual berapa",
            "annual leave berapa hari",
        ],
        "jawaban": "Karyawan berhak mendapatkan 12 hari cuti tahunan setelah bekerja selama 12 bulan berturut-turut."
    },
    {
        "kategori": "cuti",
        "pertanyaan_utama": "Bagaimana cara mengajukan cuti?",
        "variasi": [
            "cara ajukan cuti",
            "prosedur pengajuan cuti",
            "mau ambil cuti gimana",
            "apply cuti dimana",
            "submit cuti bagaimana",
            "cara request cuti",
            "pengajuan cuti lewat mana",
            "mau cuti harus ngapain",
            "langkah ambil cuti",
            "cara minta cuti",
        ],
        "jawaban": "Pengajuan cuti dilakukan melalui portal HRIS maksimal 3 hari sebelum tanggal pengambilan cuti."
    },
    {
        "kategori": "cuti",
        "pertanyaan_utama": "Berapa lama cuti melahirkan?",
        "variasi": [
            "cuti melahirkan berapa bulan",
            "maternity leave berapa lama",
            "cuti hamil berapa hari",
            "hak cuti lahiran",
            "cuti persalinan",
            "cuti ibu melahirkan",
            "lama cuti hamil",
            "durasi cuti melahirkan",
            "jatah cuti lahiran",
            "berapa hari cuti melahirkan",
        ],
        "jawaban": "Cuti melahirkan diberikan selama 3 bulan (90 hari kalender) dengan gaji penuh."
    },
    {
        "kategori": "cuti",
        "pertanyaan_utama": "Apakah sisa cuti bisa diuangkan?",
        "variasi": [
            "cuti bisa dicairkan tidak",
            "sisa cuti jadi uang",
            "tukar cuti dengan uang",
            "cuti hangus atau diuangkan",
            "kompensasi sisa cuti",
            "cuti tidak terpakai gimana",
            "cuti bisa dituker duit",
            "cuti yang tidak diambil",
            "cairkan sisa cuti",
            "konversi cuti ke uang",
        ],
        "jawaban": "Sesuai kebijakan perusahaan, sisa cuti tahunan tidak dapat diuangkan dan akan hangus di akhir tahun jika tidak digunakan."
    },
    {
        "kategori": "cuti",
        "pertanyaan_utama": "Berapa jatah cuti menikah?",
        "variasi": [
            "cuti nikah berapa hari",
            "hak cuti pernikahan",
            "cuti kawin",
            "jatah cuti wedding",
            "cuti untuk menikah",
            "berapa lama cuti nikah",
            "cuti khusus menikah",
            "marriage leave",
            "izin nikah berapa hari",
            "cuti hari pernikahan",
        ],
        "jawaban": "Karyawan diberikan cuti khusus menikah selama 3 hari kerja."
    },
    
    # ==================== KATEGORI: GAJI ====================
    {
        "kategori": "gaji",
        "pertanyaan_utama": "Kapan gaji bulanan cair?",
        "variasi": [
            "tanggal gajian",
            "gaji turun kapan",
            "payroll kapan",
            "salary kapan masuk",
            "gaji dibayar tanggal berapa",
            "jadwal gajian",
            "kapan terima gaji",
            "gaji masuk tanggal",
            "pembayaran gaji kapan",
            "payday kapan",
        ],
        "jawaban": "Gaji dibayarkan setiap tanggal 25. Jika tanggal 25 jatuh pada hari libur, maka akan dibayarkan pada hari kerja sebelumnya."
    },
    {
        "kategori": "gaji",
        "pertanyaan_utama": "Di mana saya bisa ambil slip gaji?",
        "variasi": [
            "download slip gaji",
            "lihat slip gaji dimana",
            "payslip dimana",
            "cara dapat slip gaji",
            "akses slip gaji",
            "cetak slip gaji",
            "slip gaji online",
            "bukti gaji dimana",
            "struk gaji",
            "print payslip",
        ],
        "jawaban": "Slip gaji dapat diunduh dalam format PDF melalui portal HRIS menu 'My Payroll'."
    },
    {
        "kategori": "gaji",
        "pertanyaan_utama": "Apakah ada potongan gaji jika izin?",
        "variasi": [
            "izin dipotong gaji",
            "gaji dipotong kalau izin",
            "unpaid leave potong gaji",
            "izin tanpa cuti kena potong",
            "kalau izin gaji berkurang",
            "potongan untuk izin pribadi",
            "izin tidak pakai cuti",
            "gaji dikurangi kalau absen",
            "absen dipotong gaji tidak",
            "potong gaji karena izin",
        ],
        "jawaban": "Izin pribadi yang tidak menggunakan jatah cuti akan dikenakan potong gaji proporsional (Unpaid Leave)."
    },
    
    # ==================== KATEGORI: BENEFIT ====================
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apa syarat klaim kacamata?",
        "variasi": [
            "klaim kacamata gimana",
            "reimburse kacamata",
            "benefit kacamata",
            "ganti kacamata kantor",
            "tunjangan kacamata",
            "claim glasses",
            "kacamata ditanggung kantor",
            "plafon kacamata berapa",
            "fasilitas kacamata",
            "beli kacamata dibayar kantor",
        ],
        "jawaban": "Anda bisa klaim kacamata 1x dalam 2 tahun dengan plafon Rp1.500.000. Lampirkan resep dokter dan kuitansi asli."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apakah ada tunjangan makan?",
        "variasi": [
            "uang makan",
            "tunjangan lunch",
            "meal allowance",
            "makan ditanggung kantor",
            "fasilitas makan",
            "uang makan karyawan",
            "tunjangan konsumsi",
            "allowance makan",
            "benefit makan",
            "subsidi makan",
        ],
        "jawaban": "Tunjangan makan diberikan dalam bentuk uang tunai yang sudah termasuk di dalam komponen gaji bulanan."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apa itu asuransi tambahan kantor?",
        "variasi": [
            "asuransi kantor apa",
            "asuransi kesehatan karyawan",
            "health insurance kantor",
            "asuransi selain bpjs",
            "asuransi swasta perusahaan",
            "coverage asuransi",
            "fasilitas asuransi",
            "benefit asuransi",
            "asuransi rawat inap",
            "asuransi rawat jalan",
        ],
        "jawaban": "Selain BPJS, kantor menyediakan asuransi swasta (Manulife/Prudential) untuk rawat inap dan rawat jalan."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apa itu tunjangan hari raya (THR)?",
        "variasi": [
            "THR kapan",
            "tunjangan lebaran",
            "bonus lebaran",
            "THR berapa",
            "uang THR",
            "tunjangan hari raya berapa",
            "THR diberikan kapan",
            "dapat THR kapan",
            "THR 1 bulan gaji",
            "syarat dapat THR",
        ],
        "jawaban": "THR diberikan sebesar 1 bulan gaji bagi yang sudah bekerja >1 tahun, diberikan maksimal H-7 Lebaran."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apakah ada bonus tahunan?",
        "variasi": [
            "bonus akhir tahun",
            "annual bonus",
            "bonus kinerja",
            "bonus performance",
            "dapat bonus kapan",
            "bonus tahunan berapa",
            "bonus perusahaan",
            "insentif tahunan",
            "year end bonus",
            "bonus berdasarkan KPI",
        ],
        "jawaban": "Bonus tahunan diberikan berdasarkan performa perusahaan dan nilai KPI individu di akhir tahun fiskal."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apakah ada bantuan duka cita?",
        "variasi": [
            "uang duka",
            "santunan kematian",
            "bantuan meninggal",
            "duka cita keluarga",
            "uang turut berduka",
            "kompensasi duka",
            "benefit kematian",
            "santunan duka",
            "bantuan keluarga meninggal",
            "tunjangan duka",
        ],
        "jawaban": "Ya, perusahaan memberikan uang duka untuk anggota keluarga inti yang meninggal dunia sesuai ketentuan PP."
    },
    {
        "kategori": "benefit",
        "pertanyaan_utama": "Apakah ada dana pinjaman karyawan?",
        "variasi": [
            "pinjaman karyawan",
            "kasbon",
            "pinjaman darurat",
            "loan karyawan",
            "minjem uang ke kantor",
            "fasilitas pinjaman",
            "koperasi karyawan",
            "pinjaman lunak",
            "emergency loan",
            "hutang ke perusahaan",
        ],
        "jawaban": "Perusahaan bekerja sama dengan koperasi karyawan untuk fasilitas pinjaman darurat."
    },
    
    # ==================== KATEGORI: LEMBUR ====================
    {
        "kategori": "lembur",
        "pertanyaan_utama": "Bagaimana cara lapor lembur?",
        "variasi": [
            "klaim lembur",
            "input lembur dimana",
            "overtime claim",
            "laporan lembur",
            "ajukan lembur",
            "cara dapat uang lembur",
            "lembur harus lapor kemana",
            "form lembur",
            "approval lembur",
            "prosedur lembur",
        ],
        "jawaban": "Lembur harus disetujui atasan di portal HRIS paling lambat H+1 setelah pengerjaan lembur selesai."
    },
    
    # ==================== KATEGORI: ADMINISTRASI ====================
    {
        "kategori": "administrasi",
        "pertanyaan_utama": "Bagaimana cara ganti password portal HR?",
        "variasi": [
            "lupa password HRIS",
            "reset password portal",
            "ganti password HR",
            "forgot password HRIS",
            "password HRIS lupa",
            "cara reset password",
            "ubah password portal",
            "login HRIS gagal",
            "tidak bisa masuk HRIS",
            "password portal expired",
        ],
        "jawaban": "Klik 'Forgot Password' pada halaman login portal HRIS atau hubungi tim IT Helpdesk."
    },
    {
        "kategori": "administrasi",
        "pertanyaan_utama": "Bagaimana cara daftar BPJS Kesehatan?",
        "variasi": [
            "daftar bpjs",
            "registrasi bpjs kesehatan",
            "bpjs keluarga",
            "tambah anggota bpjs",
            "cara ikut bpjs",
            "pendaftaran bpjs",
            "bpjs untuk keluarga",
            "dokumen bpjs",
            "syarat daftar bpjs",
            "bpjs kesehatan kantor",
        ],
        "jawaban": "Serahkan fotokopi KK dan KTP anggota keluarga ke bagian HR Admin di lantai 2."
    },
    {
        "kategori": "administrasi",
        "pertanyaan_utama": "Bagaimana jika kartu akses hilang?",
        "variasi": [
            "id card hilang",
            "kartu karyawan hilang",
            "access card hilang",
            "kehilangan kartu akses",
            "ganti kartu akses",
            "buat kartu baru",
            "kartu kantor hilang",
            "badge hilang",
            "kartu security hilang",
            "lapor kartu hilang",
        ],
        "jawaban": "Segera lapor ke bagian Security/General Affair untuk penonaktifan kartu lama dan pembuatan kartu baru (biaya Rp50rb)."
    },
    {
        "kategori": "administrasi",
        "pertanyaan_utama": "Bagaimana cara pesan ruang rapat?",
        "variasi": [
            "booking meeting room",
            "reservasi ruang meeting",
            "pesan ruangan",
            "book ruang rapat",
            "jadwal ruang meeting",
            "pakai ruang rapat",
            "cara booking room",
            "meeting room availability",
            "ruangan untuk meeting",
            "schedule room",
        ],
        "jawaban": "Pemesanan ruang rapat dilakukan melalui kalender Microsoft Outlook atau Google Calendar kantor."
    },
    
    # ==================== KATEGORI: KARIR ====================
    {
        "kategori": "karir",
        "pertanyaan_utama": "Apa syarat promosi jabatan?",
        "variasi": [
            "cara naik jabatan",
            "syarat kenaikan pangkat",
            "promosi karyawan",
            "naik level gimana",
            "kriteria promosi",
            "kapan bisa dipromosikan",
            "promotion criteria",
            "kenaikan jabatan",
            "syarat naik grade",
            "career advancement",
        ],
        "jawaban": "Promosi didasarkan pada penilaian kinerja (KPI) minimal 'A' selama 2 periode berturut-turut dan ketersediaan posisi."
    },
    {
        "kategori": "karir",
        "pertanyaan_utama": "Bagaimana prosedur resign?",
        "variasi": [
            "cara resign",
            "mau keluar kerja",
            "prosedur pengunduran diri",
            "resign notice period",
            "one month notice",
            "surat resign",
            "berhenti kerja gimana",
            "keluar dari perusahaan",
            "undur diri",
            "resignation process",
        ],
        "jawaban": "Karyawan wajib menyerahkan surat pengunduran diri minimal 30 hari sebelum tanggal terakhir bekerja (One Month Notice)."
    },
    {
        "kategori": "karir",
        "pertanyaan_utama": "Apa itu sistem KPI?",
        "variasi": [
            "KPI itu apa",
            "key performance indicator",
            "penilaian kinerja",
            "performance review",
            "evaluasi karyawan",
            "KPI gimana caranya",
            "target KPI",
            "nilai KPI",
            "sistem penilaian kerja",
            "assessment karyawan",
        ],
        "jawaban": "KPI adalah indikator performa utama yang dinilai setiap semester untuk menentukan kenaikan gaji dan bonus."
    },
    {
        "kategori": "karir",
        "pertanyaan_utama": "Kapan evaluasi karyawan kontrak?",
        "variasi": [
            "kontrak diperpanjang kapan",
            "evaluasi PKWT",
            "kontrak habis gimana",
            "perpanjangan kontrak",
            "diangkat tetap kapan",
            "status kontrak",
            "review karyawan kontrak",
            "masa kontrak selesai",
            "kontrak mau habis",
            "kontrak ke tetap",
        ],
        "jawaban": "Evaluasi dilakukan 1 bulan sebelum masa kontrak berakhir untuk menentukan perpanjangan atau pengangkatan tetap."
    },
    {
        "kategori": "karir",
        "pertanyaan_utama": "Apakah perusahaan membiayai sertifikasi?",
        "variasi": [
            "biaya sertifikasi",
            "training sertifikasi",
            "sertifikat ditanggung",
            "certification program",
            "biaya ujian sertifikasi",
            "professional certification",
            "kantor bayar sertifikasi",
            "L&D sertifikasi",
            "program sertifikasi",
            "biaya exam ditanggung",
        ],
        "jawaban": "Ya, melalui program Learning & Development, perusahaan menanggung biaya sertifikasi yang relevan dengan job desc."
    },
    {
        "kategori": "karir",
        "pertanyaan_utama": "Bagaimana cara ikut training internal?",
        "variasi": [
            "daftar training",
            "ikut pelatihan",
            "training karyawan",
            "jadwal training",
            "internal training",
            "program pelatihan",
            "learning program",
            "cara join training",
            "training gratis kantor",
            "workshop internal",
        ],
        "jawaban": "Daftar melalui kalender pelatihan di portal HR Learning atau hubungi atasan Anda."
    },
    
    # ==================== KATEGORI: FASILITAS ====================
    {
        "kategori": "fasilitas",
        "pertanyaan_utama": "Apakah ada jemputan karyawan?",
        "variasi": [
            "shuttle bus kantor",
            "antar jemput karyawan",
            "bus karyawan",
            "transportasi kantor",
            "jemputan dari mana",
            "shuttle kantor",
            "fasilitas antar jemput",
            "bus jemputan",
            "kendaraan kantor",
            "commute ke kantor",
        ],
        "jawaban": "Saat ini perusahaan menyediakan shuttle bus di 3 titik: Bekasi, Depok, dan Tangerang menuju kantor pusat."
    },
    {
        "kategori": "fasilitas",
        "pertanyaan_utama": "Di mana lokasi ruang laktasi?",
        "variasi": [
            "ruang menyusui",
            "nursing room",
            "tempat pompa asi",
            "lactation room",
            "ruang asi",
            "fasilitas laktasi",
            "tempat ibu menyusui",
            "breastfeeding room",
            "pumping room",
            "ruangan untuk menyusui",
        ],
        "jawaban": "Ruang laktasi tersedia di lantai 3, tepat di sebelah klinik kesehatan kantor."
    },
    {
        "kategori": "fasilitas",
        "pertanyaan_utama": "Bagaimana cara pinjam laptop kantor?",
        "variasi": [
            "pinjam laptop",
            "request laptop",
            "butuh laptop",
            "laptop untuk kerja",
            "borrow laptop",
            "peminjaman laptop",
            "laptop kantor",
            "minta laptop",
            "loan laptop",
            "laptop sementara",
        ],
        "jawaban": "Silakan ajukan request peminjaman melalui aplikasi IT Asset Management."
    },
    {
        "kategori": "fasilitas",
        "pertanyaan_utama": "Apa syarat mendapatkan laptop baru?",
        "variasi": [
            "laptop baru kapan",
            "ganti laptop",
            "refresh laptop",
            "laptop replacement",
            "dapat laptop baru",
            "laptop rusak ganti",
            "upgrade laptop",
            "laptop sudah tua",
            "peremajaan laptop",
            "laptop baru karyawan",
        ],
        "jawaban": "Laptop baru diberikan setiap 4 tahun sekali sebagai bagian dari program peremajaan perangkat kerja."
    },
    
    # ==================== KATEGORI: KEBIJAKAN ====================
    {
        "kategori": "kebijakan",
        "pertanyaan_utama": "Apa aturan pakaian hari Jumat?",
        "variasi": [
            "dresscode jumat",
            "pakaian casual friday",
            "baju jumat",
            "friday dress code",
            "batik friday",
            "pakaian kerja jumat",
            "aturan baju jumat",
            "jumat pakai apa",
            "casual friday",
            "dress code friday",
        ],
        "jawaban": "Setiap hari Jumat, karyawan diwajibkan menggunakan pakaian Batik atau Smart Casual yang rapi."
    },
    {
        "kategori": "kebijakan",
        "pertanyaan_utama": "Jam berapa jam kerja dimulai?",
        "variasi": [
            "jam masuk kantor",
            "jam kerja",
            "working hours",
            "office hours",
            "jam operasional",
            "masuk jam berapa",
            "pulang jam berapa",
            "jadwal kerja",
            "jam kantor",
            "shift kerja",
        ],
        "jawaban": "Jam kerja operasional dimulai pukul 08.30 WIB hingga 17.30 WIB dengan waktu istirahat 1 jam."
    },
    {
        "kategori": "kebijakan",
        "pertanyaan_utama": "Apakah boleh kerja remote (WFH)?",
        "variasi": [
            "WFH policy",
            "kerja dari rumah",
            "work from home",
            "remote working",
            "hybrid working",
            "boleh WFH tidak",
            "aturan WFH",
            "WFA",
            "kerja remote",
            "WFH berapa hari",
        ],
        "jawaban": "Kebijakan WFH saat ini adalah Hybrid (3 hari di kantor, 2 hari di rumah) sesuai jadwal tim masing-masing."
    },
    {
        "kategori": "kebijakan",
        "pertanyaan_utama": "Apa sanksi jika sering telat?",
        "variasi": [
            "hukuman telat",
            "sanksi terlambat",
            "telat kena SP",
            "datang telat",
            "keterlambatan karyawan",
            "punishment telat",
            "telat berapa kali kena",
            "terlambat masuk",
            "late penalty",
            "konsekuensi telat",
        ],
        "jawaban": "Keterlambatan lebih dari 3x dalam sebulan tanpa alasan jelas akan dikenakan Surat Peringatan (SP) Lisan."
    },
    {
        "kategori": "kebijakan",
        "pertanyaan_utama": "Apa prosedur jika sakit?",
        "variasi": [
            "izin sakit",
            "sick leave",
            "sakit tidak masuk",
            "lapor sakit",
            "surat dokter",
            "sakit harus ngapain",
            "tidak masuk karena sakit",
            "prosedur sakit",
            "medical leave",
            "cuti sakit",
        ],
        "jawaban": "Informasikan atasan langsung dan serahkan surat keterangan dokter ke HR jika sakit lebih dari 1 hari."
    },
    
    # ==================== KATEGORI: REIMBURSEMENT ====================
    {
        "kategori": "reimbursement",
        "pertanyaan_utama": "Bagaimana cara klaim parkir?",
        "variasi": [
            "reimburse parkir",
            "klaim biaya parkir",
            "parkir diganti",
            "biaya parkir",
            "claim parking",
            "parkir meeting client",
            "parkir business trip",
            "ganti uang parkir",
            "reimbursement parkir",
            "parkir visit client",
        ],
        "jawaban": "Klaim parkir hanya berlaku untuk kunjungan klien (business trip) dengan melampirkan karcis asli di form reimbursement."
    },
    {
        "kategori": "reimbursement",
        "pertanyaan_utama": "Bagaimana cara klaim reimbursement medis?",
        "variasi": [
            "klaim medical",
            "reimburse obat",
            "klaim biaya dokter",
            "medical reimbursement",
            "ganti biaya berobat",
            "claim kesehatan",
            "reimburse rumah sakit",
            "klaim rawat jalan",
            "medical claim",
            "ganti biaya medis",
        ],
        "jawaban": "Unggah foto kuitansi asli dan resume medis ke modul 'Reimbursement' di portal HRIS."
    },
    
    # ==================== KATEGORI: KONTAK ====================
    {
        "kategori": "kontak",
        "pertanyaan_utama": "Siapa kontak darurat HR?",
        "variasi": [
            "nomor HR",
            "hotline HR",
            "telepon HR",
            "contact HR",
            "hubungi HR",
            "nomor darurat HR",
            "HR hotline",
            "emergency contact HR",
            "call HR",
            "WA HR",
        ],
        "jawaban": "Anda bisa menghubungi HR Hotline di nomor 0812-XXXX-XXXX untuk keadaan darurat."
    },
    
    # ==================== KATEGORI: GREETING ====================
    {
        "kategori": "greeting",
        "pertanyaan_utama": "Halo, apa yang bisa kamu lakukan?",
        "variasi": [
            "halo",
            "hi",
            "hello",
            "hai",
            "hey",
            "selamat pagi",
            "selamat siang",
            "selamat sore",
            "kamu bisa apa",
            "fungsi kamu apa",
            "bot ini untuk apa",
            "apa ini",
            "kamu siapa",
            "perkenalkan diri",
        ],
        "jawaban": "Saya adalah asisten HR digital. Saya bisa menjawab pertanyaan seputar kebijakan kantor, cuti, gaji, benefit, dan administrasi HR lainnya. Silakan tanyakan apa saja!"
    },
    {
        "kategori": "greeting",
        "pertanyaan_utama": "Terima kasih bantuannya.",
        "variasi": [
            "terima kasih",
            "makasih",
            "thanks",
            "thank you",
            "thx",
            "tq",
            "trims",
            "terimakasih ya",
            "makasih banyak",
            "thanks a lot",
        ],
        "jawaban": "Sama-sama! Senang bisa membantu Anda. Ada lagi yang ingin ditanyakan?"
    },
    {
        "kategori": "greeting",
        "pertanyaan_utama": "Sampai jumpa",
        "variasi": [
            "bye",
            "goodbye",
            "dadah",
            "sampai nanti",
            "see you",
            "bye bye",
            "selamat tinggal",
            "sudah cukup",
            "tidak ada lagi",
            "cukup sekian",
        ],
        "jawaban": "Terima kasih sudah menggunakan layanan HR Chatbot! Sampai jumpa lagi. 👋"
    },
]

# Fungsi untuk mendapatkan semua pertanyaan dan jawaban dalam format flat
def get_flat_qa_pairs():
    """Menghasilkan list of tuples (pertanyaan, jawaban, kategori)"""
    pairs = []
    for item in HR_KNOWLEDGE_BASE:
        # Tambahkan pertanyaan utama
        pairs.append((item["pertanyaan_utama"], item["jawaban"], item["kategori"]))
        # Tambahkan semua variasi
        for variasi in item["variasi"]:
            pairs.append((variasi, item["jawaban"], item["kategori"]))
    return pairs

# Fungsi untuk mendapatkan semua kategori unik
def get_categories():
    return list(set(item["kategori"] for item in HR_KNOWLEDGE_BASE))

if __name__ == "__main__":
    pairs = get_flat_qa_pairs()
    print(f"Total pertanyaan (dengan variasi): {len(pairs)}")
    print(f"Kategori: {get_categories()}")
