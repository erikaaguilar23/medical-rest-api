# app.py
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
    """
    Create a MySQL connection with safe defaults.
    """
    auth_plugin = os.getenv("DB_AUTH_PLUGIN", "mysql_native_password")
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "110515"),
        database=os.getenv("DB_NAME", "hospital"),
        auth_plugin=auth_plugin
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
    # Hardcoded demo auth
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
# RESPONSE FORMATTER
# -------------------------
def format_response(data, fmt):
    if fmt == "xml":
        xml = dicttoxml.dicttoxml(data, custom_root="response", attr_type=False)
        response = make_response(xml)
        response.headers["Content-Type"] = "application/xml"
        return response
    return jsonify(data)

# -------------------------
# DIAGNOSIS ROUTES
# -------------------------
@app.route("/diagnosis", methods=["GET"])
def get_diagnoses():
    fmt = request.args.get("format", "json")
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT idDiagnosis AS id, diagnosis_name, category FROM diagnosis")
        result = cursor.fetchall()
        return format_response(result, fmt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try: cursor.close(); conn.close()
        except: pass

@app.route("/diagnosis/<int:id>", methods=["GET"])
def get_diagnosis(id):
    fmt = request.args.get("format", "json")
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT idDiagnosis AS id, diagnosis_name, category FROM diagnosis WHERE idDiagnosis=%s", (id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Diagnosis not found"}), 404
        return format_response(result, fmt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try: cursor.close(); conn.close()
        except: pass

@app.route("/diagnosis", methods=["POST"])
@token_required
def create_diagnosis():
    data = request.get_json() or {}
    name = data.get("diagnosis_name")
    category = data.get("category")
    if not name or not category:
        return jsonify({"error": "diagnosis_name and category are required"}), 400
    try:
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO diagnosis (diagnosis_name, category) VALUES (%s, %s)", (name, category))
        conn.commit()
        return jsonify({"message": "Diagnosis created", "id": cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try: cursor.close(); conn.close()
        except: pass

@app.route("/diagnosis/<int:id>", methods=["PUT"])
@token_required
def update_diagnosis(id):
    data = request.get_json() or {}
    name = data.get("diagnosis_name")
    category = data.get("category")
    if not name or not category:
        return jsonify({"error": "diagnosis_name and category are required"}), 400
    try:
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE diagnosis SET diagnosis_name=%s, category=%s WHERE idDiagnosis=%s", (name, category, id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Diagnosis not found"}), 404
        return jsonify({"message": "Diagnosis updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try: cursor.close(); conn.close()
        except: pass

@app.route("/diagnosis/<int:id>", methods=["DELETE"])
@token_required
def delete_diagnosis(id):
    try:
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diagnosis WHERE idDiagnosis=%s", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Diagnosis not found"}), 404
        return jsonify({"message": "Diagnosis deleted"})
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Cannot delete diagnosis - referenced by patients"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try: cursor.close(); conn.close()
        except: pass

# -------------------------
# DOCTORS ROUTES
# -------------------------
@app.route("/doctors", methods=["GET"])
def get_doctors():
    fmt = request.args.get("format", "json")
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT iddoctors AS id, doctor_name, specialization FROM doctors")
        result = cursor.fetchall()
        return format_response(result, fmt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try: cursor.close(); conn.close()
        except: pass

@app.route("/doctors/<int:id>", methods=["GET"])
def get_doctor(id):
    fmt = request.args.get("format", "json")
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT iddoctors AS id, doctor_name, specialization FROM doctors WHERE iddoctors=%s", (id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Doctor not found"}), 404
        return format_response(result, fmt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try: cursor.close(); conn.close()
        except: pass

@app.route("/doctors", methods=["POST"])
@token_required
def create_doctor():
    data = request.get_json() or {}
    name = data.get("doctor_name")
    specialization = data.get("specialization")
    if not name or not specialization:
        return jsonify({"error": "doctor_name and specialization are required"}), 400
    try:
        conn = db_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctors (doctor_name, specialization) VALUES (%s, %s)", (name, specialization))
        conn.commit()
        return jsonify({"message": "Doctor created", "id": cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try: cursor.close(); conn.close()
        except: pass

# -------------------------
# PATIENTS ROUTES
# -------------------------
@app.route("/patients", methods=["GET"])
def get_patients():
    fmt = request.args.get("format", "json")
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT p.idPatient AS id, p.name, p.age, p.Diagnosis_idDiagnosis AS diagnosis_id,
                   d.diagnosis_name AS diagnosis_name, d.category AS diagnosis_category
            FROM patient p
            LEFT JOIN diagnosis d ON p.Diagnosis_idDiagnosis = d.idDiagnosis
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        return format_response(rows, fmt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try: cursor.close(); conn.close()
        except: pass

# -------------------------
# ASSIGNMENTS ROUTES
# -------------------------
@app.route("/assignments", methods=["GET"])
def get_assignments():
    fmt = request.args.get("format", "json")
    try:
        conn = db_conn()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT dhp.doctors_iddoctors AS doctor_id,
                   doc.doctor_name,
                   dhp.Patient_idPatient AS patient_id,
                   pat.name AS patient_name,
                   dhp.Patient_Diagnosis_idDiagnosis AS diagnosis_id
            FROM doctors_has_patient dhp
            LEFT JOIN doctors doc ON dhp.doctors_iddoctors = doc.iddoctors
            LEFT JOIN patient pat ON dhp.Patient_idPatient = pat.idPatient
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        return format_response(rows, fmt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try: cursor.close(); conn.close()
        except: pass

# -------------------------
# ROOT
# -------------------------
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Medical REST API — endpoints: /login, /diagnosis, /doctors, /patients, /assignments"
    })

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
