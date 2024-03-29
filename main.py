import colorama
import os
from etl import check_students, check_campus_staff, check_intervenant, check_modules
from queries import add_students, add_staff, add_intervenants, add_modules
import pandas as pd
from colorama import Fore
import numpy

colorama.init(autoreset=True)

if __name__ == "__main__":
	data_files = os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/data')
	accounting = alternance = grades = campus_staff = intervenants = modules = students = None

	for file in data_files:
		if file == 'Accounting.csv':
			accounting = pd.read_csv('data/' + file).drop_duplicates()
		elif file == 'Alternance.csv':
			alternance = pd.read_csv('data/' + file).drop_duplicates()
		elif file == 'Grades.csv':
			grades = pd.read_csv('data/' + file).drop_duplicates()
		elif file == 'Liste_CampusStaff.csv':
			campus_staff = pd.read_csv('data/' + file, delimiter=';').drop_duplicates()
		elif file == 'Liste_Intervenants.csv':
			intervenants = pd.read_csv('data/' + file).drop_duplicates()
		elif file == 'Modules.csv':
			modules = pd.read_csv('data/' + file).drop_duplicates()
		elif file == 'Students.csv':
			students = pd.read_csv('data/' + file).drop_duplicates()
			students = students.replace({numpy.nan: None})
		else:
			print(f"{Fore.RED} Error in data files : Wrong name or wrong data source type")
			print(f"{Fore.WHITE} Files must be in the following list: Accounting.csv, Alternance.csv ,Grades.csv, Liste_CampusStaff.csv, Liste_Intervenants.csv, Modules.csv, Students.csv")
			print(f"{Fore.WHITE} And you have : {', '.join(data_files)}")
			break

	if modules is not None:
		add_modules(check_modules(modules))
	else:
		print(f"{Fore.YELLOW} Warning : No datafile for modules")

	if (students is not None) and (accounting is not None) and (alternance is not None) and (grades is not None):
		add_students(check_students(students, accounting, alternance, grades))
	else:
		print(f"{Fore.YELLOW} Warning : No datafile for students or accounting")
	
	if intervenants is not None:
		add_intervenants(check_intervenant(intervenants))
	else:
		print(f"{Fore.YELLOW} Warning : No datafile intervenants")

	if campus_staff is not None:
		add_staff(check_campus_staff(campus_staff))
	else:
		print(f"{Fore.YELLOW} Warning : No datafile for staff")
