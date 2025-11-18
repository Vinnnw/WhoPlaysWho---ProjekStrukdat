import streamlit as st
import requests

# ==============================================================================
# 1. SETUP KONSTANTA & FUNGSI API
# ==============================================================================

# Ganti dengan API Key Anda yang sudah didapat
TMDB_API_KEY = "e76b4db28d15b094e06f08fd37a29267" 
API_URL = "https://api.themoviedb.org/3" 
GAMBAR_PREFIX = "https://image.tmdb.org/t/p/w500" 
GAMBAR_PREFIX_ACTOR = "https://image.tmdb.org/t/p/w200" # Lebih kecil untuk aktor

@st.cache_data(ttl=3600)
def ambil_data_dari_api(endpoint, params=None): 
    """Fungsi umum untuk mengambil data dari TMDb dengan caching."""
    url = f"{API_URL}/{endpoint}?api_key={TMDB_API_KEY}"
    if params:
        url += f"&{params}" 
        
    try:
        respons = requests.get(url)
        respons.raise_for_status() 
        return respons.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error saat mengambil data dari API: {e}")
        return None

def cari_film(query):
    """Fungsi pencarian film (F4) Halaman 1."""
    return ambil_data_dari_api("search/movie", params=f"query={query}") 


# ==============================================================================
# 2. INISIALISASI SESSION STATE (Disederhanakan)
# ==============================================================================

if 'selected_movie_id' not in st.session_state:
    st.session_state.selected_movie_id = None 
if 'page' not in st.session_state:
    st.session_state.page = 'search_page' # Halaman awal: Pencarian
    
    
# ==============================================================================
# 3. FUNGSI HALAMAN (PAGE FUNCTIONS)
# ==============================================================================

# --- FUNGSI actor_detail_page DIHAPUS ---

def movie_detail_page():
    """Menampilkan halaman detail film, dengan tampilan aktor statis."""
    
    movie_id = st.session_state.selected_movie_id
    
    # Ambil Data Film (F2) dan Kredit (F3)
    data_film = ambil_data_dari_api(f"movie/{movie_id}")
    data_kredit = ambil_data_dari_api(f"movie/{movie_id}/credits")

    if data_film and 'title' in data_film:
        st.title(data_film['title'])
        
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            # Tampilkan Poster
            if data_film.get('poster_path'):
                poster_url = GAMBAR_PREFIX + data_film['poster_path']
                st.image(poster_url, width=250)
            else:
                st.image("https://via.placeholder.com/250x375.png?text=No+Poster", width=250)

        with col_info:
            st.subheader("Sinopsis")
            st.info(data_film.get('overview', 'Sinopsis tidak tersedia.'))
            st.markdown(f"**Tahun Rilis:** {data_film.get('release_date', 'N/A')[:4]}")
            st.markdown(f"**Rating:** {data_film.get('vote_average', 0.0):.1f} / 10")
        
        st.markdown("---")

        # Logika Tampilan Aktor Statis
        st.subheader("Para Aktor Utama (Maksimal 15) 🌟")

        if data_kredit and 'cast' in data_kredit:
            aktor_utama = data_kredit['cast'][:15] 
            
            if aktor_utama:
                # Membuat kolom untuk tampilan horizontal
                cols = st.columns(len(aktor_utama))
                
                for i, aktor in enumerate(aktor_utama):
                    with cols[i]:
                        
                        # Menampilkan Foto Aktor
                        if aktor.get('profile_path'):
                            profile_url = GAMBAR_PREFIX_ACTOR + aktor['profile_path']
                            st.image(profile_url, width=100)
                        else:
                            st.text(" [No Image] ")
                        
                        # Hanya menampilkan nama (tidak ada tombol)
                        st.markdown(f"**{aktor['name']}**")

                        st.caption(f"Sebagai: {aktor['character']}")
        else:
            st.warning("Data aktor tidak tersedia untuk film ini.")

    if st.button("⬅️ Kembali ke Pencarian"):
        st.session_state.page = 'search_page'
        st.session_state.selected_movie_id = None
        st.rerun()

def search_page():
    """Halaman Utama Pencarian (F4, F5, F6)"""
    
    st.title("🎬 Movie Profile Explorer (MAP-X)")
    st.caption("Minggu 1 & 2: Pencarian Efisien")
    
    # F4: Input Nama Film
    input_nama_film = st.text_input(
        "Masukkan Judul Film untuk Mencari:",
        placeholder="Contoh: Interstellar",
        key='search_input' 
    )

    # ----------------------------------------------------
    # F5 & F6: DROPDOWN HASIL PENCARIAN dan PEMILIHAN
    # ----------------------------------------------------

    movies = []
    movie_id_map = {}

    if input_nama_film and len(input_nama_film) >= 3:
        hasil_pencarian = cari_film(input_nama_film) 
        movies = hasil_pencarian.get('results', [])

    if movies:
        movie_options = []
        
        for movie in movies[:15]: 
            title = movie['title']
            year = movie.get('release_date', '')[:4]
            option_label = f"{title} ({year})"
            
            movie_options.append(option_label)
            movie_id_map[option_label] = movie['id']

        movie_options.insert(0, '--- Pilih Film dari Hasil Pencarian ---')
        
        # F6: Tampilkan Selectbox
        selected_option = st.selectbox(
            "Hasil Ditemukan, Pilih Film:", 
            movie_options,
            index=0, 
            key='movie_selector' 
        )
        
        # F6: Logika Pemilihan ID
        if selected_option != '--- Pilih Film dari Hasil Pencarian ---':
            st.session_state.selected_movie_id = movie_id_map[selected_option]
            st.session_state.page = 'movie_detail' # Langsung pindah ke halaman detail
            st.rerun()
        
    elif input_nama_film and len(input_nama_film) >= 3:
        st.warning(f"Film dengan judul '{input_nama_film}' tidak ditemukan.")


# ==============================================================================
# 4. FUNGSI UTAMA APLIKASI (Disederhanakan)
# ==============================================================================

def main():
    """Fungsi utama untuk menjalankan aplikasi dan mengelola navigasi."""
    st.set_page_config(layout="wide")
    
    # Logika Navigasi: Hanya dua halaman yang dikelola
    if st.session_state.page == 'search_page':
        search_page()
    elif st.session_state.page == 'movie_detail':
        movie_detail_page()

if __name__ == "__main__":
    main()
