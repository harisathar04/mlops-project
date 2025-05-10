const schedule = require("node-schedule");
const axios = require("axios");

const cities = ["London", "New York", "Tokyo", "Paris", "Sydney"];
const baseURL = "http://localhost:3000/weather/";

const fetchWeatherData = async () => {
  for (const city of cities) {
    try {
      const response = await axios.get(`${baseURL}/${city}`);
      console.log(`Data fetched successfully for ${city}`);
    } catch (error) {
      console.error(`Failed to fetch data for ${city}:`, error.message);
    }
  }
};

// Schedule the task to run every 12 hours
schedule.scheduleJob("0 */12 * * *", fetchWeatherData);
//schedule.scheduleJob("*/30 * * * * *", fetchWeatherData);

console.log("Weather data collection scheduled.");
