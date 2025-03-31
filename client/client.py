import requests

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
url = 'http://{}:{}'.format(SERVER_IP, SERVER_PORT)

def connect() -> (int,str):
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
        if return_code == 0:
            break
        else:
            print(return_message)
        user_input = str(input("Do you want to try again? Y/N\n"))
        if user_input.capitalize() == "N":
            break
    return return_code


if __name__ == '__main__':

    return_code = establish_connection()
    if return_code != 0:
        print("Thanks for using this program")
        exit(return_code)

    #if cannot connect end program

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
