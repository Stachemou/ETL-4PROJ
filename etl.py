import csv
import os
import petl as etl

campus_staff = etl.fromcsv('data/Liste_CampusStaff.csv', delimiter = ';')
etudiant_administratifs = etl.fromcsv('data/Liste_Etudiant_Administratifs.csv', delimiter = ';')
etudiant_alternance = etl.fromcsv('data/Liste_Etudiant_Alternance.csv', delimiter = ';')
etudiant_compta = etl.fromcsv('data/Liste_Etudiant_Compta.csv', delimiter = ';')
etudiant_pedagogie_notes = etl.fromcsv('data/Liste_Etudiant_Pédagogie_Notes.csv', delimiter = ';')
liste_intervenants = etl.fromcsv('data/Liste_Intervenants.csv')

csv_list = [campus_staff, etudiant_administratifs, etudiant_alternance, etudiant_compta, etudiant_pedagogie_notes, liste_intervenants]

header = []
all_header = []
for i in csv_list:
	current_header = etl.header(i)
	header.append(current_header)
	for h in current_header:
		all_header.append(h)


count_occ = {}
for i in all_header:
	if i not in count_occ:
		count_occ[i] = all_header.count(i)

print(count_occ)
