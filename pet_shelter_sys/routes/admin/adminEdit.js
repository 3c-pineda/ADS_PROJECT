var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', async function(req, res) {
  res.render('admin/adminEdit', { title: 'Admin - Edit/Modify Page' });
});

router.post('/', async function(req, res) {});

module.exports = router;
