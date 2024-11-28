var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('admin/adminDelete', { title: 'Admin - Delete Page' });
});

module.exports = router;
