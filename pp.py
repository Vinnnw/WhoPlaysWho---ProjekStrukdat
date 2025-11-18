import streamlit as st
import requests

# ==============================================================================
# 1. SETUP KONSTANTA & FUNGSI API
# ==============================================================================
# (Bagian ini akan dikerjakan bersama di awal, atau oleh Person 1)

TMDB_API_KEY = "e76b4db28d15b094e06f08fd37a29267" 
API_URL = "https://api.themoviedb.org/3" 
GAMBAR_PREFIX = "https://image.tmdb.org/t/p/w500" 
GAMBAR_PREFIX_ACTOR = "https://image.tmdb.org/t/p/w200"

@st.cache_data(ttl=3600)
def ambil_data_dari_api(endpoint, params=None): 
    """Mengambil data dari TMDb."""
    url = f"{API_URL}/{endpoint}?api_key={TMDB_API_KEY}"
    if params: url += f"&{params}" 
    try:
        respons = requests.get(url)
        respons.raise_for_status() 
        return respons.json()
    except requests.exceptions.RequestException:
        return None

# ==============================================================================
# 2. INISIALISASI SESSION STATE & PENGATURAN TAMPILAN
# ==============================================================================
# (Bagian ini akan dikerjakan oleh Person 1)

if 'selected_movie_id' not in st.session_state:
    st.session_state.selected_movie_id = None 

st.set_page_config(layout="wide")
st.title("🎬 Movie Profile Explorer (MAP-X)")

# ==============================================================================
# 3. FUNGSI TAMPILAN DETAIL FILM (F2, F3)
# ==============================================================================
# (Dikerjakan bersama oleh Person 2 & Person 3, di branch masing-masing)

def tampilkan_detail_film(movie_id):
    """Menampilkan detail film, dengan fokus Aktor di bagian atas."""
    data_film = ambil_data_dari_api(f"movie/{movie_id}")
    data_kredit = ambil_data_dari_api(f"movie/{movie_id}/credits")

    if not data_film or 'title' not in data_film:
        st.error("Gagal memuat detail film.")
        return

    st.header(data_film['title'])
    
    # -----------------------------------------------
    # 1. DAFTAR AKTOR (Person 3)
    # -----------------------------------------------
    # [START: Person 3 - Actor Grid Logic]
    st.subheader("Para Aktor Utama (Top 20) 🌟")

    if data_kredit and 'cast' in data_kredit:
        aktor_utama = data_kredit['cast'][:20] 
        NUM_COLS = 5 # Menampilkan 5 aktor per baris
        
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
    # [END: Person 3 - Actor Grid Logic]
    
    st.markdown("---")
    
    # -----------------------------------------------
    # 2. POSTER & SINOPSIS (Person 2)
    # -----------------------------------------------
    # [START: Person 2 - Movie Detail Logic]
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
        st.rerun()
    # [END: Person 2 - Movie Detail Logic]

# ==============================================================================
# 4. FUNGSI UTAMA APLIKASI (Pencarian & Navigasi)
# ==============================================================================
# (Dikerjakan oleh Person 1)

def main_app():
    """Mengelola alur Pencarian (F4, F5, F6) dan Detail Film."""

    if st.session_state.selected_movie_id:
        tampilkan_detail_film(st.session_state.selected_movie_id)
        return

    st.caption("Pencarian dan Pemilihan Film")
    
    input_nama_film = st.text_input(
        "Masukkan Judul Film untuk Mencari:",
        placeholder="Contoh: Interstellar",
        key='search_input' 
    )

    movies, movie_id_map = [], {}

    if input_nama_film and len(input_nama_film) >= 3:
        hasil_pencarian = ambil_data_dari_api("search/movie", params=f"query={input_nama_film}") 
        movies = hasil_pencarian.get('results', [])

    if movies:
        for movie in movies[:10]:
            label = f"{movie['title']} ({movie.get('release_date', '')[:4]})"
            movie_id_map[label] = movie['id']

        movie_options = ['--- Pilih Film dari Hasil Pencarian ---'] + list(movie_id_map.keys())
        
        selected_option = st.selectbox(
            "Hasil Ditemukan, Pilih Film:", 
            movie_options,
            index=0, 
            key='movie_selector' 
        )
        
        if selected_option != '--- Pilih Film dari Hasil Pencarian ---':
            st.session_state.selected_movie_id = movie_id_map[selected_option]
            st.rerun()

    elif input_nama_film and len(input_nama_film) >= 3:
        st.warning(f"Film dengan judul '{input_nama_film}' tidak ditemukan.")


if __name__ == "__main__":
    main_app()
