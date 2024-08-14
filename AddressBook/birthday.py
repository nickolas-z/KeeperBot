from .field import Field
from datetime import datetime
from colorama import Style, init, Fore

init(autoreset=True)


class Birthday(Field):
    """Class for storing a birthday date. It has format validation (DD.MM.YYYY)."""

    BIRTHDAY_FORMAT = "%d.%m.%Y"

    def __init__(self, value):
        self.date = self.validate(value)
        super().__init__(self.date)

    @staticmethod
    def validate(value):
        """
        Check for the correctness of the birthday format.
        The age of the contact should not exceed 100 years.
        """
        try:
            date = datetime.strptime(value, Birthday.BIRTHDAY_FORMAT)
        except ValueError:
            raise ValueError(
                f"{Fore.RED}Invalid date format. Use 'DD.MM.YYYY'.{Style.RESET_ALL}"
            )

        current_date = datetime.now()
        min_date = current_date.replace(year=current_date.year - 100)
        max_date = current_date

        if date < min_date or date > max_date:
            raise ValueError(
                f"{Fore.RED}Invalid date. Date must be between {min_date.strftime(Birthday.BIRTHDAY_FORMAT)} and {max_date.strftime(Birthday.BIRTHDAY_FORMAT)}.{Style.RESET_ALL}"
            )
        return date

    def __repr__(self) -> str:
        """
        Return a string representation of the Phone object.

        Returns:
            str: The string representation of the Phone object.

        """
        return f"{self.__class__.__name__}(value='{self.value}')"


if __name__ == "__main__":
    field = Birthday("example value")
    print(field.__doc__)
    for name, func in field.__class__.__dict__.items():
        if callable(func):
            print(name)
            print(func.__doc__)
