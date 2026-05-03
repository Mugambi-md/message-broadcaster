import tkinter as tk
from base_window import BaseWindow, CustomButton, LabelButton

class MyApp(BaseWindow):
    def __init__(self, root, db):
        self.window = root
        self.window.title("Multiple Message")
        self.window.config(bg="aliceblue")
        self.center_window(self.window, 720, 600)
        self.window.grab_set()

        self.db = db
        self.main_frame = tk.Frame(
            self.window, bg="aliceblue", bd=4, relief="solid"
        )
        self.btn_frame = tk.Frame(self.main_frame, bg="aliceblue")
        self.content_frame = tk.Frame(self.main_frame, bg="white")
        self.center_frame = tk.Frame(
            self.content_frame, bd=2, relief="ridge", bg="aliceblue"
        )
        self.sms_list = tk.Frame(self.content_frame, bd=1, relief="ridge")

        self.build_ui()

    def build_ui(self):
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        tk.Label(
            self.main_frame, text="Multiple Message Sender", bg="aliceblue",
            fg="purple", font=("Georgia", 20, "italic", "bold", "underline")
        ).pack(side="top", anchor="sw", padx=5)
        self.btn_frame.pack(side="left", fill="y")
        self.content_frame.pack(fill="both", expand=True)
        message_btn = LabelButton(
            self.btn_frame, text="📩", font=("Arial", 18, "bold"), bg="aliceblue",
            fg="blue", command=None, tooltip_text="Messages"
        ).get_widget()
        message_btn.pack(pady=10)

        contact_btn = LabelButton(
            self.btn_frame, text="👨‍👧‍👧", font=("Arial", 18, "bold"), bg="aliceblue",
            fg="blue", command=None, tooltip_text="Available Contacts"
        ).get_widget()
        contact_btn.pack(pady=10)
        broadcast_btn = LabelButton(
            self.btn_frame, text="📢", font=("Arial", 18, "bold"), bg="aliceblue",
            fg="blue", command=None, tooltip_text="Broadcast Message"
        ).get_widget()
        broadcast_btn.pack(pady=10)
        upload_btn = LabelButton(
            self.btn_frame, text="➕👤", font=("Arial", 16, "bold"), bg="aliceblue",
            fg="blue", command=None, tooltip_text="Add Contacts"
        ).get_widget()
        upload_btn.pack(pady=10)
        # title_label.place(relx=0.0, rely=0.0, anchor="nw", relheight=0.07)
        list_height = float(self.content_frame.winfo_height() - 0.07)
        list_width = self.content_frame.winfo_width()
        self.sms_list.pack(side="left", fill="y")

        self.center_frame.place(
            relx=0, rely=0.07, relheight=list_height, relwidth=list_width
        )


        # Make label and btn frame width adjust automatically
        def adjust_width(event=None):
            # Get btn_frame actual width
            self.btn_frame.update_idletasks() # ensure size is calculated
            btn_w = self.btn_frame.winfo_width()
            # Set label width = total sms_frame width - btn_frame width - some padding
            total_w = self.content_frame.winfo_width()
            sms_list_width = (total_w / 3) + 35
            self.sms_list.config(width=sms_list_width)
            # if total_w > btn_w:
                # title_label.config(
                #     width=(total_w - btn_w - 20) // 20
                # )
        # Bind resize events
        self.content_frame.bind("<Configure>", adjust_width)
        self.btn_frame.bind("<Configure>", adjust_width)

        # Initial adjustment
        self.content_frame.after(100, adjust_width)


if __name__ == '__main__':
    from database import Database
    conn = Database()
    parent=tk.Tk()
    BaseWindow.enable_dpi_scaling(parent, scale=1.25)
    MyApp(parent, conn)
    parent.mainloop()