const axios = require("axios");
const fs = require("fs");
const path = require("path");
const { parse } = require("json2csv"); // Converts JSON to CSV

const API_KEY = '586e85742d7a0ead830de40d092da419'

const getWeatherByCity = async (req, res) => {
  const { city } = req.params;

  try {
    console.log(API_KEY);
    // Fetch 5-day weather forecast
    const response = await axios.get(
      `https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${API_KEY}&units=metric`
    );

    const { list, city: cityInfo } = response.data;

    const weatherData = list.map((entry) => ({
      date: entry.dt_txt.split(" ")[0],
      time: entry.dt_txt.split(" ")[1],
      temperature: entry.main.temp,
      humidity: entry.main.humidity,
      windSpeed: entry.wind.speed,
      weatherCondition: entry.weather[0].description,
    }));

    // Save data to a CSV file
    const csv = parse(weatherData);
    const outputDir = path.join(__dirname, "../data");
    const outputPath = path.join(outputDir, `${city}_weather.csv`);

    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir);
    }

    fs.writeFileSync(outputPath, csv);

    // Send response
    res.status(200).json({
      success: true,
      message: `Weather data saved successfully for ${city}.`,
      dataPath: outputPath,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to fetch weather data",
      error: error.response ? error.response.data : error.message,
    });
  }
};

module.exports = { getWeatherByCity };
