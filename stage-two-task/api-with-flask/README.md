HNG Stage 2 Backend Task: User Authentication & Organisation API

This project implements a RESTful API using Flask and PostgreSQL for user authentication and organisation management.

Installation

Prerequisites: Ensure you have Python 3 and pip (the package manager for Python) installed.

Clone the Repository:
If you're using Git, clone this repository using the following command:

git clone https://github.com/johnson-oragui/HNG-Backend-Track.git

change Directory to stage-two-task

Install Dependencies::

pip install -r requirements.txt

Configuration

Environment Variables: Create a file named .env in your project's root directory with the following line, replacing DB_NAME, DB_PWD, DB_HOST, DB_USER with your actual DB_NAME, DB_PWD, DB_HOST, DB_USER:

Setup

 Database Setup:
   - Connect your application to a PostgreSQL database.
   - Ensure ORM integration if chosen (optional).

DB_NAME=<some database name>
DB_PWD=<some password>
DB_HOST=<some host>
DB_USER=<some userame>

Running the Application

Start the Flask Development Server:
Execute the following command from the project's root directory:


Create Tables:
create a file:
# create_table.py
from models import DBStorage

with DBStorage() as sess:
    sess.creat_tables()

run the file.
python3 -m create_table

This will map the models to the database and create the Tables.

python3 -m api.run

This will start the Flask development server, running at http://127.0.0.1:5000/


2. User Model:
   - Define a user model with the following properties:

     {
         "userId": "string", // Unique
         "firstName": "string", // Required
         "lastName": "string", // Required
         "email": "string", // Unique, Required
         "password": "string", // Required
         "phone": "string"
     }

   - Implement validation for all fields.

3. User Authentication:
   - Implement JWT-based authentication.
   - Hash passwords before storing in the database.

4. Organisation Model:
   - Define an organisation model with:
     {
         "orgId": "string", // Unique
         "name": "string", // Required
         "description": "string"
     }


Endpoints:

User Registration

- POST `api/auth/register`
  - Registers a new user and creates a default organisation.
  - Request body:
    {
        "firstName": "string", // Required
        "lastName": "string", // Required
        "email": "string", // Required, Unique
        "password": "string", // Required
        "phone": "string"
    }

  - Successful response (201):
    {
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": "eyJh...",
            "user": {
                "userId": "string",
                "firstName": "string",
                "lastName": "string",
                "email": "string",
                "phone": "string"
            }
        }
    }


User Login

- POST `api/auth/login`
  - Logs in a user.
  - Request body:
    {
        "email": "string", // Required
        "password": "string" // Required
    }

  - Successful response (200):
    {
        "status": "success",
        "message": "Login successful",
        "data": {
            "accessToken": "eyJh...",
            "user": {
                "userId": "string",
                "firstName": "string",
                "lastName": "string",
                "email": "string",
                "phone": "string"
            }
        }
    }


User Details

- GET `/api/users/:id`
  - Retrieves user details.
  - Protected endpoint.

Organisation Management

- GET `/api/organisations`
  - Retrieves all organisations belonging to the logged-in user.
  - Protected endpoint.

- GET `/api/organisations/:orgId`
  - Retrieves details of a specific organisation.
  - Protected endpoint.

- POST `/api/organisations`
  - Creates a new organisation.
  - Request body:
    {
        "name": "string", // Required
        "description": "string"
    }

  - Successful response (201):
    {
        "status": "success",
        "message": "Organisation created successfully",
        "data": {
            "orgId": "string",
            "name": "string",
            "description": "string"
        }
    }


- POST `/api/organisations/:orgId/users`
  - Adds a user to a specific organisation.
  - Request body:
    {
        "userId": "string" // Required
    }

  - Successful response (200):
    {
        "status": "success",
        "message": "User added to organisation successfully"
    }


Testing

- Unit Tests:
  - Cover token generation and expiry.
  - Ensure users can only access permitted organisation data.

- End-to-End Tests:
  - Test `POST /auth/register` for successful registration, validation errors, and database constraints.

Directory Structure

api/
api/__init__.py
api/app
api/app/__init__.py
api/config.py
api/run.py
api/app/routes
api/app/routes/__init__.py
api/app/routes/auth.py
api/app/routes/dashboard.py
api/app/routes/organisation.py

models/
models/__init__.py
models/base.py
models/user.py
models/organisation.py
models/user_organisation.py
models/db_engine
models/db_engine/__init__.py
models/db_engine/db_engine.py

tests/
tests/__init__.py
tests/test_auth_spec.py
tests/test_auth_manager.py
tests/test_db_engine/__init__.py
tests/test_db_engine/test_db_storage.py

utils/
utils/__init__.py
utils/auth_manager.py
utils/validate_data.py

__init__.py

How to Submit

Host your API on a free hosting service and submit the base URL of your endpoints
`https://hng-task2.randommallstudio.tech`.

Submission Deadline: Sunday 7th July, 2024 at 11:59 PM GMT.
