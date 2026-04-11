import tkinter as tk
from base_window import BaseWindow

class MyApp(BaseWindow):
    def __init__(self, root, db):
        self.window = root
        self.window.title("Multiple Message")
        self.window.config(bg="aliceblue")
        self.center_window(self.window, 800, 600)
        self.window.grab_set()

        self.db = db
        self.main_frame = tk.Frame(
            self.window, bg="aliceblue", bd=4, relief="solid"
        )

        self.build_ui()

    def build_ui(self):
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))


if __name__ == '__main__':
    from database import Database
    conn = Database()
    parent=tk.Tk()
    MyApp(parent, conn)
    parent.mainloop()