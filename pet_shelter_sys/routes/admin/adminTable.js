var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('admin/adminTable', { title: 'Admin - Table Page' });
});

module.exports = router;
