# Imports
import threading
import time
import psutil
import ctypes

from ctypes import wintypes
from pypresence import Presence
from programs import programs
from gui import setup_tray_icon
from tools import log_message, run_event

# Variables
client_id = "1278677048994562110"
user32 = ctypes.WinDLL('user32', use_last_error=True)


# Methods
def connect_to_discord():
    log_message("Connecting to Discord...")

    try:
        RPC = Presence(client_id)
        RPC.connect()
        log_message("Connected to Discord RPC successfully!")

        return RPC
    except Exception as e:
        log_message(f"Failed to connect to Discord RPC: {e}")


def get_active_window_process_name():
    hwnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    if pid.value:
        try:
            process = psutil.Process(pid.value)
            return process.name().lower()
        except Exception as e:
            log_message(f"Error retrieving process name: {e}")
            return None

    return None


def update_discord_status(program, RPC):
    status = programs.get(program, {"state": "Idle", "details": "Idle", "large_icon": None, "small_icon": None})

    large_icon = status["large_icon"]
    small_icon = status["small_icon"]
    details = status["details"]

    if large_icon:
        try:
            RPC.update(
                state=status["state"],
                details=details,
                large_image=large_icon,
                small_image=small_icon,
                party_size=[1, 1]
            )

            log_message(f"Status updated: {status['state']} (Details: {details}, Small Icon: {small_icon})")
        except Exception as e:
            log_message(f"Failed to update Discord status: {e}")
    else:
        log_message(f"Large icon not found for {program}. Skipping update")


def start_program(RPC):
    while run_event.is_set():
        active_program = get_active_window_process_name()

        if active_program:
            if active_program in programs:
                update_discord_status(active_program, RPC)
            else:
                log_message(f"Active window '{active_program}' is not in the list of tracked programs.")
        else:
            log_message("No active window found.")

        time.sleep(3)


# Run
if __name__ == "__main__":
    tray_thread = threading.Thread(target=setup_tray_icon)
    tray_thread.daemon = True
    tray_thread.start()

    rpc = connect_to_discord()
    start_program(rpc)
