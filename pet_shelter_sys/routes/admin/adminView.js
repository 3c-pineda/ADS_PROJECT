var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
res.render('admin/adminView', { title: 'Admin - View Page' });
});

router.post ('/', async function (req, res) {
  let animal_id = req.body.animal_id;
  const url = `http://localhost:5000/api/animals/${animal_id}`;
  let response = await fetch(url);
  let data = await response.json();
  console.log(data);
  res.render('admin/adminView', { title: 'Admin - View Page', animal: data});
});

module.exports = router;
