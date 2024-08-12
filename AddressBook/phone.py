from .field import Field
import re
from colorama import Fore, Style


class Phone(Field):
    """Class for storing phone numbers. Has format validation (10 digits)."""

    def __init__(self, value: str) -> None:
        """
        Initialize a Phone object.

        Args:
            value (str): The phone number value.

        Raises:
            ValueError: If the phone number is not a 10-digit number.

        """
        if not self.is_valid(value):
            raise ValueError(
                f"{Fore.RED}Phone number must be a 10-digit number.{Style.RESET_ALL}"
            )
        super().__init__(value)

    @staticmethod
    def is_valid(value: str) -> bool:
        """
        Check if the phone number format is valid.

        Args:
            value (str): The phone number value.

        Returns:
            bool: True if the phone number is valid, False otherwise.

        """
        return (
            value is not None
            and value.strip() != ""
            and value.isdigit()
            and len(value) == 10
        )

    def normalize_phone(self, phone_number: str) -> str:
        """
        Normalize and return a cleaned phone number.

        Args:
            phone_number (str): The string that contains the phone number.

        Returns:
            str: The standardized phone number.

        """
        # Remove all characters except '+' at the beginning and digits
        cleaned_number = re.sub(r"(?!^\+)[\D]", "", phone_number)
        length_number = len(cleaned_number)

        # Check if the number starts with '+'
        if cleaned_number.startswith("+"):
            # If yes, leave it as it is
            return cleaned_number
        elif length_number == 9:  # format: 9 digits (e.g., 679910599)
            return "+380" + cleaned_number
        elif length_number == 10:  # format: 10 digits (e.g., 0679910599)
            return "+38" + cleaned_number
        elif length_number == 11 and cleaned_number.startswith(
            "80"
        ):  # format: 80xxxxxxxxx
            return "+3" + cleaned_number
        elif length_number == 12 and cleaned_number.startswith(
            "380"
        ):  # format: 380xxxxxxxxx
            return "+" + cleaned_number
        elif length_number == 12 and not cleaned_number.startswith(
            "380"
        ):  # other 12-digit numbers
            return "+" + cleaned_number
        else:  # all other cases
            return "+38" + cleaned_number

    def __repr__(self) -> str:
        """
        Return a string representation of the Phone object.

        Returns:
            str: The string representation of the Phone object.

        """
        return f"{self.__class__.__name__}(value='{self.value}')"


if __name__ == "__main__":
    field = Phone("example value")
    print(field.__doc__)
    for name, func in field.__class__.__dict__.items():
        if callable(func):
            print(f"{Fore.RED}{name}{Style.RESET_ALL}")
            print(f"{Fore.RED}{func.__doc__}{Style.RESET_ALL}")
