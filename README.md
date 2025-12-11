## Medical REST API (Flask & MySQL)

Project Description

This project is a CRUD REST API for managing hospital data, including patients, doctors, diagnoses, and assignments.
The API supports JSON and XML responses, JWT authentication, and comes with automated tests for all endpoints.
It is designed to act as an interface for clients that understand JSON or XML and to demonstrate secure and tested API development.

## Installation Instructions

Clone the repository
git clone https://github.com/erikaaguilar23/medical-rest-api.git
cd medical-rest-api

## Create a virtual environment
python -m venv venv

##Activate the virtual environment
source venv/Scripts/activate

## Install dependencies
pip install -r requirements.txt

## MySQL Database Setup

Create the database:

CREATE DATABASE hospital;
USE hospital;


Create tables (examples):

CREATE TABLE diagnosis (
    idDiagnosis INT AUTO_INCREMENT PRIMARY KEY,
    diagnosis_name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL
);

CREATE TABLE doctors (
    iddoctors INT AUTO_INCREMENT PRIMARY KEY,
    doctor_name VARCHAR(255) NOT NULL,
    specialization VARCHAR(255) NOT NULL
);

CREATE TABLE patient (
    idPatient INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    Diagnosis_idDiagnosis INT,
    FOREIGN KEY (Diagnosis_idDiagnosis) REFERENCES diagnosis(idDiagnosis)
);

CREATE TABLE doctors_has_patient (
    doctors_iddoctors INT,
    Patient_idPatient INT,
    Patient_Diagnosis_idDiagnosis INT,
    PRIMARY KEY (doctors_iddoctors, Patient_idPatient),
    FOREIGN KEY (doctors_iddoctors) REFERENCES doctors(iddoctors),
    FOREIGN KEY (Patient_idPatient) REFERENCES patient(idPatient)
);

## Running the API
Activate your virtual environment if not already active.

## Run the Flask app:
pthon app.py

By default, the API will run at:
http://127.0.0.1:5000/

## API Endpoints
Authentication

POST /login
Request Body: { "username": "admin", "password": "1234" }
Response: { "token": "JWT_TOKEN_HERE" }

Diagnosis

GET /diagnosis – list all diagnoses
Optional format: /diagnosis?format=xml or ?format=json

GET /diagnosis/<id> – get diagnosis by ID

POST /diagnosis – create diagnosis (requires JWT)

PUT /diagnosis/<id> – update diagnosis (requires JWT)

DELETE /diagnosis/<id> – delete diagnosis (requires JWT)

Doctors

GET /doctors – list all doctors

GET /doctors/<id> – get doctor by ID

POST /doctors – create doctor (requires JWT)

Patients

GET /patients – list all patients, optionally in XML or JSON

Assignments

GET /assignments – list assignments linking doctors and patients

JWT Authentication
Use the token received from /login in the Authorization header
Authorization: Bearer <JWT_TOKEN>


Required for POST, PUT, DELETE endpoints.

Example Requests
# Login
curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username":"admin","password":"1234"}'

# Get diagnoses in JSON
curl http://127.0.0.1:5000/diagnosis?format=json

# Get patients in XML
curl http://127.0.0.1:5000/patients?format=xml

## Running Tests
Make sure the virtual environment is active.

## Run all tests
pytest -v
pytest tests/

Tests cover all CRUD operations, error handling, and format options (JSON/XML).

