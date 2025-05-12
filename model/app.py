from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

# Get the absolute path to the directory where app.py is located
model_dir = os.path.dirname(os.path.abspath(__file__))

# Load your pre-trained model and label encoder using absolute paths
model = joblib.load(os.path.join(model_dir, "temperature_prediction_model.pkl"))
label_encoder_city = joblib.load(os.path.join(model_dir, "label_encoder_city.pkl"))

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    print("Received data:", data)
    # try:
    #     # Extract features from request
    humidity = float(data['humidity'])
    wind_speed = float(data['windSpeed'])
    city = data['city']
    day = int(data['day'])
    hour = int(data['hour'])

    # Encode the city
    encoded_city = label_encoder_city.transform([city])[0]

    # Prepare input for the model
    input_data = {
        'humidity': [humidity],
        'windSpeed': [wind_speed],
        'city': [encoded_city],
        'day': [day],
        'hour': [hour]
    }
    X = pd.DataFrame(input_data)

    # Make prediction
    prediction = model.predict(X)
    return jsonify({'predicted_temperature': prediction[0]})
    # except KeyError as e:
    #     return jsonify({'error': f'Missing key in input JSON: {str(e)}'}), 400
    # except ValueError as e:
    #     return jsonify({'error': f'Value error: {str(e)}'}), 400
    # except Exception as e:
    #     return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/')
def home():
    return "Welcome to the Weather Prediction API!"


if __name__ == '__main__':
    app.run(port=5001, debug=True)
