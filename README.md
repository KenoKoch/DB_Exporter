# Beschreibung

Dieses Python-Programm verbindet sich mit einer Siemens SPS, überwacht ein Trigger-Signal und exportiert bei Erkennung Daten aus der SPS in eine SQLite-Datenbank. 
Das Trigger Bit wird in der SPS gesetzt und sobald die Daten exportiert sind vom Python Skript zurückgesetzt.
Wenn die Einrichtung abgeschlossen ist liegen die Einstellwerte in einem json File und die Einrichtmaske wird bei erneutem starten nicht ausgeführt.

---

## Inbetriebnahme


1. Zwei DB's im Tia Projekt anlegen (Wichtig DB darf nicht optimiert sein !!!!)
2. Ein DB ist für das Trigger Bit, hier das Erste Bit zum starten des Exports setzen. Einen weiteren DB für den Inhalt der Daten
3. DBExporter.exe in einen leeren Ordner legen und ausführen
4. In der Maske IP Adresse sowie DB Nummern, Rack/Slot(Aus Hardware Config) sowie Offsets der zu exportierenden Daten eintragen(Nur Bytes angeben)
5. Im Aufgabenplaner Programm beim starten des Rechner ausführen

---
