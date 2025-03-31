import requests

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
url = 'http://{}:{}'.format(SERVER_IP, SERVER_PORT)

def connect() -> (int,str):
    try:
        response = requests.get(url)
        return 0, "SUCCESS: Connection established"
    except requests.exceptions.ConnectionError:
        return -1, "ERROR: Cannot connect to server"
    except requests.exceptions.Timeout:
        return -1, "ERROR: Timeout server is not responding"
    except requests.exceptions.RequestException as e:
        return -1, "ERROR: Unknown error"


if __name__ == '__main__':
    print(connect())
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
