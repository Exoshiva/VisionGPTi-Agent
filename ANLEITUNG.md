# Setup-Anleitung für VisionGPTi auf einem neuen PC

Dieses Dokument beschreibt die notwendigen Schritte, um den VisionGPTi-Agenten auf einem neuen Windows-PC ohne Administratorrechte einzurichten und auszuführen.

---

## Schritt 0: Vorbereitung (Auf dem Haupt-PC)

Bevor du das Projekt auf einen neuen PC überträgst, muss eine `requirements.txt`-Datei erstellt werden. Diese Datei listet alle notwendigen Python-Bibliotheken auf.

1.  Öffne ein PowerShell-Terminal im Projektverzeichnis.
2.  Aktiviere die virtuelle Umgebung:
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```
3.  Erstelle die `requirements.txt`-Datei mit folgendem Befehl:
    ```powershell
    python -m pip freeze > requirements.txt
    ```

---

## Einrichtung auf dem neuen PC

### Schritt 1: Python installieren

Stelle sicher, dass Python (Version 3.9 oder neuer) installiert ist.
* **WICHTIG:** Wähle bei der Installation unter Windows die Option **"Add Python to PATH"** aus.

### Schritt 2: Ollama installieren

Der Agent benötigt Ollama, um die lokalen Sprachmodelle auszuführen.
1.  Installiere Ollama von der offiziellen Webseite: [https://ollama.com/](https://ollama.com/)
2.  Öffne nach der Installation ein Terminal und lade das Standard-Modell für den Agenten herunter:
    ```bash
    ollama run gemma:2b
    ```

### Schritt 3: Projekt-Dateien kopieren

Kopiere deinen gesamten Projektordner auf den neuen PC. Er sollte mindestens die folgenden Dateien enthalten:
* `vision_gpti_agent.py`
* `themen_liste.txt`
* `requirements.txt` (aus der Vorbereitung)

### Schritt 4: Virtuelle Umgebung (`venv`) einrichten

Dies ist der wichtigste Schritt, um Konflikte zu vermeiden und ohne Admin-Rechte zu arbeiten.

1.  Öffne ein PowerShell-Terminal und navigiere in deinen Projektordner.
2.  Erstelle die `venv` (dieser Befehl muss nur einmal pro Projekt ausgeführt werden):
    ```powershell
    python -m venv .venv
    ```
3.  Aktiviere die `venv` für deine aktuelle Terminal-Sitzung:
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```
    Dein Terminal-Prompt sollte sich nun ändern und `(.venv)` am Anfang anzeigen.

4.  **Falls ein Fehler auftritt:** Sollte die Aktivierung aufgrund von Sicherheitsrichtlinien fehlschlagen, erlaube Skripte nur für diese Sitzung mit:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```
    Bestätige die Nachfrage mit `J` und versuche die Aktivierung erneut.

### Schritt 5: Abhängigkeiten installieren

Installiere mit diesem einen Befehl alle notwendigen Python-Bibliotheken in deine aktive `venv`:
```powershell
python -m pip install -r requirements.txt
```

### Schritt 6: Agenten starten

Alles ist bereit. Du kannst den Agenten jetzt wie gewohnt starten.

* **Aufgaben-gesteuerten Modus starten:**
    ```powershell
    python vision_gpti_agent.py --mode task
    ```
* **Autonomen Modus starten:**
    ```powershell
    python vision_gpti_agent.py --mode autonomous
    ```