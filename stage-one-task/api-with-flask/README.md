Simple Weather App API

Description

This Python project provides a Flask application that offers a single API endpoint (/hello) to retrieve and display location-based weather information. The application utilizes the geocoder and requests libraries to:

Extract the user's IP address.
Geolocate the user's IP to determine their approximate location (city and country).
Fetch weather data (temperature in Celsius) for the user's location using the OpenWeatherMap API (requires an API key).

Installation

Prerequisites: Ensure you have Python 3 and pip (the package manager for Python) installed.

Clone the Repository: If you're using Git, clone this repository using the following command:

git clone https://github.com/johnson-oragui/HNG-Backend-Track.git

Create a Virtual Environment (Optional but Recommended): It's highly recommended to create a virtual environment to isolate project dependencies. Here's an example using venv:

python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat  # Windows


Install Dependencies: Inside the virtual environment, install the required libraries using pip:

pip install Flask requests geocoder python_dotenv

Configuration

1. OpenWeatherMap API Key: This project requires an API key from OpenWeatherMap to access weather data. Obtain a free API key by registering on their website (https://openweathermap.org/).

2. Environment Variables: Create a file named .env in your project's root directory with the following line, replacing YOUR_API_KEY with your actual API key:

API_KEY=YOUR_API_KEY

Running the Application

Activate Virtual Environment (if applicable): If you created a virtual environment, activate it before running the application.

Start the Flask Development Server: Execute the following command from the project's root directory:

python -m api.app


This will start the Flask development server, typically running at http://127.0.0.1:5000/ (the default port for Flask development servers).

API Endpoint

The application provides a single API endpoint:

/hello (GET):
Accepts an optional query parameter visitor_name to personalize the greeting message.
Retrieves the user's IP address, geolocates it (city and country), and fetches weather data from OpenWeatherMap (temperature in Celsius).
Returns a JSON response containing:
client_ip: User's IP address.
location: User's approximate location (city and country).
greeting: Personalized greeting message with the retrieved temperature.
Returns a 404 error if geolocation or weather data retrieval fails.

Example Usage

# Without visitor_name parameter
curl http://127.0.0.1:5000/hello

# With visitor_name parameter
curl http://127.0.0.1:5000/hello?visitor_name=John

Testing

The project doesn't include dedicated test files, but you can use testing frameworks like pytest to write unit tests for the user_locate function and other critical parts of your application.

Further Considerations

Error Handling: Consider adding more specific error handling for different types of exceptions or API failures.
Security: Remember to exclude the .env file from version control to avoid exposing your API key.
Documentation: You can extend the docstrings for functions like user_locate to provide more details about their behavior and parameters.
Deployment: For deployment to a production environment, you'll need to configure the appropriate web server (e.g., Gunicorn)
