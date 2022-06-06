from datetime import datetime
import os
import random
import time
import pandas as pd
import re
import unicodedata

students = pd.read_csv('data/Students.csv').drop_duplicates().sample(10)
accounting = pd.read_csv('data/Accounting.csv').drop_duplicates()
alternance = pd.read_csv('data/Alternance.csv').drop_duplicates()
grades = pd.read_csv('data/Grades.csv').drop_duplicates()

campus_staff = pd.read_csv('data/Liste_CampusStaff.csv', delimiter=';').drop_duplicates()

intervenants = pd.read_csv('data/Liste_Intervenants.csv').drop_duplicates()
modules = pd.read_csv('data/Modules.csv').drop_duplicates()

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,}$' 

def check_uuidv4(uuid):
    return type(uuid) == str and len(uuid) == 36

def check_str(string):
    return type(string) == str

def check_number(number):
    n_type = type(number)
    return n_type == int or n_type == float

def clean_string(string):
    return re.sub(r'[^A-Za-z0-9]+', '', unicodedata.normalize("NFKD", string))

def random_date(start, end, time_format, prop):
    start_time = time.mktime(time.strptime(start, time_format))
    end_time = time.mktime(time.strptime(end, time_format))

    ptime = start_time + prop * (end_time - start_time)

    return time.strftime(time_format, time.localtime(ptime))

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
        
        # generation d'une date de naissance
        if 'birth_date' not in student:
            student['birth_date'] = random_date("1/1/1980", "1/1/2006", '%m/%d/%Y', random.random())

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

def check_campus_staff():
    valid_staff = []
    for index, row in campus_staff.iterrows():
        if not (check_number(row['id']) and check_str(row['first_name']) and check_str(row['last_name']) and
			re.fullmatch(regex, row['email']) and check_str(row['email']) and check_str(row['Campus']) and check_str(row['Roles'])):
            continue
        else:
            valid_staff.append(row.to_dict())
    return valid_staff

def check_intervenant():
    valid_intervenant= []
    for index, row in intervenants.iterrows():
        if not (check_number(row['id']) and check_str(row['first_name']) and check_str(row['last_name']) and
			re.fullmatch(regex, row['email']) and check_str(row['email']) and check_str(row['modules']) and
			len(row['modules']) == 5 and check_str(row['Section'])):
            continue
        else:
            valid_intervenant.append(row.to_dict())
    return valid_intervenant

def check_modules():
    valid_modules = []
    for index, row in modules.iterrows():
        if not (check_uuidv4(row['id']) and check_str(row['moduleId']) and len(row['moduleId']) == 5 and
			check_str(row['moduleName']) and check_str(row['moduleDescription']) and
			check_number(row['credits']) and check_str(row['cursus'])):
            continue
        else:
            valid_modules.append(row.to_dict())
    return valid_modules