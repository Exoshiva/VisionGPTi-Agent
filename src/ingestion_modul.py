import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

# ======= KONFIGURATION =======
# Stelle sicher, dass diese Werte mit deinem Haupt-Agenten übereinstimmen
DB_PATH = "./chroma_db"
COLLECTION_NAME = "agi-agent-local-memory"
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

# Der Dateiname deiner Konversations-Daten
JSONL_FILE_PATH = "konversationen.jsonl" # WICHTIG: Passe diesen Namen bei Bedarf an

def initialize_components():
    """Initialisiert DB-Client, Collection und Embedding-Modell."""
    print("Initialisiere Komponenten...")
    db_client = chromadb.PersistentClient(path=DB_PATH)
    collection = db_client.get_or_create_collection(name=COLLECTION_NAME)
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print("Komponenten initialisiert.")
    return collection, embedding_model

def process_jsonl_file(collection, embedding_model, filepath: str):
    """
    Liest eine JSONL-Datei, verarbeitet jede Zeile als separate Konversation
    und fügt sie als Dokument zur ChromaDB hinzu.
    """
    if not os.path.exists(filepath):
        print(f"[FEHLER] Die Datei '{filepath}' wurde nicht gefunden.")
        return

    print(f"Beginne mit der Verarbeitung der Datei: {filepath}")
    
    # Wir sammeln die Daten in Stapeln (Batches), um die Effizienz zu erhöhen
    batch_size = 100
    documents_batch = []
    metadatas_batch = []
    ids_batch = []
    line_number = 0

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line_number += 1
            try:
                # Lade die JSON-Daten aus der Zeile
                data = json.loads(line)

                # Extrahiere die relevanten Konversations-Teile
                # ANNAHME: Deine JSONL-Datei hat Schlüssel wie 'user', 'assistant', 'timestamp'
                # WICHTIG: Passe diese Logik an die exakte Struktur deiner JSONL-Datei an!
                user_query = data.get('user', '')
                assistant_response = data.get('assistant', '')
                timestamp = data.get('timestamp', 'unbekannt')
                
                # Kombiniere die Teile zu einem einzigen Text-Dokument
                full_conversation = f"Nutzerfrage: {user_query}\nAntwort des Agenten: {assistant_response}"
                
                # Füge das Dokument und die Metadaten zum aktuellen Stapel hinzu
                documents_batch.append(full_conversation)
                metadatas_batch.append({"source": filepath, "line": line_number, "timestamp": timestamp})
                ids_batch.append(f"conv-{line_number}")

                # Wenn der Stapel voll ist, verarbeite ihn
                if len(documents_batch) >= batch_size:
                    _process_batch(collection, embedding_model, documents_batch, metadatas_batch, ids_batch)
                    # Setze die Stapel zurück
                    documents_batch, metadatas_batch, ids_batch = [], [], []

            except json.JSONDecodeError:
                print(f"[WARNUNG] Zeile {line_number} konnte nicht als JSON verarbeitet werden. Überspringe...")
                continue
    
    # Verarbeite den letzten, möglicherweise unvollständigen Stapel
    if documents_batch:
        _process_batch(collection, embedding_model, documents_batch, metadatas_batch, ids_batch)

    print("\nVerarbeitung der JSONL-Datei abgeschlossen.")

def _process_batch(collection, embedding_model, documents, metadatas, ids):
    """Vektorisiert einen Stapel von Dokumenten und fügt sie der DB hinzu."""
    print(f"Verarbeite Stapel mit {len(documents)} Dokumenten...")
    embeddings = embedding_model.encode(documents, convert_to_tensor=False).tolist()
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    print(f"Stapel erfolgreich zum Gedächtnis hinzugefügt.")

if __name__ == "__main__":
    # Stelle sicher, dass deine Konversationsdatei existiert
    if not os.path.exists(JSONL_FILE_PATH):
        print(f"[FEHLER] Bitte erstelle die Datei '{JSONL_FILE_PATH}' und füge deine Konversationsdaten ein.")
    else:
        collection, model = initialize_components()
        process_jsonl_file(collection, model, JSONL_FILE_PATH)
        print(f"\nIngestion abgeschlossen. Das Gedächtnis enthält jetzt insgesamt {collection.count()} Wissens-Dokumente.")