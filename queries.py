import json
import string
import requests
from api_credentials import API
from main import log

def display_result(status_code: int, json: dict):
	if status_code == 200:
		log.success(json, extra=status_code)
	else:
		json = {"status_code": "epinrpe"}
		log.error("sfsf %s", extra=json)


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
	display_result(r.status_code, r.json)

d = {"status_code": 200}
display_result(200, d)
