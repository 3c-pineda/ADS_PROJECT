var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('admin/adminDelete', { title: 'Admin - Delete Page' });
});

router.post('/', async function(req, res) {
  let animal_id = req.body.animal_id;
  let method = req.body.method;
  let animal_name = req.body.animal_name;
  if ( method === 'POST') {
    console.log(`animal id: ${animal_id}`);
    res.render('admin/adminDelete', { title: 'Admin - Delete Page', animal_id: animal_id, animal_name: animal_name });
  } else {
    const url = `http://localhost:5000/api/animals/${animal_id}`;
    console.log(url);
    let response = await fetch(url,
      {
        method: 'DELETE'
      }
    );
    let data = await response.json();
    if (response.ok) {
      res.redirect('http://localhost:3000/admin/adminTable');
    } else {
      console.log(data);
      res.status(500).send('Something went wrong. Please try again later.');
    }
  }
});

module.exports = router;
