import streamlit as st
from google import genai
from google.oauth2 import service_account
from PIL import Image
import io

st.set_page_config(page_title="Infalible Enterprise", page_icon="🏢")
st.title("🏢 Peritaje Profesional (Vertex AI)")

# --- CONFIGURACIÓN DE PUERTA EMPRESA ---
try:
    # Extraemos el JSON de los secrets
    creds_info = dict(st.secrets["gcp_service_account"])
    
    # Arreglamos el formato de la clave privada (el clásico error de los saltos de línea)
    creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
    
    # Creamos el cliente de Gemini especificando VERTEX AI
    client = genai.Client(
        vertexai=True,
        project=creds_info["project_id"],
        location="us-central1", # Cambia esto si tu proyecto está en otra región (ej: europe-west1)
        credentials=service_account.Credentials.from_service_account_info(creds_info)
    )
    st.sidebar.success(f"Conectado a Vertex: {creds_info['project_id']}")
except Exception as e:
    st.error(f"Error de conexión Vertex: {e}")
    st.stop()

# --- INTERFAZ ---
st.info("Sistema de peritaje bajo infraestructura de Google Cloud.")

col1, col2 = st.columns(2)
with col1:
    foto1 = st.file_uploader("Foto 1", type=['jpg', 'jpeg', 'png'])
with col2:
    foto2 = st.file_uploader("Foto 2", type=['jpg', 'jpeg', 'png'])

if foto1 and foto2:
    if st.button("🚀 REALIZAR TASACIÓN EMPRESARIAL"):
        try:
            with st.spinner("Vertex AI analizando..."):
                img1 = Image.open(foto1)
                img2 = Image.open(foto2)
                
                # Usamos el modelo estable de Vertex
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[
                        "Eres un tasador industrial. Analiza marca, modelo y estado de esta máquina basándote en las fotos.", 
                        img1, 
                        img2
                    ]
                )
                
                st.subheader("Informe Pericial:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Fallo en Vertex: {e}")
