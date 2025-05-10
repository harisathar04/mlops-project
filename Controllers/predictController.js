const axios = require("axios");

// Function to handle prediction logic
exports.predictWeather = async (req, res) => {
  const { humidity, windSpeed, city, day, hour } = req.body;

  try {
    // Log the request data before sending it
    console.log("Sending data to Flask API:", {
      humidity,
      windSpeed,
      city,
      day,
      hour,
    });

    // Call Flask API
    const response = await axios.post(
      "http://localhost:5001/predict",
      {
        humidity,
        windSpeed,
        city,
        day,
        hour,
      },
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    res.json(response.data); // Send the prediction back to the frontend
  } catch (error) {
    console.error("Error calling Flask API:", error.message);
    res.status(500).send({
      error: "Error calling prediction service",
      details: error.message,
    });
  }
};
