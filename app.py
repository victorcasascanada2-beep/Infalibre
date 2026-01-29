# 2. CONEXIÓN EMPRESARIAL (LIMPIEZA DE LLAVE)
try:
    # Cargamos el bloque de la cuenta de servicio de los secrets
    creds_info = dict(st.secrets["gcp_service_account"])
    
    # --- PROCESO DE LIMPIEZA DE LLAVE PRIVADA ---
    raw_key = creds_info["private_key"]
    raw_key = raw_key.strip().strip('"').strip("'")
    clean_key = raw_key.replace("\\n", "\n")
    creds_info["private_key"] = clean_key
    
    # --- DEFINICIÓN DE SCOPES (LA SOLUCIÓN AL ERROR) ---
    # Esto le dice a Google que el bot tiene permiso para usar servicios de Cloud (Vertex AI)
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    
    # Creamos el objeto de credenciales con el scope incluido
    google_creds = service_account.Credentials.from_service_account_info(
        creds_info, 
        scopes=scopes
    )
    
    # Inicializamos el cliente apuntando a VERTEX AI
    client = genai.Client(
        vertexai=True,
        project=creds_info["project_id"],
        location="us-central1",
        credentials=google_creds
    )
    
    st.sidebar.success(f"✅ Conectado a GCP: {creds_info['project_id']}")
    
except Exception as e:
    st.error("❌ Error en la llave o conexión")
    st.info(f"Detalle técnico: {e}")
    st.stop()
