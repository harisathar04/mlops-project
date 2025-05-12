from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "http://localhost:5001/predict"

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        data = {
            "humidity": float(request.form["humidity"]),
            "windSpeed": float(request.form["windSpeed"]),
            "city": request.form["city"],
            "day": int(request.form["day"]),
            "hour": int(request.form["hour"])
        }

        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            prediction = response.json().get("predicted_temperature", "Error")

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
