import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib  # For saving the split data

# Directory containing CSV files
data_dir = "../data/"
files = [file for file in os.listdir(data_dir) if file.endswith("_weather.csv")]

print(files)

# Initialize lists for combined data
data = []

# Read and combine data from all files
for file in files:
    city_name = file.split("_")[0]  # Extract city name from file name
    file_path = os.path.join(data_dir, file)
    df = pd.read_csv(file_path)
    df["city"] = city_name
    data.append(df)

# Combine all city data into a single DataFrame
df_combined = pd.concat(data, ignore_index=True)

# Convert date and time into a single datetime column
df_combined["datetime"] = pd.to_datetime(df_combined["date"] + " " + df_combined["time"])
df_combined.drop(columns=["date", "time"], inplace=True)

label_encoder_weather = LabelEncoder()
df_combined["weatherCondition"] = label_encoder_weather.fit_transform(df_combined["weatherCondition"])

label_encoder_city = LabelEncoder()
df_combined["city"] = label_encoder_city.fit_transform(df_combined["city"])

# Save the encoder
joblib.dump(label_encoder_city, 'label_encoder_city.pkl')

# Define features (X) and target (y)
X = df_combined[["datetime", "humidity", "windSpeed", "city"]] # Exclude 'temperature'
y = df_combined["temperature"]  # Target variable

# Convert datetime into numerical features (day, hour, etc.)
X["day"] = X["datetime"].dt.day
X["hour"] = X["datetime"].dt.hour
X.drop(columns=["datetime"], inplace=True)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save the split data for later use
joblib.dump((X_train, X_test, y_train, y_test), "processed_data.pkl")
