import random
import json
from datetime import datetime
from pathlib import Path

USED_FILE = "used_randoms.json"

def load_used():
    if Path(USED_FILE).exists():
        with open(USED_FILE, "r") as f:
            return json.load(f)
    return {}

def save_used(data):
    with open(USED_FILE, "w") as f:
        json.dump(data, f)

def generate_unique_random():
    today = datetime.now().strftime('%Y%m%d')
    used = load_used()
    used_today = set(used.get(today, []))

    while True:
        num = random.randint(1, 999)
        if num not in used_today:
            used_today.add(num)
            used[today] = list(used_today)
            save_used(used)
            return f"EDUKG-{today}-{num:03d}"

