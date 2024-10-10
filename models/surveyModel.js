const fs = require('fs');
const path = require('path');

exports.saveSurvey = ({ genre, listeningTime }, callback) => {
    const csvLine = `${genre},${listeningTime}\n`;
    const filePath = path.join(__dirname, '../output/survey_results.csv');
    fs.appendFile(filePath, csvLine, callback);
};