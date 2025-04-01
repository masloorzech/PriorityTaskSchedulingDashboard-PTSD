import requests
from globals import *

def handle_show_users() -> None:
    response = requests.get(url + "/users")
    if response.status_code == 200:
        try:
            data = response.json()
            users = data.get("data", [])
            for user in users:
                print(user)
        except ValueError:
            print("Error: Cannot parse data as JSON.")
    else:
        print(f"Error: Server returned code {response.status_code}")