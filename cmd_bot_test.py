import shlex
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.formatted_text import ANSI
from colorama import init, Fore, Style
from enum import Enum, auto

# Ініціалізація colorama
init(autoreset=True)


class BotCmd(Enum):
    ADD = auto()
    CHANGE = auto()
    EDIT_NOTE = auto()
    DELETE_NOTE = auto()
    ADD_TAGS = auto()
    DELETE_TAG = auto()
    GET_NOTES_BY_TAG = auto()
    GET_NOTE = auto()
    GET_NOTES = auto()
    PHONE = auto()
    ALL = auto()
    ADD_BIRTHDAY = auto()
    SHOW_BIRTHDAY = auto()
    SHOW_BIRTHDAYS = auto()
    EDIT_CONTACT_INFO = auto()
    EDIT_CONTACT_PHONE = auto()
    DELETE_CONTACT_PHONE = auto()
    DELETE_CONTACT_INFO = auto()
    DELETE_CONTACT = auto()
    HELLO = auto()
    SEARCH_BY = auto()
    CLOSE = auto()
    EXIT = auto()
    HELP = auto()


commands = {
    "add": {
        "id": BotCmd.ADD,
        "description": "Add a new contact or add details to an existing contact",
        "format": "add [name] [phone/email/address/note/birthday]",
        "subcommands": {
            "name": "Add a new contact with a name",
            "phone": "Add a phone number to an existing contact",
            "email": "Add/replace an email for the specified contact",
            "address": "Add/replace an address for the specified contact",
            "note": "Add note for the specified contact",
            "birthday": "Add a birthday (DD.MM.YYYY) for the specified contact",
        },
    },
    "help": {
        "id": BotCmd.HELP,
        "description": "Show help information",
        "format": "help",
        "subcommands": {},
    },
    "exit": {
        "id": BotCmd.EXIT,
        "description": "Exit the program",
        "format": "exit",
        "subcommands": {},
    },
    # ... (інші команди)
}


def build_completer(commands):
    completer_dict = {}
    for command, details in commands.items():
        if "subcommands" in details:
            completer_dict[command] = build_completer(details["subcommands"])
        else:
            completer_dict[command] = None
    return completer_dict


def display_help(commands):
    for command, details in commands.items():
        print(f"{Fore.CYAN}{command}{Style.RESET_ALL}: {details['description']}")
        if "subcommands" in details:
            for subcommand, subdesc in details["subcommands"].items():
                print(f"  {Fore.YELLOW}{subcommand}{Style.RESET_ALL}: {subdesc}")


def process_command(command, args):
    match command:
        case BotCmd.CLOSE | BotCmd.EXIT:
            print(f"{Fore.YELLOW}Good bye!{Style.RESET_ALL}")
            return False
        case BotCmd.HELLO:
            print(f"{Fore.GREEN}How can I help you?{Style.RESET_ALL}")
        case BotCmd.ADD:
            print(f"{Fore.GREEN}Adding contact...{Style.RESET_ALL}")
        # Додайте інші команди тут
        case BotCmd.HELP:
            display_help(commands)
        case _:
            print(f"{Fore.RED}Invalid command.{Style.RESET_ALL}")
    return True


completer = NestedCompleter.from_nested_dict(build_completer(commands))

session = PromptSession(completer=completer)


def get_bottom_toolbar():
    text = session.default_buffer.text.strip()
    parts = text.split()
    if parts:
        command_name = parts[0]
        command = commands.get(command_name)
        if command:
            return ANSI(f"{Fore.GREEN}Format: {command['format']}{Style.RESET_ALL}")
    return ANSI(
        f"{Fore.GREEN}Format: command [subcommand] [arguments]{Style.RESET_ALL}"
    )


running = True
while running:
    try:
        text = session.prompt("> ", bottom_toolbar=get_bottom_toolbar)
        parts = shlex.split(text.strip())
        if parts:
            command_name = parts[0]
            args = parts[1:]
            command = commands.get(command_name, {}).get("id")
            if command:
                running = process_command(command, args)
            else:
                print(f"{Fore.RED}Unknown command: {command_name}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        continue
    except EOFError:
        break
