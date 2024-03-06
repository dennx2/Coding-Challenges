const express = require("express");

const app = express();
const PORT = process.env.PORT || 3000;

// Add CORS headers middleware
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*"); // Allow requests from any origin
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
  next();
});

// Define a route for handling requests to your external API
app.get("/chromeext-xml", async (req, res) => {
  try {
    // Fetch data from the external API
    const response = await fetch("https://codingchallenges.substack.com/feed");

    if (!response.ok) {
      throw new Error("Failed to fetch data");
    }

    // Get the JSON data from the response
    const data = await response.text();

    // Send the data back to the client
    res.send(data);
  } catch (error) {
    console.error("Error:", error);
    res.status(500).send("Internal Server Error");
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
