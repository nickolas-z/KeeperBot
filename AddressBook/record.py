from typing import Union

from .address import Address
from .email import Email
from .name import Name
from .phone import Phone
from .birthday import Birthday
from colorama import Fore, Style


class Record:
    """Class for storing contact information, including name and phone number list."""

    def __init__(self, user_name: str) -> None:
        """
        Initialize a new Record object.

        Args:
            user_name (str): The name of the contact.

        """
        self.name = Name(user_name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone_number: str) -> None:
        """
        Add a new phone number to the record.

        Args:
            phone_number (str): The phone number to add.

        """
        phone = Phone(phone_number)
        if self.find_phone(phone_number) is not None:
            raise ValueError(f"{Fore.RED}Phone number already exists.{Style.RESET_ALL}")
        self.phones.append(phone)

    def remove_phone(self, phone_number: str) -> None:
        """
        Remove a phone number from the record.

        Args:
            phone_number (str): The phone number to remove.

        """
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_number, new_number: str) -> None:
        """
        Edit a phone number in the record.

        Args:
            old_number (str): The old phone number to replace.
            new_number (str): The new phone number to add.

        """
        self.remove_phone(old_number)
        self.add_phone(new_number)

    def find_phone(self, phone_number: str) -> Union[Phone, None]:
        """
        Find a phone number in the record.

        Args:
            phone_number (str): The phone number to find.

        Returns:
            Phone: The Phone object if found, None otherwise.

        """
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def sort_phones(self) -> None:
        """Sort the phone numbers in the record."""
        self.phones.sort(key=lambda phone: phone.value, reverse=False)

    def add_birthday(self, birthday: str) -> None:
        """
        Add a birthday to the record.

        Args:
            birthday (str): The birthday to add.

        """
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        """ 
        Add an email to the record.
        Args:
            email (str): The email to add.
        """
        self.email = Email(email)

    def __str__(self) -> str:
        """
        Return a string representation of the Record object.

        Returns:
            str: The string representation of the Record object.

        """
        result = [f"Contact name: {self.name.value}"]
        phones_str = "; ".join(p.value for p in self.phones)
        if phones_str:
            result.append(f"Phones: {phones_str}")
        if self.email:
            result.append(f"Email: {self.email.value}")
        if self.birthday:
            result.append(f"Birthday: {self.birthday.value.strftime('%d.%m.%Y')}")
        if self.address:
            result.append(f"Address: {self.address}")

        return "; ".join(result)

    def __repr__(self) -> str:
        """
        Return a string representation of the Record object.

        Returns:
            str: The string representation of the Record object.

        """
        return f"{self.__class__.__name__}(value='{self.name.value}')"

    def __setstate__(self, state):
        self.name = state.get("name", None)
        self.phones = state.get("phones", [])
        self.birthday = state.get("birthday", None)
        self.email = state.get('email', None)
        self.address = state.get('address', None)

    def add_address(self, address):
        """
        Add an address to the record.
        Args:
            address (str): The address to add.
        """
        self.address = Address(address)


if __name__ == "__main__":
    field = Record("example value")
    print(field.__doc__)
    for name, func in field.__class__.__dict__.items():
        if callable(func):
            print(Fore.RED + name)
            print(Fore.RED + func.__doc__)
            print(Style.RESET_ALL)
