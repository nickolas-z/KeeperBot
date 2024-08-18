from enum import Enum, auto
from typing import Union
from colorama import Fore

class BotCmd(Enum):
    """
    Enum for available commands.
    """

    HELLO = auto()
    HELP = auto()
    CLOSE = auto()
    EXIT = auto()
    ADD_CONTACT = auto()
    ADD_EMAIL = auto()
    ADD_ADDRESS = auto()
    ADD_BIRTHDAY = auto()
    ADD_NOTE = auto()
    ADD_TAG = auto()

    SHOW_ALL_CONTACTS = auto()
    SHOW_BIRTHDAY = auto()
    SHOW_BIRTHDAYS = auto()
    SHOW_PHONES = auto()
    SHOW_NOTES = auto()

    EDIT_INFO = auto()
    EDIT_PHONE = auto()
    EDIT_NOTE = auto()

    DELETE_CONTACT = auto()
    DELETE_PHONE = auto()
    DELETE_INFO = auto()
    DELETE_NOTE = auto()
    DELETE_TAG = auto()

    FIND_NOTES_BY_TAG = auto()
    FIND_NOTES_BY_TITLE = auto()

    SEARCH_BY = auto()
    SEARCH_BY_ALL = auto()
    SEARCH_BY_NAME = auto()
    SEARCH_BY_PHONE = auto()
    SEARCH_BY_EMAIL = auto()
    SEARCH_BY_ADDRESS = auto()
    SEARCH_BY_BIRTHDAY = auto()
    SEARCH_BY_NOTE = auto()
    SEARCH_BY_TAG = auto()

    @staticmethod
    def get_commands():
        """
        This function returns a dictionary of all available commands.
        Return:
            dict: all available commands.
        """
        return {
            "hello": {
                "id": BotCmd.HELLO,
                "description": f"Get a greeting from the bot",
                "format": "",
                "subcommands": {},
            },
            "help": {
                "id": BotCmd.HELP,
                "description": "Displays help for available commands",
                "format": "",
                "subcommands": {},
            },
            "exit": {
                "id": BotCmd.EXIT,
                "description": "Exit the program",
                "format": "",
                "subcommands": {},
            },
            "close": {
                "id": BotCmd.EXIT,
                "description": "Exit the program",
                "format": "",
                "subcommands": {},
            },
            "add": {
                "description": "Add a new contact or add details to an existing contact",
                "format": "[contact, email, address, birthday, note, tags]",
                "subcommands": {
                    "contact": {
                        "id": BotCmd.ADD_CONTACT,
                        "description": "Add a new contact with a name or replace an existing phone number",
                        "format": "[name] [phone]",
                        "subcommands": {},
                    },
                    "email": {
                        "id": BotCmd.ADD_EMAIL,
                        "description": "Add/replace an email for the specified contact",
                        "format": "[name] [email]",
                        "subcommands": {},
                    },
                    "address": {
                        "id": BotCmd.ADD_ADDRESS,
                        "description": "Add/replace an address for the specified contact",
                        "format": "[name] [address]",
                        "subcommands": {},
                    },
                    "birthday": {
                        "id": BotCmd.ADD_BIRTHDAY,
                        "description": "Add/replace a birthday for the specified contact",
                        "format": "[name] [DD.MM.YYYY]",
                        "subcommands": {},
                    },
                    "note": {
                        "id": BotCmd.ADD_NOTE,
                        "description": "Add note for the specified contact",
                        "format": "[contact name]",
                        "subcommands": {},
                    },
                    "tags": {
                        "id": BotCmd.ADD_TAG,
                        "description": "Add tag to note",
                        "format": "[note title]",
                        "subcommands": {},
                    },
                },
            },
            "edit": {
                "description": "Edit contact information",
                "format": "[info, phone, note]",
                "subcommands": {
                    "info": {
                        "id": BotCmd.EDIT_INFO,
                        "description": "Edit contact information",
                        "format": "[name] [name, birthday, email, address] [new value]",
                        "subcommands": {},
                    },
                    "phone": {
                        "id": BotCmd.EDIT_PHONE,
                        "description": "Edit contact phone number",
                        "format": "[name] [old phone] [new phone]",
                        "subcommands": {},
                    },
                    "note": {
                        "id": BotCmd.EDIT_NOTE,
                        "description": "Edit note by title",
                        "format": "[contact name] [note title]",
                        "subcommands": {},
                    },
                },
            },
            "delete": {
                "description": "Delete contact information",
                "format": "[contact, phone, info, note, tag]",
                "subcommands": {
                    "contact": {
                        "id": BotCmd.DELETE_CONTACT,
                        "description": "Delete contact",
                        "format": "contact [name]",
                        "subcommands": {},
                    },
                    "phone": {
                        "id": BotCmd.DELETE_PHONE,
                        "description": "Delete contact phone number",
                        "format": "[name] [phone]",
                        "subcommands": {},
                    },
                    "info": {
                        "id": BotCmd.DELETE_INFO,
                        "description": "Delete contact info",
                        "format": "[name] [birthday, email, address]",
                        "subcommands": {},
                    },
                    "note": {
                        "id": BotCmd.DELETE_NOTE,
                        "description": "Delete note by title",
                        "format": "[contact name] [note title]",
                        "subcommands": {},
                    },
                    "tag": {
                        "id": BotCmd.DELETE_TAG,
                        "description": "Delete tag",
                        "format": "[tag name] [note title]",
                        "subcommands": {},
                    },
                },
            },
            "show": {
                "description": "Show information about a contact",
                "format": "[all, birthday, birthdays, phones, notes]",
                "subcommands": {
                    "all": {
                        "id": BotCmd.SHOW_ALL_CONTACTS,
                        "description": "Show all contacts in the address book",
                        "format": "",
                        "subcommands": {},
                    },
                    "birthday": {
                        "id": BotCmd.SHOW_BIRTHDAY,
                        "description": "Show the birthday for the specified contact",
                        "format": "[name]",
                        "subcommands": {},
                    },
                    "birthdays": {
                        "id": BotCmd.SHOW_BIRTHDAYS,
                        "description": "Show birthdays that will occur within the next number of days, empty for today",
                        "format": "[days/empty]",
                        "subcommands": {},
                    },
                    "phones": {
                        "id": BotCmd.SHOW_PHONES,
                        "description": "Show phones for the specified contact",
                        "format": "[name]",
                        "subcommands": {},
                    },
                    "notes": {
                        "id": BotCmd.SHOW_NOTES,
                        "description": "Show all notes phones for the specified contact",
                        "format": "[name]",
                        "subcommands": {},
                    },
                },
            },
            "find": {
                "description": "Find information about a contact",
                "format": "[notes-by-tag, notes-by-title]",
                "subcommands": {
                    "notes-by-tag": {
                        "id": BotCmd.FIND_NOTES_BY_TAG,
                        "description": "Find all notes by tag",
                        "format": "",
                        "subcommands": {},
                    },
                    "notes-by-title": {
                        "id": BotCmd.FIND_NOTES_BY_TITLE,
                        "description": "Find notes by title",
                        "format": "[note title]",
                        "subcommands": {},
                    },
                },
            },
            "search-by": {
                "description": "Search for contacts by field",
                "format": "[all, name, phone, email, address, birthday, note, tag]",
                "subcommands": {
                    "all": {
                        "id": BotCmd.SEARCH_BY_ALL,
                        "description": "Search by all fields for all contacts",
                        "format": "[text]",
                        "subcommands": {},
                    },
                    "name": {
                        "id": BotCmd.SEARCH_BY_NAME,
                        "description": "Search by name for all contacts",
                        "format": "[text]",
                        "subcommands": {},
                    },
                    "phone": {
                        "id": BotCmd.SEARCH_BY_PHONE,
                        "description": "Search by phone for all contacts",
                        "format": "[phone]",
                        "subcommands": {},
                    },
                    "email": {
                        "id": BotCmd.SEARCH_BY_EMAIL,
                        "description": "Search by email for all contacts",
                        "format": "[email]",
                        "subcommands": {},
                    },
                    "address": {
                        "id": BotCmd.SEARCH_BY_ADDRESS,
                        "description": "Search by address for all contacts",
                        "format": "[address]",
                        "subcommands": {},
                    },
                    "birthday": {
                        "id": BotCmd.SEARCH_BY_BIRTHDAY,
                        "description": "Search by birthday for all contacts",
                        "format": "[DD.MM.YYYY]",
                        "subcommands": {},
                    },
                    "note": {
                        "id": BotCmd.SEARCH_BY_NOTE,
                        "description": "Search by note for all contacts",
                        "format": "[note title]",
                        "subcommands": {},
                    },
                    "tag": {
                        "id": BotCmd.SEARCH_BY_TAG,
                        "description": "Search by tag for all contacts",
                        "format": "[tag name]",
                        "subcommands": {},
                    },
                },
            },
        }

    @staticmethod
    def show_help() -> None:
        """
        This function displays help for available commands.
        """
        print(f"{Fore.CYAN}Available commands (tab to complete):")
        for cmd, details in BotCmd.get_commands().items():
            print(
                f"{Fore.YELLOW}{cmd} {Fore.WHITE} {details['format']}: {Fore.LIGHTBLACK_EX}{details['description']}"
            )
            if "subcommands" in details and details["subcommands"]:
                for subcmd, subdetails in details["subcommands"].items():
                    print(
                        f"  {Fore.GREEN}{subcmd} {Fore.WHITE}{subdetails['format']}: {Fore.LIGHTBLACK_EX} {subdetails['description']}"
                    )

    @staticmethod
    def get_command_format(command, args) -> str:
        commands = BotCmd.get_commands()
        if command in commands:
            cmd_details = commands[command]
            if (
                "subcommands" in cmd_details
                and args
                and args[0] in cmd_details["subcommands"]
            ):
                subcommand = args[0]
                subcmd_details = cmd_details["subcommands"][subcommand]
                return f"{command} {subcmd_details['format']}"
            else:
                return f"{command} {cmd_details['format']}"
        return None

    @staticmethod
    def create_completer_dict(commands=None) -> dict:
        """
        This function creates a nested dictionary for the completer.

        Return:
            dict: nested dictionary for the completer.
        """
        commands = BotCmd.get_commands() if commands is None else commands
        completer_dict = {}
        for cmd, details in commands.items():
            if "subcommands" in details and details["subcommands"]:
                completer_dict[cmd] = BotCmd.create_completer_dict(details["subcommands"])
            else:
                completer_dict[cmd] = None
        return completer_dict

    @staticmethod
    def get_command_name(command) -> Union[str, None]:
        """
        This function returns the command name
        from get_commands() and all fields subcommands for the given command enum.
        Args:
            command (BotCmd): command id.
        Return:
            str: command name.
        """
        commands = BotCmd.get_commands()
        for cmd, details in commands.items():
            if "id" in details and command == details["id"]:
                return cmd
            if "subcommands" in details:
                for subcmd, subdetails in details["subcommands"].items():
                    if "id" in subdetails and command == subdetails["id"]:
                        return subcmd

    def get_command_name(self) -> Union[str, None]:
        """
        This function returns the command name
        from get_commands() and all fields subcommands for the given command enum.
        Args:
            command (BotCmd): command id.
        Return:
            str: command name.
        """
        commands = BotCmd.get_commands()
        for cmd, details in commands.items():
            if "id" in details and self == details["id"]:
                return cmd
            if "subcommands" in details:
                for subcmd, subdetails in details["subcommands"].items():
                    if "id" in subdetails and self == subdetails["id"]:
                        return subcmd

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return self.name.lower()

    def __int__(self):
        return self.value

    def __hash__(self) -> int:
        return super().__hash__()
