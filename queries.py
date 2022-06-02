import json
import string
import numpy
import requests
from api_credentials import API
from colorama import Style, Fore, Back

def display_result(status_code: int, json: string):
	if status_code == 200:
		print(f"{Fore.LIGHTGREEN_EX} Success {Fore.WHITE}{status_code} : {Style.DIM}{json}")
	else:
		print(f"{Fore.RED} Error {status_code} : {json}")

def add_students(pload):
	headers = { "Accept": "application/json;", "Content-Type": "application/json" }
	r = requests.post(API + "/students", headers= headers, json = pload)	
	display_result(r.status_code, r.text)

