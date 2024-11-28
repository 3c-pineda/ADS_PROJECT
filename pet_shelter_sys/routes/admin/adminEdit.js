var express = require('express');
var router = express.Router();
const multer = require('multer');
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

/* GET home page. */
router.get('/:animal_id', async function(req, res) {
  const { animal_id } = req.params;
  let response = await fetch(`http://localhost:5000/api/animals/${animal_id}`);
  if (!response.ok) {
    return res.status(500).send(`message: ${response}`);
  }
  let data = await response.json();
  // Format the arrival_date to YYYY-MM-DD if it's a Date object
  if (data) {
    data.arrival_date = new Date(data.arrival_date).toISOString().split('T')[0];
    data.adoption_date = new Date(data.adoption_date).toISOString().split('T')[0];
    data.birthday = new Date(data.birthday).toISOString().split('T')[0];
    data.vacc_date = new Date(data.vacc_date).toISOString().split('T')[0];
  }
  res.render('admin/adminEdit', { title: 'Admin - Edit/Modify Page', animal: data });
});

router.post('/:animal_id', upload.single('profpic'), async function(req, res) {
  const { animal_id } = req.params;
  const apiEndpoint = `http://localhost:5000/api/animals/${animal_id}`;
  try {
    // Get other form data
    const animalData = req.body;  // This contains the other form fields
    const formData = new FormData();

    // Check if an image was uploaded
    if (req.file) {
      // Create a Blob from the buffer and specify the MIME type for the image
      const imgBlob = new Blob([req.file.buffer], { type: req.file.mimetype });
      // Append the image as a Blob, passing the original filename as the third argument
      formData.append('image', imgBlob, req.file.originalname);
    }

    // Append the other form fields to the FormData object
    Object.keys(animalData).forEach(key => {
      formData.append(key, animalData[key]);
    });

    console.log(formData);
    // Send the form data (image and fields) to the external API
    const response = await fetch(apiEndpoint, {
      method: 'PUT',  // Use PUT for updating the animal data
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      return res.status(response.status).json({ error: errorData });
    } else {
      const result = await response.json();
      console.log(result);
      return res.redirect(301, 'http://localhost:3000/admin/adminTable');
    }
  } catch (error) {
    console.error("Error updating animal:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
});


module.exports = router;
