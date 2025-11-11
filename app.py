import streamlit as st
import requests

# ----------------------------------------------------
# F1: INTEGRASI DAN SETUP API
# ----------------------------------------------------

# Kunci API yang Anda berikan
TMDB_API_KEY = "e76b4db28d15b094e06f08fd37a29267" 
# BASE URL TMDB API yang BENAR
TMDB_API_BASE_URL = "https://api.themoviedb.org/3" 
# BASE URL TMDB untuk menampilkan gambar (misalnya ukuran w500)
IMAGE_PREFIX_URL = "https://image.tmdb.org/t/p/w500" 

# ID Film Uji Coba (Contoh: Inception)
TEST_MOVIE_ID = 27205

# Menggunakan cache Streamlit agar permintaan API tidak diulang setiap kali widget diubah
@st.cache_data(ttl=3600)
def get_movie_details(movie_id):
    """Mengambil detail film dari TMDb."""
    # URL yang benar: /3/movie/{id}
    url = f"{TMDB_API_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status() # Cek status HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengambil detail film: {e}")
        return {}

@st.cache_data(ttl=3600)
def get_movie_credits(movie_id):
    """Mengambil daftar aktor (credits) dari TMDb."""
    # URL yang benar: /3/movie/{id}/credits
    url = f"{TMDB_API_BASE_URL}/movie/{movie_id}/credits?api_key={TMDB_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status() # Cek status HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengambil data aktor: {e}")
        return {}


# ----------------------------------------------------
# TAMPILAN UTAMA STREAMLIT
# ----------------------------------------------------

st.title("🎬 Movie & Actor Profile Explorer (MAP-X)")
st.caption("Fokus Minggu 1: Menampilkan detail film statis dan daftar aktor.")
st.markdown("---")

# ----------------------------------------------------
# F2: PENGAMBILAN DAN TAMPILAN DETAIL FILM
# ----------------------------------------------------

st.subheader(f"Detail Film Uji Coba (ID: {TEST_MOVIE_ID})")
movie_data = get_movie_details(TEST_MOVIE_ID)

if 'title' in movie_data:
    st.header(movie_data['title'])
    
    col_img, col_info = st.columns([1, 2]) # Bagi layar untuk poster dan info
    
    with col_img:
        # Menampilkan Poster
        if movie_data.get('poster_path'):
            # PERBAIKAN: Gunakan IMAGE_PREFIX_URL untuk menampilkan gambar
            poster_url = IMAGE_PREFIX_URL + movie_data['poster_path']
            st.image(poster_url, width=250)
        else:
            st.write("Poster tidak tersedia.")

    with col_info:
        st.subheader("Sinopsis")
        st.info(movie_data.get('overview', 'Sinopsis tidak tersedia.'))
        
        # Penanganan data rilis yang mungkin kosong
        release_date = movie_data.get('release_date', 'N/A')
        release_year = release_date[:4] if release_date != 'N/A' and len(release_date) >= 4 else 'N/A'

        st.write(f"**Tahun Rilis:** {release_year}")
        st.write(f"**Rating:** {movie_data.get('vote_average', 0.0):.1f} / 10")
        
else:
    # Error akan ditampilkan oleh fungsi get_movie_details jika gagal mengambil data
    st.error("❌ Gagal memuat detail film. Pastikan API Key valid dan berfungsi.")


st.markdown("---")

# ----------------------------------------------------
# F3: PENGAMBILAN DAN TAMPILAN DATA AKTOR PRIMER
# ----------------------------------------------------

st.subheader("👨‍🎤 Daftar Aktor Utama (Cast)")
credits_data = get_movie_credits(TEST_MOVIE_ID)

if credits_data and 'cast' in credits_data:
    # Ambil 8 aktor utama saja
    actors = credits_data['cast'][:8] 
    actor_columns = st.columns(len(actors))

    for i, actor in enumerate(actors):
        with actor_columns[i]:
            actor_id = actor['id']
            
            # Tampilkan Nama Aktor dan Karakter
            st.markdown(f"**{actor['name']}**")
            st.caption(f"Sebagai: {actor['character']}")
            
            # Tampilkan Foto Profil
            if actor.get('profile_path'):
                # PERBAIKAN: Gunakan IMAGE_PREFIX_URL untuk menampilkan foto
                profile_url = IMAGE_PREFIX_URL + actor['profile_path']
                st.image(profile_url, width=100)
            else:
                # Placeholder jika tidak ada foto
                st.write("No Photo")
            
            # Catatan untuk Minggu 3: Link/ID sudah tersedia
            # st.caption(f"ID Aktor: {actor_id}") 
            
else:
    st.warning("Data aktor tidak ditemukan untuk film ini.")

st.markdown("---")
st.markdown("**Status:** Code siap dijalankan. Harap pastikan lingkungan virtual sudah aktif (`source .venv/bin/activate`) sebelum menjalankan `streamlit run app.py`.")