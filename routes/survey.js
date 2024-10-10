const express = require('express');
const router = express.Router();
const surveyController = require('../controllers/surveyController');

router.post('/submit-survey', surveyController.submitSurvey);

module.exports = router;