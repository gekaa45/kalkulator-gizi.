# Kalkulator Gizi Makanan

Sistem Pemantauan Nutrisi Harian Terintegrasi yang dirancang untuk membantu pengguna menghitung kebutuhan metabolisme tubuh (BMR & TDEE)

## Fitur
Aplikasi ini dibagi menjadi 3 kategori alur utama secara bertahap (multi-step wizard):
1. Kategori 1: Profil & Rekam Medis Fisik
   * Input data fisik meliputi jenis kelamin, umur, tinggi badan, dan berat badan.
   * Pemilihan tingkat aktivitas fisik harian untuk akurasi perhitungan energi.
   * Perhitungan otomatis BMR (Basal Metabolic Rate) dan TDEE (Total Daily Energy Expenditure).
2. Kategori 2: Catatan Konsumsi Makanan Harian
   * Pemilihan bahan makanan secara dinamis langsung dari database sistem.
   * Pengaturan kuantitas porsi konsumsi interaktif dengan kelipatan 100 gram.
3. Kategori 3: Hasil Analisis & Lembar Medis
   * Rekapitulasi total nutrisi harian (Energi/Kalori, Protein, Lemak, dan Karbohidrat).
   * Evaluasi status kalori (Seimbang / Defisit / Surplus) lengkap dengan lembar rekomendasi pola makan praktis.
   * Catatan pemenuhan kebutuhan protein harian yang disesuaikan dengan berat badan pengguna.

---
Proyek ini dibuat menggunakan ekosistem Python dengan pustaka sebagai berikut:
* [Streamlit](https://streamlit.io/) - Framework untuk antarmuka web interaktif.
* [Pandas](https://pandas.pydata.org/) - Manajemen dan manipulasi dataset bahan makanan (nutrition.csv).
* [Scikit-Learn](https://scikit-learn.org/) - Pustaka pendukung analisis komputasi.

---

## Struktur File Repositori
Pastikan struktur file di dalam repositori Anda tersusun sebagai berikut:
```text
kalkulator-gizi/
├── app.py            # File utama kode logika aplikasi Streamlit
├── style.css         # File kustomisasi gaya tampilan UI Premium
├── nutrition.csv     # Database kandungan nutrisi bahan makanan
└── requirements.txt  # Daftar dependensi library untuk deployment

Panduan menjalankan:
1. git clone [https://github.com/username-kamu/kalkulator-gizi.git](https://github.com/username-kamu/kalkulator-gizi.git)
cd kalkulator-gizi
2. pip install -r requirements.txt
3. python -m streamlit run app.py


