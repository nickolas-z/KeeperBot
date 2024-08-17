import pickle
from functools import wraps

from colorama import Fore, Style, init
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from tabulate import tabulate

from AddressBook import Record, AddressBook, Birthday
from bot_cmd import BotCmd
from helpers import Application, input_error, print_execution_time
from AddressBook.addressbook_errors import (
    InvalidEmailError,
    InvalidPhoneNumberError,
    InvalidBirthdayError,
)


class Bot(Application):
    """
    Application class
    """

    contacts_info = None

    def __init__(self, app_name, filename="addressbook.pkl"):
        super().__init__(app_name)
        self.filename = filename
        self.book = Bot.__load_data(self.filename)

        self.commands_list = BotCmd.get_all_commands(exclude_prefix="@")
        self.command_completer = WordCompleter(self.commands_list, ignore_case=True)
        self.session = PromptSession(completer=self.command_completer)
        Bot.contacts_info = self.book

    @staticmethod
    def __parse_input(user_input):
        """
        This function splits the user input string into a command and arguments.
        Args:
            user_input: the string input by the user.
        Return:
            tuple: (command, list of arguments) or None if the input is incorrect.
        """
        try:
            cmd, *args = user_input.split()
            cmd = cmd.strip().lower()
            return BotCmd(cmd), args
        except ValueError:
            return None

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

    def data_saver(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            Bot.__save_data(Bot.contacts_info)

            return result

        return inner

    @data_saver
    @input_error
    def add_contact(self, args=None):
        """
        This function adds a new contact to the address book step-by-step.
        Args:
            args: list of command arguments (optional).
        Return:
            str: message indicating the execution result.
        """
        if args is None or len(args) < 1:
            name = input("Please enter the name of the contact: ")
        else:
            name = args[0]

        while True:
            phone = input(f"Please enter the phone number for {name}: ")

            try:
                existing_contact = self.book.find_phone(phone)
                if existing_contact:
                    if existing_contact.name.value != name:
                        message = (
                            f"Phone number {Fore.WHITE}{phone}{Fore.YELLOW} already exists for contact "
                            f"{Fore.WHITE}{existing_contact.name}{Fore.YELLOW}. "
                            f"Add it to {Fore.WHITE}{name}{Fore.YELLOW}?"
                        )
                        if not Bot.__confirm(message):
                            print(f"{Fore.RED}Operation cancelled.{Style.RESET_ALL}")
                            continue

                record = self.book.find_contact(name)
                message = "Contact updated."
                if record is None:
                    record = Record(name)
                    self.book.add_record(record)
                    message = "Contact added."

                record.add_phone(phone)
                return message
            except InvalidPhoneNumberError as e:
                print(str(e))
                print(
                    f"{Fore.YELLOW}Please enter a valid phone number.{Style.RESET_ALL}"
                )

                continue

    @data_saver
    @input_error
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
    def show_phone(self, args):
        """This function displays the phone number of a contact.
        Args:
            args: list of command arguments.
        Return:
            str: phone number of the contact.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: phone [name]{Style.RESET_ALL}"
            )

        name = args[0]
        record = self.book.find_contact(name)

        if record:
            phones = [phone.value for phone in record.phones]
            if phones:
                table_data = [[name, phone] for phone in phones]
                headers = ["Name", "Phone Number"]
                print(tabulate(table_data, headers, tablefmt="fancy_grid"))
            else:
                return f"{Fore.RED}No phone numbers found for {name}.{Style.RESET_ALL}"
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
                f"{Fore.RED}Invalid input. Use: show-birthday [name]{Style.RESET_ALL}"
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

    @data_saver
    @input_error
    def show_info(self, args=None):
        """
        This function provides a menu to show different types of contact information.
        Args:
            args: list of command arguments (optional).
        Return:
            str: message indicating the execution result.
        """
        print("Choose the information you want to display:")
        print("1. Show all contacts")
        print("2. Show phones for a contact")
        print("3. Show birthday for a contact")
        print("4. Show upcoming birthdays")
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            return self.show_all()

        elif choice == "2":
            if args is None or len(args) < 1:
                name = input("Please enter the name of the contact: ")
            else:
                name = args[0]
            return self.show_phone([name])

        elif choice == "3":
            if args is None or len(args) < 1:
                name = input("Please enter the name of the contact: ")
            else:
                name = args[0]
            return self.show_birthday([name])

        elif choice == "4":
            days = input(
                "Enter the number of days to show upcoming birthdays (or press Enter to show for today): "
            )
            return self.show_birthdays([days])

        else:
            return f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}"

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
                f"{Fore.RED}Invalid input. Use: show-birthdays [number of days or empty for today]{Style.RESET_ALL}"
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

    @staticmethod
    def __show_help() -> None:
        """
        This function displays help for available commands.
        """
        print(f"{Fore.WHITE}Available commands (tab to complete):")
        print(f"{Fore.GREEN}\tall - {Fore.YELLOW}Show {Fore.WHITE}all contacs.")
        print(
            f"{Fore.GREEN}\tadd-new-contact {Fore.YELLOW} "
            f"- add a new contact{Fore.WHITE} with a name and phone number, or add a phone number to an existing contact;"
        )
        print(
            f"{Fore.GREEN}\tadd-contact-info {Fore.YELLOW}[name]"
            f"- {Fore.WHITE}add contact information (phone, email, address, note, tags, boirthday) for the specified contact;"
        )
        print(
            f"{Fore.GREEN}\tedit-contact-info {Fore.YELLOW}[name]- {Fore.WHITE}edit or update contact info (name, phone, email, address, boirthday);"
        )
        print(
            f"{Fore.GREEN}\tshow-info {Fore.YELLOW}- show information{Fore.WHITE} (phones for a contact, birthday for a contact, upcoming birthdays);"
        )
        print(
            f"{Fore.GREEN}\tget-info {Fore.YELLOW}- get information{Fore.WHITE} (all notes, notes by tag, note by title);"
        )
        print(
            f"{Fore.GREEN}\tdelete-menu {Fore.YELLOW}- delete{Fore.WHITE} (contact, name, phone, email, address, boirthday, note);"
        )
        print(
            f"{Fore.GREEN}\tclose {Fore.WHITE}or {Fore.GREEN}exit - {Fore.YELLOW}close {Fore.WHITE}the program."
        )

    @data_saver
    @input_error
    def add_contact_info(self, args):
        """
        This function provides a menu to add different types of contact information.
        Args:
            args: list of command arguments.
        Return:
            str: message indicating the execution result.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: add-contact-info [name]{Style.RESET_ALL}"
            )

        name = args[0]
        print("Choose the information you want to add:")
        print("1. Phone")
        print("2. Email")
        print("3. Address")
        print("4. Note")
        print("5. Tags")
        print("6. Birthday")
        choice = input("Enter the number of your choice: ")

        record = self.book.find_contact(name)
        if not record:
            raise KeyError(f"{Fore.RED}Contact {name} not found.{Style.RESET_ALL}")

        if choice == "1":
            while True:
                phone = input(f"Enter the phone number for {name}: ")
                try:
                    record.add_phone(phone)
                    return f"Phone number {phone} added for {name}."
                except InvalidPhoneNumberError as e:
                    print(str(e))

        elif choice == "2":
            while True:
                email = input(f"Enter the email address for {name}: ")
                try:
                    record.add_email(email)
                    return f"Email address {email} added for {name}."
                except InvalidEmailError as e:
                    print(str(e))

        elif choice == "3":
            while True:
                address = input(f"Enter the address for {name}: ")
                try:
                    record.add_address(address)
                    return f"Address {address} added for {name}."
                except ValueError as e:
                    print(str(e))

        elif choice == "4":
            while True:
                note_title = input(f"Enter the title of the note for {name}: ")
                note_content = input("Enter the content of the note: ")
                try:
                    record.add_note(note_title, note_content)
                    return f"Note '{note_title}' added for {name}."
                except ValueError as e:
                    print(str(e))

        elif choice == "5":
            while True:
                note_title = input(
                    f"Enter the title of the note to add tags for {name}: "
                )
                tags = input("Enter tags separated by spaces: ").split()
                try:
                    record.add_tag_to_note_by_title(note_title, tags)
                    return f"Tags added to note '{note_title}' for {name}."
                except ValueError as e:
                    print(str(e))

        elif choice == "6":
            while True:
                birthday = input(f"Enter the birthday (DD.MM.YYYY) for {name}: ")
                try:
                    record.add_birthday(birthday)
                    return f"Birthday {birthday} added for {name}."
                except InvalidBirthdayError as e:
                    print(str(e))

        else:
            return f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}"

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

            telephone = input(
                f"{Fore.CYAN}{name}{Style.RESET_ALL}, please enter your phone: "
            )

            try:
                record.add_phone(telephone)
            except ValueError as e:
                print(Fore.RED + str(e))

            if record.name and record.phones:
                print(f"{Fore.GREEN}{record.name} - {record.phones[0]} ")

    @data_saver
    @print_execution_time
    def run(self):
        init(autoreset=True)
        owner = self.book.get_owner()

        if owner is None:
            self.add_owner()
        else:
            print(
                f"{Fore.MAGENTA}Glad to see you, {owner.name}!{Style.RESET_ALL}",
                end="\n\n",
            )

        Bot.__show_help()
        print(f"Address book has {len(self.book.data)} contact(s).")

        while True:
            user_input = self.session.prompt("Enter a command: ")
            parsed_input = Bot.__parse_input(user_input)

            if not parsed_input:
                print(Fore.RED + "Invalid command format.")
                continue

            command, args = parsed_input

            match command:
                case BotCmd.CLOSE | BotCmd.EXIT:
                    print(
                        f"{Fore.YELLOW}Good bye{' ' + str(owner.name) if owner else ''}!{Style.RESET_ALL}"
                    )

                    break
                case BotCmd.HELLO:
                    print(f"{Fore.GREEN}How can I help you?")
                case BotCmd.CONTACT_ADD:
                    print(f"{Fore.GREEN}{self.add_contact(args)}")
                case BotCmd.CONTACT_SHOW_PHONES:
                    print(f"{Fore.CYAN}{self.show_phone(args)}")
                case BotCmd.CONTACT_SHOW_ALL:
                    print(self.show_all())
                case BotCmd.BIRTHDAY_ADD:
                    self.add_birthday(args)
                case BotCmd.BIRTHDAY_SHOW:
                    print(f"{Fore.CYAN}{self.show_birthday(args)}")
                case BotCmd.BIRTHDAY_SHOW_ALL:
                    print(f"{Fore.MAGENTA}{self.show_birthdays(args)}")
                case BotCmd.HELP:
                    self.__show_help()
                case BotCmd.ADD_EMAIL:
                    print(f"{Fore.GREEN}{self.add_email(args)}")
                case BotCmd.ADD_ADDRESS:
                    print(f"{Fore.GREEN}{self.add_address(args)}")
                case BotCmd.EDIT:
                    print(f"{Fore.MAGENTA}{self.edit_contact_info(args)}")
                case BotCmd.EDIT_CONTACT_PHONE:
                    print(f"{Fore.MAGENTA}{self.edit_contact_phone(args)}")
                case BotCmd.DELETE:
                    print(f"{Fore.MAGENTA}{self.delete_contact_info(args)}")
                case BotCmd.DELETE_CONTACT_PHONE:
                    print(f"{Fore.MAGENTA}{self.delete_contact_phone(args)}")
                case BotCmd.DELETE_CONTACT:
                    print(f"{Fore.MAGENTA}{self.delete_contact(args)}")
                case BotCmd.SEARCH_BY:
                    print(f"{Fore.GREEN}{self.search_by(args)}")
                case BotCmd.ADD_NOTE:
                    print(f"{Fore.GREEN}{self.add_note(args)}")
                case BotCmd.EDIT_NOTE:
                    print(f"{Fore.GREEN}{self.edit_note(args)}")
                case BotCmd.DELETE_NOTE:
                    print(f"{Fore.GREEN}{self.delete_note(args)}")
                case BotCmd.ADD_TAG:
                    print(f"{Fore.GREEN}{self.add_tags(args)}")
                case BotCmd.DELETE_TAG:
                    print(f"{Fore.GREEN}{self.delete_tag(args)}")
                case BotCmd.GET_NOTES_BY_TAG:
                    print(f"{self.get_notes_by_tag(args)}")
                case BotCmd.GET_NOTE_BY_TITLE:
                    print(f"{Fore.GREEN}{self.get_note_by_title(args)}")
                case BotCmd.GET_ALL_NOTES:
                    print(f"{self.get_notes(args)}")
                case BotCmd.ADD_CONTACT_INFO:
                    print(f"{Fore.GREEN}{self.add_contact_info(args)}")
                case BotCmd.GET_INFO:
                    print(f"{Fore.GREEN}{self.get_info(args)}")
                case BotCmd.SEARCH_INFO:
                    print(f"{Fore.GREEN}{self.search_info(args)}")
                case BotCmd.DELETE_INFO:
                    print(f"{Fore.GREEN}{self.delete_info(args)}")
                case BotCmd.SHOW_INFO:
                    print(f"{Fore.GREEN}{self.show_info(args)}")
                case _:
                    print(f"{Fore.RED}Invalid command.")

    @data_saver
    @input_error
    def get_info(self, args):
        """
        This function provides a menu to get different types of contact information.
        Args:
            args: list of command arguments.
        Return:
            str: message indicating the execution result.
        """
        print("Choose the information you want to retrieve:")
        print("1. Get all notes")
        print("2. Get notes by tag")
        print("3. Get note by title")
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            if len(args) == 0:
                name = input("Please enter the name of the contact: ")
            elif len(args) == 1:
                name = args[0]
            else:
                raise ValueError(
                    f"{Fore.RED}Invalid input. Use: get-info [name]{Style.RESET_ALL}"
                )

            return self.get_notes([name])

        elif choice == "2":
            tag = input("Enter the tag to search notes: ")
            return self.get_notes_by_tag([tag])

        elif choice == "3":
            note_title = input("Enter the note title: ")
            return self.get_note_by_title([note_title])

        else:
            return f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}"

    @data_saver
    @input_error
    def search_info(self, args):
        """
        This function provides a menu to search for different types of contact information.
        Args:
            args: list of command arguments.
        Return:
            str: message indicating the execution result.
        """
        print("Choose the information you want to search:")
        print("1. Search by name")
        print("2. Search by phone number")
        print("3. Search by email")
        print("4. Search by address")
        print("5. Search by note content")
        print("6. Search by tag")
        print("7. Search by birthday")
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            if len(args) == 0:
                name = input("Please enter the name of the contact: ")
            elif len(args) == 1:
                name = args[0]
            else:
                raise ValueError(
                    f"{Fore.RED}Invalid input. Use: search-info [name]{Style.RESET_ALL}"
                )

            return self.search_by(["name", name])

        elif choice == "2":
            phone = input("Enter the phone number: ")
            return self.search_by(["phone", phone])

        elif choice == "3":
            email = input("Enter the email address: ")
            return self.search_by(["email", email])

        elif choice == "4":
            address = input("Enter the address: ")
            return self.search_by(["address", address])

        elif choice == "5":
            note_content = input("Enter the note content: ")
            return self.search_by(["note", note_content])

        elif choice == "6":
            tag = input("Enter the tag: ")
            return self.search_by(["tag", tag])

        elif choice == "7":
            birthday = input("Enter the birthday (DD.MM.YYYY): ")
            return self.search_by(["birthday", birthday])

        else:
            return f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}"

    @data_saver
    @input_error
    def delete_info(self, args):
        """
        This function provides a menu to delete different types of contact information.
        Args:
            args: list of command arguments.
        Return:
            str: message indicating the execution result.
        """
        print("Choose the information you want to delete:")
        print("1. Delete contact")
        print("2. Delete phone")
        print("3. Delete email")
        print("4. Delete address")
        print("5. Delete birthday")
        print("6. Delete note by title")
        print("7. Delete tag from note")
        choice = input("Enter the number of your choice: ")

        if len(args) == 0:
            name = input("Please enter the name of the contact: ")
        elif len(args) == 1:
            name = args[0]
        else:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: delete-info [name]{Style.RESET_ALL}"
            )

        record = self.book.find_contact(name)
        if not record and choice != "1":
            raise KeyError(f"{Fore.RED}Contact {name} not found.{Style.RESET_ALL}")

        if choice == "1":
            return self.delete_contact([name])

        elif choice == "2":
            phone = input(f"Enter the phone number to delete for {name}: ")
            return self.delete_contact_phone([name, phone])

        elif choice == "3":
            return self.delete_contact_info([name, "email"])

        elif choice == "4":
            return self.delete_contact_info([name, "address"])

        elif choice == "5":
            return self.delete_contact_info([name, "birthday"])

        elif choice == "6":
            note_title = input(f"Enter the note title to delete for {name}: ")
            return self.delete_note_by_title([note_title])

        elif choice == "7":
            note_title = input(f"Enter the note title to remove tag from for {name}: ")
            tag = input(f"Enter the tag to remove from the note: ")
            return self.delete_tag([tag, note_title])

        else:
            return f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}"

    @data_saver
    @input_error
    def delete_note(self, args):
        """
        This function deletes a note of a contact.
        """
        if len(args) < 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: delete-note [note_title]{Style.RESET_ALL}"
            )
        note_title = " ".join(args)

        self.book.delete_note_by_title(note_title)
        return f"Note {note_title} deleted."

    @data_saver
    @input_error
    def delete_tag(self, args):
        """
        This function deletes a tag from a note.
        """
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: delete-tag [tag] [note_title]{Style.RESET_ALL}"
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
                f"{Fore.RED}Invalid input. Use: get-notes-by-tag [tag]{Style.RESET_ALL}"
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
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: get-note [note_title]{Style.RESET_ALL}"
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
                f"{Fore.RED}Invalid input. Use: get-notes [name]{Style.RESET_ALL}"
            )
        name, *_ = args

        record = self.book.find_contact(name)

        if record:
            return self.build_table_for_notes(record.notes)
        else:
            raise KeyError(f"{Fore.RED}Contact not found. {Style.RESET_ALL}")

    def build_table_for_notes(self, notes):
        table_data = [
            [note.title, ", ".join(str(tag) for tag in note.tags), note.value]
            for note in notes
        ]

        headers = ["Title", "Tags", "Note"]

        return tabulate(table_data, headers, tablefmt="fancy_grid")

    @data_saver
    @input_error
    def delete_contact(self, args):
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
        This function provides a menu to edit different types of contact information.
        Args:
            args: list of command arguments.
        Return:
            str: message indicating the execution result.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: edit-contact-info [name]{Style.RESET_ALL}"
            )

        name = args[0]
        print("Choose the information you want to edit:")
        print("1. Name")
        print("2. Phone")
        print("3. Email")
        print("4. Address")
        print("5. Birthday")
        choice = input("Enter the number of your choice: ")

        record = self.book.find_contact(name)
        if not record:
            raise KeyError(f"{Fore.RED}Contact {name} not found.{Style.RESET_ALL}")

        if choice == "1":
            new_name = input(f"Enter the new name for {name}: ")
            record.edit_name(new_name)
            return f"Name changed to {new_name} for contact {name}."

        elif choice == "2":
            old_phone = input(f"Enter the current phone number for {name}: ")
            new_phone = input(f"Enter the new phone number for {name}: ")
            try:
                record.edit_phone(old_phone, new_phone)
                return f"Phone number updated to {new_phone} for {name}."
            except InvalidPhoneNumberError as e:
                print(str(e))
                return "Phone number not updated."

        elif choice == "3":
            new_email = input(f"Enter the new email address for {name}: ")
            try:
                record.edit_email(new_email)
                return f"Email address updated to {new_email} for {name}."
            except InvalidEmailError as e:
                print(str(e))
                return "Email address not updated."

        elif choice == "4":
            new_address = input(f"Enter the new address for {name}: ")
            record.edit_address(new_address)
            return f"Address updated to {new_address} for {name}."

        elif choice == "5":
            new_birthday = input(f"Enter the new birthday (DD.MM.YYYY) for {name}: ")
            try:
                record.edit_birthday(new_birthday)
                return f"Birthday updated to {new_birthday} for {name}."
            except InvalidBirthdayError as e:
                print(str(e))
                return "Birthday not updated."

        else:
            return f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}"

    @data_saver
    @input_error
    def delete_contact_info(self, args):
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: delete-contact-info [name] [field name]{Style.RESET_ALL}"
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
    def delete_contact_phone(self, args):
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: delete-contact-phone [name] [phone number]{Style.RESET_ALL}"
            )
        name, number, *_ = args
        record = self.book.find_contact(name)
        if record:
            return record.remove_phone(number)
        else:
            return f"Contact with name {name} not found"