const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");
const surveyRoutes = require("./routes/survey");

const app = express();
const PORT = 3000;

// Middleware to parse form data
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files
app.use(express.static(path.join(__dirname, "public")));

// Use survey routes
app.use("/", surveyRoutes);

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
