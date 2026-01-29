import streamlit as st
from PIL import Image
import ia_engine  # Importamos tu nuevo módulo

# Configuración de Página
st.set_page_config(page_title="Infalible Vertex", page_icon="🏢", layout="centered")
st.title("🏢 Peritaje Profesional Vertex")

# 1. GESTIÓN DE CONEXIÓN
if "gcp_service_account" not in st.secrets:
    st.error("❌ Configura los Secrets en Streamlit Cloud.")
    st.stop()

# Usamos una variable de estado para no reconectar en cada clic
if "vertex_client" not in st.session_state:
    try:
        creds = dict(st.secrets["gcp_service_account"])
        st.session_state.vertex_client = ia_engine.conectar_vertex(creds)
        st.sidebar.success(f"✅ Conectado a {creds['project_id']}")
    except Exception as e:
        st.sidebar.error(f"❌ Error de conexión: {e}")
        st.stop()

# 2. INTERFAZ DE SUBIDA
st.write("Sube las imágenes para el peritaje técnico.")

col1, col2 = st.columns(2)
with col1:
    foto1 = st.file_uploader("Foto Frontal", type=['jpg', 'jpeg', 'png'], key="f1")
with col2:
    foto2 = st.file_uploader("Foto Detalle", type=['jpg', 'jpeg', 'png'], key="f2")

# 3. ACCIÓN
if foto1 and foto2:
    st.divider()
    if st.button("🚀 INICIAR TASACIÓN VERTEX"):
        try:
            with st.spinner("Analizando bajo protocolos de Google Cloud..."):
                img1 = Image.open(foto1)
                img2 = Image.open(foto2)
                
                # Llamamos al motor de IA
                informe = ia_engine.realizar_peritaje(
                    st.session_state.vertex_client, 
                    [img1, img2]
                )
                
                st.success("✅ Análisis Finalizado")
                st.markdown("### 📋 Informe de Tasación Profesional")
                st.markdown(informe)
                
        except Exception as e:
            st.error(f"❌ Error en el peritaje: {e}")

st.sidebar.divider()
st.sidebar.caption("v1.5 - Rama Desarrollo (Modular)")
