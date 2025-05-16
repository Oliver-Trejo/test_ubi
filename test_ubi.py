import streamlit as st
from streamlit_javascript import st_javascript
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="GPS Real", layout="centered")
st.title("📍 Obtén tu ubicación en tiempo real")

# Obtener ubicación con JavaScript correctamente
coordenadas = st_javascript("""
    async function getCoords() {
        return await new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition(
                (pos) => resolve({ value: { lat: pos.coords.latitude, lon: pos.coords.longitude } }),
                (err) => resolve({ value: null })
            );
        });
    }
    getCoords();
""")

# Mostrar coordenadas y mapa si están disponibles
if coordenadas and "lat" in coordenadas and "lon" in coordenadas:
    lat = coordenadas["lat"]
    lon = coordenadas["lon"]
    st.success(f"✅ Coordenadas obtenidas:\nLatitud: {lat}\nLongitud: {lon}")

    # Mostrar mapa con marcador
    mapa = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], tooltip="📍 Aquí estás").add_to(mapa)
    folium_static(mapa)
else:
    st.warning("⚠️ Asegúrate de permitir el acceso a la ubicación en tu navegador.")
