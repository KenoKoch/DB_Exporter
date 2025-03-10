import sqlite3
import json
from snap7.util import *
import datetime




def Lade_UI_Daten():
    with open('UI_data.json', 'r') as f:
        return json.load(f)
    
def Werte_Übernehmen():
    global Geladene_Daten, Data_Struct, Export
    Geladene_Daten = Lade_UI_Daten()
    Data_Struct = Geladene_Daten['data_structure']
    Export = Geladene_Daten['Export']
    print(Data_Struct)

def DB_Erstellen(table_name='SPS_Export', db_name= "Daten.db"):    

    # Verbindung zur SQLite-Datenbank herstellen oder erstellen, falls nicht vorhanden
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # SQL-Befehl zum Erstellen der Tabelle vorbereiten
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, Datum TEXT"

    # Durch data_structure iterieren und INTEGER Spalten hinzufügen
    for index, (data_type, offset, name) in enumerate(Data_Struct):
        if isinstance(data_type, str) and "integer" in data_type.lower():
            column_name = name.replace('.', '_').replace('-', '_')
            create_table_sql += f", {column_name} INTEGER"
        elif isinstance(data_type, str) and "string" in data_type.lower():
            column_name = name.replace('.', '_').replace('-', '_')
            create_table_sql += f", {column_name} TEXT"
        elif isinstance(data_type, str) and "real" in data_type.lower():
            column_name = name.replace('.', '_').replace('-', '_')
            create_table_sql += f", {column_name} REAL"
       
    create_table_sql += ")"

    # Tabelle erstellen
    cursor.execute(create_table_sql)

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()
    
def DB_Speichern(values):
    conn = sqlite3.connect('Daten.db')  # Ersetzen Sie 'Daten.db' durch den Pfad Ihrer Datenbank
    cursor = conn.cursor()

    values['Datum'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Dynamisches Erstellen des SQL-Befehls zum Einfügen der Daten
    columns = ', '.join(values.keys())
    placeholders = ', '.join(['?'] * len(values))
    insert_query = f"INSERT INTO SPS_Export ({columns}) VALUES ({placeholders})"

    try:
        # Einfügen der Daten
        cursor.execute(insert_query, tuple(values.values()))
        conn.commit()  # Änderungen speichern
    except sqlite3.Error as e:
        print(f"Fehler beim Einfügen der Daten: {e}")
    finally:
        cursor.close()
        conn.close()



def decode_s7_string(byte_string):
    actual_length = byte_string[1]
    return byte_string[2:2+actual_length].decode('ascii', errors='ignore').strip('\x00')

def Export_DB(client):

    # Datenstruktur laden
    Werte_Übernehmen()
    DB_Erstellen()
    values = {}


    for index, (data_type, offset, name) in enumerate(Data_Struct):
        offset_int = int(offset)
        
        if isinstance(data_type, str) and "integer" in data_type.lower():
            value = client.db_read(Export, offset_int, 2)  # DB-Nummer, Offset, Anzahl der Bytes
            int_value = get_int(value, 0)  # Konvertierung in Integer
            column_name = name.replace('.', '_').replace('-', '_')
            values[column_name] = int_value

        elif isinstance(data_type, str) and "string" in data_type.lower():
            value = client.db_read(Geladene_Daten['Export'], offset_int, 256)  # 256 Bytes für STRING
            string_value = decode_s7_string(value)  # Umwandlung in String
            column_name = name.replace('.', '_').replace('-', '_')
            values[column_name] = string_value

        elif isinstance(data_type, str) and "real" in data_type.lower():
            value = client.db_read(Geladene_Daten['Export'], offset_int, 4)  # 4 Bytes für REAL
            real_value = get_real(value, 0)  # Konvertierung in Real
            column_name = name.replace('.', '_').replace('-', '_')
            values[column_name] = real_value

    # Einmaliges Speichern aller gesammelten Werte in der Datenbank
    DB_Speichern(values)

       


# Aufrufen
def Main():
    Lade_UI_Daten()
    DB_Erstellen()
    print(Data_Struct, Export)


if __name__ == "__main__":
    Main() 
 