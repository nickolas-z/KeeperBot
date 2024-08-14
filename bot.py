import pickle

from colorama import Fore, Style, init

from AddressBook import Record, AddressBook
from cmd import Cmd
from helpers import Application, input_error, print_execution_time


class Bot(Application):
    """
    Application class
    """

    def __init__(self, app_name, filename="addressbook.pkl"):
        super().__init__(app_name)
        self.filename = filename
        self.book = Bot.__load_data(self.filename)

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
            return Cmd(cmd), args
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
                f"{Fore.RED}Invalid input. Use: add [name] [phone]{Style.RESET_ALL}"
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
                f"{Fore.RED}Invalid input. Use: change [name] [old_phone] [new_phone]{Style.RESET_ALL}"
            )
        name, old_phone, new_phone = args
        record = self.book.find_contact(name)
        if record:
            record.edit_phone(old_phone, new_phone)
            return f"Contact {name} updated."
        else:
            raise KeyError(f"{Fore.RED}Contact {name} not found.{Style.RESET_ALL}")

    def show_all(self):
        """This function displays all contacts.
        Return:
            str: list of contacts.
        """
        if not self.book.data:
            return "No contacts found."

        result = ""
        for name, record in self.book.data.items():
            result += f"\n{str(record)}"
        return result.strip()

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
            raise KeyError(f"{Fore.RED}Contact {name} not found.{Style.RESET_ALL}")

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
                f"{Fore.RED}Invalid input. Use: add-birthday [name] [birthday]{Style.RESET_ALL}"
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
                f"{Fore.RED}Invalid input. Use: show-birthday [name]{Style.RESET_ALL}"
            )
        name = args[0]
        record = self.book.find_contact(name)
        if record:
            return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y') if record.birthday else 'Not set'}"
        else:
            raise KeyError(f"{Fore.RED}Contact {name} not found.{Style.RESET_ALL}")

    def birthdays(self):
        """
        This function displays birthdays that will occur within the next week.
        Return:
            str: list of birthdays.
        """
        upcoming_birthdays = self.book.get_upcoming_birthdays()
        if not upcoming_birthdays:
            return "No upcoming birthdays."
        result = "Upcoming birthdays:\n"
        for entry in upcoming_birthdays:
            result += f"{entry['name']}: {entry['congratulation_date']}\n"
        return result.strip()

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
            f"{Fore.GREEN}\tchange {Fore.YELLOW}[name] [old phone] [new phone]{Fore.WHITE} "
            f"- change the phone number for the specified contact;"
        )
        print(f"{Fore.GREEN}\tadd-email {Fore.YELLOW}[name] [email]{Fore.WHITE} "
              f"- add/replace an email for the specified contact;")
        print(f"{Fore.GREEN}\tadd-address {Fore.YELLOW}[name] [address]{Fore.WHITE} "
              f"- add/replace an address for the specified contact;")
        print(
            f"{Fore.GREEN}\tphone {Fore.YELLOW}[name]{Fore.WHITE} - show phone numbers for the specified contact;"
        )
        print(f"{Fore.GREEN}\tall{Fore.WHITE} - show all contacts in the address book;")
        print(
            f"{Fore.GREEN}\tadd-birthday {Fore.YELLOW}[name] [birthday] {Fore.WHITE}"
            f"- add a birthday (DD.MM.YYYY) for the specified contact;"
        )
        print(
            f"{Fore.GREEN}\tshow-birthday {Fore.YELLOW}[name] {Fore.WHITE}"
            f"- show the birthday for the specified contact;"
        )
        print(
            f"{Fore.GREEN}\tbirthdays{Fore.WHITE} - show birthdays that will occur within the next week;"
        )
        print(f"{Fore.GREEN}\thello {Fore.WHITE}- get a greeting from the bot;")
        print(
            f"{Fore.GREEN}\tclose {Fore.WHITE}or {Fore.GREEN}exit {Fore.WHITE}- close the program."
        )

    @print_execution_time
    def run(self):
        init(autoreset=True)
        Bot.__show_help()
        print(f"Address book has {len(self.book.data)} contact(s).")

        while True:
            user_input = input("Enter a command: ")
            parsed_input = Bot.__parse_input(user_input)

            if not parsed_input:
                print(Fore.RED + "Invalid command format.")
                continue

            command, args = parsed_input

            match command:
                case Cmd.CLOSE | Cmd.EXIT:
                    print(f"{Fore.YELLOW}Good bye!")
                    break
                case Cmd.HELLO:
                    print(f"{Fore.GREEN}How can I help you?")
                case Cmd.CONTACT_ADD:
                    print(f"{Fore.GREEN}{self.add_contact(args)}")
                case Cmd.CONTACT_CHANGE:
                    print(f"{Fore.YELLOW}{self.change_contact(args)}")
                case Cmd.CONTACT_SHOW_PHONES:
                    print(f"{Fore.CYAN}{self.show_phone(args)}")
                case Cmd.CONTACT_SHOW_ALL:
                    print(f"{Fore.MAGENTA}{self.show_all()}")
                case Cmd.BIRTHDAY_ADD:
                    print(f"{Fore.GREEN}{self.add_birthday(args)}")
                case Cmd.BIRTHDAY_SHOW:
                    print(f"{Fore.CYAN}{self.show_birthday(args)}")
                case Cmd.BIRTHDAY_SHOW_ALL:
                    print(f"{Fore.MAGENTA}{self.birthdays()}")
                case Cmd.HELP:
                    self.__show_help()
                case Cmd.ADD_EMAIL:
                    print(f"{Fore.GREEN}{self.add_email(args)}")
                case _:
                    print(f"{Fore.RED}Invalid command.")

            Bot.__save_data(self.book)

    @input_error
    def add_email(self, args):
        if len(args) != 2:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: add-email [name] [email]{Style.RESET_ALL}"
            )
        name, email = args

        record = self.book.find_contact(name)
        if record:
            record.add_email(email)
            return f"Email for {name} added."
        else:
            raise KeyError(f"{Fore.RED}Contact {name} not found. Please create contact first. {Style.RESET_ALL}")

    @input_error
    def add_address(self, args):
        if len(args) != 2:
            raise ValueError(
                f"{Fore.RED}Invalid input. Use: add-address [name] [address]{Style.RESET_ALL}"
            )
        name, address = args

        record = self.book.find_contact(name)
        if record:
            record.add_address(address)
            return f"Address for {name} added."
        else:
            raise KeyError(f"{Fore.RED}Contact {name} not found. Please create contact first. {Style.RESET_ALL}")
