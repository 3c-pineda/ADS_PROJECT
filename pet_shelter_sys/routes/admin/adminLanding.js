const express = require('express');
const router = express.Router();

router.get('/', async function (req, res, next) {
  try {
    // Fetch data from all the Flask API endpoints
    const speciesResponse = await fetch('http://localhost:5000/species-distribution'); // Flask API URL
    const adoptionStatusResponse = await fetch('http://localhost:5000/adoption-status');
    const ageDistributionResponse = await fetch('http://localhost:5000/age-distribution');
    
    // Check if all responses are successful
    if (!speciesResponse.ok || !adoptionStatusResponse.ok || !ageDistributionResponse.ok) {
      throw new Error(`HTTP error! One of the responses failed.`);
    }

    // Parse the JSON data from each response
    const speciesData = await speciesResponse.json();
    const adoptionStatusData = await adoptionStatusResponse.json();
    const ageDistributionData = await ageDistributionResponse.json();

    // Pass data to the EJS template
    res.render('admin/adminLanding', {
      title: 'Admin - Landing Page',
      speciesData: speciesData,
      adoptionStatusData: adoptionStatusData,
      ageDistributionData: ageDistributionData
    });

  } catch (error) {
    console.error('Error fetching data from API:', error.message);
    res.status(500).send('Error fetching data from API');
  }
});

module.exports = router;
