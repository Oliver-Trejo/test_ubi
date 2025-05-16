import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import folium
from folium.features import CustomIcon
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

    # Marcar ubicación del usuario
    folium.Marker(
        [lat, lon],
        tooltip="📍 Tú",
        popup="Tu ubicación",
        icon=folium.Icon(color="blue")
    ).add_to(mapa)

    # --- CONSULTA A GOOGLE PLACES API ---
    API_KEY = st.secrets["google_places_key"]
    tipo_iconos = {
        "hospital": "https://cdn-icons-png.flaticon.com/512/1484/1484848.png",
        "clinic": "https://cdn-icons-png.flaticon.com/512/2967/2967350.png",
        "laboratory": "https://cdn-icons-png.flaticon.com/512/3343/3343841.png"
    }

    for tipo, icon_url in tipo_iconos.items():
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

            # Crear ícono personalizado más grande
            icono_personalizado = CustomIcon(
                icon_image=icon_url,
                icon_size=(40, 40)
            )

            folium.Marker(
                [ubicacion["lat"], ubicacion["lng"]],
                popup=f"{nombre}\n{direccion}",
                tooltip=nombre,
                icon=icono_personalizado
            ).add_to(mapa)

    # Mostrar el mapa con todos los marcadores
    folium_static(mapa)

else:
    st.warning("⚠️ Presiona el botón para obtener tu ubicación.")
