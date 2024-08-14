from collections import UserDict
from datetime import datetime, date, timedelta
from .record import Record
from .birthday import Birthday
from typing import Union
from colorama import Fore, Style, init

init(autoreset=True)


class AddressBook(UserDict):
    """Class for storing and managing contact records."""

    def add_record(self, record: Record) -> None:
        """Add a record to the address book.

        Args:
            record (Record): The record to be added.

        Raises:
            ValueError: If the record is invalid.
        """
        if not isinstance(record, Record) or not record.name.value:
            raise ValueError(f"{Fore.RED}Invalid record.{Style.RESET_ALL}")
        self.data[record.name.value] = record

    def find_phone(self, phone: str) -> Union[Record, None]:
        """Find a contact by phone number.

        Args:
            phone (str): The phone number to search for.

        Returns:
            Union[str, None]: The record of the first found contact, or None if not found.
        """
        # TODO: Refactor this method to return a list of records with the same phone number.
        for record in self.data.values():
            for number in record.phones:
                if phone == number.value:
                    return record
        return None

    def find_contact(self, name: str) -> Union[Record, None]:
        """Find a record by name.

        Args:
            name (str): The name to search for.

        Returns:
            Union[Record, None]: The found record, or None if not found.
        """
        return self.data.get(name, None)

    def delete(self, name: str) -> None:
        """Delete a record by name.

        Args:
            name (str): The name of the record to delete.

        Raises:
            ValueError: If the record is not found or the name is invalid.
        """
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(
                f"{Fore.RED}Record not found or invalid name.{Style.RESET_ALL}"
            )

    def get_upcoming_birthdays(self):
        """Function returns a list of dictionaries with users and their birthdays.
        Args:
            _text: a list of dictionaries with users and their birthdays.
        Return:
            upcoming_birthdays: a list of dictionaries with users and their birthdays,
                who celebrate their birthday this week.
        """
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.date.date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days

                if 0 <= delta_days <= 7:
                    congratulation_date = birthday_this_year

                    if congratulation_date.weekday() >= 5:  # 5 - Saturday, 6 - Sunday
                        congratulation_date += timedelta(
                            days=(7 - congratulation_date.weekday())
                        )

                    upcoming_birthdays.append(
                        {
                            "name": record.name.value,
                            "congratulation_date": congratulation_date.strftime(
                                Birthday.BIRTHDAY_FORMAT
                            ),
                        }
                    )

        return upcoming_birthdays

    def sort_records(self) -> None:
        """Sort the records in the address book by name."""
        sorted_records = sorted(
            self.data.values(), key=lambda record: record.name.value
        )
        self.data = {record.name.value: record for record in sorted_records}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value='{self.value}')"


if __name__ == "__main__":
    field = AddressBook("example value")
    print(field.__doc__)
    for name, func in field.__class__.__dict__.items():
        if callable(func):
            print(name)
            print(func.__doc__)
