from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

FILE_NAME = "traffic_rl.csv"

# 🔹 Home route (avoid Not Found)
@app.route("/")
def home():
    return "🚦 Traffic API Running! Use /traffic"

# 🔹 Main API
@app.route("/traffic", methods=["GET"])
def get_traffic():

    if not os.path.exists(FILE_NAME):
        return jsonify({
            "queue": [0, 0, 0, 0],
            "signal": 0,
            "throughput": 0,
            "delay": 0
        })

    try:
        df = pd.read_csv(FILE_NAME)

        if len(df) < 4:
            return jsonify({
                "queue": [0, 0, 0, 0],
                "signal": 0,
                "throughput": 0,
                "delay": 0
            })

        last = df.iloc[-4:]

        queue = last["queue"].tolist()
        signal = int(last["signal"].iloc[0])
        throughput = int(last["throughput"].iloc[-1])
        delay = float(last["delay"].iloc[-1])

        return jsonify({
            "queue": queue,
            "signal": signal,
            "throughput": throughput,
            "delay": delay
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)