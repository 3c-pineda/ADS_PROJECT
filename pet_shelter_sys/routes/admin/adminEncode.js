var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('admin/adminEncode', { title: 'Admin - Encoding Page' });
});

router.post('/', function(req, res) {
// Perform a PUT request using fetch API
fetch(url, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer yourAuthToken' // Replace with actual authorization if needed
  },
  body: JSON.stringify(requestData) // Convert the data to JSON before sending
})
  .then(response => response.json()) // Parse the JSON response
  .then(data => {
    console.log('Success:', data); // Handle success
  })
  .catch(error => {
    console.error('Error:', error); // Handle error
  });

});
module.exports = router;
