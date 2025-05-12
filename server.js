const cookieParser = require("cookie-parser");
const express = require("express");
const dotenv = require("dotenv");
const app = express();
const path = require("path");
const { spawn } = require("child_process");

// Absolute path to the Python executable
const pythonPath = "python3";

// Spawn Flask process
const flaskProcess = spawn(pythonPath, ["app.py"], {
  cwd: path.resolve(__dirname, "model"), // Set working directory to 'model'
});

flaskProcess.stdout.on("data", (data) => {
  console.log(`Flask stdout: ${data}`);
});

flaskProcess.stderr.on("data", (data) => {
  console.error(`Flask stderr: ${data}`);
});

flaskProcess.on("close", (code) => {
  console.log(`Flask process exited with code ${code}`);
});

app.use(cookieParser());
app.use(express.json());

dotenv.config();
const WeatherRoutes = require("./Routes/weatherRoutes");
const predictRoute = require("./Routes/predict");

app.use("/weather", WeatherRoutes);
app.use("/api", predictRoute);

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
