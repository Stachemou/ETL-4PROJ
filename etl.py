from datetime import datetime
import random
import time
import pandas as pd
import re
import unicodedata

regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,}$'


def check_uuidv4(uuid):
    return type(uuid) == str and len(uuid) == 36


def check_str(string):
    return type(string) == str


def check_number(number):
    n_type = type(number)
    return n_type == int or n_type == float


def clean_string(string):
    return re.sub(r'[^A-Za-z\d]+', '', unicodedata.normalize("NFKD", string))


def random_date(start, end, time_format, prop):
    start_time = time.mktime(time.strptime(start, time_format))
    end_time = time.mktime(time.strptime(end, time_format))

    ptime = start_time + prop * (end_time - start_time)

    return time.strftime(time_format, time.localtime(ptime))


def check_students(students: pd.DataFrame, accounting: pd.DataFrame, alternance: pd.DataFrame, grades: pd.DataFrame):
    valid_students = []

    for index, row in students.iterrows():
        student = row.to_dict()

        # Check base student
        if not check_uuidv4(student["id"]) and not check_str(student["first_name"]) and not \
                check_str(student["last_name"]) and not check_str(student["campus"]) and not \
                check_str(student["cursus"]) and not check_number(student["entry_level"]) and \
                not check_number(student["exit_level"]) and not check_number(student["current_level"]) \
                and not check_str(student["entry_date"]) and not check_str(student["exit_date"]):
            continue

        if check_str(student["entry_date"]):
            student["entry_date"] = datetime.strptime(student["entry_date"], "%d/%m/%Y").isoformat()

        if check_str(student["exit_date"]):
            student["exit_date"] = datetime.strptime(student["exit_date"], "%d/%m/%Y").isoformat()

        if 'email' not in student:
            student['email'] =\
                f"{clean_string(student['first_name'])}.{clean_string(student['last_name'])}@supinfo.com".lower()
        else:
            if not check_str(student['email']) and not re.fullmatch(regex, student['email']):
                continue

        # generation d'une date de naissance
        if 'birth_date' not in student:
            student['birth_date'] = random_date("1/1/1980", "1/1/2006", '%m/%d/%Y', random.random())
        else:
            if not check_str(student["birth_date"]):
                continue
            student["birth_date"] = datetime.strptime(student["birth_date"], "%d/%m/%Y").isoformat()

        # Check accounting
        if accounting["student_id"].isin([student["id"]]).any():
            student_accounting = accounting.loc[accounting["student_id"] == student["id"]].to_dict(orient="records")[0]

            if check_number(student_accounting["amount_due"]) and check_number(student_accounting["percent_paid"]) and \
                    check_number(student_accounting["amount_paid"]):
                student_accounting["type"] = "Échelonnement"
                student["accounting"] = student_accounting

        # Check jobs
        if alternance["student"].isin([student["id"]]).any():
            student_job = alternance.loc[alternance["student"] == student["id"]].to_dict(orient="records")[0]

            if check_str(student_job["contrat"]) and check_str(student_job["companyName"]) and \
                    check_number(student_job["topay_student"]) and check_number(student_job["topay_company"]) and \
                    check_str(student_job["hire_date"]):
                student_job["hire_date"] = datetime.strptime(student_job["hire_date"], "%d/%m/%Y").isoformat()
                # change initial to stage
                student_job["contrat"] = "stage" if student_job["contrat"] == "initial" else student_job["contrat"]
                # Generate end date of job
                student_job["end_date"] = random_date("1/1/2023", "1/1/2024", '%m/%d/%Y', random.random())
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


def check_campus_staff(campus_staff: pd.DataFrame):
    valid_staff = []
    roles_list = ["Admin. plateforme", "Direction académique", "Administration", "Pédagogie", "Intervenant", "Étudiant"]

    for index, row in campus_staff.iterrows():
        if not (check_number(row['id']) and check_str(row['first_name']) and check_str(row['last_name']) and
                re.fullmatch(regex, row['email']) and check_str(row['email']) and check_str(row['Campus']) and
                check_str(row['Roles'])):
            continue
        else:
            if row['Roles'] not in roles_list:
                if convert_role(row['Roles']) is not None:
                    row['Roles'] = convert_role(row['Roles'])
                else:
                    continue
            # generation d'une date de naissance
            if 'birth_date' not in row:
                row['birth_date'] = random_date("1/1/1980", "1/1/1999", '%m/%d/%Y', random.random())
            else:
                if not check_str(row["birth_date"]):
                    continue
                row["birth_date"] = datetime.strptime(row["birth_date"], "%d/%m/%Y").isoformat()
            valid_staff.append(row.to_dict())
    return valid_staff


def convert_role(role):
    if role == "Full Professor" or role == "Coordinateur":
        return "Pédagogie"
    elif role == "Directeur academique":
        return "Direction académique"
    elif role == "Professor":
        return "Intervenant"
    else:
        return None


def check_intervenant(intervenants: pd.DataFrame):
    valid_intervenant = []
    for index, row in intervenants.iterrows():
        if not (check_number(row['id']) and check_str(row['first_name']) and check_str(row['last_name']) and
                re.fullmatch(regex, row['email']) and check_str(row['email']) and check_str(row['modules']) and
                len(row['modules']) == 5 and check_str(row['Section'])):
            continue
        else:
            # generation d'une date de naissance
            if 'birth_date' not in row:
                row['birth_date'] = random_date("1/1/1980", "1/1/1999", '%m/%d/%Y', random.random())
            else:
                if not check_str(row["birth_date"]):
                    continue
                row["birth_date"] = datetime.strptime(row["birth_date"], "%d/%m/%Y").isoformat()
            row['Section'] = row['Section'][:-2]
            row['modules'] = row['modules'][1:]
            valid_intervenant.append(row.to_dict())
    return valid_intervenant


def check_modules(modules: pd.DataFrame):
    valid_modules = []
    for index, row in modules.iterrows():
        if not (check_uuidv4(row['id']) and check_str(row['moduleId']) and len(row['moduleId']) == 5 and
                check_str(row['moduleName']) and check_str(row['moduleDescription']) and
                check_number(row['credits']) and check_str(row['cursus'])):
            continue
        else:
            row['year'] = row['moduleId'][0]
            row['moduleId'] = row['moduleId'][1:]
            valid_modules.append(row.to_dict())
    return valid_modules
