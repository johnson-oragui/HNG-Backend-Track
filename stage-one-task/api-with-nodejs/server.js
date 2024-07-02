const dotenv = require('dotenv');
const express = require('express');
const router = require('./routes/routes');

dotenv.config()

const PORT = process.env.PORT || 5001;

const server = express();

// will retrieve ip if not forwarded and when forwarded if express app is behind
// a reverse proxy like nginx
server.set('trust proxy', true);

server.use(express.urlencoded({ extended: true }));

server.use('/', router);

server.listen(PORT, () => {
    console.log(`server running on http://localhost:${PORT}/api/hello`)
});
