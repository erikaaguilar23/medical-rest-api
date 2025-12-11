import mysql.connector
import json

with open("aguilar.json", "r") as config_file:
    config = json.load(config_file)

conn = mysql.connector.connect(
    host=config["host"],
    user=config["user"],
    password=config["password"],
    database=config["database"]
)

cursor = conn.cursor(dictionary=True)

# -----------------------------
# RETRIEVE DATA FROM ALL TABLES
# -----------------------------
tables = ["diagnosis", "doctors", "patient", "doctors_has_patient"]
export_data = {}

for table in tables:
    cursor.execute(f"SELECT * FROM {table};")
    rows = cursor.fetchall()
    export_data[table] = rows
    print(f"Retrieved {len(rows)} rows from {table}")

# -----------------------------
# CONVERT DATA TO JSON
# -----------------------------
json_output = json.dumps(export_data, indent=4)
print("\nGenerated JSON:\n", json_output)

# -----------------------------
# SAVE TO FILE
# -----------------------------
with open("medical_database.json", "w") as file:
    file.write(json_output)

print("\nJSON saved as medical_database.json")

cursor.close()
conn.close()
