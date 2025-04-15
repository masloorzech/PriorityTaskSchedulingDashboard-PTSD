import os
import requests
from utils import display_info, display_error, display_success, display_command
from globals import *
from admin_commands import handle_show_users


user_id =""

SYSTEM_NAME = "\033[92m\033[1mPTSD\033[0m"

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
        display_info("Establishing connection to server")
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

def register(username, password) -> str:
    global user_id
    if check_if_user_exist(username):
      display_error("Username already taken")
      return None
    data = {"username": username, "password": password}
    response = requests.post(url + "users/register", json=data)
    if response.status_code == 201:
        response = requests.post(f"{url}/users/get_user_id", json=data)
        user_id = response.json().get("user_id")
    else:
      display_error("Failed to register user")
    clear_screen()
    display_success("Registered successfully")
    return username

def log_in(username, password) -> str:
    global user_id
    data = {"username": username, "password": password}
    response = requests.post(f"{url}/users/log_in", json=data)
    if response.status_code == 200:
        clear_screen()
        response_data = response.json()
        user_id = response_data.get("user_id")
        display_success("Logged in successfully")
        return username
    else:
        display_error("Failed to login")
        return None

def quit_system() -> None:
    print("\033[1;91mExiting the system...\033[0m")
    exit(0)

def display_logging_commands() -> None:
    display_command("log","<username> <password>","Log into system")
    display_command("reg","<username> <password> <password>","Register system")
    display_command("quit",info="Quit system")

def display_system_commands() -> None:
    display_command("log out", info = "Log out of system")
    display_command("help", info = "Display help")
    display_command("quit", info = "Quit system")
    display_command("show", info = "Shows tasklists if in main catalogue, if inside task list shows all tasks")
    display_command("add", "<name>",info = "Adds new tasklist, select using select command, if inside task list adds new task")
    display_command("select", "<name>",info = "Selects tasklist and allows to adding task to it")
    display_command("delete", "<name>",info = "Deletes tasklist if inside task list deletes task")
    display_command("mark", "<name>",info = "Marks task as done")
    display_command("unmark", "<name>",info = "Marks task as undone")

def show_actual_task_list_tasks(actual_list) -> None:
  print(f"📋{actual_list}:")
  tasklists = get_user_tasklists()
  for task in get_tasklist_by_title(tasklists, actual_list)["tasks"]:
    status = "✅" if task["done"] else "❌"
    print(f" {status} {task['title']}")
    pass

def perform_logging() -> str:
    display_title_message()
    display_logging_commands()
    while True:
        user_input = input(SYSTEM_NAME+ ": ").split(" ")
        if user_input[0] == "log" and len(user_input) == 3:
          username = user_input[1]
          password = user_input[2]
          if log_in(username, password) is not None:
            return username
        elif user_input[0] == "reg" and len(user_input) == 4:
          username = user_input[1]
          password = user_input[2]
          repeated_password = user_input[3]
          if password != repeated_password:
            display_error("Passwords are not the same")
          else:
            if register(username, password) is not None:
              return username
        elif user_input[0] == "quit":
            return None
        else:
          display_error("Unknown command")

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
        elif user_input.startswith("delete user"):
            user_id_to_delete = user_input.split(" ")[2]
            result = agreement_form("Are you sure to delete user " + user_id_to_delete + " y/n")
            if result:
                request = requests.post(f"{url}/users/delete_user", json={"admin_id": user_id , "user_id": user_id_to_delete})
                print(request.json())
                print("\033[92mSUCCESS:\033[0m Deleted " + user_id_to_delete)

def display_all_user_lists() -> None:
  response = requests.get(f"{url}/tasks/{user_id}/tasklists")
  if response.status_code == 200:
    user_lists = response.json()
    if not user_lists:
      print("📭 You don't have any task lists")
    else:
      for user_list in user_lists:
        print(f"📋 {user_list.get('title', '[no title]')}")
  else:
    print("❌ Nie udało się pobrać list.")

def get_user_tasklists():
  res = requests.get(f"{url}/tasks/{user_id}/tasklists")
  if res.status_code == 200:
    return res.json()
  else:
    display_error("Failed to get user tasklists")
    return []

