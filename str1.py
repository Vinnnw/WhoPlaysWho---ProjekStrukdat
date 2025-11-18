import streamlit as st
import requests

# ==============================================================================
# 1. SETUP KONSTANTA & FUNGSI API (Sama seperti sebelumnya)
# ==============================================================================

TMDB_API_KEY = "e76b4db28d15b094e06f08fd37a29267" 
API_URL = "https://api.themoviedb.org/3" 

@st.cache_data(ttl=3600)
def ambil_data_dari_api(endpoint, params=None): 
    # ... (Fungsi API tidak berubah) ...
    url = f"{API_URL}/{endpoint}?api_key={TMDB_API_KEY}"
    if params: url += f"&{params}" 
    try:
        respons = requests.get(url)
        respons.raise_for_status() 
        return respons.json()
    except requests.exceptions.RequestException:
        return None

def cari_film(query):
    return ambil_data_dari_api("search/movie", params=f"query={query}") 

# ==============================================================================
# 2. INISIALISASI SESSION STATE & PENGATURAN TAMPILAN
# ==============================================================================

if 'selected_movie_id' not in st.session_state:
    st.session_state.selected_movie_id = None 

st.set_page_config(layout="wide")


# --- CSS KUSTOM UNTUK TAMPILAN 'WhoPlaysWho' ---
# CSS ini menyembunyikan header default Streamlit dan membuat header kustom
st.markdown("""
<style>
/* 1. Menyembunyikan elemen default Streamlit */
.stApp {
    background-color: white; /* Atur background body utama menjadi putih */
}
header {
    visibility: hidden; /* Sembunyikan header default Streamlit */
    height: 0px;
}

/* 2. Style untuk Header Merah Kustom */
.custom-header {
    background-color: #C0392B; /* Warna Merah Khas */
    padding: 30px 0; /* Padding atas dan bawah */
    color: white;
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 20px; /* Jarak dari header ke konten */
}

/* 3. Style untuk Judul 'WhoPlaysWho' */
.app-title {
    color: white;
    font-family: sans-serif;
    letter-spacing: 2px;
}
.app-title span {
    color: #FFC300; /* Warna kuning atau terang untuk kata kedua */
}

/* 4. Memastikan input/dropdown terpusat */
.stTextInput, .stSelectbox {
    width: 600px; /* Lebar yang masuk akal */
    margin: 0 auto; /* Menengahkan input widget */
}

/* 5. Mengatur ikon di tengah halaman */
.movie-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 100px; /* Jarak dari atas */
}

</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. FUNGSI UTAMA APLIKASI (Pencarian & Navigasi)
# ==============================================================================

def main_app():
    """Mengelola alur Pencarian (F4, F5, F6) dan Detail Film."""

    # Tampilkan Detail Film jika ID sudah terpilih (Navigasi Halaman Detail)
    if st.session_state.selected_movie_id:
        # Langsung pindah ke halaman detail karena sudah dipilih
        st.switch_page("pages/hal2.py") 
        return

    # --- Header Kustom ---
    st.markdown('<div class="custom-header"><span class="app-title">WhoPlays</span><span class="app-title" style="color:#FFFFFF">Who</span></div>', unsafe_allow_html=True)


    # --- Konten Pencarian (Ditempatkan di Tengah) ---
    
    # F4: Input Nama Film
    input_nama_film = st.text_input(
        "Search here",
        label_visibility="hidden", # Menyembunyikan label "Search here"
        placeholder="Search here",
        key='search_input' 
    )


    movies, movie_id_map = [], {}

    if input_nama_film and len(input_nama_film) >= 3:
        hasil_pencarian = cari_film(input_nama_film) 
        movies = hasil_pencarian.get('results', [])

    if movies:
        # F5: Persiapan Dropdown Hasil Pencarian
        for movie in movies[:10]:
            label = f"{movie['title']} ({movie.get('release_date', '')[:4]})"
            movie_id_map[label] = movie['id']

        movie_options = ['--- Pilih Film dari Hasil Pencarian ---'] + list(movie_id_map.keys())
        
        # F6: Tampilkan Selectbox & Logika Pemilihan
        selected_option = st.selectbox(
            "Hasil Ditemukan, Pilih Film:", 
            movie_options,
            index=0, 
            key='movie_selector' 
        )
        
        if selected_option != '--- Pilih Film dari Hasil Pencarian ---':
            st.session_state.selected_movie_id = movie_id_map[selected_option]
            st.switch_page("pages/hal2.py") # Navigasi
            
    elif input_nama_film and len(input_nama_film) >= 3:
        st.warning(f"Film dengan judul '{input_nama_film}' tidak ditemukan.")


if __name__ == "__main__":
    main_app()
