import streamlit as st
import pandas as pd
import sklearn as sk

st.set_page_config(
    page_title="Kalkulator Gizi Harian",
    page_icon="🩺",
    layout="centered"
)

# Membaca file style.css eksternal
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    local_css("style.css")
except FileNotFoundError:
    pass

URL_BANNER = "https://i.pinimg.com/1200x/b4/dc/e0/b4dce0118481543f22e2b2cecca6f8eb.jpg"

st.markdown(f"""
    <div class="banner-container">
        <img class="banner-img" src="{URL_BANNER}" alt="Banner Buah Segar">
    </div>
    <div class="main-title">Kalkulator Gizi Makanan</div>
    <div class="sub-title">Sistem Pemantauan Nutrisi Harian Terintegrasi</div>
""", unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 1

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'jenis_kelamin': "---",
        'umur': 20,
        'tinggi_badan': 160,
        'berat_badan': 55,
        'tingkat_aktivitas': "---",
        'bmr': 0.0,
        'tdee': 0.0
    }

if 'makanan_terpilih' not in st.session_state:
    st.session_state.makanan_terpilih = []

# Fungsi untuk mereset aplikasi kembali ke awal
def reset_ke_awal():
    st.session_state.step = 1
    st.session_state.user_data = {
        'jenis_kelamin': "---",
        'umur': 20,
        'tinggi_badan': 160,
        'berat_badan': 55,
        'tingkat_aktivitas': "---",
        'bmr': 0.0,
        'tdee': 0.0
    }
    st.session_state.makanan_terpilih = []

# ========================================================
# DATASET
# ========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("nutrition.csv")
    df['name'] = df['name'].str.strip()
    return df

try:
    df_makanan = load_data()
except FileNotFoundError:
    st.error("File 'nutrition.csv' tidak ditemukan. Pastikan file diletakkan di folder yang sama.")
    st.stop()


# ========================================================
# PROFIL
# ========================================================
if st.session_state.step == 1:
    st.subheader("📋 Kategori 1: Profil & Rekam Medis Fisik")
    
    jk = st.selectbox(
        "Pilih Jenis Kelamin", 
        ["---", "Pria", "Wanita"], 
        index=["---", "Pria", "Wanita"].index(st.session_state.user_data['jenis_kelamin'])
    )
    
    if jk == "---":
        st.info("ℹ️ Silakan tentukan jenis kelamin Anda untuk memulai analisis gizi.")
        st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)
        st.caption(f"📊 **Informasi Sistem:** Terdeteksi {len(df_makanan)} jenis bahan makanan di dalam database siap analisis.")
    else:
        col_in1, col_in2, col_in3 = st.columns(3)
        with col_in1:
            umur = st.number_input("Umur (Tahun)", min_value=0, max_value=120, value=st.session_state.user_data['umur'])
        with col_in2:
            tinggi_badan = st.number_input("Tinggi Badan (CM)", min_value=0, max_value=250, value=st.session_state.user_data['tinggi_badan'])
        with col_in3:
            berat_badan = st.number_input("Berat Badan (KG)", min_value=0, max_value=300, value=st.session_state.user_data['berat_badan'])

        list_aktivitas = [
            "---",
            "Jarang gerak / Aktivitas pasif (Duduk terus)",
            "Aktivitas ringan (Olahraga ringan 1-3 kali/minggu)",
            "Aktivitas sedang (Olahraga intensitas sedang 3-5 kali/minggu)",
            "Aktivitas berat (Olahraga berat 6-7 kali/minggu)",
            "Aktivitas sangat berat (Latihan fisik intens 2x sehari / Atlet)"
        ]
        
        # Mencari indeks aktivitas sebelumnya jika ada
        default_act_idx = list_aktivitas.index(st.session_state.user_data['tingkat_aktivitas']) if st.session_state.user_data['tingkat_aktivitas'] in list_aktivitas else 0
        
        tingkat_aktivitas = st.selectbox("Tingkat Aktivitas Fisik Harian", list_aktivitas, index=default_act_idx)
        
        if tingkat_aktivitas != "---":
            # Hitung BMR
            if jk == "Pria":
                bmr = (10 * berat_badan) + (6.25 * tinggi_badan) - (5 * umur) + 5
            else:
                bmr = (10 * berat_badan) + (6.25 * tinggi_badan) - (5 * umur) - 161
            
            # Hitung TDEE
            if "Jarang gerak" in tingkat_aktivitas:
                tdee = bmr * 1.2
            elif "Aktivitas ringan" in tingkat_aktivitas:
                tdee = bmr * 1.375
            elif "Aktivitas sedang" in tingkat_aktivitas:
                tdee = bmr * 1.55
            elif "Aktivitas berat" in tingkat_aktivitas:
                tdee = bmr * 1.725
            elif "Aktivitas sangat berat" in tingkat_aktivitas:
                tdee = bmr * 1.9
                
            # Simpan ke session state
            st.session_state.user_data = {
                'jenis_kelamin': jk,
                'umur': umur,
                'tinggi_badan': tinggi_badan,
                'berat_badan': berat_badan,
                'tingkat_aktivitas': tingkat_aktivitas,
                'bmr': bmr,
                'tdee': tdee
            }
            
            st.write("")
            if st.button("Lanjut ke Pilihan Makanan ➡️", use_container_width=True):
                st.session_state.step = 2
                st.rerun()


