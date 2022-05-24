import csv
import json
import time
from datetime import datetime
import os
import pandas as pd

# campus_staff = etl.fromcsv('data/Liste_CampusStaff.csv', delimiter = ';')
students = pd.read_csv('data/Students.csv').drop_duplicates()
accountings = pd.read_csv('data/Accounting.csv').drop_duplicates()
alternance = pd.read_csv('data/Alternance.csv').drop_duplicates()
grades = pd.read_csv('data/Grades.csv').drop_duplicates()
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

		print(students_valide, accounting_valide, grades_valide, alternance_valide)

		if students_valide and accounting_valide:
			to_push = {'student': row.to_json(), 'accounting': row_accounting.iloc[0].to_json()}
			if alternance_valide:
				to_push['alternance']= row_alternance.iloc[0].to_json()
			if grades_valide:
				to_push['grades'] = []
				for index, i in rows_grades.iterrows():
					to_push['grades'].append(i.to_json())
			valides_students.append(json.dumps(to_push))

			print(valides_students)
		input()

	return valides_students

student_list = check_student()