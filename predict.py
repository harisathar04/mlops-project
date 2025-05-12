import sys
import joblib
import pandas as pd

# Load the pre-trained model and label encoder
model = joblib.load('./model/temperature_condition_model.pkl')
label_encoder_city = joblib.load('./model/label_encoder_city.pkl')  # Assuming this was saved

# Get input features from the arguments passed by Node.js
features = sys.argv[1:]  # Assuming features are passed as arguments

# Prepare the input data
city = str(features[3])  # Ensure it's a plain Python string
encoded_city = label_encoder_city.transform([city])[0]  # Encode the city

if city not in label_encoder_city.classes_:
    raise ValueError(f"City '{city}' not recognized. Available cities: {label_encoder_city.classes_}")

data = {
    'temperature': [float(features[0])],
    'humidity': [float(features[1])],
    'windSpeed': [float(features[2])],
    'city': [encoded_city],  # Use encoded city
    'day': [int(features[4])],
    'hour': [int(features[5])]
}

# Convert to DataFrame
X = pd.DataFrame(data)

# Make prediction
prediction = model.predict(X)

# Output the prediction
print(prediction[0])
