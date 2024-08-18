from .field import Field


class Address(Field):
    """Class for storing an address."""
    
    def __init__(self, value: str) -> None:
        """Initialize the Address field with a value.

        Args:
            value (str): The value of the Address field.

        Raises:
            ValueError: If the value is empty.
        """
        if not value:
            raise ValueError("Address field cannot be empty.")
        super().__init__(value)

    def __repr__(self) -> str:
        """Return a string representation of the Address field.

        Returns:
            str: The string representation of the Address field.
        """
        return f"{self.__class__.__name__}(value='{self.value}')"

    def __str__(self) -> str:
        """Return a string representation of the Address field.

        Returns:
            str: The string representation of the Address field.
        """
        return str(self.value)