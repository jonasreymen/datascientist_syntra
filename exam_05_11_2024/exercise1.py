import terminal_logger
import data_provider
import actions
import tabulate

data = data_provider.get_data()

def print_list(with_filters: bool = False) -> None:
    """ prints a list in terminal with specified filters if needed """
    print_data_list(
        get_list(
            generate_filters_via_input() if with_filters is True else None
        )
    )

def get_list(filters: dict = {}) -> list[dict]:
    """ shows a list of data """
    items = filter_list(filters)
    
    return items

def generate_filters_via_input() -> dict:
    """ generate the filter list """
    filters = {}
    for header in data_provider.get_headers():
        question_response = input(f"filter value for '{header}' (leave empty if not desired): ")

        if question_response:
            filters[header] = question_response

    return filters

def print_data_list(data_list: list[dict]) -> None:
    if not data_list:
        terminal_logger.error("List is empty")
        return
    
    print(tabulate.tabulate(data_list, headers="keys", tablefmt="grid"))
    print("")

def select_sort_option() -> dict:
    """ Asks User which sort option should be used """
    options = [
        {
            "label": "Sort by Name a-z",
            "func": lambda x: x["artiestennaam"].lower(),
            "reverse": False
        }
    ]
    
    for i, option in enumerate(options):
        print(f"{i}) {option["label"]}")
    print("")
    
    try:
        sort_option = input("Which sort option would you like to choose: ")
        return options[int(sort_option)]
    except (ValueError, IndexError):
        terminal_logger.error("Please provide a valid sort option")
        return select_sort_option()

def filter_list(filters: dict) -> list[dict]:
    """ filter list """
    if not filters:
        return data

    filtered_map = []
    for row in data:
        is_valid = True
        for f, value in filters.items():
            if row[f].lower() != value.lower():
                is_valid = False

        if is_valid is True:
            filtered_map.append(row)

    return filtered_map

def sort_list() -> None:
    """ sorts list """
    data_list = get_list()
    sort_option = select_sort_option()
    terminal_logger.notice(f"Sorting with option '{sort_option['label']}'")
    print_data_list(sorted(data_list, key=sort_option["func"], reverse=sort_option["reverse"]))

def get_row() -> dict:
    """ get row by ID"""
    identifier_field = "id"
    identifier = input(f"please provide {identifier_field} for row selection: ")
    filtered_rows = get_list({identifier_field: identifier})

    if len(filtered_rows) == 1:
        return filtered_rows[0]
    
    if len(filtered_rows) == 0:
        terminal_logger.error(f"No row found, please provide a correct {identifier_field}\n")
        return get_row()
    
    if len(filtered_rows) > 1:
        terminal_logger.error(f"Multiple rows found for {identifier_field}")
        exit()

def edit() -> None:
    """ changes data """
    terminal_logger.notice("Edit a row\n")
    row = get_row()
    
    for header in data_provider.get_headers():
        value = input(f"define a value for '{header}' (default: {row[header]}): ")

        if value:
            row[header] = value

    print("")
    terminal_logger.success("edit student succesfull: ")
    print("")
    print_data_list([row])

def add() -> None:
    """ add a row """
    terminal_logger.notice("Adding a row\n")
    row_data = {}

    for header in data_provider.get_headers():
        row_data[header] = input(f"supply a value for {header}: ")

    data.append(row_data)
    terminal_logger.success("added a row")
    print_data_list([row_data])

def remove() -> None:
    """ removing a row """
    terminal_logger.notice("Deleting a row\n")
    row = get_row()
    data.pop(data.index(row))
    terminal_logger.success("Succesfully removed a row:\n")
    print_data_list([row])
    print("")

def export():
    filename = data_provider.write_csv(data)
    terminal_logger.success(f"Write succesfull, see: {filename}")

def show_actions():
    actions.show_actions()

actions.add_action("Toon alle acties", lambda: show_actions())
actions.add_action("Voeg een muzikant toe", lambda: add())
actions.add_action("Verwijder een muzikant", lambda: remove())
actions.add_action("Toon alle muzikanten in tabulate", lambda: print_list(False))
actions.add_action("Toon alle muzikanten op basis van filters in tabulate", lambda: print_list(True))
actions.add_action("Pas een muzikant aan", lambda: edit())
actions.add_action("Sorteer muzikanten", lambda: sort_list())
actions.add_action("Schrijf huidige data weg naar een nieuw csv bestand.", lambda: export())

show_actions()
while True:
    actions.handle_actions()