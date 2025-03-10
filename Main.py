from Data_Processing import Export_DB
import time
from User_Interface import UI
import os
import sys

def main():


    # Setzen des Arbeitsverzeichnisses auf den Ort der Datei
    exe_path = os.path.dirname(sys.executable)
    os.chdir(exe_path)

    
    if not os.path.exists('UI_data.json'):
        print("UI_data.json wurde nicht gefunden. Starte die UI ")
        UI_I = UI()
        UI_I.run()
    else:
         print("UI_data.json ist vorhanden. UI wird nicht ausgeführt.")

    from PLC_Connection import connect_to_plc, check_trigger, reset_trigger

    client = connect_to_plc()
    if not client:
        return

    print("Warte auf Trigger-Signal...")
    try:
        while True:
            if check_trigger(client):
                print("Trigger erkannt. Starte Export...")
                Export_DB(client)
                reset_trigger(client)
            time.sleep(4)  # 4s Pause
    except KeyboardInterrupt:
        print("Programm durch Benutzer beendet.")
    finally:
        if client:
            client.disconnect()
            print("Verbindung zur SPS getrennt.")
        
    input("Drücken Sie Enter, um das Programm zu beenden...")

if __name__ == "__main__":
    main()