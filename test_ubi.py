import streamlit as st
from streamlit_javascript import st_javascript

st.set_page_config(page_title="Mis Coordenadas GPS", layout="centered")
st.title("📍 Obtén tus coordenadas GPS en tiempo real")

# Obtener coordenadas desde el navegador (construido correctamente)
coords = st_javascript("""
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

# Mostrar coordenadas si existen
if coords and "lat" in coords and "lon" in coords:
    st.success(f"✅ Coordenadas detectadas:")
    st.code(f"Latitud: {coords['lat']}\nLongitud: {coords['lon']}")
else:
    st.warning("Activa los permisos de ubicación para continuar.")
