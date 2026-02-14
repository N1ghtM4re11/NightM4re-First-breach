import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "files")
DEFAULT_FILE = os.path.join(FILES_DIR, "flag")

os.makedirs(FILES_DIR, exist_ok=True)

while True:
    files = [
        f for f in os.listdir(FILES_DIR)
        if os.path.isfile(os.path.join(FILES_DIR, f))
    ]

    if len(files) == 0:
        with open(DEFAULT_FILE, "w") as f:
            f.write("placeholder\n")
        print("[+] flag file recreated")

    time.sleep(5)
