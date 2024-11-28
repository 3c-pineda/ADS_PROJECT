var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('admin/adminLogin', { title: 'Admin - Login' });
});

router.post('/', async function (req, res) {
    let username = req.body.username;
    let password = req.body.password;

    // Logic for checking username and password (like before)
    let response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    let data = await response.json();

    if (response.ok) {
        // Pass success message to the EJS template
        res.render('admin/adminLogin', { title: 'Admin - Login', message: 'Login successful' });
    } else {
        // Pass error message to the EJS template
        res.render('admin/adminLogin', { title: 'Admin - Login', error: 'Wrong username or password' });
    }
});

module.exports = router;