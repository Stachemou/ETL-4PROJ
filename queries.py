from email import header
import requests
from api_credentials import API

def add_user(first_name, last_name, birth_date, email, password, gender, region, campus):
	pload = {
		"user": {
			"first_name": first_name,
			"last_name": last_name,
			"birth_date": birth_date,
			"email": email,
			"password1": password,
			"password2": gender,
			"address": "Earth",
			"gender": gender,
			"region": region,
			"campus": campus,
			"position_id": 5
		}
	}
	headers = { "Accept": "application/json;", "Content-Type": "application/json" }
	r = requests.post(API + "/users", headers= headers, json = pload)
	print(r.status_code)
	print(r.json)


