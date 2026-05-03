import tkinter as tk
from tkinter import filedialog, messagebox
from base_window import BaseWindow, CustomComboBox, LabelButton, CustomEntry
from backend import InputReader
from utils import ImportController


class ImportContactGUI(BaseWindow):
    def __init__(self, parent, db):
        self.window = tk.Toplevel(parent)
        self.window.title("Contact Upload")
        # self.center_window(self.window, 300, 350, parent)
        self.window.configure(bg="aliceblue")
        self.window.transient(parent)
        self.window.grab_set()

        self.controller = ImportController(db)
        self.file_path = None
        self.columns = []
        self.first_name_var = tk.StringVar()
        self.second_name_var = tk.StringVar()
        self.s_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.location_var = tk.StringVar()
        # NOTE: Dropdown list font (this is the tricky part in Tkinter
        self.window.option_add("*TCombobox*Listbox.font", ("Arial", 12))
        self.main_frame = tk.Frame(
            self.window, bg="aliceblue", bd=4, relief="solid"
        )
        self.drop_frame = None
        self.drop_label = None
        self.name_combo = None
        self.location_combo = None
        self.contact_combo = None

        self.build_ui()

    def build_ui(self):
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.show_upload_window()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_upload_window(self):
        self.clear_main_frame()

        # Title
        top_frame = tk.Frame(self.main_frame, bg="aliceblue")
        top_frame.pack(side="top", fill="x")
        tk.Label(
            top_frame, text="Upload Contact", bg="aliceblue", fg="purple",
            font=("Georgia", 20, "bold", "italic", "underline")
        ).pack(side="left", anchor="sw")
        upload_btn = LabelButton(
            top_frame, text="➕👤", font=("Arial", 14, "bold"), bg="aliceblue",
            fg="blue", command=self.show_single_contact_ui,
            tooltip_text="+ One Contacts"
        ).get_widget()
        upload_btn.pack(side="right")
        self.drop_frame = tk.Frame(
            self.main_frame, bg="aliceblue", bd=2, relief="ridge"
        )
        self.drop_frame.pack(fill="x", padx=5, pady=(0, 5))
        self.drop_label = tk.Label(
            self.drop_frame, text="Click to Select File", bg="lightgray",
            height=4, cursor="hand2", fg="blue", font=("Arial", 12, "italic")
        )
        self.drop_label.pack(fill="x")
        self.drop_label.bind("<Button-1>", self.select_file)
        combo_frame = tk.Frame(self.main_frame, bg="aliceblue")
        # self.name_combo_obj = CustomComboBox(combo_frame, values=None, width=13)
        # self.contact_combo_obj = CustomComboBox(combo_frame, values=None, width=13)
        # self.location_combo_obj = CustomComboBox(
        #     combo_frame, values=None, width=15, state="normal"
        # )
        self.name_combo = CustomComboBox(combo_frame, values=None, width=13)
        self.contact_combo = CustomComboBox(combo_frame, values=None, width=13)
        self.location_combo = CustomComboBox(
            combo_frame, values=None, width=15, state="normal"
        )
        combo_frame.pack(fill="both", expand=True, pady=5)
        tk.Label(
            combo_frame, text="Contact Name:", bg="aliceblue", fg="blue",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0)
        self.name_combo.grid(row=1, column=0, padx=5)
        tk.Label(
            combo_frame, text="Phone Number:", bg="aliceblue", fg="blue",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=1)
        self.contact_combo.grid(row=1, column=1, padx=5)
        tk.Label(
            combo_frame, text="Type Location If Not Available", fg="blue",
            bg="aliceblue", font=("Arial", 12, "bold")
        ).grid(row=2, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="w")
        self.location_combo.grid(
            row=3, column=0, columnspan=2, padx=10, sticky="w"
        )
        self.name_combo.disable()
        self.contact_combo.disable()
        self.location_combo.disable()
        # Save Button
        tk.Button(
            self.main_frame, text="Upload Contact", bg="blue", fg="white", bd=4,
            relief="groove", font=("Arial", 12, "bold"), command=self.save_data
        ).pack(pady=10, anchor="center")

    # Switch to single contact UI
    def show_single_contact_ui(self):
        self.clear_main_frame()
        # New title
        top_frame = tk.Frame(self.main_frame, bg="aliceblue")
        top_frame.pack(side="top", fill="x")
        tk.Label(
            top_frame, text="Single Contact", bg="aliceblue", fg="purple",
            font=("Georgia", 20, "bold", "italic", "underline")
        ).pack(side="left", anchor="sw")
        upload_btn = LabelButton(
            top_frame, text="➕👨‍👧‍👧", font=("Arial", 14, "bold"), bg="aliceblue",
            fg="blue", command=self.show_upload_window, tooltip_text="Upload Contacts"
        ).get_widget()
        upload_btn.pack(side="right")
        entry_frame = tk.Entry(
            self.main_frame, bg="aliceblue", bd=2, relief="ridge"
        )
        entry_frame.pack(fill="both", expand=True)
        tk.Label(
            entry_frame, text="First Name", bg="aliceblue", fg="blue",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            entry_frame, text="Second Name", bg="aliceblue", fg="blue",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=1, sticky="w", padx=5)
        first_name = CustomEntry(
            parent=entry_frame, variable=self.first_name_var, width=15,
            placeholder="Enter 1ˢᵗ Name"
        ).get_widget()
        first_name.grid(row=1, column=0, padx=(0, 5))
        second_name = CustomEntry(
            parent=entry_frame, variable=self.second_name_var, width=15,
            placeholder="Enter 2ⁿᵈ Name"
        ).get_widget()
        second_name.grid(row=1, column=1, padx=(5, 0))
        tk.Label(
            entry_frame, text="Other Names (Optional) *", bg="aliceblue",
            fg="dodgerblue", font=("Arial", 12, "bold", "italic")
        ).grid(row=2, column=0, columnspan=2, padx=5, sticky="w")
        other_name = CustomEntry(
            parent=entry_frame, variable=self.s_name_var, width=25,
            placeholder="Enter Other Names (optional)"
        ).get_widget()
        other_name.grid(row=3, column=0, columnspan=2, padx=5)
        tk.Label(
            entry_frame, text="Phone Number:", bg="aliceblue", fg="blue",
            font=("Arial", 12, "bold")
        ).grid(row=4, column=0, sticky="e", padx=(5, 0), pady=5)
        phone_number = CustomEntry(
            parent=entry_frame, variable=self.phone_var, width=15,
            placeholder="01/07xxxxxxxx"
        ).get_widget()
        phone_number.grid(row=4, column=1, sticky="w", padx=(0, 5), pady=5)

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

            self.name_combo.set_values(self.columns)
            self.contact_combo.set_values(self.columns)
            self.location_combo.set_values(self.columns)
            self.name_combo.enable()
            self.contact_combo.enable()
            self.location_combo.enable()
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