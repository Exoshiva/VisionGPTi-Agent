# VisionGPTi Agent - (Genesis SML-Ökosystem)

![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)

Ein souveräner, modularer und ethisch gesteuerter KI-Agent, der für den Offline-First-Betrieb konzipiert ist. VisionGPTi ist die Referenzimplementierung des Genesis SML-Ökosystems und wird durch den **NovaQCore**, einen manifest-basierten Ethik-Kernel, geleitet.

## Vision

Das Ziel dieses Projekts ist die Schaffung eines Werkzeugs der Ermächtigung. VisionGPTi soll als autarke, dezentrale KI-Plattform dienen, die dem Nutzer die volle Kontrolle über seine Daten und die KI-Prozesse zurückgibt und gleichzeitig als "Mobiles Klassenzimmer" in bildungsschwachen Regionen eingesetzt werden kann.

## Features

* **Zwei Betriebsmodi:**
    * **Autonomer Modus:** Der Agent verfolgt selbstständig hochrangige Ziele, verfeinert diese und generiert eigene Forschungsfragen.
    * **Aufgaben-gesteuerter Modus:** Der Agent arbeitet eine vordefinierte Liste von Themen aus einer Textdatei ab.
* **Hybrider Betrieb:** Der Agent arbeitet primär offline mit seinem lokalen Gedächtnis, kann aber bei Bedarf auf ein Web-Recherche-Modul zugreifen, um neue Informationen zu sammeln.
* **Lokales Ökosystem:** Nutzt ausschließlich lokale und Open-Source-Komponenten für maximale Datensouveränität (Ollama, ChromaDB).
* **Ethische Leitplanken:** Jede generierte Antwort wird gegen ein anpassbares Set ethischer Regeln geprüft.
* **Modulare SML-Architektur:** Kernfunktionen wie Webrecherche sind als austauschbare "Sovereign Machine Learning" (SML)-Module konzipiert.

## Tech-Stack

* **Sprache:** Python 3.9+
* **LLM-Runner:** Ollama (z.B. mit `gemma:2b`, `llama3:8b`, etc.)
* **Vektor-Datenbank (Gedächtnis):** ChromaDB
* **Embedding-Modelle:** SentenceTransformers
* **Vision-Modelle:** Transformers (CLIP)
* **Web-Scraping:** DDGS, Requests, BeautifulSoup4

## Ordnerstruktur

```
/
├── .venv/                  # Virtuelle Python-Umgebung
├── chroma_db/              # Lokale Vektor-Datenbank (Memory Alpha)
├── recherche_quellen/      # (Optional) Ordner für manuelle Wissens-Dateien
├── themen_liste.txt        # Aufgabenliste für den 'task'-Modus
├── vision_gpti_agent.py    # Das Hauptskript des Agenten
├── inspect_db.py           # Werkzeug zum Einsehen der Datenbank
├── LICENSE                 # AGPL-3.0 Lizenz
└── README.md               # Diese Datei
```

## Getting Started

### 1. Klonen des Repositories
```bash
git clone <deine-repo-url>
cd <dein-repo-name>
```

### 2. Virtuelle Umgebung erstellen und aktivieren
Es wird dringend empfohlen, eine virtuelle Umgebung zu verwenden.

```powershell
# venv erstellen (nur einmal)
python -m venv .venv

# venv aktivieren (jedes Mal, wenn du ein neues Terminal öffnest)
.\.venv\Scripts\Activate.ps1
```
*Falls bei der Aktivierung ein Fehler auftritt, erlaube Skripte für diese Sitzung mit:*
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

### 3. Abhängigkeiten installieren
```bash
python -m pip install -r requirements.txt
```
*(Hinweis: Du musst noch eine `requirements.txt`-Datei mit allen Paketen erstellen. Nutze dazu bei aktiver venv den Befehl `python -m pip freeze > requirements.txt`)*

### 4. Ollama einrichten
Stelle sicher, dass Ollama installiert ist und das gewünschte Modell heruntergeladen wurde.
```bash
ollama run gemma:2b
```

## Usage

Der Agent kann über Kommandozeilen-Argumente in verschiedenen Modi gestartet werden.

### Aufgaben-gesteuerter Modus (Standard)
Der Agent arbeitet die Themen aus der `themen_liste.txt` ab.

1.  Befülle die `themen_liste.txt` mit deinen Recherche-Themen (ein Thema pro Zeile).
2.  Starte den Agenten:
    ```bash
    python vision_gpti_agent.py --mode task
    ```
    Die Ergebnisse werden in die Datei `recherche_ergebnisse.txt` geschrieben.

### Autonomer Modus
Der Agent versucht, sein `INITIAL_OBJECTIVE` selbstständig zu verfolgen.

```bash
python vision_gpti_agent.py --mode autonomous
```

## Contributing

Beiträge zur Verbesserung von VisionGPTi sind willkommen. Bitte erstelle einen Fork des Repositories, nimm deine Änderungen in einem separaten Branch vor und erstelle einen Pull Request mit einer klaren Beschreibung deiner Änderungen.

## License

Dieses Projekt ist unter der **AGPL-3.0** lizenziert. Siehe die `LICENSE`-Datei für weitere Details.