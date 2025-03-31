import getpass
import hashlib
import os
from idlelib.run import flush_stdout

import requests

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
url = 'http://{}:{}'.format(SERVER_IP, SERVER_PORT)

COMMAND_PREFIX = ""

ACTIVE_USER = "SYSTEM"


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

def display_title_message()->None:
    if ACTIVE_USER == "SYSTEM":
        print(f"Welcome in \033[1;97mPriority Task Scheduling Dashboard - PTSD\033[0m")
    else:
        print(f"Welcome \033[2;97m{ACTIVE_USER}\033[0m in \033[1;97mPriority Task Scheduling Dashboard - PTSD\033[0m")


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

def register() -> None:
    global ACTIVE_USER
    if ACTIVE_USER != "SYSTEM":
        return

    login = input("Enter login: ")
    #Check if user exist in database
    while True:
        password = input("Enter password: ")
        second_password = input("Enter password again: ")
        if password != second_password:
            print("\033[91mERROR:\033[0m Passwords do not match")
            continue
        break

    clear_screen()

    ACTIVE_USER = login
    hashed_password = hashlib.sha512(password.encode()).hexdigest()

    password = second_password = None
    #send data to server

def log_in() -> None:
    if ACTIVE_USER != "SYSTEM":
        return
    login = input("Enter login: ")
    while True:
        password = input("Enter password: ")
        password_hash = hashlib.sha512(password.encode()).hexdigest()
        #send data to server check if user exist
        pass

    clear_screen()

def quit_system() -> None:
    print("\033[1;91mExiting the system...\033[0m")
    exit(0)

COMMANDS = {
    f"{COMMAND_PREFIX}log": log_in,
    f"{COMMAND_PREFIX}reg": register,
    f"{COMMAND_PREFIX}q": quit_system,
    f"{COMMAND_PREFIX}quit": quit_system,
}

def perform_logging() -> None:
    display_title_message()
    print(f"Log in using: \033[1;92m{COMMAND_PREFIX}log\033[0m\n"
          f"Register using: \033[1;92m{COMMAND_PREFIX}reg\033[0m\n"
          f"Or quit using: \033[1;92m{COMMAND_PREFIX}q\033[0m, \033[1;92m{COMMAND_PREFIX}quit \033[0m")
    while True:
        user_input = input(f"{ACTIVE_USER}:").strip().lower()
        if user_input in COMMANDS:
            COMMANDS[user_input]()
        else:
            print("\033[91mERROR:\033[0m Unknown command")
        if ACTIVE_USER != "SYSTEM":
            return




def run_main_functionality():
    display_title_message()
    while True:
        pass


if __name__ == '__main__':
    establish_connection()
    perform_logging()
    run_main_functionality()




    #connect to the server
    #log to the server if first try just create account
    #use system
    #SPECIFICATION
    # - logging
    # - adding new task lists
    # - adding new tasks to chosen list
    # - sorting using priority, expected time, time_of_adding
    # - use genetic neural network to choose the best order of execution
    # - ask for whether
    # - ask for a joke
    # - quick back to main list
