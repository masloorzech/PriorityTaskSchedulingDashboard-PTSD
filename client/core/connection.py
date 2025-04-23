import requests
from utils.globals import url


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