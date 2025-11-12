import streamlit as st
import requests


# Kunci API TMDb Anda
TMDB_API_KEY = "e76b4db28d15b094e06f08fd37a29267" 
# URL dasar untuk semua panggilan API
API_URL = "https://api.themoviedb.org/3" 
# URL dasar untuk menampilkan gambar (ukuran w500)
GAMBAR_PREFIX_URL = "https://image.tmdb.org/t/p/w500" 

# TAMPILAN UTAMA STREAMLIT

st.title("WhoPlaysWho?")
st.caption("Cari tahu siapa aktor di balik karakter film favorit Anda!")
st.markdown("---")

# --- FUNGSI UTAMA (Dipertahankan agar Streamlit CEPAT) ---
# Menggunakan cache agar Streamlit tidak memanggil API berulang kali
@st.cache_data(ttl=3600)
def ambil_data_dari_api(endpoint):
    """Fungsi sederhana untuk mengambil data JSON dari endpoint TMDb."""
    url_lengkap = f"{API_URL}/{endpoint}&api_key={TMDB_API_KEY}"
    try:
        respons = requests.get(url_lengkap)
        return respons.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengambil data: {e}")
        return None

# BAGIAN PENCARIAN FILM

# 1. Input Teks untuk Mencari Nama Film
nama_film_cari = st.text_input(
    "Cari Film:", 
    placeholder="Masukin nama film yang mau kamu cari", 
    key="cari_bar"
)

id_film_terpilih = None
data_film = None
data_kredit = None

if nama_film_cari:
    # 2. Melakukan Pencarian
    endpoint_cari = f"search/movie?query={nama_film_cari}"
    hasil_cari = ambil_data_dari_api(endpoint_cari)

    if hasil_cari and hasil_cari.get('results'):
        results = hasil_cari['results']
        
        # Siapkan opsi untuk dropdown
        opsi_film = {
            f"{r['title']} ({r.get('release_date', '')[:4]})": r['id']
            for r in results
        }
        
        # 3. Dropdown untuk Memilih Film
        judul_terpilih = st.selectbox(
            "Pilih Hasil yang Sesuai:", 
            options=list(opsi_film.keys())
        )
        
        # Dapatkan ID dari film yang dipilih
        id_film_terpilih = opsi_film.get(judul_terpilih)
    
    else:
        st.warning(f"Ngga ada nama film kayak gitu")

# BAGIAN MENAMPILKAN DETAIL FILM

if id_film_terpilih:
    st.markdown("---")
    
    # 4. Ambil Detail Film
    endpoint_detail = f"movie/{id_film_terpilih}?"
    data_film = ambil_data_dari_api(endpoint_detail)
    
    # 5. Ambil Data Aktor
    endpoint_kredit = f"movie/{id_film_terpilih}/credits?"
    data_kredit = ambil_data_dari_api(endpoint_kredit)

    
    if data_film and 'title' in data_film:
        st.header(data_film['title'])
        
        kol_gambar, kol_info = st.columns([1, 2])
        
        with kol_gambar:
            # Tampilkan Poster
            if data_film.get('poster_path'):
                url_poster = GAMBAR_PREFIX_URL + data_film['poster_path']
                st.image(url_poster, width=250)
            else:
                st.write("Poster tidak tersedia.")

        with kol_info:
            st.subheader("Sinopsis")
            # Menampilkan Sinopsis Asli
            st.info(data_film.get('overview', 'Sinopsis tidak tersedia.'))
            
            tanggal_rilis = data_film.get('release_date', 'N/A')
            tahun_rilis = tanggal_rilis[:4] if tanggal_rilis != 'N/A' and len(tanggal_rilis) >= 4 else 'N/A'

            st.write(f"**Tahun Rilis:** {tahun_rilis}")
            st.write(f"**Rating:** {data_film.get('vote_average', 0.0):.1f} / 10")
            
    # BAGIAN MENAMPILKAN AKTOR UTAMA
    
    st.markdown("---")
    st.subheader("Daftar Aktor Utama")
    
    if data_kredit and 'cast' in data_kredit:
        aktor_utama = data_kredit['cast'][:8] 
        jumlah_aktor = len(aktor_utama)
        
        if jumlah_aktor > 0:
            kolom_aktor = st.columns(jumlah_aktor)

            for i, aktor in enumerate(aktor_utama):
                with kolom_aktor[i]:
                    st.markdown(f"**{aktor['name']}**")
                    st.caption(f"Sebagai: {aktor['character']}")
                    
                    # Tampilkan Foto Profil
                    if aktor.get('profile_path'):
                        url_profil = GAMBAR_PREFIX_URL + aktor['profile_path']
                        st.image(url_profil, width=100)
                    else:
                        st.write("Foto tidak tersedia.")
    else:
        st.warning("Data aktor tidak ditemukan untuk film ini.")