def get_tasklist_by_title(tasklists, title):
  for tl in tasklists:
    if tl["title"].lower() == title.lower():
      return tl
  return None

def check_tasklist_exists(tasklists, title):
  for tl in tasklists:
    if tl["title"].lower() == title.lower():
      return True
  return False

def mark_task(tasklist,task_name) ->None:
  response = requests.patch(f"{url}/tasks/{user_id}/tasklists/{tasklist}/tasks/{task_name}/done")
  if response.status_code == 200:
    return
  else:
    display_error("Failed to mark task")

def unmark_task(tasklist,task_name) ->None:
  response = requests.patch(f"{url}/tasks/{user_id}/tasklists/{tasklist}/tasks/{task_name}/undone")
  if response.status_code == 200:
    return
  else:
    display_error("Failed to unmark task")

def add_new_task_list(list_name) -> None:
    request = requests.post(f"{url}/tasks/{user_id}/tasklists", json={"title": list_name})
    if request.status_code == 201:
      display_all_user_lists()
    else:
      display_error(f"Failed to create {list_name}")

def add_new_task(list_title, task_name) -> None:
  request = requests.post(f"{url}/tasks/{user_id}/tasklists/{list_title}/tasks", json={"title": task_name})
  if request.status_code == 201:
    show_actual_task_list_tasks(list_title)
  else:
    display_error(f"Failed to create {task_name}")

def delete_tasklist(list_title):
    endpoint = f"{url}/tasks/{user_id}/tasklists/{list_title}"
    response = requests.delete(endpoint)
    if response.status_code == 200:
        display_all_user_lists()

def delete_task(list_title, task_title):
    endpoint = f"{url}/tasks/{user_id}/tasklists/{list_title}/tasks/{task_title}"
    response = requests.delete(endpoint)

    if response.status_code == 200:
        show_actual_task_list_tasks(list_title)

def run_main_functionality(username: str) -> str:
    display_title_message(username)
    display_system_commands()
    actual_list = None
    while True:
        input_text = f"\033[92m\033[1m{actual_list}\033[0m: "  if actual_list is not None else ""
        user_input = input(SYSTEM_NAME+ ": " + input_text).split(" ")
        if user_input[0] in {"log out", "logout"}:
            return "log out"
        elif user_input[0] in {"quit", "q"}:
            quit_system()
        elif user_input[0] in {"help", "h", "?"}:
            display_system_commands()
        if actual_list is None:
          if user_input[0] == "show":
                display_all_user_lists()
          elif user_input[0] == "delete" and len(user_input) == 2:
              delete_tasklist(user_input[1].strip())
          elif user_input[0] == "add" and len(user_input) == 2:
              list_name = user_input[1].strip()
              add_new_task_list(list_name)
          elif user_input[0] == "select" and len(user_input) == 2:
              selected_list = user_input[1]
              tasklists = get_user_tasklists()
              if check_tasklist_exists(tasklists, selected_list):
                actual_list = selected_list
                show_actual_task_list_tasks(actual_list)
              else:
                display_error("Tasklist does not exist")


        if actual_list is not None:
            if user_input[0] == "show":
              show_actual_task_list_tasks(actual_list)
            elif user_input[0] == "back":
                actual_list = None
            elif user_input[0] == "add" and len(user_input) >= 2:
              task_name = ""
              for i in range(1, len(user_input)):\
                add_new_task(actual_list, user_input[i].strip())
            elif user_input[0] == "mark" and len(user_input) >= 2:
              for i in range(1, len(user_input)):
                mark_task(actual_list, user_input[i].strip())
              show_actual_task_list_tasks(actual_list)
            elif user_input[0] == "unmark" and len(user_input) >= 2:
              for i in range(1, len(user_input)):
                unmark_task(actual_list, user_input[i].strip())
              show_actual_task_list_tasks(actual_list)
            elif user_input[0] == "delete" and len(user_input) ==2:
                delete_task(actual_list, user_input[1].strip())

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

