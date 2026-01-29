import streamlit as st
from google import genai
from google.oauth2 import service_account
from PIL import Image
import io
import google.generativeai as genai_v2 # Usamos el motor directo
# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Infalible Vertex", page_icon="🏢", layout="centered")
st.title("🏢 Peritaje Profesional Vertex")

# 2. CONEXIÓN EMPRESARIAL (VERSIÓN BLINDADA)

# 2. CONEXIÓN EMPRESARIAL DIRECTA
try:
    creds_info = dict(st.secrets["gcp_service_account"])
    
    # Limpieza de llave
    p_key = creds_info["private_key"].strip().replace("\\n", "\n")
    
    # Autenticación directa por API Key o credenciales simplificadas
    # Para Vertex AI Studio a veces es más fácil usar la API KEY si la tienes, 
    # pero sigamos con tu service account:
    
    certificaciones = service_account.Credentials.from_service_account_info(
        creds_info, 
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    
    # Cambiamos a la inicialización estándar que no requiere mTLS (el certificado que te pide)
    client = genai.Client(
        vertexai=True,
        project=creds_info["project_id"],
        location="us-central1",
        credentials=certificaciones
    )
    
    st.sidebar.success(f"✅ Sistema Activo")
    
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()
    
    # Inicializamos el cliente de IA apuntando a Vertex
    client = genai.Client(
        vertexai=True,
        project=creds_info.get("project_id"),
        location="us-central1",
        credentials=google_creds
    )
    
    st.sidebar.success(f"✅ Conectado a GCP: {creds_info.get('project_id')}")
    
except Exception as error_conexion:
    st.error("❌ Error Crítico en la conexión con Google Cloud")
    st.warning(f"Diagnóstico técnico: {str(error_conexion)}")
    st.info("💡 Verifica que el ID del proyecto en la consola sea igual al de tus Secrets.")
    st.stop()

# 3. INTERFAZ DE USUARIO
st.write("Sube las imágenes para que la IA de empresa realice el peritaje.")

col1, col2 = st.columns(2)
with col1:
    foto1 = st.file_uploader("Foto Frontal", type=['jpg', 'jpeg', 'png'])
with col2:
    foto2 = st.file_uploader("Foto Detalle", type=['jpg', 'jpeg', 'png'])

if foto1 and foto2:
    st.divider()
    if st.button("🚀 INICIAR TASACIÓN VERTEX"):
        try:
            with st.spinner("Analizando bajo protocolos de Google Cloud..."):
                # Cargamos las imágenes
                img1 = Image.open(foto1)
                img2 = Image.open(foto2)
                
                # El Prompt estructurado para maquinaria agrícola
                prompt = """
                Actúa como un tasador experto de maquinaria agrícola. 
                Analiza estas fotos y genera un informe detallado con:
                1. MARCA Y MODELO: Identificación más probable.
                2. ESTADO VISUAL: Evaluación de chapa, neumáticos, motor (si es visible) y mantenimiento.
                3. VALOR ESTIMADO: Rango de precio en el mercado actual (Europa).
                Responde de forma profesional, estructurada y en español.
                """
                
                # --- CAMBIO EN LA PARTE FINAL DEL CÓDIGO ---

                # --- CAMBIO EN LA PARTE FINAL DEL CÓDIGO ---
                
                # Sustituye la línea antigua por esta:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",  # <--- Este es el modelo que tienes activo
                    contents=[prompt, img1, img2]
                )
                
                st.success("✅ Análisis Finalizado")
                st.markdown("### 📋 Informe de Tasación Profesional")
                st.markdown(response.text)
                
        except Exception as error_ia:
            st.error(f"❌ Error durante el análisis de la IA")
            st.warning(f"Detalle: {str(error_ia)}")
            st.info("Revisa si la cuenta de servicio tiene el rol 'Usuario de Vertex AI' en Google Cloud.")

# Pie de página
st.sidebar.divider()
st.sidebar.caption("Peritaje Profesional Vertex v1.2")
