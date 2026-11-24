from flask import Flask, jsonify, render_template, request
from agent import recommend_parking
from parking_data import load_spaces, save_spaces, generate_spaces, simulate

app = Flask(__name__)
history = []

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/spaces")
def get_spaces():
    return jsonify(load_spaces())

@app.post("/api/recommend")
def recommend():
    body = request.get_json(force=True)
    try:
        driver = {"x": float(body.get("x", 0)), "y": float(body.get("y", 0))}
        max_distance = float(body.get("max_distance", 100))
        if max_distance < 0:
            raise ValueError("Maximum distance cannot be negative.")
        preference = body.get("preference", "Regular")
        if preference not in ("Regular", "EV", "Disabled"):
            raise ValueError("Unknown parking type.")
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    result = recommend_parking(load_spaces(), driver, preference, max_distance)
    entry = {
        "time": __import__("datetime").datetime.now().strftime("%H:%M:%S"),
        "driver": driver, "preference": preference,
        "recommendation": result["recommendation"]["id"] if result["recommendation"] else None,
        "distance": result["recommendation"]["calculated_distance"] if result["recommendation"] else None,
        "success": result["recommendation"] is not None
    }
    history.insert(0, entry)
    del history[20:]
    result["history"] = history
    return jsonify(result)

@app.get("/api/history")
def get_history():
    return jsonify(history)

@app.post("/api/simulate")
def run_simulation():
    spaces = simulate(load_spaces())
    save_spaces(spaces)
    return jsonify(spaces)

@app.post("/api/generate")
def generate():
    spaces = generate_spaces()
    save_spaces(spaces)
    return jsonify(spaces)

@app.post("/api/reset")
def reset():
    spaces = generate_spaces(seed=42)
    save_spaces(spaces)
    history.clear()
    return jsonify(spaces)

@app.post("/api/update/<slot_id>")
def update_slot(slot_id):
    body = request.get_json(force=True)
    spaces = load_spaces()
    target = next((s for s in spaces if s["id"] == slot_id), None)
    if not target:
        return jsonify({"error": "Parking slot not found."}), 404
    status = body.get("status")
    if status not in ("Available", "Occupied", "Reserved"):
        return jsonify({"error": "Invalid status."}), 400
    target["status"] = status
    save_spaces(spaces)
    return jsonify(target)

if __name__ == "__main__":
    app.run(debug=True)\n