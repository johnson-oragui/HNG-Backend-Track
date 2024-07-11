Project Name: Simple Weather App API (Express.js Edition)

Description:

This Node.js project provides a RESTful API built with Express.js to retrieve and display location-based weather information. The application utilizes various libraries to:

Extract the user's IP address.
Geolocate the user's IP to determine their approximate location (city and country).
Fetch weather data (temperature in Celsius) for the user's location using the OpenWeatherMap API (requires an API key).
Installation:

Prerequisites: Ensure you have Node.js and npm (Node Package Manager) installed. You can verify their versions using:

Bash
node -v
npm -v

Clone the Repository:
If you're using Git, clone this repository using the following command:


git clone https://github.com/johnson-oragui/HNG-Backend-Track.git

Install Dependencies:
Navigate to the project directory and install the required libraries using npm:

npm install express geoip-lite dotenv request


Configuration:

OpenWeatherMap API Key:
This project requires an API key from OpenWeatherMap to access weather data. Obtain a free API key by registering on their website (https://openweathermap.org/).

Environment Variables: Create a file named .env in your project's root directory with the following line, replacing YOUR_API_KEY with your actual API key:

API_KEY=YOUR_API_KEY

Running the Application:

Start the Development Server:
Execute the following command from the project's root directory:


npm start

This will start the development server, running at http://localhost:5000/

API Endpoints:

The application provides a single API endpoint:

/hello (GET):

Accepts an optional query parameter visitor_name to personalize the greeting message.
Retrieves the user's IP address, geolocates it (city and country), and fetches weather data from OpenWeatherMap (temperature in Celsius).
Returns a JSON response containing:
client_ip: User's IP address.
location: User's approximate location (city and country).
greeting: Personalized greeting message with the retrieved temperature.

Returns a 404 error if geolocation or weather data retrieval fails.
Example Usage:

Without visitor_name parameter:

curl http://localhost:3000/hello

With visitor_name parameter:

curl http://localhost:3000/hello?visitor_name=Johnson
Testing:

Yet to write a unittest for this.

Deployment:

For deploying to a production environment, you'll need to configure the appropriate web server (e.g., nginx) and handle potential security considerations.

AUTHOR:
Johnson Oragui <johnson.oragui@gmail.com>

