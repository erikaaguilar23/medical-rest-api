CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;

DROP TABLE IF EXISTS doctors_has_patient;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS diagnosis;

CREATE TABLE diagnosis (
  idDiagnosis int NOT NULL AUTO_INCREMENT,
  diagnosis_name varchar(45) NOT NULL,
  category varchar(45) NOT NULL,
  PRIMARY KEY (idDiagnosis)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO diagnosis (idDiagnosis, diagnosis_name, category) VALUES
(1,'hypertension','cardiovascular'),
(2,'asthma','respiratory'),
(3,'migraine','neurological'),
(4,'diabetes','endocrine'),
(5,'chickenpox','infection');

CREATE TABLE doctors (
  iddoctors int NOT NULL AUTO_INCREMENT,
  doctor_name varchar(45) NOT NULL,
  specialization varchar(45) NOT NULL,
  PRIMARY KEY (iddoctors)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO doctors (iddoctors, doctor_name, specialization) VALUES
(1,'marc rebbit','cardiology'),
(2,'raymart diaz','pediatrics'),
(3,'axel flores','neurology'),
(4,'eden rose','pulmonology');

CREATE TABLE patient (
  idPatient int NOT NULL AUTO_INCREMENT,
  name varchar(45) NOT NULL,
  age varchar(45) NOT NULL,
  Diagnosis_idDiagnosis int NOT NULL,
  PRIMARY KEY (idPatient, Diagnosis_idDiagnosis),
  KEY fk_Patient_Diagnosis_idx (Diagnosis_idDiagnosis),
  CONSTRAINT fk_Patient_Diagnosis FOREIGN KEY (Diagnosis_idDiagnosis) REFERENCES diagnosis (idDiagnosis)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO patient (idPatient, name, age, Diagnosis_idDiagnosis) VALUES
(1,'erika','22',1),
(2,'zyra','25',2),
(3,'jacob','40',3),
(4,'rabang','30',4);

CREATE TABLE doctors_has_patient (
  doctors_iddoctors int NOT NULL,
  Patient_idPatient int NOT NULL,
  Patient_Diagnosis_idDiagnosis int NOT NULL,
  PRIMARY KEY (doctors_iddoctors, Patient_idPatient, Patient_Diagnosis_idDiagnosis),
  KEY fk_doctors_has_Patient_Patient1_idx (Patient_idPatient, Patient_Diagnosis_idDiagnosis),
  KEY fk_doctors_has_Patient_doctors1_idx (doctors_iddoctors),
  CONSTRAINT fk_doctors_has_Patient_doctors1 FOREIGN KEY (doctors_iddoctors) REFERENCES doctors (iddoctors),
  CONSTRAINT fk_doctors_has_Patient_Patient1 FOREIGN KEY (Patient_idPatient, Patient_Diagnosis_idDiagnosis) REFERENCES patient (idPatient, Diagnosis_idDiagnosis)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO doctors_has_patient (doctors_iddoctors, Patient_idPatient, Patient_Diagnosis_idDiagnosis) VALUES
(1,1,1),(2,2,2),(3,3,3),(4,4,4);
