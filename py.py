import streamlit as st
import requests

TMDB_API_KEY = "e76b4db28d15b094e06f08fd37a29267" 
API_URL = "https://api.themoviedb.org/3" 
GAMBAR_PREFIX = "https://image.tmdb.org/t/p/w500" 
DEFAULT_MOVIE_ID = 157336 # Interstellar


@st.cache_data(ttl=3600)
def ambil_data_dari_api(endpoint):  
    url = f"{API_URL}/{endpoint}?api_key={TMDB_API_KEY}"
    try:
        respons = requests.get(url)
        return respons.json()
    except:
        return None

id_film = st.text_input(
    "Masukkan ID Film TMDb:")

if id_film:
    st.markdown("---")
    
    data_film = ambil_data_dari_api(f"movie/{id_film}")
    data_kredit = ambil_data_dari_api(f"movie/{id_film}/credits")


    if data_film and 'title' in data_film:
        st.header(data_film['title'])
        
    st.subheader("Sinopsis")
    st.info(data_film.get('overview', 'FILMNYA GAADA.'))
        
    st.markdown(f"**Tahun Rilis:** {data_film.get('release_date', 'N/A')[:4]}")
    st.markdown(f"**Rating:** {data_film.get('vote_average', 0.0):.1f} / 10")
        
 
    st.markdown("---")
    st.subheader("Para Aktor")
        
    if data_kredit and 'cast' in data_kredit:
  
            aktor_utama = data_kredit['cast'][:5] 
            
            if aktor_utama:
                cols = st.columns(len(aktor_utama))
                for i, aktor in enumerate(aktor_utama):
                    st.markdown(f"**{aktor['name']}**")
                    st.caption(f"Sebagai: {aktor['character']}")
        
    else:
        st.error("filmnya gaada, aktornya juga dong")

    st.json(data_film)
