# ==============================================================================
# VisionGPTi Agent - Souveränes KI-Ökosystem
# Version: 2.8
# Letzte Änderung: 03. September 2025
# Copyright © 2025 Lars Patzenbein / Exoshiva / ΞXΘLΛB
# ==============================================================================

import os
import sys
import uuid
import time
import threading
import random
import numpy as np
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import warnings
import argparse

# --- DYNAMISCHE PFAD-ANPASSUNG ---
# Stellt sicher, dass das Skript Module und Daten aus dem Projekt-Root findet.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# ======= LOKALE KI-, DB- & WEB-ABHÄNGIGKEITEN =======
from openai import OpenAI
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import CLIPProcessor, CLIPModel
from swiplserver import PrologMQI
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

# NLTK-Daten einmalig herunterladen
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

# ======= KONFIGURATION (LOKAL) =======
local_llm_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
LLM_MODEL = "gemma:2b"

# --- Pfade werden jetzt relativ zum Projekt-Root gebildet ---
DB_PATH = os.path.join(ROOT_DIR, "data", "chroma_db")
TOPIC_FILE_PATH = os.path.join(ROOT_DIR, "data", "input", "themen_liste.txt")
RESULTS_DIR = os.path.join(ROOT_DIR, "data", "output")


db_client = chromadb.PersistentClient(path=DB_PATH)
collection = db_client.get_or_create_collection(name="agi-agent-local-memory")

EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2' 
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
EMBEDDING_DIMENSION = embedding_model.get_sentence_embedding_dimension()

warnings.filterwarnings("ignore", message=".*`label` is deprecated.*")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# ======= AGENTEN-KONFIGURATION =======
AGENT_NAME = "VisionGPTi"
AGENT_VERSION = "2.8" 

INITIAL_OBJECTIVE = "Analysiere die neuesten Trends bei KI-gestützten Cyberangriffen und erstelle eine Übersicht der Bedrohungslandschaft."
EUREKA_GOAL = "Formuliere eine fundierte Hypothese über die wahrscheinlichste zukünftige Entwicklung von KI-Angriffstools in den nächsten 12-18 Monaten."
ETHICAL_CONSTRAINTS = "Outputs must be safe, ethical, and avoid harm or misinformation. Be helpful and harmless."

# ======= HELFERFUNKTIONEN, KLASSEN & MODULE =======

def get_embedding(text: str) -> List[float]:
    if not text or not isinstance(text, str):
        return [0.0] * EMBEDDING_DIMENSION
    embedding = embedding_model.encode(text, convert_to_tensor=False)
    return embedding.tolist()

class EpisodicMemory:
    def __init__(self, max_size: int = 100):
        self.events: List[Dict] = []
        self.max_size = max_size
    def add_event(self, event_content: str, timestamp: float):
        event_vector = get_embedding(event_content)
        self.events.append({"content": event_content, "vector": event_vector, "timestamp": timestamp})
        if len(self.events) > self.max_size:
            self.events.pop(0)
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        if not self.events: return []
        query_vec = np.array(get_embedding(query))
        event_vectors = np.array([e['vector'] for e in self.events])
        similarities = np.dot(event_vectors, query_vec) / (np.linalg.norm(event_vectors, axis=1) * np.linalg.norm(query_vec))
        sorted_indices = np.argsort(np.nan_to_num(similarities))[-top_k:][::-1]
        return [self.events[i] for i in sorted_indices]

def gpt(query: str, system_prompt: str = "You are an autonomous AI agent.") -> str:
    try:
        response = local_llm_client.chat.completions.create(model=LLM_MODEL, messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": query}])
        return response.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] LLM call failed: {e}")
        return "Error: Could not get a response from the local LLM."

def _clean_search_query(query: str) -> str:
    query = query.replace("**", "").replace("*", "").replace(":", "").replace('"', "").strip()
    return query

def search_web(query: str, max_results: int = 3) -> list[dict]:
    print(f"[Web-Recherche] Suche nach: '{query}'...")
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
        print(f"[Web-Recherche] {len(results)} Ergebnisse gefunden.")
        return results
    except Exception as e:
        print(f"[ERROR] Websuche fehlgeschlagen: {e}")
        return []

