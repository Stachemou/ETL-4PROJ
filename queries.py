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


def add_students(pload):
	headers = { "Accept": "application/json;", "Content-Type": "application/json" }
	r = requests.post(API + "/students", headers= headers, json = pload)	
	display_result(r.status_code, r.json)

