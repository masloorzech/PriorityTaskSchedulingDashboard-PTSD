import requests
from utils.globals import url

def check_if_user_exist(username:str)->bool:
    response = requests.post(f"{url}/users/user_exist", json={"username": username})
    user_exists = response.json().get("exists", False)
    if user_exists:
        return True
    else:
        return False

def log_in(username:str, password:str) -> (bool,str,str):
    data = {"username": username, "password": password}
    response = requests.post(f"{url}/users/log_in", json=data)
    if response.status_code == 200:
        response_data = response.json()
        user_id = response_data.get("user_id")
        return True,user_id, username
    else:
        return False,"", ""

def register(username:str, password:str) -> (bool,str,str):
    if check_if_user_exist(username):
        return False,"", "Username already taken"

    data = {"username": username, "password": password}
    response = requests.post(url + "/users/register", json=data)

    if response.status_code == 201:
        response = requests.post(f"{url}/users/get_user_id", json=data)
        user_id = response.json().get("user_id")
        return True, user_id, username
    else:
        return False, "", "Failed to register user"
