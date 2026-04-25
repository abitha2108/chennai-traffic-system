from flask import Flask, jsonify
from sumo_handler import connect_sumo, step, get_vehicle_count

app = Flask(__name__)

# connect once
connect_sumo()

@app.route("/traffic")
def traffic():
    try:
        step()

        queue = get_vehicle_count()
        signal = queue.index(max(queue)) if queue else 0

        return jsonify({
            "queue": queue,
            "signal": signal
        })

    except Exception as e:
        return jsonify({
            "queue": [0,0,0,0],
            "signal": 0,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)