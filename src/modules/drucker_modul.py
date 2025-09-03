import os
import tempfile
import platform
import time

def print_text(content: str, filename_prefix: str = "VisionGPTi_Druck") -> bool:
    """
    Nimmt einen Text-String, speichert ihn in einer temporären Datei 
    und sendet ihn an den Standarddrucker (primär für Windows).

    Args:
        content (str): Der zu druckende Textinhalt.
        filename_prefix (str): Ein Präfix für den Namen der temporären Datei.

    Returns:
        bool: True, wenn der Auftrag erfolgreich gesendet wurde, sonst False.
    """
    # Überprüft, ob das Betriebssystem Windows ist, da os.startfile("print") hier am zuverlässigsten ist.
    if platform.system() != "Windows":
        print(f"[DRUCKER-FEHLER] Diese Druckfunktion ist für Windows optimiert und auf '{platform.system()}' nicht direkt verfügbar.")
        return False

    try:
        # Erstelle eine temporäre Textdatei mit einem sinnvollen Namen
        with tempfile.NamedTemporaryFile(mode='w', prefix=f"{filename_prefix}_", suffix=".txt", delete=False, encoding='utf-8') as temp_file:
            temp_file.write(content)
            temp_filepath = temp_file.name
        
        print(f"[DRUCKER] Temporäre Datei für den Druckauftrag erstellt: {temp_filepath}")

        # Nutze den Windows-Befehl "print" über die os.startfile Funktion
        # Dies sendet die Datei an den im System konfigurierten Standarddrucker.
        print(f"[DRUCKER] Sende Druckauftrag für '{temp_filepath}' an den Standarddrucker...")
        os.startfile(temp_filepath, "print")
        print("[DRUCKER] Druckauftrag erfolgreich an das Betriebssystem übergeben.")
        
        # Gib dem System etwas Zeit, die Datei zu verarbeiten, bevor sie gelöscht wird.
        time.sleep(10) 
        os.remove(temp_filepath)
        print(f"[DRUCKER] Temporäre Datei '{temp_filepath}' wurde gelöscht.")
        
        return True

    except Exception as e:
        print(f"[DRUCKER-FEHLER] Konnte den Druckauftrag nicht senden: {e}")
        return False

if __name__ == '__main__':
    # Dies ist ein Beispiel, wie das Modul direkt getestet werden kann
    print("Starte Testlauf für das Drucker-Modul...")
    
    # Beispielhafter Textinhalt
    test_inhalt = """
    Genesis SML-Ökosystem - Testdruck
    ===================================

    Dies ist ein Test des Drucker-Moduls für den VisionGPTi-Agenten.

    - Modul: drucker_modul.py
    - Funktion: print_text()
    - Status: Test erfolgreich.

    Wenn dieses Dokument gedruckt wird, funktioniert das Modul wie erwartet.
    """
    
    # Rufe die Druckfunktion auf
    print_text(test_inhalt, filename_prefix="Testdruck")