import streamlit as st
from google import genai
from PIL import Image
import io

# 1. Configuración de página
st.set_page_config(page_title="Infalible V1.0", page_icon="🚜")
st.title("🚜 Peritaje Infalible")

# 2. Inicialización del Cliente (Puerta AI Studio)
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    st.sidebar.success("Conectado a Gemini")
except Exception as e:
    st.error(f"Error configurando la llave: {e}")
    st.stop()

# 3. Interfaz de subida
st.subheader("Sube las 2 fotos para tasar")
foto1 = st.file_uploader("Foto Frontal", type=['jpg', 'jpeg', 'png'], key="f1")
foto2 = st.file_uploader("Foto Detalle / Motor", type=['jpg', 'jpeg', 'png'], key="f2")

if foto1 and foto2:
    col1, col2 = st.columns(2)
    with col1: st.image(foto1, caption="Foto 1", width=250)
    with col2: st.image(foto2, caption="Foto 2", width=250)
    
    # 4. Botón de ejecución
    if st.button("🚀 REALIZAR TASACIÓN"):
        try:
            with st.spinner("Analizando imágenes..."):
                # Convertimos las fotos a formato PIL para Gemini
                img1 = Image.open(foto1)
                img2 = Image.open(foto2)
                
                prompt = "Analiza estas dos fotos de maquinaria agrícola y propón un precio de mercado basado en su estado visual."
                
                # Llamada a la IA
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[prompt, img1, img2]
                )
                
                st.divider()
                st.markdown("### Resultado de la Tasación:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"❌ La IA ha fallado: {e}")
