import requests

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
url = 'http://{}:{}'.format(SERVER_IP, SERVER_PORT)

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

def perform_logging() -> None:
    print("Welcome to \033[1;97mTASK SYSTEM 2.0\033[0m\nPlease log in (command: \033[1;92m-log\033[0m), register (command: \033[1;92m-reg\033[0m) or quit (command: \033[1;92m-q\033[0m)")
    while True:
        user_input = input(">").strip().upper()
        if user_input == "-LOG_IN":
            pass
        elif user_input == "-REGISTER":
            pass
        elif user_input == "-Q":
            exit()
        else:
            print("\033[91mERROR:\033[0m Unknown command")


if __name__ == '__main__':

    perform_logging()

    returned_value = establish_connection()



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
