import mlflow
import mlflow.sklearn
import joblib
import argparse
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true', help='Run in development mode (quick dry run)')
args = parser.parse_args()

# Load the processed data
X_train, X_test, y_train, y_test = joblib.load("processed_data.pkl")

# If dev mode is enabled, reduce dataset size
if args.dev:
    X_train = X_train[:50]
    y_train = y_train[:50]
    X_test = X_test[:10]
    y_test = y_test[:10]
    print("Running in DEV mode: using small data subset")

# Start MLflow experiment
if not args.dev:
    mlflow.start_run()
    mlflow.log_param("model_type", "LinearRegression")

# Initialize and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error (MSE):", mse)
print("R-Squared (R²):", r2)

# Save model
joblib.dump(model, "temperature_prediction_model.pkl")

# Log with MLflow (skip in dev)
if not args.dev:
    mlflow.log_metric("mean_squared_error", mse)
    mlflow.log_metric("r_squared", r2)
    mlflow.sklearn.log_model(model, "linear_regression_model")
    mlflow.end_run()
