VisionGPTi Agent - (Genesis SML-Ökosystem)
Ein souveräner, modularer und ethisch gesteuerter KI-Agent, der für den Offline-First-Betrieb konzipiert ist. VisionGPTi ist die Referenzimplementierung des Genesis SML-Ökosystems und wird durch den NovaQCore, einen manifest-basierten Ethik-Kernel, geleitet.

Vision
Das Ziel dieses Projekts ist die Schaffung eines Werkzeugs der Ermächtigung. VisionGPTi soll als autarke, dezentrale KI-Plattform dienen, die dem Nutzer die volle Kontrolle über seine Daten und die KI-Prozesse zurückgibt und gleichzeitig als "Mobiles Klassenzimmer" in bildungsschwachen Regionen eingesetzt werden kann.

Kern-Features
Zwei Betriebsmodi:

Autonomer Modus: Der Agent verfolgt selbstständig hochrangige Ziele, verfeinert diese und generiert eigene Forschungsfragen.

Aufgaben-gesteuerter Modus: Der Agent arbeitet eine vordefinierte Liste von Themen aus einer Textdatei ab.

Hybrider Betrieb: Der Agent arbeitet primär offline mit seinem lokalen Gedächtnis, kann aber bei Bedarf auf ein Web-Recherche-Modul zugreifen, um neue Informationen zu sammeln.

Lokales Ökosystem: Nutzt ausschließlich lokale und Open-Source-Komponenten für maximale Datensouveränität (Ollama, ChromaDB).

Ethische Leitplanken: Jede generierte Antwort wird gegen ein anpassbares Set ethischer Regeln geprüft.

Modulare SML-Architektur: Kernfunktionen wie Webrecherche sind als austauschbare "Sovereign Machine Learning" (SML)-Module konzipiert.

Technologie-Stack
Sprache: Python 3.9+

LLM-Runner: Ollama (z.B. mit gemma:2b, llama3:8b, etc.)

Vektor-Datenbank (Gedächtnis): ChromaDB

Embedding-Modelle: SentenceTransformers

Web-Scraping: DDGS, Requests, BeautifulSoup4

Zusätzliche Tools: venv, git, pip

Ordnerstruktur
/
├── .venv/                  # Virtuelle Python-Umgebung
├── chroma_db/              # Lokale Vektor-Datenbank (Memory Alpha)
├── data/                   # Enthält Eingabe- und Ausgabedaten
│   ├── input/              # Aufgabenliste für den 'task'-Modus
│   └── output/             # Ergebnisse der Recherche
├── docs/                   # Projektdokumentation und Whitepaper
├── recherche_quellen/      # (Optional) Ordner für manuelle Wissens-Dateien
├── src/                    # Quellcode des Agenten und der Module
├── tests/                  # Tests für den Agenten
├── ANLEITUNG.md            # Allgemeine Anleitung für das Projekt
├── CODE_OF_CONDUCT.md      # Verhaltenskodex für die Community
├── CONTRIBUTING.md         # Richtlinien für Beiträge zum Projekt
├── LICENSE.md              # AGPL-3.0 Lizenz
├── README.md               # Diese Datei
├── SECURITY.md             # Sicherheitsrichtlinien
├── SUPPORT.md              # Support- und Kontaktinformationen
└── requirements.txt        # Python-Abhängigkeiten
Getting Started
Repository klonen

Bash

git clone https://github.com/Exoshiva/VisionGPTi-Agent.git
cd VisionGPTi-Agent
Virtuelle Umgebung erstellen & aktivieren
Es wird dringend empfohlen, eine virtuelle Umgebung zu verwenden.

Bash

# venv erstellen (nur einmal)
python -m venv .venv

# venv aktivieren (jedes Mal, wenn du ein neues Terminal öffnest)
.\.venv\Scripts\Activate.ps1
Abhängigkeiten installieren

Bash

python -m pip install -r requirements.txt
Ollama einrichten
Stelle sicher, dass Ollama installiert ist und das gewünschte Modell heruntergeladen wurde.

Bash

ollama run gemma:2b
Usage
Der Agent kann über Kommandozeilen-Argumente in verschiedenen Modi gestartet werden.

Aufgaben-gesteuerter Modus (Standard)
Der Agent arbeitet die Themen aus der data/input/themen_liste.txt ab.

Bash

python src/vision_gpti_agent.py --mode task
Die Ergebnisse werden in den data/output-Ordner geschrieben.

Autonomer Modus
Der Agent versucht, sein INITIAL_OBJECTIVE selbstständig zu verfolgen.

Bash

python src/vision_gpti_agent.py --mode autonomous
Community & Beiträge
Wir sind ein Projekt, das von der Gemeinschaft lebt. Deine Mitwirkung ist entscheidend, um unsere Mission voranzutreiben.

Code beitragen: Siehe unsere CONTRIBUTING.md-Datei, um zu erfahren, wie du Pull Requests einreichen kannst.

Verhaltenskodex: Wir verpflichten uns zu einem positiven und inklusiven Umfeld. Lies unseren CODE_OF_CONDUCT.md.

Sicherheit melden: Wenn du eine Sicherheitslücke findest, melde sie bitte vertraulich. Informationen dazu findest du in SECURITY.md.

Support & Fragen: Für allgemeine Anfragen und Support, lies unsere SUPPORT.md-Datei.

Lizenz
Dieses Projekt ist unter der GNU Affero General Public License v3.0 (AGPL-3.0) lizenziert. Weitere Details findest du in der LICENSE.md-Datei.

Kontakt
Webseite: www.exoshiva.org
X (ehemals Twitter): @Exoshiva_KI