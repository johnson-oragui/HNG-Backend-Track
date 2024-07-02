const express = require('express');
const HelloController = require('../controllers/helloController');

router = express.Router();

router.get('/api/hello', HelloController.hello)

module.exports = router;
