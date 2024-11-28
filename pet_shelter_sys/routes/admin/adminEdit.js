var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('admin/adminEdit', { title: 'Admin - Edit/Modify Page' });
});

module.exports = router;
