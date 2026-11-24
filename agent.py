"""Rule-based rational parking agent using Euclidean distance."""
import math

def euclidean_distance(a, b):
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2)

def recommend_parking(spaces, driver, preference="Regular", max_distance=100):
    """Return the nearest available compatible slot and a transparent decision trace."""
    trace = [
        f"Received driver position ({driver['x']}, {driver['y']}).",
        f"Preference: {preference}; maximum distance: {max_distance} units."
    ]
    available = [s for s in spaces if s["status"] == "Available"]
    trace.append(f"Availability filter: {len(available)} of {len(spaces)} spaces are available.")
    compatible = [s for s in available if s["type"] == preference]
    trace.append(f"Type filter: {len(compatible)} available spaces match {preference}.")
    evaluated = []
    for space in compatible:
        distance = euclidean_distance(driver, space)
        if distance <= float(max_distance):
            evaluated.append({**space, "calculated_distance": round(distance, 2)})
    trace.append(f"Distance filter: {len(evaluated)} candidates are within the walking limit.")
    evaluated.sort(key=lambda s: (s["calculated_distance"], s["id"]))
    if not evaluated:
        trace.append("No slot satisfies every constraint. Try another type or a larger walking limit.")
        return {"recommendation": None, "candidates": [], "trace": trace}
    best = evaluated[0]
    trace.append(f"Selected {best['id']}: minimum distance among suitable candidates.")
    return {"recommendation": best, "candidates": evaluated, "trace": trace}\n