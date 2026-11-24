# Smart Parking Management Agent

A beginner-friendly AI project built with Python, Flask, HTML, CSS, JavaScript, and Chart.js. It simulates a parking facility and uses an explainable rule-based intelligent agent to recommend the nearest suitable available parking slot.

## Features
- Live dashboard statistics and occupancy chart
- 36-slot interactive parking map with type/status filters and slot editing
- Python recommendation engine using Euclidean distance
- Driver location presets, parking-type preference, and maximum walking distance
- Transparent reasoning trace and decision history
- PEAS representation, rational-agent demonstration, workflow, and academic documentation
- Dataset generation, reset, one-step simulation, and automatic simulation mode

## Requirements
- Python 3.9 or newer
- pip
- Internet connection only for Google Fonts and Chart.js CDN (the Flask application and AI logic run locally)

## Run locally

1. Extract the ZIP and open a terminal in the `smart-parking-agent` folder.
2. (Recommended) Create and activate a virtual environment:

   **Windows**
   ```bash
   py -m venv venv
   venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask server:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## Project structure

```text
smart-parking-agent/
├── app.py                    # Flask routes and API
├── agent.py                  # AI decision algorithm
├── parking_data.py           # Dataset generation and simulation
├── dataset/
│   └── parking_data.json     # Simulated parking records
├── templates/
│   └── index.html            # Dashboard structure
├── static/
│   ├── css/style.css         # Responsive dark theme
│   └── js/script.js          # Dashboard interactions and API calls
├── requirements.txt
└── README.md
```

## AI algorithm

1. Read driver coordinates and parking preference.
2. Keep only spaces with status `Available`.
3. Keep only spaces whose type matches the requested type.
4. Calculate Euclidean distance from the driver to each candidate:
   `d = sqrt((x2 - x1)^2 + (y2 - y1)^2)`
5. Discard candidates beyond the maximum walking distance.
6. Sort by `(distance, parking ID)` and choose the first candidate.
7. If no candidates remain, return a clear no-match result.

The tie-break rule is ascending parking ID, so equal-distance decisions are deterministic.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/spaces` | Read parking dataset |
| POST | `/api/recommend` | Run intelligent agent |
| GET | `/api/history` | Read current-session decisions |
| POST | `/api/simulate` | Randomly update slot states |
| POST | `/api/generate` | Generate a new dataset |
| POST | `/api/reset` | Restore deterministic demo dataset |
| POST | `/api/update/<slot_id>` | Update one slot's status |

Example recommendation request:
```json
{
  "x": 5,
  "y": 5,
  "preference": "Regular",
  "max_distance": 100
}
```

## Demonstration / viva flow
1. Explain the problem and the PEAS cards.
2. Show the live dataset and slot status colors.
3. Select Main entrance, Regular, and a walking limit; click **Find best parking**.
4. Explain the filter counts and Euclidean distance in the reasoning trace.
5. Change one slot's status by clicking it.
6. Run a simulation step and show how statistics and the recommendation change.
7. Explain rationality: the agent avoids unavailable spaces and chooses the closest valid option based on the current percepts and user constraints.

## Academic notes and limitations
This is a simulated, rule-based intelligent agent—not a machine-learning model. It uses straight-line Euclidean distance rather than a real pedestrian route. Data is stored in a local JSON file, so it is intended for a single-user classroom demo. The project does not connect to physical sensors, maps, payment systems, or a real parking reservation service.

## Troubleshooting
- If `python` is not recognized on Windows, try `py app.py`.
- If port 5000 is already in use, stop the other process or change the port in the final `app.run(...)` line.
- If the chart or fonts do not load, check internet access; the core dashboard and agent do not require an API key.\n