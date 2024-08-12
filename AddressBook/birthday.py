from .field import Field
from datetime import datetime
from colorama import Style, init, Fore

init(autoreset=True)


class Birthday(Field):
    """Class for storing a birthday date. It has format validation (DD.MM.YYYY)."""

    def __init__(self, value):
        self.date = self.validate(value)
        super().__init__(self.date)

    @staticmethod
    def validate(value):
        """Check for the correctness of the birthday format."""
        try:
            return datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError(
                f"{Fore.RED}Invalid date format. Use 'DD.MM.YYYY'.{Style.RESET_ALL}"
            )

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
