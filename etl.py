import csv
import json
from datetime import datetime
import os
import numpy
import pandas as pd
import re
import unicodedata

from queries import add_students

students = pd.read_csv('data/Students.csv').drop_duplicates().sample(10)
accounting = pd.read_csv('data/Accounting.csv').drop_duplicates()
alternance = pd.read_csv('data/Alternance.csv').drop_duplicates()
grades = pd.read_csv('data/Grades.csv').drop_duplicates()

campus_staff = pd.read_csv('data/Liste_CampusStaff.csv', delimiter=';').drop_duplicates()

intervenants = pd.read_csv('data/Liste_Intervenants.csv').drop_duplicates()
modules = pd.read_csv('data/Modules.csv').drop_duplicates()

def check_uuidv4(uuid):
    return type(uuid) == str and len(uuid) == 36


def check_str(string):
    return type(string) == str


def check_number(number):
    n_type = type(number)
    return n_type == int or n_type == float

def clean_string(string):
    return re.sub(r'[^A-Za-z0-9]+', '', unicodedata.normalize("NFKD", string))

def check_students():
    valid_students = []

    for index, row in students.iterrows():
        student = row.to_dict()

        # Check base student
        if not check_uuidv4(student["id"]) and not check_str(student["first_name"]) and not \
                check_str(student["last_name"]) and not check_str(student["campus"]) and check_str(student["cursus"]):
            continue
        
        if 'email' not in student:
            student['email'] = f"{clean_string(student['first_name'])}.{clean_string(student['last_name'])}@supinfo.com".lower()


        # Check accounting
        if accounting["student_id"].isin([student["id"]]).any():
            student_accounting = accounting.loc[accounting["student_id"] == student["id"]].to_dict(orient="records")[0]

            if check_number(student_accounting["amount_due"]) and check_number(student_accounting["percent_paid"]) and \
                    check_number(student_accounting["amount_paid"]):
                student["accounting"] = student_accounting

        # Check jobs
        # TODO: Multiple jobs
        if alternance["student"].isin([student["id"]]).any():
            student_job = alternance.loc[alternance["student"] == student["id"]].to_dict(orient="records")[0]

            if check_str(student_job["contrat"]) and check_str(student_job["companyName"]) and \
                    check_number(student_job["topay_student"]) and check_number(student_job["topay_company"]):
                student_job["hire_date"] = datetime.strptime(student_job["hire_date"], "%d/%m/%Y").isoformat()
                student["job"] = student_job

        # Check grades
        if grades["student"].isin([student["id"]]).any():
            student_grades = grades.loc[grades["student"] == student["id"]].to_dict(orient="records")
            student["grades"] = []

            for grade in student_grades:
                if check_str(grade["cursus"]) and re.search(r"^\d\w+$", grade["module"]):
                    module_split = list(filter(None, re.split(r"^(\d)", grade["module"])))

                    grade["year"] = int(module_split[0])
                    grade["name"] = module_split[1]
                    del grade["module"]

                    student["grades"].append(grade)

        valid_students.append(student)

    return valid_students

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,}$' 

def check_campus_staff():
	to_return = []
	for index, row in campus_staff.iterrows():
		campus_staff_valide = False
		if (type(row['id']) == int and type(row['first_name']) == str and type(row['last_name']) == str and
			re.fullmatch(regex, row['email']) and type(row['email']) == str and type(row['Campus']) == str and type(row['Roles']) == str):
			campus_staff_valide = True
		if campus_staff_valide:
			to_return.append(json.dumps(row.to_json()))
	return to_return

def check_intervenant():
	to_return = []
	for index, row in intervenants.iterrows():
		intervenant_valide = False
		if (type(row['id']) == int and type(row['first_name']) == str and type(row['last_name']) == str and
			re.fullmatch(regex, row['email']) and type(row['email']) == str and type(row['modules']) == str and
			len(row['modules']) == 5 and type(row['Section']) == str):
			intervenant_valide = True
		if intervenant_valide:
			to_return.append(json.dumps(row.to_json()))
	return to_return

def check_modules():
	to_return = []
	for index, row in modules.iterrows():
		module_valide = False
		if (type(row['id']) == str and len(row['id']) == 36 and type(row['moduleId']) == str and len(row['moduleId']) == 5 and
			type(row['moduleName']) == str and type(row['moduleDescription']) == str and
			type(row['credits']) == int and type(row['cursus']) == str):
			module_valide = True
		if module_valide:
			to_return.append(json.dumps(row.to_json()))
	return to_return

# check_campus_staff()
# check_intervenant())

add_students(check_students())

# check_modules()