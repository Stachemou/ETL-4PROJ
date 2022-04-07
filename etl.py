import csv
import os
import petl as etl

campus_staff = etl.fromcsv('data/Liste_CampusStaff.csv', delimiter = ';')

print(campus_staff)