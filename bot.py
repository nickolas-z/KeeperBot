import pickle
from functools import wraps
from typing import Union

from colorama import Fore, Style, init
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.formatted_text import ANSI
from tabulate import tabulate

from AddressBook import Record, AddressBook, Birthday, Note
from bot_cmd import BotCmd
from helpers import Application, input_error, print_execution_time

init(autoreset=True)


class Bot(Application):
    """
    Application class
    """

    contacts_info = None

    def __init__(self, app_name, filename="addressbook.pkl"):
        super().__init__(app_name)
        self.filename = filename
        self.book = Bot.__load_data(self.filename)

        self.__session = PromptSession()
        self.__completer_dict = BotCmd.create_completer_dict()
        self.__completer = NestedCompleter.from_nested_dict(self.__completer_dict)

        Bot.contacts_info = self.book

    def get_bottom_toolbar(self):
        """
        This function returns the bottom toolbar text.
        Return:
            str: bottom toolbar text.
        """
        text = self.__session.default_buffer.text.strip()
        parts = text.split()
        # this function found in BotCmd.get_commands() command sequence and return format of command
        if parts:
            command_name = parts[0]
            command = BotCmd.get_command_format(command_name, parts[1:])
            if command:
                return ANSI(f"{Fore.GREEN}Format: {command}{Style.RESET_ALL}")

        return ANSI(
            f"{Fore.GREEN}Format: command [subcommand] [arguments]{Style.RESET_ALL}"
        )

    @staticmethod
    def __confirm(message):
        """
        This function asks the user for confirmation.
        Args:
            message: the message to display.
        Return:
            bool: True if the user confirms, False otherwise.
        """
        print(f"{Fore.YELLOW}{message}")
        user_input = input("Enter 'yes' to confirm: ")
        return user_input.strip().lower() == "yes"

    @staticmethod
    def data_saver(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            Bot.__save_data(Bot.contacts_info)

            return result

        return inner

    @data_saver
    @input_error
    def add_contact(self, args):
        """
        This function adds a new contact to the address book.
        Args:
            args: list of command arguments.
        Return:
            str: message indicating the execution result.
        """
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: add [name] [phone]{Style.RESET_ALL}"
            )
        name, phone, *_ = args

        # Check if the phone number already exists for another contact
        existing_contact = self.book.find_phone(phone)
        if existing_contact:
            if existing_contact.name.value != name:
                # Ask for confirmation to add the same phone number to the new contact
                message = (
                    f"Phone number {Fore.WHITE}{phone}{Fore.YELLOW} already exists for contact "
                    f"{Fore.WHITE}{existing_contact.name}{Fore.YELLOW}. "
                    f"Add it to {Fore.WHITE}{name}{Fore.YELLOW}?"
                )
                if not Bot.__confirm(message):
                    return f"{Fore.RED}Operation cancelled.{Style.RESET_ALL}"

        record = self.book.find_contact(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            self.book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        return message

    def show_all(self):
        """This function displays all contacts.
        Return:
            str: list of contacts.
        """
        if self.book.data:
            self.book.data = dict(sorted(self.book.data.items()))
        return self.build_table_for_records(self.book.values())

    def build_table_for_records(self, records):
        if not records:
            return "No contacts found."

        table_data = [
            [
                record.name,
                ", ".join(str(phone) for phone in record.phones),
                record.email,
                record.birthday,
                record.address,
                ", ".join(note.title for note in record.notes),
                ", ".join(
                    ", ".join(str(tag) for tag in note.tags) for note in record.notes
                ),
                "+" if record.owner else "",
            ]
            for record in records
        ]

        headers = [
            "Name",
            "Phone",
            "Email",
            "Birthday",
            "Address",
            "Notes",
            "Tag",
            "Owner",
        ]

        return tabulate(table_data, headers, tablefmt="fancy_grid")

    @input_error
    def show_phones(self, args):
        """This function displays the phone number of a contact.
        Args:
            args: list of command arguments.
        Return:
            str: phone number of the contact.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: phone [name]{Style.RESET_ALL}"
            )

        name = args[0]
        record = self.book.find_contact(name)

        if record:
            phones = [phone.value for phone in record.phones]
            if phones:
                table_data = [[name, phone] for phone in phones]
                headers = ["Name", "Phone Number"]
                print(tabulate(table_data, headers, tablefmt="fancy_grid"))
                return ""
            else:
                return f"{Fore.RED}No phone numbers found for {name}.{Style.RESET_ALL}"
        else:
            raise KeyError(f"{Fore.RED}Contact {name} not found.{Style.RESET_ALL}")

    @data_saver
    @input_error
    def add_birthday(self, args):
        """
        This function adds a birthday to a contact.
        Args:
            args: list of command arguments.
        Return:
            str: message indicating the execution result.
        """
        if len(args) != 2:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: add-birthday [name] [birthday]{Style.RESET_ALL}"
            )
        name, birthday = args
        record = self.book.find_contact(name)
        if record:
            record.add_birthday(birthday)
            return f"Birthday for {name} added."
        else:
            raise KeyError(f"{Fore.RED}Contact {name} not found.{Style.RESET_ALL}")

    @input_error
    def show_birthday(self, args):
        """
        This function displays the birthday of a contact.
        Args:
            args: list of command arguments.
        Return:
            str: birthday of the contact.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: show-birthday [name]{Style.RESET_ALL}"
            )
        name = args[0]

        record = self.book.find_contact(name)
        if record:
            birthday = (
                record.birthday.value.strftime(Birthday.BIRTHDAY_FORMAT)
                if record.birthday
                else "Not set"
            )
            table_data = [[name, birthday]]
            headers = ["Name", "Birthday"]
            print(tabulate(table_data, headers, tablefmt="fancy_grid"))
        else:
            raise KeyError(f"{Fore.RED}Contact {name} not found.{Style.RESET_ALL}")

    @input_error
    def show_birthdays(self, args):
        """
        This function displays birthdays that will occur within the next week.
        Return:
            str: list of birthdays.
        """
        upcoming_birthdays = list()

        if len(args) == 0:
            upcoming_birthdays = self.book.get_upcoming_birthdays()
        elif len(args) == 1 and args[0].isdigit():
            upcoming_birthdays = self.book.get_upcoming_birthdays(int(args[0]))
        else:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: show-birthdays [number of days or empty for today]{Style.RESET_ALL}"
            )

        if not upcoming_birthdays:
            print(f"No upcoming birthdays.")
            return

        table_data = [[record.name, record.birthday] for record in upcoming_birthdays]

        headers = ["Name", "Birthday"]
        print(f"{Fore.GREEN}Upcoming birthdays:{Style.RESET_ALL}")
        print(tabulate(table_data, headers, tablefmt="fancy_grid"))

    @staticmethod
    def __save_data(book, filename="addressbook.pkl"):
        """
        Save the given book data to a file using pickle serialization.
        Args:
            book: The book data to be saved.
            filename: The name of the file to save the data to. Default is "addressbook.pkl".
        Returns:
            None
        """

        with open(filename, "wb") as f:
            pickle.dump(book, f)

    @staticmethod
    def __load_data(filename: str) -> AddressBook:
        """
        Load the book data from a file using pickle serialization.
        Args:
            filename: The name of the file to load the data from.
        Returns:
            AddressBook: The loaded book data.
        """
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()

    @data_saver
    @input_error
    def add_owner(self):
        print("Let's start by recording your personal details.", end="\n\n")

        res = input(
            f"Record your data: {Fore.GREEN}Yes{Style.RESET_ALL}/{Fore.RED}No{Style.RESET_ALL} "
        )

        if res.lower() == "Yes".lower():
            name = input("Your name: ")

            record = Record(name)
            record.check_owner()

            self.book.add_record(record)

            def add_owner_phone():
                telephone = input(
                    f"{Fore.CYAN}{name}{Style.RESET_ALL}, please enter your phone: "
                )

                try:
                    record.add_phone(telephone)
                except ValueError as e:
                    print(Fore.RED + str(e))
                    return add_owner_phone()

                if record.name and record.phones:
                    return f"{Fore.GREEN}{record.name} - {record.phones[0]} "

            print(add_owner_phone())

    @data_saver
    @input_error
    def add_email(self, args):
        if len(args) != 2:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: add-email [name] [email]{Style.RESET_ALL}"
            )
        name, email = args

        record = self.book.find_contact(name)
        if record:
            record.add_email(email)
            return f"Email for {name} added."
        else:
            raise KeyError(
                f"{Fore.RED}Contact {name} not found. Please create contact first. {Style.RESET_ALL}"
            )

    @data_saver
    @input_error
    def add_address(self, args):
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: add-address [name] [address]{Style.RESET_ALL}"
            )
        name = args[0]
        del args[0]
        address = " ".join(args)

        record = self.book.find_contact(name)
        if record:
            record.add_address(address)
            return f"Address for {name} added."
        else:
            raise KeyError(
                f"{Fore.RED}Contact {name} not found. Please create contact first. {Style.RESET_ALL}"
            )

    @input_error
    def search_by(self, args) ->  Union[str, None]:
        """
        This function interacts with the user to gather search criteria,
        and then performs the search based on the provided criteria.
        """
        # Proceed with the search using the provided or collected args
        if len(args) != 2:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: search-by [field] [value]{Style.RESET_ALL}"
            )

        field, value = args
        # Assuming AddressBook has a method find_contacts_by_field
        records = self.book.find_contacts_by_field(field, value)

        if records:
            print(f"{self.build_table_for_records(records)}")
            return ""
        else:
            raise KeyError(
                f"{Fore.RED}No contacts found for the specified {field}.{Style.RESET_ALL}"
            )

    @data_saver
    @input_error
    def add_note(self, args):
        """
        This function adds a note to a contact.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: add note [conntact name]{Style.RESET_ALL}"
            )
        contact_name, *_ = args

        record = self.book.find_contact(contact_name)
        if record:
            title = input("Enter note title: ")
            if not title:
                return None

            note = input("Enter note content: \n")
            record.add_note(title, note)

            return f"Note for {contact_name} added."
        else:
            raise KeyError(
                f"{Fore.RED}Contact {contact_name} not found. Please create contact first. {Style.RESET_ALL}"
            )

    @data_saver
    @input_error
    def edit_note(self, args):
        """
        This function edits a note of a contact.
        """
        if len(args) < 1:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: edit note [contact name] [note title]{Style.RESET_ALL}"
            )
        owner, *note_title = args
        note_title = " ".join(note_title)

        record = self.book.find_contact(owner)
        if not record:
            raise KeyError(f"{Fore.RED}Contact {owner} not found. {Style.RESET_ALL}")

        note = record.find_note_by_title(note_title)
        if note:

            def get_new_value(title=None, value=None):
                if not title:
                    title = input("Enter new note title: \n")
                    if not title:
                        print(f"{Fore.RED}Title cannot be empty. {Style.RESET_ALL}")
                        return get_new_value()

                new_value = input("Enter new note content: \n")
                return Note(title, new_value)

            new_note = get_new_value()
            record.edit_note_by_title(note_title, new_note.title, new_note.value)
            return f"Note {note_title} edited. New note: {note}"
        else:
            raise KeyError(f"{Fore.RED}Note {note_title} not found. {Style.RESET_ALL}")

    @data_saver
    @input_error
    def delete_note(self, args):
        """
        This function deletes a note of a contact.
        """
        if len(args) < 1:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: delete-note [note_title]{Style.RESET_ALL}"
            )
        owner, *note_title = args
        note_title = " ".join(note_title)

        record = self.book.find_contact(owner)
        if not record:
            raise KeyError(f"{Fore.RED}Contact {owner} not found. {Style.RESET_ALL}")

        record.remove_note_by_title(note_title)
        return f"Note {note_title} deleted."

    @data_saver
    @input_error
    def add_tags(self, args):
        """
        This function adds tags to a note.
        """
        if len(args) < 1:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: add tags [note title]{Style.RESET_ALL}"
            )
        note_title = " ".join(args)

        note = self.book.find_note_by_title(note_title)
        if note:
            tags = input("Enter tags separated by space: ").split()
            note.tags = note.tags + tags
            return f"Tags added to {note_title}."
        else:

            raise KeyError(f"{Fore.RED}Note {note_title} not found. {Style.RESET_ALL}")

    @data_saver
    @input_error
    def delete_tag(self, args):
        """
        This function deletes a tag from a note.
        """
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: delete tag [tag] [note_title]{Style.RESET_ALL}"
            )
        tag, *note_title = args
        note_title = " ".join(note_title)

        note = self.book.find_note_by_title(note_title)
        if note:
            note.tags = [t for t in note.tags if t != tag]
            return f"Tag {tag} deleted from {note_title}."
        else:
            raise KeyError(f"{Fore.RED}Note {note_title} not found. {Style.RESET_ALL}")

    @input_error
    def get_notes_by_tag(self, args):
        """
        This function finds all notes with specified tag.
        """

        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: get-notes-by-tag [tag]{Style.RESET_ALL}"
            )
        tag, *_ = args

        notes = self.book.find_notes_by_tag(tag)
        if notes:
            return self.build_table_for_notes(notes)
        else:
            raise KeyError(f"{Fore.RED}Notes not found. {Style.RESET_ALL}")

    @input_error
    def get_note_by_title(self, args):
        """
        This function finds note by title.
        """
        if len(args) < 1:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: find notes-by-title [note title]{Style.RESET_ALL}"
            )
        note_title = " ".join(args)

        note = self.book.find_note_by_title(note_title)
        if note:
            return str(note)
        else:
            raise KeyError(f"{Fore.RED}Note {note_title} not found. {Style.RESET_ALL}")

    @input_error
    def get_notes(self, args):
        """
        This function finds all notes for specified contact.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: show notes [name]{Style.RESET_ALL}"
            )
        name, *_ = args

        record = self.book.find_contact(name)

        if record:
            return self.build_table_for_notes(record.notes)
        else:
            raise KeyError(f"{Fore.RED}Contact not found. {Style.RESET_ALL}")

    def build_table_for_notes(self, notes):
        """
        This function builds a table for notes.
        Args:
            notes: list of notes.
        """
        table_data = [
            [note.title, ", ".join(str(tag) for tag in note.tags), note.value]
            for note in notes
        ]

        headers = ["Title", "Tags", "Note"]

        return tabulate(table_data, headers, tablefmt="fancy_grid")

    @data_saver
    @input_error
    def delete_contact(self, args):
        """
        This function deletes a contact from the address book.
        Args:
            args: list of command arguments.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: delete contact [name]{Style.RESET_ALL}"
            )
        name, *_ = args
        record = self.book.find_contact(name)
        if record:
            return self.book.delete(name)
        else:
            return f"Contact with name {name} not found"

    @data_saver
    @input_error
    def edit_contact_info(self, args):
        """
        This function edits a contact's information.
        Args:
            args: list of command arguments
        """
        if len(args) < 3:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: edit info [name] [field name] [new value]{Style.RESET_ALL}"
            )
        name, field, *new_value = args
        new_value = " ".join(new_value)

        record = self.book.find_contact(name)
        method = field.lower()
        if method == "name" and record:
            return self.book.update_name(name, new_value)
        if record:
            return getattr(record, f"edit_{method}")(new_value)
        else:
            return f"{Fore.RED}Contact with name {name} not found{Style.RESET_ALL}"

    @data_saver
    @input_error
    def delete_contact_info(self, args):
        """
        This function deletes a contact's information.
        Args:
            args: list of command arguments
        """
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: delete іnfo [name] [field name]{Style.RESET_ALL}"
            )
        name, field, *_ = args
        record = self.book.find_contact(name)
        method = field.lower()
        if record:
            return getattr(record, f"delete_{method}")()
        else:
            return f"Contact with name {name} not found"

    @data_saver
    @input_error
    def edit_contact_phone(self, args):
        """
        This function edits a contact's phone number.
        Args:
            args: list of command arguments
        """
        if len(args) < 3:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: edit phone [name] [old phone] [new phone]{Style.RESET_ALL}"
            )
        name, old_number, new_number, *_ = args
        record = self.book.find_contact(name)
        if record:
            return record.edit_phone(old_number, new_number)
        else:
            return f"Contact with name {name} not found"

    @data_saver
    @input_error
    def delete_contact_phone(self, args):
        """
        This function deletes a contact's phone number.
        Args:
            args: list of command arguments
        """
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid format. Use: delete-contact-phone [name] [phone number]{Style.RESET_ALL}"
            )
        name, number, *_ = args
        record = self.book.find_contact(name)
        if record:
            return record.remove_phone(number)
        else:
            return f"Contact with name {name} not found"

    def handle_command(self, command: BotCmd, args) -> bool:
        """
        This function handles the user command.
        Args:
            command: the command to execute.
            args: list of command arguments.
        Return:
            bool: True if the command was handled successfully, False otherwise.
        """
        match command:
            case BotCmd.HELLO:
                print(
                    f"{Fore.GREEN} Hi {self.__owner.name if self.__owner else ''}! How can I help you?"
                )
            case BotCmd.HELP:
                BotCmd.show_help()
            case BotCmd.CLOSE | BotCmd.EXIT:
                print(
                    f"{Fore.YELLOW}Good bye{' ' + str(self.__owner.name) if self.__owner else ''}!{Style.RESET_ALL}"
                )
                return False
            case BotCmd.ADD_CONTACT:
                print(f"{Fore.GREEN}{self.add_contact(args)}")
            case BotCmd.ADD_EMAIL:
                print(f"{Fore.GREEN}{self.add_email(args)}")
            case BotCmd.ADD_ADDRESS:
                print(f"{Fore.GREEN}{self.add_address(args)}")
            case BotCmd.ADD_BIRTHDAY:
                print(f"{Fore.GREEN}{self.add_birthday(args)}")
            case BotCmd.ADD_NOTE:
                print(f"{Fore.GREEN}{self.add_note(args)}")
            case BotCmd.ADD_TAG:
                print(f"{Fore.GREEN}{self.add_tags(args)}")

            case BotCmd.SHOW_ALL_CONTACTS:
                print(self.show_all())
            case BotCmd.SHOW_BIRTHDAY:
                self.show_birthday(args)
            case BotCmd.SHOW_BIRTHDAYS:
                self.show_birthdays(args)
            case BotCmd.SHOW_PHONES:
                print(f"{Fore.GREEN}{self.show_phones(args)}")
            case BotCmd.SHOW_NOTES:
                print(f"{self.get_notes(args)}")

            case BotCmd.EDIT_INFO:
                print(f"{Fore.GREEN}{self.edit_contact_info(args)}")
            case BotCmd.EDIT_PHONE:
                print(f"{Fore.GREEN}{self.edit_contact_phone(args)}")
            case BotCmd.EDIT_NOTE:
                print(f"{Fore.GREEN}{self.edit_note(args)}")

            case BotCmd.DELETE_CONTACT:
                print(f"{Fore.GREEN}{self.delete_contact(args)}")
            case BotCmd.DELETE_PHONE:
                print(f"{Fore.GREEN}{self.delete_contact_phone(args)}")
            case BotCmd.DELETE_INFO:
                print(f"{Fore.GREEN}{self.delete_contact_info(args)}")
            case BotCmd.DELETE_NOTE:
                print(f"{Fore.GREEN}{self.delete_note(args)}")
            case BotCmd.DELETE_TAG:
                print(f"{Fore.GREEN}{self.delete_tag(args)}")

            case BotCmd.FIND_NOTES_BY_TAG:
                print(f"{self.get_notes_by_tag(args)}")
            case BotCmd.FIND_NOTES_BY_TITLE:
                print(f"{Fore.GREEN}{self.get_note_by_title(args)}")

            case (
                BotCmd.SEARCH_BY_ALL
                | BotCmd.SEARCH_BY_NAME
                | BotCmd.SEARCH_BY_PHONE
                | BotCmd.SEARCH_BY_EMAIL
                | BotCmd.SEARCH_BY_ADDRESS
                | BotCmd.SEARCH_BY_BIRTHDAY
                | BotCmd.SEARCH_BY_NOTE
                | BotCmd.SEARCH_BY_TAG
            ):
                args = [command.get_command_name(), *args]
                print(f"{Fore.GREEN}{self.search_by(args)}")

        return True

    @data_saver
    @print_execution_time
    def run(self):
        """
        This function runs the application.
        """
        self.__owner = self.book.get_owner()

        if self.__owner is None:
            self.add_owner()
        else:
            print(
                f"{Fore.WHITE}Glad to see you, {self.__owner.name}!{Style.RESET_ALL}",
                end="\n\n",
            )

        BotCmd.show_help()
        print(f"\nAddress book has {len(self.book.data)} contact(s).\n")
        print(f"Enter a command to continue...")

        # get all commands for loop usage
        commands = BotCmd.get_commands()

        while True:
            user_input = self.__session.prompt(
                "> ", completer=self.__completer, bottom_toolbar=self.get_bottom_toolbar
            )
            parts = user_input.split()
            if not parts:
                continue

            command = parts[0]
            args = parts[1:]

            if command in commands:
                cmd_details = commands[command]
                if (
                    "subcommands" in cmd_details
                    and args
                    and args[0] in cmd_details["subcommands"]
                ):
                    subcommand = args[0]
                    subcmd_details = cmd_details["subcommands"][subcommand]
                    if not self.handle_command(subcmd_details["id"], args[1:]):
                        break
                else:
                    if "id" in cmd_details:
                        if not self.handle_command(cmd_details["id"], args):
                            break
                    elif "format" in cmd_details:
                        print(
                            f"{Fore.RED}{command} {cmd_details['format']}"
                        )
                    else:
                        print(
                            f"{Fore.RED}Unknown subcommand: {args[0] if args else {command}}"
                        )
            else:
                print(f"{Fore.RED}Unknown command: {command}")
