import snap7
from User_Interface import UI
import json
import time


def Lade_UI_Daten():
    try:
        with open('UI_data.json', 'r') as f:
            return json.load(f)
    except:
        return None

def connect_to_plc():
    # globale Variablen definieren
    global IP, Rack, Slot, Trigger, Export, TRIGGER_DB, TRIGGER_OFFSET
    # Daten aus json laden
    Geladene_Daten = Lade_UI_Daten()
    if Geladene_Daten != None:
        IP = Geladene_Daten['IP']
        Rack = Geladene_Daten['Rack']
        Slot = Geladene_Daten['Slot']
        Trigger = Geladene_Daten['Trigger']
        Export = Geladene_Daten['Export']
        TRIGGER_DB = Trigger
        TRIGGER_OFFSET = 0
        print(IP, TRIGGER_DB, Export)
    else:
        print(f"Fehler beim laden der UI Daten {IP}")

    client = snap7.client.Client()

    try:
        client.connect(IP, Rack, Slot)
        print(f"Verbunden mit SPS: {IP}")
        return client
    except Exception as e:
        print(f"Fehler beim Verbinden mit der SPS: {e}")
        return None
    
def reconnect(client):
    try:
        client.disconnect()  # trennt die Vernindung falls besteht
        time.sleep(2)  # Warten 
        client.connect(IP, Rack, Slot)  # Wiederherstellen der Verbindung
        print("Verbindung zur SPS wurde wiederhergestellt.")
    except Exception as e:
        print(f"Fehler beim Wiederherstellen der Verbindung: {e}")

def check_trigger(client):
    try:
        db_data = client.db_read(TRIGGER_DB, TRIGGER_OFFSET, 1)
        return db_data[0] & 0x01  # Prüft das erste Bit
    except Exception as e:
        print(f"Fehler beim Lesen des Trigger-Bits: {e}")
        reconnect(client)
        return check_trigger(client)

def reset_trigger(client):
    try:
        client.db_write(TRIGGER_DB, TRIGGER_OFFSET, b'\x00')
        print("Trigger zurückgesetzt")
    except Exception as e:
        print(f"Fehler beim Zurücksetzen des Trigger-Bits: {e}")

# Aufrufen wenn manueller Skript start
if __name__ == "__main__":
   connect_to_plc()
   check_trigger()
   reset_trigger()
