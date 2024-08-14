import re

from colorama import Fore, Style
from .addressbook_errors import InvalidEmailError
from .field import Field


class Email(Field):
    """Class for storing email address."""

    def __init__(self, value: str) -> None:
        """Initialize the Email field with a value.

        Args:
            value (str): The value of the Email field.

        Raises:
            ValueError: If the value is empty or invalid.
        """
        Email.__validate_email(value)

        super().__init__(value)

    def __repr__(self) -> str:
        """Return a string representation of the Email field.

        Returns:
            str: The string representation of the Email field.
        """
        return f"{self.__class__.__name__}(value='{self.value}')"
    
    def __str__(self) -> str:
        """Return a string representation of the Email field.

        Returns:
            str: The string representation of the Email field.
        """
        return str(self.value)

    @staticmethod
    def __validate_email(email: str) -> None:
        """Check if the email address format is valid.

        Args:
            email (str): The email address value.

        Returns:
            none: If the email address is valid, raise an error otherwise.

        Raises:
            InvalidEmailError: If the email address is invalid.
        """
        if not email:
            raise InvalidEmailError(f"{Fore.RED}Email field cannot be empty.{Style.RESET_ALL}")
        if not isinstance(email, str):
            raise InvalidEmailError(f"{Fore.RED}Email field must be a string.{Style.RESET_ALL}")

        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if re.match(email_pattern, email) is None:
            raise InvalidEmailError(f"{Fore.RED}Invalid email address.{Style.RESET_ALL}")

