import mlflow
import mlflow.sklearn
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the processed data
X_train, X_test, y_train, y_test = joblib.load("processed_data.pkl")

# Start MLflow experiment
mlflow.start_run()

# Log model parameters
mlflow.log_param("model_type", "LinearRegression")

# Initialize Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Log metrics
mlflow.log_metric("mean_squared_error", mse)
mlflow.log_metric("r_squared", r2)

print("Mean Squared Error (MSE):", mse)
print("R-Squared (R²):", r2)

# Save and log the trained model
joblib.dump(model, "temperature_prediction_model.pkl")
mlflow.sklearn.log_model(model, "linear_regression_model")

# End the MLflow run
mlflow.end_run()
