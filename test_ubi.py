import streamlit as st
from streamlit_javascript import st_javascript
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="GPS Manual", layout="centered")
st.title("📍 Obtén tu ubicación con un clic")

if st.button("📍 Obtener mi ubicación"):
    coords = st_javascript("""
        new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        value: {
                            lat: position.coords.latitude,
                            lon: position.coords.longitude
                        }
                    });
                },
                () => resolve({ value: null })
            );
        });
    """)

    if coords and coords.get("lat") and coords.get("lon"):
        lat = coords["lat"]
        lon = coords["lon"]
        st.success(f"✅ Coordenadas: Latitud {lat}, Longitud {lon}")

        mapa = folium.Map(location=[lat, lon], zoom_start=16)
        folium.Marker([lat, lon], tooltip="📍 Aquí estás").add_to(mapa)
        folium_static(mapa)
    else:
        st.error("❗ No se pudo obtener la ubicación. Asegúrate de permitir el acceso.")
