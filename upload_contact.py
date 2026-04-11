import tkinter as tk
from tkinter import filedialog, messagebox
from base_window import BaseWindow, CustomComboBox
from backend import InputReader
from utils import ImportController


class ImportContactGUI(BaseWindow):
    def __init__(self, parent, db):
        self.window = tk.Toplevel(parent)
        self.window.title("Contact Upload")
        self.center_window(self.window, 300, 350, parent)
        self.window.configure(bg="aliceblue")
        self.window.transient(parent)
        self.window.grab_set()

        self.controller = ImportController(db)
        self.file_path = None
        self.columns = []
        # NOTE: Dropdown list font (this is the tricky part in Tkinter
        self.window.option_add("*TCombobox*Listbox.font", ("Arial", 12))
        self.main_frame = tk.Frame(
            self.window, bg="aliceblue", bd=4, relief="solid"
        )
        self.drop_frame = tk.Frame(
            self.main_frame, bg="aliceblue", bd=2, relief="ridge"
        )
        self.drop_label = tk.Label(
            self.drop_frame, text="Click to Select File", bg="lightgray",
            height=4, cursor="hand2", fg="blue",font=("Arial", 12, "italic")
        )
        self.combo_frame = tk.Frame(self.main_frame, bg="aliceblue")
        self.name_combo = CustomComboBox(
            self.combo_frame, values=None, width=13
        ).get_widget()
        self.contact_combo = CustomComboBox(
            self.combo_frame, values=None, width=13
        ).get_widget()
        self.location_combo = CustomComboBox(
            self.combo_frame, values=None, width=15, state="normal"
        ).get_widget()

        self.build_ui()

    def build_ui(self):
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        # Title
        tk.Label(
            self.main_frame, text="Upload Contact", bg="aliceblue",
            font=("Georgia", 22, "bold", "italic", "underline"), fg="purple"
        ).pack(side="top", anchor="center", pady=(5, 0))
        self.drop_frame.pack(fill="x", padx=5, pady=(0, 5))
        self.drop_label.pack(fill="x")
        self.drop_label.bind("<Button-1>", self.select_file)
        self.combo_frame.pack(fill="both", expand=True, pady=5)
        tk.Label(
            self.combo_frame, text="Contact Name:", bg="aliceblue", fg="blue",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0)
        self.name_combo.grid(row=1, column=0, padx=5)
        tk.Label(
            self.combo_frame, text="Phone Number:", bg="aliceblue", fg="blue",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=1)
        self.contact_combo.grid(row=1, column=1, padx=5)
        tk.Label(
            self.combo_frame, text="Type Location If Not Available", fg="blue",
            bg="aliceblue", font=("Arial", 12, "bold")
        ).grid(row=2, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="w")
        self.location_combo.grid(row=3, column=0, columnspan=2, padx=5, sticky="w")

        # Save Button
        tk.Button(
            self.main_frame, text="Save Contact", bg="blue", fg="white", bd=4,
            relief="groove", font=("Arial", 12, "bold"), command=self.save_data
        ).pack(pady=5, anchor="center")

    # File Selection
    def select_file(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return
        self.file_path = file_path
        self.load_columns()

    # Load Columns Into Combo boxes
    def load_columns(self):
        try:
            reader = InputReader(self.file_path)
            self.columns = reader.get_columns()

            self.name_combo["values"] = self.columns
            self.contact_combo["values"] = self.columns
            self.location_combo["values"] = self.columns
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.window)

    def save_data(self):
        if not self.file_path:
            messagebox.showwarning(
                "Warning", "Please Select File first.", parent=self.window
            )
            return

        name_col = self.name_combo.get()
        contact_col = self.contact_combo.get()
        location_value = self.location_combo.get()

        # Determine if it's a column or manual entry
        if location_value in self.columns:
            location_col = location_value
            manual_location = None
        else:
            location_col = None
            manual_location = location_value.capitalize() if location_value else None

        if not name_col or not contact_col:
            messagebox.showwarning(
                "Warning", "Select Required Columns.", parent=self.window
            )
            return

        try:
            inserted = self.controller.import_contacts(
                self.file_path, name_col, contact_col, location_col, manual_location
            )
            messagebox.showinfo(
                "Success", f"{inserted} Contacts Imported Successfully.",
                parent=self.window
            )
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.window)

if __name__ == "__main__":
    from database import Database
    db = Database()
    db.create_tables()
    root=tk.Tk()
    # Enable DPI scaling (call once before widgets)
    BaseWindow.enable_dpi_scaling(root, scale=1.25)
    ImportContactGUI(root, db)
    root.mainloop()