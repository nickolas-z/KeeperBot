import pickle
from tabulate import tabulate
from colorama import Fore, Style, init
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import PromptSession

from AddressBook import Record, AddressBook, Birthday
from bot_cmd import BotCmd
from helpers import Application, input_error, print_execution_time
from functools import wraps


class Bot(Application):
    """
    Application class
    """
    contacts_info = None

    def __init__(self, app_name, filename="addressbook.pkl"):
        super().__init__(app_name)
        self.filename = filename
        self.book = Bot.__load_data(self.filename)

        self.commands_list = BotCmd.get_all_commands()
        self.command_completer = WordCompleter(
            self.commands_list, ignore_case=True)
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
                f"{Fore.RED}Invalid input. Use: add [name] [phone]{
                    Style.RESET_ALL}"
            )
        name, phone, *_ = args

        # Check if the phone number already exists for another contact
        existing_contact = self.book.find_phone(phone)
        if existing_contact:
            if existing_contact.name.value != name:
                # Ask for confirmation to add the same phone number to the new contact
                message = (f"Phone number {Fore.WHITE}{phone}{Fore.YELLOW} already exists for contact "
                           f"{Fore.WHITE}{existing_contact.name}{Fore.YELLOW}. "
                           f"Add it to {Fore.WHITE}{name}{Fore.YELLOW}?")
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

    @data_saver
    @input_error
    def change_contact(self, args):
        """
        This function changes the phone number of a contact.
        Args:
            args: list of command arguments.
        Return:
            str: message indicating the execution result.
        """
        if len(args) != 3:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: change [name] [old_phone] [new_phone]{
                    Style.RESET_ALL}"
            )

        name, old_phone, new_phone = args
        record = self.book.find_contact(name)

        if record:
            try:
                valid_phone = Phone(new_phone)
                record.edit_phone(old_phone, new_phone)
                return f"Contact {name} updated."
            except ValueError as e: 
                return f"{Fore.RED}Failed to update contact: {str(e)}{Style.RESET_ALL}"
        else:
            raise KeyError(f"{Fore.RED}Contact {
                           name} not found.{Style.RESET_ALL}")

    def show_all(self):
        """This function displays all contacts.
        Return:
            str: list of contacts.
        """
        if not self.book.data:
            print("No contacts found.")

        table_data = [
            [
                record.name,
                ", ".join(str(phone) for phone in record.phones),
                record.email,
                record.birthday,
                record.address,
                ", ".join(note.title for note in record.notes),
                ", ".join(", ".join(str(tag) for tag in note.tags)
                          for note in record.notes),
                "+" if record.owner else "",
            ] for name, record in self.book.data.items()
        ]

        headers = ["Name", "Phone", "Email", "Birthday",
                   "Address", "Notes", "Tag", "Owner"]

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
            if len(phones) == 1:
                return f"{name}: {phones[0]}."
            else:
                return f"{name}: {'; '.join(phones)}."
        else:
            raise KeyError(f"{Fore.RED}Contact {
                           name} not found.{Style.RESET_ALL}")

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
                f"{Fore.RED}Invalid input. Use: add-birthday [name] [birthday]{
                    Style.RESET_ALL}"
            )
        name, birthday = args
        record = self.book.find_contact(name)
        if record:
            record.add_birthday(birthday)
            return f"Birthday for {name} added."
        else:
            raise KeyError(f"{Fore.RED}Contact {
                           name} not found.{Style.RESET_ALL}")

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
                f"{Fore.RED}Invalid input. Use: show-birthday [name]{
                    Style.RESET_ALL}"
            )

        name = args[0]

        record = self.book.find_contact(name)
        if record:
            return f"{name}'s birthday: {record.birthday.value.strftime(Birthday.BIRTHDAY_FORMAT) if record.birthday else 'Not set'}"
        else:
            raise KeyError(f"{Fore.RED}Contact {
                           name} not found.{Style.RESET_ALL}")

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
                f"{Fore.RED}Invalid input. Use: show-birthdays [number of days or empty for today]{
                    Style.RESET_ALL}"
            )

        if not upcoming_birthdays:
            print(f"No upcoming birthdays.")
            return

        table_data = [[record.name, record.birthday]
                      for record in upcoming_birthdays]

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
        print(
            f"{Fore.GREEN}\tadd {Fore.YELLOW}[name] [phone]{Fore.WHITE} "
            f"- add a new contact with a name and phone number, or add a phone number to an existing contact;"
        )
        print(
            f"{Fore.GREEN}\tchange {
                Fore.YELLOW}[name] [old phone] [new phone]{Fore.WHITE} "
            f"- change the phone number for the specified contact;"
        )
        print(f"{Fore.GREEN}\tadd-email {Fore.YELLOW}[name] [email]{Fore.WHITE} "
              f"- add/replace an email for the specified contact;")
        print(f"{Fore.GREEN}\tadd-address {Fore.YELLOW}[name] [address]{Fore.WHITE} "
              f"- add/replace an address for the specified contact;")
        print(f"{Fore.GREEN}\tadd-note {Fore.YELLOW}[author_name]{Fore.WHITE} "
              f"- add note for the specified contact;")
        print(f"{Fore.GREEN}\tedit-note {Fore.YELLOW}[note_title]{Fore.WHITE} "
              f"- edit note by title;")
        print(f"{Fore.GREEN}\tdelete-note {Fore.YELLOW}[note_title]{Fore.WHITE} "
              f"- delete note by title;")
        print(f"{Fore.GREEN}\tadd-tags {Fore.YELLOW}[note_title]{Fore.WHITE} "
              f"- add tags to note;")
        print(f"{Fore.GREEN}\tdelete-tag {Fore.YELLOW}[tag] [note_title]{Fore.WHITE} "
              f"- delete specified tag for specified note;")
        print(f"{Fore.GREEN}\tget-notes-by-tag {Fore.YELLOW}[tag]{Fore.WHITE} "
              f"- finds all notes with specified tag;")
        print(f"{Fore.GREEN}\tget-note {Fore.YELLOW}[note_title]{Fore.WHITE} "
              f"- finds note with specified title;")
        print(f"{Fore.GREEN}\tget-notes {Fore.YELLOW}[name]{Fore.WHITE} "
              f"- returns all notes for specified contact;")

        print(
            f"{Fore.GREEN}\tphone {Fore.YELLOW}[name]{
                Fore.WHITE} - show phone numbers for the specified contact;"
        )
        print(f"{Fore.GREEN}\tall{
              Fore.WHITE} - show all contacts in the address book;")
        print(
            f"{Fore.GREEN}\tadd-birthday {
                Fore.YELLOW}[name] [birthday] {Fore.WHITE}"
            f"- add a birthday (DD.MM.YYYY) for the specified contact;"
        )
        print(
            f"{Fore.GREEN}\tshow-birthday {Fore.YELLOW}[name] {Fore.WHITE}"
            f"- show the birthday for the specified contact;"
        )
        print(
            f"{Fore.GREEN}\tshow-birthdays{Fore.YELLOW} [days] {
                Fore.WHITE} - show birthdays that will occur within the next number of days, empty for today;"
        )
        print(
            f"{Fore.GREEN}\tedit-contact-info {Fore.YELLOW}[name] [available field name. List of examples: [name, birthday, email, address]] [new value] {
                Fore.WHITE}- update contact info;"
        )
        print(
            f"{Fore.GREEN}\tedit-contact-phone {Fore.YELLOW}[name] [old phone] [new phone] {
                Fore.WHITE}- update contact phone;"
        )
        print(
            f"{Fore.GREEN}\tdelete-contact-phone {Fore.YELLOW}[name] [phone number] {
                Fore.WHITE}- delete contact phone;"
        )
        print(
            f"{Fore.GREEN}\tdelete-contact-info {
                Fore.YELLOW}[name] [available field name. List of examples: [birthday, email, address]] {Fore.WHITE}- delete contact info;"
        )
        print(
            f"{Fore.GREEN}\tdelete-contact {Fore.YELLOW}[name] {Fore.WHITE}- delete contact;")
        print(f"{Fore.GREEN}\thello {Fore.WHITE}- get a greeting from the bot;")
        print(
            f"{Fore.GREEN}\tsearch-by {Fore.YELLOW}{Fore.WHITE} "
            f"- find contants by specified field and value;"
        )
        print(
            f"{Fore.GREEN}\tclose {Fore.WHITE}or {
                Fore.GREEN}exit {Fore.WHITE}- close the program."
        )

    @data_saver
    @input_error
    def add_owner(self):
        print("Let's start by recording your personal details.", end="\n\n")

        res = input(f"Record your data: {Fore.GREEN}Yes{
                    Style.RESET_ALL}/{Fore.RED}No{Style.RESET_ALL} ")

        if res.lower() == "Yes".lower():
            name = input("Your name: ")

            record = Record(name)
            record.check_owner()

            self.book.add_record(record)

            telephone = input(f"{Fore.CYAN}{name}{
                              Style.RESET_ALL}, please enter your phone: ")

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
            print(f"{Fore.MAGENTA}Glad to see you, {
                  owner.name}!{Style.RESET_ALL}", end="\n\n")

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
                    print(f"{Fore.YELLOW}Good bye{' ' + str(owner.name)
                          if owner else ''}!{Style.RESET_ALL}")

                    break
                case BotCmd.HELLO:
                    print(f"{Fore.GREEN}How can I help you?")
                case BotCmd.CONTACT_ADD:
                    print(f"{Fore.GREEN}{self.add_contact(args)}")
                case BotCmd.CONTACT_CHANGE:
                    print(f"{Fore.YELLOW}{self.change_contact(args)}")
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
                case _:
                    print(f"{Fore.RED}Invalid command.")

    @data_saver
    @input_error
    def add_email(self, args):
        if len(args) != 2:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: add-email [name] [email]{
                    Style.RESET_ALL}"
            )
        name, email = args

        record = self.book.find_contact(name)
        if record:
            record.add_email(email)
            return f"Email for {name} added."
        else:
            raise KeyError(f"{Fore.RED}Contact {
                           name} not found. Please create contact first. {Style.RESET_ALL}")

    @data_saver
    @input_error
    def add_address(self, args):
        if len(args) != 2:
            raise ValueError(f"{Fore.RED}Invalid input. Use: add-address [name] [address]{Style.RESET_ALL}"
                             )
        name, address = args

        record = self.book.find_contact(name)
        if record:
            record.add_address(address)
            return f"Address for {name} added."
        else:
            raise KeyError(f"{Fore.RED}Contact {
                           name} not found. Please create contact first. {Style.RESET_ALL}")

    @input_error
    def search_by(self, args=None):
        """
        This function interacts with the user to gather search criteria,
        and then performs the search based on the provided criteria.
        """

        # If args are not provided, interactively gather them
        if args is None or len(args) != 2:
            print("Choose a search criterion:")
            print("1. Search by name")
            print("2. Search by phone number")
            print("3. Search by email")
            print("4. Search by address")
            print("5. Search by note")
            print("6. Search by tag")
            print("7. Search by birthday")
            print("8. Search by all criteria")
            criterion_choice = input("Enter the criterion number: ")

            if criterion_choice == "1":
                field = "name"
                value = input("Enter the name to search: ")
            elif criterion_choice == "2":
                field = "phone"
                value = input("Enter the phone number to search: ")
            elif criterion_choice == "3":
                field = "email"
                value = input("Enter the email to search: ")
            elif criterion_choice == "4":
                field = "address"
                value = input("Enter the address to search: ")
            elif criterion_choice == "5":
                field = "note"
                value = input("Enter the note text to search: ")
            elif criterion_choice == "6":
                field = "tag"
                value = input("Enter the tag to search: ")
            elif criterion_choice == "7":
                field = "birthday"
                value = input("Enter the birthday (DD.MM.YYYY) to search: ")
            elif criterion_choice == "8":
                field = "all"
                value = input(
                    "Enter the keyword to search across all criteria: ")
            else:
                print(f"{Fore.RED}Invalid criterion. Please try again.{
                      Style.RESET_ALL}")
                return

            args = [field, value]

        # Proceed with the search using the provided or collected args
        if len(args) != 2:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: search-by [field] [value]{
                    Style.RESET_ALL}"
            )

        field, value = args

        # Assuming AddressBook has a method find_contacts_by_field
        records = self.book.find_contacts_by_field(field, value)

        if records:
            result = ""
            for record in records:
                result += f"\n{str(record)}"
            return result.strip()
        else:
            raise KeyError(f"{Fore.RED}No contacts found for the specified {
                           field}.{Style.RESET_ALL}")

    @data_saver
    @input_error
    def add_note(self, args):
        """
        This function adds a note to a contact.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: add-note [author_name] [note_title]{
                    Style.RESET_ALL}"
            )
        author_name, *_ = args

        record = self.book.find_contact(author_name)
        if record:
            title = input("Enter note title [enter to exit]: ")
            if not title:
                return None

            note = input("Enter note content: \n")
            record.add_note(title, note)

            return f"Note for {author_name} added."
        else:
            raise KeyError(f"{Fore.RED}Contact {
                           author_name} not found. Please create contact first. {Style.RESET_ALL}")

    @data_saver
    @input_error
    def edit_note(self, args):
        """
        This function edits a note of a contact.
        """
        if len(args) < 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: edit-note [note_title]{
                    Style.RESET_ALL}"
            )
        note_title = " ".join(args)

        note = self.book.find_note_by_title(note_title)
        if note:
            new_note = input("Enter new note content: \n")
            note.value = new_note
            return f"Note {note_title} edited."
        else:
            raise KeyError(f"{Fore.RED}Note {
                           note_title} not found. {Style.RESET_ALL}")

    @data_saver
    @input_error
    def delete_note(self, args):
        """
        This function deletes a note of a contact.
        """
        if len(args) < 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: delete-note [note_title]{
                    Style.RESET_ALL}"
            )
        note_title = ' '.join(args)

        self.book.delete_note_by_title(note_title)
        return f"Note {note_title} deleted."

    @data_saver
    @input_error
    def add_tags(self, args):
        """
        This function adds tags to a note.
        """
        if len(args) < 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: add-tags [note_title]{
                    Style.RESET_ALL}"
            )
        note_title = " ".join(args)

        note = self.book.find_note_by_title(note_title)
        if note:
            tags = input("Enter tags separated by space: ").split()
            note.tags = note.tags + tags
            return f"Tags added to {note_title}."
        else:

            raise KeyError(f"{Fore.RED}Note {
                           note_title} not found. {Style.RESET_ALL}")

    @data_saver
    @input_error
    def delete_tag(self, args):
        """
        This function deletes a tag from a note.
        """
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: delete-tag [tag] [note_title]{
                    Style.RESET_ALL}"
            )
        tag, *note_title = args
        note_title = " ".join(note_title)

        note = self.book.find_note_by_title(note_title)
        if note:
            note.tags = [t for t in note.tags if t != tag]
            return f"Tag {tag} deleted from {note_title}."
        else:
            raise KeyError(f"{Fore.RED}Note {
                           note_title} not found. {Style.RESET_ALL}")

    @input_error
    def get_notes_by_tag(self, args):
        """
        This function finds all notes with specified tag.
        """

        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: get-notes-by-tag [tag]{
                    Style.RESET_ALL}"
            )
        tag, *_ = args

        notes = self.book.find_notes_by_tag(tag)
        if notes:
            result = ""
            for note in notes:
                result += f"\n{str(note)}"
            return result.strip()
        else:
            raise KeyError(f"{Fore.RED}Notes not found. {Style.RESET_ALL}")

    @input_error
    def get_note_by_title(self, args):
        """
        This function finds note by title.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: get-note [note_title]{
                    Style.RESET_ALL}"
            )
        note_title = " ".join(args)

        note = self.book.find_note_by_title(note_title)
        if note:
            return str(note)
        else:
            raise KeyError(f"{Fore.RED}Note {
                           note_title} not found. {Style.RESET_ALL}")

    @input_error
    def get_notes(self, args):
        """
        This function finds all notes for specified contact.
        """
        if len(args) != 1:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: get-notes [name]{
                    Style.RESET_ALL}"
            )
        name, *_ = args

        record = self.book.find_contact(name)

        if record:
            return self.build_table_for_notes(record)
        else:
            raise KeyError(f"{Fore.RED}Contact not found. {Style.RESET_ALL}")

    def build_table_for_notes(self, record):
        table_data = [
            [
                note.title,
                ", ".join(str(tag) for tag in note.tags),
                note.value
            ] for note in record.notes
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
            return f'Contact with name {name} not found'

    @data_saver
    @input_error
    def edit_contact_info(self, args):
        if len(args) < 3:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: edit-contact-info [name] [field name] [new value]{
                    Style.RESET_ALL}"
            )
        name, field, new_value, *_ = args
        record = self.book.find_contact(name)
        method = field.lower()
        if record:
            return getattr(record, f"edit_{method}")(new_value)
        else:
            return f'Contact with name {name} not found'

    @data_saver
    @input_error
    def delete_contact_info(self, args):
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: delete-contact-info [name] [field name]{
                    Style.RESET_ALL}"
            )
        name, field, *_ = args
        record = self.book.find_contact(name)
        method = field.lower()
        if record:
            return getattr(record, f"delete_{method}")()
        else:
            return f'Contact with name {name} not found'

    @data_saver
    @input_error
    def edit_contact_phone(self, args):
        if len(args) < 3:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: edit-contact-phone [name] [old phone] [new phone]{
                    Style.RESET_ALL}"
            )
        name, old_number, new_number, *_ = args
        record = self.book.find_contact(name)
        if record:
            return record.edit_phone(old_number, new_number)
        else:
            return f'Contact with name {name} not found'

    @data_saver
    @input_error
    def delete_contact_phone(self, args):
        if len(args) < 2:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: delete-contact-phone [name] [phone number]{
                    Style.RESET_ALL}"
            )
        name, number, *_ = args
        record = self.book.find_contact(name)
        if record:
            return record.remove_phone(number)
        else:
            return f'Contact with name {name} not found'
