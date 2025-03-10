import customtkinter as ctk
import json
import tkinter.messagebox as messagebox
import time



class UI:
    def __init__(self):
        # Allgemeine Einstellungen
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.UI = ctk.CTk()
        self.UI.title("DB Exporter")
        self.UI.geometry("460x650")  # Vergrößerte Fenstergröße

        # Eingaben zum Verbinden
        self.create_connection_inputs()

        # Eingaben zur Datenstruktur
        self.create_data_structure_inputs()

        self.submit_button = ctk.CTkButton(self.UI, text="Verbinden", width=225 ,command=self.save_values)
        self.submit_button.grid(row=17, column=0, columnspan=2, pady=10)

        self.IP = None
        self.Rack = None
        self.Slot = None
        self.Trigger = None
        self.Export = None
        self.data_structure = []

    def create_connection_inputs(self):
        labels = ["IP-Adresse:", "Rack:", "Slot:", "Trigger DB:", "Export DB:"]
        entries = ["E_IP", "E_Rack", "E_Slot", "E_Trigger", "E_Export"]

        for i, (label, entry) in enumerate(zip(labels, entries)):
            ctk.CTkLabel(self.UI, text=label).grid(row=i, column=0, sticky="W", padx=5, pady=5)
            setattr(self, entry, ctk.CTkEntry(self.UI, width=150))
            getattr(self, entry).grid(row=i, column=1, sticky="W", padx=5, pady=5)

    def create_data_structure_inputs(self):
        ctk.CTkLabel(self.UI, text="Datenstruktur:").grid(row=5, column=0, columnspan=4, sticky="W", padx=5, pady=10)
        ctk.CTkLabel(self.UI, text="Name").grid(row=6, column=0, columnspan=2, sticky="W", padx=5, pady=5)
        ctk.CTkLabel(self.UI, text="Datentyp").grid(row=6, column=2, columnspan=2, sticky="W", padx=5, pady=5)
        ctk.CTkLabel(self.UI, text="Offset").grid(row=6, column=4, columnspan=2, sticky="W", padx=5, pady=5)

        self.data_type_entries = []
        self.offset_entries = []
        self.name_entries = []

        data_types = ["integer", "string", "real"]

        for i in range(10):
            name_entry = ctk.CTkEntry(self.UI, width=225)
            name_entry.grid(row=i+7, column=0, columnspan=2, sticky="W", padx=5, pady=2)
            self.name_entries.append(name_entry)

            data_type_var = ctk.StringVar(value= "Datentyp")  # Standardwert ist der erste Eintrag
            data_type_menu = ctk.CTkOptionMenu(self.UI, values=data_types, variable=data_type_var, width=150)
            data_type_menu.grid(row=i+7, column=2, columnspan=2, sticky="W", padx=6, pady=2)
            self.data_type_entries.append(data_type_var)

            offset_entry = ctk.CTkEntry(self.UI, width=50)
            offset_entry.grid(row=i+7, column=4, columnspan=2, sticky="W", padx=5, pady=2)
            self.offset_entries.append(offset_entry)

    def run(self):
        self.UI.mainloop()
        return self.data_structure, self.IP, self.Rack, self.Slot, self.Trigger, self.Export

    def save_values(self):
        try:
            self.IP = self.E_IP.get()
            self.Rack = int(self.E_Rack.get())
            self.Slot = int(self.E_Slot.get()) 
            self.Trigger = int(self.E_Trigger.get())
            self.Export = int(self.E_Export.get())

            self.data_structure = []
            for data_type_var, offset_entry, name_entry in zip(self.data_type_entries, self.offset_entries, self.name_entries):
                dt = data_type_var.get()  # Hier rufen wir den Wert der StringVar ab
                off = offset_entry.get()
                name = name_entry.get()
                if dt and off and name:
                    self.data_structure.append((dt, off, name))

            # Daten in Json File speichern

            UI_Data = {
                'IP': self.IP,
                'Rack': self.Rack,
                'Slot': self.Slot,
                'Trigger': self.Trigger,
                'Export': self.Export,
                'data_structure': self.data_structure
            }
            with open('UI_data.json', 'w') as f:
                json.dump(UI_Data, f)

            
            time.sleep(3)
            messagebox.showinfo("Erfolg", "Eingaben übernommen")
            self.UI.destroy()
        except Exception as e:
            print(f"Fehler beim Übernehmen der Werte: {e}")
        

    


if __name__ == "__main__":
    UI_I = UI() 
    UI_I.run()
