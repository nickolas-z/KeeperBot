from AddressBook.tag import Tag
from AddressBook.field import Field
from colorama import Fore, Style


class Note(Field):
    """Class for storing a note."""

    def __init__(self, title: str, value: str = None) -> None:
        """Initialize the Name field with a value.

        Args:
            title (str): The title of the note.
            value (str): The note content.
            
        Raises:
            ValueError: If the title is empty.
        """
        if not title:
            raise ValueError(f"{Fore.RED}Name field cannot be empty.{Style.RESET_ALL}")

        self.title = title
        self.tags: list[Tag] = []
        super().__init__(value)

    def __repr__(self) -> str:
        """Return a string representation of the Name field.

        Returns:
            str: The string representation of the Name field.
        """
        return f"{self.__class__.__name__}(title='{self.title}', value='{self.value}')"
    
    def __str__(self) -> str:
        """Return a string representation of the Name field.

        Returns:
            str: The string representation of the Name field.
        """
        tags = ", ".join([str(tag) for tag in self.tags])
        result = f"Note: [{self.title}]: {self.value}"
        if tags:
            result += f"\nTags: {tags}"
        return result


if __name__ == "__main__":
    field = Note("example title")
    print(field.__doc__)
    for name, func in field.__class__.__dict__.items():
        if callable(func):
            print(name)
            print(func.__doc__)
