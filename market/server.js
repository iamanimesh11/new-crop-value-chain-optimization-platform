const express = require('express');
const app = express();
const fs = require('fs');

// Read the JSON data from your file
const jsonData = JSON.parse(fs.readFileSync('data/commodity.json', 'utf8'));

// Define an API endpoint that returns the JSON data
app.get('/api/data', (req, res) => {
    res.json(jsonData);
});

const port = process.env.PORT || 3000; // Choose a port for your server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
