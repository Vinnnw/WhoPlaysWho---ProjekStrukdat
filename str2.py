# Simpan file ini di folder 'pages/'
import streamlit as st
import pandas as pd # Diperlukan untuk visualisasi F9
import requests
import altair as alt # Diperlukan untuk visualisasi F9

# ==============================================================================
# 1. Impor API dari app.py
# ==============================================================================
try:
    from app import ambil_data_dari_api
except ImportError:
    st.error("Error: Tidak dapat mengimpor fungsi 'ambil_data_dari_api' dari app.py.")
    st.stop()


# Konstanta Gambar
GAMBAR_PREFIX = "https://image.tmdb.org/t/p/w500" 
GAMBAR_PREFIX_ACTOR = "https://image.tmdb.org/t/p/w200"

# ==============================================================================
# 2. CSS OVERRIDE (Person 2)
# ==============================================================================

st.markdown("""
<style>
/* Menghilangkan background image dari app.py dan menggantinya dengan warna putih */
.stApp {
    background-image: none;
    background-color: white; 
    color: black; 
    padding-top: 20px;
}
/* Mengatur agar tombol kembali juga terlihat jelas */
.stButton>button {
    background-color: #C0392B; 
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. FUNGSI VISUALISASI F9 (Person 3)
# ==============================================================================

def generate_actor_productivity_chart(credits_data):
    """F9: Menghasilkan Grafik Produktivitas Aktor (Simulasi Data)."""
    
    st.subheader("📊 Visualisasi Data Proyek (F9: Produktivitas Aktor)")
    
    # *** KERANGKA KERJA F9 (Ganti dengan data yang diolah dari API NYATA) ***
    data = pd.DataFrame({
        'Tahun': [2018, 2019, 2020, 2021, 2022, 2023],
        'Jumlah Film': [1, 3, 5, 2, 4, 1]
    })
    
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Tahun:O', title='Tahun Rilis'),
        y=alt.Y('Jumlah Film:Q', title='Jumlah Produksi'),
        tooltip=['Tahun', 'Jumlah Film']
    ).properties(
        title='Contoh: Produktivitas Produksi Film Aktor'
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    # -----------------------------------------------------------------------


# ==============================================================================
# 4. FUNGSI TAMPILAN DETAIL FILM & AKTOR
# ==============================================================================

def tampilkan_detail_film(movie_id):
    """Menampilkan detail film, dengan fokus Aktor di bagian atas."""
    
    data_film = ambil_data_dari_api(f"movie/{movie_id}")
    data_kredit = ambil_data_dari_api(f"movie/{movie_id}/credits")

    if not data_film or 'title' not in data_film:
        st.error("Gagal memuat detail film.")
        return

    st.header(data_film['title'])
    
    # -----------------------------------------------
    # A. DAFTAR AKTOR (Person 3)
    # -----------------------------------------------
    st.subheader("Para Aktor Utama (Top 20) 🌟")

    if data_kredit and 'cast' in data_kredit:
        aktor_utama = data_kredit['cast'][:20] 
        NUM_COLS = 5 
        
        for row_start in range(0, len(aktor_utama), NUM_COLS):
            row_actors = aktor_utama[row_start : row_start + NUM_COLS]
            cols = st.columns(len(row_actors)) 
            
            for i, aktor in enumerate(row_actors):
                with cols[i]:
                    path = aktor.get('profile_path')
                    st.image(f"{GAMBAR_PREFIX_ACTOR}{path}" if path else "https://via.placeholder.com/100x150.png?text=No+Image", width=100)
                    st.markdown(f"**{aktor['name']}**")
                    st.caption(f"Sebagai: {aktor['character']}")
                    st.markdown("---", unsafe_allow_html=True)
    else:
        st.warning("Data aktor tidak tersedia.")
    
    st.markdown("---")
    
    # -----------------------------------------------
    # B. AREA VISUALISASI (Person 3)
    # -----------------------------------------------
    generate_actor_productivity_chart(data_kredit)
    st.markdown("---")
    
    # -----------------------------------------------
    # C. POSTER & SINOPSIS (Person 2)
    # -----------------------------------------------
    st.subheader("Detail Film & Sinopsis")

    col_img, col_info = st.columns([1, 2])
    with col_img:
        path = data_film.get('poster_path')
        st.image(f"{GAMBAR_PREFIX}{path}" if path else "https://via.placeholder.com/250x375.png?text=No+Poster", width=250)
    with col_info:
        st.info(data_film.get('overview', 'Sinopsis tidak tersedia.'))
        st.markdown(f"**Tahun Rilis:** {data_film.get('release_date', 'N/A')[:4]}")
        st.markdown(f"**Rating:** {data_film.get('vote_average', 0.0):.1f} / 10")
    
    if st.button("⬅️ Kembali ke Pencarian", key='back_btn'):
        st.session_state.selected_movie_id = None
        st.switch_page("app.py")


# ==============================================================================
# LOGIKA EKSEKUSI HALAMAN 
# ==============================================================================

if __name__ == "__main__":
    
    if 'selected_movie_id' not in st.session_state or st.session_state.selected_movie_id is None:
        st.warning("Silakan pilih film terlebih dahulu di halaman utama.")
        st.switch_page("app.py")
    else:
        st.set_page_config(layout="wide")
        tampilkan_detail_film(st.session_state.selected_movie_id)
