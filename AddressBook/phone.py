from .field import Field
import re
from colorama import Fore, Style


class Phone(Field):
"""Class for storing telephone numbers. Validates international telephone numbers."""

    def __init__(self, value: str) -> None:

        normalized_value = self.normalize_phone(value)
        if not self.is_valid(normalized_value):
            raise ValueError(
                f"{Fore.RED}The phone number must be in international format and begin with '+' followed by 10 to 15 digits.{
                    Style.RESET_ALL}"
            )
        super().__init__(normalized_value)

    @staticmethod
    def is_valid(value: str) -> bool:

        pattern = r"^\+\d{10,15}$"
        return re.match(pattern, value) is not None

    @staticmethod
    def normalize_phone(phone_number: str) -> str:

        cleaned_number = re.sub(r"(?!^\+)[\D]", "", phone_number)
        length_number = len(cleaned_number)

        if cleaned_number.startswith("+"):
            return cleaned_number
        elif length_number == 9:
            return "+380" + cleaned_number
        elif length_number == 10:
            return "+38" + cleaned_number
        elif length_number == 11 and cleaned_number.startswith(
            "80"
        ):
            return "+3" + cleaned_number
        elif length_number == 12 and cleaned_number.startswith(
            "380"
        ):
            return "+" + cleaned_number
        elif length_number == 12 and not cleaned_number.startswith(
            "380"
        ):
            return "+" + cleaned_number
        else:
            return "+38" + cleaned_number

    def __repr__(self) -> str:

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
