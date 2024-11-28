var express = require('express');
var router = express.Router();


/* GET adopt grid page. */
router.get('/', async function (req, res, next) {
  try {
    const response = await fetch('http://localhost:5000/api/animals'); 
    const animals = await response.json();
    res.render('adoptGrid', { title: 'Adopt', animals });
  } catch (error) {
    console.error('Error fetching animal data:', error);
    res.render('adoptGrid', { title: 'Adopt', animals: [] });
  }
});

module.exports = router;
