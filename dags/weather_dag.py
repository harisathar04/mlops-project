from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import joblib
import pandas as pd

# Load the pre-trained model and label encoder
model = joblib.load('/opt/airflow/model/weather_condition_model.pkl')
label_encoder_city = joblib.load('/opt/airflow/model/label_encoder_city.pkl')

def predict_weather(**kwargs):
    # Get input features from the arguments passed by Node.js
    features = kwargs['dag_run'].conf['features']  # Assuming features are passed as DAG run configuration

    # Prepare the input data
    city = str(features[3])  # Ensure it's a plain Python string

    if city not in label_encoder_city.classes_:
        raise ValueError(f"City '{city}' not recognized. Available cities: {label_encoder_city.classes_}")

    encoded_city = label_encoder_city.transform([city])[0]  # Encode the city

    # Replace the city name with the encoded city value
    features[3] = encoded_city

    # Convert features to a DataFrame
    input_data = pd.DataFrame([features], columns=['feature1', 'feature2', 'feature3', 'city'])

    # Predict the weather condition
    prediction = model.predict(input_data)

    # Output the prediction
    print(f"Predicted weather condition: {prediction[0]}")

# Define default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'weather_prediction_dag',
    default_args=default_args,
    description='A DAG to predict weather conditions',
    schedule_interval='@daily',
)

# Define the task using PythonOperator
predict_task = PythonOperator(
    task_id='predict_weather',
    provide_context=True,
    python_callable=predict_weather,
    dag=dag,
)

# Set the task in the DAG
predict_task