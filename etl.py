import csv
import json
from datetime import datetime
import os
from tkinter.ttk import Separator
import pandas as pd
import re

from queries import add_students

students = pd.read_csv('data/Students.csv').drop_duplicates()
accountings = pd.read_csv('data/Accounting.csv').drop_duplicates()
alternance = pd.read_csv('data/Alternance.csv').drop_duplicates()
grades = pd.read_csv('data/Grades.csv').drop_duplicates()

campus_staff = pd.read_csv('data/Liste_CampusStaff.csv', delimiter=';').drop_duplicates()

intervenants = pd.read_csv('data/Liste_Intervenants.csv').drop_duplicates()
modules = pd.read_csv('data/Modules.csv').drop_duplicates()

# check students data
def check_student():
	valides_students = []
	for index, row in students.iterrows():
		students_valide = False
		accounting_valide = False
		grades_valide = False
		alternance_valide = False

		if( type(row['id']) == str and len(row['id']) == 36 and type(row['first_name']) == str and
			type(row['last_name']) == str and type(row['campus']) == str and
			type(row['cursus']) == str):
			students_valide = True
		else:
			students_valide = False
			break

		if accountings['student_id'].isin([row['id']]).any():
			row_accounting = accountings.loc[accountings['student_id'] == row['id']].reindex()
			if (type(row_accounting['student_id'].iloc[0]) == str and len(row_accounting['student_id'].iloc[0]) == 36 and
				(row_accounting['amount_due'].dtype == float or int) and
				row_accounting['percent_paid'].dtype == float and row_accounting['amount_paid'].dtype == float
				):
				accounting_valide = True
		
		if grades['student'].isin([row['id']]).any():
			rows_grades = grades.loc[grades['student'] == row['id']].reindex()
			for index, i in rows_grades.iterrows():
				if(type(i['cursus']) == str and type(i['module']) == str and len(i['module']) == 5 and
					type(i['student']) == str and len(i['student']) == 36 and type(i['grade']) == float):
					grades_valide = True
				else:
					grades_valide = False
					break

		if alternance['student'].isin([row['id']]).any():
			row_alternance = alternance.loc[alternance['student'] == row['id']]
			if(type(row_alternance['student'].iloc[0]) == str and len(row_alternance['student'].iloc[0]) == 36 and
				type(row_alternance['contrat'].iloc[0]) == str and type(row_alternance['companyName'].iloc[0]) == str and 
				type(row_alternance['topay_student']) == int or float and type(row_alternance['topay_company']) == int or float):
				row_alternance['hire_date'].iloc[0] = datetime.strptime(row_alternance['hire_date'].iloc[0], '%d/%m/%Y').date()
				alternance_valide = True


		if students_valide and accounting_valide:
			to_push = {'student': row.to_json(), 'accounting': row_accounting.iloc[0].to_json()}
			if alternance_valide:
				to_push['alternance']= row_alternance.iloc[0].to_json()
			if grades_valide:
				to_push['grades'] = []
				for index, i in rows_grades.iterrows():
					to_push['grades'].append(i.to_json())
			valides_students.append(json.dumps(to_push))

	return valides_students

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
add_students(check_student())

# check_modules()