import terminal_logger
from typing import Callable

action_list = []

def add_action(label: str, func: Callable[[], None]) -> None:
    action_list.append(
        {
            "label": label,
            "func": func
        }
    )

def show_actions() -> None:
    """ shows a list of actions """
    terminal_logger.notice("Actions list\n")
    for i, action in enumerate(action_list):
        print(f"{i}) {action["label"]}")
    print("")

def __get_action_func() -> Callable[[], None]:
    """ Prompts the user to select an action and returns the corresponding function.  """
    try:
        input_number = int(input("Your option: "))
        return action_list[input_number]["func"]
    except (ValueError, IndexError):
        terminal_logger.error("\nCould not handle this action, please provide one of the list\n")
        show_actions()
        return __get_action_func()

def handle_actions() -> None:
    """ Executes the selected action. """
    func = __get_action_func()
    func()