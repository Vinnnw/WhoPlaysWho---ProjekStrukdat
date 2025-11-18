# Simpan file ini di folder 'pages/'
import streamlit as st
import sys
import os

# ----------------------------------------------------------------------
# Impor fungsi dari file utama (app.py)
# ----------------------------------------------------------------------
try:
    # Mengimpor fungsi API dari file utama (app.py)
    from app import ambil_data_dari_api
except ImportError:
    st.error("Error: Tidak dapat mengimpor fungsi 'ambil_data_dari_api' dari app.py.")
    st.stop()


# Konstanta Gambar
GAMBAR_PREFIX = "https://image.tmdb.org/t/p/w500" 
GAMBAR_PREFIX_ACTOR = "https://image.tmdb.org/t/p/w200"

# ==============================================================================
# FUNGSI TAMPILAN DETAIL FILM (F2, F3)
# ==============================================================================

def tampilkan_detail_film(movie_id):
    """Menampilkan detail film, dengan fokus Aktor di bagian atas."""
    
    # Ambil Data
    data_film = ambil_data_dari_api(f"movie/{movie_id}")
    data_kredit = ambil_data_dari_api(f"movie/{movie_id}/credits")

    if not data_film or 'title' not in data_film:
        st.error("Gagal memuat detail film.")
        return

    st.header(data_film['title'])
    
    # -----------------------------------------------
    # 1. DAFTAR AKTOR (FOKUS UTAMA)
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
    # 2. POSTER & SINOPSIS (DETAIL FILM)
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
        # Tombol kembali yang akan mengarahkan ke file app.py
        st.session_state.selected_movie_id = None
        st.switch_page("app.py")


# ==============================================================================
# LOGIKA EKSEKUSI HALAMAN (Memastikan TIDAK ADA Inputan Baru)
# ==============================================================================

if __name__ == "__main__":
    
    if 'selected_movie_id' not in st.session_state or st.session_state.selected_movie_id is None:
        # Jika halaman ini diakses tanpa ID film (seharusnya tidak terjadi), kembalikan
        st.warning("Silakan pilih film terlebih dahulu di halaman utama.")
        st.switch_page("app.py")
    else:
        st.set_page_config(layout="wide")
        tampilkan_detail_film(st.session_state.selected_movie_id)
