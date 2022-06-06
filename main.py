import coloredlogs, verboselogs, logging
import colorama
from etl import check_students, check_campus_staff, check_intervenant, check_modules
from queries import add_students, add_staff, add_intervenants, add_modules


colorama.init(autoreset=True)


if __name__ == "__main__":
	add_students(check_students())
	# check_campus_staff()
	# check_intervenant()
	# check_modules()

