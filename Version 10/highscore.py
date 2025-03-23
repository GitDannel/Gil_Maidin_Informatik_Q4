import os

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0

def save_highscore(level):
    current = load_highscore()
    if level > current:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(level))