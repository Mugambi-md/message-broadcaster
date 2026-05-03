import tkinter as tk
import os
from tkinter import ttk


class BaseWindow:
    ICON_PATH = "myicon.ico"

    @staticmethod
    def set_icon(window):
        """Sets the window icon for Tk or Toplevel."""
        if not os.path.exists(BaseWindow.ICON_PATH):
            return

        try:
            if BaseWindow.ICON_PATH.endswith(".ico"):
                window.iconbitmap(BaseWindow.ICON_PATH)
            else:
                icon = tk.PhotoImage(file=BaseWindow.ICON_PATH)
                window.iconphoto(True, icon)
        except (tk.TclError, FileNotFoundError):
            # Icon format not supported or platform limitation
            pass

    @staticmethod
    def center_window(window, width=800, height=600, parent=None):
        """Centers a Tk or Toplevel window.
        - If 'parent' is given, centers relative to the parent window.
        - Otherwise, centers on the screen."""
        # Ensure window has calculated dimensions
        window.update_idletasks()
        # Apply icon automatically
        BaseWindow.set_icon(window)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        if parent:
            parent.update_idletasks()
            parent_x = parent.winfo_x()
            parent_y = parent.winfo_y()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            x = parent_x + (parent_width - width) //2
            y = parent_y + (parent_height - height) //2
        else:
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
        # Ensure the window stays on screen
        x = max(0, min(x, screen_width - width))
        y = max(0, min(y, screen_height - height))
        window.geometry(f"{width}x{height}+{x}+{y}")
        # Fade-in only for child windows
        if parent:
            BaseWindow.fade_in(window)
            # Fade-out
            BaseWindow.bind_fade_close(window)

    @staticmethod
    def enable_dpi_scaling(window, scale=1.25):
        """
        Enable DPI scaling for high-resolution displays.
        Call once on root window.
        """
        try:
            window.tk.call("tk", "scaling", scale)
        except tk.TclError:
            pass

    @staticmethod
    def fade_in(window, duration=150, steps=10):
        """
        Smooth fade-in animation.
        Duration: total time in ms.
        steps: animation smoothness
        """
        window.attributes("-alpha", 0.0)
        window.update_idletasks()

        delay = max(1, duration // steps)
        def _fade(step=0):
            alpha = step / steps
            window.attributes("-alpha", alpha)
            if step < steps:
                window.after(delay, _fade, step + 1)

        _fade()

    @staticmethod
    def bind_fade_close(window):
        """Intercept Window close (X button) and apply fade-out."""
        window.protocol(
            "WM_DELETE_WINDOW", lambda: BaseWindow.fade_out(window)
        )

    @staticmethod
    def fade_out(window, duration=120, steps=6):
        """Fade out then destroy or callback."""
        delay = max(1, duration // steps)

        def _fade(step=steps):
            alpha = step / steps
            window.attributes("-alpha", alpha)
            if step > 0:
                window.after(delay, _fade, step - 1)
            else:
                window.destroy()

        _fade()


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg, width=None):
        super().__init__(parent, bg=bg)

        self.canvas = tk.Canvas(
            self, bg=bg, highlightthickness=0, width=width)
        self.scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.window_id = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.window_id, width=e.width)
        )
        # Scroll config
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # Layout
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Mousewheel binding only when mouse is over canvas or inner frame
        for widget in (self.canvas, self.scrollable_frame):
            widget.bind("<Enter>", self._bind_mousewheel)
            widget.bind("<Enter>", self._unbind_mousewheel)

    def _bind_mousewheel(self, event):
        # Windows/ macOS
        self.canvas.bind("<Mousewheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_linux_scroll_up)
        self.canvas.bind("<Button-5>", self._on_linux_scroll_down)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind("<MouseWheel>")
        self.canvas.unbind("<Button-4>")
        self.canvas.unbind("<Button-5>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_linux_scroll_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def _on_linux_scroll_down(self, event):
        self.canvas.yview_scroll(1, "units")


class CustomComboBox:
    def __init__(self, parent, values=None, state="readonly", width=20):
        self.parent = parent
        self.values = values if values else []
        self.state = state
        self.width = width

        # Create style for better dropdown visibility
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Style name (unique to avoid conflicts)
        self.style_name = "Custom.TCombobox"
        self.style.configure(self.style_name, font=("Arial", 12))

        # Create combobox
        self.combobox = ttk.Combobox(
            self.parent, values=self.values, state=self.state, width=self.width,
            style=self.style_name, font=("Arial", 12)
        )

    def __getattr__(self, item):
        return getattr(self.combobox, item)

    # def get_widget(self):
    #     return self.combobox

    def set(self, value):
        self.combobox.set(value)

    def clear(self):
        self.combobox.set("")

    def set_values(self, values):
        self.values = values
        self.combobox["values"] = values

    def bind(self, event, callback):
        self.combobox.bind(event, callback)

    def set_default(self, index=0):
        if self.values:
            self.combobox.current(index)

    def disable(self):
        self.combobox.configure(state="disabled")

    def enable(self):
        self.combobox.configure(state=self.state)


class CustomButton:
    def __init__(self, parent, text, font, command=None, width=10):
        self.parent = parent
        self.text = text
        self.command = command
        self.width = width
        self.font = font

        self.button = tk.Button(
            self.parent, text=self.text, command=self.command, bg="blue",
            fg="white", width=self.width, font=self.font, bd=4, relief="groove",
            cursor="hand2", activebackground="darkblue", activeforeground="white"
        )

    def get_widget(self):
        return self.button

    def enable(self):
        self.button.config(state="normal")

    def disable(self):
        self.button.config(state="disabled")

    def bind(self, event, callback):
        self.button.bind(event, callback)


class LabelButton:
    def __init__(self, parent, text, font, bg, fg=None, command=None, tooltip_text=""):
        self.parent = parent
        self.command = command
        self.tooltip_text = tooltip_text

        # Create label (acts like a button)
        self.label = tk.Label(
            self.parent, text=text, bg=bg, fg=fg, font=font, cursor="hand2"
        )

        # Bind Click
        if command:
            self.label.bind("<Button-1>", lambda e: self.command())

        # Tooltip setup
        self.after_id = None
        self.tooltip = None
        self.label.bind("<Enter>", self.show_tooltip)
        self.label.bind("<Leave>", self.hide_tooltip)

    def get_widget(self):
        return self.label

    def show_tooltip(self, event=None):
        if not self.tooltip_text:
            return

        x = self.label.winfo_rootx() + 20
        y = self.label.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.label)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")

        tk.Label(
            self.tooltip, text=self.tooltip_text, bg="lightyellow",
            fg="black", relief="solid", bd=1, font=("Arial", 10)
        ).pack()

    def schedule_tooltip(self, event=None):
        self.after_id = self.label.after(500, self.show_tooltip)

    def hide_tooltip(self, event=None):
        if self.after_id:
            self.label.after_cancel(self.after_id)
            self.after_id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class CustomEntry:
    def __init__(self, parent, variable, width, placeholder):
        self.parent = parent
        self.var = variable
        self.placeholder = placeholder

        self.entry = tk.Entry(
            self.parent, textvariable=self.var, bd=2, relief="solid",
            font=("Arial", 12), width=width
        )
        self.add_placeholder()

    def get_widget(self):
        return self.entry

    def enable(self):
        self.entry.config(state="normal")

    def disable(self):
        self.entry.config(state="disabled")

    def bind(self, event, callback):
        self.entry.bind(event, callback)

    def add_placeholder(self):
        if not self.var.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="blue")

        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, event=None):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg="black")

    def _add_placeholder(self, event=None):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="blue")