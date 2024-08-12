from colorama import Fore, Style
from colorama import init


class Field:
    """Base class for record fields."""

    def __init__(self, value: str) -> None:
        """Initialize the Field object with a value."""
        self.value = value

    def __str__(self) -> str:
        """Return a string representation of the Field object."""
        return str(self.value)

    def __repr__(self) -> str:
        """Return a string representation that can be used to recreate the Field object."""
        return f"{self.__class__.__name__}(value='{self.value}')"

    def get_value(self) -> str:
        """Return the value of the Field object."""
        return self.value

    def set_value(self, value: str) -> None:
        """Set the value of the Field object."""
        self.value = value

    def reset_value(self) -> None:
        """Reset the value of the Field object to its initial value."""
        self.value = ""

    def validate(self) -> None:
        """Validate the value of the Field object."""
        # Add your validation logic here
        pass

    def save(self) -> None:
        """Save the Field object to a database or file."""
        # Add your save logic here
        pass


if __name__ == "__main__":
    init()

    field = Field("example value")
    print(Fore.RED + field.__doc__ + Style.RESET_ALL)
    for name, func in field.__class__.__dict__.items():
        if callable(func):
            print(Fore.RED + name + Style.RESET_ALL)
            print(Fore.RED + func.__doc__ + Style.RESET_ALL)
