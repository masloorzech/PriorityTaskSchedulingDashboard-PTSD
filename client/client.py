import os
import requests
from globals import *
from admin_commands import handle_show_users


COMMAND_PREFIX = ""

user_id =""

def connect() -> tuple[int,str]:
    try:
        response = requests.get(url)
        return 0, "\033[92mSUCCESS:\033[0m Connection established"
    except requests.exceptions.ConnectionError:
        return -1, "\033[91mERROR:\033[0m Cannot connect to server"
    except requests.exceptions.Timeout:
        return -1, "\033[91mERROR:\033[0m Timeout server is not responding"
    except requests.exceptions.RequestException as e:
        return -1, "\033[91mERROR:\033[0m Unknown error"

def display_title_message(username = "")->None:
    print(f"Welcome \033[2;97m{username}\033[0m in \033[1;97mPriority Task Scheduling Dashboard - PTSD\033[0m")

def establish_connection() -> int:
    while True:
        print("\033[94mEstablishing connection to server\033[0m")
        return_code, return_message = connect()

        print(return_message)
        if return_code == 0:
            break

        result = agreement_form("Do you want to try again? Y/N\n")
        if not result:
            exit()

    return return_code

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def check_if_user_exist(username:str)->bool:
    response = requests.post(f"{url}/user_exist", json={"username": username})
    user_exists = response.json().get("exists", False)
    if user_exists:
        return True
    else:
        return False

def register() -> str:
    global user_id
    print("To quit enter: quit")
    username = input("Enter login: ")
    if username == "quit":
        return None
    if check_if_user_exist(username):
        print("User exists, try logging in.")
        return log_in(username)
    while True:
        password = input("Enter password: ")
        second_password = input("Enter password again: ")
        if password != second_password:
            print("\033[91mERROR:\033[0m Passwords do not match try again.")
            continue

        data = {"username": username, "password": password}
        response = requests.post(url + "/register", json=data)
        if response.status_code == 201:
            response = requests.post(f"{url}/get_user_id", json=data)
            user_id = response.json().get("user_id")
            break

        print("\033[91mERROR:\033[0m Failed to register user")

    clear_screen()
    print("User registered successfully!")



    password = second_password = None
    return username

def log_in(username = None) -> str:
    global user_id
    print("To quit enter: quit in any field")
    while True:
        if username is None:
            username = input("Enter login: ")
        else:
            print(f"Enter username: {username}")
        if username == "quit":
            return None

        password = input("Enter password: ")

        if password == "quit":
            return None

        data = {"username": username, "password": password}
        request = requests.post(f"{url}/log_in", json=data)
        if request.status_code == 200:
            clear_screen()
            response = requests.post(f"{url}/get_user_id", json=data)
            user_id = response.json().get("user_id")
            print("\033[92mSUCCESS:\033[0m Logged in successfully")
            return username
        else:
            username = None
            print("Incorrect login or password")

def quit_system() -> None:
    print("\033[1;91mExiting the system...\033[0m")
    exit(0)

def display_logging_commands() -> None:
    print(f"Log in using: \033[1;92m{COMMAND_PREFIX}log\033[0m\n"
          f"Register using: \033[1;92m{COMMAND_PREFIX}reg\033[0m\n"
          f"Or quit using: \033[1;92m{COMMAND_PREFIX}q\033[0m, \033[1;92m{COMMAND_PREFIX}quit \033[0m")

def display_system_commands() -> None:
    print(f"Log out using: \033[1;92m{COMMAND_PREFIX}log out\033[0m\n"
          f"Display help using: \033[1;92m{COMMAND_PREFIX}help\033[0m, \033[1;92m{COMMAND_PREFIX}h\033[0m, \033[1;92m{COMMAND_PREFIX}?\033[0m\n"
          f"Or quit using: \033[1;92m{COMMAND_PREFIX}q\033[0m, \033[1;92m{COMMAND_PREFIX}quit \033[0m")


def perform_logging() -> str:
    display_title_message()
    display_logging_commands()
    while True:
        user_input = input().strip().lower()
        if user_input in LOGGING_COMMANDS:
            username = LOGGING_COMMANDS[user_input]()
            if username is not None:
                return username
            else:
               display_logging_commands()
        else:
            print("\033[91mERROR:\033[0m Unknown command")


def agreement_form(input_text)->bool:
    while True:
        result = input(input_text+'\n').lower()
        if result == "y":
            return True
        elif result == "n":
            return False
        else:
            print("\033[91mERROR:\033[0m Unknown command")


def run_admin_functionality() -> str:
    while True:
        user_input = input().strip().lower()
        if user_input in {"quit", "q"}:
            quit_system()
        elif user_input in {"log out", "logout"}:
            return "log out"
        elif user_input == "show users":
            handle_show_users()
        elif user_input.startswith("delete "):
            user_id_to_delete = user_input.split(" ")[1]
            result = agreement_form("Are you sure to delete user " + user_id_to_delete)
            if result:
                print("\033[92mSUCCESS:\033[0m Deleted " + user_id_to_delete)





def run_main_functionality(username: str) -> str:
    display_title_message(username)
    display_system_commands()
    actual_list = None
    while True:
        input_text = actual_list+":" if actual_list is not None else ""
        user_input = input(input_text).strip().lower()
        if user_input in {"log out", "logout"}:
            return "log out"
        elif user_input in {"quit", "q"}:
            quit_system()
        elif user_input in {"help", "h", "?"}:
            display_system_commands()
        elif user_input == "ptsd show":
            # ask server for all user lists and display all
            pass
        elif user_input == "ptsd show all":
            #ask server for all user lists and display all tasks in all lists
            pass
        elif user_input.startswith("ptsd delete "):
            list_name = user_input.split(" ")[2]
            print(f"Deleting {list_name}")
            #delete task list
            pass
        elif user_input.startswith("ptsd add "):
            #adding new task list
            list_name = user_input.split(" ")[2]
            print(f"Adding {list_name}")
            pass

        elif user_input.startswith("ptsd select"):
            list_name = user_input.split(" ")[2]
            print(f"Selecting {list_name}")
            #set acctual list on listname if avaliable
            actual_list = list_name
            pass

        if actual_list is not None:
            if user_input == "show":
                #display all user tasks inside actual list
                pass
            elif user_input == "clear":
                #clear all tasks inside actual list
                pass
            elif user_input == "back":
                #back to main editor
                actual_list = None
            elif user_input.startswith("add "):
                #adding new task to list
                pass
            elif user_input.startswith("delete "):
                task_id = user_input.split(" ")[1]
                #deletig taks via id
                pass
            elif user_input.startswith("done "):
                task_id = user_input.split(" ")[1]
                #checking task via id
                pass
            elif user_input.startswith("undone "):
                task_id = user_input.split(" ")[1]
                #unchecking task via id
                pass


LOGGING_COMMANDS = {
    f"{COMMAND_PREFIX}log": log_in,
    f"{COMMAND_PREFIX}reg": register,
    f"{COMMAND_PREFIX}q": quit_system,
    f"{COMMAND_PREFIX}quit": quit_system,
}

if __name__ == '__main__':
    establish_connection()
    while True:
        user = perform_logging()
        if user is None:
            exit()
        if user == "ADMIN":
            print("Logged as ADMIN")
            run_admin_functionality()
        else:
            action = run_main_functionality(user)
            if action == "log out":
                print("Logged out")

