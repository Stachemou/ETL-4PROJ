from datetime import datetime
import string
import requests
from api_credentials import API
from colorama import Style, Fore


def send_request(endpoint: string, pload):
    headers = {"Accept": "application/json;", "Content-Type": "application/json"}
    return requests.post(API + endpoint, headers=headers, json=pload)


def display_result(status_code: int, json: string, information: string):
    if status_code == 200:
        print(f"{Fore.LIGHTGREEN_EX} {datetime.now()} Success, {information} {Fore.WHITE}{status_code} : {Style.DIM}{json}")
    else:
        print(f"{Fore.RED} {datetime.now()} Error {status_code} : {json}")


def add_students(pload):
    r = send_request("/students", pload)
    display_result(r.status_code, r.text, 'students have been added')


def add_staff(pload):
    r = send_request("/staff", pload)
    display_result(r.status_code, r.text, 'staff has been added')


def add_intervenants(pload):
    r = send_request("/scts", pload)
    display_result(r.status_code, r.text, 'intervenants, have been added')


def add_modules(pload):
    r = send_request("/modules", pload)
    display_result(r.status_code, r.text, 'modules, have been added')
