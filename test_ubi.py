import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import folium_static
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="🧭 Clínicas cercanas", layout="centered")
st.title("📍 Encuentra hospitales, clínicas y laboratorios cerca de ti")

# --- OBTENER UBICACIÓN ---
location = streamlit_geolocation()

if location and location.get("latitude") and location.get("longitude"):
    lat = location["latitude"]
    lon = location["longitude"]
    st.success(f"✅ Coordenadas detectadas:\nLatitud: {lat}\nLongitud: {lon}")

    # Crear mapa centrado
    mapa = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], tooltip="📍 Tú", popup="Tu ubicación", icon=folium.Icon(color="blue")).add_to(mapa)

    # --- CONSULTA A GOOGLE PLACES API ---
    API_KEY = st.secrets["google_places_key"]
    tipos = ["hospital", "clinic", "laboratory"]

    for tipo in tipos:
        url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
            f"location={lat},{lon}&radius=3000&type={tipo}&key={API_KEY}"
        )
        respuesta = requests.get(url)
        resultados = respuesta.json().get("results", [])

        for lugar in resultados:
            nombre = lugar.get("name", "Sin nombre")
            ubicacion = lugar["geometry"]["location"]
            direccion = lugar.get("vicinity", "")

            folium.Marker(
                [ubicacion["lat"], ubicacion["lng"]],
                popup=f"{nombre}\n{direccion}",
                tooltip=nombre,
                icon=folium.Icon(color="green", icon="plus-sign")
            ).add_to(mapa)

    # Mostrar mapa
    folium_static(mapa)

else:
    st.warning("⚠️ Presiona el botón para obtener tu ubicación.")
