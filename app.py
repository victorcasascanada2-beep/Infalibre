import streamlit as st
from google import genai 
from google.oauth2 import service_account
from PIL import Image
import io

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Infalible Vertex", page_icon="🏢", layout="centered")
st.title("🏢 Peritaje Profesional Agrícola Noroeste")

# 2. CONEXIÓN EMPRESARIAL (ÚNICA Y LIMPIA)
@st.cache_resource # Para no reconectar en cada click
def inicializar_cliente():
    try:
        if "gcp_service_account" not in st.secrets:
            st.error("❌ Faltan credenciales en Secrets")
            st.stop()

        creds_info = dict(st.secrets["gcp_service_account"])
        
        # Limpieza de llave privada
        raw_key = str(creds_info.get("private_key", ""))
        clean_key = raw_key.strip().strip('"').strip("'").replace("\\n", "\n")
        creds_info["private_key"] = clean_key
        
        google_creds = service_account.Credentials.from_service_account_info(
            creds_info, 
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        
        # Inicialización del cliente Vertex AI
        client = genai.Client(
            vertexai=True,
            project=creds_info.get("project_id"),
            location="us-central1",
            credentials=google_creds
        )
        return client, creds_info.get('project_id')
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")
        st.stop()

client, project_id = inicializar_cliente()
st.sidebar.success(f"✅ Sistema Activo: {project_id}")

# 3. INTERFAZ DE USUARIO
st.write("Sube las imágenes para realizar la tasación con búsqueda real en Europa.")

col1, col2 = st.columns(2)
with col1:
    foto1 = st.file_uploader("Foto Frontal", type=['jpg', 'jpeg', 'png'])
with col2:
    foto2 = st.file_uploader("Foto Detalle / Horas", type=['jpg', 'jpeg', 'png'])

if foto1 and foto2:
    st.divider()
    if st.button("🚀 INICIAR TASACIÓN PROFESIONAL"):
        try:
            with st.spinner("Buscando en Agriaffaires, Mascus y analizando fotos..."):
                # Procesamiento de imágenes
                img1 = Image.open(foto1)
                img2 = Image.open(foto2)
                
                # Prompt con instrucciones de búsqueda real (Igual a la versión Free)
                prompt = """
                ACTÚA COMO RESPONSABLE DE USADOS DE AGRÍCOLA NOROESTE.
                1. IDENTIFICACIÓN: Analiza las fotos y confirma marca, modelo y horas.
                2. BÚSQUEDA REAL: Utiliza Google Search para encontrar al menos 10 anuncios reales de este modelo en Europa (Mascus, Agriaffaires, Tractorpool).
                3. TABLA DE MERCADO: Genera una tabla con: Modelo, Año, Horas, Precio y Portal.
                4. VALORACIÓN: Calcula el Precio de Venta (media de mercado) y el Precio de Compra (-15%).
                5. ESTADO: Compara visualmente el tractor de las fotos con los encontrados.
                
                Responde directamente con la tabla y la valoración. Prohibido avisos legales o introducciones.
                """

                # LLAMADA CLAVE: Usamos el modelo estable y ACTIVAMOS GROUNDING
                # Esto es lo que hace que funcione como la versión gratuita
                response = client.models.generate_content(
                    model="gemini-1.5-flash", # El nombre estable que funciona con herramientas
                    contents=[prompt, img1, img2],
                    config={
                        "tools": [{"google_search": {}}], # AQUÍ ESTÁ EL TRUCO
                        "temperature": 0.0
                    }
                )
                
                st.success("✅ Análisis Finalizado")
                st.markdown(response.text)
                
                # Botón de descarga del HTML (Simulado)
                st.download_button("Descargar Informe HTML", response.text, "tasacion.html", "text/html")
                
        except Exception as error_ia:
            st.error(f"❌ Error durante el análisis")
            st.warning(f"Detalle: {str(error_ia)}")
