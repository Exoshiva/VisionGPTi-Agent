import os
import uvicorn

# WICHTIG: Setzt die Konfiguration, *bevor* die Chroma-App importiert wird.
# Dies teilt dem Server mit, wo er seine Datenbankdateien speichern und laden soll.
os.environ['CHROMA_PERSIST_DIRECTORY'] = './chroma_db'
os.environ['CHROMA_SERVER_HOST'] = '0.0.0.0'
os.environ['CHROMA_SERVER_HTTP_PORT'] = '8000'
os.environ['CHROMA_API_IMPL'] = 'local'

# Die FastAPI-App wird jetzt direkt aus dem korrekten Modul importiert
from chromadb.app import app

print("Starte ChromaDB UI Server auf http://localhost:8000 ...")
# Uvicorn wird angewiesen, die importierte 'app' zu starten
uvicorn.run(app)