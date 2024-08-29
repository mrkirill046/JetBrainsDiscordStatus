# Imports
import pystray
import sys
import tkinter as tk

from tkinter import scrolledtext
from tools import get_image, log_message, resource_path, run_event


# Methods
def on_close():
    log_message("Closing GUI")
    root.withdraw()
    setup_tray_icon()


def on_quit(icon, item):
    log_message("Exiting application")
    run_event.clear()
    sys.exit()


def on_open(icon, item):
    log_message("Starting application gui")
    icon.visible = False
    start_gui()


def setup_tray_icon():
    image = get_image()
    icon = pystray.Icon("example", image, "JetBrains Discord Status")

    icon.menu = pystray.Menu(
        pystray.MenuItem("Открыть", on_open),
        pystray.MenuItem("Выйти", on_quit)
    )

    icon.run_detached()


def start_gui():
    global root

    root = tk.Tk()

    screen_width = root.winfo_screenwidth() / 1.5
    screen_height = root.winfo_screenheight() / 1.5
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()

    x = (screen_width - window_width) // 3
    y = (screen_height - window_height) // 3

    root.title("JetBrains Discord Status")
    root.geometry(f'{int(screen_width)}x{int(screen_height)}+{int(x)}+{int(y)}')
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.iconbitmap(resource_path("assets/icon.ico"))
    root.resizable(width=False, height=False)

    log_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
    log_display.pack(expand=True, fill=tk.BOTH)

    def update_logs():
        with open("assets/logs/app.log", "r", encoding="utf-8") as log_file:
            logs = log_file.read()

        log_display.config(state='normal')
        log_display.delete(1.0, tk.END)
        log_display.insert(tk.END, logs)
        log_display.see(tk.END)
        log_display.config(state='disabled')
        root.after(1000, update_logs)

    update_logs()
    root.mainloop()
