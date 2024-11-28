var express = require('express');
var router = express.Router();

/* GET home page. */

router.get('/', function(req, res, next) {
  res.render('contactUs', { title: 'Contact Us' });
});

router.post('/', async function(req, res) {
  let name = req.body.name;
  let email = req.body.email;
  let subject = req.body.subject;
  let reason = req.body.reason;
  let description = req.body.description;
  console.log(name);
  console.log(email);
  console.log(subject);
  console.log(reason);
  console.log(description);
  let response = await fetch('http://localhost:5000/api/contact-us', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name, email, subject, reason, description })
  });
  res.redirect(301, 'http://localhost:3000/contactUs');
});

module.exports = router;
