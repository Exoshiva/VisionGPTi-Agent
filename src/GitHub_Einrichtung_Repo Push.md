## Schritt-für-Schritt-Anleitung: Dein GitHub-Repository einrichten
Folge diesen Schritten, um dein lokales Projekt mit einem neuen GitHub-Repository zu verbinden und deine Arbeit hochzuladen (pushen).

1. Ein neues Repository auf GitHub erstellen
Gehe auf GitHub.com.

Klicke oben rechts auf das +-Symbol und wähle "New repository".

Repository name: Gib deinem Projekt einen Namen (z.B. VisionGPTi-Agent).

Description: Füge eine kurze Beschreibung hinzu.

Wähle "Public", damit andere den Code sehen können.

WICHTIG: Setze KEINEN Haken bei "Add a README file", "Add .gitignore" oder "Choose a license". Da wir diese Dateien bereits lokal haben, starten wir mit einem leeren Repository.

Klicke auf "Create repository".

2. Dein lokales Projekt mit dem GitHub-Repository verbinden
GitHub zeigt dir jetzt eine Seite mit Befehlen. Wir benutzen die Option "…or push an existing repository from the command line".

Öffne dein PowerShell-Terminal, stelle sicher, dass deine venv aktiv ist (.venv) und du dich im Hauptverzeichnis deines Projekts befindest (E:\...). Führe dann die folgenden Befehle nacheinander aus:

Schritt 2.1: Git initialisieren
(Dieser Befehl muss nur einmal pro Projekt ausgeführt werden)

PowerShell

git init
Schritt 2.2: Alle Dateien zum "Staging" hinzufügen
(Der Punkt . bedeutet "alle Dateien im aktuellen Ordner")

PowerShell

git add .
Schritt 2.3: Deinen ersten "Commit" erstellen
(Ein Commit ist eine Momentaufnahme deiner Arbeit. Die -m-Option ist für die Commit-Nachricht)

PowerShell

git commit -m "Initial commit: Projekt-Setup und erster Agenten-Prototyp"
Schritt 2.4: Den Haupt-Branch umbenennen
(Der Standard-Branch wird heute oft main statt master genannt)

PowerShell

git branch -M main
Schritt 2.5: Dein lokales Repository mit dem Online-Repository verbinden
(Kopiere die URL von deiner GitHub-Seite. Sie sieht so ähnlich aus)

PowerShell

git remote add origin https://github.com/DEIN_BENUTZERNAME/VisionGPTi-Agent.git
Schritt 2.6: Deine Arbeit hochladen (Push)
(Dies ist der Befehl, den du immer wieder benutzen wirst, um Änderungen hochzuladen)

PowerShell

git push -u origin main
## Ergebnis
Nachdem der push-Befehl durchgelaufen ist, lade deine GitHub-Seite neu. Du wirst sehen, dass alle deine lokalen Ordner und Dateien jetzt online sind.

Dein Projekt ist nun eingerichtet und versioniert. Alle zukünftigen Änderungen kannst du mit git add ., git commit -m "..." und git push einfach aktualisieren.