# ========================================================
# PILIHAN MAKANAN
# ========================================================
elif st.session_state.step == 2:
    st.subheader("🥗 Kategori 2: Catatan Konsumsi Makanan Harian")
    
    # Tampilkan info ringkas TDEE pasien di atas sebagai acuan
    st.caption(f"🎯 Batas Energi Harian Anda (TDEE): **{int(st.session_state.user_data['tdee'])} kkal**")
    
    makanan_terpilih = st.multiselect(
        "Pilih daftar makanan yang dikonsumsi hari ini:", 
        options=df_makanan['name'].unique(),
        default=st.session_state.makanan_terpilih
    )
    
    st.session_state.makanan_terpilih = makanan_terpilih
    
    if makanan_terpilih:
        st.write("")
        st.markdown("##### ⚖️ Atur Kuantitas Porsi Konsumsi (Kelipatan 100g):")
        
        # Dictionary untuk menampung porsi sementara
        porsi_dict = {}
        
        for makanan in makanan_terpilih:
            row = df_makanan[df_makanan['name'] == makanan].iloc[0]
            col1, col2 = st.columns([3, 1])
            with col1:
                porsi_dict[makanan] = st.number_input(
                    f"Porsi untuk {makanan} (Standar: {row['calories']} kkal)", 
                    min_value=0.1, 
                    value=1.0, 
                    step=0.5,
                    key=f"step2_porsi_{makanan}"
                )
            with col2:
                if pd.notna(row['image']) and str(row['image']).startswith("http"):
                    st.image(row['image'], width=80)
                    
        # Simpan porsi yang diinput ke session state porsi makanan
        st.session_state.porsi_makanan = porsi_dict
        
        st.write("")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("⬅️ Kembali", use_container_width=True):
                st.session_state.step = 1
                st.rerun()
        with col_btn2:
            if st.button("Lihat Hasil & Rekomendasi 📊", use_container_width=True):
                st.session_state.step = 3
                st.rerun()
    else:
        st.info("💡 Silakan pilih minimal 1 jenis makanan untuk melanjutkan analisis gizi.")
        if st.button("⬅️ Kembali ke Profil", use_container_width=True):
            st.session_state.step = 1
            st.rerun()


