from typing import Union
from .name import Name
from .phone import Phone
from .birthday import Birthday
from colorama import Fore, Style


class Record:
    """Class for storing contact information, including name and phone number list."""

    def __init__(self, name: str) -> None:
        """
        Initialize a new Record object.

        Args:
            name (str): The name of the contact.

        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None

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

    def __str__(self) -> str:
        """
        Return a string representation of the Record object.

        Returns:
            str: The string representation of the Record object.

        """
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}."

    def __repr__(self) -> str:
        """
        Return a string representation of the Record object.

        Returns:
            str: The string representation of the Record object.

        """
        return f"{self.__class__.__name__}(value='{self.value}')"


if __name__ == "__main__":
    field = Record("example value")
    print(field.__doc__)
    for name, func in field.__class__.__dict__.items():
        if callable(func):
            print(Fore.RED + name)
            print(Fore.RED + func.__doc__)
            print(Style.RESET_ALL)
