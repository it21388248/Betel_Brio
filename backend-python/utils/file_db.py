import os
import json

DB_PATH = "uploads/files_db.json"

def load_files():
    if not os.path.exists(DB_PATH):
        return []

    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_files(files):
    with open(DB_PATH, "w") as f:
        json.dump(files, f, indent=2)
