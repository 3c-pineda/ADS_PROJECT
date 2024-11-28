var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', async function(req, res, next) {
  let response = await fetch ('http://localhost:5000/api/animal-about');
  let data = await response.json();
  console.log(data);

  let response1 = await fetch ('http://localhost:5000/api/animals');
  let data1 = await response1.json();
  console.log(data1);

  let adopted_number = data.length; 
  let rescued_number = data1.length;
  res.render('aboutUs', { title: 'About Us', adopted_number: adopted_number, rescued_number: rescued_number });
});

module.exports = router;
