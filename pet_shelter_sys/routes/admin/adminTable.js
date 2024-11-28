var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', async function(req, res, next) {
  try {
    // Fetch the data from your API endpoint
    const response = await fetch('http://localhost:5000/api/animals'); // Ensure the correct API path
    const animalData = await response.json();

    // Render the adminTable view, passing the data
    res.render('admin/adminTable', { 
      title: 'Admin - Table Page', 
      animals: animalData // Pass the animal data to EJS
    });
  } catch (error) {
    console.error('Error fetching animals:', error);
    res.status(500).send('Error fetching data.');
  }
});

module.exports = router;