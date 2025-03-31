import requests

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
url = 'http://{}:{}'.format(SERVER_IP, SERVER_PORT)

def connect():
    response = requests.get(url)
    print(response.text)

if __name__ == '__main__':
    connect()
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