# ========================================================
#  HASIL & REKOMENDASI GIZI
# ========================================================
elif st.session_state.step == 3:
    st.subheader("📊 Kategori 3: Hasil Analisis & Lembar Medis")
    
    # Mengambil data dari state sebelumnya
    ud = st.session_state.user_data
    makanan_terpilih = st.session_state.makanan_terpilih
    porsi_makanan = st.session_state.get('porsi_makanan', {})
    
    total_kalori = 0.0
    total_protein = 0.0
    total_lemak = 0.0
    total_karbo = 0.0
    
    for makanan in makanan_terpilih:
        row = df_makanan[df_makanan['name'] == makanan].iloc[0]
        porsi = porsi_makanan.get(makanan, 1.0)
        
        total_kalori += porsi * float(row['calories'])
        total_protein += porsi * float(row['proteins'])
        total_lemak += porsi * float(row['fat'])
        total_karbo += porsi * float(row['carbohydrate'])
        
    # 1. Tampilan Kebutuhan Energi Awal
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric(label="Basal Metabolic Rate (BMR)", value=f"{int(ud['bmr'])} kkal")
    with col_res2:
        st.metric(label="Total Daily Energy Expenditure (TDEE)", value=f"{int(ud['tdee'])} kkal")
        
    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)
    
    # 2. Rekapitulasi Nutrisi Makanan yang dikonsumsi
    st.markdown("##### 🍽️ Total Nutrisi yang Dikonsumsi Hari Ini:")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Total Energi", f"{total_kalori:.1f} kkal")
    m_col2.metric("🍖 Protein", f"{total_protein:.1f} g")
    m_col3.metric("🥑 Lemak", f"{total_lemak:.1f} g")
    m_col4.metric("🍞 Karbohidrat", f"{total_karbo:.1f} g")
    
    st.write("")
    
    # 3. Evaluasi Kalori & Box Rekomendasi
    selisih_kalori = ud['tdee'] - total_kalori
    
    if abs(selisih_kalori) <= 150:
        st.success(f"⚖️ **Status Kalori: Seimbang!** Asupan energi harian Anda ({total_kalori:.1f} kkal) sesuai dengan ambang batas TDEE Anda ({ud['tdee']:.1f} kkal).")
        st.markdown("""
        <div class="rekomendasi-box">
            <strong>Panduan Pola Makan (Maintenance):</strong><br>
            • Pertahankan menu ini jika fokus utama Anda menjaga stabilitas berat badan saat ini.<br>
            • Pastikan konsumsi air mineral tetap terjaga minimal 2 hingga 2.5 liter per hari untuk kelancaran metabolisme tubuh.
        </div>
        """, unsafe_allow_html=True)
    elif selisih_kalori > 150:
        st.warning(f"📉 **Status Kalori: Defisit Energi!** Tubuh mengalami defisit energi sebesar **{selisih_kalori:.1f} kkal** hari ini.")
        st.markdown("""
        <div class="rekomendasi-box">
            <strong>Panduan Pola Makan (Deficit):</strong><br>
            • <strong>Rencana Penurunan Berat Badan:</strong> Rentang defisit energi Anda berada pada batas aman yang sehat. Pertahankan konsistensi ini.<br>
            • <strong>Rencana Peningkatan Berat Badan:</strong> Sangat disarankan untuk meningkatkan konsumsi makanan padat nutrisi makro yang kaya lemak baik, seperti alpukat atau kacang-kacangan.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"📈 **Status Kalori: Surplus Energi!** Terjadi kelebihan pasokan asupan sebesar **{abs(selisih_kalori):.1f} kkal** dari batas toleransi harian.")
        st.markdown("""
        <div class="rekomendasi-box">
            <strong>Panduan Pola Makan (Surplus):</strong><br>
            • <strong>Rencana Penurunan Berat Badan:</strong> Kurangi konsumsi karbohidrat sederhana atau lemak jenuh esok hari. Tingkatkan aktivitas fisik sedang untuk membakar sisa energi.<br>
            • <strong>Rencana Pembentukan Massa Otot:</strong> Target surplus terpenuhi. Pastikan diimbangi dengan latihan beban yang optimal agar protein terserap dengan baik ke jaringan otot.
        </div>
        """, unsafe_allow_html=True)

    # 4. Evaluasi Protein Singkat
    st.write("")
    if total_protein < (ud['berat_badan'] * 1.0):
        st.info(f"⚠️ **Catatan Protein:** Capaian protein baru menyentuh {total_protein:.1f}g. Disarankan menambah menu tinggi protein (seperti dada ayam, ikan, tempe, tahu) agar setara berat badan Anda ({ud['berat_badan']}g) guna menjaga regenerasi sel.")
    else:
        st.success(f"✅ **Catatan Protein:** Kebutuhan protein harian tubuh Anda ({total_protein:.1f}g) sudah terpenuhi dengan sangat baik.")

    # ========================================================
    # TOMBOL KENDALI 
    # ========================================================
    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)
    
    col_back1, col_back2 = st.columns(2)
    with col_back1:
        if st.button("⬅️ Ubah Menu Pilihan Makanan", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    with col_back2:
        if st.button("🔄 Kembali ke Halaman Awal", use_container_width=True):
            reset_ke_awal()
            st.rerun()