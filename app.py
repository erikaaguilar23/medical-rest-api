import os
import datetime
from functools import wraps
from flask import Flask, request, jsonify, make_response
import mysql.connector
import dicttoxml
import jwt

# -------------------------
# FLASK APP CONFIG
# -------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "please_change_this_secret_for_prod")
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

# -------------------------
# DATABASE CONNECTION
# -------------------------
def db_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "110515"),
        database=os.getenv("DB_NAME", "hospital"),
        auth_plugin=os.getenv("DB_AUTH_PLUGIN", "mysql_native_password")
    )

# -------------------------
# JWT AUTHENTICATION
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username & password required"}), 400

    if username == "admin" and password == "1234":
        payload = {
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return jsonify({"token": token})
    return jsonify({"error": "invalid credentials"}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header:
            return jsonify({"error": "Token missing!"}), 401
        token = auth_header.split(" ")[1].strip() if auth_header.startswith("Bearer ") else auth_header.strip()
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return decorated

# -------------------------
# RESPONSE FORMAT
# -------------------------
def format_response(data, fmt):
    if fmt == "xml":
        xml = dicttoxml.dicttoxml(data, custom_root="response", attr_type=False)
        response = make_response(xml)
        response.headers["Content-Type"] = "application/xml"
        return response
    return jsonify(data)

# -------------------------
# DIAGNOSIS
# -------------------------
@app.route("/diagnosis", methods=["GET"])
def get_diagnoses():
    fmt = request.args.get("format", "json")
    term = request.args.get("search")
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        if term:
            cursor.execute("SELECT idDiagnosis AS id, diagnosis_name, category FROM diagnosis WHERE diagnosis_name LIKE %s", (f"%{term}%",))
        else:
            cursor.execute("SELECT idDiagnosis AS id, diagnosis_name, category FROM diagnosis")
        result = cursor.fetchall()
        return format_response(result, fmt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close(); conn.close()

# ... (keep existing GET single, POST, PUT, DELETE for diagnosis) ...

# -------------------------
# DOCTORS
# -------------------------
@app.route("/doctors", methods=["GET"])
def get_doctors():
    fmt = request.args.get("format", "json")
    term = request.args.get("search")
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        if term:
            cursor.execute("SELECT iddoctors AS id, doctor_name, specialization FROM doctors WHERE doctor_name LIKE %s", (f"%{term}%",))
        else:
            cursor.execute("SELECT iddoctors AS id, doctor_name, specialization FROM doctors")
        rows = cursor.fetchall()
        return format_response(rows, fmt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close(); conn.close()

# ... (keep existing GET single, POST for doctors) ...

# -------------------------
# PATIENTS CRUD
# -------------------------
@app.route("/patients", methods=["GET"])
def get_patients():
    fmt = request.args.get("format", "json")
    term = request.args.get("search")
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        if term:
            cursor.execute("""
                SELECT p.idPatient AS id, p.name, p.age, p.Diagnosis_idDiagnosis AS diagnosis_id,
                       d.diagnosis_name AS diagnosis_name
                FROM patient p
                LEFT JOIN diagnosis d ON p.Diagnosis_idDiagnosis = d.idDiagnosis
                WHERE p.name LIKE %s
            """, (f"%{term}%",))
        else:
            cursor.execute("""
                SELECT p.idPatient AS id, p.name, p.age, p.Diagnosis_idDiagnosis AS diagnosis_id,
                       d.diagnosis_name AS diagnosis_name
                FROM patient p
                LEFT JOIN diagnosis d ON p.Diagnosis_idDiagnosis = d.idDiagnosis
            """)
        rows = cursor.fetchall()
        return format_response(rows, fmt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close(); conn.close()

@app.route("/patients", methods=["POST"])
@token_required
def create_patient():
    data = request.get_json() or {}
    name = data.get("name")
    age = data.get("age")
    diagnosis = data.get("diagnosis_id")
    if not name or age is None:
        return jsonify({"error": "name and age required"}), 400
    try:
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patient (name, age, Diagnosis_idDiagnosis) VALUES (%s,%s,%s)",
            (name, age, diagnosis)
        )
        conn.commit()
        return jsonify({"message": "Patient created", "id": cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close(); conn.close()

@app.route("/patients/<int:id>", methods=["PUT"])
@token_required
def update_patient(id):
    data = request.get_json() or {}
    name = data.get("name")
    age = data.get("age")
    diagnosis = data.get("diagnosis_id")
    if not name or age is None:
        return jsonify({"error": "name and age required"}), 400
    try:
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE patient SET name=%s, age=%s, Diagnosis_idDiagnosis=%s WHERE idPatient=%s",
                       (name, age, diagnosis, id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Patient not found"}), 404
        return jsonify({"message": "Patient updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close(); conn.close()

@app.route("/patients/<int:id>", methods=["DELETE"])
@token_required
def delete_patient(id):
    try:
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patient WHERE idPatient=%s", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Patient not found"}), 404
        return jsonify({"message": "Patient deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close(); conn.close()

# -------------------------
# ASSIGNMENTS CRUD
# -------------------------
@app.route("/assignments", methods=["GET"])
def get_assignments():
    fmt = request.args.get("format", "json")
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT dhp.doctors_iddoctors AS doctor_id,
                   doc.doctor_name,
                   dhp.Patient_idPatient AS patient_id,
                   pat.name AS patient_name,
                   dhp.Patient_Diagnosis_idDiagnosis AS diagnosis_id
            FROM doctors_has_patient dhp
            LEFT JOIN doctors doc ON dhp.doctors_iddoctors = doc.iddoctors
            LEFT JOIN patient pat ON dhp.Patient_idPatient = pat.idPatient
        """)
        rows = cursor.fetchall()
        return format_response(rows, fmt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close(); conn.close()

@app.route("/assignments", methods=["POST"])
@token_required
def create_assignment():
    data = request.get_json() or {}
    doc_id = data.get("doctor_id")
    pat_id = data.get("patient_id")
    diag_id = data.get("diagnosis_id")
    if not doc_id or not pat_id:
        return jsonify({"error": "doctor_id and patient_id required"}), 400
    try:
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO doctors_has_patient (doctors_iddoctors, Patient_idPatient, Patient_Diagnosis_idDiagnosis)
            VALUES (%s, %s, %s)
        """, (doc_id, pat_id, diag_id))
        conn.commit()
        return jsonify({"message": "Assignment created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close(); conn.close()

@app.route("/assignments", methods=["DELETE"])
@token_required
def delete_assignment():
    doc_id = request.args.get("doctor_id")
    pat_id = request.args.get("patient_id")
    if not doc_id or not pat_id:
        return jsonify({"error": "doctor_id and patient_id required"}), 400
    try:
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM doctors_has_patient
            WHERE doctors_iddoctors=%s AND Patient_idPatient=%s
        """, (doc_id, pat_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Assignment not found"}), 404
        return jsonify({"message": "Assignment deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close(); conn.close()

# -------------------------
# ROOT
# -------------------------
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Medical REST API — endpoints: /login, /diagnosis, /doctors, /patients, /assignments"})

if __name__ == "__main__":
    app.run(debug=True)
