const fs = require("fs");
const path = require("path");
const surveyModel = require("../models/surveyModel");
const logger = require("../utils/logger");

exports.submitSurvey = (req, res) => {
  const { genre, "listening-time": listeningTime } = req.body;

  // Log the received data for debugging
  logger.log("Received data:", req.body);

  // Validate the data
  if (!genre || !listeningTime) {
    logger.log("Invalid input:", req.body);
    return res.status(400).send("Invalid input");
  }

  // Ensure the output directory exists
  const outputDir = path.join(__dirname, "../output");
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Save to CSV
  surveyModel.saveSurvey({ genre, listeningTime }, (err) => {
    if (err) {
      logger.log("Error writing to file:", err);
      return res.status(500).send("Server error");
    }
    logger.log("Survey submitted successfully:", { genre, listeningTime });
    res.send("Survey submitted successfully");
  });
};
