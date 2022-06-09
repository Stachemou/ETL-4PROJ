from posixpath import dirname
import colorama
import os
from etl import check_students, check_campus_staff, check_intervenant, check_modules
from queries import add_students, add_staff, add_intervenants, add_modules
import pandas as pd
from colorama import Style, Fore, Back

colorama.init(autoreset=True)

if __name__ == "__main__":
	data_files = os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/data')
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
			students = pd.read_csv('data/' + file).drop_duplicates().sample(1)
		else:
			print(f"{Fore.RED} Error in data files : Wrong name or wrong data source type")
			print(f"{Fore.WHITE} Files must be in the following list: Accounting.csv, Alternance.csv ,Grades.csv, Liste_CampusStaff.csv, Liste_Intervenants.csv, Modules.csv, Students.csv")
			print(f"{Fore.WHITE} And you have : {', '.join(data_files)}")
			break

	if 'students' in locals() and 'accounting' in locals():
		add_students(check_students(students, accounting, alternance, grades))
	else:
		print(f"{Fore.YELLOW} Warning : No datafile for students or accounting")

	if 'modules' in locals():
		add_modules(check_modules(modules))
	else:
		print(f"{Fore.YELLOW} Warning : No datafile for modules")
	
	if 'intervenants' in locals():
		add_intervenants(check_intervenant(intervenants))
	else:
		print(f"{Fore.YELLOW} Warning : No datafile intervenants")

	if 'campus_staff' in locals():
		add_staff(check_campus_staff(campus_staff))
	else:
		print(f"{Fore.YELLOW} Warning : No datafile for staff")

