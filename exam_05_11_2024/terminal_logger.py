from colorama import Style, Fore

def error(description: str) -> None:
    """ prints a red colored message """
    print(f"{Fore.RED}{description}{Style.RESET_ALL}")

def success(description: str) -> None:
    """ prints a green colored message """
    print(f"{Fore.GREEN}{description}{Style.RESET_ALL}")
    
def notice(description: str) -> None:
    """ prints a yellow colored message """
    print(f"{Fore.YELLOW}{description}{Style.RESET_ALL}")