import chromadb
import pprint

# Pfad zu deiner Datenbank
DB_PATH = "./chroma_db"
COLLECTION_NAME = "agi-agent-local-memory"

print(f"Verbinde mit der ChromaDB im Verzeichnis: {DB_PATH}")

# Verbinde dich mit der existierenden, persistenten Datenbank
client = chromadb.PersistentClient(path=DB_PATH)

try:
    # Hole die Collection, die der Agent benutzt
    collection = client.get_collection(name=COLLECTION_NAME)

    # Hole ALLE Einträge aus der Collection
    # Die .get()-Methode ohne Argumente holt alles
    results = collection.get(include=["metadatas", "documents"])

    count = len(results['ids'])
    print(f"\nInspektion der Collection '{COLLECTION_NAME}'...")
    print(f"Insgesamt {count} Einträge gefunden.")
    print("-" * 70)

    # Gehe durch alle Einträge und gib sie formatiert aus
    for i in range(count):
        metadata = results['metadatas'][i]
        document = results['documents'][i]

        print(f"Eintrag #{i+1}")
        print(f"Metadaten: {pprint.pformat(metadata)}")
        print("Dokument-Inhalt:")
        # Fügt eine Einrückung für bessere Lesbarkeit hinzu
        indented_document = "\n".join([f"  {line}" for line in document.split('\n')])
        print(indented_document)
        print("-" * 70)

except ValueError:
    print(f"\n[FEHLER] Die Collection '{COLLECTION_NAME}' wurde nicht gefunden.")
    print("Stelle sicher, dass der Agent bereits gelaufen ist und Daten gespeichert hat.")
except Exception as e:
    print(f"\nEin unerwarteter Fehler ist aufgetreten: {e}")