from .field import Field
import re
from colorama import Fore, Style


class Phone(Field):
    """Class for storing phone numbers. Validates international Phone numbers."""

    def __init__(self, value: str) -> None:
        """
        Initialize a Phone object.

        Args:
            value (str): The phone number value.

        Raises:
            ValueError: If the phone number does not follow the international format.
        """
        normalized_value = self.normalize_phone(value)
        if not self.is_valid(normalized_value):
            raise ValueError(
                f"{Fore.RED}The phone number must be in international format and begin with '+' followed by 12 to 15 digits.{Style.RESET_ALL}"
            )
        super().__init__(normalized_value)

    @staticmethod
    def is_valid(value: str) -> bool:
        """
        Check if the phone number format is valid.

        Args:
            value (str): The phone number value.

        Returns:
            bool: True if the phone number is valid, False otherwise.
        """
        pattern = r"^\+\d{12,15}$"
        return re.match(pattern, value) is not None

    @staticmethod
    def normalize_phone(phone_number: str) -> str:
        """
        Normalize and return a cleaned phone number.

        Args:
            phone_number (str): The string that contains the phone number.

        Returns:
            str: The standardized phone number.

        """
        # Remove all characters except '+' at the beginning and digits
        cleaned_number = re.sub(r"(?!^\+)[\D]", "", phone_number)

        # Check if the number starts with '+'
        if cleaned_number.startswith("+"):
            # If yes, leave it as it is
            return cleaned_number

        # If the number does not start with '+', add it manually
        if len(cleaned_number) >= 12:  # minimum length of international number
            return "+" + cleaned_number
        else:
            raise ValueError(
                f"{Fore.RED}The phone number must be in international format and begin with '+' followed by 12 to 15 digits.{Style.RESET_ALL}"
            )

    def __repr__(self) -> str:
        """
        Return a string representation of the Phone object.

        Returns:
            str: The string representation of the Phone object.
        """
        return f"{self.__class__.__name__}(value='{self.value}')"


if __name__ == "__main__":
    try:
        field = Phone("+123456789012")
        print(field.__doc__)
        for name, func in field.__class__.__dict__.items():
            if callable(func):
                print(f"{Fore.RED}{name}{Style.RESET_ALL}")
                print(f"{Fore.RED}{func.__doc__}{Style.RESET_ALL}")
    except ValueError as e:
        print(e)
