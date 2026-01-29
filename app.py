import streamlit as st
from google import genai
from google.oauth2 import service_account
from PIL import Image
import io

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Infalible Vertex", page_icon="🏢", layout="centered")
st.title("🏢 Peritaje Profesional Vertex")

# 2. CONEXIÓN EMPRESARIAL (LIMPIEZA DE LLAVE)
try:
    # Cargamos el bloque de la cuenta de servicio de los secrets
    creds_info = dict(st.secrets["gcp_service_account"])
    
    # --- PROCESO DE LIMPIEZA DE LLAVE PRIVADA ---
    # Esto elimina comillas extra, espacios y arregla los saltos de línea (\n)
    raw_key = creds_info["private_key"]
    
    # Quitamos espacios y comillas accidentales al principio y al final
    raw_key = raw_key.strip().strip('"').strip("'")
    
    # Convertimos los \n de texto en saltos de línea reales
    clean_key = raw_key.replace("\\n", "\n")
    
    # Reasignamos la llave limpia
    creds_info["private_key"] = clean_key
    
    # Inicializamos el cliente apuntando a VERTEX AI
    client = genai.Client(
        vertexai=True,
        project=creds_info["project_id"],
        location="us-central1",
        credentials=service_account.Credentials.from_service_account_info(creds_info)
    )
    st.sidebar.success(f"✅ Conectado a GCP: {creds_info['project_id']}")
    
except Exception as e:
    st.error("❌ Error en la llave o conexión")
    st.info(f"Detalle técnico: {e}")
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
                # Abrimos las fotos
                img1 = Image.open(foto1)
                img2 = Image.open(foto2)
                
                # EL PROMPT PROFESIONAL
                prompt = """
                Actúa como un tasador experto de maquinaria agrícola. 
                Analiza estas fotos y genera un informe con:
                1. MARCA Y MODELO: Identificación más probable.
                2. ESTADO VISUAL: Evaluación de chapa, neumáticos y mantenimiento.
                3. VALOR ESTIMADO: Rango de precio en el mercado actual (Europa).
                Responde de forma profesional y estructurada.
                """
                
                # Llamada a Gemini 1.5 Flash (Rápido y eficiente)
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[prompt, img1, img2]
                )
                
                st.success("Análisis Finalizado")
                st.markdown("### 📋 Informe de Tasación")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error en la IA: {e}")
            st.info("Revisa si tienes activada la API de Vertex AI en tu consola de Google Cloud.")
