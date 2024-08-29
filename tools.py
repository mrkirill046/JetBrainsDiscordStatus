# Imports
import os
import sys
import threading
import time

from PIL import Image

# Variables
run_event = threading.Event()
run_event.set()


# Methods
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)


def log_message(message):
    print(message)

    if not os.path.exists("assets/logs"):
        os.makedirs("assets/logs")

    with open("assets/logs/app.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


def get_image():
    icon_path = "assets/icon.ico"

    if os.path.isfile(icon_path):
        return Image.open(resource_path(icon_path))
    else:
        raise FileNotFoundError(f"Icon file not found: {icon_path}")
