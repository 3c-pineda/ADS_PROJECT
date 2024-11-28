var express = require('express');
var router = express.Router();

/* GET home page. */

router.get('/', function(req, res, next) {
  res.render('petDesc', { title: 'Pet Description' });
});

module.exports = router;