def scrape_url_content(url: str) -> str:
    print(f"[Web-Recherche] Lade Inhalt von: {url}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for script_or_style in soup(["script", "style"]): script_or_style.decompose()
        text = '\n'.join(chunk for chunk in (phrase.strip() for line in (line.strip() for line in soup.get_text().splitlines()) for phrase in line.split("  ")) if chunk)
        return text
    except requests.RequestException as e:
        print(f"[ERROR] Fehler beim Abrufen der URL {url}: {e}")
        return ""

def store_memory(text: str, metadata: Dict = None):
    vector = get_embedding(text)
    doc_id = str(uuid.uuid4())
    if metadata is None: metadata = {}
    collection.add(ids=[doc_id], embeddings=[vector], documents=[text], metadatas=[metadata])

def retrieve_memory(query: str, top_k: int = 10) -> List[str]:
    if not query: return []
    vector = get_embedding(query)
    results = collection.query(query_embeddings=[vector], n_results=top_k, include=['documents'])
    return results['documents'][0] if results['documents'] else []

# ... (Hier könnten weitere Kernfunktionen wie detect_contradictions etc. stehen)

# ======= KERN-PROZESS-FUNKTION =======
def process_prompt(prompt: str, shared_lock: threading.Lock, episodic_memory: EpisodicMemory) -> str:
    with shared_lock:
        memories = retrieve_memory(prompt, top_k=5)
        context = "\n".join(memories)
        decision_prompt = f"User prompt: \"{prompt}\"\nMy existing knowledge: \"{context if context else 'None.'}\"\nIs my existing knowledge sufficient to give a detailed, specific answer, or do I need to search the web? Answer YES or NO."
        decision = gpt(decision_prompt, system_prompt="You are a decision-making component.").strip().upper()
        web_context = ""
        if "YES" in decision:
            print("[INFO] Entscheidung getroffen: Web-Recherche wird gestartet.")
            clean_prompt = _clean_search_query(prompt)
            search_results = search_web(clean_prompt)
            if search_results:
                content_list = []
                for result in search_results:
                    scraped_content = scrape_url_content(result['href'])
                    if scraped_content:
                        memory_to_store = f"Source: {result['href']}\nContent: {scraped_content[:1500]}..."
                        print(f"[INFO] Neue Information von '{result['href']}' wird dem Gedächtnis hinzugefügt.")
                        store_memory(memory_to_store, {"type": "web_research", "source": result['href']})
                        content_list.append(memory_to_store)
                web_context = "\n\n".join(content_list)
        else:
            print("[INFO] Entscheidung getroffen: Keine Web-Recherche, internes Wissen ist ausreichend.")
        
        full_prompt = f"Objective: {prompt}\n\nMy internal knowledge:\n{context}\n\nFresh information from web research:\n{web_context if web_context else 'None.'}\n\nProvide a detailed, synthesized answer."
        answer = gpt(full_prompt)
        
        # ... (Alignment Check könnte hier stehen)
        
        memory_content = f"Prompt: {prompt}\nAnswer: {answer}"
        store_memory(memory_content, {"type": "insight"})
        episodic_memory.add_event(memory_content, time.time())
        return answer

# ======= BETRIEBSMODI =======
def self_improving_loop(max_cycles: int = 10, max_branches: int = 3):
    # Diese Funktion ist für zukünftige Nutzung reserviert und müsste wieder voll ausprogrammiert werden.
    print("Autonomer Modus ist aktuell in Überarbeitung.")
    pass

def task_driven_research_loop(topic_file: str = TOPIC_FILE_PATH):
    if not os.path.exists(topic_file):
        print(f"[FEHLER] Die Themenliste '{topic_file}' wurde nicht gefunden.")
        # Erstelle eine Beispiel-Datei, wenn sie fehlt
        with open(topic_file, "w", encoding="utf-8") as f:
            f.write("Was ist das Genesis SML-Ökosystem?\n")
        print(f"Eine Beispiel-Themenliste wurde unter '{topic_file}' erstellt. Bitte befülle sie.")
        return
        
    with open(topic_file, 'r', encoding='utf-8') as f:
        topics = [line.strip() for line in f if line.strip()]
        
    print(f"Starte aufgaben-gesteuerte Recherche für {len(topics)} Themen.")
    
    lock = threading.Lock()
    episodic_memory = EpisodicMemory()
    
    os.makedirs(RESULTS_DIR, exist_ok=True) # Stelle sicher, dass der Output-Ordner existiert

    for topic in topics:
        print(f"\n{'='*20} BEGINNE RECHERCHE ZU: '{topic}' {'='*20}")
        answer = process_prompt(topic, lock, episodic_memory)
        if answer:
            safe_filename = "".join(c for c in topic if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_') + ".md"
            filepath = os.path.join(RESULTS_DIR, safe_filename)
            print(f"Speichere Ergebnis in: '{filepath}'")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# Recherche-Ergebnis für: {topic}\n\n{answer}")
        else:
            print(f"\n{'='*20} KEIN ERGEBNIS FÜR: '{topic}' {'='*20}")
        time.sleep(random.uniform(2, 5))
        
    print("\nAlle Themen wurden abgearbeitet. Recherche abgeschlossen.")

# ======= SKRIPT-STARTPUNKT MIT MODUS-AUSWAHL =======
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{AGENT_NAME} v{AGENT_VERSION}")
    parser.add_argument("--mode", type=str, choices=['autonomous', 'task'], default='task', help="Wähle den Betriebsmodus.")
    args = parser.parse_args()
    
    if args.mode == 'autonomous':
        print("Starte Agenten im autonomen Modus...")
        self_improving_loop()
    elif args.mode == 'task':
        print("Starte Agenten im aufgaben-gesteuerten Modus...")
        task_driven_research_loop()