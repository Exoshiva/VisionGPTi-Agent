import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Führt eine Websuche mit DuckDuckGo durch und gibt die Top-Ergebnisse zurück.
    """
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
    """
    Extrahiert den reinen Textinhalt von einer Webseite.
    """
    print(f"[Web-Recherche] Lade Inhalt von: {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Wirft einen Fehler bei schlechtem Statuscode (4xx oder 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Entfernt Skript- und Style-Elemente
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Extrahiert den Text und bereinigt ihn
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)

        return clean_text
    except requests.RequestException as e:
        print(f"[ERROR] Fehler beim Abrufen der URL {url}: {e}")
        return ""