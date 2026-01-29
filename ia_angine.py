from google import genai
from google.oauth2 import service_account

def conectar_vertex(creds_dict):
    """Establece la conexión con Vertex AI usando las credenciales de los secrets."""
    # Limpieza de llave privada
    raw_key = str(creds_dict.get("private_key", ""))
    clean_key = raw_key.strip().strip('"').strip("'").replace("\\n", "\n")
    creds_dict["private_key"] = clean_key
    
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    
    google_creds = service_account.Credentials.from_service_account_info(
        creds_dict, 
        scopes=scopes
    )
    
    client = genai.Client(
        vertexai=True,
        project=creds_dict.get("project_id"),
        location="us-central1",
        credentials=google_creds
    )
    return client

def realizar_peritaje(client, lista_imagenes):
    """Envía las imágenes a Gemini y devuelve el informe."""
    prompt = """
    Actúa como un tasador experto de maquinaria agrícola. 
    Analiza estas fotos y genera un informe detallado con:
    1. MARCA Y MODELO: Identificación más probable.
    2. ESTADO VISUAL: Evaluación de chapa, neumáticos, motor y mantenimiento.
    3. VALOR ESTIMADO: Rango de precio en el mercado actual (Europa).
    Responde de forma profesional, estructurada y en español.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[prompt] + lista_imagenes
    )
    return response.text
