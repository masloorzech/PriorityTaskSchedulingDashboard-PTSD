
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