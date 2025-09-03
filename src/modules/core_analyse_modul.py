import chromadb

# Dies ist eine Platzhalter-Importanweisung.
# In der finalen Version würden wir die gpt-Funktion aus dem Haupt-Agenten importieren,
# aber für die modulare Struktur definieren wir sie hier vorerst separat.
from vision_gpti_agent import gpt, COLLECTION_NAME, DB_PATH

def analyze_and_structure_knowledge(topic: str) -> str:
    """
    Führt eine tiefgreifende Analyse des gesamten in der ChromaDB gespeicherten Wissens
    durch und erstellt eine strukturierte Gliederung zu einem bestimmten Thema.

    Args:
        topic (str): Das Hauptthema, auf das sich die Gliederung konzentrieren soll.

    Returns:
        str: Die fertig formatierte, strukturierte Gliederung als Text.
    """
    print(f"[Core-Analyse] Starte die Analyse für das Thema: '{topic}'")

    # 1. Sammle alle relevanten Dokumente aus dem Gedächtnis
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_collection(name=COLLECTION_NAME)
        
        # Hole eine große Menge an Dokumenten, um einen guten Überblick zu bekommen
        # Wir durchsuchen die Datenbank nach dem übergeordneten Thema.
        results = collection.query(
            query_texts=[topic],
            n_results=500  # Fordere eine hohe Anzahl von Dokumenten an
        )
        
        knowledge_base = "\n\n---\n\n".join(results['documents'][0])
        
        if not knowledge_base:
            return "[Core-Analyse] FEHLER: Konnte kein Wissen zu diesem Thema im Gedächtnis finden."
            
        print(f"[Core-Analyse] {len(results['documents'][0])} relevante Dokumente aus dem Gedächtnis geladen.")

    except Exception as e:
        return f"[Core-Analyse] FEHLER: Konnte nicht auf das Gedächtnis zugreifen. Grund: {e}"

    # 2. Erstelle einen detaillierten Befehl (Prompt) für das LLM
    structuring_prompt = f"""
    Basierend auf der folgenden umfangreichen Wissensbasis, die aus meinen persönlichen Konversationen und Notizen besteht, erstelle eine detaillierte, hierarchische und gut strukturierte Gliederung zum Thema "{topic}".

    Die Gliederung sollte die wichtigsten Konzepte, wiederkehrende Themen, Schlüsselentscheidungen und die Entwicklung der Ideen klar darstellen. Verwende Markdown für die Formatierung (z.B. mit #, ##, ###, -).

    --- WISSENSBASIS ---
    {knowledge_base}
    --- ENDE WISSENSBASIS ---

    Erstelle jetzt die finale, strukturierte Gliederung:
    """

    # 3. Rufe das LLM auf, um die Gliederung zu erstellen
    print("[Core-Analyse] Das LLM wird nun die Gliederung erstellen. Dies kann einen Moment dauern...")
    final_structure = gpt(structuring_prompt, system_prompt="Du bist ein hochintelligenter Analyse-Agent, der darauf spezialisiert ist, unstrukturierte Informationen zu synthetisieren und in klaren Gliederungen darzustellen.")
    
    print("[Core-Analyse] Analyse abgeschlossen.")
    return final_structure

if __name__ == '__main__':
    # Dies ist ein Beispiel, wie das Modul direkt getestet werden kann
    print("Starte Testlauf für das Core-Analyse-Modul...")
    # Definiere das Hauptthema deiner 20.000 Seiten
    haupt_thema = "Die Entwicklung des Genesis SML-Ökosystems und seiner Kernphilosophie"
    
    struktur = analyze_and_structure_knowledge(haupt_thema)
    
    print("\n" + "="*50)
    print("FINALE ERSTELLTE GLIEDERUNG")
    print("="*50 + "\n")
    print(struktur)
    
    # Speichere das Ergebnis in einer Datei
    with open("analyse_ergebnis.md", "w", encoding="utf-8") as f:
        f.write(struktur)
    print("\nDie Gliederung wurde in 'analyse_ergebnis.md' gespeichert.")