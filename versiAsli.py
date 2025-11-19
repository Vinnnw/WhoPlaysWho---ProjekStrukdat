import streamlit as st
import requests

# ==============================================================================
# 1. SETUP KONSTANTA & FUNGSI API
# ==============================================================================

TMDB_API_KEY = "e76b4db28d15b094e06f08fd37a29267" 
API_URL = "https://api.themoviedb.org/3" 

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

def cari_film(query):
    return ambil_data_dari_api("search/movie", params=f"query={query}") 

# ==============================================================================
# 2. INISIALISASI SESSION STATE & CSS KUSTOM
# ==============================================================================

if 'selected_movie_id' not in st.session_state:
    st.session_state.selected_movie_id = None 

st.set_page_config(layout="wide")

# GANTI URL DI BAWAH INI dengan URL publik gambar background Anda
BACKGROUND_IMAGE_URL = "https://images5.alphacoders.com/689/thumb-1920-689398.jpg" 

st.markdown(f"""
<style>
/* 1. Mengatur Background Penuh Layar */
.stApp {{
    background-image: url("{BACKGROUND_IMAGE_URL}"); 
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    height: 100vh;
}}

/* 2. Menyembunyikan Header Default Streamlit */
header, footer {{
    visibility: hidden;
    height: 0px;
}}

/* 3. Style untuk Overlay Konten Tengah (Kotak Merah Transparan) */
.content-overlay {{
    background-color: rgba(192, 57, 43, 0.7); 
    border-radius: 15px; 
    padding: 30px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    text-align: center;
    backdrop-filter: blur(3px);
    position: relative; /* Penting untuk positioning judul */
}}

/* 4. Style Judul (WhoPlaysWho) */
.app-title-overlay {{
    color: white;
    font-size: 90px !important;
    font-weight: 500;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
    margin-bottom: 7px;
    text-align: center;
    width: 100%;
}}

/* 5. Style Deskripsi */
.app-description {{
    color: white;
    font-size: 18px !important;
    margin-bottom: 20px;
    text-shadow: 5px 5px 5px rgba(0, 0, 0, 0.6);
    text-align: center;
    /* Atau, lebih singkat: margin: 20px auto; (jika margin atas/bawah tidak perlu diubah) */
}}

/* 6. Menghilangkan label widget input */
.stTextInput label {{
    display: none;
}}

/* 7. Menengahkan input secara vertikal */
.center-container {{
    padding-top: 10vh; 
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* 8. Menyesuaikan tampilan Judul di atas Overlay */
.title-wrapper {{
    /* Mengangkat judul secara visual di atas kotak merah */
    margin-top: -80px; 
    padding-bottom: 10px;
}}

</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. FUNGSI UTAMA APLIKASI (Pencarian & Navigasi)
# ==============================================================================

def main_app():
    """Mengelola alur Pencarian (F4, F5, F6) dan Detail Film."""

    if st.session_state.selected_movie_id:
        st.switch_page("pages/hal2.py") 
        return

    st.markdown('<div class="center-container">', unsafe_allow_html=True)

    col1, col_center, col3 = st.columns([1, 4, 1])

    with col_center:
        
        # 1. Overlay Header dan Judul (Menggunakan Div yang terpisah untuk visual stacking)
        st.markdown('<div class="content-overlay">', unsafe_allow_html=True)

        # Judul (Dibuat terpisah secara visual di atas kotak)
        st.markdown('<div class="title-wrapper">', unsafe_allow_html=True)
        st.markdown('<p class="app-title-overlay">WhoPlays<span style="color:#FF0000;">Who</span></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Deskripsi
        st.markdown('<p class="app-description">Lagi kepo sama siapa yang main di film favoritmu? Tenang, di sini kamu bisa cari film apa pun dan langsung lihat daftar aktornya. Siapa tahu kamu nemu aktor baru yang bakal jadi idolamu.</p>', unsafe_allow_html=True)

        # F4: Input Nama Film
        input_nama_film = st.text_input(
            "Search Film:",
            placeholder="Cari film di sini...",
            key='search_input' 
        )

        st.markdown('</div>', unsafe_allow_html=True) # Penutup Overlay Konten

        # 3. Logika Pencarian dan Dropdown
        movies, movie_id_map = [], {}

        if input_nama_film and len(input_nama_film) >= 3:
            hasil_pencarian = ambil_data_dari_api("search/movie", params=f"query={input_nama_film}") 
            movies = hasil_pencarian.get('results', [])

        if movies:
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
                st.switch_page("pages/hal2.py")

        elif input_nama_film and len(input_nama_film) >= 3:
            st.warning(f"Film dengan judul '{input_nama_film}' tidak ditemukan.")

    st.markdown('</div>', unsafe_allow_html=True) # Penutup Center Container

if __name__ == "__main__":
    main_app()
