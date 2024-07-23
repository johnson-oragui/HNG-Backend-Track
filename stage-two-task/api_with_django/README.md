HNG Stage 2 Backend Task: User Authentication & Organisation API.

This project implements a RESTful API using Django and PostgreSQL for user authentication and organisation management.

Installation

Prerequisites: Ensure you have Python 3 and pip (the package manager for Python) installed.

Clone the Repository:
If you're using Git, clone this repository using the following command:

git clone https://github.com/johnson-oragui/HNG-Backend-Track.git


Install Dependencies:
Inside the virtual environment, install the required libraries using pip:

pip install drf-yasg swagger-ui pyyaml django-swagger-ui

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

Start the Django Development Server:
Execute the following command from the project's root directory:

Change directory into api.
cd api

Run Migrations:
python3 manage.py makemigrations
python3 manage.py migrate

This will map the models to the database.

python3 manage.py runserver

This will start the Django development server, typically running at http://127.0.0.1:8000/ (the default port for Django development servers).


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

- POST `/auth/register`
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

- POST `/auth/login`
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


project_root/
│
├── api/
│   ├── authentication/
│   ├── user/
│   ├── user_organisation/
│   ├── organisation
│
├── manage.py
└── README.md


How to Submit

Host your API on a free hosting service and submit the base URL of your endpoints
`https://hng-task2.randommallstudio.tech`.

Submission Deadline: Sunday 7th July, 2024 at 11:59 PM GMT.

