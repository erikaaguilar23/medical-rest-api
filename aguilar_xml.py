import xml.etree.ElementTree as ET

# Parsing the XML File
tree = ET.parse('aguilar_xml_dump.xml')
root = tree.getroot()
print("Root tag:", root.tag)

# Number of main tables inside <database>
print("Number of tables:", len(root))

# Accessing the first table (diagnosis_table)
first_table = root[0]
print("First table tag:", first_table.tag)
print("Number of rows:", len(first_table))

# Looping Through Diagnosis Table
print("\n--- Diagnosis Table ---")
for diag in root.find('diagnosis_table'):
    print("ID:", diag.find('idDiagnosis').text)
    print("Diagnosis Name:", diag.find('diagnosis_name').text)
    print("Category:", diag.find('category').text)
    print()

# Looping Through Doctors
print("\n--- Doctors Table ---")
for doc in root.find('doctors_table'):
    print("Doctor ID:", doc.find('iddoctors').text)
    print("Name:", doc.find('doctor_name').text)
    print("Specialization:", doc.find('specialization').text)
    print()

# Accessing attributes (if nodes had attributes — yours currently don't)
# Example: print attributes of patient rows (if later added)
for patient in root.find('patients_table'):
    print("Patient tag attributes:", patient.attrib)

# Using iter() to get all <age> tags
print("\nAll ages found:")
for age in root.iter('age'):
    print(age.text)

# Using findall() to get all <patient> nodes
patients = root.find('patients_table').findall('patient')
print("\nNumber of patients:", len(patients))

# Modifying XML Data (example)
# Change 1st patient age
root.find('patients_table')[0].find('age').text = "99"

# Remove the category from the 1st diagnosis
first_diagnosis = root.find('diagnosis_table')[0]
category_node = first_diagnosis.find('category')
first_diagnosis.remove(category_node)

# Save changes to a new file
tree.write('updated_database.xml')
print("\nXML file updated and saved as updated_database.xml")
