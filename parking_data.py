"""Dataset helpers for the Smart Parking Management Agent."""
import json, random
from pathlib import Path

DATA_FILE = Path(__file__).parent / "dataset" / "parking_data.json"

def load_spaces():
    with DATA_FILE.open(encoding="utf-8") as f:
        return json.load(f)

def save_spaces(spaces):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(spaces, f, indent=2)

def generate_spaces(count=36, seed=None):
    rng = random.Random(seed)
    spaces = []
    for i in range(1, count + 1):
        x, y = ((i - 1) % 6) * 12 + 5, ((i - 1) // 6) * 10 + 5
        spaces.append({
            "id": f"P{i}", "slot_number": i, "x": x, "y": y,
            "distance": round((x*x + y*y) ** 0.5, 2),
            "status": rng.choices(["Available", "Occupied", "Reserved"], [0.55, 0.35, 0.10])[0],
            "type": "EV" if i % 6 == 0 else ("Disabled" if i % 6 == 3 else "Regular")
        })
    return spaces

def simulate(spaces):
    updated = [dict(s) for s in spaces]
    for space in updated:
        if random.random() < 0.16:
            space["status"] = random.choices(
                ["Available", "Occupied", "Reserved"], [0.58, 0.34, 0.08]
            )[0]
    return updated\n