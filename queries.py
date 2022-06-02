import json
import string
import numpy
import requests
from api_credentials import API
from main import log

def display_result(status_code: int, json: dict):
	if status_code == 200:
		log.success(json, extra=status_code)
	else:
		json = {"status_code": "epinrpe"}
		log.error("sfsf %s", extra=json)

def transform_int(value):
	if isinstance(value, numpy.int):
		return int(value)
	elif isinstance(value, numpy.float):
		return float(value)
	return value

def transform_int_students(students):
	for index, _ in enumerate(students):
		students[index]['accounting']['id'] = transform_int(students[index]['accounting']['id'])
	return students

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def add_students(pload):
	headers = { "Accept": "application/json;", "Content-Type": "application/json" }
	r = requests.post(API + "/students", headers= headers, json = pload)	
	display_result(r.status_code, r.json)

