import csv
import time
from datetime import datetime
import os
import pandas as pd

# campus_staff = etl.fromcsv('data/Liste_CampusStaff.csv', delimiter = ';')
students = pd.read_csv('data/Students.csv').drop_duplicates()
accounting = pd.read_csv('data/Accounting.csv').drop_duplicates()
alternance = pd.read_csv('data/Alternance.csv').drop_duplicates()
grades = pd.read_csv('data/Grades.csv').drop_duplicates()
modules = pd.read_csv('data/Modules.csv').drop_duplicates()

for index, row in students.iterrows():
	students_valide = False
	accounting_valide = False
	grades_valide = False

	if( type(row['id']) == str and len(row['id']) == 36 and type(row['first_name']) == str and
		type(row['last_name']) == str and type(row['campus']) == str and
		type(row['cursus']) == str):
		students_valide = True
	else:
		students_valide = False
		break

	if accounting['student_id'].isin([row['id']]).any():
		row_accounting = accounting.loc[accounting['student_id'] == row['id']].reindex()
		if (type(row_accounting['student_id'].iloc[0]) == str and len(row_accounting['student_id'].iloc[0]) == 36 and
			(row_accounting['amount_due'].dtype == float or int) and
			row_accounting['percent_paid'].dtype == float and row_accounting['amount_paid'].dtype == float
			):
			accounting_valide = True
	
	if grades['student'].isin([row['id']]).any():
		rows_grades = grades.loc[grades['student'] == row['id']].reindex()
		for index, i in rows_grades.iterrows():
			if(type(i['cursus']) == str and type(i['module']) == str and len(i['cursus']) == 5 and
				type(i['student']) == str and len(i['student']) == 36 and type(i['module']) == float):
				grades_valide = True
			else:
				grades_valide = False
				break

	if alternance['student'].isin([row['id']]).any():
		row_alternance = alternance.loc[alternance['student'] == row['id']]
		print(type(row_alternance['topay_student']) == int and type(row_alternance['topay_company']) == int)
		if(type(row_alternance['student'].iloc[0]) == str and len(row_alternance['student'].iloc[0]) == 36 and
			type(row_alternance['contrat'].iloc[0]) == str and type(row_alternance['companyName'].iloc[0]) == str and 
			type(row_alternance['topay_student']) == int or float and type(row_alternance['topay_company']) == int or float):
			row_alternance['hire_date'] = datetime.strptime(row_alternance['hire_date'].iloc[0], '%d/%m/%Y').date()
	input()

