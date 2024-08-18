from colorama import Fore, Style
from .field import Field


class Tag(Field):
    """Class for storing contact names. Mandatory field."""

    def __init__(self, value: str) -> None:
        """Initialize the tag field with a value.

        Args:
            value (str): The value of the Tag field.

        Raises:
            ValueError: If the value is empty.
        """
        if not value:
            raise ValueError(f"{Fore.RED}Name field cannot be empty.{Style.RESET_ALL}")
        
        super().__init__(value)
        
    def __str__(self) -> str:
        """Return a string representation of the Name field.

        Returns:
            str: The string representation of the Name field.
        """
        return str(self.value)

    def __repr__(self) -> str:
        """Return a string representation of the Name field.

        Returns:
            str: The string representation of the Name field.
        """
        return f"{self.__class__.__name__}(value='{self.value}')"


if __name__ == "__main__":
    field = Tag("example tag")
    print(field.__doc__)
    for name, func in field.__class__.__dict__.items():
        if callable(func):
            print(name)
            print(func.__doc__)
