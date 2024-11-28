var express = require('express');
var router = express.Router();

/* GET home page. */

router.get('/:animal_id', async function(req, res, next) {
const { animal_id } = req.params;
  // let animal_id = req.body.animal_id;
  const url = `http://localhost:5000/api/animals/${animal_id}`;
  let response = await fetch(url);
  let data = await response.json();
  console.log(data);
  res.render('petDesc', { title: 'Pet Description', animal: data});
});


module.exports = router;
