import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import folium_static
import requests

# Configuración general
st.set_page_config(page_title="Ubicación y clínicas", layout="centered")
st.title("📍 Encuentra clínicas, hospitales o laboratorios cerca de ti")

# Botón para actualizar ubicación
if st.button("🔄 Actualizar mi ubicación"):
    st.session_state["ubicacion"] = streamlit_geolocation()

# Recuperar ubicación guardada
location = st.session_state.get("ubicacion", None)

if location and location.get("latitude") and location.get("longitude"):
    lat = location["latitude"]
    lon = location["longitude"]
    st.success(f"✅ Ubicación detectada:\nLatitud: {lat}\nLongitud: {lon}")

    # Mapa base
    mapa = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], tooltip="📍 Tú", popup="Tu ubicación", icon=folium.Icon(color="blue")).add_to(mapa)

    # Consulta a Google Places
    API_KEY = st.secrets["google_places_key"]
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lon}&rankby=distance&keyword=hospital+clinica+laboratorio&key={API_KEY}"
    )
    response = requests.get(url)
    lugares = response.json().get("results", [])

    if lugares:
        for lugar in lugares:
            nombre = lugar.get("name", "Sin nombre")
            direccion = lugar.get("vicinity", "")
            ubicacion = lugar["geometry"]["location"]

            folium.Marker(
                [ubicacion["lat"], ubicacion["lng"]],
                popup=f"{nombre}\n{direccion}",
                tooltip=nombre,
                icon=folium.Icon(color="green", icon="plus-sign")
            ).add_to(mapa)

    else:
        st.info("No se encontraron lugares cercanos con esas características.")

    # Mostrar mapa final
    folium_static(mapa)

else:
    st.warning("Presiona el botón 'Actualizar mi ubicación' para comenzar.")
