# Step 1: Use Python image
FROM python:3.9-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the entire Flask app
COPY . .

# Step 5: Expose Flask port (default 5000)
EXPOSE 5001

# Step 6: Run the Flask app
CMD ["python", "app.py"]
