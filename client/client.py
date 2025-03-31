import os
import requests

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
url = 'http://{}:{}'.format(SERVER_IP, SERVER_PORT)

COMMAND_PREFIX = ""


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

        user_input = input("Do you want to try again? Y/N\n").strip().upper()

        if user_input == "N":
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
            break

        print("\033[91mERROR:\033[0m Failed to register user")

    clear_screen()
    print("User registered successfully!")
    password = second_password = None
    return username

def log_in(username = None) -> str:
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
        response = request.json().get("logged_in", True)
        if response:
            clear_screen()
            print("\033[92mSUCCESS:\033[0m Logged in successfully")
            return username
        else:
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

def run_main_functionality(username: str) -> str:
    display_title_message(username)
    display_system_commands()
    while True:
        user_input = input().strip().lower()
        if user_input in {"log out", "logout"}:
            return "log out"
        elif user_input in {"quit", "q"}:
            quit_system()
        elif user_input in {"help", "h", "?"}:
            display_system_commands()


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

        action = run_main_functionality(user)
        if action == "log out":
            print("Logged out")

