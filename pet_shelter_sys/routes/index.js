var express = require('express');
var router = express.Router();

/* GET home page. */

router.get('/', function(req, res, next) {
  // Define the endpoint URL
const url = "http://localhost:5000/api/animals";

//Function to categorize age
function categorizeAge(age, species) {
  if (species.toLowerCase() === 'dog') {
    if (age <= 2) return 'Young';
    else if (age <= 7) return 'Adult';
    else return 'Elder';
  } else if (species.toLowerCase() === 'cat') {
    if (age <= 2) return 'Young';
    else if (age <= 10) return 'Adult';
    else return 'Elder';
  } else {
    return 'Unknown'; // If neither dog nor cat
  }
}

// Fetch data from the API
fetch(url)
  .then(response => {
    return response.json(); // Parse JSON data
  })
  .then(data => {
    console.log("Animals:", data[0]['animal_id']); // Log the data
    const rdata = data.reverse(); 

    // Add age category to each animal
    rdata.forEach(animal => {
      animal.ageCategory = categorizeAge(animal.age, animal.species);
    });

    res.render('index', { title: 'Pet-Friend Shelter', animal: rdata[0], animal1: rdata[1], animal2: rdata[2] });
    
  })
  .catch(error => {
    console.error("Error fetching animals:", error);
  });
});

module.exports = router;
 