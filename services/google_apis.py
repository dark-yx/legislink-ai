# legislink-ai/services/google_apis.py

"""
Módulo para centralizar todas las interacciones con las APIs de Google.
Esto incluye Google Drive, Google Calendar, Vertex AI, etc.
"""

# Próximamente: Clases y funciones para interactuar con:
# - Google Drive API (subir, descargar, buscar archivos)
# - Vertex AI (búsqueda semántica, modelos generativos)
# - Google Calendar API (crear eventos, recordatorios)

import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from config.settings import settings
from google.cloud import aiplatform
import logging

SCOPES = ['https://www.googleapis.com/auth/drive']

def _get_google_creds():
    """Obtiene las credenciales de Google desde la cuenta de servicio."""
    credentials_path = settings.GOOGLE_APPLICATION_CREDENTIALS
    if not credentials_path or not os.path.exists(credentials_path):
        logging.error(f"Archivo de credenciales no encontrado en: {credentials_path}")
        return None
    
    return service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES)

def get_drive_service():
    """Autentica y devuelve un objeto de servicio de Google Drive."""
    creds = _get_google_creds()
    if not creds:
        return None
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(file_name: str, file_content: str, mimetype: str = 'text/plain'):
    """Sube un archivo a la carpeta especificada en Google Drive."""
    service = get_drive_service()
    if not service:
        return {"error": "No se pudo conectar con Google Drive."}
    
    folder_id = settings.GOOGLE_DRIVE_FOLDER_ID
    if not folder_id:
        return {"error": "El ID de la carpeta de Google Drive no está configurado."}
        
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    
    fh = io.BytesIO(file_content.encode('utf-8'))
    media = MediaIoBaseUpload(fh, mimetype=mimetype, resumable=True)
    
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        logging.info(f"Archivo '{file_name}' subido a Google Drive con ID: {file.get('id')}")
        return {"id": file.get('id'), "link": file.get('webViewLink')}
    except Exception as e:
        logging.error(f"Error al subir el archivo a Google Drive: {e}")
        return {"error": "Ocurrió un error durante la subida del archivo."}

# --- Vertex AI Search (Matching Engine) Functions ---
# (Mantener las funciones de Vertex AI si ya existen o añadirlas)

def get_vertex_ai_client():
    """Inicializa y devuelve el cliente de Vertex AI."""
    try:
        aiplatform.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)
        return aiplatform
    except Exception as e:
        logging.error(f"Error al inicializar Vertex AI: {e}")
        return None

def query_vector_search(index_endpoint_id: str, query_embedding: list, num_neighbors: int = 5):
    """Realiza una búsqueda de vecinos más cercanos en un endpoint de índice."""
    client = get_vertex_ai_client()
    if not client:
        return {"error": "No se pudo inicializar Vertex AI."}
    try:
        index_endpoint = client.MatchingEngineIndexEndpoint(index_endpoint_name=index_endpoint_id)
        response = index_endpoint.find_neighbors(
            queries=[query_embedding],
            num_neighbors=num_neighbors
        )
        return response
    except Exception as e:
        logging.error(f"Error al consultar Vector Search: {e}")
        return {"error": str(e)}

def upsert_to_index(index_id: str, datapoints: list):
    """Inserta o actualiza vectores de datos en un índice existente."""
    client = get_vertex_ai_client()
    if not client:
        return {"error": "No se pudo inicializar Vertex AI."}
    try:
        index = client.MatchingEngineIndex(index_name=index_id)
        index.upsert_datapoints(datapoints=datapoints)
        logging.info(f"Upsert de {len(datapoints)} datapoints al índice {index_id} exitoso.")
        return {"status": "success"}
    except Exception as e:
        logging.error(f"Error al hacer upsert en el índice: {e}")
        return {"error": str(e)}
