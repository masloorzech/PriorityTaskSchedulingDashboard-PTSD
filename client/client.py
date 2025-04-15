import requests

from utils.utils import display_info, display_error, display_success, clear_screen, display_logging_commands, \
    display_system_commands, display_title_message
from utils.globals import *
SYSTEM_NAME = "\033[92m\033[1mPTSD\033[0m"

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

def quit_system() -> None:
    print("\033[1;91mExiting the system...\033[0m")
    exit(0)

def show_actual_task_list_tasks(user_id,actual_list) -> None:
    print(f"📋{actual_list}:")
    response, tasklists = get_user_tasklists(user_id)
    if response:
        for task in get_tasklist_by_title(tasklists, actual_list)["tasks"]:
            status = "✅" if task["done"] else "❌"
            print(f" {status} {task['title']}")
            pass

def perform_logging() -> (str,str):
    display_title_message()
    display_logging_commands()
    while True:
        user_input = input(SYSTEM_NAME+ ": ").split(" ")
        if user_input[0] == "log" and len(user_input) == 3:
          username = user_input[1]
          password = user_input[2]
          response, user_id, username = log_in(username, password)
          if response:
              clear_screen()
              display_success("Successfully logged in")
              return user_id, username
          else:
              display_error("Login failed")

        elif user_input[0] == "reg" and len(user_input) == 4:
            username = user_input[1]
            password = user_input[2]
            repeated_password = user_input[3]
            if password != repeated_password:
                display_error("Passwords are not the same")
                continue

            response, user_id, username = register(username, password)
            if response:
                clear_screen()
                display_success("Successfully registered")
                return user_id, username
            else:
                display_error(username) #In this case username is used lika a buffer for error message

        elif user_input[0] == "quit":
            return "",""
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

def display_all_user_lists(user_id:str) -> None:
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

def perform_deleting_tasklist(user_id:str, listname: str) -> None:
    response, message = delete_tasklist(user_id, listname)
    if response:
        display_all_user_lists(user_id)
    else:
        display_error(message)

def perform_adding_tasklist(user_id:str, listname: str) -> None:
    response, message = add_new_task_list(user_id, listname)
    if response:
        display_all_user_lists(user_id)
    else:
        display_error(message)

def run_main_functionality(user_id:str,username: str) -> None:
    display_title_message(username)
    display_system_commands()
    actual_list = None
    while True:
        input_text = f"\033[92m\033[1m{actual_list}\033[0m: "  if actual_list is not None else ""
        user_input = input(SYSTEM_NAME+ ": " + input_text).split(" ")
        if user_input[0] in {"log out", "logout"}:
            return None

        elif user_input[0] in {"quit", "q"}:
            quit_system()

        elif user_input[0] in {"help", "h", "?"}:
            display_system_commands()

        if actual_list is None:
            if user_input[0] == "show":
                display_all_user_lists(user_id)

            elif user_input[0] == "delete" and len(user_input) == 2:
               perform_deleting_tasklist(user_id, user_input[1].strip())

            elif user_input[0] == "add" and len(user_input) == 2:
                perform_adding_tasklist(user_id, user_input[1].strip())

            elif user_input[0] == "select" and len(user_input) == 2:
                selected_list = user_input[1]
                result, tasklists = get_user_tasklists(user_id)
                if result:
                    if check_tasklist_exists(tasklists, selected_list):
                        actual_list = selected_list
                        show_actual_task_list_tasks(user_id,actual_list)
                    else:
                        display_error("Tasklist does not exist")
            elif user_input[0] == 'clear':
                clear_screen()

        if actual_list is not None:
            if user_input[0] == "show":
                show_actual_task_list_tasks(user_id,actual_list)
            elif user_input[0] == "back":
                actual_list = None
            elif user_input[0] == "add" and len(user_input) >= 2:
                taskname = ""
                for i in range(1, len(user_input)):
                    taskname += user_input[i] + " "

                add_new_task(user_id, actual_list, taskname.strip())
                show_actual_task_list_tasks(user_id,actual_list)

            elif user_input[0] == "mark" and len(user_input) >= 2:
                taskname = ""
                for i in range(1, len(user_input)):
                    taskname += user_input[i] + " "
                mark_task(user_id,actual_list, taskname.strip())
                show_actual_task_list_tasks(user_id,actual_list)

            elif user_input[0] == "unmark" and len(user_input) >= 2:
                taskname = ""
                for i in range(1, len(user_input)):
                    taskname += user_input[i] + " "

                unmark_task(user_id,actual_list, taskname.strip())
                show_actual_task_list_tasks(user_id,actual_list)

            elif user_input[0] == "delete" and len(user_input) >=2:
                taskname = ""
                for i in range(1, len(user_input)):
                    taskname += user_input[i] + " "

                delete_task(user_id,actual_list, taskname.strip())
                show_actual_task_list_tasks(user_id,actual_list)

if __name__ == '__main__':
    from core.auth import log_in, register
    from core.connection import connect
    from core.tasklist import delete_tasklist, add_new_task_list, get_user_tasklists, check_tasklist_exists, \
        add_new_task, mark_task, unmark_task, delete_task, get_tasklist_by_title
    establish_connection()
    while True:
        user_id,username = perform_logging()
        if user_id == "":
            exit()
        else:
            run_main_functionality(user_id, username)


