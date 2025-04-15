import requests
from utils.globals import url

def get_user_tasklists(user_id:str) -> (bool, str):
    res = requests.get(f"{url}/tasks/{user_id}/tasklists")
    if res.status_code == 200:
        return True, res.json()
    else:
        return False, "Failed to get user tasklists"

def mark_task(user_id:str,tasklist:str,task_name:str) ->(bool, str):
    response = requests.patch(f"{url}/tasks/{user_id}/tasklists/{tasklist}/tasks/{task_name}/done")
    if response.status_code == 200:
        return True, "Success"
    else:
        return False, "Failed to mark task"

def unmark_task(user_id:str,tasklist:str,task_name:str) ->(bool, str):
    response = requests.patch(f"{url}/tasks/{user_id}/tasklists/{tasklist}/tasks/{task_name}/undone")
    if response.status_code == 200:
        return True, "Success"
    else:
        return False,"Failed to unmark task"

def add_new_task_list(user_id:str,list_name:str) -> (bool, str):
    request = requests.post(f"{url}/tasks/{user_id}/tasklists", json={"title": list_name})
    if request.status_code == 201:
        return True, "Success"
    else:
        return False, f"Failed to create {list_name}"

def add_new_task(user_id:str,list_title:str, task_name:str) -> (bool, str):
    request = requests.post(f"{url}/tasks/{user_id}/tasklists/{list_title}/tasks", json={"title": task_name})
    if request.status_code == 201:
        return True, "Success"
    else:
        return False, f"Failed to create {task_name}"

def delete_tasklist(user_id:str,list_title:str) -> (bool, str):
    endpoint = f"{url}/tasks/{user_id}/tasklists/{list_title}"
    response = requests.delete(endpoint)
    if response.status_code == 200:
        return True, "Success"
    else:
        return False, f"Failed to delete tasklist {list_title}"

def delete_task(user_id:str,list_title:str, task_title:str) -> (bool, str):
    endpoint = f"{url}/tasks/{user_id}/tasklists/{list_title}/tasks/{task_title}"
    response = requests.delete(endpoint)
    if response.status_code == 200:
        return True, "Success"
    else:
        return False, f"Failed to delete task {task_title}"

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