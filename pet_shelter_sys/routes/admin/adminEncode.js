var express = require('express');
var router = express.Router();
const multer = require('multer');
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('admin/adminEncode', { title: 'Admin - Encoding Page' });
});


router.post('/', upload.single('profpic'), async (req, res) => {
  const apiEndpoint = 'http://localhost:5000/api/animals';

  try {
      if (!req.file) {
          return res.status(400).json({ error: 'No image uploaded' });
      }

      const animalData = req.body;  // This contains the other form fields
      const formData = new FormData();
      
      // Create a Blob from the buffer and specify the MIME type
      const imgBlob = new Blob([req.file.buffer], { type: req.file.mimetype });
      
      // Append the image as a Blob, passing the original filename as the third argument
      formData.append('image', imgBlob, req.file.originalname);
      
      // Append the other form fields
      Object.keys(animalData).forEach(key => {
          formData.append(key, animalData[key]);
      });

      const response = await fetch(apiEndpoint, {
          method: 'POST',
          body: formData,
      });

      if (!response.ok) {
          const errorData = await response.json();
          return res.status(response.status).json({ error: errorData });
      } else {
          const result = await response.json();
          return res.redirect(301, 'http://localhost:3000/admin/adminTable');
      }
  } catch (error) {
      console.error("Error creating animal:", error);
      return res.status(500).json({ error: "Internal server error" });
  }
});



module.exports = router;
