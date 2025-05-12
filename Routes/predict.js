// routes/predict.js
const express = require("express");
const router = express.Router();
const predictController = require("../Controllers/predictController");

// Define the POST route for prediction
router.post("/predict", predictController.predictWeather);

module.exports = router;
