import string
import requests
from api_credentials import API
from colorama import Style, Fore, Back


def display_result(status_code: int, json: string, information: string):
    if status_code == 200:
        print(f"{Fore.LIGHTGREEN_EX} Success, {information} {Fore.WHITE}{status_code} : {Style.DIM}{json}")
    else:
        print(f"{Fore.RED} Error {status_code} : {json}")


def add_students(pload):
    headers = {"Accept": "application/json;", "Content-Type": "application/json"}
    r = requests.post(API + "/students", headers=headers, json=pload)
    display_result(r.status_code, r.text, 'students have been added')


def add_staff(pload):
    headers = {"Accept": "application/json;", "Content-Type": "application/json"}
    r = requests.post(API + "/staff", headers=headers, json=pload)
    display_result(r.status_code, r.text, 'staff has been added')


def add_intervenants(pload):
    headers = {"Accept": "application/json;", "Content-Type": "application/json"}
    r = requests.post(API + "/scts", headers=headers, json=pload)
    display_result(r.status_code, r.text, 'intervenants, have been added')


def add_modules(pload):
    headers = {"Accept": "application/json;", "Content-Type": "application/json"}
    r = requests.post(API + "/modules", headers=headers, json=pload)
    display_result(r.status_code, r.text, 'modules, have been added')
