import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from gantry_controller import Beast  # Assuming your Beast class is in a file named beast.py

class GantryControlApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gantry Control")
        self.master.geometry("800x480")  # Match the Waveshare LCD resolution
        self.master.attributes("-fullscreen", True)  # Enable full-screen mode
        self.beast = Beast()

        # Main Frame
        self.main_frame = ttk.Frame(master, padding=20)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Title
        self.title_label = ttk.Label(self.main_frame, text="Gantry Control", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=20)

        # Button Frame
        self.button_frame = ttk.Frame(self.main_frame, padding=10)
        self.button_frame.pack(fill=BOTH, expand=True)

        # Buttons with rounded corners and shadows
        self.home_button = ttk.Button(
            self.button_frame, text="Home", command=self.home, style="Primary.TButton", width=20
        )
        self.home_button.grid(row=0, column=0, padx=10, pady=10)

        self.move_storage_button = ttk.Button(
            self.button_frame, text="Move to Storage", command=lambda: self.move_to("storage_1"), style="Success.TButton", width=20
        )
        self.move_storage_button.grid(row=0, column=1, padx=10, pady=10)

        self.move_printer_button = ttk.Button(
            self.button_frame, text="Move to Printer", command=lambda: self.move_to("printer_1"), style="Info.TButton", width=20
        )
        self.move_printer_button.grid(row=0, column=2, padx=10, pady=10)

        # Filament Slot Selection
        self.slot_label = ttk.Label(self.main_frame, text="Select Filament Slot (1-4):", font=("Helvetica", 14))
        self.slot_label.pack(pady=10)

        self.slot_frame = ttk.Frame(self.main_frame, padding=10)
        self.slot_frame.pack(pady=10)

        self.slot_var = ttk.StringVar(value="1")
        self.slot_entry = ttk.Entry(self.slot_frame, textvariable=self.slot_var, font=("Helvetica", 14), width=5)
        self.slot_entry.grid(row=0, column=0, padx=10)

        self.slot_button = ttk.Button(
            self.slot_frame, text="Set Slot", command=self.set_slot, style="Warning.TButton"
        )
        self.slot_button.grid(row=0, column=1, padx=10)

        # Load Buttons
        self.load_gantry_button = ttk.Button(
            self.main_frame, text="Load Gantry", command=self.load_gantry, style="Primary.Outline.TButton", width=25
        )
        self.load_gantry_button.pack(pady=10)

        self.load_printer_button = ttk.Button(
            self.main_frame, text="Load Printer", command=self.load_printer, style="Danger.Outline.TButton", width=25
        )
        self.load_printer_button.pack(pady=10)

    def home(self):
        try:
            self.beast.home_state()
            messagebox.showinfo("Success", "Gantry homed successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def move_to(self, location):
        try:
            self.beast.move_gantry_to(location)
            messagebox.showinfo("Success", f"Gantry moved to {location}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def set_slot(self):
        try:
            slot = int(self.slot_var.get())
            if 1 <= slot <= 4:
                self.beast.activeSlot = slot
                self.beast.change_active_slot()
                messagebox.showinfo("Success", f"Filament slot set to {slot}")
            else:
                raise ValueError("Slot must be between 1 and 4")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_gantry(self):
        try:
            self.beast.load_gantry_with_filament()
            messagebox.showinfo("Success", "Gantry loaded with filament")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_printer(self):
        try:
            self.beast.load_printer_with_filament()
            messagebox.showinfo("Success", "Printer loaded with filament")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = ttk.Window(themename="flatly")
    GantryControlApp(app)
    app.mainloop()
