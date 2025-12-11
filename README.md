Medical REST API
A CRUD REST API built with Flask and MySQL for managing medical data.
Supports JSON and XML output formats and includes JWT authentication for secure endpoints.

Project Description
This project implements a REST API for a medical database containing diagnoses, doctors, patients, and assignments.
It allows users to create, read, update, and delete records, search for specific entries, and export data in JSON or XML format.

Key Features:

CRUD operations for diagnoses, doctors, patients, and assignments
Search functionality for diagnoses, doctors, and patients
Secure endpoints using JWT authentication
JSON or XML output formatting
Fully tested endpoints (manual/Postman or automated)
Installation Instructions

Clone the repository:
git clone 
cd medical-rest-api 
pip install -r requirements.txt

Set up your MySQL database:
DB_HOST=localhost DB_USER=root DB_PASS=your_password DB_NAME=mydb SECRET_KEY=your_secret_key


Install Requirements
python -m venv venv
venv\Scripts\activate 
pip install -r requirements.txt 
pip install flask mysql-connector-python dicttoxml pyjwt

Run the Flask API server:
python app.py

Usage Examples
Login POST /login Content-Type: application/json

{ "username": "admin", "password": "1234" }

Response:

{ "token": "jwt_token_here" }

Get All Diagnoses GET /diagnosis?format=json Authorization: Bearer

Response:

[ {"id": 1, "diagnosis_name": "Flu", "category": "Viral"}, {"id": 2, "diagnosis_name": "Diabetes", "category": "Chronic"} ]

Create a New Patient POST /patients Authorization: Bearer Content-Type: application/json

{ "name": "John Doe", "age": 45, "diagnosis_id": 2 }

API Endpoints
Endpoint Method Description JWT Required Params/Body /login POST Login and get JWT token No JSON: username, password /diagnosis GET Get all diagnoses No ?format=json/xml /diagnosis/ GET Get single diagnosis No id in URL /diagnosis POST Create diagnosis Yes JSON: diagnosis_name, category /diagnosis/ PUT Update diagnosis Yes JSON: diagnosis_name, category /diagnosis/ DELETE Delete diagnosis Yes id in URL /patients GET Get all patients No ?format=json/xml /patients/ GET Get single patient No id in URL /patients POST Create patient Yes JSON: name, age, diagnosis_id /patients/ PUT Update patient Yes JSON: name, age, diagnosis_id /patients/ DELETE Delete patient Yes id in URL /assignments GET Get all assignments No ?format=json/xml /assignments POST Create assignment Yes JSON: doctor_id, patient_id, diagnosis_id /assignments DELETE Delete assignment Yes Query: doctor_id, patient_id, diagnosis_id Running Tests

You can test endpoints using Postman or curl.

RUNNING TEST
pytest tests/
