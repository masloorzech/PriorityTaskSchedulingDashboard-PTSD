import os

def display_error(message:str = "") -> None:
  print(f"\033[91m\033[1mERROR:\033[0m \033[91m{message}\033[0m")

def display_success(message:str ="") -> None:
  print(f"\033[92m\033[1mSUCCESS:\033[0m \033[92m{message}\033[0m")

def display_info(message:str="") -> None:
  print(f"\033[96m\033[1mInformation:\033[0m \033[96m{message}\033[0m")

def display_command(command: str = "", args: str = "", info: str = "") -> None:
    formatted_command = f"\033[95m\033[1m{command}\033[0m"
    formatted_args = f" \033[3m{args}\033[0m" if args else ""
    print(f"{formatted_command}{formatted_args} -> {info}")

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def display_logging_commands() -> None:
    display_command("log","<username> <password>","Log into system")
    display_command("reg","<username> <password> <password>","Register system")
    display_command("quit",info="Quit system")

def display_system_commands() -> None:
    display_command("log out", info = "Log out of system")
    display_command("help", info = "Display help")
    display_command("quit", info = "Quit system")
    display_command("weather", "<city>",info = "Shows weather in selected city")
    display_command("weather",info = "Shows weather in actual coordinates")
    display_command("show", info = "Shows tasklists if in main catalogue, if inside task list shows all tasks")
    display_command("add", "<name>",info = "Adds new tasklist, select using select command, if inside task list adds new task")
    display_command("select", "<name>",info = "Selects tasklist and allows to adding task to it")
    display_command("delete", "<name>",info = "Deletes tasklist if inside task list deletes task")
    display_command("mark", "<name>",info = "Marks task as done")
    display_command("unmark", "<name>",info = "Marks task as undone")

def display_title_message(username = "")->None:
    print(f"Welcome \033[2;97m{username}\033[0m in \033[1;97mPriority Task Scheduling Dashboard - PTSD\033[0m")

def display_weather(data):
    print("📍 Weather for:", data.get("city", "Unknown city"))
    print("🌡️ Temperature:", data.get("temperature"), "°C")
    print("💧 Humidity:", data.get("humidity"), "%")
    print("🌥️ Description:", data.get("description").capitalize())


